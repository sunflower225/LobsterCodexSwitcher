## 1. OpenSpec And Skill Planning

- [x] 1.1 完成 proposal/design/specs，明确项目内 Skill、Agent CLI、部署入口的要求
- [x] 1.2 确定 Skill 目录结构、frontmatter 与 references 拆分方式

## 2. Project-Local Skill

- [x] 2.1 使用 skill-creator 初始化项目内 Skill 骨架
- [x] 2.2 编写 SKILL.md，覆盖用户与 Agent 的主要工作流
- [x] 2.3 编写 references/examples，说明 CLI 参数、排序规则与部署路径

## 3. Agent CLI Commands

- [x] 3.1 为 codex-switcher 增加 argparse 非交互入口
- [x] 3.2 实现账号列表排序、JSON 输出和最佳账号选择
- [x] 3.3 实现按 selector 切换账号与非交互存档当前账号

## 4. Global Install Paths

- [x] 4.1 增加标准 Python 入口元数据，支持更快的全局安装
- [x] 4.2 保持 install.py 兼容，并在 README 中补充新旧安装方式

## 5. Verification

- [x] 5.1 验证 Skill 文件结构和内容符合预期
- [x] 5.2 验证 CLI 参数在文本输出和 JSON 输出下均可用
- [x] 5.3 验证新的全局安装入口与现有 install.py 路径都可工作
