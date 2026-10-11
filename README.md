# Procreate 插画画法教程工作室

版本：**1.1.0**。建议仓库：`wakazhangjiahuang/procreate-tutorial-studio`，可见性选择 **Private**。

这是与账号当前部署版本一致的 Skill 源码和知识资产包。用于将一张用户原稿转化为十张独立中文 Procreate / 手绘画法过程图，以及一份详细资料表格。账号中的插件可以使用随包资产运行；本仓库上传完成后，可作为版本化知识来源。

## 上传到 GitHub

1. 创建名为 `procreate-tutorial-studio` 的私有仓库。
2. 解压下载的 ZIP，进入里面的 `procreate-tutorial-studio` 文件夹。
3. 将文件夹**里面的全部文件与目录**上传至仓库根目录，不要把 ZIP 本身作为知识资料上传，也不要额外套一层同名目录。
4. 确认仓库根目录直接出现 `KB-MANIFEST.json`、`SKILL.md`、`requirements.txt`，并保留 `assets/`、`references/`、`scripts/`、`sources/`、`LICENSES/` 和 `agents/` 的原有路径。
5. 上传完成后，把仓库链接提供给助手。核实真实文件和提交 SHA 后，再同步 `sources/REGISTRY.json` 与部署版。当前 `PREPARED_NOT_UPLOADED` 是交付时状态，不能提前改成已读取远端；不要猜测 commit SHA。

仓库建议地址：https://github.com/wakazhangjiahuang/procreate-tutorial-studio

## 核心行为

- 原稿决定题材、身份、时代风格、笔触、线条、轮廓、色值关系、上色与画法。
- 教程样例只提供教学组织与版式；不引入样例题材、配色或画法。
- 十张全部承担真实绘画动作。第一张开始绘制，第十张完成最后一个具体操作；封面由用户的独立系统负责。
- 每页记录前置状态、操作区域、图层、工具、动作、可见变化与完成标准，并核验九次相邻转换。
- 默认十张独立 PNG，3:4、3072×4096、sRGB、干净纯白页面。实际像素必须解码验证；非原生输出需在同一表格说明处理方法和限制。
- 不新增原稿没有的体积、高光、柔光、渐变、纸底或氛围渲染，不用透明度和滤镜假装绘制过程。
- 只有成品时采用“依据原稿推演的可复现画法”；分层不等于真实历史；未经证据支持，不填写原作者的准确笔刷名和参数。

## 两类交付严格分开

**本仓库包**保存规则、模板、脚本和来源记录，供安装、维护与复用。

**实际作品 ZIP**仅包含十张独立 PNG 和 `原稿风格与画法资料.xlsx`，恰好 11 个文件。表格包含五张工作表：原稿视觉 DNA、色值与对象、十步画法、笔刷与操作、资料来源。内部计划和评审记录不进入作品包。

## 文件职责

| 路径 | 用途 |
|---|---|
| `SKILL.md` | 触发条件、完整执行链路与异常处理 |
| `KB-MANIFEST.json` | 按任务选择资源的入口、路径与 SHA256 |
| `references/` | 原稿识别、样例隔离、笔刷证据、递进、验收、数据契约、多仓库路由 |
| `assets/` | 内部十步计划、单页提示词、评审模板与五表 XLSX 模板 |
| `scripts/` | 输入检查、依赖验证、尺寸/颜色验证、表格生成、11 文件白名单打包与可选 PSD 读取 |
| `sources/` | 多个 GitHub 来源的职责、固定版本与实际读取范围 |
| `LICENSES/` | 第三方许可和改编归属 |

## 已提炼的来源

| 来源 | 采用范围 |
|---|---|
| 用户已有过程重建 Skill | 输入审计、过程证据与交付方式；已按本教程契约改写 |
| `wakazhangjiahuang/brush` | 工艺、材质、笔刷职责和证据方法；按固定版本按需读取，不镜像原生笔刷与商业素材 |
| `JimLiu/baoyu-skills` | 经过改编的页面内容分块与提示词组织；删除封面链、CTA、固定配色及模型逻辑 |
| `psd-tools/psd-tools` | 可选 PSD 事实读取接口；不作为 `.procreate` 或历史过程解析器 |

上述来源详情与固定提交保存在 `sources/REGISTRY.json`。过程重建 Skill 的独立 GitHub 地址尚未核实，保留空值，不填写猜测地址。

本项目的自写代码及用户资料不在本次交付中自动宣布开源；第三方 MIT 声明保留于 `LICENSES/`。仓库不包含用户原稿、客户资料、商业笔刷、发布文案或测试生成图。

## 运行检查

使用 Python 3.10 或更高版本。当前已实测 Python 3.12、Pillow 12.3.0、openpyxl 3.1.5；运行依赖锁定在 `requirements.txt`。

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s scripts/tests -v
python scripts/select_assets.py KB-MANIFEST.json tutorial
```

其他任务入口：`analysis`、`planning`、`production`、`review`、`delivery`、`routing`、`psd`。业务运行顺序见 `references/data-contract.md`。

`psd-tools` 是未捆绑的可选依赖；普通 PNG/JPEG 输入不需要安装。缺少该依赖时可采用导出的分层 PNG。

本次部署核验：十项合成脚本测试通过、25 项 Manifest 资产哈希一致、八个入口可解析、Skill 结构检查通过。合成测试验证契约与文件流程，不证明真实插画视觉质量、中文生图保真或 Procreate 真机复现。

## 启动示例

在 ChatGPT 中选择「Procreate 插画画法教程工作室」，上传插画原稿；样例图、分层稿或录屏可以同时提供。

> 使用本轮原稿制作十张独立中文 Procreate 画法过程图。深度识别原稿的时代风格、笔触、线条、轮廓、上色与色值关系，保持同一作品身份和画法；样例只用于教学版式。十张都用于实际操作，检查步骤递进和间隔，默认纯白底、3:4、4K。最终只交付十张 PNG 与一份详细风格及画法 XLSX 的压缩包。
