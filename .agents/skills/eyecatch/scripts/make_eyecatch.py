#!/usr/bin/env -S uv --quiet run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow"]
# ///
"""
make_eyecatch.py - ブログアイキャッチ画像生成

ベース画像にタイトルテキストを重ねてアイキャッチ画像を作成する。

使い方:
  uv run make_eyecatch.py <ベース画像> <タイトル> <出力ファイル> [オプション]

例:
  uv run make_eyecatch.py assets/eyecatch.base.png "Pythonで始めるAPI開発" eyecatch.png
  uv run make_eyecatch.py assets/eyecatch.base.png "タイトル" out.png --size 80
  uv run make_eyecatch.py assets/eyecatch.base.png "タイトル" out.png --font-url "https://..."
"""

import argparse
import hashlib
import os
import sys
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

from PIL import Image, ImageDraw, ImageFont

# --- デフォルト設定 ---
DEFAULT_FONT_URL = "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Bold.otf"
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "eyecatch-fonts"
DEFAULT_FONT_SIZE = 64
DEFAULT_MAX_WIDTH_RATIO = 0.80
DEFAULT_TEXT_COLOR = (51, 51, 51, 255)  # 濃いグレー


def get_font(url: str, cache_dir: Path) -> Path:
    """フォントをダウンロードしてキャッシュ。キャッシュがあればそれを返す。"""
    cache_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(url.split("?")[0]).suffix or ".ttf"
    basename = Path(url.split("?")[0]).stem
    cache_key = hashlib.md5(url.encode()).hexdigest()[:8]
    cached = cache_dir / f"{basename}_{cache_key}{ext}"

    if cached.exists() and cached.stat().st_size > 0:
        return cached

    print(f"フォントをダウンロード中: {url}", file=sys.stderr)
    tmp = cached.with_suffix(".tmp")
    try:
        req = Request(url, headers={"User-Agent": "eyecatch-generator/1.0"})
        with urlopen(req, timeout=60) as resp, open(tmp, "wb") as f:
            f.write(resp.read())
        tmp.rename(cached)
        print(f"キャッシュ保存: {cached}", file=sys.stderr)
        return cached
    except (URLError, OSError) as e:
        tmp.unlink(missing_ok=True)
        print(f"ダウンロード失敗: {e}", file=sys.stderr)
        fallbacks = sorted(
            list(cache_dir.glob("*.otf")) + list(cache_dir.glob("*.ttf"))
        )
        if fallbacks:
            print(f"フォールバック: {fallbacks[0].name}", file=sys.stderr)
            return fallbacks[0]
        raise RuntimeError(
            "使用可能なフォントがありません。ネットワーク接続を確認してください。"
        )


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """テキストが画像幅に収まるよう自動改行する。

    英語はスペース区切り、日本語は文字単位で折り返す。
    混在テキストでも自然な位置で改行する。
    """
    bbox = font.getbbox(text)
    if bbox[2] - bbox[0] <= max_width:
        return [text]

    lines = []
    current = ""
    last_break = ""  # 最後にスペースで区切れた位置までの文字列

    for ch in text:
        test = current + ch
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] > max_width:
            # スペース区切りの位置があればそこで改行（英語の単語を守る）
            if last_break:
                lines.append(last_break.rstrip())
                # last_break以降の残り + 現在の文字を次の行へ
                current = current[len(last_break) :].lstrip() + ch
                last_break = ""
            elif current:
                lines.append(current)
                current = ch
            else:
                current = ch
        else:
            current = test
            if ch == " ":
                last_break = current

    if current:
        lines.append(current.strip())
    return lines


def generate_eyecatch(
    base_path: str,
    title: str,
    output_path: str,
    font_path: Path,
    font_size: int = DEFAULT_FONT_SIZE,
) -> None:
    """アイキャッチ画像を生成する。"""
    img = Image.open(base_path).convert("RGBA")
    width, height = img.size

    font = ImageFont.truetype(str(font_path), font_size)

    max_text_width = int(width * DEFAULT_MAX_WIDTH_RATIO)
    lines = wrap_text(title, font, max_text_width)

    # 各行のサイズを計算（bboxのオフセットも考慮）
    line_bboxes = [font.getbbox(line) for line in lines]
    line_heights = [bb[3] - bb[1] for bb in line_bboxes]
    line_widths = [bb[2] - bb[0] for bb in line_bboxes]
    line_x_offsets = [bb[0] for bb in line_bboxes]
    line_y_offsets = [bb[1] for bb in line_bboxes]
    line_spacing = int(font_size * 0.4)
    total_text_height = sum(line_heights) + line_spacing * (len(lines) - 1)

    # テキストを中央に描画
    draw = ImageDraw.Draw(img)
    y = (height - total_text_height) // 2
    for i, line in enumerate(lines):
        x = (width - line_widths[i]) // 2 - line_x_offsets[i]
        draw.text((x, y - line_y_offsets[i]), line, font=font, fill=DEFAULT_TEXT_COLOR)
        y += line_heights[i] + line_spacing

    img = img.convert("RGB")
    img.save(output_path)
    w, h = img.size
    print(f"生成完了: {output_path} ({w}x{h})")


def main():
    parser = argparse.ArgumentParser(description="ブログアイキャッチ画像を生成する")
    parser.add_argument("base", help="ベース画像のパス")
    parser.add_argument("title", help="タイトルテキスト")
    parser.add_argument("output", help="出力ファイルパス")
    parser.add_argument("--font-url", default=None, help="フォントのURL (TTF/OTF)")
    parser.add_argument(
        "--font-file", default=None, help="ローカルフォントファイルのパス"
    )
    parser.add_argument(
        "--size",
        type=int,
        default=DEFAULT_FONT_SIZE,
        help=f"フォントサイズ (default: {DEFAULT_FONT_SIZE})",
    )

    args = parser.parse_args()

    base = Path(args.base)
    if not base.exists():
        print(f"ベース画像が見つかりません: {base}", file=sys.stderr)
        sys.exit(1)

    if args.font_file:
        font_path = Path(args.font_file)
        if not font_path.exists():
            print(f"フォントファイルが見つかりません: {font_path}", file=sys.stderr)
            sys.exit(1)
    else:
        font_url = args.font_url or os.environ.get(
            "EYECATCH_FONT_URL", DEFAULT_FONT_URL
        )
        cache_dir = Path(os.environ.get("EYECATCH_FONT_CACHE", str(DEFAULT_CACHE_DIR)))
        font_path = get_font(font_url, cache_dir)

    output_dir = Path(args.output).parent
    if output_dir != Path("."):
        output_dir.mkdir(parents=True, exist_ok=True)

    generate_eyecatch(args.base, args.title, args.output, font_path, args.size)


if __name__ == "__main__":
    main()
