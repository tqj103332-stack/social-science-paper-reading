# 社会科学论文精读（social-science-paper-reading）

> A WorkBuddy skill for deep, structured reading of social science papers.

一个专门用于**社会科学论文深度精读**的 WorkBuddy 技能。它针对社会科学论文的特点，围绕「研究问题 → 研究动机 → 方法机制 → 实验验证 → 结论」五个维度展开结构化解析，并把五维度串联成一条从研究背景到结果的完整理解链条，帮助读者把一篇论文读懂、读透、读成自己的知识。

## 功能特性

- **五维度结构化分析**：研究问题、研究动机、方法机制、实验验证、结论，每个维度都要求给出原文依据，不凭空概括、不编造数据。
- **逻辑串联**：把五维度连成「现象 → 问题 → 方法 → 证据 → 结论」的可复述因果叙事。
- **社科方法速查**：内置识别策略表（RCT/DID/IV/RDD/PSM/固定效应等）、效度威胁清单、8 项方法质量判据，用于批判性评析。
- **PDF 读取 + OCR**：三级兜底——内置 Read 直接读 PDF → `extract_pdf.py` 提取文本并检测扫描版 → `ocr_pdf.py` 对扫描版/图片型论文做 OCR 识别。
- **中文输出**：默认简体中文精读报告，英文论文保留关键术语原文并注译。

## 分析框架

| 维度 | 解析内容 |
|------|----------|
| 研究问题 | 核心问题、问题类型（描述/解释/预测）、文献位置 |
| 研究动机 | 现实 / 理论 / 文献三层动机 |
| 方法机制 | 数据、识别策略、变量、因果机制、内生性威胁 |
| 实验验证 | 主要发现、稳健性/安慰剂/异质性/机制检验、可靠性 |
| 结论 | 核心结论、贡献、局限、未来方向 |

五维度解析后，用一句话因果叙事串联全文：

```
现象/问题（动机） → 研究问题（切入点） → 方法（如何回答） → 证据（验证结果） → 结论（贡献与局限）
```

## 目录结构

```
social-science-paper-reading/
├── SKILL.md                           # 技能入口：工作流 + 输出模板
├── references/
│   ├── analysis-framework.md          # 五维度详细判别要点 + 追问清单
│   └── social-science-methods.md      # 社科研究方法速查
└── scripts/
    ├── extract_pdf.py                 # PDF 文本提取 + 扫描版自动检测
    ├── ocr_pdf.py                     # 扫描版/图片型 PDF 的 OCR
    └── README.md                      # 脚本用法与依赖安装
```

## 安装

1. 将本目录复制（或解压）到 WorkBuddy 的技能目录：

   ```bash
   # 用户级（跨项目可用，推荐）
   cp -r social-science-paper-reading ~/.workbuddy/skills/

   # 或项目级（团队共享）
   cp -r social-science-paper-reading <项目>/.workbuddy/skills/
   ```

2. 重启或刷新 WorkBuddy，技能即生效。

## 使用方法

### 触发技能

在 WorkBuddy 对话中，把论文 PDF 拖入对话并说「精读这篇论文」「帮我分析这个 PDF」等，技能会自动加载并输出结构化精读报告。

### 手动提取文本 / OCR

当 PDF 无法直接读取时，使用脚本：

```bash
# 提取文字层 + 检测是否扫描版
python scripts/extract_pdf.py paper.pdf -o paper.txt

# 扫描版/图片型 PDF → OCR（中英混排）
python scripts/ocr_pdf.py paper.pdf -o paper_ocr.txt --lang chi_sim+eng --dpi 300
```

### 依赖

首次使用 OCR 前需安装：

```bash
pip install pymupdf pytesseract pillow
brew install tesseract tesseract-lang   # macOS；tesseract-lang 提供中文语言包
```

详见 `scripts/README.md`。

## 输出模板

精读报告按以下结构输出：

1. 一句话总结
2. 研究问题
3. 研究动机
4. 方法机制
5. 实验验证
6. 结论
7. 逻辑串联（完整理解链条）
8. 批判性评析

## License

[MIT](LICENSE)
