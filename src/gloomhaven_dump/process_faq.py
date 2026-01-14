"""Convert FAQ HTML to markdown while preserving spoiler tags."""

from pathlib import Path

import html2text
from selectolax.parser import HTMLParser


def wrap_hidden_spans(html: str) -> str:
    """Wrap <span class="hidden"> content in <details> tags."""
    tree = HTMLParser(html)

    for span in tree.css("span.hidden"):
        text = span.text(strip=False)
        details = f"<details><summary>SPOILER</summary>{text}</details>"
        span.replace_with(details)

    return tree.html


def process_faq() -> None:
    html_path = Path("gloomhaven-2e-faq.html")
    output_path = Path("gloomhaven_output/faq.md")

    if not html_path.exists():
        print(f"❌ FAQ HTML not found: {html_path}")
        return

    html_content = html_path.read_text(encoding="utf-8")

    # Wrap hidden spans in details tags
    html_content = wrap_hidden_spans(html_content)

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.ignore_emphasis = False
    h.body_width = 0
    h.protect_links = True
    h.wrap_links = False
    h.bypass_tables = True

    markdown = h.handle(html_content)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    original_size = len(html_content)
    new_size = len(markdown)
    reduction = (1 - new_size / original_size) * 100

    print("✓ Converted FAQ to markdown")
    print(f"  Original: {original_size:,} bytes")
    print(f"  Markdown: {new_size:,} bytes")
    print(f"  Reduction: {reduction:.1f}%")
    print(f"  Output: {output_path}")


def main() -> None:
    process_faq()


if __name__ == "__main__":
    main()
