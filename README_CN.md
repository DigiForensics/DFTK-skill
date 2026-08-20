# DFTK Skill

这是 [DigiForensics/DFTK](https://github.com/DigiForensics/DFTK) 的独立 Agent Skill。

DFTK 提供结构化的取证能力和 `Observation / Evidence` 结果。本仓库提供调查指引，帮助 Agent 明确证据需求、选择能力、核验发现并在报告中标注来源。

## 安装

将 DFTK 主仓库地址直接交给 Agent：

```text
https://github.com/DigiForensics/DFTK
```

Agent 应安装 `dftk[mcp]`；随后 `dftk agent setup --install-skill` 会自动拉取匹配版本的
完整 DFTK-skill，并生成可审核的 MCP 配置片段。完整且安全的步骤见 [INSTALL_AGENT.md](INSTALL_AGENT.md)。

## 版本

`3.4.0`，与 DFTK `3.4.x` 对齐。

## 安装

请安装完整的 Skill 目录，包括 `references/`、示例、模板和 `skills/`。仅复制入口文件无法提供完整指引。

常见目录：

```text
~/.agents/skills/dftk/
~/.kimi-code/skills/dftk/
~/.workbuddy/skills/dftk/
~/.claude/skills/dftk/
~/.codex/skills/dftk/
~/.hermes/skills/dftk/
```

推荐通过 `dftk agent setup` 完成对应版本快照的安装和 MCP 配置准备：

```bash
dftk agent setup --root <只读证据目录> --workspace <可写案件目录> --install-skill
```

## 目录结构

```text
dftk/
  SKILL.md            # 入口和调查范围说明
  references/         # 按需读取的专题指引
  examples/           # 调查示例
  templates/          # 输出报告模板
```

## 设计边界

本仓库包含指引和模板，不含取证解析器或 Agent 运行时。可执行能力由 `DFTK` 主仓库和 PyPI 包提供。

生成的[能力目录](references/capabilities.md)与对应的 DFTK 发布 manifest 保持一致。

文档归属和专项 Skill 格式见英文 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 维护者

- **维护者：** [DyNooob](https://github.com/DyNooob) — DigiForensics · [博客](https://buno.dev)
- **所属组织：** [DigiForensics](https://www.digiforensics.cn) · [LLMCN](https://www.llmcn.org)
- **许可证：** [Apache-2.0](LICENSE)
