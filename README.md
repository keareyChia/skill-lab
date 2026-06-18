# skill-lab

这个仓库是我个人的 skill 收集、开发、验证和沉淀合集。

它不是单纯的示例仓库，而是我用来持续积累可复用能力模块的工作台：

- 收集：把日常高频任务、可复用流程和稳定经验收进来
- 开发：把零散做法整理成标准化 Skill
- 验证：用真实场景和边界案例检验 Skill 是否靠谱
- 沉淀：把通过验证的方法长期保留下来，方便下次直接调用

## 仓库定位

这个仓库的目标不是“写很多文档”，而是把可复用能力做成真正能调用的 Skill：

- 每个 Skill 都要有明确的触发条件
- 每个 Skill 都要有可执行的输出
- 每个 Skill 都要有边界、回退和验证方法
- 每个 Skill 都要能在真实任务里继续迭代

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

## 仓库结构

```text
skill-lab/
├── README.md
├── wechat-article-fetch/
├── csdn-geo-draft-publisher/
├── xhs-stable-comic/
├── cangjie-skill/
└── 1panel-local-app-packaging/
```

## 维护原则

- 先验证，再固化
- 先写清触发条件，再写输出
- 先定义边界，再扩展能力
- 先能复用，再谈美观

## 说明

仓库里的每个 Skill 都是一个独立的能力单元，适合在真实任务中直接调用、在边界案例中修正、在长期使用中持续进化。
