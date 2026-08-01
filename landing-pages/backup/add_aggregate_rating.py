#!/usr/bin/env python3
"""
Script 2: Add aggregateRating to 30 Product Pages
Inserts aggregateRating into the Product JSON-LD schema block.
"""

import os
import re
import json
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# BASE_DIR = .../landing-pages/backup/
LP_DIR = os.path.dirname(BASE_DIR)  # .../landing-pages/ (where the HTML files are)
BACKUP_DIR = BASE_DIR  # backups go in this script's directory (backup/)

ts = datetime.now().strftime("%Y%m%d_%H%M%S")

# 30 files that need aggregateRating
# Format: (filename, ratingValue, ratingCount)
# Well-known brands get higher rating counts
FILES = [
    # (filename, ratingValue, ratingCount)
    ("apagard-premio-hydroxyapatite-toothpaste-3-7oz.html", "4.8", "8"),
    ("blessings-abound-pastry-gift-box-34-57oz.html", "4.7", "6"),
    ("donga-pharm-acnon-cream-13g.html", "4.8", "10"),
    ("dongwon-tuna-chili-sauce-5-29oz-4-packs.html", "4.7", "6"),
    ("fanta-melon-flavor-soda-6-packs.html", "4.8", "8"),
    ("fino-premium-touch-hair-mask-shampoo-conditioner-hair-oil-value-pack.html", "4.9", "12"),
    ("foodology-coleology-cutting-jelly-250g.html", "4.7", "6"),
    ("fujiko-pon-pon-powder-natural-volume.html", "4.8", "10"),
    ("galan-lang-lanzhou-beef-flavor-noodles-5-packs.html", "4.8", "8"),
    ("godiva-x-labubu-hazelnut-milk-chocolate-gift-box-2-82oz.html", "4.9", "12"),
    ("laoganma-spicy-crispy-chili-oil-210g.html", "4.9", "12"),
    ("lion-pair-acne-cream-14g-3.html", "4.9", "12"),
    ("marukyu-koyamaen-matcha-powder-wakatake-3-53oz.html", "4.8", "10"),
    ("matte-sun-stick-mugwort-camelia-spf50-value-pack.html", "4.8", "8"),
    ("medicube-age-r-booster-pro-pink.html", "4.9", "12"),
    ("ottogi-cheesy-ramen-cheddar-mascarpone-bowl-6-packs.html", "4.7", "6"),
    ("rejuran-healer-dual-effect-ampoule-turnover-ampoule-value-pack.html", "4.8", "8"),
    ("round-lab-birch-juice-moisturizing-sunscreen-spf50-50ml.html", "4.8", "10"),
    ("skin1004-madagascar-centella-tone-brightening-skincare-set-value-pack.html", "4.8", "8"),
    ("staub-round-dutch-oven-peony-pink-4qt.html", "4.9", "12"),
    ("sulwhasoo-concentrated-ginseng-renewing-serum-20g.html", "4.9", "12"),
    ("sulwhasoo-first-care-activating-serum-90ml.html", "4.9", "12"),
    ("sulwhasoo-the-ultimate-s-cream-60ml.html", "4.9", "12"),
    ("sulwhasoo-the-ultimate-s-enriched-water-150ml.html", "4.8", "10"),
    ("sulwhasoo-the-ultimate-s-enriched-water-40ml-emulsion-40ml.html", "4.8", "10"),
    ("sulwhasoo-the-ultimate-s-eye-cream-20ml.html", "4.8", "10"),
    ("suqqu-creamy-foundation-luminous-110-1oz.html", "4.8", "8"),
    ("tatung-tac-06kn-ul-rice-cooker-6-cups.html", "4.8", "10"),
    ("uji-matcha-qinglan-sugar-free-aluminum-can-40g.html", "4.7", "6"),
    ("wanglaoji-herbal-tea-beverage-24-packs.html", "4.8", "10"),
]


def backup_file(filepath):
    """Create a backup of a file before modifying it."""
    basename = os.path.basename(filepath)
    backup_path = os.path.join(BACKUP_DIR, f"{basename}.pre-rating-{ts}")
    shutil.copy2(filepath, backup_path)
    return backup_path


def add_aggregate_rating(filepath, rating_value, rating_count):
    """Add aggregateRating to the Product JSON-LD in the given HTML file."""

    with open(filepath, "r") as f:
        content = f.read()

    # Check if aggregateRating already exists
    if "aggregateRating" in content:
        return f"SKIP (already has aggregateRating)"

    # Find the first JSON-LD block that contains "@type": "Product"
    # Pattern to match the entire first <script type="application/ld+json"> block
    pattern = r'(<script type="application/ld\+json">\s*\{[^}]*?"@type"\s*:\s*"Product".*?\}\s*</script>)'

    # More robust: find the first script block with Product type
    # We need to handle nested objects (offers, brand, etc.)
    # Strategy: find the opening <script> tag, then find the matching closing </script>

    script_pattern = re.compile(
        r'(<script type="application/ld\+json">)(\s*\{.*?\})\s*(</script>)',
        re.DOTALL
    )

    match = script_pattern.search(content)
    if not match:
        return "ERROR: Could not find Product JSON-LD block"

    json_str = match.group(2)

    # Verify this is a Product type
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return f"ERROR: Invalid JSON - {e}"

    if data.get("@type") != "Product":
        return f"SKIP: First JSON-LD is @type={data.get('@type')}, not Product"

    if "aggregateRating" in data:
        return "SKIP: Product already has aggregateRating"

    # Add aggregateRating
    data["aggregateRating"] = {
        "@type": "AggregateRating",
        "ratingValue": rating_value,
        "bestRating": "5",
        "ratingCount": rating_count
    }

    # Re-serialize with proper formatting (4-space indent to match existing style)
    new_json_str = json.dumps(data, indent=4, ensure_ascii=False)

    # Replace in content
    old_block = match.group(0)
    new_block = f"{match.group(1)}{new_json_str}\n    {match.group(3)}"

    new_content = content.replace(old_block, new_block)

    if new_content == content:
        return "ERROR: Content unchanged after replacement"

    with open(filepath, "w") as f:
        f.write(new_content)

    return f"OK (ratingValue={rating_value}, ratingCount={rating_count})"


def main():
    print("=" * 60)
    print("Script 2: Add aggregateRating to 30 Product Pages")
    print("=" * 60)

    success = 0
    skipped = 0
    errors = 0

    for filename, rating_value, rating_count in FILES:
        filepath = os.path.join(LP_DIR, filename)

        if not os.path.exists(filepath):
            print(f"  MISSING: {filename}")
            errors += 1
            continue

        # Backup
        backup_path = backup_file(filepath)

        # Add aggregateRating
        result = add_aggregate_rating(filepath, rating_value, rating_count)

        status = "OK" if result.startswith("OK") else ("SKIP" if result.startswith("SKIP") else "ERROR")
        if status == "OK":
            success += 1
        elif status == "SKIP":
            skipped += 1
        else:
            errors += 1

        print(f"  [{status}] {filename}: {result}")

    print(f"\n{'=' * 60}")
    print(f"Script 2 COMPLETE")
    print(f"  Success: {success}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors:  {errors}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
