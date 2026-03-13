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
import re
import sys
import unicodedata
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


def _is_katakana(ch: str) -> bool:
    """カタカナ（長音符ー含む）かどうか判定する。"""
    return ch == "ー" or unicodedata.category(ch).startswith("Lo") and "\u30A0" <= ch <= "\u30FF"


# 行頭禁則文字（行頭に来てはいけない文字）
_NO_START = set(
    "\u3001\u3002\uff0c\uff0e\u30fb\uff1a\uff1b\uff1f\uff01"  # 、。，．・：；？！
    "\u30fc"  # ー
    "\uff09\u300d\u300f\u3011\u3009\u300b\u3015\uff5d\u3017\u3019\u301b"  # ）」』】〉》〕｝〗〙〛
    "\u2018\u2019"  # ''
    "\u002d\u301c"  # -〜
    "?!:;,.)]}"  # ASCII版
)
# 小書きカナも行頭禁則
_NO_START |= set(
    "\u3041\u3043\u3045\u3047\u3049\u3063\u3083\u3085\u3087\u308e"  # ぁぃぅぇぉっゃゅょゎ
    "\u30a1\u30a3\u30a5\u30a7\u30a9\u30c3\u30e3\u30e5\u30e7\u30ee\u30f5\u30f6"  # ァィゥェォッャュョヮヵヶ
)


def _text_width(text: str, font: ImageFont.FreeTypeFont) -> int:
    bb = font.getbbox(text)
    return bb[2] - bb[0]


def _tokenize(text: str) -> list[str]:
    """テキストをトークンに分割する。

    英単語（連続ASCII）やカタカナ語（連続カタカナ）はまとまりとして保持し、
    それ以外の文字は1文字ずつトークンにする。
    """
    tokens: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        # ASCII 英数字やスペースの連続 → まとめる（スペースは後ろに付ける）
        if ord(ch) < 0x100:
            j = i
            while j < len(text) and ord(text[j]) < 0x100:
                j += 1
            # スペース区切りで分割し、スペースは前のトークンに付与
            segment = text[i:j]
            parts = segment.split(" ")
            for k, part in enumerate(parts):
                token = part
                if k < len(parts) - 1:
                    token += " "
                if token:
                    tokens.append(token)
            i = j
        # カタカナの連続 → まとめる
        elif _is_katakana(ch):
            j = i
            while j < len(text) and _is_katakana(text[j]):
                j += 1
            tokens.append(text[i:j])
            i = j
        else:
            tokens.append(ch)
            i += 1
    return tokens


def _wrap_tokens(
    tokens: list[str], font: ImageFont.FreeTypeFont, max_width: int
) -> list[str]:
    """トークン列を行に分割する（貪欲法）。"""
    lines: list[str] = []
    current = ""

    for token in tokens:
        test = current + token
        if current and _text_width(test.rstrip(), font) > max_width:
            # トークンが1つで max_width を超える場合は文字単位で分割
            if not current.strip():
                for ch in token:
                    test2 = current + ch
                    if current and _text_width(test2.rstrip(), font) > max_width:
                        lines.append(current.rstrip())
                        current = ch
                    else:
                        current = test2
                continue

            lines.append(current.rstrip())
            current = token.lstrip() if token.strip() else ""
        else:
            current = test

    if current.strip():
        lines.append(current.rstrip())
    return lines


def _apply_kinsoku(lines: list[str]) -> list[str]:
    """行頭禁則処理: 禁則文字が行頭に来ていたら前の行に押し込む。"""
    if len(lines) <= 1:
        return lines
    result = [lines[0]]
    for i in range(1, len(lines)):
        line = lines[i]
        # 行頭が禁則文字なら前の行に移動
        while line and line[0] in _NO_START and result:
            result[-1] = result[-1] + line[0]
            line = line[1:]
        result.append(line)
    return [l for l in result if l]


def _balance_lines(
    text: str, font: ImageFont.FreeTypeFont, max_width: int
) -> list[str]:
    """行の長さを均等化する。

    貪欲法で得た行数をベースに、全行がmax_width以内かつ
    行幅の差が最小になるよう調整する。
    """
    tokens = _tokenize(text)
    greedy = _wrap_tokens(tokens, font, max_width)
    n_lines = len(greedy)

    if n_lines <= 1:
        return greedy

    # 目標幅を max_width から徐々に狭めて、同じ行数で収まる最小幅を探す
    total_width = _text_width(text, font)
    target = total_width // n_lines  # 均等の理想幅

    # target ~ max_width の範囲で二分探索
    lo, hi = target, max_width
    best = greedy

    for _ in range(20):
        mid = (lo + hi) // 2
        candidate = _wrap_tokens(tokens, font, mid)
        candidate = _apply_kinsoku(candidate)
        if len(candidate) <= n_lines and all(
            _text_width(l, font) <= max_width for l in candidate
        ):
            best = candidate
            hi = mid
        else:
            lo = mid + 1

    return best


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    r"""テキストが画像幅に収まるよう自動改行する。

    - \n による明示的な改行をサポート
    - カタカナ語を途中で分割しない
    - 行頭禁則処理（句読点・小書きカナ等が行頭に来ない）
    - 行の長さを均等化
    """
    # \n が含まれていれば明示的改行として扱う
    if "\n" in text:
        segments = text.split("\n")
        lines: list[str] = []
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            if _text_width(seg, font) <= max_width:
                lines.append(seg)
            else:
                lines.extend(_balance_lines(seg, font, max_width))
        return lines

    if _text_width(text, font) <= max_width:
        return [text]

    return _balance_lines(text, font, max_width)


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
