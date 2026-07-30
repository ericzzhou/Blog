#!/usr/bin/env python3
"""Inject Pro Tips sections into all product landing pages."""

import glob
import json
import os
import re

BASE = "/Users/ericzhou/workspace/zhouzk.com/homepage/landing-pages"

TIPS_CSS = """
    /* Tips Section */
    .tips-section {
      padding: 4rem 2rem;
      background: var(--cream, #fefcf8);
    }
    .tips-section .section-title {
      text-align: center;
      font-size: 1.6rem;
      margin-bottom: 0.5rem;
    }
    .tips-section .section-subtitle {
      text-align: center;
      color: #666;
      margin-bottom: 2rem;
      font-size: 0.95rem;
    }
    .tips-grid {
      max-width: 800px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1rem;
    }
    .tip-card {
      background: #fff;
      border: 1px solid #e5e7eb;
      border-radius: 10px;
      padding: 1.2rem;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .tip-card:hover {
      border-color: var(--primary, #2563eb);
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .tip-card .tip-icon {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
    }
    .tip-card h3 {
      font-size: 0.95rem;
      margin-bottom: 0.3rem;
    }
    .tip-card p {
      font-size: 0.85rem;
      color: #666;
      line-height: 1.5;
      margin: 0;
    }
"""

def get_category(filepath):
    with open(filepath) as f:
        content = f.read()
    m = re.search(r'"@type":\s*"BreadcrumbList".*?"itemListElement":\s*\[(.*?)\]', content, re.DOTALL)
    if m:
        names = re.findall(r'"name":\s*"([^"]+)"', m.group(1))
        if len(names) >= 3:
            return names[2]
    return None

def get_product_name(filepath):
    with open(filepath) as f:
        content = f.read()
    m = re.search(r'"@type":\s*"Product".*?"name":\s*"([^"]+)"', content, re.DOTALL)
    if m:
        return m.group(1)
    return os.path.basename(filepath).replace('.html', '').replace('-', ' ').title()

# ── Tips content by category ─────────────────────────────────────────

def tips_sunscreen(product, brand, **kw):
    return [
        ("☀️", "Two-Finger Rule", "Apply two finger-lengths of sunscreen for full face and neck coverage. Most people under-apply, reducing actual SPF protection."),
        ("🔄", "Reapply Every 2 Hours", "Set a timer when outdoors. Reapply immediately after swimming, sweating, or towel-drying — even with water-resistant formulas."),
        ("🧴", "Layer Correctly", "Apply sunscreen as the LAST step of skincare, BEFORE makeup. Wait 1-2 minutes for it to set before applying primer or foundation."),
        ("📅", "Check Expiry Dates", "Sunscreen loses effectiveness after expiration. Most products are good for 12 months after opening. Write the open date on the bottle."),
    ]

def tips_beverages_tea(product, brand, **kw):
    return [
        ("🌡️", "Serve at Right Temperature", "Green/jasmine tea: 175°F (80°C). Black tea: 200°F (93°C). Matcha: 160°F (70°C). Wrong temperature kills flavor."),
        ("🫖", "Steep Time Matters", "Green tea: 1-2 minutes. Black tea: 3-5 minutes. Over-steeping makes tea bitter. Use a timer for consistent results."),
        ("🧊", "Iced Tea Shortcut", "Brew double-strength hot tea, then pour over ice. This prevents dilution and keeps the full flavor profile intact."),
        ("📦", "Storage Tips", "Keep tea in an airtight container away from light, heat, and moisture. Never store near spices — tea absorbs surrounding odors."),
    ]

def tips_noodles_ramen(product, brand, **kw):
    return [
        ("💧", "Exact Water Amount", "Use exactly the amount of water specified on the package. Too much water dilutes the broth; too little makes it overly salty."),
        ("⏱️", "Timing Is Everything", "Cook noodles for the exact time listed (usually 3-4 min). Overcooked noodles turn mushy. Set a timer — don't guess."),
        ("🥚", "Upgrade Your Bowl", "Add a soft-boiled egg (6.5 min boil), sliced green onions, or a sheet of nori. These $1 additions make it restaurant-quality."),
        ("🔥", "Broth Last", "Add the seasoning packet AFTER draining most water, not during boiling. This preserves the full flavor intensity."),
    ]

def tips_sauces_condiments(product, brand, **kw):
    return [
        ("🥄", "Start Small", "Asian condiments are often more intense than Western equivalents. Start with half the amount you'd use for soy sauce or vinegar, then adjust."),
        ("🧊", "Refrigerate After Opening", "Most Asian sauces and pastes last longer refrigerated. Laoganma chili crisp, gochujang, and miso all benefit from cold storage."),
        ("🍳", "Cooking vs Dipping", "Many condiments work both ways. Add chili oil during stir-frying for depth, or drizzle on finished dishes for a flavor punch."),
        ("📅", "Check the Date", "Artisanal sauces often have shorter shelf lives than mass-produced ones. Use within 3-6 months of opening for peak flavor."),
    ]

def tips_rice_cookers(product, brand, **kw):
    return [
        ("🍚", "Rinse Rice 3 Times", "Always rinse rice until water runs clear. This removes excess starch and prevents gummy texture. Use the included measuring cup for accuracy."),
        ("⚡", "Use the Right Setting", "White rice ≠ brown rice ≠ sushi rice. Each grain type has an optimal cooking program. Using the wrong setting affects texture significantly."),
        ("🧹", "Clean the Steam Vent", "Monthly, check and clean the steam vent and inner lid gasket. Buildup affects cooking performance and can cause odors."),
        ("📏", "Water Ratio Matters", "Follow the water level lines inside the pot. They account for the rice cup measurement (180ml), not US cups (240ml)."),
    ]

def tips_kitchen_appliances(product, brand, **kw):
    return [
        ("📖", "Read the Manual First", "Asian appliances often have features not common in US models. The manual explains special settings that can transform your cooking."),
        ("🔌", "Verify Voltage", "Confirm your appliance is rated for US 120V before first use. Using a 100V Japanese domestic model without a transformer will damage it."),
        ("🧹", "Regular Maintenance", "Clean removable parts after each use. Descale kettles monthly with vinegar solution. This extends appliance life by years."),
        ("📐", "Don't Overfill", "Respect the max fill lines. Overfilling soy milk makers or electric skilts causes spills and can damage heating elements."),
    ]

def tips_hair_care(product, brand, **kw):
    return [
        ("🚿", "Squeeze Before Applying", "Gently squeeze excess water from hair before applying masks. Too much water dilutes the treatment and reduces effectiveness."),
        ("⏰", "3-5 Minutes Is Enough", "Japanese hair masks are concentrated. Leaving them on longer than recommended doesn't add benefits and can weigh hair down."),
        ("🎯", "Mid-Lengths to Ends Only", "Apply masks and treatments from mid-lengths to ends. Avoid the scalp — this prevents greasy roots and clogged follicles."),
        ("🌡️", "Warm Towel Boost", "Wrap hair in a warm (not hot) towel for 2 minutes after applying the mask. Heat opens cuticles and improves ingredient absorption."),
    ]

def tips_serums_ampoules(product, brand, **kw):
    return [
        ("🤲", "Press, Don't Rub", "Korean serums are best applied by gently pressing into skin. Rubbing creates friction and can irritate. Pat until fully absorbed."),
        ("📐", "Thinnest to Thickest", "Apply in order of texture: watery toner → serum/ampoule → essence → moisturizer. This ensures each layer penetrates properly."),
        ("🌙", "Night Is Prime Time", "Skin repair peaks at night. Use active serums (retinol, peptides, vitamin C) in your PM routine for maximum effectiveness."),
        ("💧", "Less Is More", "A pea-sized amount covers the full face. Over-applying serum doesn't increase benefits — it wastes product and can cause pilling."),
    ]

def tips_acne_treatment(product, brand, **kw):
    return [
        ("🧼", "Cleanse First", "Always apply acne treatment to clean, dry skin. Residual makeup or sunscreen blocks active ingredients from reaching the blemish."),
        ("📏", "Thin Layer Only", "More product ≠ faster results. A thin, even layer is optimal. Over-application causes dryness and irritation without speeding healing."),
        ("☀️", "Sunscreen Is Mandatory", "Acne treatments increase sun sensitivity. Always apply SPF 30+ during the day, even if you're mostly indoors."),
        ("⏳", "Give It 4-6 Weeks", "Skin cycles take about 28 days. Most acne treatments need 4-6 weeks of consistent use before you see significant improvement."),
    ]

def tips_beauty_devices(product, brand, **kw):
    return [
        ("🧴", "Use Conductive Gel", "RF and microcurrent devices need a conductive medium. Use the recommended gel or a water-based serum — never on dry skin."),
        ("🔄", "Consistent Motion", "Keep the device moving in upward, outward strokes. Staying in one spot too long can cause irritation or uneven results."),
        ("📅", "3-5 Times Per Week", "More is not better. Skin needs recovery time between sessions. Follow the recommended frequency for your device type."),
        ("🧹", "Clean After Each Use", "Wipe the device head with a soft cloth after every session. Buildup affects conductivity and can harbor bacteria."),
    ]

def tips_masks_sets(product, brand, **kw):
    return [
        ("🧼", "Clean Skin First", "Apply masks to freshly cleansed skin. Residual dirt or makeup blocks the essence from penetrating effectively."),
        ("⏱️", "Don't Overdo the Time", "15-20 minutes is optimal. Leaving a sheet mask on until it dries out actually reverses the hydration — the mask starts absorbing moisture FROM your skin."),
        ("👋", "Pat the Excess", "After removing the mask, pat remaining essence into skin instead of washing it off. This is concentrated treatment serum."),
        ("🔒", "Seal with Moisturizer", "Apply moisturizer after the mask to lock in all the active ingredients. Without this step, much of the benefit evaporates."),
    ]

def tips_snacks(product, brand, **kw):
    return [
        ("📦", "Reseal Tightly", "Asian snacks often come in packaging without zip locks. Use clips or transfer to airtight containers to maintain freshness and crunch."),
        ("🌡️", "Room Temperature Is Best", "Many Asian snacks taste best at room temperature. Rice crackers, mochi, and cookies lose texture when refrigerated."),
        ("🍵", "Pair with Tea", "Traditional Asian snacks are designed to pair with tea. Matcha with sweet snacks, jasmine with savory — the combinations enhance both."),
        ("📅", "Check Best-By Dates", "Imported snacks may have shorter shelf lives than domestic products. Check dates upon arrival and consume within recommended timeframes."),
    ]

def tips_dried_goods(product, brand, **kw):
    return [
        ("🫙", "Airtight Storage", "Transfer dried goods to glass jars with tight lids. This prevents moisture absorption and keeps flavors intact for months."),
        ("🧊", "Freeze for Longevity", "Goji berries, jujubes, and similar dried fruits last even longer in the freezer. No need to thaw before adding to soups or teas."),
        ("🚿", "Rinse Before Use", "Quick-rinse dried goods under cold water before cooking. This removes any dust or residue from the drying process."),
        ("🍲", "Add Late in Cooking", "For soups and stews, add dried goods in the last 15-20 minutes. Overcooking breaks them down and loses their texture and nutrients."),
    ]

def tips_gift_boxes(product, brand, **kw):
    return [
        ("🎁", "Gift-Ready Packaging", "These products come in presentation-ready packaging. No additional wrapping needed for most occasions — just add a card."),
        ("🌡️", "Store Cool and Dry", "Keep gift boxes away from heat and humidity. Chocolate and pastry items are especially sensitive to temperature changes."),
        ("📅", "Check Best-By Dates", "Gift boxes contain multiple items with different shelf lives. Check all dates before gifting to ensure freshness."),
        ("✈️", "Shipping Tips", "If shipping directly to the recipient, choose expedited delivery for perishable items. Add a gift note at checkout on Yami."),
    ]

def tips_health_personal_care(product, brand, **kw):
    return [
        ("📖", "Follow the Instructions", "Read and follow the product directions carefully. Dosage and application methods are optimized for safety and effectiveness."),
        ("🧴", "Patch Test First", "For any new personal care product, test on a small area of skin first. Wait 24 hours to check for reactions before full use."),
        ("📅", "Track Usage", "Note when you opened the product. Most personal care items have a PAO (Period After Opening) symbol showing how many months they're good for."),
        ("🌡️", "Store Properly", "Keep personal care products in a cool, dry place. Bathroom humidity can degrade product quality over time."),
    ]

def tips_canned_food(product, brand, **kw):
    return [
        ("🥫", "Check the Can", "Before use, inspect for dents, bulges, or rust. Damaged cans may compromise food safety. When in doubt, don't use it."),
        ("🧊", "Refrigerate After Opening", "Once opened, transfer contents to a glass or plastic container. Don't store open cans in the fridge — the metal can affect flavor."),
        ("🍳", "Heat Gently", "Canned fish and seafood are already cooked. Heat gently if desired — overcooking makes them tough and dry."),
        ("📅", "Rotate Your Stock", "Practice FIFO (First In, First Out). Use older cans first and check best-by dates regularly."),
    ]

def tips_fragrance(product, brand, **kw):
    return [
        ("💫", "Pulse Points", "Apply to wrists, inner elbows, behind ears, and base of throat. Body heat at these points helps project the fragrance throughout the day."),
        ("🚫", "Don't Rub Wrists", "After spraying, let the fragrance dry naturally. Rubbing breaks down top notes and changes the scent profile."),
        ("👕", "Fabric Lasts Longer", "Fragrance lasts longer on fabric than skin. Lightly spritz on clothing collar or scarf for all-day wear (test on inconspicuous area first)."),
        ("📦", "Store Away from Light", "Keep perfume in its box or a dark drawer. UV light and heat degrade fragrance oils, changing the scent over time."),
    ]

def tips_makeup(product, brand, **kw):
    return [
        ("🧴", "Prep Your Skin", "Cleanse, tone, and moisturize before applying makeup. Well-prepped skin creates a smooth canvas and helps foundation last longer."),
        ("📐", "Less Is More", "Japanese makeup is designed for buildable coverage. Start with a thin layer and add only where needed for a natural finish."),
        ("💡", "Blend the Edges", "The key to natural-looking foundation is blending at the jawline, hairline, and nose. Use a damp sponge or brush for seamless edges."),
        ("🌙", "Double Cleanse at Night", "After wearing makeup, use an oil cleanser first, then a water-based cleanser. This ensures complete removal without stripping skin."),
    ]

def tips_marketplace(product, brand, **kw):
    return [
        ("🛒", "Bundle for Free Shipping", "Yami offers free shipping on orders over $49. Plan your order to hit the threshold — it's easy with 10,000+ products."),
        ("📅", "Check Expiry Dates", "All products show lot and expiry information. Yami's US warehouse QC verifies these before shipping."),
        ("🔍", "Read Product Descriptions", "Asian products may have different formulations than Western equivalents. Check ingredients and size carefully before ordering."),
        ("⭐", "Use Reviews", "Yami product reviews include photos and verified purchase tags. They're a great resource for checking authenticity and quality."),
    ]

TIPS_MAP = {
    "Sunscreen": tips_sunscreen,
    "Beverages & Tea": tips_beverages_tea,
    "Noodles & Ramen": tips_noodles_ramen,
    "Sauces & Condiments": tips_sauces_condiments,
    "Rice Cookers": tips_rice_cookers,
    "Kitchen Appliances": tips_kitchen_appliances,
    "Hair Care": tips_hair_care,
    "Serums & Ampoules": tips_serums_ampoules,
    "Acne Treatment": tips_acne_treatment,
    "Beauty Devices": tips_beauty_devices,
    "Masks & Sets": tips_masks_sets,
    "Snacks": tips_snacks,
    "Dried Goods": tips_dried_goods,
    "Gift Boxes": tips_gift_boxes,
    "Health & Personal Care": tips_health_personal_care,
    "Canned Food": tips_canned_food,
    "Fragrance": tips_fragrance,
    "Makeup": tips_makeup,
    "Marketplace": tips_marketplace,
}

def build_tips_html(product, tips_items):
    cards = ""
    for icon, title, desc in tips_items:
        cards += f"""        <div class="tip-card">
            <div class="tip-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
"""
    return f"""
    <!-- Pro Tips Section -->
    <section class="tips-section" aria-label="Pro tips">
        <h2 class="section-title">Pro Tips for {product.split('|')[0].strip()[:40]}</h2>
        <p class="section-subtitle">Get the most out of your purchase with these practical tips</p>
        <div class="tips-grid">
{cards}        </div>
    </section>
"""

def inject_tips(filepath, dry_run=False):
    basename = os.path.basename(filepath)
    category = get_category(filepath)
    if not category or category not in TIPS_MAP:
        print(f"  SKIP (no category): {basename}")
        return False

    product = get_product_name(filepath)
    tips_fn = TIPS_MAP[category]
    tips_items = tips_fn(product=product, brand=category)

    with open(filepath) as f:
        content = f.read()

    if 'class="tips-section"' in content:
        print(f"  SKIP (tips exists): {basename}")
        return False

    tips_html = build_tips_html(product, tips_items)

    if dry_run:
        print(f"  DRY: {basename} ({category}, {len(tips_items)} tips)")
        return True

    # Inject CSS before last </style> before </head>
    head_end = content.find('</head>')
    style_end = content.rfind('</style>', 0, head_end)
    if style_end == -1:
        print(f"  ERROR (no </style>): {basename}")
        return False
    content = content[:style_end] + TIPS_CSS + "\n" + content[style_end:]

    # Inject HTML before FAQ section (or before CTA if no FAQ)
    faq_pos = content.find('    <!-- FAQ Section -->')
    if faq_pos != -1:
        content = content[:faq_pos] + tips_html + "\n" + content[faq_pos:]
    else:
        cta_pos = content.find('    <!-- CTA -->')
        if cta_pos == -1:
            cta_pos = content.find('    <!-- Final CTA -->')
        if cta_pos != -1:
            content = content[:cta_pos] + tips_html + "\n" + content[cta_pos:]
        else:
            print(f"  WARN (no injection point): {basename}")
            return False

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"  OK: {basename} ({category}, {len(tips_items)} tips)")
    return True


def main():
    import sys
    dry_run = '--dry-run' in sys.argv

    files = sorted(glob.glob(os.path.join(BASE, "*.html")))
    skip = {'index.html', 'test-simple.html', 'kikkoman-fixed.html'}
    files = [f for f in files if os.path.basename(f) not in skip]

    print(f"Processing {len(files)} pages (dry_run={dry_run})...\n")
    ok = skip_count = 0
    for f in files:
        if inject_tips(f, dry_run=dry_run):
            ok += 1
        else:
            skip_count += 1
    print(f"\nDone: {ok} injected, {skip_count} skipped")


if __name__ == "__main__":
    main()
