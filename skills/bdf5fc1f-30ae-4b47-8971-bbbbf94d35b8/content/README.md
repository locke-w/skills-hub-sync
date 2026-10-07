# idea-stage-validation

> A Claude Code / Claude Agent **Skill** that pressure-tests a fuzzy product idea into an evidence-backed bet — Claude acts as a structured **devil's advocate**. Based on Anthropic's *"AI startup lifecycle · Idea stage."*

把一个模糊的产品/创业想法，用结构化「魔鬼代言人」流程推到"不是赌直觉，而是对着证据下注"。方法基于 Anthropic「AI 创业生命周期 · 想法阶段」。

## 覆盖（想法阶段 4 步，不造原型）

1. **定义并压力测试问题假设** — 冻结一句可证伪的问题；拆 5 要素（每个标"已知/假设"）；列互斥根因
2. **市场研究 + 竞品分层地图** — 4 层竞品（含"用户现在的免费替代"）+ TAM/SAM/SOM + 买家地图
3. **设计并跑客户访谈** — Mom-Test 提纲（只挖过去、不推销）；让用户去聊真人，带笔记回来复盘
4. **设计方案概念** — 现实检查点（被证伪就别设计）+ 3 个最承重假设（假设→必须为真→失败后果）

> 不做第 5 步造原型；MVP 是之后另一个阶段。

## 核心原则

- **问题 ≠ 方案**：先冻结一句可证伪的问题，再攻击
- **三档证据**：armchair 自我推理 ＜ opencli 抓的真实群体声音 ＜ 1:1 真人访谈
- 用 [**opencli**](https://github.com/jackwener/opencli) 抓 HN / Reddit / 小红书 / 知乎 / X 的真实抱怨与竞品评价做反证
- 每步**说人话 + 止损闸门**：随时可提前判死，"早死是成功不是失败"
- **必须真人访谈才放行**

## 安装

```bash
git clone https://github.com/AlineFan/idea-stage-validation.git \
  ~/.claude/skills/idea-stage-validation
```

确保 `~/.claude/skills/idea-stage-validation/SKILL.md` 存在。然后在 Claude Code 里带想法来（"我想做一个 X""这个值不值得做"），或输入 `/idea-stage-validation`。

## 依赖

"找反证"步骤用 [opencli](https://github.com/jackwener/opencli)：

```bash
npm install -g @jackwener/opencli   # Node ≥ 21
opencli doctor                       # COOKIE 站（小红书/知乎/Reddit/X）需登录 Chrome + 扩展
```

PUBLIC 站点（如 HackerNews）免登录直接可用；COOKIE 站点需浏览器扩展或在已登录环境运行。

## 实战

已在多个真实想法上跑通。最有价值的一次：在写一行代码之前就判死了一个会撞结构性障碍 + 免费 DIY 红海的想法——零建造成本，早死省力。这正是它的意义。

## License

见 [LICENSE](LICENSE)。
