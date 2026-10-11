# 内部数据与脚本

以 assets/step-plan.template.json 为字段模板，空字段不是可运行计划。按实际原稿填完整数据，work_type=ARTWORK_TUTORIAL。脚本要求真实源路径/哈希、七项 DNA、色值、职责、来源、操作依赖与十个实际动作页。schema_version=1.1.0。

operations 是工艺节点，每个 REQUIRED 节点恰好映射一页，可由同页有序小动作共同构成目标；depends_on 必须更早执行。operation_ids 顺序是同页动作顺序。十页前置文字必须自足；脚本只证明字段/依赖，不自动证明中文可操作。
每页 references 包含 source.id；02–10 还含前页编号。white_regions 是画布中无字无画的白色矩形 [x0,y0,x1,y1]，不能遮去整页背景问题。
native_name 仅在 VERIFIED/VERIFIED_METADATA 且有真实源哈希时填写；推荐类别写 role/alternative，未核实名称留 null。表格无宏、公式或在线取图。

内部 review.template.json 的门禁默认为 NOT_RUN。实际查看后记录 basis、reviewer、method、time、scope；填写当前 plan SHA256 与各 PNG SHA256。计划或 PNG 改变使原记录失效。SYNTHETIC_TEST 只供代码测试，打包输出 PACKAGE_TEST_PASS，不能称艺术测试。

从 Skill 根目录执行（业务文件放独立 WORK_DIR）：

```bash
python scripts/inspect_input.py /absolute/artwork.png --role ARTWORK_MASTER
python scripts/select_assets.py KB-MANIFEST.json tutorial
python scripts/validate_plan.py /absolute/WORK_DIR/plan.json
python scripts/verify_pages.py /absolute/WORK_DIR/plan.json /absolute/WORK_DIR --review /absolute/WORK_DIR/review.json
python scripts/build_workbook.py /absolute/WORK_DIR/plan.json /absolute/WORK_DIR
python scripts/package_delivery.py /absolute/WORK_DIR/plan.json /absolute/WORK_DIR /absolute/WORK_DIR/review.json /absolute/OUTPUT/作品_10步画法.zip
```

依赖：Pillow、openpyxl；创建工具使用 PyYAML。requirements.txt 固定本次实际运行版本。PSD 可选适配器无依赖时按设计返回代码 2 与 PSD_RUNTIME_UNAVAILABLE；明确启用前选择并锁定 psd-tools 版本，本发行不安装未经测试的可选库。

verify_pages 没给 review 时只做结构检查；最终 package_delivery 必须有匹配当前文件的完整通过记录。颜色要求明确 sRGB profile 或 PNG sRGB 标记；不凭无标记文件推定。必要时通过支持的导出/颜色管理工具转换，不能改名或伪写色彩空间。
