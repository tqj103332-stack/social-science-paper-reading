# 脚本使用说明

本目录包含两个 PDF 处理脚本，用于在精读前获取论文全文文本。

## 依赖安装

脚本基于 Python，需先安装依赖：

```bash
# Python 包（pymupdf 提取文本；pytesseract + pillow 用于 OCR）
pip install pymupdf pytesseract pillow

# 系统 Tesseract OCR 引擎（macOS）
brew install tesseract tesseract-lang
#   tesseract         —— OCR 引擎本体
#   tesseract-lang    —— 语言包（含中文 chi_sim；只处理英文论文可省略，用 --lang eng）

# Linux（Debian/Ubuntu）
sudo apt install tesseract-ocr tesseract-ocr-chi-sim
```

> 注意：如果使用 WorkBuddy 的隔离 Python 环境，`pip` 需替换为该环境下的路径，
> 例如 `~/.workbuddy/binaries/python/envs/default/bin/pip install ...`。

## extract_pdf.py —— 提取文本 + 扫描版检测

优先使用本脚本提取 PDF 文字层，并自动判断是否为扫描版。

```bash
python extract_pdf.py paper.pdf -o paper.txt
```

- `-o/--output`：输出文本文件（省略则打印到标准输出）。
- `--min-chars 100`：判定扫描版的平均每页字符数阈值（默认 100）。
- 检测信息打印到 stderr，不混入正文。

若输出提示「判定为扫描版/图片型 PDF」，改用 `ocr_pdf.py`。

## ocr_pdf.py —— 扫描版/图片型 PDF 的 OCR

当 PDF 无文字层时，用本脚本做 OCR 识别。

```bash
python ocr_pdf.py paper.pdf -o paper_ocr.txt --lang chi_sim+eng --dpi 300
```

- `-o/--output`：输出 OCR 文本。
- `--lang`：OCR 语言，默认 `chi_sim+eng`（中文+英文）；纯英文论文用 `--lang eng`。
- `--dpi`：渲染分辨率，扫描件建议 300（越高越清晰但越慢）。
- `--pages`：页范围，如 `1-10` 或 `3,5,8`（省略处理全部）。

## 处理策略建议

1. 论文有文字层（电子版）→ 直接用 Read 工具读取，或 `extract_pdf.py` 提取。
2. 论文是扫描版/图片型 → 用 `ocr_pdf.py` 做 OCR，中英混排用 `chi_sim+eng`。
3. OCR 结果可能存在错字，精读时对关键数字、专有名词、公式需结合上下文校正。
