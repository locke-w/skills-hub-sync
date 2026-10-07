#!/usr/bin/env python3
"""auto-xhs 阶段 1：character.json → character_profile.md + prompts.md + prompts.json

用法:
  render_character.py <character.json|char_dir|编号>   渲染单个人物（覆盖 profile/prompts）
  render_character.py --all-batch [DIR...]             批量渲染（缺省 = MATERIAL 下所有含 character.json 的人物）

不会改动 ASSET 下已有图片；只确保 ASSET/<char_dir>/ 目录存在。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import library as L  # noqa: E402

AVOID00 = ("English text, letters, anime, cartoon, 3d render, CGI, doll, figurine, plastic skin, "
           "beauty filter, western features, youthful face, deformed hands")
AVOID01 = ("English text, letters, real living human, skin pores, plaster, stone column, room, "
           "furniture, outdoor scenery, western features, youthful face, deformed hands")
SCENE_AVOID = ("English text, letters, watermark, anime, cartoon, CGI look, cheap toy plastic shine, "
               "western features, youthful face, deformed hands, extra fingers, missing fingers, "
               "floating objects, broken geometry")


def is_full(c: dict) -> bool:
    return c["posture"] in ("FW", "FM")


def spec_line(c: dict, cfg: dict) -> str:
    if is_full(c):
        return f"全身 (Full-body) · {cfg['prompt']['full_cm']}"
    return f"胸像 (Bust) · {cfg['prompt']['bust_cm']}"


def prompt_00(c: dict) -> str:
    if is_full(c):
        body = (f"Candid documentary full-body portrait photograph of a real {c['ifts']}, "
                f"full-body view from head to feet, {c['setting']}, wearing {c['cloth']}, {c['light00']}")
    else:
        body = (f"Candid documentary portrait photograph of a real {c['ifts']}, "
                f"Keep the upper body, {c['setting']}, wearing {c['cloth']}, {c['light00']}")
    return (f"Square 1:1 composition. {body}. Shot on Hasselblad 90mm f/3.2, "
            f"Kodak Portra 400 film grain. Avoid: {AVOID00}.")


def prompt_01(c: dict, cfg: dict) -> str:
    if is_full(c):
        body = (f"Macro studio product photo of a {cfg['prompt']['full_cm']} 3D printed painted resin "
                f"full-body model, full-body view, {c['ifts']}, sculpted {c['cloth01']}, "
                f"full-body standing on a weighted circular base")
    else:
        body = (f"Macro studio product photo of a {cfg['prompt']['bust_cm']} 3D printed painted resin "
                f"bust, Keep the upper body, {c['ifts']}, sculpted {c['cloth01']}, "
                f"mounted on a dark beveled pedestal base")
    return (f"Square 1:1 composition. {body}, subtle resin SSS finish, light gray cyclorama, "
            f"softbox lighting. Shot on RF 100mm f/8. Avoid: {AVOID01}.")


def scene_prompt(cfg: dict, slot: str, s: dict) -> str:
    extra = C.cfg_get(cfg, "prompt.slot_extra", {}).get(slot)
    avoid = SCENE_AVOID + (", " + extra if extra else "")
    cover = C.cfg_get(cfg, "prompt.cover_cue", "") + " " if slot in cfg["generation"]["cover_candidates"] else ""
    return (f"{cfg['prompt']['scene_cue']} {s['en']} {cover}"
            f"Shot on {s['shot']}. Avoid: {avoid}.")


def render_prompts(cfg: dict, c: dict) -> str:
    slot_names = cfg["generation"]["slot_names"]
    covers = cfg["generation"]["cover_candidates"]
    p00, p01 = prompt_00(c), prompt_01(c, cfg)
    full = is_full(c)
    frame00 = ("`Candid documentary full-body portrait photograph of a real` … `full-body view`" if full
               else "`Candid documentary portrait photograph of a real` … `Keep the upper body`")
    frame01 = (f"`Macro studio product photo of a {cfg['prompt']['full_cm']} 3D printed painted resin full-body model`" if full
               else f"`Macro studio product photo of a {cfg['prompt']['bust_cm']} 3D printed painted resin bust, Keep the upper body`")
    base01 = (f"`full-body standing on a weighted circular base, subtle resin SSS finish, "
              f"light gray cyclorama, softbox lighting, Shot on RF 100mm f/8`" if full
              else f"`mounted on a dark beveled pedestal base, subtle resin SSS finish, "
                   f"light gray cyclorama, softbox lighting, Shot on RF 100mm f/8`")
    L = [f"# {c['dir']} 11 视角标准提示词手册", "",
         f"> **角色分类**：{spec_line(c, cfg)}",
         f"> **时代节点**：{c['era']}",
         "> **引擎与画幅**：全部 Gemini 图像模型（Gemini App 最高档）｜ 00/01 · 1:1 ｜ 02–10 · 3:4", "",
         "## 0. 人物唯一性指纹 Token 序列 (IFTS)", "", "```text", c["ifts"], "```", "",
         "## 一、 建模参考视角（00 & 01 · 1:1）", "",
         "### 视角 00: 【基底定妆照】真实生活写实摄影", "- **画幅比例**：`1:1`", "",
         "#### 中文提示词说明", c["cn00"], "", "#### 英文提示词", "```text", p00, "```", "",
         "### 视角 01: 【模型标准像】0° 正面微缩手办棚拍", "- **画幅比例**：`1:1`", "",
         "#### 中文提示词说明", c["cn01"], "", "#### 英文提示词", "```text", p01, "```", "",
         "#### 🔍 00 ➔ 01 微调置换对齐表",
         "| 维度 | 视角 00 | 视角 01 | 算子 |", "| --- | --- | --- | --- |",
         f"| 主体媒介与景别 | {frame00} | {frame01} | ① 主体置换为 3D 打印树脂模型，景别锁保留 |",
         f"| 人物指纹 (IFTS) | `{c['ifts']}` | `{c['ifts']}` | ② 逐字继承（0 差异） |",
         f"| 服装 | `wearing {c['cloth']}` | `sculpted {c['cloth01']}` | ② 保留色彩款式，追加 sculpted |",
         f"| 环境底座 | `{c['setting']}, {c['light00']}, Shot on Hasselblad 90mm f/3.2, Kodak Portra 400 film grain` | {base01} | ③ 生活场景置换为深色工艺品底座与浅灰影棚 |",
         "| 负向 | `Avoid: English text, letters, anime, cartoon, 3d render, doll, figurine, plastic skin…` | `Avoid: English text, letters, real living human, skin pores, plaster, stone column…` | ④ 01 剔除 3D/手办拦截词，改拦活人与石膏 |",
         "", "## 二、 Gemini 场景视角（02–10）", ""]
    for slot in cfg["generation"]["views_scene"]:
        s = c["scenes"][slot]
        star = " ★ 封面候选" if slot in covers else ""
        L += [f"### 视角 {slot}: 【{slot_names[slot]}】{s['title']}{star}", "- **画幅比例**：`3:4`", "",
              "#### 中文提示词说明", s["cn"], "", "#### 英文提示词", "```text",
              scene_prompt(cfg, slot, s), "```", ""]
    return "\n".join(L)


def dedup_table(cfg: dict, c: dict) -> list[str]:
    s = L.dedup_summary(cfg, c)
    rows = ["| 维度 | 本人物取值 | 去重结论 |", "| --- | --- | --- |"]
    overlap = {r[3]["dir"]: (r[0], r[1], r[2]) for r in s["overlap_top5"]}
    top = s["overlap_top5"][0] if s["overlap_top5"] else (0, 0, 0, {"dir": "—"})
    rows.append(f"| 信物 | {' + '.join(c.get('signature_props', []))} | "
                f"全库 2-gram 最高重合 {top[0]}（{top[3]['dir']}） |")
    rows.append(f"| 色彩 | {' + '.join(c.get('colors', []))} | "
                f"全库 2-gram 最高重合见 top5（{', '.join(f'{r[2]}@{r[3]['dir'][:12]}' for r in s['overlap_top5'][:3])}） |")
    rows.append(f"| 职业 | {c.get('vocation', '')} | 全库职业 2-gram 最高重合 {top[1]} |")
    rows.append(f"| 骨相 | {c['card']['d1'][:30]}… | 人工比对，见原档案 dedup 备注 |")
    verdict = "未超阈值，通过" if not s["over"] else "⚠️ 超过阈值"
    rows.append(f"| IFTS | {len(c['ifts'].split())} 词 | 全库（含归档）最高 Jaccard "
                f"{s['ifts_jaccard_max']:.2f}（对 {s['ifts_jaccard_peer']}，去停用词后按词集），"
                f"阈值 {s['ifts_threshold']}，{verdict} |")
    return rows


def render_profile(cfg: dict, c: dict) -> str:
    d = c["card"]
    quota = ("✅ 30% 现代配额（2020–2026 离世 · 享年 40–60 岁）" if c.get("modern")
             else "常规配额（70%：历史转型期 / 高龄祖辈 / 老伴）")
    slot_names = cfg["generation"]["slot_names"]
    asset_root = C.asset_root(cfg)
    L_ = [f"# 人物资产档案：{c['dir']}", "",
          f"> **资产编号**：char_{c['num']}_{c['posture']}  ",
          f"> **人物定位**：{c['title_cn']}  ",
          f"> **分类规格**：{spec_line(c, cfg)}  ",
          f"> **代际亲缘**：{c['kin']}  ",
          f"> **时代节点**：{c['era']}  ",
          f"> **配额归属**：{quota}  ",
          "> **工艺制程**：嘉立创全彩 WJP 光敏树脂 · 次表面散射 (SSS) · 哑光涂层  ",
          "> **版权状态**：100% 提示词虚构生成 · 零真人照片依赖 · 无名人参考 · AI 虚构示例角色（文案侧按手艺人设计手记/第二人称视角使用）  ",
          "", "---", "",
          "## 零、 五维人物深度铸造画像卡 (5D Character Forging Card)", "",
          f"- **人物编号与代号**：char_{c['num']}_{c['posture']} ({c['title_cn']})",
          f"- **年龄与定位**：{d['age']}",
          f"- **D1 面部骨相指纹**：{d['d1']}",
          f"- **D2 生理微瑕签名**：{d['d2']}",
          f"- **D3 服饰色彩 DNA**：{d['d3']}",
          f"- **D4 随身信物锚定**：{d['d4']}",
          f"- **D5 神态动态基线**：{d['d5']}", "",
          "- **提取唯一性指纹 Token 序列 (IFTS)**：",
          f"  `{c['ifts']}`",
          f"  （{len(c['ifts'].split())} 词，按空白分词；00 与 01 逐字连续嵌入）", "",
          "---", "", "## 一、 人物小传与生计时代背景", "", c["bio"], "",
          "---", "", "## 二、 五重去重登记（信物/色彩/职业/骨相/IFTS，数值由 library.py --dedup 实测）", ""]
    L_ += dedup_table(cfg, c)
    L_ += ["", "---", "", "## 三、 3D 打印物理工程规约", "",
           f"- **规格**：{spec_line(c, cfg)}；" + ("一体化加重圆形工艺品底座（直径 40–45mm），重心落在双脚之间。" if is_full(c)
                                                else "一体化微倒角深色工艺品底座（禁石膏柱 / 大理石柱）。"),
           "- **壁厚**：实心封闭网格，壁厚 ≥ 1.5mm；细长件（眼镜腿、绳、杆）加粗至 ≥ 1.5mm。",
           f"- **信物熔接**：{c['print']}",
           "- **材质**：WJP 全彩光敏树脂，哑光涂层，皮肤区 SSS 微透光，无真人毛孔。", "",
           "---", "", "## 四、 场景图规划（02–10 · 3:4 · 07/10 封面候选）", "",
           "| 视角 | 场景 | 专属信物 | 光影 |", "| --- | --- | --- | --- |"]
    L_ += [f"| {k} {slot_names[k]} | {c['scenes'][k]['title']} | {c['scenes'][k]['prop']} | {c['scenes'][k]['light']} |"
           for k in sorted(c["scenes"])]
    L_ += ["", f"> 手办固定描述（figurine_anchor，02–10 逐字复用）：`{c['figurine_anchor']}`", "",
           "> 图片目录（仅放图片）：`" + str(asset_root / c["dir"]) + "/`，文件名 `0.jpg`、`1.jpg`、`视角02_专属老座.jpg` … `视角10_时光重叠.jpg`。", ""]
    return "\n".join(L_)


REQUIRED = ["num", "posture", "dir", "title_cn", "kin", "era", "ifts", "setting",
            "cloth", "cloth01", "light00", "card", "bio", "print", "cn00", "cn01",
            "scenes", "figurine_anchor", "signature_props", "signature_props_en",
            "colors", "vocation"]
CARD_KEYS = ["age", "d1", "d2", "d3", "d4", "d5"]
SCENE_KEYS = ["title", "cn", "en", "shot", "prop", "light", "camera", "location"]


def check_fields(c: dict, cfg: dict) -> list[str]:
    missing = [k for k in REQUIRED if k not in c]
    if isinstance(c.get("card"), dict):
        missing += [f"card.{k}" for k in CARD_KEYS if k not in c["card"]]
    if isinstance(c.get("scenes"), dict):
        for slot in cfg["generation"]["views_scene"]:
            if slot not in c["scenes"]:
                missing.append(f"scenes.{slot}")
                continue
            s = c["scenes"][slot]
            missing += [f"scenes.{slot}.{k}" for k in SCENE_KEYS if k not in s]
    else:
        missing.append("scenes")
    return missing


def render_one(cfg: dict, cj_path: Path) -> Path:
    c = json.loads(cj_path.read_text(encoding="utf-8"))
    missing = check_fields(c, cfg)
    if missing:
        raise SystemExit(f"❌ {cj_path} 缺少必填字段：{', '.join(missing)}\n"
                         f"   字段规格见 references/character/character-json.md")
    out_dir = cj_path.parent
    (out_dir / "character_profile.md").write_text(render_profile(cfg, c), encoding="utf-8")
    (out_dir / "prompts.md").write_text(render_prompts(cfg, c), encoding="utf-8")
    # prompts.json 由 validate_prompts 的 export 生成
    import validate_prompts as V
    ch = C.load_character(cfg, out_dir)
    V.export_json(ch, cfg, out_dir / "prompts.json")
    (C.asset_root(cfg) / c["dir"]).mkdir(parents=True, exist_ok=True)
    print("rendered", c["dir"])
    return out_dir


def main() -> int:
    ap = argparse.ArgumentParser(description="character.json → profile + prompts")
    ap.add_argument("target", nargs="?")
    ap.add_argument("--all-batch", nargs="*", metavar="DIR",
                    help="批量渲染；不给参数时渲染 MATERIAL 下所有含 character.json 的人物")
    args = ap.parse_args()
    cfg = C.load_config()

    if args.all_batch is not None:
        dirs = [C.resolve_char_dir(cfg, a) for a in args.all_batch] if args.all_batch else \
            [d for d in sorted(C.material_root(cfg).glob("char_*"))
             if d.is_dir() and (d / "character.json").is_file()]
        for d in dirs:
            render_one(cfg, d / "character.json")
        print(f"共渲染 {len(dirs)} 个人物")
        return 0
    if not args.target:
        ap.print_help()
        return 2
    p = Path(args.target).expanduser()
    if p.is_file():
        cj = p
    else:
        cj = C.resolve_char_dir(cfg, args.target) / "character.json"
    render_one(cfg, cj)
    return 0


if __name__ == "__main__":
    sys.exit(main())
