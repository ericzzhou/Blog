#!/usr/bin/env python3
"""Batch inject breadcrumb navigation and related products sections into all landing pages."""

import os
import re
import json
import sys

LANDING_DIR = os.path.dirname(os.path.abspath(__file__))

EXCLUDE_FILES = {"index.html", "kikkoman-fixed.html", "test-simple.html"}

CATEGORIES = {
    "Sunscreen": {
        "breadcrumb": "Sunscreen",
        "department": "Beauty",
        "products": {
            "beauty-of-joseon-relief-sun-rice-probiotics-spf50-50ml": "Relief Sun: Rice + Probiotics SPF50+",
            "beauty-of-joseon-relief-sun-rice-probiotics-spf50-50ml-value-pack": "Relief Sun SPF50+ 50ml Value Pack",
            "beauty-of-joseon-matte-sun-stick-mugwort-camelia-spf50-0-63oz": "Matte Sun Stick Mugwort + Camelia",
            "matte-sun-stick-mugwort-camelia-spf50-value-pack": "Matte Sun Stick Value Pack",
            "biore-uv-aqua-rich-watery-essence-spf50-70g": "Biore UV Aqua Rich Watery Essence SPF50+",
            "biore-uv-aqua-rich-watery-essence-spf50-70g-value-pack": "Biore UV Aqua Rich SPF50+ Value Pack",
            "nivea-super-sun-protect-water-gel-spf50-140g": "Nivea Super Sun Protect Water Gel SPF50",
            "round-lab-birch-juice-moisturizing-sunscreen-spf50-50ml": "Round Lab Birch Juice Sunscreen SPF50+",
            "round-lab-birch-juice-moisturizing-sun-cream-spf50": "Round Lab Birch Juice Sun Cream SPF50+",
            "skin1004-madagascar-centella-hyalu-cica-sun-serum-50ml": "SKIN1004 Centella Hyalu-Cica Sun Serum",
            "skin1004-madagascar-centella-hyalu-cica-sun-serum-value-pack": "SKIN1004 Centella Sun Serum Value Pack",
        },
    },
    "Serums & Ampoules": {
        "breadcrumb": "Serums & Ampoules",
        "department": "Beauty",
        "products": {
            "sulwhasoo-concentrated-ginseng-renewing-serum-20g": "Sulwhasoo Concentrated Ginseng Serum",
            "sulwhasoo-first-care-activating-serum-90ml": "Sulwhasoo First Care Activating Serum",
            "sulwhasoo-the-ultimate-s-cream-60ml": "Sulwhasoo The Ultimate S Cream",
            "sulwhasoo-the-ultimate-s-enriched-water-150ml": "Sulwhasoo The Ultimate S Enriched Water",
            "sulwhasoo-the-ultimate-s-enriched-water-40ml-emulsion-40ml": "Sulwhasoo Ultimate S Water + Emulsion Set",
            "sulwhasoo-the-ultimate-s-eye-cream-20ml": "Sulwhasoo The Ultimate S Eye Cream",
            "rejuran-healer-dual-effect-ampoule-1oz": "REJURAN Healer Dual Effect Ampoule",
            "rejuran-healer-dual-effect-ampoule-turnover-ampoule-value-pack": "REJURAN Healer Ampoule Value Pack",
            "beauty-of-joseon-revive-eye-serum-ginseng-retinal": "Beauty of Joseon Revive Eye Serum",
        },
    },
    "Acne Treatment": {
        "breadcrumb": "Acne Treatment",
        "department": "Beauty",
        "products": {
            "donga-pharm-acnon-cream-13g": "DONGA PHARM Acnon Cream",
            "lion-pair-acne-cream-14g-3": "LION PAIR Acne Cream 14g x 3",
            "pair-acne-treatment-cream-24g": "PAIR Acne Treatment Cream",
            "pair-acne-creamy-face-wash-foam-80g": "PAIR Acne Creamy Face Wash",
        },
    },
    "Masks & Sets": {
        "breadcrumb": "Masks & Sets",
        "department": "Beauty",
        "products": {
            "ilso-super-melting-sebum-softener-value-pack": "ILSO Melting Sebum Softener",
            "keana-nadeshiko-pore-care-rice-mask-10pcs": "Keana Nadeshiko Pore Care Rice Mask",
            "skin1004-madagascar-centella-tone-brightening-skincare-set-value-pack": "SKIN1004 Centella Tone Brightening Set",
            "skin1004-madagascar-centella-travel-kit": "SKIN1004 Centella Travel Kit",
        },
    },
    "Beauty Devices": {
        "breadcrumb": "Beauty Devices",
        "department": "Beauty",
        "products": {
            "medicube-age-r-booster-pro-pink": "MEDICUBE Age-R Booster Pro #Pink",
            "spiii-star-edition-hertz-rf-beauty-device": "YAMAN SPIII Hertz RF Beauty Device",
            "the-zeus-iii-facial-tech-tool-massage-gel-essence": "Dr.Arrivo The Zeus III Facial Tool",
            "fujiko-pon-pon-powder-natural-volume": "FUJIKO Pon Pon Powder",
        },
    },
    "Makeup": {
        "breadcrumb": "Makeup",
        "department": "Beauty",
        "products": {
            "suqqu-creamy-foundation-luminous-110-1oz": "SUQQU The Creamy Foundation #110",
        },
    },
    "Fragrance": {
        "breadcrumb": "Fragrance",
        "department": "Beauty",
        "products": {
            "tamburins-perfume-chamo-1-69oz": "TAMBURINS Perfume #CHAMO",
        },
    },
    "Hair Care": {
        "breadcrumb": "Hair Care",
        "department": "Beauty",
        "products": {
            "fino-premium-touch-hair-mask-230g": "FINO Premium Touch Hair Mask 230g",
            "fino-premium-touch-hair-mask-shampoo-conditioner-hair-oil-value-pack": "FINO Hair Mask + Shampoo + Conditioner + Oil Set",
            "fino-repair-shampoo-conditioner-550ml": "FINO Repair Shampoo + Conditioner 550ml",
            "fino-shampoo-conditioner-hair-mask-value-pack": "FINO Shampoo + Conditioner + Mask Set",
            "tsubaki-golden-hair-mask-180g": "TSUBAKI Golden Hair Mask",
            "tsubaki-premium-repair-hair-mask-180g": "TSUBAKI Premium Repair Hair Mask",
        },
    },
    "Sauces & Condiments": {
        "breadcrumb": "Sauces & Condiments",
        "department": "Food",
        "products": {
            "laoganma-spicy-chili-crispy-7-4oz": "LAOGANMA Spicy Chili Crispy",
            "laoganma-spicy-crispy-chili-oil-210g": "LAOGANMA Spicy Crispy Chili Oil",
            "kikkoman-hello-kitty-soy-sauce-5oz": "KIKKOMAN Hello Kitty Soy Sauce 5oz",
            "kikkoman-hello-kitty-soy-sauce-dispenser": "KIKKOMAN Hello Kitty Soy Sauce Dispenser",
            "sb-umami-topping-crunchy-garlic-chili-oil-mild": "S&B Umami Topping Garlic Chili Oil Mild",
            "sb-umami-topping-crunchy-garlic-chili-oil-mild-4-packs": "S&B Umami Topping Garlic Chili Oil Mild 4-Pack",
            "sb-umami-topping-crunchy-garlic-chili-oil-spicy": "S&B Umami Topping Garlic Chili Oil Spicy",
            "zhou-hei-ya-braising-sauce-seasoning-mix-14-1oz": "Zhou Hei Ya Braising Sauce",
            "dongwon-tuna-chili-sauce-5-29oz-4-packs": "DONGWON Tuna with Chili Sauce 4-Pack",
        },
    },
    "Snacks": {
        "breadcrumb": "Snacks",
        "department": "Food",
        "products": {
            "bibizan-steaming-dried-sweet-potatoes-250g": "BiBiZan Steaming Dried Sweet Potatoes",
            "bibizan-sweet-potato-strips-sugar-free-250g": "BiBiZan Sweet Potato Strips Sugar-Free",
            "korean-honey-butter-potato-chips-2-11oz-3-value-pack": "Honey Butter Potato Chips Value Pack",
            "malawangzi-latiao-mala-extra-spicy": "MALAWANGZI Latiao Mala Extra Spicy",
            "rice-crackers-classic-milk-flavor-8-53oz": "Rice Crackers Classic Milk Flavor",
            "egg-tarts-cake-14-1oz": "Egg Tarts Cake",
            "jellyb-konjac-jelly-lychee-10pcs-sugar-free": "Jelly.B Konjac Jelly Lychee Sugar-Free",
        },
    },
    "Noodles & Ramen": {
        "breadcrumb": "Noodles & Ramen",
        "department": "Food",
        "products": {
            "ichiran-ramen-classic-hakata-thin-noodles-5-packs": "ICHIRAN Classic Hakata Tonkotsu Ramen",
            "marutai-kumamoto-black-garlic-oil-tonkotsu-ramen": "MARUTAI Kumamoto Black Garlic Oil Ramen",
            "samyang-buldak-carbonara-hot-chicken-ramen-5-packs": "SAMYANG Buldak Carbonara Ramen",
            "samyang-buldak-quattro-cheese-hot-chicken-ramen-5-packs": "SAMYANG Buldak Quattro Cheese Ramen",
            "ottogi-cheesy-ramen-cheddar-flavor-4-packs": "OTTOGI Cheesy Ramen Cheddar",
            "ottogi-cheesy-ramen-cheddar-mascarpone-bowl-6-packs": "OTTOGI Cheesy Ramen Mascarpone Bowl",
            "galan-lang-lanzhou-beef-flavor-noodles-5-packs": "Galan Lang Lanzhou Beef Noodles",
            "galan-lang-lanzhou-ramen-beef-flavor-noodles-2-servings": "Galan Lang Lanzhou Ramen 2 Servings",
            "cunlvjia-honey-cold-noodles": "Cunlvjia Honey Cold Noodles",
        },
    },
    "Canned Food": {
        "breadcrumb": "Canned Food",
        "department": "Food",
        "products": {
            "dongwon-bts-jin-special-edition-tuna-12-cans": "Dongwon BTS Jin Tuna Gift Set",
        },
    },
    "Beverages & Tea": {
        "breadcrumb": "Beverages & Tea",
        "department": "Food",
        "products": {
            "binggrae-banana-flavored-milk-drink-6-packs": "BINGGRAE Banana Flavored Milk",
            "chagee-boya-jasmine-tea": "CHAGEE BOYA Jasmine Green Tea",
            "fanta-melon-flavor-soda-6-packs": "Fanta Melon Flavor Soda",
            "jayone-honey-passion-fruit-tea-35oz": "JAYONE Honey Passion Fruit Tea",
            "marukyu-koyamaen-matcha-powder-1-41oz": "MARUKYU KOYAMAEN Matcha Powder",
            "marukyu-koyamaen-matcha-powder-wakatake-3-53oz": "MARUKYU KOYAMAEN Matcha Wakatake",
            "mizuho-ramune-drink-7-flavors-combo-pack": "MIZUHO Ramune 7 Flavors Combo",
            "otsuka-oronamin-vitamin-c-soda-6-packs": "Oronamin C Vitamin Soda",
            "uji-matcha-qinglan-sugar-free-aluminum-can-40g": "Uji Matcha Qinglan Sugar-Free",
            "wanglaoji-herbal-tea-beverage-24-packs": "WANGLAOJI Herbal Tea",
        },
    },
    "Dried Goods": {
        "breadcrumb": "Dried Goods",
        "department": "Food",
        "products": {
            "dried-red-dates-jujubes-80oz": "Dried Red Dates Jujubes",
            "ocm-organic-ningxia-jujube-16oz": "OCM Organic Ningxia Jujube",
            "szechuan-flavor-premium-dried-goji-berries-7-94oz": "Premium Dried Goji Berries",
        },
    },
    "Gift Boxes": {
        "breadcrumb": "Gift Boxes",
        "department": "Food",
        "products": {
            "blessings-abound-pastry-gift-box-34-57oz": "Dao Xiang Cun Pastry Gift Box",
            "godiva-x-labubu-hazelnut-milk-chocolate-gift-box-2-82oz": "GODIVA x LABUBU Chocolate Gift Box",
            "isabelle-taiwan-pineapple-cakes-16-9oz": "ISABELLE Taiwan Pineapple Cakes",
            "new-year-candy-gift-box-14-82oz": "HSUFUCHI New Year Candy Gift Box",
        },
    },
    "Rice Cookers": {
        "breadcrumb": "Rice Cookers",
        "department": "Home",
        "products": {
            "tatung-multi-functional-rice-cooker-tac-6g-sf-white": "TATUNG Multi-Functional Rice Cooker",
            "tatung-pearl-white-rice-cooker-tac-10g-10-cup": "TATUNG Pearl White Rice Cooker 10-Cup",
            "tatung-stainless-steel-vanilla-cream-rice-cooker-tac-06in": "TATUNG Stainless Steel Rice Cooker",
            "tatung-tac-06kn-ul-rice-cooker-6-cups": "TATUNG TAC-06KN Rice Cooker 6-Cup",
            "tatung-tac-11kn-ul-rice-cooker-11-cup": "TATUNG TAC-11KN Rice Cooker 11-Cup",
            "zojirushi-induction-heating-rice-cooker-np-hcc10": "ZOJIRUSHI IH Rice Cooker NP-HCC10",
            "zojirushi-induction-heating-rice-cooker-np-hcc18": "ZOJIRUSHI IH Rice Cooker NP-HCC18",
            "zojirushi-micom-rice-cooker-ns-tsc10": "ZOJIRUSHI Micom Rice Cooker NS-TSC10",
            "zojirushi-micom-rice-cooker-ns-tsc18": "ZOJIRUSHI Micom Rice Cooker NS-TSC18",
        },
    },
    "Kitchen Appliances": {
        "breadcrumb": "Kitchen Appliances",
        "department": "Home",
        "products": {
            "joyoung-low-purine-soy-milk-machine-dj12n-k7g": "JOYOUNG Low-Purine Soy Milk Machine",
            "joyoung-multi-function-wellness-kettle-k08-wy601u": "JOYOUNG Multi-Function Wellness Kettle",
            "joyoung-soy-milk-maker-1-3l-dj13u-g91": "JOYOUNG Soy Milk Maker 1.3L",
            "joyoung-soy-milk-maker-dj10u-k1-brown": "JOYOUNG Soy Milk Maker DJ10U-K1",
            "olayks-kitchen-dish-sterilizer-42l": "OLAYKS Kitchen Dish Sterilizer 42L",
            "staub-round-dutch-oven-peony-pink-4qt": "Staub Round Dutch Oven 4QT",
            "zojirushi-gourmet-expert-electric-skillet-ep-pbc10": "ZOJIRUSHI Electric Skillet EP-PBC10",
        },
    },
    "Health & Personal Care": {
        "breadcrumb": "Health & Personal Care",
        "department": "Health",
        "products": {
            "apagard-premio-hydroxyapatite-toothpaste-3-7oz": "APAGARD Premio Hydroxyapatite Toothpaste",
            "foodology-coleology-cutting-jelly-250g": "FOODOLOGY Cutting Jelly",
            "okamoto-001-extra-lubricated-condoms-large-fit-6pcs-value-pack": "OKAMOTO 001 Extra Lubricated Value Pack",
            "okamoto-001-ultra-thin-condoms-15pcs-value-pack": "OKAMOTO 001 Ultra Thin Value Pack",
            "sagami-001-original-condoms-10pcs-value-pack": "SAGAMI 001 Original Value Pack",
        },
    },
    "Marketplace": {
        "breadcrumb": "Marketplace",
        "department": "Marketplace",
        "products": {
            "asian-market-online-yami": "Asian Market Online - Yami",
        },
    },
}

DEPARTMENTS = {
    "Beauty": ["Sunscreen", "Serums & Ampoules", "Acne Treatment", "Masks & Sets", "Beauty Devices", "Makeup", "Fragrance"],
    "Food": ["Sauces & Condiments", "Snacks", "Noodles & Ramen", "Canned Food", "Beverages & Tea", "Dried Goods", "Gift Boxes"],
    "Home": ["Rice Cookers", "Kitchen Appliances"],
    "Health": ["Health & Personal Care"],
    "Marketplace": ["Marketplace"],
}


def build_lookup():
    slug_to_info = {}
    for cat_name, cat_data in CATEGORIES.items():
        for slug, display_name in cat_data["products"].items():
            slug_to_info[slug] = {
                "category": cat_name,
                "breadcrumb": cat_data["breadcrumb"],
                "department": cat_data["department"],
                "display_name": display_name,
            }
    return slug_to_info


def get_related_products(current_slug, slug_to_info, max_count=4):
    info = slug_to_info[current_slug]
    cat_name = info["category"]
    dept = info["department"]

    same_cat = [
        (s, CATEGORIES[cat_name]["products"][s])
        for s in CATEGORIES[cat_name]["products"]
        if s != current_slug
    ]

    if len(same_cat) >= 3:
        return same_cat[:max_count]

    related = list(same_cat)
    seen = {current_slug} | {s for s, _ in same_cat}

    for sibling_cat in DEPARTMENTS.get(dept, []):
        if sibling_cat == cat_name:
            continue
        for s, name in CATEGORIES[sibling_cat]["products"].items():
            if s not in seen:
                related.append((s, name))
                seen.add(s)
            if len(related) >= max_count:
                break
        if len(related) >= max_count:
            break

    if len(related) < 3:
        popular = [
            ("biore-uv-aqua-rich-watery-essence-spf50-70g", "Biore UV Aqua Rich Watery Essence SPF50+"),
            ("laoganma-spicy-chili-crispy-7-4oz", "LAOGANMA Spicy Chili Crispy"),
            ("ichiran-ramen-classic-hakata-thin-noodles-5-packs", "ICHIRAN Classic Hakata Tonkotsu Ramen"),
            ("binggrae-banana-flavored-milk-drink-6-packs", "BINGGRAE Banana Flavored Milk"),
            ("tatung-multi-functional-rice-cooker-tac-6g-sf-white", "TATUNG Multi-Functional Rice Cooker"),
        ]
        for s, name in popular:
            if s not in seen:
                related.append((s, name))
                seen.add(s)
            if len(related) >= max_count:
                break

    return related[:max_count]


CSS_BLOCK = """
        /* Breadcrumb Navigation */
        .breadcrumb-nav {
            position: absolute; top: 56px; left: 0; right: 0;
            text-align: center; font-size: 0.75rem; color: var(--gray);
            z-index: 1;
        }
        .breadcrumb-nav a {
            color: var(--primary); text-decoration: none;
            transition: opacity 0.2s;
        }
        .breadcrumb-nav a:hover { opacity: 0.7; }
        .breadcrumb-sep { color: var(--gray); opacity: 0.5; margin: 0 4px; }
        .breadcrumb-current { color: var(--dark); }

        /* Related Products */
        .related-section {
            padding: 80px 24px;
            background: var(--primary-light);
        }
        .related-title {
            font-size: clamp(1.5rem, 3vw, 2.2rem);
            font-weight: 800; text-align: center;
            margin-bottom: 12px; letter-spacing: -0.02em;
            color: var(--dark);
        }
        .related-sub {
            font-size: 0.95rem; color: var(--gray);
            text-align: center; margin-bottom: 40px;
        }
        .related-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px; max-width: 960px; margin: 0 auto;
        }
        .related-card {
            display: flex; align-items: center; justify-content: space-between;
            background: var(--white); border-radius: 16px;
            padding: 20px 24px; text-decoration: none;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .related-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 24px rgba(0,0,0,0.1);
        }
        .related-name {
            font-size: 0.9rem; font-weight: 600;
            color: var(--dark); line-height: 1.3;
        }
        .related-arrow {
            color: var(--primary); font-size: 1.2rem;
            flex-shrink: 0; margin-left: 12px;
        }
        .related-browse {
            text-align: center; margin-top: 32px;
        }
        .related-browse-link {
            color: var(--primary); text-decoration: none;
            font-weight: 600; font-size: 0.9rem;
        }
        .related-browse-link:hover { text-decoration: underline; }"""


def make_breadcrumb_html(breadcrumb_cat, product_name):
    return f"""
        <nav class="breadcrumb-nav" aria-label="Breadcrumb">
            <a href="/">Home</a><span class="breadcrumb-sep">/</span><a href="/landing-pages/">Products</a><span class="breadcrumb-sep">/</span><span class="breadcrumb-current" aria-current="page">{product_name}</span>
        </nav>"""


def make_breadcrumb_jsonld(breadcrumb_cat, product_name):
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://zhouzk.com/"},
            {"@type": "ListItem", "position": 2, "name": "Landing Pages", "item": "https://zhouzk.com/landing-pages/"},
            {"@type": "ListItem", "position": 3, "name": breadcrumb_cat, "item": "https://zhouzk.com/landing-pages/"},
            {"@type": "ListItem", "position": 4, "name": product_name},
        ],
    }
    return f"""
    <script type="application/ld+json">
    {json.dumps(data, indent=2, ensure_ascii=False)}
    </script>"""


def make_related_html(related_products, category_short):
    cards = ""
    for slug, name in related_products:
        cards += f"""            <a href="./{slug}" class="related-card fade-in">
                <span class="related-name">{name}</span>
                <span class="related-arrow">&rarr;</span>
            </a>
"""
    return f"""
    <!-- Related Products -->
    <section class="related-section fade-in" aria-label="Related products">
        <h2 class="related-title">Related Products</h2>
        <p class="related-sub">You might also like these {category_short} products</p>
        <div class="related-grid">
{cards}        </div>
        <div class="related-browse">
            <a href="/landing-pages/" class="related-browse-link">Browse all products &rarr;</a>
        </div>
    </section>
"""


def extract_product_name_from_title(html):
    m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
    if m:
        title = m.group(1).strip()
        title = re.sub(r"\s*[|–—].*$", "", title).strip()
        return title
    return ""


def inject_page(html, slug, slug_to_info):
    info = slug_to_info[slug]
    product_name = extract_product_name_from_title(html)
    if not product_name:
        product_name = info["display_name"]

    breadcrumb_cat = info["breadcrumb"]
    related = get_related_products(slug, slug_to_info)

    # 1. Inject CSS before </style>
    if "/* Breadcrumb Navigation */" in html:
        return html, "already_injected"
    html = html.replace("    </style>", CSS_BLOCK + "\n    </style>", 1)

    # 2. Add position: relative to .hero if not already there
    if "position: relative" not in html.split(".hero")[1].split("}")[0] if ".hero" in html else True:
        html = re.sub(
            r"(\.hero\s*\{)",
            r"\1\n            position: relative;",
            html,
            count=1,
        )

    # 3. Inject breadcrumb HTML as first child of hero section
    breadcrumb_html = make_breadcrumb_html(breadcrumb_cat, product_name)
    hero_pattern = re.compile(r'(<section\s+class="hero"[^>]*>)')
    html = hero_pattern.sub(r"\1" + breadcrumb_html, html, count=1)

    # 4. Inject BreadcrumbList JSON-LD before </head>
    jsonld_html = make_breadcrumb_jsonld(breadcrumb_cat, product_name)
    html = html.replace("</head>", jsonld_html + "\n</head>", 1)

    # 5. Inject Related Products section before <footer>
    related_html = make_related_html(related, breadcrumb_cat.lower())
    html = html.replace("    <footer>", related_html + "    <footer>", 1)

    return html, "ok"


def main():
    dry_run = "--dry-run" in sys.argv
    slug_to_info = build_lookup()

    html_files = sorted(
        f for f in os.listdir(LANDING_DIR)
        if f.endswith(".html") and f not in EXCLUDE_FILES
    )

    print(f"{'[DRY RUN] ' if dry_run else ''}Found {len(html_files)} landing pages to process.\n")

    results = {"ok": 0, "already_injected": 0, "error": 0}
    errors = []

    for filename in html_files:
        slug = filename.replace(".html", "")
        if slug not in slug_to_info:
            errors.append(f"  SKIP {filename}: not in category mapping")
            results["error"] += 1
            continue

        filepath = os.path.join(LANDING_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()

        new_html, status = inject_page(html, slug, slug_to_info)
        results[status] = results.get(status, 0) + 1

        if status == "ok" and not dry_run:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_html)

        info = slug_to_info[slug]
        related = get_related_products(slug, slug_to_info)
        related_names = [name for _, name in related]
        print(f"  {status.upper():20s} {filename}")
        if status == "ok":
            print(f"    Category: {info['category']} | Related: {len(related)} products")

    print(f"\n{'=' * 60}")
    print(f"Results: {results}")
    if errors:
        print(f"\nErrors/Skips:")
        for e in errors:
            print(e)
    if dry_run:
        print("\n[DRY RUN] No files were modified.")


if __name__ == "__main__":
    main()
