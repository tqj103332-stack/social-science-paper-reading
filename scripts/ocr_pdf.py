#!/usr/bin/env python3
"""ocr_pdf.py — 扫描版/图片型 PDF 的 OCR 识别

用于社会科学论文精读：当 PDF 无文字层（扫描版、图片型）时，
将每一页渲染为高清图片，再调用 Tesseract OCR 引擎识别文字。

用法：
    python ocr_pdf.py <input.pdf> [--output out.txt] [--lang chi_sim+eng]
                   [--dpi 300] [--pages 1-10]

说明：
    - 渲染分辨率由 --dpi 控制，扫描件建议 300。
    - --lang 指定 OCR 语言（中文+英文默认 chi_sim+eng；纯英文用 eng）。
    - --pages 指定页范围（如 1-10 或 3,5,8），省略则处理全部页面。

依赖：
    pip install pymupdf pytesseract pillow
    系统 Tesseract：macOS 用 `brew install tesseract tesseract-lang`
                   （tesseract-lang 提供 chi_sim 中文语言包）
"""

import argparse
import io
import sys


def get_fitz():
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz
        except ImportError:
            sys.stderr.write("[错误] 缺少 PyMuPDF，请运行：pip install pymupdf\n")
            sys.exit(2)
    return fitz


def get_tesseract():
    """导入 pytesseract 并探测系统 tesseract 路径。"""
    try:
        import pytesseract
    except ImportError:
        sys.stderr.write("[错误] 缺少 pytesseract，请运行：pip install pytesseract pillow\n")
        sys.exit(2)

    import os
    import shutil

    # 若 PATH 中已能找到 tesseract，无需手动设置
    if shutil.which("tesseract"):
        return pytesseract

    # 否则探测 macOS Homebrew / Linux 常见安装路径
    for p in ("/opt/homebrew/bin/tesseract", "/usr/local/bin/tesseract", "/usr/bin/tesseract"):
        if os.path.exists(p):
            pytesseract.pytesseract.tesseract_cmd = p
            break
    return pytesseract


def parse_pages(spec, n_pages):
    """解析页范围字符串，返回 0 基页码列表。"""
    if spec is None:
        return list(range(n_pages))
    indices = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            a, b = int(a), int(b)
            indices.update(range(a - 1, b))
        else:
            indices.add(int(part) - 1)
    return sorted(i for i in indices if 0 <= i < n_pages)


def main():
    parser = argparse.ArgumentParser(
        description="对扫描版/图片型 PDF 执行 OCR 识别"
    )
    parser.add_argument("input", help="输入的 PDF 文件路径")
    parser.add_argument("--output", "-o", help="输出文本文件路径（默认打印到 stdout）")
    parser.add_argument("--lang", default="chi_sim+eng", help="OCR 语言（默认 chi_sim+eng）")
    parser.add_argument("--dpi", type=int, default=300, help="渲染分辨率（默认 300）")
    parser.add_argument("--pages", help="页范围，如 1-10 或 3,5,8（默认全部）")
    args = parser.parse_args()

    fitz = get_fitz()
    pytesseract = get_tesseract()

    try:
        from PIL import Image
    except ImportError:
        sys.stderr.write("[错误] 缺少 Pillow，请运行：pip install pillow\n")
        sys.exit(2)

    try:
        doc = fitz.open(args.input)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"[错误] 无法读取 PDF：{e}\n")
        sys.exit(1)

    page_indices = parse_pages(args.pages, doc.page_count)
    sys.stderr.write(
        f"[OCR] 共 {doc.page_count} 页，本次处理 {len(page_indices)} 页，"
        f"dpi={args.dpi}，语言={args.lang}\n"
    )

    out_parts = []
    for idx in page_indices:
        page = doc[idx]
        pix = page.get_pixmap(dpi=args.dpi, colorspace=fitz.csRGB)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        try:
            text = pytesseract.image_to_string(img, lang=args.lang)
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if "chi_sim" in msg or "language" in msg.lower():
                sys.stderr.write(
                    f"[错误] 第 {idx + 1} 页 OCR 失败，可能是缺少语言包 {args.lang}。\n"
                    "macOS 请运行：brew install tesseract-lang\n"
                    f"或改用纯英文：--lang eng\n原始错误：{msg}\n"
                )
                sys.exit(1)
            sys.stderr.write(f"[错误] 第 {idx + 1} 页 OCR 失败：{msg}\n")
            sys.exit(1)
        out_parts.append(f"\n===== 第 {idx + 1} 页 =====\n{text}")
        sys.stderr.write(f"[OCR] 第 {idx + 1} 页完成\n")

    doc.close()
    full_text = "\n".join(out_parts)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(full_text)
        sys.stderr.write(f"[完成] OCR 文本已写入 {args.output}\n")
    else:
        sys.stdout.write(full_text)


if __name__ == "__main__":
    main()
