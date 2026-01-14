# Extract PDF with default quality
extract:
    uv run marker_single gloomhaven-2e-rulebook.pdf \
        --output_dir ./gloomhaven_output \
        --output_format markdown \
        --disable_image_extraction \
        --paginate_output \
        --html_tables_in_markdown \
        --keep_pageheader_in_output \
        --keep_pagefooter_in_output

# Extract with high quality (better OCR/layout detection, no LLM)
extract-hq:
    uv run marker_single gloomhaven-2e-rulebook.pdf \
        --output_dir ./gloomhaven_output \
        --output_format markdown \
        --highres_image_dpi 300 \
        --lowres_image_dpi 192 \
        --layout_batch_size 4 \
        --detection_batch_size 4 \
        --recognition_batch_size 4 \
        --disable_image_extraction \
        --paginate_output \
        --html_tables_in_markdown \
        --keep_pageheader_in_output \
        --keep_pagefooter_in_output

# Process FAQ HTML to markdown
faq:
    uv run python -m gloomhaven_dump.process_faq

# Clean markdown output
clean:
    uv run python -m gloomhaven_dump.clean_output

# Validate extraction quality
validate:
    uv run python -m gloomhaven_dump.validate

# Full pipeline: extract, faq, clean, validate
all: extract faq clean validate

# High quality pipeline
all-hq: extract-hq faq clean validate

# Re-run clean and validate on existing output
check: clean validate
    @echo "✓ All checks passed"

# Remove output directory
reset:
    rm -rf gloomhaven_output

# Sync dependencies
sync:
    uv sync

# Default recipe shows available commands
default:
    @just --list
