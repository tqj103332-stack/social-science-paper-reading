#!/usr/bin/env python3
"""extract_pdf.py — PDF 文本提取 + 扫描版检测

用于社会科学论文精读：从 PDF 提取纯文本，并自动检测是否为扫描版
（扫描版没有可提取的文字层，需要走 OCR 兜底）。

用法：
    python extract_pdf.py <input.pdf> [--output out.txt] [--min-chars 100]

说明：
    - 提取到的文本写入 --output（省略则打印到 stdout）。
    - 检测信息（页数、字符数、是否扫描版）打印到 stderr，不混入正文。
    - 当判定为扫描版时，提示改用 ocr_pdf.py。

依赖：pymupdf
安装：pip install pymupdf
"""

import argparse
import sys


def get_fitz():
    """导入 PyMuPDF，兼容新旧包名，缺失时给出安装指引。"""
    try:
        import pymupdf as fitz  # 新包名
    except ImportError:
        try:
            import fitz  # 旧包名
        except ImportError:
            sys.stderr.write(
                "[错误] 缺少 PyMuPDF 依赖。请先安装：\n"
                "    pip install pymupdf\n"
            )
            sys.exit(2)
    return fitz


def extract_text(fitz, path: str):
    """逐页提取文本，返回 (全文字符串, 每页字符数列表)。"""
    doc = fitz.open(path)
    pages_text = []
    char_counts = []
    for page in doc:
        text = page.get_text("text")
        pages_text.append(text)
        char_counts.append(len(text.strip()))
    doc.close()
    return "\n".join(pages_text), char_counts


def main():
    parser = argparse.ArgumentParser(
        description="从 PDF 提取文本并检测是否为扫描版"
    )
    parser.add_argument("input", help="输入的 PDF 文件路径")
    parser.add_argument("--output", "-o", help="输出文本文件路径（默认打印到 stdout）")
    parser.add_argument(
        "--min-chars", type=int, default=100,
        help="判定扫描版的平均每页字符数阈值（默认 100）",
    )
    args = parser.parse_args()

    fitz = get_fitz()

    try:
        full_text, char_counts = extract_text(fitz, args.input)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"[错误] 无法读取 PDF：{e}\n")
        sys.exit(1)

    total_chars = sum(char_counts)
    n_pages = len(char_counts)
    avg_chars = total_chars / n_pages if n_pages else 0
    blank_pages = sum(1 for c in char_counts if c == 0)

    is_scanned = avg_chars < args.min_chars

    sys.stderr.write(
        f"[检测] 页数={n_pages}  总字符={total_chars}  平均每页={avg_chars:.0f} 字符"
        f"  空页={blank_pages}\n"
    )
    if is_scanned:
        sys.stderr.write(
            f"[检测] 判定为扫描版/图片型 PDF（平均每页字符 {avg_chars:.0f} < 阈值 "
            f"{args.min_chars}）。建议改用 ocr_pdf.py 做 OCR 识别。\n"
        )
    else:
        sys.stderr.write("[检测] 存在可提取的文字层，可直接使用提取文本。\n")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(full_text)
        sys.stderr.write(f"[完成] 文本已写入 {args.output}\n")
    else:
        sys.stdout.write(full_text)


if __name__ == "__main__":
    main()
