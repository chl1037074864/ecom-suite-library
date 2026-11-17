# 电商套图库（阿群工作台可用）

把 [EcomGen](https://github.com/linbei0/EcomGen) 的 **1,173 套电商详情页分镜脚本**整理成精简、可按类目检索的外部库，供阿群工作台扩展（侧车）调用。

- 源仓库：`linbei0/EcomGen`（MIT），commit `894e7fb62d50eb8f1f79959cadba97bb791bdc03`
- 原始路径：`packages/ecom-suite/src/suites/`
- 本库形态：**精简版**（每套只保留阿群能用的字段），26.8 KB → 约 4.3 KB/套

---

## 目录

```
.
├─ index.json                 # 1173 条索引（类目/子类/套名/镜数/关键词/路径）
├─ suites-slim/
│  ├─ muying/                 # 母婴（176）
│  ├─ meizhuangcaizhuang/     # 美妆彩妆（43）
│  ├─ hufugehu/               # 护肤个护（140）
│  ├─ jiajuriyong/            # 家居日用（120）
│  ├─ jiajujiafang/           # 家具家纺（49）
│  ├─ chongwuyongpin/         # 宠物用品（56）
│  ├─ shoujishuma/            # 手机数码（52）
│  ├─ wanju/                  # 玩具（25）
│  └─ …                       # 其余类目
├─ PROVENANCE.json            # 来源、commit、抓取时间、处理规则
├─ tools/export_to_aqun.py    # 把某一套转成阿群"类型组合 + 额外需求"
└─ LICENSE                    # MIT（来自 EcomGen）
```

## 怎么调用

公开仓库下三种取法（按国内可用性排序）：

```bash
# 1) jsDelivr CDN（国内最快，带缓存）
https://cdn.jsdelivr.net/gh/<USER>/<REPO>@main/index.json
https://cdn.jsdelivr.net/gh/<USER>/<REPO>@main/suites-slim/muying/0517-muying-baobaoyujin.json

# 2) raw.githubusercontent
https://raw.githubusercontent.com/<USER>/<REPO>/main/index.json

# 3) GitHub Pages（在仓库 Settings → Pages 选 main 分支根目录）
https://<USER>.github.io/<REPO>/index.json
```

私有仓库时，侧车带 PAT 走 API：

```bash
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/<USER>/<REPO>/contents/index.json
```

## 数据结构

`index.json`：

```json
{
  "schema": "aqun-ecom-suite-index/1",
  "total": 1173,
  "categories": {"母婴": 176, "美妆彩妆": 43},
  "items": [
    {
      "id": "suite-muying-baobaoyujin",
      "slug": "muying",
      "l1": "母婴", "l2": "洗护", "leaf": "六层泡泡纱婴儿浴巾",
      "name": "六层泡泡纱婴儿浴巾款",
      "shots": 8,
      "kw": ["婴儿浴巾", "六层纱布", "吸水速干"],
      "path": "suites-slim/muying/0517-muying-baobaoyujin.json"
    }
  ]
}
```

单套精简文件：

```json
{
  "id": "suite-muying-baobaoyujin",
  "name": "六层泡泡纱婴儿浴巾款",
  "l1": "母婴", "l2": "洗护", "leaf": "六层泡泡纱婴儿浴巾",
  "desc": "六层柔纱加厚吸水，透气亲肤…",
  "kw": ["婴儿浴巾", "六层纱布", "吸水速干"],
  "style": {"direction": "soft pastel baby-care…", "palette": [...], "temperature": "warm"},
  "shots": [
    {"role": "HERO", "intent": "搜索首图一眼看清产品形态与粉彩色系…", "textZone": "none", "ratio": "2:3", "ref": true}
  ]
}
```

## 精简规则

保留：`id / name / l1 / l2 / leaf / kw / desc / styleLock / 每镜(role,intent,textZone,ratio,ref)`
丢弃：`camera / lighting / background / props / productOccupancy / whitespace / negativePrompt / promptTemplate / resolution / provenance`（阿群没有对应参数槽位）

## 许可与归属

- 本库数据来自 `linbei0/EcomGen`，遵循 **MIT**，保留原 `LICENSE` 与版权声明。
- EcomGen 的模板上游来源见其 `packages/ecom-skill/UPSTREAM.md`（`liangdabiao/ecom-details-image`）。
- 二次分发请保留本 README 与 `PROVENANCE.json` 中的来源与 commit 记录。
