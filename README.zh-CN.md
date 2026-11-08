<p align="center"><a href="README.md">English</a> &nbsp;·&nbsp; <strong>简体中文</strong></p>

<p align="center"><img src="assets/logo.svg" width="54" height="54" alt=""></p>
<h1 align="center">diffnote</h1>
<p align="center"><strong>先把改动理清，再写 PR。</strong></p>
<p align="center">把本地 Git 变更整理成可修改的草稿：改动区域、文件元数据、增删行数，以及有来源的复核线索。无需模型或服务器。</p>
<p align="center"><a href="#快速开始">快速开始</a> &nbsp;·&nbsp; <a href="#实际使用">使用方式</a> &nbsp;·&nbsp; <a href="docs/guide.zh-CN.md">完整手册</a> &nbsp;·&nbsp; <a href="CONTRIBUTING.md">参与贡献</a></p>

<p align="center"><a href="assets/demo.gif" title="点击查看原尺寸演示"><img src="assets/demo.gif" width="860" alt="从工作区、暂存区生成草稿，再查看文件元数据、审阅线索与 JSON 输出。"></a></p>

从工作区、暂存区生成草稿，再查看文件元数据、审阅线索与 JSON 输出。 [录制与复现](docs/showcase.md)。

## 为什么需要它

diff 告诉你改了什么，PR 还需要有用的解释。diffnote 先从所选改动整理事实；再由你补上“为什么改”和真正执行过的验证。

## 快速开始

需要 macOS / Linux、Python 3.11+ 与 Git 2.31+。演示使用临时合成 Git 数据，安装可能下载构建工具。

`0.2` 源码位于 `noah/diffnote` 分支，仓库默认 `main` 仍是旧 `0.1` 接口。请明确选择分支：

```bash
git clone --branch noah/diffnote https://github.com/LucasXlab/diffnote.git
cd diffnote
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
python scripts/demo.py
```

保持环境已激活，进入自己的项目，确认要描述的改动：

```bash
cd /absolute/path/to/your/repo
git diff --cached --stat
diffnote --staged --markdown --output pr-draft.md
```

打开 `pr-draft.md`，核对文件和增删行数，再补上**为什么改**以及实际做过的验证。没有选中改动时得到空草稿，不表示整个工作区没有改动。`--output`（别名 `--save`）以私有权限新建文件，拒绝覆盖已有文件；分析报错不创建输出。下一份草稿请换文件名。

`0.2` 接口不调用模型，不提供旧版 `--llm`、`--color`；保留 `--no-color`、Markdown 与 JSON。CLI 报告文字目前使用英文。

## 实际使用

### 先描述下一次提交

```bash
diffnote --staged --markdown
```

此命令只选暂存区；不加 `--staged` 时检查已跟踪工作树，包含已暂存修改。未跟踪文件只有暂存后才进入报告。

### 选择分支比较，或导出结构化结果

```bash
diffnote --base main --markdown
diffnote --range main...feature --markdown
diffnote --staged --json
```

`A..B` 比较提交端点，`A...B` 比较共同祖先至 B。工作树 / 暂存草稿标题取自当前路径，不借用无关的旧提交标题。

退出 `0` 仅表示支持范围内的分析完成，不是批准改动；退出 `2` 包括参数、Git、限额、超时和解析失败。工具不会执行项目测试。

## 适用边界

草稿不证明意图、语义正确或安全。不支持的补丁与不完整 Git 数据会明确失败。报告含真实路径和标题，分享前须检查；配置与 helper 防护也不构成恶意 Git 程序沙箱。

详细参数、更多演示和技术边界见[中文使用手册](docs/guide.zh-CN.md)。

## 参与贡献

请从[贡献指南](CONTRIBUTING.md)开始，使用合成输入复现问题，并报告实际执行的验证。

[MIT 许可证](LICENSE) · [English](README.md)
