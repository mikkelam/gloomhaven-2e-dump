"""Clean and post-process extracted markdown output."""

import re
from pathlib import Path


def clean_markdown(text: str) -> str:
    # Remove excessive blank lines (max 2 consecutive)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Fix garbled lines (OCR artifacts)
    text = re.sub(r"^# The perverse Edge.*?108 109\s*$", "", text, flags=re.MULTILINE)

    # Clean up weird header formatting
    text = re.sub(r"O-O-O-O-O+", "", text)

    # Remove orphaned image tags that should have descriptions
    # Keep the image reference but on single line
    text = re.sub(r"\n!\[\]\([^)]+\)\n\n!\[\]\([^)]+\)\n", "\n", text)

    # Clean up multiple spaces
    text = re.sub(r" {2,}", " ", text)

    # Ensure single newline at end of file
    text = text.rstrip() + "\n"

    return text


def clean_markdown_file(md_path: Path) -> None:
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    text = md_path.read_text(encoding="utf-8")
    cleaned = clean_markdown(text)

    # Only write if changes were made
    if cleaned != text:
        md_path.write_text(cleaned, encoding="utf-8")
        print(f"✓ Cleaned {md_path}")
    else:
        print(f"✓ No changes needed for {md_path}")


def main() -> None:
    output_dir = Path("gloomhaven_output/Gloomhaven-2025-Rulebook")

    if not output_dir.exists():
        print(f"Output directory not found: {output_dir}")
        return

    for md_file in output_dir.glob("*.md"):
        clean_markdown_file(md_file)


if __name__ == "__main__":
    main()
