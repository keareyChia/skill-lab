# skill-lab

我个人的 skill 工作台，用来收集、开发、验证和沉淀可复用的能力模块。

这里的每个 skill 都走过四步：

- 收集：把日常高频任务、可复用流程和踩过的经验收进来
- 开发：把零散做法整理成标准化的 Skill
- 验证：用真实场景和边界案例检验它是否靠谱
- 沉淀：留下通过验证的版本，下次直接调用

## 仓库定位

比起堆文档，我更在意每个 skill 能不能真的被调用、被信任。所以收进来的 skill 都尽量满足：

- 有明确的触发条件
- 有可执行的输出
- 有边界、回退和验证方法
- 能在真实任务里继续迭代

## 快速索引

### 1. `wechat-article-fetch`

- 核心能力：抓取微信公众号文章并转换为 Markdown
- 适用场景：`mp.weixin.qq.com` 链接、公众号正文入库、知识库归档
- 关键方法：iPhone MicroMessenger UA + HTML 提取 + captcha/fallback 判断
- 典型产出：文章正文、Markdown、JSON、可入库文本

### 2. `csdn-geo-draft-publisher`

- 核心能力：把 AI-GEO 基础资产改写成 CSDN 技术草稿并辅助填写
- 适用场景：品牌内容结构化、技术文章草稿生成、人工审核发布
- 关键方法：输入资产分层、教程型结构、Playwright 可见浏览器、Human-in-the-loop
- 典型产出：文章正文、标题、摘要、标签、检查清单、草稿填充状态

### 3. `xhs-stable-comic`

- 核心能力：小红书 `AI + 健身` 方向的人设、内容、选题和四格漫画工作流
- 适用场景：账号冷启动、视觉系统搭建、漫画连载、内容复盘
- 关键方法：先人设后内容、角色卡/画风卡初始化、AIGC 合规与真人证据优先
- 典型产出：账号人设卡、内容世界观、选题、脚本、画风卡、漫画提示词

### 4. `cangjie-skill`

- 核心能力：把一本书的方法论蒸馏成可调用、可测试、可组合的 Skills
- 适用场景：书籍知识复用、方法论拆解、Skill 生态化管理
- 关键方法：整书理解、并行提取、三重验证、RIA++ 结构化、Zettelkasten 链接、压力测试
- 典型产出：`BOOK_OVERVIEW.md`、`INDEX.md`、多个独立 `SKILL.md`、测试提示集

### 5. `1panel-local-app-packaging`

- 核心能力：把自定义 Docker 应用包装成 1Panel 本地应用，并准备 AppStore 提交流程
- 适用场景：1Panel 应用市场缺失、自定义容器纳管、Compose 项目标准化、PR 提交准备
- 关键方法：先分清本地纳管 vs 提交上架、`1panel app init` 生成模板、标准目录结构、安装表单、升级/卸载脚本
- 典型产出：1Panel 应用包、目录规范、验证清单、提交步骤

### 6. `baoyu-skills`

- 核心能力：宝玉（JimLiu）整理的 20+ 个 AI Agent 技能合集，分内容生成、AI 生成后端、效率工具三类
- 适用场景：小红书图卡、信息图、封面图、幻灯片、知识漫画、文章插图，以及发布到 X / 公众号 / 微博、图像生成、YouTube 字幕、网页转 Markdown、翻译排版
- 关键方法：插件市场分发（`/plugin marketplace add`）、风格 × 布局 / 多维度组合、真实 Chrome + CDP 绕过反自动化、多服务商图像后端自动选择
- 典型产出：可发布的图卡 / 信息图 / 封面 / 幻灯片 / 漫画、Markdown / HTML、各平台草稿、翻译稿
- 上游仓库：[JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)（保留嵌套 `.git`，可单独 `git pull` 更新）

### 7. `qiaomu-novel-generator`

- 核心能力：把一句故事想法先拆成可选的剧情策略，确认后再写成原创、完整、低 AI 味的中文短篇小说
- 适用场景：爽文 / 武侠 / 修仙 / 悬疑 / 职场内斗 / 科幻短篇、经典桥段重构、参考作品联网搜索后重构
- 关键方法：先定剧情引擎（情绪承诺 → 高压关系 → 冲突场 → 桥段重构 → 升级节奏 → 结尾余味）再落笔、反 AI 味检查、开篇语义清晰门槛、版权安全边界
- 典型产出：可选剧情策略、确认版大纲、完整短篇正文、按九项门槛的质量自检
- 上游仓库：[joeseesun/qiaomu-novel-generator](https://github.com/joeseesun/qiaomu-novel-generator)（保留嵌套 `.git`，可单独 `git pull` 更新）

## 仓库结构

```text
skill-lab/
├── README.md
├── wechat-article-fetch/
├── csdn-geo-draft-publisher/
├── xhs-stable-comic/
├── cangjie-skill/
├── 1panel-local-app-packaging/
├── baoyu-skills/
└── qiaomu-novel-generator/
```

## 维护原则

- 先验证，再固化
- 先写清触发条件，再写输出
- 先定义边界，再扩展能力
- 先能复用，再谈美观

## 说明

每个 skill 都是独立的能力单元：在真实任务里直接用，在边界案例里修，在长期使用中慢慢长好。其中 `baoyu-skills` 和 `qiaomu-novel-generator` 来自上游开源仓库，本仓库保留了它们各自的嵌套 `.git`，既能在这里看到全部文件，也能进目录单独 `git pull` 跟进上游更新。
