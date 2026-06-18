# 1Panel Local App Packaging

## 这个 Skill 是什么

当你想把一个自定义 Docker 应用变成 1Panel 能纳管的本地应用，或者进一步整理成可提交到 1Panel AppStore 的应用包时，使用这个 Skill。

它关注的不是应用本身，而是 **1Panel 认得的目录结构、声明文件、版本文件、安装脚本和提交流程**。

## 适用场景

- 1Panel 应用商店里没有你要的应用，但你想自己封装
- 想把一个现成的 Docker Compose 项目包装成 1Panel 本地应用
- 想理解 `1panel app init` 生成的模板如何改
- 想把本地应用整理成可提交 PR 的 AppStore 规范包
- 想为个人项目建立可重复的 1Panel 部署模板

## 核心方法论

### 1. 先分清目标

先判断你要的是哪一种：

- **本地纳管**：只需要 1Panel 管理启动、停止、升级、日志、端口、环境变量
- **AppStore 提交**：还要满足仓库规范、命名规范、README、logo、版本目录和 PR 流程

这两种目标的目录和工序相同一部分，但提交要求更严格。

### 2. 先看 1Panel 的识别契约

1Panel 本地应用的关键不是 UI，而是它能否识别下面这些文件：

- 顶层 `data.yml`：应用声明
- 顶层 `README.md`：应用说明
- `logo.png`：应用图标
- 版本目录：如 `1.0.0/`
- 版本目录下的 `data.yml`：安装表单参数
- 版本目录下的 `docker-compose.yml`：运行编排
- 版本目录下的 `data/scripts/`：初始化、升级、卸载脚本

### 3. 目录结构要标准

常见结构如下：

```text
<app-key>/
  logo.png
  data.yml
  README.md
  1.0.0/
    data.yml
    data/
      scripts/
        init.sh
        upgrade.sh
        uninstall.sh
    docker-compose.yml
```

要点：

- `app-key` 用英文小写
- 版本目录不要带 `v`
- 图标尽量小而标准
- 安装参数和运行编排分层放置

### 4. 先用命令生成模板

优先使用 1Panel 的初始化命令来生成骨架，而不是手写猜结构：

```bash
1panel app help
1panel app init -k <app-key> -v <version>
```

这个步骤的价值在于：

- 避免目录拼错
- 避免字段漏写
- 避免版本目录结构不符合 1Panel 预期

### 5. 用 Compose 思维封装应用

封装自定义应用时，核心是把已有 Docker Compose 项目整理成：

- 可安装
- 可配置
- 可升级
- 可卸载
- 可迁移

因此要重点关注：

- 端口映射
- 持久化卷
- 环境变量
- 健康检查
- 启停脚本
- 数据目录归属

### 6. 先做本地应用，再考虑提交

不要一上来就按“提交 AppStore”标准死磕。

推荐顺序：

1. 先让本地 1Panel 能安装
2. 再确认升级、卸载、重启、日志都正常
3. 再整理 README、logo、分类、版本号
4. 最后考虑 PR 到 appstore

## 标准流程

### A. 本地封装流程

1. 确定应用 key 和版本号
2. `1panel app init -k ... -v ...` 生成模板
3. 把 Docker Compose 改成你的服务
4. 配好环境变量和卷
5. 补全 `data.yml`
6. 写安装/升级/卸载脚本
7. 试装一次，确认可以纳管

### B. AppStore 提交流程

1. fork `1Panel-dev/appstore`
2. clone `dev` 分支
3. 新建分支：`app/<app-name>`
4. 按规范放入应用目录
5. 补充 README、logo、版本目录
6. 本地验证
7. 提交 PR

## 判断是否合格

一个可交付的 1Panel 应用至少应满足：

- 1Panel 能识别并安装
- 环境变量能在表单里配置
- 数据卷能持久化
- 容器重启后状态正常
- 升级和卸载不破坏数据
- README 能让别人快速看懂用途和边界

## 常见坑

- 把版本号写成 `v1.0.0`
- 顶层 `data.yml` 和版本目录 `data.yml` 混淆
- 忘了写 `README.md` 和 `logo.png`
- Compose 里用了本机硬编码路径
- 没处理好数据卷权限
- 只顾着能跑，没考虑升级和卸载
- 直接往官方仓库提，没先在本地验证

## 这个 Skill 的输出风格

当用户要你“做一个 1Panel 应用”时，默认输出以下内容：

- 应用定位
- app key 建议
- 目录结构
- `data.yml` 设计思路
- `docker-compose.yml` 改造思路
- 安装/升级/卸载脚本责任划分
- 本地验证清单
- 是否适合提交到 AppStore

## 触发示例

- `帮我把这个 Docker 项目包装成 1Panel 应用`
- `我想做一个 1Panel 本地应用`
- `这个项目怎么提交到 1Panel appstore`
- `1Panel 的 app init 生成的文件怎么改`
- `帮我设计一个 1Panel app 的目录结构`
- `我要把自定义容器交给 1Panel 管理`

## 简短原则

- 先本地纳管，再考虑上架
- 先按模板生成，再按项目调整
- 先能安装，再谈美观
- 先验证升级卸载，再谈提交 PR

## 参考文件

### `references/contract.md`

1Panel 本地应用的识别契约、目录结构和字段职责。

### `references/workflow.md`

从需求到本地纳管，再到 AppStore 提交的完整流程。

### `references/checklist.md`

安装前、安装中、安装后、提交前的验证清单。

### `templates/app-data.yml.template`

顶层应用声明文件模板。

### `templates/version-data.yml.template`

版本目录下安装表单模板。

### `templates/docker-compose.yml.template`

1Panel 可纳管的 Compose 模板。

### `templates/scripts/init.sh.template`

安装初始化脚本模板。

### `templates/scripts/upgrade.sh.template`

升级脚本模板。

### `templates/scripts/uninstall.sh.template`

卸载脚本模板。
