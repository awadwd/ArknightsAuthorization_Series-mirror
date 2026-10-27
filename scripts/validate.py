#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据仓库校验脚本
================
用法：
    python scripts/validate.py            # 校验仓库根目录下的数据文件
    python scripts/validate.py --strict   # 把「缺失数据」也当作错误

校验项：
  1. 文件可解析、顶层类型正确
  2. Box_Id.json 盒级必填字段齐全、类型正确
  3. character1..characterN 键位连续（不能出现 character1、character3 这种空洞）
  4. 盒号唯一（Box_id 是字符串，避免 1.0 被当成数字 1）
  5. 条码唯一、barcode 必须出现在 barcodes 中
  6. 日期格式统一为 YYYY/MM/DD，且可解析
  7. market_price 为 {ELITE1:int, ELITE2:int}
  8. Box_Index.json 与 Box_Id.json 同步（盒号集合、数量一致）
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE_RE = re.compile(r"^(\d{4})/(\d{1,2})/(\d{1,2})$")
DATE_FIELDS = ["release_date", "replicate_date"] + ["replicate_date_%02d" % i for i in range(1, 6)]
BOX_TYPES = {"normal", "ambience", "cooperation", "special", "whitelist", ""}
MAX_CHAR = 9

errors, warns = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warns.append(msg)


def load(name):
    p = os.path.join(ROOT, name)
    if not os.path.exists(p):
        err("缺少文件: %s" % name)
        return None
    try:
        return json.loads(io.open(p, "r", encoding="utf-8-sig").read())
    except Exception as e:
        err("%s 解析失败: %s" % (name, e))
        return None


def check_box(b, seen_ids, seen_barcodes):
    bid = b.get("Box_id")
    if not isinstance(bid, str) or not bid.strip():
        err("存在 Box_id 非字符串或为空的条目: %r" % (bid,))
        return
    if bid in seen_ids:
        err("Box_id 重复: %s" % bid)
    seen_ids.add(bid)

    # 必填
    for k in ("Box_id", "size", "material", "retail_price", "type", "replicate", "Box_ImageUrl"):
        if k not in b:
            err("%s 缺少必填字段 %s" % (bid, k))

    # 布尔型字段必须是字符串 "true"/"false"
    for k in ("type", "replicate"):
        if k in b and b[k] not in ("true", "false"):
            err("%s.%s 必须是字符串 \"true\"/\"false\"，实际 %r" % (bid, k, b[k]))

    # 日期
    for k in DATE_FIELDS:
        v = b.get(k)
        if v in (None, ""):
            continue
        m = DATE_RE.match(str(v))
        if not m:
            err("%s.%s 日期格式应为 YYYY/MM/DD，实际 %r" % (bid, k, v))
            continue
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if not (1 <= mo <= 12 and 1 <= d <= 31):
            err("%s.%s 日期非法: %s" % (bid, k, v))

    if not b.get("release_date"):
        warn("%s 缺少 release_date（日历页不会显示）" % bid)

    # Box_type
    if b.get("Box_type") and b["Box_type"] not in BOX_TYPES:
        warn("%s.Box_type 未知取值: %r" % (bid, b["Box_type"]))

    # 干员：键位连续
    chars, idxs = [], []
    for k in b:
        m = re.match(r"^character(\d+)$", k)
        if m:
            idxs.append(int(m.group(1)))
            chars.append(b[k])
    if idxs:
        idxs.sort()
        if idxs != list(range(1, len(idxs) + 1)):
            err("%s 干员键位不连续: character%s" % (bid, idxs))
        if max(idxs) > MAX_CHAR:
            warn("%s 干员数 %d 超过文档上限 %d" % (bid, max(idxs), MAX_CHAR))
    else:
        err("%s 没有任何 characterN 干员" % bid)

    names = set()
    for c in chars:
        if not isinstance(c, dict):
            err("%s 的 characterN 不是对象" % bid)
            continue
        n = c.get("name")
        if not n:
            err("%s 有干员缺少 name" % bid)
        elif n in names:
            err("%s 干员重名: %s" % (bid, n))
        else:
            names.add(n)
        if not c.get("imageUrl"):
            warn("%s / %s 缺少 imageUrl" % (bid, n))
        mp = c.get("market_price")
        if mp is None:
            warn("%s / %s 缺少 market_price" % (bid, n))
        elif not isinstance(mp, dict):
            err("%s / %s market_price 不是对象" % (bid, n))
        else:
            for ek in ("ELITE1", "ELITE2"):
                if ek not in mp:
                    warn("%s / %s market_price 缺 %s" % (bid, n, ek))
                elif not isinstance(mp[ek], (int, float)) or isinstance(mp[ek], bool):
                    err("%s / %s market_price.%s 必须是数字" % (bid, n, ek))

    # 条码
    codes = b.get("barcodes")
    if codes is not None:
        if not isinstance(codes, list):
            err("%s.barcodes 必须是数组" % bid)
            codes = []
        for c in codes:
            if not isinstance(c, str) or not c.strip():
                err("%s.barcodes 含非法条码: %r" % (bid, c))
                continue
            if c in seen_barcodes:
                err("条码重复: %s（%s 与之前某盒）" % (c, bid))
            seen_barcodes.add(c)
        single = b.get("barcode")
        if single and single not in codes:
            err("%s.barcode (%s) 不在 barcodes 中" % (bid, single))
    elif b.get("barcode"):
        warn("%s 有 barcode 但缺 barcodes 数组" % bid)
    if not codes and not b.get("barcode"):
        warn("%s 缺少条码（扫码无法定位）" % bid)


def main():
    strict = "--strict" in sys.argv

    boxes = load("Box_Id.json")
    if boxes is not None:
        if not isinstance(boxes, list):
            err("Box_Id.json 顶层必须是数组")
        else:
            ids, bcs = set(), set()
            for b in boxes:
                if isinstance(b, dict):
                    check_box(b, ids, bcs)
                else:
                    err("Box_Id.json 存在非对象元素")
            print("Box_Id.json: %d 盒" % len(boxes))

    for name in ("searchWord.json", "guessNew_Box_Id.json"):
        d = load(name)
        if d is None:
            continue
        if not isinstance(d, list):
            err("%s 顶层必须是数组" % name)
        else:
            print("%s: %d 条" % (name, len(d)))

    version = load("Version.json")
    if isinstance(version, dict):
        rows = version.get("data")
        if not isinstance(rows, list) or not rows:
            err("Version.json.data 必须是非空数组")
        else:
            for r in rows:
                if not r.get("Version"):
                    err("Version.json 有条目缺 Version")
            print("Version.json: %d 条，当前 %s" % (len(rows), rows[0].get("Version")))

    # 索引同步
    index = load("Box_Index.json")
    if isinstance(index, list) and isinstance(boxes, list):
        a = [b.get("Box_id") for b in boxes]
        b_ = [i.get("Box_id") for i in index]
        if a != b_:
            err("Box_Index.json 与 Box_Id.json 不同步（顺序或盒号不一致，请重新运行 scripts/build_index.py）")
        else:
            print("Box_Index.json: %d 盒（已同步）" % len(index))

    print("\n" + "=" * 56)
    if warns:
        print("警告 %d 条：" % len(warns))
        for w in warns:
            print("  ! " + w)
    if errors:
        print("错误 %d 条：" % len(errors))
        for e in errors:
            print("  x " + e)
        print("\n校验失败")
        return 1
    if strict and warns:
        print("\n--strict 模式下警告视为失败")
        return 1
    print("\n校验通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
