#!/usr/bin/env -S uv --quiet run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow", "cairosvg"]
# ///
"""
gradient_eyecatch.py - グラデーション+アイコン+タイトルのアイキャッチ画像生成 PoC

使い方:
  uv run poc/gradient_eyecatch.py --icon terraform --title "Terraform管理AWSリソース名を\nリソースの再作成を避けてリネームする" --output poc/output_eyecatch.png
  uv run poc/gradient_eyecatch.py --icon terraform --title "タイトル" --output out.png --gradient-style analogous
"""

import argparse
import colorsys
import hashlib
import io
import json
import math
import os
import sys
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

from PIL import Image, ImageDraw, ImageFont
import cairosvg

# --- simple-icons ブランドカラーDB (よく使うものをハードコード + CDN fallback) ---
# https://github.com/simple-icons/simple-icons/blob/develop/_data/simple-icons.json
KNOWN_BRANDS = {
    "terraform": {"color": "#7B42BC", "slug": "terraform"},
    "aws": {"color": "#232F3E", "slug": "amazonaws"},
    "amazonaws": {"color": "#232F3E", "slug": "amazonaws"},
    "docker": {"color": "#2496ED", "slug": "docker"},
    "kubernetes": {"color": "#326CE5", "slug": "kubernetes"},
    "python": {"color": "#3776AB", "slug": "python"},
    "github": {"color": "#181717", "slug": "github"},
    "linux": {"color": "#FCC624", "slug": "linux"},
    "typescript": {"color": "#3178C6", "slug": "typescript"},
    "react": {"color": "#61DAFB", "slug": "react"},
    "nextjs": {"color": "#000000", "slug": "nextdotjs"},
    "postgresql": {"color": "#4169E1", "slug": "postgresql"},
    "redis": {"color": "#DC382D", "slug": "redis"},
    "nginx": {"color": "#009639", "slug": "nginx"},
    "go": {"color": "#00ADD8", "slug": "go"},
    "rust": {"color": "#000000", "slug": "rust"},
    "cloudflare": {"color": "#F38020", "slug": "cloudflare"},
    "vercel": {"color": "#000000", "slug": "vercel"},
    "datadog": {"color": "#632CA6", "slug": "datadog"},
    "grafana": {"color": "#F46800", "slug": "grafana"},
    "prometheus": {"color": "#E6522C", "slug": "prometheus"},
    "ansible": {"color": "#EE0000", "slug": "ansible"},
    "jenkins": {"color": "#D24939", "slug": "jenkins"},
    "githubactions": {"color": "#2088FF", "slug": "githubactions"},
    "amazonaws-lambda": {"color": "#FF9900", "slug": "awslambda"},
    "awslambda": {"color": "#FF9900", "slug": "awslambda"},
}

# --- 定数 ---
CACHE_DIR = Path.home() / ".cache" / "eyecatch-icons"
DEFAULT_FONT_URL = "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Bold.otf"
DEFAULT_FONT_CACHE = Path.home() / ".cache" / "eyecatch-fonts"
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 630
ICON_SIZE = 200
DEFAULT_FONT_SIZE = 48


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """#RRGGBB → (R, G, B)"""
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    """RGB(0-255) → HSL(0-360, 0-1, 0-1)"""
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return (h * 360, s, l)


def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    """HSL(0-360, 0-1, 0-1) → RGB(0-255)"""
    r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))


def generate_gradient_colors(
    brand_hex: str, style: str = "warm_spread"
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """ブランドカラーからグラデーションの2色を決定論的に生成する。

    style:
      - warm_spread: アイコン色の補色方向に暖色系グラデーション（参考画像風）
      - analogous: 類似色（±30°）でまとまりのあるグラデーション
      - complementary: 補色方向（±90°）で鮮やかなグラデーション
      - pastel: パステル調（彩度下げ・明度上げ）
    """
    r, g, b = hex_to_rgb(brand_hex)
    h, s, l = rgb_to_hsl(r, g, b)

    if style == "warm_spread":
        # ブランドカラーから色相を+60°〜+140°回転させた暖色グラデーション
        # 例: 紫(274°) → ピンク(334°) 〜 黄色(54°)
        # 明度を高めに設定し、濃い色のアイコン/テキストとのコントラストを確保
        h1 = (h + 60) % 360
        h2 = (h + 140) % 360
        c1 = hsl_to_rgb(h1, 0.55, 0.80)
        c2 = hsl_to_rgb(h2, 0.50, 0.90)

    elif style == "analogous":
        # 類似色: H±30°, 明度を上げてパステル寄りに
        h1 = (h - 30) % 360
        h2 = (h + 30) % 360
        c1 = hsl_to_rgb(h1, min(s, 0.6), 0.7)
        c2 = hsl_to_rgb(h2, min(s, 0.6), 0.8)

    elif style == "complementary":
        # 補色方向: H±90°で鮮やかに
        h1 = (h + 90) % 360
        h2 = (h - 90) % 360
        c1 = hsl_to_rgb(h1, min(s * 0.8, 0.7), 0.7)
        c2 = hsl_to_rgb(h2, min(s * 0.8, 0.7), 0.8)

    elif style == "pastel":
        # パステル: 同色相で彩度を下げ明度を上げる
        c1 = hsl_to_rgb(h, s * 0.4, 0.85)
        c2 = hsl_to_rgb((h + 40) % 360, s * 0.3, 0.92)

    else:
        raise ValueError(f"Unknown gradient style: {style}")

    return c1, c2


def create_gradient_image(
    width: int, height: int,
    color1: tuple[int, int, int],
    color2: tuple[int, int, int],
    angle_deg: float = 135,
) -> Image.Image:
    """2色の線形グラデーション画像を生成する。"""
    img = Image.new("RGB", (width, height))
    pixels = img.load()

    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    # グラデーション方向の最大距離
    max_dist = abs(width * cos_a) + abs(height * sin_a)

    for y in range(height):
        for x in range(width):
            # ピクセル位置のグラデーション軸上の投影
            dist = x * cos_a + y * sin_a
            t = max(0, min(1, (dist + max_dist / 2) / max_dist))
            r = int(color1[0] + (color2[0] - color1[0]) * t)
            g = int(color1[1] + (color2[1] - color1[1]) * t)
            b = int(color1[2] + (color2[2] - color1[2]) * t)
            pixels[x, y] = (r, g, b)

    return img


def fetch_svg_icon(slug: str) -> bytes:
    """simple-icons CDNからSVGを取得してキャッシュする。"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = CACHE_DIR / f"{slug}.svg"

    if cached.exists():
        return cached.read_bytes()

    url = f"https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/{slug}.svg"
    print(f"アイコンを取得中: {url}", file=sys.stderr)
    req = Request(url, headers={"User-Agent": "eyecatch-generator/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            svg_data = resp.read()
        cached.write_bytes(svg_data)
        return svg_data
    except URLError as e:
        print(f"アイコン取得失敗: {e}", file=sys.stderr)
        raise


def svg_to_png(svg_data: bytes, width: int, height: int, color: str | None = None) -> Image.Image:
    """SVGをPNG(Pillow Image)に変換する。色を変更可能。"""
    svg_str = svg_data.decode("utf-8")

    # simple-iconsのSVGはfill無し。色を指定してレンダリング
    if color:
        # SVGのルート要素にfill属性を追加
        svg_str = svg_str.replace("<svg ", f'<svg fill="{color}" ', 1)

    png_data = cairosvg.svg2png(
        bytestring=svg_str.encode("utf-8"),
        output_width=width,
        output_height=height,
    )
    return Image.open(io.BytesIO(png_data)).convert("RGBA")


def get_font(url: str, cache_dir: Path) -> Path:
    """フォントをダウンロードしてキャッシュ。"""
    cache_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(url.split("?")[0]).suffix or ".ttf"
    basename = Path(url.split("?")[0]).stem
    cache_key = hashlib.md5(url.encode()).hexdigest()[:8]
    cached = cache_dir / f"{basename}_{cache_key}{ext}"

    if cached.exists() and cached.stat().st_size > 0:
        return cached

    print(f"フォントをダウンロード中: {url}", file=sys.stderr)
    req = Request(url, headers={"User-Agent": "eyecatch-generator/1.0"})
    with urlopen(req, timeout=60) as resp:
        data = resp.read()
    cached.write_bytes(data)
    return cached


def draw_title(
    img: Image.Image,
    title: str,
    font_path: Path,
    font_size: int,
    text_color: tuple[int, int, int, int],
    y_offset: int = 0,
) -> None:
    """タイトルテキストを画像中央下部に描画する。"""
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(font_path), font_size)
    width, height = img.size
    max_text_width = int(width * 0.72)

    # テキスト折り返し（\n対応、幅超過時は自動折り返し）
    if "\n" in title:
        lines = []
        for seg in title.split("\n"):
            seg = seg.strip()
            if not seg:
                continue
            bb = font.getbbox(seg)
            if bb[2] - bb[0] <= max_text_width:
                lines.append(seg)
            else:
                lines.extend(_simple_wrap(seg, font, max_text_width))
    else:
        lines = _simple_wrap(title, font, max_text_width)

    # 描画位置の計算
    line_bboxes = [font.getbbox(line) for line in lines]
    line_heights = [bb[3] - bb[1] for bb in line_bboxes]
    line_widths = [bb[2] - bb[0] for bb in line_bboxes]
    line_x_offsets = [bb[0] for bb in line_bboxes]
    line_y_offsets = [bb[1] for bb in line_bboxes]
    line_spacing = int(font_size * 0.4)
    total_text_height = sum(line_heights) + line_spacing * (len(lines) - 1)

    # テキストは画像の55%〜92%の領域に中央配置
    text_area_top = height * 0.55
    text_area_bottom = height * 0.92
    y = int(text_area_top + (text_area_bottom - text_area_top - total_text_height) / 2)

    for i, line in enumerate(lines):
        x = (width - line_widths[i]) // 2 - line_x_offsets[i]
        draw.text((x, y - line_y_offsets[i]), line, font=font, fill=text_color)
        y += line_heights[i] + line_spacing


def _simple_wrap(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """簡易テキスト折り返し。"""
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bb = font.getbbox(test)
        if bb[2] - bb[0] > max_width and current:
            lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)
    return lines


def generate_eyecatch(
    icon_name: str,
    title: str,
    output_path: str,
    gradient_style: str = "warm_spread",
    brand_color_override: str | None = None,
    icon_color: str | None = None,
    font_size: int = DEFAULT_FONT_SIZE,
) -> None:
    """グラデーション+アイコン+タイトルのアイキャッチ画像を生成する。"""

    # 1. ブランド情報の取得
    brand = KNOWN_BRANDS.get(icon_name.lower())
    if brand:
        slug = brand["slug"]
        brand_hex = brand_color_override or brand["color"]
    else:
        slug = icon_name.lower()
        brand_hex = brand_color_override or "#6366F1"  # デフォルト: indigo

    print(f"ブランド: {slug}, カラー: {brand_hex}", file=sys.stderr)

    # 2. グラデーション色の生成
    c1, c2 = generate_gradient_colors(brand_hex, gradient_style)
    print(f"グラデーション: RGB{c1} → RGB{c2}", file=sys.stderr)

    # 3. グラデーション背景の生成
    img = create_gradient_image(IMAGE_WIDTH, IMAGE_HEIGHT, c1, c2, angle_deg=135)
    img = img.convert("RGBA")

    # 4. SVGアイコンの取得と配置
    svg_data = fetch_svg_icon(slug)
    # アイコンの色: ブランドカラーそのまま（グラデ背景に映える）
    render_color = icon_color or brand_hex
    icon_img = svg_to_png(svg_data, ICON_SIZE, ICON_SIZE, color=render_color)

    # アイコンの中心を画像高さの30%に配置
    icon_x = (IMAGE_WIDTH - ICON_SIZE) // 2
    icon_y = int(IMAGE_HEIGHT * 0.30 - ICON_SIZE / 2)
    img.paste(icon_img, (icon_x, icon_y), icon_img)

    # 5. タイトルテキストの描画
    font_path = get_font(DEFAULT_FONT_URL, DEFAULT_FONT_CACHE)

    # テキスト色はグラデーション背景に対してコントラストが出る色
    # 明るいグラデーションなら暗いテキスト
    avg_l = (rgb_to_hsl(*c1)[2] + rgb_to_hsl(*c2)[2]) / 2
    if avg_l > 0.5:
        text_color = (40, 40, 40, 255)  # ダークグレー
    else:
        text_color = (255, 255, 255, 255)  # ホワイト

    draw_title(img, title, font_path, font_size, text_color)

    # 6. 出力
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(str(output))
    w, h = img.size
    print(f"生成完了: {output} ({w}x{h})", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="グラデーション+アイコン+タイトルのアイキャッチ画像生成"
    )
    parser.add_argument("--icon", required=True, help="アイコン名 (例: terraform, docker, aws)")
    parser.add_argument("--title", required=True, help="タイトルテキスト (\\nで改行)")
    parser.add_argument("--output", required=True, help="出力ファイルパス")
    parser.add_argument(
        "--gradient-style",
        default="warm_spread",
        choices=["warm_spread", "analogous", "complementary", "pastel"],
        help="グラデーションスタイル (default: warm_spread)",
    )
    parser.add_argument("--brand-color", default=None, help="ブランドカラー上書き (例: #7B42BC)")
    parser.add_argument("--icon-color", default=None, help="アイコン描画色 (例: #7B42BC)")
    parser.add_argument("--font-size", type=int, default=DEFAULT_FONT_SIZE, help="フォントサイズ")

    args = parser.parse_args()

    # \n をリテラル改行に変換
    title = args.title.replace("\\n", "\n")

    generate_eyecatch(
        icon_name=args.icon,
        title=title,
        output_path=args.output,
        gradient_style=args.gradient_style,
        brand_color_override=args.brand_color,
        icon_color=args.icon_color,
        font_size=args.font_size,
    )


if __name__ == "__main__":
    main()
