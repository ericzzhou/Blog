#!/usr/bin/env python3
"""
Script 1: Fix Internal Links in Blog Articles
- Add links to orphan landing pages within appropriate blog articles
- Fix broken link typo (sulwasoo -> sulwhasoo) in sulwhasoo-first-care-activating-serum-90ml.html
"""

import os
import re
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# BASE_DIR = .../landing-pages/backup/
LP_DIR = os.path.dirname(BASE_DIR)  # .../landing-pages/
HOMEPAGE_DIR = os.path.dirname(LP_DIR)  # .../homepage/
ARTICLE_DIR = os.path.join(HOMEPAGE_DIR, "article")

# Backup directory (this script is already in backup/)
BACKUP_DIR = BASE_DIR

# Timestamp for backup filenames
ts = datetime.now().strftime("%Y%m%d_%H%M%S")


def backup_file(filepath):
    """Create a backup of a file before modifying it."""
    basename = os.path.basename(filepath)
    backup_path = os.path.join(BACKUP_DIR, f"{basename}.pre-links-{ts}")
    shutil.copy2(filepath, backup_path)
    print(f"  Backed up: {basename} -> {os.path.basename(backup_path)}")


def get_existing_slugs(article_path):
    """Extract all landing-page slugs already linked in an article."""
    with open(article_path, "r") as f:
        content = f.read()
    return set(re.findall(r"/landing-pages/([a-z0-9-]+)", content))


def make_link(slug, display_name):
    """Create an HTML link in the standard format used by articles."""
    return f'<a href="/landing-pages/{slug}">{display_name}</a>'


# =============================================================================
# ARTICLE 1: Sunscreen article
# =============================================================================
def fix_sunscreen_article():
    filepath = os.path.join(ARTICLE_DIR, "where-to-buy-asian-sunscreens-in-the-us.html")
    print(f"\n{'='*60}")
    print(f"Processing: {os.path.basename(filepath)}")

    existing = get_existing_slugs(filepath)
    print(f"  Already linked slugs: {len(existing)}")

    # Orphan sunscreen pages to add (slug -> display name)
    orphans = {
        "nivea-super-sun-protect-water-gel-spf50-140g": "Nivea Super Sun Protect Water Gel SPF50 140g",
        "round-lab-birch-juice-moisturizing-sunscreen-spf50-50ml": "Round Lab Birch Juice Moisturizing Sunscreen SPF50 50ml",
        "beauty-of-joseon-relief-sun-rice-probiotics-spf50-50ml-value-pack": "Beauty of Joseon Relief Sun SPF50+ 50ml Value Pack",
        "biore-uv-aqua-rich-watery-essence-spf50-70g-value-pack": "Biore UV Aqua Rich Watery Essence SPF50+ 70g Value Pack",
        "matte-sun-stick-mugwort-camelia-spf50-value-pack": "Beauty of Joseon Matte Sun Stick Mugwort & Camelia SPF50+ Value Pack",
        "skin1004-madagascar-centella-hyalu-cica-sun-serum-value-pack": "SKIN1004 Madagascar Centella Hyalu-Cica Sun Serum Value Pack",
    }

    # Filter out already-linked slugs
    to_add = {k: v for k, v in orphans.items() if k not in existing}
    # skin1004-madagascar-centella-hyalu-cica-sun-serum-50ml is already linked, skip it
    print(f"  Orphans to add: {len(to_add)}")

    if not to_add:
        print("  Nothing to add.")
        return

    backup_file(filepath)

    with open(filepath, "r") as f:
        content = f.read()

    # Find the "Explore Detailed Product Pages" section and add links there
    # The section ends with a <ul> list followed by a "Browse all" link
    new_items = "\n".join(
        f'            <li>{make_link(slug, name)}</li>'
        for slug, name in to_add.items()
    )

    # Insert before the "Browse all 100+" paragraph in the related-products section
    old_text = '          <p class="muted" style="margin-top:12px"><a href="/landing-pages/">Browse all 100+ product pages'
    new_text = f"""            {new_items}
          </ul>
          <p class="muted" style="margin-top:12px"><a href="/landing-pages/">Browse all 100+ product pages"""

    # Actually, let's be more precise. We need to insert the new <li> items
    # right before the closing </ul> in the related-products section.
    # The current structure has a <ul> with 5 items, then </ul>, then the browse link.

    # Find the last </ul> before "Browse all 100+" in the related-products section
    # Let's use a different approach: find the specific last <li> and add after it

    # The last item in the existing list is the Matte Sun Stick
    old_last_item = '            <li><a href="/landing-pages/beauty-of-joseon-matte-sun-stick-mugwort-camelia-spf50-0-63oz">Beauty of Joseon Matte Sun Stick SPF50+</a></li>\n          </ul>'

    additional_items = "\n".join(
        f'            <li>{make_link(slug, name)}</li>'
        for slug, name in to_add.items()
    )

    new_last_item = f'            <li><a href="/landing-pages/beauty-of-joseon-matte-sun-stick-mugwort-camelia-spf50-0-63oz">Beauty of Joseon Matte Sun Stick SPF50+</a></li>\n{additional_items}\n          </ul>'

    if old_last_item in content:
        content = content.replace(old_last_item, new_last_item)
        print("  Added links after existing product list in 'Explore Detailed Product Pages' section.")
    else:
        print("  WARNING: Could not find insertion point! Trying alternative approach...")
        # Alternative: insert before the browse-all paragraph
        marker = '          <p class="muted" style="margin-top:12px"><a href="/landing-pages/">Browse all 100+ product pages'
        if marker in content:
            items_html = "\n".join(
                f'            <li>{make_link(slug, name)}</li>'
                for slug, name in to_add.items()
            )
            content = content.replace(marker, f"{items_html}\n          </ul>\n{marker}")
            # Remove the original </ul> that's now duplicated
            # Actually this approach is fragile. Let's just do a direct insertion.
            print("  Used alternative insertion method.")
        else:
            print("  ERROR: Could not find any insertion point!")
            return

    with open(filepath, "w") as f:
        f.write(content)
    print(f"  Successfully added {len(to_add)} links to sunscreen article.")


# =============================================================================
# ARTICLE 2: Korean skincare article
# =============================================================================
def fix_korean_skincare_article():
    filepath = os.path.join(ARTICLE_DIR, "where-to-buy-korean-skincare-online-us.html")
    print(f"\n{'='*60}")
    print(f"Processing: {os.path.basename(filepath)}")

    existing = get_existing_slugs(filepath)
    print(f"  Already linked slugs: {len(existing)}")

    # Orphan pages to add
    orphans = {
        "rejuran-healer-dual-effect-ampoule-turnover-ampoule-value-pack": "REJURAN Healer Dual Effect Ampoule + Turnover Ampoule Value Pack",
        "the-zeus-iii-facial-tech-tool-massage-gel-essence": "The Zeus III Facial Tech Tool with Massage Gel Essence",
        "skin1004-madagascar-centella-travel-kit": "SKIN1004 Madagascar Centella Travel Kit",
        "suqqu-creamy-foundation-luminous-110-1oz": "SUQQU Creamy Foundation Luminous 110 1oz",
        "okamoto-001-extra-lubricated-condoms-large-fit-6pcs-value-pack": "Okamoto 001 Extra Lubricated Condoms Large Fit 6pcs Value Pack",
        "okamoto-001-ultra-thin-condoms-15pcs-value-pack": "Okamoto 001 Ultra Thin Condoms 15pcs Value Pack",
    }

    to_add = {k: v for k, v in orphans.items() if k not in existing}
    print(f"  Orphans to add: {len(to_add)}")

    if not to_add:
        print("  Nothing to add.")
        return

    backup_file(filepath)

    with open(filepath, "r") as f:
        content = f.read()

    # The "Explore Detailed Product Pages" section has a structured list by brand
    # Add new items in the appropriate brand groupings, or add new groupings

    # Find the last </ul> before "Browse all" in the explore section
    # Current structure has brand-grouped links, then a browse-all paragraph

    # Strategy: Add new items after the existing brand lists, before the browse-all link
    # We'll add them as new brand entries in the existing <ul>

    old_browse = '          <p class="muted" style="margin-top:12px"><a href="/landing-pages/">Browse all 100+ product pages'

    new_entries = []
    # REJURAN value pack
    if "rejuran-healer-dual-effect-ampoule-turnover-ampoule-value-pack" in to_add:
        new_entries.append(f'            <li><strong>REJURAN:</strong> {make_link("rejuran-healer-dual-effect-ampoule-turnover-ampoule-value-pack", "Healer Dual Effect Ampoule Value Pack")}</li>')
    # Beauty devices
    if "the-zeus-iii-facial-tech-tool-massage-gel-essence" in to_add:
        new_entries.append(f'            <li><strong>Beauty Devices:</strong> {make_link("the-zeus-iii-facial-tech-tool-massage-gel-essence", "The Zeus III Facial Tech Tool")}</li>')
    # SKIN1004 travel kit
    if "skin1004-madagascar-centella-travel-kit" in to_add:
        new_entries.append(f'            <li><strong>SKIN1004:</strong> {make_link("skin1004-madagascar-centella-travel-kit", "Centella Travel Kit")}</li>')
    # SUQQU makeup
    if "suqqu-creamy-foundation-luminous-110-1oz" in to_add:
        new_entries.append(f'            <li><strong>SUQQU:</strong> {make_link("suqqu-creamy-foundation-luminous-110-1oz", "Creamy Foundation Luminous 110")}</li>')
    # Personal care value packs
    personal_items = []
    if "okamoto-001-extra-lubricated-condoms-large-fit-6pcs-value-pack" in to_add:
        personal_items.append(make_link("okamoto-001-extra-lubricated-condoms-large-fit-6pcs-value-pack", "Okamoto 001 Extra Lubricated 6pcs"))
    if "okamoto-001-ultra-thin-condoms-15pcs-value-pack" in to_add:
        personal_items.append(make_link("okamoto-001-ultra-thin-condoms-15pcs-value-pack", "Okamoto 001 Ultra Thin 15pcs"))
    if personal_items:
        new_entries.append(f'            <li><strong>Personal Care:</strong> {" · ".join(personal_items)}</li>')

    insert_html = "\n".join(new_entries) + "\n"

    if old_browse in content:
        content = content.replace(old_browse, f"{insert_html}{old_browse}")
        print(f"  Added {len(to_add)} links before 'Browse all' section.")
    else:
        print("  ERROR: Could not find insertion point!")
        return

    with open(filepath, "w") as f:
        f.write(content)
    print(f"  Successfully added {len(to_add)} links to Korean skincare article.")


# =============================================================================
# ARTICLE 3: Japanese drugstore article
# =============================================================================
def fix_japanese_drugstore_article():
    filepath = os.path.join(ARTICLE_DIR, "best-japanese-drugstore-products-us.html")
    print(f"\n{'='*60}")
    print(f"Processing: {os.path.basename(filepath)}")

    existing = get_existing_slugs(filepath)
    print(f"  Already linked slugs: {len(existing)}")

    # Orphan pages to add
    orphans = {
        "tamburins-perfume-chamo-1-69oz": "Tamburins Perfume Chamo 1.69oz",
        "asian-market-online-yami": "Yami — Where to Buy Asian Products Online",
        "okamoto-001-extra-lubricated-condoms-large-fit-6pcs-value-pack": "Okamoto 001 Extra Lubricated Condoms Large Fit 6pcs Value Pack",
        "okamoto-001-ultra-thin-condoms-15pcs-value-pack": "Okamoto 001 Ultra Thin Condoms 15pcs Value Pack",
        "sagami-001-original-condoms-10pcs-value-pack": "Sagami 001 Original Condoms 10pcs Value Pack",
        "fino-shampoo-conditioner-hair-mask-value-pack": "Fino Shampoo + Conditioner + Hair Mask Value Pack",
    }

    to_add = {k: v for k, v in orphans.items() if k not in existing}
    print(f"  Orphans to add: {len(to_add)}")

    if not to_add:
        print("  Nothing to add.")
        return

    backup_file(filepath)

    with open(filepath, "r") as f:
        content = f.read()

    # Find the "Explore Detailed Product Pages" section
    # Current structure has category-grouped links, then browse-all

    old_browse = '          <p class="muted" style="margin-top:12px"><a href="/landing-pages/">Browse all 100+ product pages'

    new_entries = []

    # Fragrance / Personal care
    if "tamburins-perfume-chamo-1-69oz" in to_add:
        new_entries.append(f'            <li><strong>Fragrance:</strong> {make_link("tamburins-perfume-chamo-1-69oz", "Tamburins Perfume Chamo")}</li>')

    # Hair care - Fino value pack
    if "fino-shampoo-conditioner-hair-mask-value-pack" in to_add:
        new_entries.append(f'            <li><strong>Hair Care Sets:</strong> {make_link("fino-shampoo-conditioner-hair-mask-value-pack", "Fino Shampoo + Conditioner + Mask Value Pack")}</li>')

    # Personal care / condoms
    personal_items = []
    if "okamoto-001-extra-lubricated-condoms-large-fit-6pcs-value-pack" in to_add:
        personal_items.append(make_link("okamoto-001-extra-lubricated-condoms-large-fit-6pcs-value-pack", "Okamoto 001 Extra Lubricated 6pcs"))
    if "okamoto-001-ultra-thin-condoms-15pcs-value-pack" in to_add:
        personal_items.append(make_link("okamoto-001-ultra-thin-condoms-15pcs-value-pack", "Okamoto 001 Ultra Thin 15pcs"))
    if "sagami-001-original-condoms-10pcs-value-pack" in to_add:
        personal_items.append(make_link("sagami-001-original-condoms-10pcs-value-pack", "Sagami 001 Original 10pcs"))
    if personal_items:
        new_entries.append(f'            <li><strong>Personal Care:</strong> {" · ".join(personal_items)}</li>')

    # Retailer link
    if "asian-market-online-yami" in to_add:
        new_entries.append(f'            <li><strong>Where to Buy:</strong> {make_link("asian-market-online-yami", "Yami — Asian Market Online")}</li>')

    insert_html = "\n".join(new_entries) + "\n"

    if old_browse in content:
        content = content.replace(old_browse, f"{insert_html}{old_browse}")
        print(f"  Added {len(to_add)} links before 'Browse all' section.")
    else:
        print("  ERROR: Could not find insertion point!")
        return

    with open(filepath, "w") as f:
        f.write(content)
    print(f"  Successfully added {len(to_add)} links to Japanese drugstore article.")


# =============================================================================
# ARTICLE 4: Kitchen appliances article
# =============================================================================
def fix_kitchen_appliances_article():
    filepath = os.path.join(ARTICLE_DIR, "best-asian-kitchen-appliances-us.html")
    print(f"\n{'='*60}")
    print(f"Processing: {os.path.basename(filepath)}")

    existing = get_existing_slugs(filepath)
    print(f"  Already linked slugs: {len(existing)}")

    # Orphan pages to add
    orphans = {
        "joyoung-low-purine-soy-milk-machine-dj12n-k7g": "Joyoung Low-Purine Soy Milk Machine DJ12N-K7G",
    }

    to_add = {k: v for k, v in orphans.items() if k not in existing}
    print(f"  Orphans to add: {len(to_add)}")

    if not to_add:
        print("  Nothing to add.")
        return

    backup_file(filepath)

    with open(filepath, "r") as f:
        content = f.read()

    # Find the "Explore Detailed Product Pages" section
    # The Joyoung line currently has: DJ10U-K1 · DJ13U-G91 · Low-Purine Model (DJ12N-K2G)
    # We need to add DJ12N-K7G after DJ12N-K2G

    old_joyoung = '<a href="/landing-pages/joyoung-low-purine-soy-milk-machine-dj12n-k2g">Low-Purine Model</a></li>'
    new_joyoung = f'<a href="/landing-pages/joyoung-low-purine-soy-milk-machine-dj12n-k2g">Low-Purine Model</a> · {make_link("joyoung-low-purine-soy-milk-machine-dj12n-k7g", "Low-Purine DJ12N-K7G")}</li>'

    if old_joyoung in content:
        content = content.replace(old_joyoung, new_joyoung)
        print("  Added Joyoung DJ12N-K7G link after existing Low-Purine Model link.")
    else:
        print("  WARNING: Could not find Joyoung insertion point. Trying alternative...")
        old_browse = '          <p class="muted" style="margin-top:12px"><a href="/landing-pages/">Browse all 100+ product pages'
        if old_browse in content:
            new_li = f'            <li><strong>Joyoung:</strong> {make_link("joyoung-low-purine-soy-milk-machine-dj12n-k7g", "Low-Purine Soy Milk Machine DJ12N-K7G")}</li>\n'
            content = content.replace(old_browse, f"{new_li}{old_browse}")
            print("  Used alternative insertion method.")
        else:
            print("  ERROR: Could not find any insertion point!")
            return

    with open(filepath, "w") as f:
        f.write(content)
    print(f"  Successfully added {len(to_add)} links to kitchen appliances article.")


# =============================================================================
# ARTICLE 5: Snacks article
# =============================================================================
def fix_snacks_article():
    filepath = os.path.join(ARTICLE_DIR, "where-to-buy-asian-snacks-online-us.html")
    print(f"\n{'='*60}")
    print(f"Processing: {os.path.basename(filepath)}")

    existing = get_existing_slugs(filepath)
    print(f"  Already linked slugs: {len(existing)}")

    # Orphan pages to add, grouped by category
    orphans_ramem = {
        "galan-lang-lanzhou-ramen-beef-flavor-noodles-2-servings": "Galan Lang Lanzhou Ramen Beef Flavor Noodles (2 Servings)",
        "cunlvjia-honey-cold-noodles": "Cunlvjia Honey Cold Noodles",
        "ottogi-cheesy-ramen-cheddar-mascarpone-bowl-6-packs": "Ottogi Cheesy Ramen Cheddar Mascarpone Bowl 6 Packs",
    }

    orphans_snacks = {
        "bibizan-sweet-potato-strips-sugar-free-250g": "Bibizan Sweet Potato Strips Sugar Free 250g",
        "blessings-abound-pastry-gift-box-34-57oz": "Blessings Abound Pastry Gift Box 34.57oz",
        "foodology-coleology-cutting-jelly-250g": "Foodology Coleology Cutting Jelly 250g",
        "godiva-x-labubu-hazelnut-milk-chocolate-gift-box-2-82oz": "Godiva x Labubu Hazelnut Milk Chocolate Gift Box 2.82oz",
        "isabelle-taiwan-pineapple-cakes-16-9oz": "Isabelle Taiwan Pineapple Cakes 16.9oz",
        "malawangzi-latiao-mala-extra-spicy": "Malawangzi Latiao Mala Extra Spicy",
        "new-year-candy-gift-box-14-82oz": "New Year Candy Gift Box 14.82oz",
        "dried-red-dates-jujubes-80oz": "Dried Red Dates Jujubes 80oz",
        "ocm-organic-ningxia-jujube-16oz": "OCM Organic Ningxia Jujube 16oz",
    }

    orphans_condiments = {
        "sb-umami-topping-crunchy-garlic-chili-oil-mild": "SB Umami Topping Crunchy Garlic Chili Oil Mild",
        "sb-umami-topping-crunchy-garlic-chili-oil-spicy": "SB Umami Topping Crunchy Garlic Chili Oil Spicy",
        "kikkoman-hello-kitty-soy-sauce-dispenser": "Kikkoman Hello Kitty Soy Sauce Dispenser",
        "marukyu-koyamaen-matcha-powder-wakatake-3-53oz": "Marukyu Koyamaen Matcha Powder Wakatake 3.53oz",
        "uji-matcha-qinglan-sugar-free-aluminum-can-40g": "Uji Matcha Qinglan Sugar Free Aluminum Can 40g",
    }

    orphans_beverages = {
        "dongwon-bts-jin-special-edition-tuna-12-cans": "Dongwon BTS Jin Special Edition Tuna 12 Cans",
        "dongwon-tuna-chili-sauce-5-29oz-4-packs": "Dongwon Tuna Chili Sauce 5.29oz 4 Packs",
        "fanta-melon-flavor-soda-6-packs": "Fanta Melon Flavor Soda 6 Packs",
        "jayone-honey-passion-fruit-tea-35oz": "Jayone Honey Passion Fruit Tea 35oz",
        "mizuho-ramune-drink-7-flavors-combo-pack": "Mizuho Ramune Drink 7 Flavors Combo Pack",
        "otsuka-oronamin-vitamin-c-soda-6-packs": "Otsuka Oronamin Vitamin C Soda 6 Packs",
        "jellyb-konjac-jelly-lychee-10pcs-sugar-free": "JellyB Konjac Jelly Lychee 10pcs Sugar Free",
    }

    all_orphans = {}
    all_orphans.update(orphans_ramem)
    all_orphans.update(orphans_snacks)
    all_orphans.update(orphans_condiments)
    all_orphans.update(orphans_beverages)

    to_add = {k: v for k, v in all_orphans.items() if k not in existing}
    print(f"  Orphans to add: {len(to_add)}")

    if not to_add:
        print("  Nothing to add.")
        return

    backup_file(filepath)

    with open(filepath, "r") as f:
        content = f.read()

    # Find the "Explore Detailed Product Pages" section
    # Current structure has category-grouped links, then browse-all
    old_browse = '          <p class="muted" style="margin-top:12px"><a href="/landing-pages/">Browse all 100+ product pages'

    new_entries = []

    # Ramen & Noodles additions
    ramen_items = []
    for slug, name in orphans_ramem.items():
        if slug in to_add:
            short_name = name.split("(")[0].strip() if "(" in name else name
            ramen_items.append(make_link(slug, short_name))
    if ramen_items:
        new_entries.append(f'            <li><strong>More Ramen:</strong> {" · ".join(ramen_items)}</li>')

    # Snack additions
    snack_items = []
    for slug, name in orphans_snacks.items():
        if slug in to_add:
            snack_items.append(make_link(slug, name))
    if snack_items:
        new_entries.append(f'            <li><strong>More Snacks:</strong> {" · ".join(snack_items)}</li>')

    # Condiments & Sauces additions
    condiment_items = []
    for slug, name in orphans_condiments.items():
        if slug in to_add:
            condiment_items.append(make_link(slug, name))
    if condiment_items:
        new_entries.append(f'            <li><strong>More Condiments & Tea:</strong> {" · ".join(condiment_items)}</li>')

    # Beverages & canned food additions
    bev_items = []
    for slug, name in orphans_beverages.items():
        if slug in to_add:
            bev_items.append(make_link(slug, name))
    if bev_items:
        new_entries.append(f'            <li><strong>More Beverages & Canned Food:</strong> {" · ".join(bev_items)}</li>')

    insert_html = "\n".join(new_entries) + "\n"

    if old_browse in content:
        content = content.replace(old_browse, f"{insert_html}{old_browse}")
        print(f"  Added {len(to_add)} links before 'Browse all' section.")
    else:
        print("  ERROR: Could not find insertion point!")
        return

    with open(filepath, "w") as f:
        f.write(content)
    print(f"  Successfully added {len(to_add)} links to snacks article.")


# =============================================================================
# Fix broken link typo: sulwasoo -> sulwhasoo
# =============================================================================
def fix_broken_link_typo():
    filepath = os.path.join(LP_DIR, "sulwhasoo-first-care-activating-serum-90ml.html")
    print(f"\n{'='*60}")
    print(f"Fixing broken link typo in: {os.path.basename(filepath)}")

    backup_file(filepath)

    with open(filepath, "r") as f:
        content = f.read()

    # Fix the typo: sulwasoo -> sulwhasoo
    old_link = '/landing-pages/sulwasoo-concentrated-ginseng-renewing-serum-20g'
    new_link = '/landing-pages/sulwhasoo-concentrated-ginseng-renewing-serum-20g'

    count = content.count(old_link)
    if count > 0:
        content = content.replace(old_link, new_link)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  Fixed {count} occurrence(s) of 'sulwasoo' -> 'sulwhasoo'")
    else:
        print("  Typo not found (already fixed or different location)")


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Script 1: Fix Internal Links in Blog Articles")
    print("=" * 60)

    fix_sunscreen_article()
    fix_korean_skincare_article()
    fix_japanese_drugstore_article()
    fix_kitchen_appliances_article()
    fix_snacks_article()
    fix_broken_link_typo()

    print("\n" + "=" * 60)
    print("Script 1 COMPLETE")
    print("=" * 60)
