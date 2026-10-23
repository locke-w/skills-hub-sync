# Agent Skills Collection (`skills-hub-sync`)

遵循 [`mattpocock/skills`](https://github.com/mattpocock/skills) 标准架构组织的 Agent Skills 仓库，完美支持 **CC Switch**、`npx skills`、**Claude Code**、**Codex**、**Gemini CLI** 与 **Antigravity**。

## 目录结构

```text
.
├── .claude-plugin/
│   ├── marketplace.json       # Claude / Codex 插件市场声明
│   └── plugin.json            # 插件元数据与全部技能路径索引
├── scripts/
│   ├── link-skills.sh         # 本地符号链接安装脚本
│   ├── list-skills.sh         # 列出仓库内所有 SKILL.md
│   └── sync-plugin-version.mjs# 同步 package.json 与 plugin.json 版本号
├── skills/
│   └── <skill-name>/          # 以技能真实名称命名的独立目录（彻底解决 content 目录冲突）
│       └── SKILL.md
└── package.json
```

## 快速安装

### 1. CC Switch
在 **CC Switch -> Skills -> 发现** 中刷新 `locke-w/skills-hub-sync` 仓库，即可独立勾选并安装任意多个技能，互不覆盖。

### 2. `skills.sh` / `npx skills`
```bash
# 安装指定技能
npx skills add locke-w/skills-hub-sync --skill <skill-name>

# 安装仓库内全部技能
npx skills add locke-w/skills-hub-sync
```

### 3. Claude Code / Codex 插件安装
```bash
codex plugin marketplace add locke-w/skills-hub-sync
codex plugin add locke-w-skills@locke-w
```

### 4. 本地开发软链
```bash
./scripts/link-skills.sh
```

## 包含的技能列表（共 55 个）

| 技能名称 (`skill-name`) | 路径 | 简介 |
| :--- | :--- | :--- |
| [`agent-reach`](./skills/agent-reach) | `skills/agent-reach` | > |
| [`alibaba-java-standards`](./skills/alibaba-java-standards) | `skills/alibaba-java-standards` | Use when writing, refactoring, reviewing, or designing Java code, Spring Boot applications, APIs,... |
| [`auto-xhs`](./skills/auto-xhs) | `skills/auto-xhs` | 纪念手办（3D 全彩打印长辈/父母/公婆/岳父母/老伴手办）小红书全流程技能：① 铸造无肖像侵权的虚构中国长辈人物（五维画像 + IFTS + 全库去重）并生成 11 视角提示词；② 驱动本机 ... |
| [`brainstorming`](./skills/brainstorming) | `skills/brainstorming` | You MUST use this before any creative work - creating features, building components, adding funct... |
| [`clerk`](./skills/clerk) | `skills/clerk` | \| |
| [`code-reviewer`](./skills/code-reviewer) | `skills/code-reviewer` | Use when conducting thorough, multi-dimensional code reviews on code changes, PRs, git diffs, ref... |
| [`cognitive-distillation-architect`](./skills/cognitive-distillation-architect) | `skills/cognitive-distillation-architect` | Use when distilling a specific person or school's cognitive operating system into a verifiable, l... |
| [`dispatching-parallel-agents`](./skills/dispatching-parallel-agents) | `skills/dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dep... |
| [`doc-coauthoring`](./skills/doc-coauthoring) | `skills/doc-coauthoring` | Guide users through a structured workflow for co-authoring documentation. Use when user wants to ... |
| [`executing-plans`](./skills/executing-plans) | `skills/executing-plans` | Use when you have a written implementation plan to execute in a separate session with review chec... |
| [`find-skills`](./skills/find-skills) | `skills/find-skills` | Helps users discover and install agent skills when they ask questions like "how do I do X", "find... |
| [`finishing-a-development-branch`](./skills/finishing-a-development-branch) | `skills/finishing-a-development-branch` | Use when implementation is complete, all tests pass, and you need to decide how to integrate the ... |
| [`fullcolor-3dprint-character-prompts`](./skills/fullcolor-3dprint-character-prompts) | `skills/fullcolor-3dprint-character-prompts` | Use when generating AI-photoreal elder, parent, in-law, or late-spouse character profiles and 11-... |
| [`gsap-animation-assistant`](./skills/gsap-animation-assistant) | `skills/gsap-animation-assistant` | GSAP assistant for generating and reviewing frontend animation code with timelines, ScrollTrigger... |
| [`java-architect`](./skills/java-architect) | `skills/java-architect` | Use when building, configuring, or debugging enterprise Java applications with Spring Boot 3.x, m... |
| [`java-coding-standards`](./skills/java-coding-standards) | `skills/java-coding-standards` | Java coding standards for Spring Boot and Quarkus services: naming, immutability, Optional usage,... |
| [`java-testing`](./skills/java-testing) | `skills/java-testing` | Test Java applications - JUnit 5, Mockito, integration testing, TDD patterns |
| [`macos-gui-automation`](./skills/macos-gui-automation) | `skills/macos-gui-automation` | Use when computer_use GUI 批准超时,需无人值守驱动 macOS 应用。 |
| [`macos-proxy-troubleshooting`](./skills/macos-proxy-troubleshooting) | `skills/macos-proxy-troubleshooting` | Use when an app hits region errors despite a proxy running. |
| [`manage-skills-hub`](./skills/manage-skills-hub) | `skills/manage-skills-hub` | Use this skill whenever an Agent needs to query, find, install, deploy, update, tag, adopt, diagn... |
| [`opencli-adapter-author`](./skills/opencli-adapter-author) | `skills/opencli-adapter-author` | Use when writing an OpenCLI adapter for a new site or adding a new command to an existing site. G... |
| [`opencli-autofix`](./skills/opencli-autofix) | `skills/opencli-autofix` | Automatically fix broken OpenCLI adapters when commands fail. Load this skill when an opencli com... |
| [`opencli-browser-sitemap`](./skills/opencli-browser-sitemap) | `skills/opencli-browser-sitemap` | Use when driving a website with opencli browser and sitemap context is available, requested, or n... |
| [`opencli-browser`](./skills/opencli-browser) | `skills/opencli-browser` | Use when an agent needs to drive a real Chrome window via opencli — inspect a page, fill forms, c... |
| [`opencli-sitemap-author`](./skills/opencli-sitemap-author) | `skills/opencli-sitemap-author` | Use when creating or maintaining OpenCLI site sitemaps: agent-facing navigation, page-state, acti... |
| [`opencli-usage`](./skills/opencli-usage) | `skills/opencli-usage` | Use at the start of any OpenCLI session — this is the top-level map of what `opencli` can do, how... |
| [`photorealistic-character-generator`](./skills/photorealistic-character-generator) | `skills/photorealistic-character-generator` | Use when generating hyper-realistic human character portraits for AI short dramas, films, commerc... |
| [`photorealistic-character`](./skills/photorealistic-character) | `skills/photorealistic-character` | Use when generating ultra-realistic human faces, creating character consistency assets for AI sho... |
| [`playwright-cli`](./skills/playwright-cli) | `skills/playwright-cli` | Automate browser interactions, test web pages and work with Playwright tests. |
| [`playwright`](./skills/playwright) | `skills/playwright` | Use when the task requires automating a real browser from the terminal (navigation, form filling,... |
| [`project-workflow-analysis-blueprint-generator`](./skills/project-workflow-analysis-blueprint-generator) | `skills/project-workflow-analysis-blueprint-generator` | Comprehensive technology-agnostic prompt generator for documenting end-to-end application workflo... |
| [`python-architect`](./skills/python-architect) | `skills/python-architect` | Use when designing, building, refactoring, or reviewing enterprise Python applications, microserv... |
| [`python-pro`](./skills/python-pro) | `skills/python-pro` | Use when building Python 3.11+ applications requiring type safety, async programming, or robust e... |
| [`receiving-code-review`](./skills/receiving-code-review) | `skills/receiving-code-review` | Use when receiving code review feedback, before implementing suggestions, especially if feedback ... |
| [`requesting-code-review`](./skills/requesting-code-review) | `skills/requesting-code-review` | Use when completing tasks, implementing major features, or before merging to verify work meets re... |
| [`security-auditor`](./skills/security-auditor) | `skills/security-auditor` | Use when conducting security audits, vulnerability assessments, threat modeling, security hardeni... |
| [`springboot-tdd`](./skills/springboot-tdd) | `skills/springboot-tdd` | 使用 JUnit 5、Mockito、MockMvc、Testcontainers 和 JaCoCo 进行 Spring Boot 的测试驱动开发 (TDD)。在添加功能、修复 Bug 或进行重... |
| [`study-notes-writer`](./skills/study-notes-writer) | `skills/study-notes-writer` | Use when generating, organizing, refactoring, or polishing study notes, learning guides, technica... |
| [`subagent-driven-development`](./skills/subagent-driven-development) | `skills/subagent-driven-development` | Use when executing implementation plans with independent tasks in the current session |
| [`systematic-debugging`](./skills/systematic-debugging) | `skills/systematic-debugging` | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| [`tech-study-docs`](./skills/tech-study-docs) | `skills/tech-study-docs` | Use when writing, structuring, or refactoring technical documentation, study notes, tech specs, A... |
| [`template-skill`](./skills/template-skill) | `skills/template-skill` | Replace with description of the skill and when Claude should use it. |
| [`tencent-docs`](./skills/tencent-docs) | `skills/tencent-docs` | 腾讯文档（docs.qq.com）-在线云文档平台，是创建、编辑、管理文档的首选 skill。涉及"新建/创建/编辑/读取/查看/搜索文档"、"保存文件"、"云文档"、"腾讯文档"、"docs.... |
| [`tencent-meeting-skill`](./skills/tencent-meeting-skill) | `skills/tencent-meeting-skill` | 在用户提及腾讯会议、视频会议、线上会议相关内容与操作时使用此技能。触发关键词包括：预约会议、创建会议、修改会议、取消会议、查询会议、会议详情、会议号、meeting_id、meeting_cod... |
| [`test-driven-development`](./skills/test-driven-development) | `skills/test-driven-development` | Use when implementing any feature or bugfix, before writing implementation code |
| [`test-engineer`](./skills/test-engineer) | `skills/test-engineer` | Use when designing test suites, writing unit/integration/E2E tests, analyzing test coverage gaps,... |
| [`using-git-worktrees`](./skills/using-git-worktrees) | `skills/using-git-worktrees` | Use when starting feature work that needs isolation from current workspace or before executing im... |
| [`verification-before-completion`](./skills/verification-before-completion) | `skills/verification-before-completion` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - ... |
| [`web-access`](./skills/web-access) | `skills/web-access` | 所有联网操作必须通过此 skill 处理，包括：搜索、网页抓取、登录后操作、网络交互等。 |
| [`web-performance-auditor`](./skills/web-performance-auditor) | `skills/web-performance-auditor` | Use when conducting web performance audits, analyzing Core Web Vitals (LCP, INP, CLS), optimizing... |
| [`web-scraping`](./skills/web-scraping) | `skills/web-scraping` | Expert in web scraping and data extraction with Python tools |
| [`wechat-miniprogram-architect`](./skills/wechat-miniprogram-architect) | `skills/wechat-miniprogram-architect` | Use when designing, building, refactoring, or reviewing WeChat Mini-Program (微信小程序) systems and e... |
| [`writing-plans`](./skills/writing-plans) | `skills/writing-plans` | Use when you have a spec or requirements for a multi-step task, before touching code |
| [`writing-skills`](./skills/writing-skills) | `skills/writing-skills` | Use when creating new skills, editing existing skills, or verifying skills work before deployment |
| [`xiaohongshu-memorial-3dprint-copywriter`](./skills/xiaohongshu-memorial-3dprint-copywriter) | `skills/xiaohongshu-memorial-3dprint-copywriter` | 小红书纪念手办（3D 打印长辈/父母/公婆/岳父母/老伴手办）专业运营技能。基于 fullcolor 人物档案与图片资产，产出可直接发布的标题、正文、话题、封面大字与图序，以及置顶评论、评论回复... |
