# 1Panel Local App Packaging Workflow

## A. 本地纳管流程

1. 确定应用 key 和版本号
2. 使用 `1panel app init -k <app-key> -v <version>` 生成模板
3. 把 Docker Compose 改成目标服务
4. 配置端口、环境变量、卷和健康检查
5. 补全顶层 `data.yml` 和版本目录 `data.yml`
6. 写安装、升级、卸载脚本
7. 本地安装验证

## B. AppStore 提交流程

1. fork `1Panel-dev/appstore`
2. clone `dev` 分支
3. 新建分支：`app/<app-name>`
4. 按规范放入应用目录
5. 补充 README、logo、版本目录
6. 本地验证
7. 提交 PR

## C. 决策顺序

如果目标不清楚，先按下面顺序判断：

- 只是要 1Panel 管理：优先本地纳管
- 想让别人也能装：整理成规范包
- 想进入官方仓库：再准备 AppStore 提交

## D. 常见失败点

- 版本号带 `v`
- 顶层和版本目录的 `data.yml` 混淆
- Compose 使用了本机硬编码路径
- 数据卷权限不对
- 只验证能启动，没有验证升级和卸载

## E. 最小验收

一个合格的本地应用，至少要能回答这些问题：

- 安装后能不能进 1Panel 管理
- 参数能不能在表单里改
- 重启会不会丢数据
- 升级会不会破坏现有数据
- 卸载后会不会误删持久化数据
