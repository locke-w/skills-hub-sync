# Fullcolor 素材库质量审计报告

> 生成时间：2026-09-24 22:18 · 校验器：`validators/validate_prompts.py`（直接解析 prompts.md）· 规则源：`config/paths.yml`
> 扫描目录：`/Users/wuyongjia/obsidian-gitee/technology/🚀 项目/3D打印/素材`

| 人物数 | ✅ 通过 | ⚠️ 仅 MAJOR | ❌ 含 BLOCKER |
| --- | --- | --- | --- |
| 12 | 9 | 1 | 2 |

## 问题分布（按人物计）

| 级别 · 规则 | 人物数 |
| --- | --- |
| MAJOR RATIO_GEMINI | 2 |
| MAJOR SCENE_SIMILAR | 2 |
| BLOCKER NO_ENGLISH | 2 |
| MAJOR TEXT_RENDER | 2 |
| MINOR COVER_SPACE | 2 |
| BLOCKER FRAMING | 1 |
| MINOR IFTS_LENGTH | 1 |
| MAJOR WORD_COUNT | 1 |

## 规则说明

- **FRAMING**：v4.1 起胸像须含 `Keep the upper body`、全身像须含 `full-body`（00 ≥1、01 ≥2）；
- **NO_ENGLISH**：v4.1 起 00/01 的 `--no` 须含 `English`，02–10 的 `Avoid:` 须含 `English text, letters`；
- **RATIO_GEMINI**：v5 起 02–10 为 3:4 竖构图；存量 1:1 素材整组重出时再改；
- **WORD_COUNT**：v5 预算 总 50–82 词、正向 ≤65（按空白分词统计）；
- **SCENE_SIMILAR**：同一槽位跨人物内容词相似度超过阈值，属同质化嫌疑，需在机位/实景/道具/光影中至少改两层。

## 逐个人物

| 人物 | 姿态 | BLOCKER | MAJOR | MINOR | 主要问题 |
| --- | --- | --- | --- | --- | --- |
| char_59_BW_在灯下缝补衣裳省吃俭用的婆婆 | BW | 12 | 3 | 2 | FRAMING, NO_ENGLISH, RATIO_GEMINI, SCENE_SIMILAR, TEXT_RENDER |
| char_60_FM_在码头拉纤绳的长江老纤夫爷爷 | FM | 11 | 3 | 1 | NO_ENGLISH, RATIO_GEMINI, TEXT_RENDER, WORD_COUNT |
| char_61_BM_2026近几年心衰离世的56岁长途冷链物流父亲 | BM | 0 | 0 | 0 |  |
| char_62_BW_2026近几年胰腺重症离世的52岁社区保洁母亲 | BW | 0 | 1 | 0 | SCENE_SIMILAR |
| char_63_FM_手持长竹篙撑乌篷船的江南水乡摆渡外公 | FM | 0 | 0 | 0 |  |
| char_64_FW_手提竹编圆扁篮沿街卖栀子花白兰花的苏南阿婆奶奶 | FW | 0 | 0 | 0 |  |
| char_65_BW_在打铁铺掌火拉皮风箱相伴一生的铁匠老伴奶奶 | BW | 0 | 0 | 0 |  |
| char_66_BM_2026近几年深夜心梗离世的54岁代驾司机父亲 | BM | 0 | 0 | 0 |  |
| char_67_FW_2026近几年积劳病逝的50岁城中村理发师母亲 | FW | 0 | 0 | 0 |  |
| char_68_FM_街口摇黑葫芦爆米花机的旧时光爷爷 | FM | 0 | 0 | 0 |  |
| char_69_BW_在绷架前绣了一辈子枕套花样的绣娘外婆 | BW | 0 | 0 | 0 |  |
| char_70_BM_在屋顶鸽棚养了一辈子鸽子的寡言公公 | BM | 0 | 0 | 0 |  |
