---
name: procreate-tutorial-studio
description: 将用户插画原稿制作成十张独立中文 Procreate/手绘画法过程图并交付详细风格与操作 XLSX；用于原稿画法拆解、十步教程、按样例组织教程版式。保持同一原稿身份、时代气质、笔触、线条和上色，默认纯白底、3:4、4K。样例只提供教学组织与版式。不用于十张不同插画、单独自媒体封面、原生笔刷构建或无字视频分镜。
---

# Procreate 插画画法教程工作室

按 v1.1.0 执行，独立运行，不依赖 Skill Box。

## 交付约束

- 十张都承担实际绘画、上色、局部修改或清理动作；01 开始绘制，10 完成最后一个真实操作。封面由用户另一个系统负责，不占十张。
- 默认十个独立 PNG，3:4、3072×4096、sRGB、页面底色 #FFFFFF。禁止合集、合并、九宫格、多阶段拼版、背景纸纹和新增氛围渲染。
- ZIP 只含十 PNG 和“原稿风格与画法资料.xlsx”，恰好 11 成员。不附封面、原稿副本、发布文案、独立计划、QA 报告、提示词、清单、字体或笔刷。
- 保留原稿真实画法；不新增原稿没有的 3D、光泽、柔光、平滑渐变、统一噪点或过度细节。不用滤镜、淡入、全图透明度模拟过程。
- 原稿决定画什么与怎么画；样例只决定教学组织和版式。固定十页不意味着固定工艺或笔刷数量。
- 本发行脚本验证上述十图规格。用户明确改变规格时显式修改并验证契约，不能让脚本覆盖用户要求。

## 执行链路

1. 盘点材料并隔离 ARTWORK_MASTER、PROCESS_EVIDENCE、LAYOUT_REFERENCE。无原稿只请求上传原稿；不把教程样例或最近其他作品升格为原稿。多稿确定主稿。
2. 实际查看原稿及局部，运行 scripts/inspect_input.py。读取[原稿与证据](references/artwork-and-evidence.md)，提炼时代风格、笔触、线条、轮廓、上色、色值、材质、尺度与留白。以占比大且决定身份的核心为主，小面积重要五官仍锁定；区分角色、主体、物品、点缀、环境、建筑、背景的核心色值组合。
3. 有样例时读取[教程版式](references/layout-and-text.md)，移除题材、媒介、笔刷信息再提炼 LayoutSpec；封面、双状态、暖纸底按本契约改为操作页、单状态、白底。
4. 选择 REAL_FRAME、LAYER_RECONSTRUCTION 或 REASONED。实际看过记录才支持实录；分层不证明历史；成品推演不虚构原作者笔刷、参数或工时。逐步记录混合证据。
5. 读取[多仓库路由](references/source-routing.md)，按 KB-MANIFEST.json 精准选择随包资产；需要 brush 时先取 Registry 固定版本 Manifest，再取相关文件。校验来源版本，禁止全仓扫描或盲从 main。可选源缺失用随包规则和职责表述回退。
6. 读取[工艺与笔刷](references/process-and-brush.md)和[递进检查](references/progression-gates.md)。建立 REQUIRED/OPTIONAL/NOT_APPLICABLE 操作依赖，把所有必需操作与重要材质映射到十页。每页填写前置状态、区域、图层、工具、动作、可见变化、完成标准。
7. 用 assets/step-plan.template.json 建内部计划。核对首步启动、九次相邻转换和第十步终态。禁止封面、纯检查、总结、成品展示充数。无法支持十个真实节点时先拆真实子动作，仍不足则说明缺口并请求过程资料或数量调整。
8. 使用当前可用图像生成/编辑能力逐张制作；编辑已有图像使用受支持的图像编辑工具。默认遵从用户最新可用 GPT 图像模型偏好；“GPT image 2.5”偏好不能冒充未经工具确认的真实调用身份。核实参考图、独立出图、中文与尺寸能力；不能只写“4K”就宣称达标。
9. 按 assets/page-prompt.template.md 组装。每张实际引用原稿，02–10 还引用已通过前序状态；原稿锁身份、前序锁状态。只改变当前声明内容，未来细节不抢跑。默认一致全景视图，必要单一局部裁切记录变换；视图变化不是绘画增量。
10. 中文默认清晰手写字感，与原稿时代气质协调。采用准确操作、工具/笔触简述和完成标准；不假定唯一内置“Procreate 字体”。有授权字体/用户手写可用，图中文字逐字核对，不遮关键笔触。
11. 读取[验收与修复](references/review-and-delivery.md)。逐张实际查看身份、画法、动作、文字、白底与去渲染，评审九次转换。失败页及后续依赖修复。按 assets/review.template.json 记录依据和真实文件 SHA256，未查看不填 PASS。
12. 按[数据与脚本](references/data-contract.md)运行 validate_plan.py、verify_pages.py、build_workbook.py、package_delivery.py。用五表模板生成一份详细 XLSX；规划/QA 留内部，最终仅交付业务 ZIP。
13. 按实际结果报告。PACKAGE_PASS 是文件/表格/已记录结论一致，不证明 Procreate 真机试画或平台效果；未执行保留 NOT_RUN。

## 条件资源与异常

- PSD：scripts/inspect_psd.py 只读事实。无 psd-tools 可用分层 PNG 回退；不阻断普通 PNG/JPG，不冒充 .procreate 解析器。
- 精确笔刷：遵守[证据规则](references/process-and-brush.md)。VERIFIED_METADATA 不是试画；名称/路径不是画感。有来源才写准确名称，否则职责与可观察行为。
- 远端资料缺失：遵守[路由](references/source-routing.md)。继续不依赖该源的部分，停止缺失资产的精确结论。自有仓库尚未上传不能假称已读取。
- 中文/尺寸不足：使用已授权、有能力的工具修复，不静默改规格或伪称原生 4K。超分方法与限制写同一表格，不重绘笔触。

内部 plan.json、review.json、原稿、状态与预览留业务工作目录；白名单打包不遍历目录。第三方许可在 Skill 内 LICENSES/，业务包不分发代码/字体。当前 Skill 的保存与维护资料不混入作品交付。
