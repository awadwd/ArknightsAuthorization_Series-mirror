#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从 Box_Id.json 生成 Box_Index.json
====================================
列表页 / 搜索页 / 日历页只需要「盒号 + 日期 + 盒内干员名」，
用这个索引可以让首屏请求从 163KB 降到 10KB 左右（约 6%）。

用法：
    python scripts/build_index.py

生成后会打印体积对比。修改 Box_Id.json 之后请重新运行，
否则 CI 的 validate.py 会报「索引不同步」。
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Box_Id.json")
DST = os.path.join(ROOT, "Box_Index.json")
MAX_CHAR = 9


def main():
    data = json.loads(io.open(SRC, "r", encoding="utf-8-sig").read())
    index = []
    for b in data:
        names = []
        for i in range(1, MAX_CHAR + 1):
            c = b.get("character%d" % i)
            if isinstance(c, dict) and c.get("name"):
                names.append(c["name"])
        index.append({
            "Box_id": b.get("Box_id"),
            "release_date": b.get("release_date", ""),
            "Box_type": b.get("Box_type", ""),
            "replicate": b.get("replicate", "false"),
            "Box_ImageUrl": b.get("Box_ImageUrl", ""),
            "characters": names,
        })

    s = json.dumps(index, ensure_ascii=False, separators=(",", ":"))
    io.open(DST, "w", encoding="utf-8", newline="\n").write(s + "\n")

    full = os.path.getsize(SRC)
    idx = os.path.getsize(DST)
    print("Box_Id.json   %7d 字节  %d 盒" % (full, len(data)))
    print("Box_Index.json %6d 字节  %d 盒  (%.1f%%)" % (idx, len(index), 100.0 * idx / full))
    return 0


if __name__ == "__main__":
    sys.exit(main())
