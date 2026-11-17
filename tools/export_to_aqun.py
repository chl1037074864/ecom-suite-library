#!/usr/bin/env python3
"""把本库中的一套套图，转成阿群工作台可用的「类型组合 + 额外需求」。

用法：
    python tools/export_to_aqun.py --id suite-muying-baobaoyujin
    python tools/export_to_aqun.py --search 浴巾 --limit 5

输出（stdout）：
    {
      "suite": {...},
      "aqun": {
        "mainTypes": ["white-bg", "sell-point", "scene-main"],
        "detailTypes": ["poster", "scene-detail", "detail-macro"],
        "extraRequirement": "第1张：白底主图，突出六层纱布堆叠形态…",
        "note": "阿群没有分镜概念，这里把 8 镜压成类型组合 + 逐张说明"
      }
    }
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.json")

# EcomGen shotRole -> 阿群类型（id 以阿群 3.9.20 为准）
ROLE_MAP = {
    "HERO": ("mainTypes", "sell-point"),
    "PAIN_POINT": ("mainTypes", "scene-main"),
    "COMPARISON": ("mainTypes", "comparison"),
    "SCENE": ("mainTypes", "scene-main"),
    "DETAIL": ("mainTypes", "detail-close"),
    "TRUST": ("detailTypes", "certificate"),
    "VARIANT": ("mainTypes", "variant"),
    "CTA": ("detailTypes", "poster"),
    "SIZE": ("mainTypes", "dimension"),
}


def load_index():
    with open(INDEX, encoding="utf-8") as f:
        return json.load(f)


def find(idx, sid=None, kw=None, limit=5):
    items = idx["items"]
    if sid:
        return [i for i in items if i["id"] == sid]
    if kw:
        out = []
        for i in items:
            blob = " ".join([i.get("name") or "", i.get("leaf") or "", " ".join(i.get("kw") or [])])
            if kw in blob:
                out.append(i)
        return out[:limit]
    return items[:limit]


def export(item):
    with open(os.path.join(ROOT, item["path"]), encoding="utf-8") as f:
        suite = json.load(f)

    main, detail, lines = [], [], []
    for n, shot in enumerate(suite["shots"], 1):
        role = shot.get("role") or "HERO"
        bucket, type_id = ROLE_MAP.get(role, ("mainTypes", "sell-point"))
        (main if bucket == "mainTypes" else detail).append(type_id)
        intent = (shot.get("intent") or "").strip()
        lines.append("第%d张（%s）：%s" % (n, role, intent))

    def uniq(seq):
        seen, out = set(), []
        for x in seq:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    return {
        "suite": {k: suite.get(k) for k in ("id", "name", "l1", "l2", "leaf", "shots")},
        "aqun": {
            "mainTypes": uniq(main),
            "detailTypes": uniq(detail),
            "extraRequirement": "\n".join(lines),
            "note": "阿群没有分镜概念，这里把 %d 镜压成类型组合 + 逐张说明" % len(suite["shots"]),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id")
    ap.add_argument("--search")
    ap.add_argument("--limit", type=int, default=5)
    a = ap.parse_args()

    hits = find(load_index(), a.id, a.search, a.limit)
    if not hits:
        print(json.dumps({"ok": False, "error": "not found"}, ensure_ascii=False))
        return
    result = [export(h) for h in hits] if a.search else export(hits[0])
    print(json.dumps({"ok": True, "data": result}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
