# 诗径 · 走到诗里

一款「地理位置触发古诗词」的 PWA 体验原型：在杭州西湖沿线的真实山水中行走，走到某处点位，便弹出当年文人在**同一处**写下的诗句——还原「站在同一块石头上」的时空重叠感。

## 理念

- **位置触发，不是搜索**：走到了，它自己浮现，而非主动查询。
- **内容考据是魂**：只收 A/B 级——A 为确指此地此景此事、文献可考；B 为确与此地相关但非专为此点而作，卡片须注明性质。查不到确指文献的点位，宁可留白不触发。
- **诚实标注**：每条诗文附文献出处与考据说明；坐标标注 `coord_source`（osm / field / estimate），estimate 点在地图上用空心虚线圈标识，正式上线前须实地打点校准。

## 已建诗径（5 条 · 23 触发点）

| 诗径 | 数据文件 | 点数 | 模式 | 代表内容 |
|------|----------|------|------|----------|
| 古龙井 · 风篁岭 | `data/poems.json` | 4 | 连线 | 秦观《龙井题名记》、苏轼《次辩才韵》、米芾《方圆庵记》 |
| 孤山 · 白堤 | `data/trail-gushan.json` | 6 | 连线 | 白居易《钱塘湖春行》、林逋《山园小梅》、苏小小、秋瑾 |
| 灵隐 · 天竺 | `data/trail-lingyin.json` | 3 | 连线 | 宋之问《灵隐寺》、白居易《冷泉亭记》、韬光 |
| 钱塘江畔 | `data/trail-qiantang.json` | 4 | 连线 | 有美堂、凤凰山、六和塔、钱塘观潮 |
| 西湖 · 名胜诗签 | `data/trail-xihu-scatter.json` | 6 | 散点 | 望湖楼、净慈寺、雷峰塔、苏堤、岳王庙 + 城市开篇三声部 |

坐标概况：osm 核验 16 点 · estimate 待测 7 点 · 实地半径核验 0 点。`c4` 有美堂在钱塘诗径与名胜诗签中共用。

考据文档见 `research/`（分区考据 + `INDEX-杭州诗词点位总索引.md`）。

## 技术

- **架构**：`index.html` 主应用 + `data/*.json` 内容库，无后端
- **地图**：Leaflet + CartoDB Voyager 无字底图（WGS-84），叠宣纸滤镜
- **定位**：Geolocation API + haversine 地理围栏；坐标统一存 WGS-84，不做 GCJ-02 偏移
- **诗径连线**：本地 Catmull-Rom 样条平滑；散点模式（`layout: scatter`）不连线
- **PWA**：`manifest.json` + `sw.js` 离线缓存（壳层、数据、地图瓦片）
- **实地校准**：`survey.html` 打点台 + 卡片内嵌校准面板，支持 GitHub Contents API 一键提交坐标
- **分发**：`start.html` 扫码入口页（实地测试用）

## 项目结构

```
index.html          # 主应用
start.html          # 扫码上路入口
survey.html         # 实地打点校准器
sw.js / manifest.json
data/*.json         # 诗径内容库
research/           # 考据文档（标准、分区、总索引）
preview/            # 诗径解说短片 HTML 预览（GitHub Pages）
gen_qr.py           # 生成扫码二维码
gen_icons.py        # 生成 PWA 图标
export_xlsx.py      # 导出考据表格
```

## 本地运行

```bash
python3 -m http.server 8770
# 浏览器打开 http://localhost:8770
# 实地测试分发页：http://localhost:8770/start.html
```

手机实地体验：访问 `start.html` 扫码，添加到主屏幕后以 PWA 模式运行。

## 当前阶段

**实地测试版原型**——核心体验闭环已跑通，下一步重点是 estimate 坐标实地打点、待落 JSON 的 6 个考据点补齐、诗文纸本终校。详见 `research/INDEX-杭州诗词点位总索引.md` 第三节。
