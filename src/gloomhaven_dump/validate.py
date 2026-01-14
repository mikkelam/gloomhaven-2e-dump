"""Validate PDF extraction quality and report issues."""

import json
from pathlib import Path
from typing import Any


def check_page_stats(page: dict[str, Any]) -> list[str]:
    warnings = []
    page_id = page["page_id"]
    metadata = page["block_metadata"]

    # Check for LLM errors during extraction
    if metadata["llm_error_count"] > 0:
        warnings.append(f"⚠️  Page {page_id}: {metadata['llm_error_count']} LLM errors")

    # Check for suspiciously low text extraction
    blocks = page["block_counts"]
    text_blocks = blocks.get("Text", 0)

    # Skip cover pages and mostly-image pages
    if text_blocks < 5 and page_id > 2:
        warnings.append(
            f"⚠️  Page {page_id}: Only {text_blocks} text blocks (possible extraction issue)"
        )

    # Check for high token usage (might indicate complex/problematic page)
    tokens = metadata.get("llm_tokens_used", 0)
    if tokens > 10000:
        warnings.append(
            f"⚠️  Page {page_id}: High token usage ({tokens}) - complex page"
        )

    return warnings


def validate_toc(meta: dict[str, Any]) -> list[str]:
    warnings = []
    toc = meta.get("table_of_contents", [])

    if not toc:
        warnings.append("⚠️  No table of contents found")
        return warnings

    # Check for reasonable TOC size
    if len(toc) < 50:
        warnings.append(f"⚠️  TOC has only {len(toc)} entries (seems low for rulebook)")

    # Check heading level distribution
    levels = [entry["heading_level"] for entry in toc]
    if max(levels) > 6:
        warnings.append(f"⚠️  TOC has heading levels > 6: max is {max(levels)}")

    return warnings


def validate_extraction(meta_path: Path) -> None:
    if not meta_path.exists():
        print(f"❌ Metadata file not found: {meta_path}")
        return

    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    print(f"📊 Validating extraction from {meta_path.name}\n")

    # Validate TOC
    toc_warnings = validate_toc(meta)
    if toc_warnings:
        print("Table of Contents Issues:")
        for warning in toc_warnings:
            print(f"  {warning}")
        print()

    # Validate page stats
    all_warnings = []
    page_stats = meta.get("page_stats", [])

    for page in page_stats:
        warnings = check_page_stats(page)
        all_warnings.extend(warnings)

    if all_warnings:
        print("Page Extraction Issues:")
        for warning in all_warnings:
            print(f"  {warning}")
        print()
    else:
        print("✓ No page extraction issues found")

    # Summary statistics
    total_pages = len(page_stats)
    total_errors = sum(p["block_metadata"]["llm_error_count"] for p in page_stats)
    total_tokens = sum(
        p["block_metadata"].get("llm_tokens_used", 0) for p in page_stats
    )

    print("\n📈 Summary:")
    print(f"  Total pages: {total_pages}")
    print(f"  Total LLM errors: {total_errors}")
    print(f"  Total tokens used: {total_tokens:,}")
    print(
        f"  Average tokens/page: {total_tokens // total_pages if total_pages else 0:,}"
    )

    # Overall assessment
    print("\n🎯 Overall Assessment:")
    if total_errors == 0 and len(all_warnings) < 5:
        print("  ✓ Extraction quality looks good!")
    elif total_errors < 5 and len(all_warnings) < 10:
        print("  ⚠️  Minor issues detected, but mostly acceptable")
    else:
        print("  ❌ Significant issues detected, consider re-extraction")


def main() -> None:
    output_dir = Path("gloomhaven_output/Gloomhaven-2025-Rulebook")

    if not output_dir.exists():
        print(f"❌ Output directory not found: {output_dir}")
        return

    meta_files = list(output_dir.glob("*_meta.json"))

    if not meta_files:
        print(f"❌ No metadata files found in {output_dir}")
        return

    for meta_file in meta_files:
        validate_extraction(meta_file)
        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
