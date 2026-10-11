# 验收与交付

实际逐张查看 identity/style/actionable/delta_matches/text_exact/no_overrender/white_background，记录具体依据与 PNG SHA256。未看 NOT_RUN、失败 FAIL，不自动填 PASS。九次转换核对 preconditions/gap/continuity/no_future_content；另判 first_step_startable/terminal_matches_master。评审绑定 plan SHA256，文件变更后重新评审对应页及后续依赖。

白底机械检查使用每页声明的空白矩形，必须处于画布内，不能替代完整视觉检查。正常字边抗锯齿不在空白区。像素差比值不代表画法合理，不要求第十张不同于原稿。

通过需要操作依赖覆盖、PNG 解码/尺寸/sRGB、空白区、所有当前文件的视觉记录、五表内容与计划一致、ZIP 集合/CRC/字节哈希。五表：原稿视觉DNA、色值与对象、十步画法、笔刷与操作、资料来源。十步恰好十行对应十图。参数建议/证据/限制属于资料字段，不另建 QA 表；无宏、在线图片或外部公式。

ZIP 平铺十 PNG 与 原稿风格与画法资料.xlsx，11 成员。只白名单，不附原稿、清单、README、文案、计划、报告、提示词、隐藏文件、字体或笔刷。
PACKAGE_PASS 表示结构/内容/已记录结论一致，不证明真机或平台效果；未试画 NOT_RUN。内部测试图形不得称为本作品或艺术验证。
