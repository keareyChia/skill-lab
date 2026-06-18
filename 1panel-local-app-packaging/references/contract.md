# 1Panel Local App Packaging

## 目的

把自定义 Docker / Docker Compose 应用包装成 1Panel 能识别、能安装、能升级、能卸载的本地应用，并准备好未来提交到 1Panel AppStore 的规范化材料。

## 目录契约

### 顶层文件

- `data.yml`：应用声明
- `README.md`：应用说明
- `logo.png`：应用图标

### 版本目录

- 版本目录名示例：`1.0.0/`
- 目录名不要带 `v`
- 版本目录下至少包含：
  - `data.yml`
  - `docker-compose.yml`
  - `data/scripts/`

## 标准结构

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

## 关键流程

1. 先确认目标：本地纳管还是 AppStore 提交
2. 用 `1panel app init -k <app-key> -v <version>` 生成模板
3. 把 Compose 项目迁移进去
4. 配好表单、环境变量、卷和健康检查
5. 写安装、升级、卸载脚本
6. 本地验证后再考虑提交 PR

## 验证清单

- 1Panel 能识别并安装
- 环境变量能配置
- 数据卷可持久化
- 容器重启后状态正常
- 升级和卸载不破坏数据
- README 能让人快速看懂用途和边界

## 模板文件

- `templates/app-data.yml.template`
- `templates/version-data.yml.template`
- `templates/docker-compose.yml.template`
- `templates/scripts/init.sh.template`
- `templates/scripts/upgrade.sh.template`
- `templates/scripts/uninstall.sh.template`

## 适用原则

- 先本地纳管，再考虑上架
- 先按模板生成，再按项目调整
- 先能安装，再谈美观
- 先验证升级卸载，再谈提交 PR
