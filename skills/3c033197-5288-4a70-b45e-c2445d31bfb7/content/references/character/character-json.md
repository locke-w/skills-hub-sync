# character.json 字段规格（auto-xhs 阶段 1 输入契约）

> `render_character.py` 的唯一输入。缺字段会直接报错并列出缺失字段名。完整示例见同目录 `character.example.json`（char_79 护林员岳父）。

## 顶层字段

| 字段 | 类型 | 必填 | 约束 |
| :--- | :--- | :---: | :--- |
| `num` | int | ✅ | 人物编号，须与目录名 `char_{num}_*` 一致，全库唯一（`library.py --next-id` 分配） |
| `posture` | str | ✅ | `BW`/`BM`（胸像 6cm）或 `FW`/`FM`（全身 12cm）；全身强制 full-body 链路 |
| `modern` | bool | ⭕ | true = 30% 现代配额（2020–2026 离世 · 享年 40–60 岁）；缺省视为 false |
| `dir` | str | ✅ | 人物目录名，须等于实际目录名 |
| `title_cn` | str | ✅ | 中文人物定位（进档案与目录名一致） |
| `kin` | str | ✅ | 代际亲缘（父辈/祖辈/伴侣/姻亲代 + 角色） |
| `era` | str | ✅ | 时代节点与生计背景一句话 |
| `ifts` | str | ✅ | IFTS 指纹序列，**15–20 个英文词**，00/01 逐字连续嵌入；全库 Jaccard < 阈值（见 studio.toml [prompt]） |
| `setting` | str | ✅ | 视角 00 生活场景（英文短语，无句号） |
| `cloth` | str | ✅ | 视角 00 服饰（英文，`wearing` 后内容） |
| `cloth01` | str | ✅ | 视角 01 雕塑化服饰（英文，`sculpted` 后内容） |
| `light00` | str | ✅ | 视角 00 光影（英文短语） |
| `card` | object | ✅ | 五维画像卡，必填子键：`age`、`d1`–`d5`（D1 骨相 / D2 生理微瑕 / D3 服饰色彩 DNA / D4 随身信物 / D5 神态动态基线） |
| `bio` | str | ✅ | 人物小传（中文一段） |
| `dedup` | array | ⭕ | 五重去重登记表 `[[维度, 取值, 结论], ...]`，由 `library.py --dedup` 实测结果填写 |
| `print` | str | ✅ | 3D 打印物理工程规约一句（熔接/壁厚/重心） |
| `cn00` | str | ✅ | 视角 00 中文说明 |
| `cn01` | str | ✅ | 视角 01 中文说明 |
| `scenes` | object | ✅ | 键 `"02"`–`"10"` 共 9 个槽位，见下表 |
| `figurine_anchor` | str | ✅ | 手办固定英文描述（如 `the 6cm resin bust of a ... with a brass valve wrench`），**必须在每个场景 `en` 中逐字出现**（大小写不敏感校验）；含人物年龄身份 + 主服饰 + 一件专属信物 |
| `signature_props` | str[] | ✅ | 专属信物中文名列表 |
| `signature_props_en` | str[] | ✅ | 专属信物英文词列表；`validate_prompts.py` PROP 规则要求每个 02–10 视角至少命中其一（可加同义别名，如 `"wooden shuttle"`） |
| `colors` | str[] | ✅ | 服饰主辅色彩（中文），五重去重色彩维用 |
| `vocation` | str | ✅ | 职业名（中文），五重去重职业维用 |
| `generation` | str | ⭕ | 代际标签（父辈/祖辈/配偶等），配额统计参考 |

## scenes["NN"] 子字段（NN ∈ 02–10）

| 字段 | 类型 | 必填 | 约束 |
| :--- | :--- | :---: | :--- |
| `title` | str | ✅ | 场景中文名 |
| `cn` | str | ✅ | 中文场景说明 |
| `en` | str | ✅ | 英文场景正文（不含 `Vertical 3:4 composition.` / `Shot on` / `Avoid:`——由渲染器按模板拼接）；须逐字含 `figurine_anchor`，至少含一个 `signature_props_en` 词；07/10 由渲染器自动加封面留白句 |
| `shot` | str | ✅ | 机身+镜头+光圈+胶片调（英文，渲染为 `Shot on {shot}`） |
| `prop` | str | ✅ | 中文道具说明（进 profile 场景规划表） |
| `light` | str | ✅ | 中文光影说明；批内同槽位四层（camera/location/prop/light）与他人至少 2 层不同，否则 VARIATION |
| `camera` | str | ✅ | 英文相机（去重四层之一） |
| `location` | str | ✅ | 英文场景位置（去重四层之一） |

## 渲染产出

`render_character.py` 从本文件生成：`character_profile.md`、`prompts.md`（11 视角全量）、`prompts.json`（经 `validate_prompts.py` 导出），并确保 `{paths.asset_dir}/{dir}/` 图片目录存在（不覆盖已有图片）。
