# Question workspace（解题工作区）

复制本文件夹来启动一道新题 / 一个新案例。这是 DFTK skill 在 Agent 处理多题取证任务时
期望的标准布局 —— 把「原始检材」「推理输出」「答案」分开，保证可复现、可审计。

```text
question-workspace/            # 复制后改名为案例 id，例如 nlyzgnx-2026-0811/
├── question.md                # 题目原文；一题一行也可以
├── evidence/                  # 原始检材，只读保存，绝不改动
│   ├── phone/                 # 手机备份、聊天导出、媒体
│   ├── apk/                   # 安装包、dex、资源文件
│   ├── server/                # 镜像、日志、数据库 dump
│   ├── pcap/                  # 流量包
│   └── <type>/                # 其他证据类型，按需增删子目录
├── work/                      # Agent 输出、解包、分析 —— 交给 AI 自己操作、规划
├── answers/                   # answer_slots.json（机器可读答案槽）+ 答案卡 markdown
└── tools/                     # 统一工具脚本：DFTK 探测到的 / 本机装的 / 用户提供的，不强求
```

## 初始化（一行）

```bash
cp -r <skill>/templates/question-workspace <案例id> && cd <案例id>
```

`<skill>` 即已安装的 dftk skill 根目录（如 `~/.workbuddy/skills/dftk`）。填完答案后运行
`python tools/validate_answers.py` 自检结构与证据路径。

## 规则

- `evidence/` 是**只读**的。原始检材放这里，绝不在原地改动。DFTK 本身是只读工具；
  如果必须解包 / 解码，把产物写到 `work/`。
- `work/` 是 Agent 的草稿区 —— 解包、解码输出、中间分析都放这里。由你（Agent）自己
  规划、操作。
- `answers/answer_slots.json` 是机器可读的答案表（格式见 `../../references/answer-slots.md`）。
  需要时也可在这里放一份人读的答案卡 `../../templates/answer-card.md`。
- `tools/` 放你通过 `dftk_doctor` 探测到的外部工具、本机已有的、或用户提供的辅助脚本。
  不强求 —— DFTK 自带能力已覆盖大部分需求。

## 工作流

1. 复制本文件夹，改名为案例 id。
2. 把原始检材放入 `evidence/<type>/`，记录其哈希。
3. 从用户的真实诉求（claim）出发（SKILL.md §2）。每一题先想清楚「需要什么证据才算数」，
   再去找。
4. 用 DFTK（优先 MCP，CLI 兜底）产出 Observation；派生产物写进 `work/`。
5. 诚实填写 `answers/answer_slots.json` —— `status` 取自 SKILL.md §10，`evidence[]` 写来源。
6. 每道 claim 的证据需求满足或确已穷尽时停止（SKILL.md §11）。

## 配合其它 skill 文档

- 推理方法：SKILL.md §2（claim-first）、§7（证据模型）、§10（verification levels）。
- 答案格式：`../../references/answer-slots.md`；人读答案卡：`templates/answer-card.md`。
- 领域参考：SKILL.md §14（android / mobile / network / database / …）。
