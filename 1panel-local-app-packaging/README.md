# 1Panel Local App Packaging

1Panel 本地应用的识别契约、标准目录结构、模板生成、Compose 封装、验证清单，以及 AppStore 提交流程。

## 这个目录解决什么问题

- 应用商店没有目标应用时，如何把自定义 Docker / Compose 项目纳入 1Panel 管理
- 如何从 0 到 1 生成一个符合 1Panel 规范的本地应用包
- 如何把本地应用进一步整理成可提交到 `1Panel-dev/appstore` 的 PR

## 核心能力

- 识别 1Panel 本地应用的目录契约
- 用 `1panel app init` 生成模板骨架
- 设计顶层 `data.yml` 与版本目录 `data.yml`
- 将 Docker Compose 项目迁移到 1Panel 应用结构
- 配置安装表单、环境变量、卷和健康检查
- 编写 init / upgrade / uninstall 脚本
- 准备本地验证和 AppStore 提交清单

## 方法论一句话

先让应用在本地 1Panel 中被识别和稳定安装，再补齐 README、logo、版本、脚本和验证清单，最后再考虑提交到官方 AppStore。

## 目录建议

```text
1panel-local-app-packaging/
├── README.md
├── SKILL.md
├── references/
│   ├── contract.md
│   ├── workflow.md
│   └── checklist.md
└── templates/
    ├── app-data.yml.template
    ├── version-data.yml.template
    ├── docker-compose.yml.template
    └── scripts/
        ├── init.sh.template
        ├── upgrade.sh.template
        └── uninstall.sh.template
```

## 文件说明

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

## 适用原则

- 先本地纳管，再考虑上架
- 先按模板生成，再按项目调整
- 先能安装，再谈美观
- 先验证升级卸载，再谈提交 PR
