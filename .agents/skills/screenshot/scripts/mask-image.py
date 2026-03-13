#!/usr/bin/env -S uv --quiet run --script
# /// script
# requires-python = "==3.13.*"
# dependencies = ["Pillow"]
# ///
"""
画像の指定領域を黒い矩形でマスクする。マスク前のオリジナルは /tmp/screenshots/ に自動退避する。

使い方:
    uv run .agents/skills/screenshot/scripts/mask-image.py <画像パス> <矩形1> [<矩形2> ...]

矩形の指定:
    "x1,y1,x2,y2" の形式で指定する（左上と右下の座標）

例:
    uv run .agents/skills/screenshot/scripts/mask-image.py poc/images/aws-console.png "980,5,1130,20" "950,30,1270,45"

オプション:
    --color R,G,B    マスクの色（デフォルト: 0,0,0 = 黒）
"""

import argparse
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw


def parse_rect(s: str) -> tuple[int, int, int, int]:
    """'x1,y1,x2,y2' 形式の文字列をタプルに変換する。"""
    parts = s.strip().split(",")
    if len(parts) != 4:
        print(f"エラー: 矩形の指定が不正です: '{s}'", file=sys.stderr)
        print("  'x1,y1,x2,y2' の形式で指定してください", file=sys.stderr)
        sys.exit(1)
    try:
        return tuple(int(p.strip()) for p in parts)  # type: ignore
    except ValueError:
        print(f"エラー: 座標は整数で指定してください: '{s}'", file=sys.stderr)
        sys.exit(1)


def parse_color(s: str) -> tuple[int, int, int]:
    """'R,G,B' 形式の文字列をタプルに変換する。"""
    parts = s.strip().split(",")
    if len(parts) != 3:
        print(f"エラー: 色の指定が不正です: '{s}'", file=sys.stderr)
        print("  'R,G,B' の形式で指定してください", file=sys.stderr)
        sys.exit(1)
    try:
        color = tuple(int(p.strip()) for p in parts)
        for c in color:
            if not 0 <= c <= 255:
                raise ValueError
        return color  # type: ignore
    except ValueError:
        print(f"エラー: 色は 0-255 の整数で指定してください: '{s}'", file=sys.stderr)
        sys.exit(1)


def backup_original(image_path: Path) -> Path | None:
    """オリジナル画像を /tmp/screenshots/ にバックアップする。"""
    backup_dir = Path("/tmp/backup")
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_dir / image_path.name
    # 同名ファイルがあれば番号を付ける
    if backup_path.exists():
        stem = image_path.stem
        suffix = image_path.suffix
        i = 1
        while backup_path.exists():
            backup_path = backup_dir / f"{stem}_{i}{suffix}"
            i += 1

    shutil.copy2(image_path, backup_path)
    return backup_path


def main():
    parser = argparse.ArgumentParser(
        description="画像の指定領域を矩形でマスクする",
    )
    parser.add_argument("image", help="マスク対象の画像ファイルパス")
    parser.add_argument("rects", nargs="+", help="マスクする矩形 (x1,y1,x2,y2)")
    parser.add_argument("--color", default="0,0,0", help="マスクの色 (R,G,B) デフォルト: 0,0,0")
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.is_file():
        print(f"エラー: ファイルが見つかりません: {image_path}", file=sys.stderr)
        sys.exit(1)

    rects = [parse_rect(r) for r in args.rects]
    color = parse_color(args.color)

    # バックアップ
    backup_path = backup_original(image_path)
    if backup_path:
        print(f"バックアップ: {backup_path}")

    # マスク処理
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    for x1, y1, x2, y2 in rects:
        draw.rectangle([x1, y1, x2, y2], fill=color)

    img.save(image_path)
    print(f"マスク完了: {image_path} ({len(rects)} 箇所)")


if __name__ == "__main__":
    main()
