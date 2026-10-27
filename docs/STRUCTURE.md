# 仓库结构说明 / Repository Structure

本仓库同时承担两个角色，改动时请区分对待：

| 角色 | 路径 | 是否可自由调整 |
|------|------|----------------|
| **客户端契约** | 根目录的 `Box_Id.json`、`searchWord.json`、`guessNew_Box_Id.json`、`Version.json` | ❌ 不可移动、不可改结构 |
| **资料存档** | `image/`、`resource/`、`assets/` | ✅ 可整理 |

---

## 一、目录树

```
.
├── Box_Id.json            核心数据：盒号 → 盒信息 + 盒内干员 + 市价（94 盒）
├── Box_Index.json         轻量索引：列表/搜索/日历页用（约 10KB，由脚本生成）
├── searchWord.json        搜索词表：中文名 / 英文名 / 日文名 / 外号
├── guessNew_Box_Id.json   未官宣新盒的预测数据（字段与 Box_Id.json 一致）
├── Version.json           版本号与更新公告，客户端用于检查更新
├── README.md              使用说明与数据字段文档
├── LICENSE                 MIT（数据版权见文末）
├── docs/
│   ├── STRUCTURE.md        本文件
│   └── DATA_QUALITY.md     数据缺失清单与修复记录
├── scripts/
│   ├── validate.py         数据结构校验（CI 每次推送都会跑）
│   └── build_index.py      从 Box_Id.json 生成 Box_Index.json
├── .github/workflows/
│   └── validate.yml        推送/PR 自动校验结构与索引同步
├── assets/
│   ├── covers/             盒图素材（散落图片归位于此）
│   └── guide/              鉴别 / 说明类长图
├── image/                 音律联觉官方大图，按年份分目录（音律2021~2026）
└── resource/              早期开源数据副本（已停止更新，仅存档）
```

---

## 二、为什么根目录那几个 JSON 不能动

客户端把 URL **硬编码**在各页面里，例如：

```
https://raw.githubusercontent.com/awadwd/ArknightsAuthorization_Series-mirror/main/Box_Id.json
https://cdn.jsdelivr.net/gh/awadwd/ArknightsAuthorization_Series-mirror@main/Box_Id.json
https://raw.gitcode.com/huangjinzhou1/ArknightsAuthorization_Series/raw/main/Box_Id.json
```

一旦文件路径变化，已发布的小程序 / App / H5 会全部 404，且**无法通过服务端修复**，
只能等用户更新客户端。所以：

> **根目录四个 JSON 的路径是冻结的。**
> 需要新增文件请直接加在根目录，不要建子目录存放它们。

### 同理：`Box_Id.json` 内部结构也不能改

客户端有 20 多处按 `character${i}` 循环读取干员：

```js
for (let i = 1; i <= n; i++) {
  const charKey = `character${i}`;
  const c = box[charKey];
}
```

因此 `character1…character9` 的**键名形式、从 1 开始连续编号**是硬约束。
把它改成 `characters: []` 数组虽然更漂亮，但会让所有客户端当场失效。

同理还有两条：

- **`Box_id` 必须保持字符串**。`1.0` 若被写成数字会变成 `1`，与 `1.0` 匹配失败。
- **不能重排数组顺序**。新盒一律追加到数组末尾，是既有约定；重排会让 diff 变成全文件，
  也不利于「哪个盒是哪次加的」追溯。

---

## 三、能改什么

### 数据结构层面

允许的改动都是**向后兼容**的：

| 改动 | 是否安全 | 说明 |
|------|----------|------|
| 新增字段 | ✅ | 旧客户端会忽略未知字段 |
| 删除值为 `""` 的键 | ✅ | 客户端统一用 `if (x)` 判断，缺失与空串等价 |
| 补全缺失的字段值 | ✅ | 例如补 `barcode` |
| 把布尔改成 `"true"`/`"false"` 字符串 | ✅ | 客户端用 `=== 'true'` 严格比较，字符串才是对的 |
| 把 `characterN` 改成数组 | ❌ | 破坏 20+ 处解析 |
| 把 `Box_id` 改成数字 | ❌ | `1.0` → `1` |
| 重排数组顺序 | ⚠️ | 不破坏功能，但破坏追溯性 |
| 改字段名（如 `serachword` → `searchword`） | ❌ | 客户端拼写就是错的，改了反而失效 |

> `serachword` 是客户端既有的拼写，属于「已发布的数据契约」，**不要修正**。

### 资源层面

`assets/`、`image/`、`resource/` 可以自由整理，只要同步更新 README 里的引用。
`image/QRCode.jpg` 与 `image/wechatCode.jpg` 被 README 直接引用，移动时记得一起改。

---

## 四、修改数据的标准流程

```bash
# 1. 改 Box_Id.json（保持 1 空格缩进，便于看懂 diff）
# 2. 重新生成索引（否则 CI 报「索引不同步」）
python scripts/build_index.py

# 3. 本地校验
python scripts/validate.py

# 4. 提交
git add -A && git commit -m "data: 新增 56.0 盒"
git push
```

推送后 GitHub Actions 会自动再跑一遍校验，失败会标红。
