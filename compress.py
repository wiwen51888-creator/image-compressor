#!/usr/bin/env python
"""图片批量压缩工具。"""

import argparse
from pathlib import Path

from PIL import Image

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def human(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"


def collect(root: Path, recursive: bool) -> list[Path]:
    it = root.rglob("*") if recursive else root.glob("*")
    return [p for p in it if p.is_file() and p.suffix.lower() in SUPPORTED]


def compress_one(src: Path, dst: Path, quality: int, max_size: int, fmt: str | None) -> tuple[int, int]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        if max_size and max(im.size) > max_size:
            ratio = max_size / max(im.size)
            im = im.resize((int(im.width * ratio), int(im.height * ratio)), Image.LANCZOS)

        target = (fmt or src.suffix.lstrip(".")).lower()
        if target in ("jpg", "jpeg"):
            im = im.convert("RGB")
            out = dst.with_suffix(".jpg")
            im.save(out, "JPEG", quality=quality, optimize=True, progressive=True)
        elif target == "png":
            out = dst.with_suffix(".png")
            im.save(out, "PNG", optimize=True)
        elif target == "webp":
            out = dst.with_suffix(".webp")
            im.save(out, "WEBP", quality=quality, method=6)
        else:
            out = dst.with_suffix(src.suffix)
            im.save(out)

    return src.stat().st_size, out.stat().st_size


def main() -> int:
    parser = argparse.ArgumentParser(description="图片批量压缩")
    parser.add_argument("directory", help="源目录")
    parser.add_argument("--out", help="输出目录")
    parser.add_argument("--quality", type=int, default=82)
    parser.add_argument("--max-size", type=int, default=0)
    parser.add_argument("--format", choices=["jpg", "png", "webp"], help="输出格式")
    parser.add_argument("--recursive", action="store_true")
    args = parser.parse_args()

    root = Path(args.directory)
    if not root.is_dir():
        print(f"[错误] 目录不存在: {root}")
        return 1

    out_root = Path(args.out) if args.out else root / "out"
    files = collect(root, args.recursive)
    if not files:
        print("没有找到图片。")
        return 0

    total_in = total_out = 0
    for src in files:
        rel = src.relative_to(root)
        dst = out_root / rel
        try:
            before, after = compress_one(src, dst, args.quality, args.max_size, args.format)
        except Exception as exc:
            print(f"[跳过] {src.name}: {exc}")
            continue
        total_in += before
        total_out += after
        rate = (1 - after / before) * 100 if before else 0
        print(f"{src.name}: {human(before)} -> {human(after)}  (-{rate:.0f}%)")

    if total_in:
        rate = (1 - total_out / total_in) * 100
        print(f"\n共 {len(files)} 张，总计 {human(total_in)} -> {human(total_out)}  (-{rate:.0f}%)")
        print(f"输出目录: {out_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())