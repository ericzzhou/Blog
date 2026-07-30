#!/usr/bin/env python3
"""Inject FAQ sections with FAQPage schema into all product landing pages."""

import glob
import json
import os
import re

BASE = "/Users/ericzhou/workspace/zhouzk.com/homepage/landing-pages"

FAQ_CSS = """
    /* FAQ Section */
    .faq-section {
      padding: 5rem 2rem;
      background: #fafafa;
    }
    .faq-section .section-title {
      text-align: center;
      font-size: 1.8rem;
      margin-bottom: 0.5rem;
    }
    .faq-section .section-subtitle {
      text-align: center;
      color: #666;
      margin-bottom: 2.5rem;
      font-size: 1rem;
    }
    .faq-list {
      max-width: 760px;
      margin: 0 auto;
    }
    .faq-list details {
      background: #fff;
      border: 1px solid #e5e7eb;
      border-radius: 10px;
      margin-bottom: 0.75rem;
      overflow: hidden;
      transition: border-color 0.2s;
    }
    .faq-list details[open] {
      border-color: var(--primary, #2563eb);
    }
    .faq-list summary {
      padding: 1rem 1.25rem;
      cursor: pointer;
      font-weight: 600;
      font-size: 1rem;
      list-style: none;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .faq-list summary::-webkit-details-marker { display: none; }
    .faq-list summary::after {
      content: '+';
      font-size: 1.3rem;
      font-weight: 300;
      color: #999;
      transition: transform 0.2s;
    }
    .faq-list details[open] summary::after {
      content: '−';
    }
    .faq-list .faq-answer {
      padding: 0 1.25rem 1rem;
      color: #555;
      line-height: 1.7;
      font-size: 0.95rem;
    }
    .faq-list .faq-answer a {
      color: var(--primary, #2563eb);
      text-decoration: underline;
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
    slug = os.path.basename(filepath).replace('.html', '').replace('-', ' ')
    return slug.title()

def get_brand(filepath):
    with open(filepath) as f:
        content = f.read()
    m = re.search(r'"brand".*?"name":\s*"([^"]+)"', content, re.DOTALL)
    if m:
        return m.group(1)
    return None

# ── FAQ content by category ──────────────────────────────────────────
# Each function returns list of (question, answer) tuples.
# {product} and {brand} are replaced at injection time.

def faq_sunscreen(product, brand, **kw):
    return [
        (f"Is {product} suitable for sensitive skin?",
         f"{brand} sunscreens are generally formulated for daily wear and are suitable for most skin types. However, always check the ingredient list for specific allergens. Patch-test on a small area before full application."),
        ("What is the difference between Korean and Japanese sunscreens?",
         "Korean sunscreens tend to focus on skincare benefits (hydration, brightening) with lightweight textures. Japanese sunscreens often prioritize water-resistance and UV protection for active lifestyles. Both use advanced UV filters not yet available in US-manufactured products."),
        ("How much sunscreen should I apply for full face coverage?",
         "Apply approximately two finger-lengths (index and middle finger) of sunscreen for adequate face and neck coverage. Reapply every 2 hours when outdoors, or immediately after swimming or heavy sweating."),
        (f"Does {product} leave a white cast?",
         f"Most modern Korean and Japanese sunscreens like {product} are formulated to minimize white cast. Chemical and hybrid filters tend to blend more seamlessly than pure mineral sunscreens. Allow 1-2 minutes for the product to settle before applying makeup."),
    ]

def faq_beverages_tea(product, brand, **kw):
    return [
        (f"How should I store {product}?",
         "Store in a cool, dry place away from direct sunlight. Once opened, refrigerate and consume within 5-7 days for best flavor. Unopened shelf-stable packages can be kept at room temperature until the best-by date."),
        (f"Is {product} suitable for a low-sugar diet?",
         f"Check the nutrition label on the product page for specific sugar content. Many Asian beverages now offer sugar-free or reduced-sugar options. {brand} products vary — some use natural sweeteners while others contain added sugar."),
        ("Are Asian beverages different from Western equivalents?",
         "Asian beverages often use different ingredients and flavor profiles — matcha instead of coffee, real fruit extracts instead of artificial flavors, and traditional recipes passed down through generations. The taste experience is typically more nuanced and less overly sweet."),
        (f"Can I buy {product} in bulk?",
         f"Yes, {product} is available in multi-pack options on Yami. Bulk purchases often come with a per-unit discount. Check the product page for current bundle deals and value packs."),
    ]

def faq_noodles_ramen(product, brand, **kw):
    return [
        (f"How do I cook {product} at home?",
         f"Follow the package instructions for best results. Generally: bring 500ml water to a boil, cook noodles for 3-4 minutes, drain, then add the seasoning packets. For {brand} ramen, the broth packet is designed to be mixed with the cooking water for maximum flavor."),
        (f"Is {product} spicy?",
         f"{brand} offers a range of spice levels. Check the product label for heat indicators. If you prefer milder flavors, start with non-spicy varieties and gradually work up. You can also adjust the chili oil packet to your preference."),
        ("What makes Asian ramen different from instant noodles?",
         "Premium Asian ramen uses higher-quality wheat noodles with better texture, and broth packets made from real bone or vegetable extracts rather than just MSG and salt. The result is a richer, more authentic restaurant-quality bowl at home."),
        (f"Does {product} contain allergens?",
         f"Most ramen products contain wheat, soy, and may contain traces of egg, milk, or shellfish. Check the ingredient list on the product page carefully if you have food allergies. {brand} products clearly label major allergens."),
    ]

def faq_sauces_condiments(product, brand, **kw):
    return [
        (f"How long does {product} last after opening?",
         f"Once opened, {product} should be stored in the refrigerator and used within 3-6 months for optimal flavor. Unopened, it can be kept in a cool, dry place until the best-by date printed on the package."),
        (f"What dishes pair well with {product}?",
         f"{product} by {brand} is versatile — use it as a dipping sauce, cooking ingredient, or finishing condiment. It works well with rice, noodles, stir-fries, dumplings, and grilled meats. Explore our Asian snacks and ramen categories for more pairing ideas."),
        (f"Is {product} suitable for vegetarians or vegans?",
         f"Check the ingredient list on the product page. Many Asian condiments are plant-based, but some contain fish sauce, oyster extract, or shrimp paste. {brand} clearly labels allergens and dietary information on packaging."),
        (f"Can I use {product} in cooking, or is it just a dipping sauce?",
         f"{product} works both ways. As a dipping sauce, it adds instant flavor. In cooking, add it during stir-frying, marinating, or as a finishing drizzle. Heat can mellow or intensify flavors depending on the product."),
    ]

def faq_rice_cookers(product, brand, **kw):
    return [
        (f"What is the difference between IH and conventional {brand} rice cookers?",
         f"Induction Heating (IH) rice cookers like {product} use electromagnetic fields to heat the entire inner pot evenly, resulting in more consistent cooking. Conventional models use a heating plate at the bottom. IH models are better for sushi rice, GABA brown rice, and mixed grain settings."),
        (f"How do I cook GABA brown rice in {product}?",
         f"Select the GABA Brown Rice setting on your {brand} cooker. This mode soaks rice at a warm temperature (about 104°F/40°C) for several hours before cooking to activate germination, increasing GABA content. Rinse rice first and use the included measuring cup for accurate ratios."),
        (f"What size {brand} rice cooker do I need?",
         f"A 5.5-cup cooker suits 1-3 people. A 10-cup cooker is better for families of 4-6 or batch cooking. Remember that 'cup' in rice cooker terms is ~180ml (a Japanese rice cup), not a US measuring cup. {product} capacity is listed on the product page."),
        (f"Is {product} compatible with US voltage?",
         f"Yes — {brand} rice cookers sold through Yami are designed for US 120V outlets. No voltage converter needed. For Japanese domestic models purchased elsewhere, always verify voltage compatibility before use."),
    ]

def faq_kitchen_appliances(product, brand, **kw):
    return [
        (f"Is {product} compatible with US voltage?",
         f"{product} by {brand} sold through Yami is designed for US 120V/60Hz outlets. No voltage converter is needed. Always check the product specifications on the listing to confirm compatibility."),
        (f"How do I clean and maintain {product}?",
         f"Refer to the user manual included with {product}. Generally: unplug before cleaning, use a damp cloth for the exterior, and follow specific cleaning instructions for removable parts. {brand} products are designed for easy maintenance."),
        (f"Does {product} come with a warranty?",
         f"{brand} products sold on Yami come with the manufacturer's standard warranty. Check the product page for specific warranty terms. Keep your receipt and packaging for warranty claims."),
        (f"Can {product} be used for meal prep?",
         f"Yes, {product} is designed for regular home use and works well for meal prep. Check the capacity and features on the product page to ensure it meets your cooking needs."),
    ]

def faq_hair_care(product, brand, **kw):
    return [
        (f"How often should I use {product}?",
         f"For hair masks like {product}, use 1-2 times per week after shampooing. Apply to damp hair focusing on mid-lengths and ends. Leave on for 3-5 minutes (or as directed), then rinse thoroughly. {brand} formulas are designed for regular use without buildup."),
        (f"Is {product} suitable for color-treated hair?",
         f"Most {brand} hair care products are gentle enough for color-treated hair. {product} helps restore moisture and shine that can be diminished by coloring. Check the product label for specific compatibility notes."),
        ("What is the difference between Fino and Tsubaki hair masks?",
         "Fino (by Shiseido) focuses on deep repair with royal jelly and PCA, ideal for damaged or chemically treated hair. Tsubaki (by Shiseido) uses camellia oil for hydration and shine, better for dry or frizzy hair. Both are premium Japanese formulas."),
        (f"Does {product} contain silicones?",
         f"Check the ingredient list on the product page. Some {brand} products contain silicones for smoothness and shine, while others are silicone-free. Both approaches have benefits — silicones provide immediate detangling, while silicone-free formulas build long-term hair health."),
    ]

def faq_serums_ampoules(product, brand, **kw):
    return [
        (f"When should I apply {product} in my skincare routine?",
         f"Apply {product} after cleansing and toning, but before moisturizer. Serums and ampoules are concentrated treatments designed to penetrate deeply. {brand} recommends pressing (not rubbing) the product into skin for maximum absorption."),
        (f"How long does it take to see results from {product}?",
         f"Most users notice initial improvements in hydration and texture within 1-2 weeks. Significant results for concerns like fine lines, dark spots, or elasticity typically require 4-8 weeks of consistent use. {product} is formulated for daily use."),
        (f"Can I layer {product} with other active ingredients?",
         f"{product} can generally be layered with complementary ingredients. However, avoid combining with strong exfoliants (AHA/BHA) or retinol in the same routine unless directed. When in doubt, alternate AM/PM usage."),
        (f"Is {product} suitable for all skin types?",
         f"{brand} formulates for a range of skin types. {product} is generally suitable for normal to dry skin. If you have oily or acne-prone skin, check the texture and ingredient list on the product page for compatibility."),
    ]

def faq_acne_treatment(product, brand, **kw):
    return [
        (f"How do I use {product} for best results?",
         f"Cleanse the affected area gently, then apply a thin layer of {product} 1-2 times daily. Start with once daily to assess tolerance. {brand} products are formulated for consistent daily use. Avoid picking or squeezing blemishes during treatment."),
        (f"Is {product} suitable for hormonal acne?",
         f"{product} can help with various types of acne including hormonal breakouts. However, persistent hormonal acne may require dermatologist consultation. {brand} acne products are designed for mild to moderate acne and work best as part of a consistent skincare routine."),
        ("Can I use acne treatment with sunscreen?",
         "Yes — sunscreen is essential when using acne treatments, as some active ingredients can increase sun sensitivity. Apply acne treatment first, wait 5-10 minutes, then apply sunscreen. Explore our sunscreen category for Korean and Japanese options that pair well."),
        (f"How long before I see improvement with {product}?",
         f"Most users see initial improvement within 1-2 weeks. Full results typically appear after 4-6 weeks of consistent use. If no improvement after 8 weeks, consider consulting a dermatologist. {product} works best with regular, uninterrupted use."),
    ]

def faq_beauty_devices(product, brand, **kw):
    return [
        (f"How do I use {product}?",
         f"Cleanse your face thoroughly before using {product}. Apply the recommended conductive gel or serum, then glide the device across your face following the included instructions. {brand} devices typically recommend 5-10 minute sessions, 3-5 times per week."),
        (f"Is {product} safe for sensitive skin?",
         f"{brand} beauty devices are designed with multiple intensity levels for different skin sensitivities. Start on the lowest setting and gradually increase. {product} is generally safe for sensitive skin when used as directed. Discontinue if irritation occurs."),
        (f"How long before I see results from {product}?",
         f"Results vary by device type and concern. Most users notice improved skin texture and radiance within 2-4 weeks of consistent use. Anti-aging and firming benefits typically require 6-8 weeks. {product} works best with regular use as part of a complete skincare routine."),
        (f"Does {product} need replacement parts?",
         f"Check the product page for maintenance requirements. Some {brand} devices have replaceable gel pads or heads. The main device unit is designed for long-term use with proper care and cleaning."),
    ]

def faq_masks_sets(product, brand, **kw):
    return [
        (f"How often should I use {product}?",
         f"Sheet masks can be used 2-3 times per week for maintenance, or daily for intensive treatment. {product} by {brand} is designed for regular use. For best results, apply to clean skin and leave on for the recommended time (usually 15-20 minutes)."),
        (f"Should I rinse off after using {product}?",
         f"Generally, no — gently pat the remaining essence into your skin. The leftover serum contains active ingredients that continue working. {brand} mask essences are designed to be absorbed, not washed off. Follow with moisturizer to seal in benefits."),
        (f"Is {product} suitable for sensitive skin?",
         f"Check the ingredient list on the product page. {brand} products are generally well-tolerated, but individual reactions vary. If you have sensitive skin, patch-test first. Look for calming ingredients like centella, madecassoside, or panthenol."),
        (f"Can I use {product} with other skincare products?",
         f"Yes — {product} works well as a treatment step in your routine. Apply after cleansing and toning, before serums and moisturizer. The mask preps your skin to better absorb subsequent products."),
    ]

def faq_snacks(product, brand, **kw):
    return [
        (f"How should I store {product}?",
         f"Store {product} in a cool, dry place. Once opened, reseal the package tightly or transfer to an airtight container to maintain freshness. Most Asian snacks are best consumed within 1-2 weeks of opening."),
        (f"Is {product} suitable for vegetarians?",
         f"Check the ingredient list on the product page. Many Asian snacks are plant-based, but some contain animal-derived ingredients like fish sauce, bonito extract, or gelatin. {brand} clearly labels allergens on packaging."),
        ("Are Asian snacks different from Western snacks?",
         "Asian snacks often feature unique flavors and textures — mochi, seaweed, rice crackers, and konjac jelly are hard to find in Western snack aisles. They tend to be less sweet, use more natural ingredients, and offer savory and umami options alongside sweet."),
        (f"Can I buy {product} in bulk?",
         f"Yes, {product} is available in multi-pack and value pack options on Yami. Bulk purchases often come with per-unit savings. Check the product page for current bundle deals."),
    ]

def faq_dried_goods(product, brand, **kw):
    return [
        (f"How should I store {product}?",
         f"Store {product} in a cool, dry place in an airtight container. Dried goods have long shelf lives but can absorb moisture and lose flavor if exposed to humidity. Once opened, refrigeration can extend freshness."),
        (f"What are the health benefits of {product}?",
         f"{product} by {brand} is a traditional Asian ingredient valued for its nutritional properties. Dried goods like jujubes, goji berries, and similar products are rich in vitamins, minerals, and antioxidants. Check the product page for specific nutritional information."),
        (f"How do I use {product} in cooking?",
         f"{product} can be eaten as a snack, added to teas and soups, or used in traditional Chinese medicine recipes. Rinse before use. For soups and teas, add during the last 15-20 minutes of cooking. {brand} products are pre-cleaned and ready to use."),
        (f"Is {product} organic?",
         f"Check the product packaging and description on the product page for organic certification. {brand} sources from reputable suppliers. Some dried goods in our collection are certified organic, while others follow traditional cultivation methods."),
    ]

def faq_gift_boxes(product, brand, **kw):
    return [
        (f"Is {product} suitable for gifting?",
         f"Absolutely — {product} by {brand} is designed as a premium gift option. The packaging is gift-ready, making it perfect for holidays, birthdays, housewarmings, and corporate gifts. Many customers purchase multiple sets during festive seasons."),
        (f"How long does {product} stay fresh?",
         f"Check the best-by date printed on the packaging. {product} typically has a shelf life of several months when stored properly in a cool, dry place. Once opened, consume within the timeframe indicated on the package for best quality."),
        (f"Can I ship {product} as a gift?",
         f"Yes, {product} can be shipped directly through Yami. The sturdy packaging is designed to withstand shipping. Consider adding a delivery note if sending directly to the recipient. Free shipping is available on orders over $49."),
        (f"Does {product} contain common allergens?",
         f"Gift boxes often contain multiple products with different ingredients. Check the product page for a complete allergen list. {brand} clearly labels major allergens including nuts, dairy, soy, wheat, and eggs."),
    ]

def faq_health_personal_care(product, brand, **kw):
    return [
        (f"How do I use {product} correctly?",
         f"Follow the instructions on the product packaging for best results. {product} by {brand} is designed for daily use. If you have specific concerns or conditions, consult with a healthcare professional before use."),
        (f"Is {product} safe for daily use?",
         f"{brand} products are formulated for regular use when following the recommended dosage or application instructions. {product} has been tested for safety. If you experience any irritation, discontinue use and consult a professional."),
        (f"Does {product} contain any harmful ingredients?",
         f"{product} sold on Yami meets safety standards for the US market. Check the ingredient list on the product page for specific components. {brand} products are manufactured under strict quality control."),
        (f"Where is {product} manufactured?",
         f"{product} by {brand} is manufactured in its country of origin (check product page for specific details). Yami verifies procurement from authorized distributors to ensure authenticity and quality."),
    ]

def faq_canned_food(product, brand, **kw):
    return [
        (f"How long does {product} last?",
         f"Canned products like {product} have a long shelf life — typically 1-3 years from the manufacturing date. Check the best-by date on the can. Once opened, transfer to a glass container, refrigerate, and consume within 3-4 days."),
        (f"Is {product} BPA-free?",
         f"Check the product packaging or description for BPA-free labeling. {brand} and many major food manufacturers have moved to BPA-free can linings. Yami product pages list available packaging information."),
        (f"How can I use {product} in recipes?",
         f"{product} is versatile — use it straight from the can, add to rice bowls, mix into pasta or stir-fry, or use as a topping. {brand} canned products are pre-cooked and ready to eat, making them convenient for quick meals."),
        (f"Is {product} a good source of protein?",
         f"Canned fish and seafood products are typically excellent sources of protein and omega-3 fatty acids. Check the nutrition facts on the {product} page for specific protein content per serving."),
    ]

def faq_fragrance(product, brand, **kw):
    return [
        (f"How long does {product} last on skin?",
         f"{product} by {brand} is an eau de parfum concentration, typically lasting 6-8 hours on skin. The amber and musk base notes provide excellent longevity. Apply to pulse points (wrists, neck, behind ears) for best projection."),
        (f"Is {product} the same fragrance worn by Jennie from BLACKPINK?",
         f"Yes — {product} (#CHAMO) is the signature fragrance associated with Jennie. It features chamomile, clary sage, and warm musk notes. The scent is unisex-leaning-feminine and evolves beautifully throughout the day."),
        (f"Can I layer {product} with other fragrances?",
         f"{product} has a complex scent profile that works well on its own. If you wish to layer, pair with unscented body products or a complementary scent from the same {brand} line. Avoid mixing with strongly competing fragrances."),
        (f"Is {product} worth the price?",
         f"At $145.11 (20% off), {product} offers Korean luxury perfumery at a competitive price point compared to Western niche fragrances ($200-400+). The quality of ingredients and unique botanical blend make it a standout value in the luxury fragrance category."),
    ]

def faq_makeup(product, brand, **kw):
    return [
        (f"How do I find my shade in {product}?",
         f"Check the product page for shade descriptions and swatches. {brand} typically offers shade guides. For foundation products like {product}, match to your jawline skin tone. When between shades, choose the lighter option for a more natural look."),
        (f"Is {product} suitable for sensitive skin?",
         f"{product} by {brand} is formulated with skincare ingredients that are generally well-tolerated. Check the ingredient list for specific allergens. Japanese makeup products like {brand} often include beneficial skincare actives."),
        (f"How do I apply {product} for best results?",
         f"Apply {product} to moisturized, prepped skin. Use a damp beauty sponge, brush, or clean fingers depending on the product type. {brand} products are designed for buildable coverage — start with a thin layer and add where needed."),
        (f"Does {product} oxidize during the day?",
         f"High-quality Japanese foundations like {product} are formulated to resist oxidation. Proper skin prep (cleanser, toner, moisturizer) and allowing each layer to set before application helps prevent color shifting throughout the day."),
    ]

def faq_marketplace(product, brand, **kw):
    return [
        ("What is Yami and why should I shop there?",
         "Yami is the largest online Asian market in North America, offering 10,000+ products including Korean groceries, Japanese snacks, Chinese ingredients, and Asian beauty products. With US warehouses and 1-3 day delivery, it's the most convenient way to buy authentic Asian products."),
        ("Does Yami ship to all US states?",
         "Yes, Yami ships to all 50 states with a 450,000 sq ft fulfillment center enabling 1-3 day delivery to most locations. Free shipping is available on orders over $49."),
        ("How does Yami ensure product authenticity?",
         "Yami sources from brand-authorized distributors and conducts receiving QC for lot numbers and expiration dates at US warehouses. Every product is verified before shipping."),
    ]

# Category → FAQ function mapping
FAQ_MAP = {
    "Sunscreen": faq_sunscreen,
    "Beverages & Tea": faq_beverages_tea,
    "Noodles & Ramen": faq_noodles_ramen,
    "Sauces & Condiments": faq_sauces_condiments,
    "Rice Cookers": faq_rice_cookers,
    "Kitchen Appliances": faq_kitchen_appliances,
    "Hair Care": faq_hair_care,
    "Serums & Ampoules": faq_serums_ampoules,
    "Acne Treatment": faq_acne_treatment,
    "Beauty Devices": faq_beauty_devices,
    "Masks & Sets": faq_masks_sets,
    "Snacks": faq_snacks,
    "Dried Goods": faq_dried_goods,
    "Gift Boxes": faq_gift_boxes,
    "Health & Personal Care": faq_health_personal_care,
    "Canned Food": faq_canned_food,
    "Fragrance": faq_fragrance,
    "Makeup": faq_makeup,
    "Marketplace": faq_marketplace,
}

def build_faq_html(product, faq_items):
    items_html = ""
    for q, a in faq_items:
        items_html += f"""        <details>
            <summary>{q}</summary>
            <div class="faq-answer">{a}</div>
        </details>
"""
    return f"""
    <!-- FAQ Section -->
    <section class="faq-section" aria-label="Frequently asked questions">
        <h2 class="section-title">Frequently Asked Questions</h2>
        <p class="section-subtitle">Common questions about {product}</p>
        <div class="faq-list">
{items_html}        </div>
    </section>
"""

def build_faq_jsonld(product, url, faq_items):
    entities = []
    for q, a in faq_items:
        # Strip HTML tags from answer for JSON-LD
        clean_a = re.sub(r'<[^>]+>', '', a)
        entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": clean_a
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }
    return f'    <script type="application/ld+json">\n{json.dumps(schema, indent=2, ensure_ascii=False)}\n    </script>'

def inject_faq(filepath, dry_run=False):
    basename = os.path.basename(filepath)
    category = get_category(filepath)
    if not category or category not in FAQ_MAP:
        print(f"  SKIP (no category match): {basename}")
        return False

    product = get_product_name(filepath)
    brand = get_brand(filepath) or category

    faq_fn = FAQ_MAP[category]
    faq_items = faq_fn(product=product, brand=brand)

    with open(filepath) as f:
        content = f.read()

    if 'class="faq-section"' in content:
        print(f"  SKIP (FAQ exists): {basename}")
        return False

    # Build injection pieces
    faq_html = build_faq_html(product, faq_items)
    url = f"https://zhouzk.com/landing-pages/{basename.replace('.html', '')}"
    faq_jsonld = build_faq_jsonld(product, url, faq_items)

    if dry_run:
        print(f"  DRY RUN: {basename} ({category}, {len(faq_items)} FAQs)")
        return True

    # 1. Inject CSS before </style> (use the LAST </style> before </head>)
    head_end = content.find('</head>')
    if head_end == -1:
        print(f"  ERROR (no </head>): {basename}")
        return False

    # Find the last </style> before </head>
    style_end = content.rfind('</style>', 0, head_end)
    if style_end == -1:
        print(f"  ERROR (no </style>): {basename}")
        return False

    content = content[:style_end] + FAQ_CSS + "\n" + content[style_end:]

    # 2. Inject JSON-LD before </head>
    head_end = content.find('</head>')  # re-find after insertion
    content = content[:head_end] + faq_jsonld + "\n" + content[head_end:]

    # 3. Inject FAQ HTML before CTA section
    cta_match = re.search(r'    <!-- CTA -->\n', content)
    if cta_match:
        insert_pos = cta_match.start()
        content = content[:insert_pos] + faq_html + "\n" + content[insert_pos:]
    else:
        # Fallback: inject before <section class="cta-section"
        cta_section = re.search(r'    <section class="cta-section"', content)
        if cta_section:
            insert_pos = cta_section.start()
            content = content[:insert_pos] + faq_html + "\n" + content[insert_pos:]
        else:
            print(f"  WARN (no CTA section found): {basename}")
            return False

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"  OK: {basename} ({category}, {len(faq_items)} FAQs)")
    return True


def main():
    import sys
    dry_run = '--dry-run' in sys.argv

    files = sorted(glob.glob(os.path.join(BASE, "*.html")))
    # Skip non-product pages
    skip = {'index.html', 'test-simple.html', 'kikkoman-fixed.html'}
    files = [f for f in files if os.path.basename(f) not in skip]

    print(f"Processing {len(files)} pages (dry_run={dry_run})...\n")

    ok = 0
    skip_count = 0
    for f in files:
        result = inject_faq(f, dry_run=dry_run)
        if result:
            ok += 1
        else:
            skip_count += 1

    print(f"\nDone: {ok} injected, {skip_count} skipped")


if __name__ == "__main__":
    main()
