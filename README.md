# 方舟通行证谷子查询工具 · 数据仓库

**ArknightsAuthorization_Series-mirror**

明日方舟通行证（谷子）查询工具的数据仓库。为 uni-app 客户端（微信小程序 / H5 / App）提供盒号数据、干员数据、官方大图与版本信息。

> **Arknights Pass (Guzi) Query Tool — Data Repository**
> A data repository for the Arknights pass (merch) query tool, powering the uni-app client (WeChat Mini Program / H5 / App) with box data, operator data, official artwork and version info.

---

## 一、这是什么 / What Is This

「明日方舟通行证」是明日方舟朝陇山推出的周边盲盒产品（亚克力通行证）。由于官方并未提供公开的盒号与干员对照资料，本仓库承担两件事：

1. **数据源**：以 JSON 形式维护全量盒号 → 干员对照表、搜索词表、尚未官宣的新盒预测数据，供客户端在线拉取；
2. **数据开源**：将整理好的数据对外开放，任何开发者都可以在自己的工具中复用。

> The "Arknights Pass" is a blind-box acrylic merch line. Since no official box-to-operator index exists, this repo maintains the full mapping in JSON form for the client to fetch online, and open-sources the dataset for other developers.

> ⚠️ 本仓库**只存数据，不含客户端源码**。客户端源码为独立项目。

---

## 二、客户端能做什么 / Client Features

扫码体验（微信小程序）：

![小程序码](./image/QRCode.jpg) ![微信二维码](./image/wechatCode.jpg)

Scan to experience the project

客户端「方舟通行证谷子查询工具」首页为可自定义排序/隐藏的工具箱，当前包含：

| 工具 | 作用 |
|------|------|
| **通行证查询** | 按干员名查盒号，或按盒号查盒内干员 |
| **通行证列表** | 浏览全部通行证及盒内干员列表 |
| **模拟抽卡** | 模拟通行证抽卡 / 线下对战 |
| **我的收藏** | 查看已收藏的通行证与干员 |
| **通行证展柜** | 生成本人拥有的通行证展柜图，用于炫耀 / 出物发布 / 换物分享 |
| **条码扫描** | 扫描包装盒条码，快速定位盒号并点亮干员 |
| **今日宜挂** | 选个场景，看看今天适合挂谁的通行证 |
| **通行证日历** | 以日历形式查看各盒上线时间线 |
| **PRTS 帮查** | 接入 PRTS 的 AI 问答助手，可自然语言帮查（精度有限，仅供参考） |
| **设置** | 搜索方式、主题等个性化开关 |
| **关于我们** | 项目信息、贡献者名单、反馈渠道 |

| Tool | Description |
|------|-------------|
| Pass Search | Find boxes by operator, or operators by box |
| Pass List | Browse all passes and their operators |
| Gacha Simulator | Simulate blind-box drawing / offline battles |
| My Collection | View favourited passes and operators |
| Pass Showcase | Generate a showcase card of your collection for trade / display |
| Barcode Scan | Scan the box barcode to jump straight to its box number |
| Daily Recommend | Scenario-based daily "who to hang" recommendation |
| Pass Calendar | Timeline of every box release date |
| PRTS Assistant | AI Q&A lookup (low precision, for reference only) |
| Settings | Search modes, theme, and other preferences |
| About Us | Project info, contributors, feedback channels |

---

## 三、使用方法 / How to Use

### 3.1 两种查询路径 / Two Query Paths

- **按干员名查盒号**：输入干员名，得到该干员出现过的全部盒号，并可继续点开查看盒内其他角色。
- **按盒号查干员**：输入盒号（如 `1.0`、`54.0`、`前航远歌`），列出该盒包含的全部干员及其市价。

### 3.2 支持的搜索方式 / Supported Search Modes

在「设置」中可分别开关：

| 搜索方式 | 说明 | 数据字段 | 默认 |
|----------|------|----------|------|
| 中文名 | 阿米娅、棘刺、风笛…… | `name` | 开 |
| 英文名 | Amiya、Exusiai…… | `englishname` | 开 |
| 日文名 | 字段已预留，待数据补齐 | `japanesename` | 关 |
| 外号 / 别名 | 兔兔（阿米娅）、鸡精（极境）……，仅部分干员有 | `serachword` | 开 |

> English name and nickname search are configurable in Settings. The Japanese name field is reserved but not yet populated.

### 3.3 盒号格式 / Box ID Format

盒号是**字符串**，不是数字，常见三类：

- **数字序列盒**：`1.0` ~ `54.0`（共 54 盒），常规周边盒
- **音律联觉系列**：以中文名命名，如 `前航远歌`、`象限解构者`、`嘉年华2026`
- **联动 / 特别 / 白名单**：如 `战术交汇`（联动）、`特别通行认证`、`白名单凭证1.0`

> ⚠️ 使用 JSON 时请勿把 `Box_id` 当作 Number 解析，`1.0` 会被解析为 `1`，导致匹配失败。

### 3.4 条码扫描 / Barcode Scan

包装盒背面条码与盒号一一对应，数据存于 `barcode` / `barcodes` 字段（`barcodes` 为数组，用于一个盒号对应多条码的情况）。扫描后可直接定位盒号并标记已拥有的干员。

---

## 四、数据文件说明 / Data Files

| 文件 | 说明 | 当前规模 |
|------|------|----------|
| `Box_Id.json` | **核心数据**：盒号 → 盒信息 + 盒内干员 + 市价 | 93 盒 / 581 条角色记录 |
| `searchWord.json` | 搜索词表：中文名 / 英文名 / 日文名 / 外号 | 418 条 |
| `guessNew_Box_Id.json` | 官方未发布的新盒预测数据（字段与 `Box_Id.json` 一致） | 1 盒 |
| `Version.json` | 版本号与更新公告，客户端用于检查更新、弹公告 | 1 条 |
| `image/` | 官方大图（音律联觉系列分年份存放于 `image/音律2021`~`音律2026`） | —— |
| `resource/` | 早期开源数据副本 | 85 盒 |
| `通行证鉴假指南.png` | 通行证真伪鉴别指南 | —— |

### 4.1 `Box_Id.json`

数组，每个元素为一个盒。**盒级字段**：

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `Box_id` | 字符串 | 盒号 | `1.0` |
| `release_date` | 字符串 | 首发日期 | `2020/05/01` |
| `replicate_date` | 字符串 | 复刻日期（部分盒有） | `2021/10/19` |
| `replicate_date_01` | 字符串 | 二次复刻日期（极少） | `2023/5/26` |
| `size` | 字符串 | 实物尺寸 | `约5*10cm` |
| `material` | 字符串 | 材质 | `亚克力、涤纶` |
| `retail_price` | 字符串 | 官方抽价 | `25元/抽` |
| `type` | 字符串 | 是否常规款 | `"true"` / `"false"` |
| `replicate` | 字符串 | 是否已复刻 | `"true"` / `"false"` |
| `Box_type` | 字符串 | 盒类型：`ambience`（音律）/ `cooperation`（联动）/ `special`（特别）/ `whitelist`（白名单） | `ambience` |
| `Box_ImageUrl` | 字符串(URL) | 官方大图 | —— |
| `barcode` | 字符串 | 主条码 | `6972643691935` |
| `barcodes` | 数组 | 全部条码（含复刻版） | `["6972643691935"]` |
| `character1`…`character9` | 对象 | 盒内第 N 个干员，最多 9 个 | —— |

**角色字段**（`characterN` 对象内）：

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `name` | 字符串 | 干员名称 | `阿米娅` |
| `imageUrl` | 字符串(URL) | 干员头像 | —— |
| `market_price` | 对象 | 市价，`ELITE1` / `ELITE2` 两档 | `{"ELITE1":100,"ELITE2":112}` |
| `hotcharacter` | 布尔值 | 热门标记（有则出现） | `true` |
| `nolyELITE1` | 布尔值 | 仅有精一版标记（有则出现） | `true` |

### 4.2 `searchWord.json`

数组，每项形如 `{"characterN": {...}}`，字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | 字符串 | 干员中文名 |
| `englishname` | 字符串 | 英文名 |
| `japanesename` | 字符串 | 日文名（当前为空，预留） |
| `serachword` | 数组 | 外号 / 别名（注意字段名原文即为 `serachword`） |

### 4.3 `Version.json`

```json
{
  "fields": ["url", "Version", "notice", "created_at", "updated_at", "created_by", "id", "_read_perm", "_write_perm"],
  "data": [ { "url": "...", "Version": "v1.9.2.2", "notice": "更新公告全文", ... } ]
}
```

---

## 五、数据接入 / Data Access

### 5.1 CDN 镜像

客户端按以下顺序做多源回退，国内访问推荐优先使用 jsDelivr / GitCode。以下以 `Box_Id.json` 为例（把文件名换成 `searchWord.json` 即可取到搜索词表）：

| 源 | 地址 |
|----|------|
| jsDelivr (CDN) | `https://cdn.jsdelivr.net/gh/awadwd/ArknightsAuthorization_Series-mirror@main/Box_Id.json` |
| GitHub Raw | `https://raw.githubusercontent.com/awadwd/ArknightsAuthorization_Series-mirror/main/Box_Id.json` |
| GitCode 镜像 | `https://raw.gitcode.com/huangjinzhou1/ArknightsAuthorization_Series/raw/main/Box_Id.json` |

### 5.2 调用示例

```javascript
const REPO = 'awadwd/ArknightsAuthorization_Series-mirror';
const src = `https://cdn.jsdelivr.net/gh/${REPO}@main/Box_Id.json`;

const boxes = await fetch(src).then(r => r.json());

// 按干员名查盒号
const found = boxes.filter(b =>
  Object.keys(b)
    .filter(k => k.startsWith('character'))
    .some(k => b[k].name === '阿米娅')
).map(b => b.Box_id);

// 按盒号查干员（注意 Box_id 一律按字符串比较）
const box = boxes.find(b => b.Box_id === '1.0');
```

### 5.3 数据现状 / Dataset Stats

| 指标 | 数值 |
|------|------|
| 盒号总数 | **93**（数字盒 54 + 音律 30 + 联动 5 + 特别 2 + 白名单 2） |
| 角色记录条目 | **581**（去重干员名 432） |
| 带市价的角色 | 580（`ELITE1` 580 / `ELITE2` 553） |
| 热门标记 / 仅精一标记 | 105 / 31 |
| 有复刻日期的盒 | 39（含 4 盒二次复刻） |
| 首发日期跨度 | 2020/05/01 ~ 2026/09/08 |
| 搜索词条目 | 418（全部含英文名，92 条含外号） |

---

## 六、版本更新 / Latest Release Notes

当前数据版本：**v1.9.2.2**

1. 新增了 1.0~52.0 中有复刻且有记录的复刻日期时间；
2. 新增了部分有多次复刻记录的信息；
3. 修复未下载数据会导致模拟抽卡闪退的问题；
4. AI 帮查页面焕新；
5. 修复已下载英文搜索词后仍会弹出推荐下载提示框的问题。

**Latest Version Update Notes:**

1. Added replication dates for boxes 1.0–52.0 that have both records and reprints.
2. Added information for boxes with multiple reprint records.
3. Fixed a crash in the gacha simulator caused by missing downloaded data.
4. Refreshed the AI lookup page.
5. Fixed the redundant download prompt appearing after English search words were already downloaded.

> 完整公告以 `Version.json` 中的 `notice` 字段为准。

---

## 七、反馈与贡献 / Feedback & Contributing

- **数据纠错 / 补录**：欢迎通过客户端的「帮助我们完善工具」问卷或「数据反馈」入口提交；
- **反馈群**：QQ 群 `128568825`；工具反馈交流 QQ 频道号 `pd46148437`；
- **参与开发**：欢迎有开发能力的博士通过客户端「关于我们」页面联系，或直接提交 PR。

> Bug reports and data corrections are welcome via the in-app feedback entry, the QQ group `128568825`, or the QQ channel `pd46148437`. Pull requests are welcome.

---

## 八、版权声明 / Copyright Notice

程序所涉及的公司名称、商标、产品等均为其各自所有者的资产，仅供识别。程序内使用的商品图片、游戏图片、动画、音频、文本原文，仅用于更好地表现游戏及商品资料，其版权属于 Arknights/上海鹰角网络科技有限公司及明日方舟朝陇山/上海木鸢网络科技有限公司。

除非另有声明，本仓库其他内容采用**知识共享 署名-非商业性使用 4.0 国际（CC BY-NC 4.0）**许可协议进行许可。未经许可不得将本仓库内容或由其衍生作品用于商业目的。

The company names, trademarks, and products mentioned in the program are the assets of their respective owners and are used solely for identification purposes. The product images, game images, animations, audio, and textual content used within the program are solely for the purpose of better representing the game and product materials, and their copyrights belong to Arknights / Shanghai Hypergryph Network Technology Co., Ltd. and Tomorrow's Ark Chaolong Mountain / Shanghai Muyuan Network Technology Co., Ltd.

Unless otherwise stated, the remaining content of this repository is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license. The content of this repository or any derivative works thereof may not be used for commercial purposes without permission.
