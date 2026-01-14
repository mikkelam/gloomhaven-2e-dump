"""Main extraction module for Gloomhaven rulebook PDF processing."""

from pathlib import Path

from marker.convert import convert_single_pdf
from marker.models import load_all_models


def extract_pdf(
    pdf_path: Path,
    output_dir: Path,
    extract_images: bool = True,
    max_pages: int | None = None,
) -> None:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    print("📖 Loading models...")
    model_lst = load_all_models()

    print(f"📄 Processing {pdf_path.name}...")
    full_text, images, out_meta = convert_single_pdf(
        str(pdf_path),
        model_lst,
        max_pages=max_pages,
        langs=["en"],
        batch_multiplier=2,
    )

    # Create output directory structure
    doc_name = pdf_path.stem
    doc_dir = output_dir / doc_name
    doc_dir.mkdir(parents=True, exist_ok=True)

    # Save markdown
    md_path = doc_dir / f"{doc_name}.md"
    md_path.write_text(full_text, encoding="utf-8")
    print(f"✓ Saved markdown: {md_path}")

    # Save metadata
    import json

    meta_path = doc_dir / f"{doc_name}_meta.json"
    meta_path.write_text(json.dumps(out_meta, indent=2), encoding="utf-8")
    print(f"✓ Saved metadata: {meta_path}")

    # Save images if requested
    if extract_images and images:
        img_dir = doc_dir / "images"
        img_dir.mkdir(exist_ok=True)

        for img_name, img_data in images.items():
            img_path = img_dir / img_name
            img_path.write_bytes(img_data)

        print(f"✓ Saved {len(images)} images to {img_dir}")
    elif extract_images:
        print("⚠️  No images found in PDF")

    print("\n✅ Extraction complete!")
    print(f"   Output directory: {doc_dir}")


def main() -> None:
    pdf_path = Path("Gloomhaven-2025-Rulebook.pdf")
    output_dir = Path("gloomhaven_output")

    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        print("   Place the PDF in the project root directory")
        return

    try:
        extract_pdf(pdf_path, output_dir, extract_images=True)
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        raise


if __name__ == "__main__":
    main()
