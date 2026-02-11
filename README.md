# ArknightsAuthenticationAssistant

明日方舟通行证查询工具小助手，使用Uni-app开发，目前已上线微信小程序版本；明日方舟通行证是明日方舟朝陇山研发的一款周边产品，一般是盲盒亚克力制品本程序对该产品的分盒、信息、抽取、干员信息可以进行查询

![image](./image/QRCode.jpg) ![image](./image/wechatCode.jpg)<br>                        免下载扫码体验本项目 Scan to experience this project<br>

本项目的角色干员信息（Box_Id.json)和搜索词数据(searchWord.json）以及猜测的官方未发布的新盒通行证猜测数据（guessNew_Box_Id.json)均是在resource中开源<br>

数据最新版本更新日志如下：<br>1.所有有在第三方app中拥有记录的【常规款】、【联动款】的干员通行证市价已全部上线<br>2.优化了调整了部分音律联觉系列的官方大图<br>3.特别款的设定集赠品“博士”通行证与愚人节整合运动系列的通行证分离<br>4.优化和调整了部分角色的烫度标记，新增及删除了部分角色的烫度标记<br>

The Lastest Version Update Notes:

1. The market prices of all operator passes, including those for "regular" and "联动款" models, which have records in third-party apps, have been fully listed online
2. Optimized and adjusted some official large images of the tonal synesthesia series
3. The special set gift "Doctor" pass is separate from the pass for the April Fools' Day integrated campaign series
4. Optimized and adjusted the heat level markers for some characters, and added and removed heat level markers for other characters

版权声明：程序所涉及的公司名称、商标、产品等均为其各自所有者的资产，仅供识别。程序内使用的商品图片、游戏图片、动画、音频、文本原文，仅用于更好地表现游戏及商品资料，其版权属于 Arknights/上海鹰角网络科技有限公司及明日方舟朝陇山/上海木鸢网络科技有限公司。<br>除非另有声明，程序其他内容采用知识共享 署名-非商业性使用 4.0 国际 许可协议进行许可。未经许可不得将本程序内容或由其衍生作品用于商业目的。<br>

Copyright Notice:The company names, trademarks, and products mentioned in the program are the assets of their respective owners and are used solely for identification purposes. The product images, game images, animations, audio, and textual content used within the program are solely for the purpose of better representing the game and product materials, and their copyrights belong to Arknights/Shanghai Yingjiao Network Technology Co., Ltd. and Tomorrow's Ark Chaolong Mountain/Shanghai Muyuan Network Technology Co., Ltd. Unless otherwise stated, the remaining content of the program is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. The content of this program or any derivative works thereof may not be used for commercial purposes without permission



参数调用类型说明
| 参数名称  | 用途 | 类型 | 注意事项 | 示例 |
|--|--|--|--|--|
| "Box_id" | 通行证盒号，一般是1.0、2.0 ..<br>音律、特殊盒除外| 字符串 | 注意不要用于Number类型 | 1.0|
| "Box_ImageUrl" | 通行证盒号的官方大图<br>数据源于Bilibili| 字符串(Url链接) |  |【链接】 |
|  "characterX" | 角色数据 | 数组 |  |
| "name" | 角色名称 | 字符串 |   | 阿米娅 |
|"imageUrl" | 角色头像 | 字符串(Url链接) |   |【链接】|
|"nolyELITE1"| 角色仅精一标记|布尔值 | |True|
|"hotcharacter"|角色热门标记| 布尔值 | | False|
|持续更新...|