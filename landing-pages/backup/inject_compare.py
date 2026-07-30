#!/usr/bin/env python3
"""
Phase 4: Inject product comparison sections into landing pages.
Each product gets 2-3 comparisons with related products in the same category.
Creates internal links and covers "X vs Y" search intent.
"""

import os
import re
import glob
import hashlib

COMPARE_CSS = """
.compare-section {
  padding: 4rem 2rem;
  background: #f8f9fa;
}
.compare-section .section-title {
  text-align: center;
  font-size: 1.6rem;
  margin-bottom: 0.5rem;
}
.compare-section .section-subtitle {
  text-align: center;
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 2rem;
}
.compare-grid {
  max-width: 900px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.2rem;
}
.compare-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.compare-card:hover {
  border-color: var(--primary, #2563eb);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.compare-card .vs-badge {
  display: inline-block;
  background: var(--primary, #2563eb);
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  margin-bottom: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.compare-card h3 {
  font-size: 0.95rem;
  margin-bottom: 0.6rem;
  line-height: 1.3;
}
.compare-card p {
  font-size: 0.85rem;
  color: #555;
  line-height: 1.6;
  margin-bottom: 0.8rem;
}
.compare-card .compare-link {
  font-size: 0.85rem;
  color: var(--primary, #2563eb);
  text-decoration: none;
  font-weight: 500;
}
.compare-card .compare-link:hover {
  text-decoration: underline;
}
"""

HEADING_VARIANTS = [
    "How Does {name} Compare?",
    "{name} vs Similar Products",
    "See How {name} Stacks Up",
    "Compare Before You Buy",
    "{name} Comparison Guide",
    "Which One Is Right for You?",
    "Alternatives to Consider",
    "{name} vs the Rest",
    "Making the Right Choice",
    "How It Compares",
]

SUBTITLE_VARIANTS = [
    "See how it stacks up against similar products in its category.",
    "Not sure which one to pick? Here's a quick comparison.",
    "We break down the key differences so you can choose with confidence.",
    "A side-by-side look at similar options.",
    "Find out what sets it apart from the competition.",
]


def get_category(content):
    m = re.search(r'"@type":\s*"BreadcrumbList".*?"itemListElement":\s*\[(.*?)\]', content, re.DOTALL)
    if not m:
        return None
    names = re.findall(r'"name":\s*"([^"]+)"', m.group(1))
    return names[2] if len(names) >= 3 else None


def get_product_name(content):
    m = re.search(r'"@type":\s*"Product".*?"name":\s*"([^"]+)"', content, re.DOTALL)
    return m.group(1) if m else None


def get_slug(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]


# ── Category comparison functions ──────────────────────────────────

def compare_sunscreen(slug, name):
    short = name.split('|')[0].strip()[:50]
    if 'biore' in slug:
        if 'value-pack' in slug:
            return [
                ('biore-uv-aqua-rich-watery-essence-spf50-70g', 'Biore UV Aqua Rich (Single)',
                 f'The value pack gives you two 70g tubes at a lower per-unit cost. If you go through sunscreen fast — daily commute, beach trips — the bundle saves money. For first-time users, the single tube is enough to test the formula.'),
                ('beauty-of-joseon-relief-sun-rice-probiotics-spf50-50ml', 'Beauty of Joseon Relief Sun',
                 f'Biore uses a watery Japanese essence that absorbs instantly. Beauty of Joseon relies on rice probiotics for deeper hydration. Oily skin tends to prefer Biore; dry skin often leans toward Beauty of Joseon.'),
            ]
        return [
            ('beauty-of-joseon-relief-sun-rice-probiotics-spf50-50ml', 'Beauty of Joseon Relief Sun',
             f'Biore UV is a Japanese watery essence — ultra-lightweight, fast-absorbing, ideal under makeup. Beauty of Joseon uses rice probiotics for a more moisturizing, dewy finish. Choose Biore for oily skin or humidity; Beauty of Joseon for dry skin or cooler weather.'),
            ('skin1004-madagascar-centella-hyalu-cica-sun-serum-spf50-50ml', 'SKIN1004 Hyalu-Cica Sun Serum',
             f'SKIN1004 adds centella asiatica and hyaluronic acid — a serum-like sunscreen that calms sensitive, irritated skin. Biore focuses on pure UV protection with a lighter feel. If redness or sensitivity is a concern, SKIN1004 is the better pick.'),
        ]
    if 'beauty-of-joseon' in slug or 'matte-sun-stick' in slug:
        if 'stick' in slug:
            if 'value-pack' in slug:
                return [
                    ('beauty-of-joseon-matte-sun-stick-mugwort-camelia-spf50-0-63oz', 'Matte Sun Stick (Single)',
                     f'The value pack includes two sticks — one for home, one for your bag. Perfect for consistent reapplication. The single stick works if you only need sun protection occasionally.'),
                    ('biore-uv-aqua-rich-watery-essence-spf50-70g', 'Biore UV Aqua Rich',
                     f'The stick format is mess-free for on-the-go reapplication over makeup. Biore\'s watery essence is better for initial full-face application in the morning. Many users keep both: Biore for AM, stick for touch-ups.'),
                ]
            return [
                ('biore-uv-aqua-rich-watery-essence-spf50-70g', 'Biore UV Aqua Rich',
                 f'The stick format is perfect for reapplication on the go — no messy hands, works over makeup. Biore\'s watery essence is better for the initial morning application. They complement each other well.'),
                ('round-lab-birch-juice-moisturizing-sunscreen-spf50-50ml', 'Round Lab Birch Juice Sunscreen',
                 f'Round Lab offers birch juice hydration in a traditional lotion format — great for all-day moisture. The stick prioritizes convenience and matte finish. Choose Round Lab for dry skin hydration, or the stick for portability.'),
            ]
        if 'value-pack' in slug:
            return [
                ('beauty-of-joseon-relief-sun-rice-probiotics-spf50-50ml', 'Relief Sun (Single)',
                 f'The value pack includes two 50ml bottles at a better per-unit price. If this is your daily sunscreen, the bundle lasts longer and saves money. First-time users may prefer the single bottle.'),
                ('biore-uv-aqua-rich-watery-essence-spf50-70g', 'Biore UV Aqua Rich',
                 f'Beauty of Joseon uses rice probiotics for a moisturizing, slightly dewy finish. Biore offers a lighter, more matte Japanese watery essence. Dry skin favors Beauty of Joseon; oily skin often prefers Biore.'),
            ]
        return [
            ('biore-uv-aqua-rich-watery-essence-spf50-70g', 'Biore UV Aqua Rich',
             f'Beauty of Joseon uses rice probiotics and traditional Korean ingredients for a moisturizing, glowy finish. Biore delivers a lighter, fast-absorbing Japanese formula. Dry skin tends to prefer Beauty of Joseon; oily skin often chooses Biore.'),
            ('skin1004-madagascar-centella-hyalu-cica-sun-serum-spf50-50ml', 'SKIN1004 Hyalu-Cica Sun Serum',
             f'SKIN1004 combines sun protection with centella asiatica for calming sensitive skin. Beauty of Joseon focuses on rice-based hydration and a natural glow. Sensitive or acne-prone skin may benefit more from SKIN1004\'s soothing formula.'),
        ]
    if 'nivea' in slug:
        return [
            ('biore-uv-aqua-rich-watery-essence-spf50-70g', 'Biore UV Aqua Rich',
             f'NIVEA offers a generous 140g water gel — great value for body and face. Biore\'s 70g Japanese formula is lighter and more cosmetically elegant for facial use. NIVEA is ideal if you want one product for face and body.'),
            ('beauty-of-joseon-relief-sun-rice-probiotics-spf50-50ml', 'Beauty of Joseon Relief Sun',
             f'NIVEA is a Western drugstore staple with a simple water gel formula. Beauty of Joseon brings Korean skincare innovation with rice probiotics and a more refined skin-feel. For skincare benefits beyond UV protection, Beauty of Joseon edges ahead.'),
        ]
    if 'round-lab' in slug:
        if 'sun-cream' in slug:
            return [
                ('round-lab-birch-juice-moisturizing-sunscreen-spf50-50ml', 'Round Lab Sunscreen (Lotion)',
                 f'The Sun Cream version has a richer, more emollient texture — better for dry skin or winter months. The lotion version is lighter and more suitable for oily skin or summer. Both share the same birch juice hydration base.'),
                ('beauty-of-joseon-relief-sun-rice-probiotics-spf50-50ml', 'Beauty of Joseon Relief Sun',
                 f'Both are hydrating Korean sunscreens, but Round Lab focuses on birch juice soothing while Beauty of Joseon uses rice probiotics for glow. Round Lab is better for sensitive, irritated skin; Beauty of Joseon for dull, dry skin.'),
            ]
        return [
            ('round-lab-birch-juice-moisturizing-sun-cream-spf50', 'Round Lab Sun Cream',
             f'The lotion version is lighter and absorbs faster — ideal for oily or combination skin. The Sun Cream is richer and more emollient, better for dry skin. Both offer the same birch juice hydration and SPF50 protection.'),
            ('biore-uv-aqua-rich-watery-essence-spf50-70g', 'Biore UV Aqua Rich',
             f'Round Lab brings birch juice hydration and a soothing, moisturizing feel. Biore is lighter and more matte — a Japanese watery essence. Choose Round Lab for hydration and skin calming; Biore for oil control and lightweight feel.'),
        ]
    if 'skin1004' in slug:
        if 'value-pack' in slug:
            return [
                ('skin1004-madagascar-centella-hyalu-cica-sun-serum-spf50-50ml', 'SKIN1004 Sun Serum (Single)',
                 f'The value pack gives you two 50ml bottles — ideal if this is your daily sunscreen. The single bottle is enough for first-time users to test the centella formula.'),
                ('biore-uv-aqua-rich-watery-essence-spf50-70g', 'Biore UV Aqua Rich',
                 f'SKIN1004 uses centella asiatica for calming and hyaluronic acid for hydration — a serum-sunscreen hybrid. Biore focuses on pure UV protection with a lighter, more matte finish. Sensitive skin benefits more from SKIN1004.'),
            ]
        return [
            ('biore-uv-aqua-rich-watery-essence-spf50-70g', 'Biore UV Aqua Rich',
             f'SKIN1004 combines sun protection with centella asiatica and hyaluronic acid — ideal for sensitive, irritated skin. Biore is a simpler, lighter Japanese formula focused on UV protection. If you need calming benefits alongside SPF, SKIN1004 wins.'),
            ('beauty-of-joseon-relief-sun-rice-probiotics-spf50-50ml', 'Beauty of Joseon Relief Sun',
             f'SKIN1004 focuses on centella-based soothing and hydration. Beauty of Joseon uses rice probiotics for a glowy, moisturizing finish. Both are excellent for dry skin — SKIN1004 for sensitivity, Beauty of Joseon for radiance.'),
        ]
    return []


def compare_rice_cookers(slug, name):
    if 'np-hcc10' in slug:
        return [
            ('zojirushi-induction-heating-rice-cooker-np-hcc18', 'Zojirushi NP-HCC18 (10 Cup)',
             f'Same premium IH heating technology, but the 10-cup model is better for families of 4+. The 5.5-cup is ideal for couples or small households. If you cook rice frequently and have the counter space, the larger model offers more flexibility.'),
            ('zojirushi-micom-rice-cooker-ns-tsc10', 'Zojirushi NS-TSC10 (Micom)',
             f'The NP uses induction heating for more even, precise cooking — noticeably better texture. The NS uses conventional heating with Micom logic at a lower price. If rice quality is your top priority, the NP is worth the upgrade.'),
        ]
    if 'np-hcc18' in slug:
        return [
            ('zojirushi-induction-heating-rice-cooker-np-hcc10', 'Zojirushi NP-HCC10 (5.5 Cup)',
             f'Same IH technology, but the 5.5-cup is more compact for smaller kitchens. The 10-cup is better for families or meal prep. Choose based on your household size.'),
            ('tatung-tac-10g', 'Tatung 10-Cup Rice Cooker',
             f'Zojirushi NP uses premium IH heating with multiple settings — significantly more expensive but produces superior rice. Tatung uses simple one-switch operation at a fraction of the price. Choose Tatung for simplicity and value; Zojirushi for rice perfection.'),
        ]
    if 'ns-tsc10' in slug:
        return [
            ('zojirushi-induction-heating-rice-cooker-np-hcc10', 'Zojirushi NP-HCC10 (IH)',
             f'The NP uses induction heating for more even heat distribution — rice texture is noticeably better. The NS uses conventional heating with Micom logic at a lower price point. If budget allows, the NP is the upgrade worth considering.'),
            ('tatung-tac-06in', 'Tatung 6-Cup Rice Cooker',
             f'Zojirushi NS offers more cooking modes (white, brown, sushi, porridge) with automated keep-warm. Tatung is a simple, durable one-switch cooker. Zojirushi is better for rice enthusiasts; Tatung for no-fuss daily cooking.'),
        ]
    if 'ns-tsc18' in slug:
        return [
            ('zojirushi-micom-rice-cooker-ns-tsc10', 'Zojirushi NS-TSC10 (5.5 Cup)',
             f'Identical technology and features — the only difference is capacity. The 5.5-cup is more compact; the 10-cup suits larger families. Choose based on how much rice you typically cook.'),
            ('zojirushi-induction-heating-rice-cooker-np-hcc18', 'Zojirushi NP-HCC18 (IH)',
             f'The NP upgrades to induction heating for superior rice texture and more precise temperature control. The NS is more affordable with still-excellent Micom cooking. The NP is the enthusiast\'s choice.'),
        ]
    if 'tac-6g' in slug:
        return [
            ('zojirushi-micom-rice-cooker-ns-tsc10', 'Zojirushi NS-TSC10',
             f'Tatung TAC-6G is a simple, affordable multi-function cooker — reliable and durable. Zojirushi offers automated multi-mode cooking with fuzzy logic and keep-warm. Choose Tatung for budget and simplicity; Zojirushi for features and rice variety.'),
            ('tatung-tac-06kn-ul', 'Tatung TAC-06KN (Stainless)',
             f'Both are 6-cup Tatung cookers. The TAC-6G is a multi-functional model; the TAC-06KN features a stainless steel exterior. Choose based on your kitchen aesthetics and feature needs.'),
        ]
    if 'tac-06in' in slug:
        return [
            ('zojirushi-micom-rice-cooker-ns-tsc10', 'Zojirushi NS-TSC10',
             f'Tatung is a simple, affordable one-switch cooker — reliable and durable. Zojirushi offers automated multi-mode cooking with keep-warm. Choose Tatung for budget and simplicity; Zojirushi for features and rice variety.'),
            ('tatung-tac-06kn-ul', 'Tatung TAC-06KN (Stainless)',
             f'Both are 6-cup Tatung cookers. The TAC-06IN features a vanilla cream finish; the TAC-06KN has a stainless steel exterior. Internally they\'re very similar — choose based on your kitchen aesthetics.'),
        ]
    if 'tac-06kn' in slug:
        return [
            ('tatung-tac-06in', 'Tatung TAC-06IN (Vanilla Cream)',
             f'Both are 6-cup Tatung cookers with the same core functionality. The TAC-06IN has a vanilla cream finish; the TAC-06KN features stainless steel. Choose based on your kitchen style.'),
            ('zojirushi-micom-rice-cooker-ns-tsc10', 'Zojirushi NS-TSC10',
             f'Tatung offers simple, reliable one-switch cooking at a budget price. Zojirushi adds automated multi-mode settings, fuzzy logic, and keep-warm. Upgrade to Zojirushi if you cook different rice types regularly.'),
        ]
    if 'tac-10g' in slug:
        return [
            ('tatung-tac-11kn-ul', 'Tatung TAC-11KN (11 Cup)',
             f'Both are large-capacity Tatung cookers. The TAC-11KN is slightly larger (11 vs 10 cups) with a stainless steel finish. The TAC-10G has a classic white design. Choose based on size needs and aesthetics.'),
            ('zojirushi-micom-rice-cooker-ns-tsc18', 'Zojirushi NS-TSC18 (10 Cup)',
             f'Zojirushi offers automated multi-mode cooking with fuzzy logic at a premium price. Tatung delivers simple, durable one-switch operation. Zojirushi for versatility; Tatung for straightforward value.'),
        ]
    if 'tac-11kn' in slug:
        return [
            ('tatung-tac-10g', 'Tatung TAC-10G (10 Cup)',
             f'Both are large Tatung cookers. The TAC-11KN holds 11 cups with stainless steel; the TAC-10G holds 10 cups in white. If you need the extra cup or prefer stainless steel, go with the TAC-11KN.'),
            ('zojirushi-induction-heating-rice-cooker-np-hcc18', 'Zojirushi NP-HCC18 (IH)',
             f'Zojirushi NP uses premium induction heating for superior rice texture — significantly more expensive. Tatung is simple and affordable. The choice depends on how much you value rice quality vs budget.'),
        ]
    if 'pearl-white' in slug or 'tac-10g' in slug.lower():
        return [
            ('tatung-tac-11kn-ul', 'Tatung TAC-11KN (11 Cup)',
             f'Both are large Tatung cookers. The TAC-11KN is slightly larger with stainless steel; this model offers a pearl white finish. Choose based on capacity needs and kitchen aesthetics.'),
            ('zojirushi-micom-rice-cooker-ns-tsc10', 'Zojirushi NS-TSC10 (5.5 Cup)',
             f'Tatung is a simple, budget-friendly one-switch cooker. Zojirushi adds automated multi-mode cooking and fuzzy logic. Upgrade to Zojirushi for more rice varieties and precise cooking control.'),
        ]
    return []


def compare_noodles_ramen(slug, name):
    if 'ichiran' in slug:
        return [
            ('marutai-kumamoto-black-garlic-oil-tonkotsu-ramen', 'Marutai Kumamoto Ramen',
             f'Both are Japanese tonkotsu ramen, but Ichiran replicates the famous Fukuoka chain experience with rich, creamy broth. Marutai\'s Kumamoto style adds black garlic oil for a distinctive aromatic twist. Ichiran for authenticity; Marutai for variety.'),
            ('samyang-buldak-quattro-cheese-hot-chicken-flavor-ramen-5-packs', 'Samyang Buldak Quattro Cheese',
             f'Completely different flavor profiles — Ichiran is a rich, savory Japanese tonkotsu; Samyang is an intensely spicy Korean fire noodle. Ichiran for comfort food; Samyang for a spicy challenge.'),
        ]
    if 'marutai' in slug:
        return [
            ('ichiran-ramen-classic-hakata-thin-noodles-5-packs', 'Ichiran Classic Hakata Ramen',
             f'Marutai\'s Kumamoto style features black garlic oil for a unique aromatic depth. Ichiran replicates the famous chain\'s classic tonkotsu — cleaner, more traditional. Marutai for garlic lovers; Ichiran for classic tonkotsu purists.'),
            ('samyang-buldak-carbonara-hot-chicken-flavor-ramen-5-packs', 'Samyang Buldak Carbonara',
             f'Marutai is a Japanese tonkotsu with savory, garlicky depth. Samyang Carbonara is Korean — spicy, creamy, and addictive. Marutai for a comforting bowl; Samyang for a spicy, trendy flavor experience.'),
        ]
    if 'samyang' in slug:
        if 'carbonara' in slug:
            return [
                ('samyang-buldak-quattro-cheese-hot-chicken-flavor-ramen-5-packs', 'Samyang Quattro Cheese',
                 f'Both are spicy Korean Buldak noodles. Carbonara adds a creamy, pasta-inspired twist with mild heat. Quattro Cheese is cheesier and slightly less spicy. Carbonara for creaminess; Quattro Cheese for maximum cheese flavor.'),
                ('ichiran-ramen-classic-hakata-thin-noodles-5-packs', 'Ichiran Classic Hakata Ramen',
                 f'Samyang is intensely spicy Korean fire noodles — a flavor challenge. Ichiran is a rich but mild Japanese tonkotsu — pure comfort. Samyang for thrill-seekers; Ichiran for a relaxing bowl.'),
            ]
        return [
            ('samyang-buldak-carbonara-hot-chicken-flavor-ramen-5-packs', 'Samyang Carbonara',
             f'Quattro Cheese is cheesier with a milder spice level. Carbonara has a creamier, pasta-inspired sauce with a bit more kick. Both are addictive — Quattro Cheese for cheese lovers, Carbonara for creamy-spicy balance.'),
            ('ottogi-cheesy-ramen-cheddar-flavor-4-packs', 'Ottogi Cheesy Ramen',
             f'Samyang Buldak is known for intense heat — even the cheese version has a real kick. Ottogi Cheesy Ramen is much milder with a focus on cheddar flavor. Choose Samyang for spice; Ottogi for a gentle, cheesy comfort bowl.'),
        ]
    if 'ottogi' in slug:
        if 'bowl' in slug:
            return [
                ('ottogi-cheesy-ramen-cheddar-flavor-4-packs', 'Ottogi Cheesy Ramen (Pack)',
                 f'The bowl version is designed for quick, convenient single servings — just add hot water. The pack version requires stovetop cooking but offers more control over texture. Bowl for convenience; pack for cooking flexibility.'),
                ('samyang-buldak-quattro-cheese-hot-chicken-flavor-ramen-5-packs', 'Samyang Quattro Cheese',
                 f'Ottogi is mild and cheesy — a gentle, comforting Korean ramen. Samyang Buldak is significantly spicier with a bolder flavor profile. Ottogi for easy-going cheese ramen; Samyang for those who like heat.'),
            ]
        return [
            ('ottogi-cheesy-ramen-cheddar-mascarpone-bowl-6-packs', 'Ottogi Cheesy Ramen Bowl',
             f'The pack version requires stovetop cooking but lets you customize texture and toppings. The bowl version is instant — just add hot water. Pack for cooking; bowl for speed.'),
            ('samyang-buldak-quattro-cheese-hot-chicken-flavor-ramen-5-packs', 'Samyang Quattro Cheese',
             f'Ottogi is mild and focused on cheddar cheese flavor — very approachable. Samyang Buldak packs real heat even in its cheese variant. Choose Ottogi for gentle comfort; Samyang for a spicy kick.'),
        ]
    if 'cunlvjia' in slug:
        return [
            ('galan-lang-lanzhou-beef-flavor-noodles-5-packs', 'Ga Lan Lang Lanzhou Ramen',
             f'Cunlvjia offers honey-flavored cold noodles — a refreshing Chinese summer dish. Ga Lan Lang brings hot Lanzhou beef ramen — a warming, savory experience. Cold noodles for summer; hot ramen for comfort.'),
            ('ichiran-ramen-classic-hakata-thin-noodles-5-packs', 'Ichiran Classic Hakata Ramen',
             f'Cunlvjia is a Chinese cold noodle dish — sweet, tangy, and refreshing. Ichiran is a Japanese hot tonkotsu ramen — rich and savory. Completely different experiences — cold vs hot, Chinese vs Japanese.'),
        ]
    if 'galan-lang' in slug:
        if '5-packs' in slug:
            return [
                ('galan-lang-lanzhou-ramen-beef-flavor-noodles-2-servings', 'Ga Lan Lang (2 Servings)',
                 f'The 5-pack gives you more bowls at a better per-unit price — great for stocking up. The 2-serving pack is ideal for trying it first or if you have limited storage.'),
                ('ichiran-ramen-classic-hakata-thin-noodles-5-packs', 'Ichiran Classic Hakata Ramen',
                 f'Ga Lan Lang replicates Lanzhou beef noodle soup — a clear, aromatic Chinese broth. Ichiran is a creamy Japanese tonkotsu. Lanzhou for light, aromatic broth; Ichiran for rich, creamy depth.'),
            ]
        return [
            ('galan-lang-lanzhou-beef-flavor-noodles-5-packs', 'Ga Lan Lang (5-Pack)',
             f'The 2-serving pack is great for a one-time trial. If you love it, the 5-pack offers better value. Both have the same authentic Lanzhou beef flavor.'),
            ('marutai-kumamoto-black-garlic-oil-tonkotsu-ramen', 'Marutai Kumamoto Ramen',
             f'Ga Lan Lang brings Chinese Lanzhou style — clear, aromatic beef broth with hand-pulled style noodles. Marutai is Japanese tonkotsu — rich, creamy pork bone broth with black garlic oil. Chinese clarity vs Japanese richness.'),
        ]
    return []


def compare_serums_ampoules(slug, name):
    if 'sulwhasoo' in slug:
        if 'first-care' in slug:
            return [
                ('sulwasoo-concentrated-ginseng-renewing-serum-20g', 'Sulwhasoo Ginseng Serum',
                 f'First Care Serum is a pre-serum booster that enhances absorption of subsequent products. The Ginseng Serum targets anti-aging directly with concentrated ginseng. Use First Care as step one; Ginseng Serum as your treatment step.'),
                ('rejuran-healer-dual-effect-ampoule-1oz', 'REJURAN Dual Effect Ampoule',
                 f'Sulwhasoo uses traditional Korean ginseng in a luxurious, fragrant formula. REJURAN relies on salmon DNA (PDRN) for cellular repair — more clinical, less fragrant. Sulwhasoo for sensory luxury; REJURAN for science-backed repair.'),
            ]
        if 'concentrated-ginseng' in slug:
            return [
                ('sulwhasoo-first-care-activating-serum-90ml', 'Sulwhasoo First Care Serum',
                 f'The Ginseng Serum is a targeted anti-aging treatment. First Care Serum is a pre-serum booster that preps skin for better product absorption. They work together — First Care first, then Ginseng Serum.'),
                ('rejuran-healer-dual-effect-ampoule-1oz', 'REJURAN Dual Effect Ampoule',
                 f'Sulwhasoo Ginseng focuses on anti-aging with traditional Korean herbal ingredients and a luxurious feel. REJURAN uses salmon DNA (PDRN) for cellular-level skin repair. Sulwhasoo for luxury experience; REJURAN for clinical repair.'),
            ]
        if 'ultimate-s-cream' in slug:
            return [
                ('sulwhasoo-first-care-activating-serum-90ml', 'Sulwhasoo First Care Serum',
                 f'The Ultimate S Cream is a rich moisturizer — the final step in your routine. First Care Serum is a lightweight pre-serum applied first to boost absorption. They complement each other in the Sulwhasoo routine.'),
                ('beauty-of-joseon-revive-eye-serum-ginseng-retinal', 'Beauty of Joseon Eye Serum',
                 f'Sulwhasoo Ultimate S Cream is a full-face luxury moisturizer with ginseng and anti-aging benefits. Beauty of Joseon Eye Serum targets the delicate eye area specifically with retinal. Full-face luxury vs targeted eye treatment.'),
            ]
        if 'eye-cream' in slug:
            return [
                ('sulwhasoo-first-care-activating-serum-90ml', 'Sulwhasoo First Care Serum',
                 f'The Eye Cream targets the delicate eye area with concentrated anti-aging ingredients. First Care Serum is a face-wide pre-serum booster. Use together for a complete Sulwhasoo routine.'),
                ('beauty-of-joseon-revive-eye-serum-ginseng-retinal', 'Beauty of Joseon Eye Serum',
                 f'Both target the eye area with ginseng. Sulwhasoo is a richer cream format from a luxury line. Beauty of Joseon uses retinal for added cell-turnover benefits at a lower price. Sulwhasoo for luxury; Beauty of Joseon for value + retinal.'),
            ]
        if 'water' in slug or 'enriched-water' in slug:
            return [
                ('sulwhasoo-first-care-activating-serum-90ml', 'Sulwhasoo First Care Serum',
                 f'Enriched Water is a hydrating toner step — lightweight, preps skin for serums. First Care Serum is a pre-serum booster that enhances absorption of everything after it. They layer well: First Care → Enriched Water → treatment serums.'),
                ('rejuran-healer-dual-effect-ampoule-1oz', 'REJURAN Dual Effect Ampoule',
                 f'Enriched Water focuses on hydration as a toner step. REJURAN Ampoule is a treatment product for skin repair and anti-aging. Hydrate first with Enriched Water, then treat with REJURAN.'),
            ]
        if 'set' in slug or 'value-pack' in slug:
            return [
                ('sulwhasoo-first-care-activating-serum-90ml', 'Sulwhasoo First Care Serum (Full Size)',
                 f'This set gives you travel-sized products to try the full Sulwhasoo routine. If you find products you love, upgrade to full sizes like the First Care Serum for the best value.'),
                ('rejuran-healer-dual-effect-ampoule-1oz', 'REJURAN Dual Effect Ampoule',
                 f'Sulwhasoo sets offer a luxurious, ginseng-based Korean routine. REJURAN focuses on a single high-performance ingredient (salmon DNA). Sulwhasoo for a complete ritual; REJURAN for targeted treatment.'),
            ]
        return [
            ('sulwhasoo-first-care-activating-serum-90ml', 'Sulwhasoo First Care Serum',
             f'This Sulwhasoo product targets specific skin concerns. The First Care Serum is the brand\'s hero product — a pre-serum that boosts absorption of your entire routine. It pairs well with any Sulwhasoo treatment product.'),
            ('rejuran-healer-dual-effect-ampoule-1oz', 'REJURAN Dual Effect Ampoule',
             f'Sulwhasoo uses traditional ginseng in a luxurious, sensorial formula. REJURAN relies on salmon DNA (PDRN) for clinical-level skin repair. Sulwhasoo for the experience; REJURAN for the science.'),
        ]
    if 'beauty-of-joseon' in slug:
        return [
            ('sulwhasoo-concentrated-ginseng-renewing-serum-20g', 'Sulwhasoo Ginseng Serum',
             f'Beauty of Joseon offers traditional Korean ingredients at an accessible price point. Sulwhasoo is a luxury brand with premium pricing and a more refined sensory experience. Both use ginseng — Beauty of Joseon for value, Sulwhasoo for luxury.'),
            ('rejuran-healer-dual-effect-ampoule-1oz', 'REJURAN Dual Effect Ampoule',
             f'Beauty of Joseon uses ginseng and retinal for anti-aging with a focus on traditional ingredients. REJURAN uses salmon DNA (PDRN) for cellular repair — more clinical and fragrance-free. Beauty of Joseon for traditional skincare; REJURAN for science-forward.'),
        ]
    if 'rejuran' in slug:
        if 'value-pack' in slug:
            return [
                ('rejuran-healer-dual-effect-ampoule-1oz', 'REJURAN Ampoule (Single)',
                 f'The value pack includes both the Dual Effect and Turnover ampoules for a complete REJURAN routine. The single ampoule is great if you want to try one before committing to the full system.'),
                ('sulwhasoo-concentrated-ginseng-renewing-serum-20g', 'Sulwhasoo Ginseng Serum',
                 f'REJURAN focuses on salmon DNA (PDRN) for cellular repair — clinical and fragrance-free. Sulwhasoo uses ginseng in a luxurious, fragrant formula. REJURAN for science; Sulwhasoo for sensory luxury.'),
            ]
        return [
            ('sulwhasoo-concentrated-ginseng-renewing-serum-20g', 'Sulwhasoo Ginseng Serum',
             f'REJURAN uses salmon DNA (PDRN) for cellular-level skin repair — clinical, fragrance-free, science-forward. Sulwhasoo uses ginseng in a luxurious, sensorial formula. REJURAN for results-focused skincare; Sulwhasoo for the experience.'),
            ('beauty-of-joseon-revive-eye-serum-ginseng-retinal', 'Beauty of Joseon Eye Serum',
             f'REJURAN is a full-face ampoule focused on skin repair and regeneration. Beauty of Joseon Eye Serum targets the delicate eye area with ginseng and retinal. Full-face treatment vs targeted eye care.'),
        ]
    return []


def compare_hair_care(slug, name):
    if 'fino' in slug.lower():
        if 'value-pack' in slug or ('shampoo' in slug and 'conditioner' in slug and 'mask' in slug):
            return [
                ('fino-premium-touch-hair-mask-230g', 'Fino Hair Mask (Single)',
                 f'The value pack includes shampoo, conditioner, mask, and hair oil — a complete Fino routine. The single mask lets you add the treatment to your existing shampoo/conditioner. Full set for maximum repair; single mask for a targeted boost.'),
                ('tsubaki-premium-repair-hair-mask-180g', 'Tsubaki Premium Repair Mask',
                 f'Both are Shiseido hair care lines. Fino focuses on deep repair with royal jelly and collagen. Tsubaki uses camellia oil for shine and moisture. Fino for damaged hair repair; Tsubaki for shine and maintenance.'),
            ]
        if 'shampoo' in slug and 'conditioner' in slug:
            return [
                ('fino-premium-touch-hair-mask-230g', 'Fino Hair Mask',
                 f'This shampoo + conditioner set handles daily cleansing. Add the Fino Hair Mask weekly for deep repair treatment. The set maintains; the mask restores.'),
                ('tsubaki-premium-repair-hair-mask-180g', 'Tsubaki Premium Repair Mask',
                 f'Fino uses royal jelly and collagen for deep repair at a budget-friendly price. Tsubaki uses premium camellia oil for shine and is positioned as a more luxurious option. Fino for repair on a budget; Tsubaki for shine and luxury.'),
            ]
        if 'repair-shampoo' in slug or 'shampoo' in slug:
            return [
                ('fino-premium-touch-hair-mask-230g', 'Fino Hair Mask',
                 f'Fino shampoo cleanses and preps hair for treatment. The hair mask provides intensive weekly repair. Use shampoo daily; mask once or twice a week for best results.'),
                ('tsubaki-golden-hair-mask-180g', 'Tsubaki Golden Hair Mask',
                 f'Fino shampoo focuses on repair with royal jelly and collagen. Tsubaki Golden Mask uses camellia oil for intense shine. Fino for damage repair; Tsubaki for luxurious shine.'),
            ]
        return [
            ('fino-repair-shampoo-conditioner-550ml', 'Fino Shampoo + Conditioner Set',
             f'The hair mask is an intensive weekly treatment. The shampoo + conditioner set handles daily cleansing and maintenance. Use both together for the complete Fino repair system.'),
            ('tsubaki-premium-repair-hair-mask-180g', 'Tsubaki Premium Repair Mask',
             f'Fino uses royal jelly and collagen for deep repair at an accessible price. Tsubaki uses camellia oil for shine and is positioned as a premium Japanese treatment. Fino for repair value; Tsubaki for luxury shine.'),
        ]
    if 'tsubaki' in slug.lower():
        if 'golden' in slug:
            return [
                ('fino-premium-touch-hair-mask-230g', 'Fino Premium Hair Mask',
                 f'Tsubaki Golden Mask uses camellia oil for brilliant shine and smoothness. Fino uses royal jelly and collagen for deep structural repair. Tsubaki for shine and finish; Fino for damage repair.'),
                ('tsubaki-premium-repair-hair-mask-180g', 'Tsubaki Premium Repair Mask',
                 f'The Golden Mask focuses on shine and smoothness with camellia oil. The Premium Repair Mask targets damage with additional conditioning agents. Golden for cosmetic shine; Premium Repair for structural fix.'),
            ]
        return [
            ('fino-premium-touch-hair-mask-230g', 'Fino Premium Hair Mask',
             f'Tsubaki uses camellia oil for shine and smoothness — a luxurious Japanese ingredient. Fino uses royal jelly and collagen for deep repair at a lower price. Tsubaki for shine and luxury; Fino for repair value.'),
            ('tsubaki-golden-hair-mask-180g', 'Tsubaki Golden Hair Mask',
             f'The Premium Repair Mask focuses on damage repair with enhanced conditioning. The Golden Mask emphasizes shine and smoothness with camellia oil. Repair for damaged hair; Golden for maintenance and glow.'),
        ]
    return []


def compare_beverages_tea(slug, name):
    if 'chagee' in slug:
        return [
            ('marukyu-koyamaen-matcha-powder-1-41oz', 'Marukyu Koyamaen Matcha',
             f'CHAGEE BOYA is a premium Chinese jasmine green tea — floral, aromatic, and delicate. Marukyu Koyamaen is Japanese matcha — earthy, umami-rich, and bold. Jasmine for light, floral moments; matcha for deep, energizing ones.'),
            ('jayone-honey-passion-fruit-tea-35oz', 'Jayone Honey Passion Fruit Tea',
             f'BOYA is a pure jasmine green tea — subtle, refined, no added sweetness. Jayone is a concentrated fruit tea jam — sweet, tangy, and versatile. BOYA for traditional tea purity; Jayone for fruity indulgence.'),
        ]
    if 'marukyu-koyamaen' in slug or 'uji-matcha' in slug or 'qinglan' in slug:
        if 'wakatake' in slug or 'uji-matcha' in slug or 'qinglan' in slug:
            return [
                ('marukyu-koyamaen-matcha-powder-1-41oz', 'Marukyu Koyamaen Premium (1.41oz)',
                 f'Wakatake is a culinary-grade matcha — ideal for lattes, baking, and cooking. The Premium (1.41oz) is closer to ceremonial grade — best for traditional usucha. Wakatake for versatility; Premium for drinking pure.'),
                ('chagee-boya-jasmine-tea', 'CHAGEE BOYA Jasmine Tea',
                 f'Marukyu Koyamaen is Japanese matcha — earthy, umami, and energizing. CHAGEE BOYA is Chinese jasmine green tea — floral, light, and calming. Matcha for a bold morning boost; jasmine for a gentle afternoon moment.'),
            ]
        return [
            ('marukyu-koyamaen-matcha-powder-wakatake-3-53oz', 'Marukyu Koyamaen Wakatake (3.53oz)',
             f'The Premium (1.41oz) is higher grade — closer to ceremonial, best for traditional tea drinking. Wakatake is culinary grade — more affordable, great for lattes and baking. Premium for sipping; Wakatake for cooking and mixing.'),
            ('chagee-boya-jasmine-tea', 'CHAGEE BOYA Jasmine Tea',
             f'This is Japanese matcha — bold, earthy, and packed with umami. CHAGEE BOYA is Chinese jasmine green tea — delicate, floral, and soothing. Matcha for energy and depth; jasmine for lightness and calm.'),
        ]
    if 'binggrae' in slug:
        return [
            ('mizuho-ramune-drink-7-flavors-combo-pack', 'Mizuho Ramune 7 Flavors',
             f'Binggrae banana milk is a creamy, nostalgic Korean classic — rich and sweet. Ramune is a Japanese fizzy soda — light, refreshing, and fun to drink (the marble bottle!). Creamy indulgence vs fizzy refreshment.'),
            ('jayone-honey-passion-fruit-tea-35oz', 'Jayone Honey Passion Fruit Tea',
             f'Binggrae is a ready-to-drink banana milk — creamy and sweet. Jayone is a concentrated fruit tea jam you mix with water — customizable sweetness. Binggrae for instant gratification; Jayone for versatile drinks.'),
        ]
    if 'mizuho' in slug:
        return [
            ('binggrae-banana-flavored-milk-drink-6-packs', 'Binggrae Banana Milk',
             f'Ramune is a Japanese fizzy soda — light, carbonated, and refreshing. Binggrae banana milk is creamy, sweet, and indulgent. Ramune for fizzy refreshment; Binggrae for creamy comfort.'),
            ('otsuka-oronamin-vitamin-c-soda-6-packs', 'Oronamin Vitamin C Soda',
             f'Both are Japanese fizzy drinks but with different profiles. Ramune is a classic sweet soda with a fun marble bottle. Oronamin is a vitamin C fortified drink with a medicinal, citrusy taste. Ramune for fun; Oronamin for a vitamin boost.'),
        ]
    if 'otsuka' in slug:
        return [
            ('mizuho-ramune-drink-7-flavors-combo-pack', 'Mizuho Ramune 7 Flavors',
             f'Oronamin is a vitamin C fortified drink with a distinctive citrusy, slightly medicinal taste. Ramune is a classic sweet soda — purely refreshing. Oronamin for a vitamin boost; Ramune for pure fizzy fun.'),
            ('binggrae-banana-flavored-milk-drink-6-packs', 'Binggrae Banana Milk',
             f'Oronamin is a Japanese carbonated vitamin drink — fizzy with a citrusy kick. Binggrae banana milk is a Korean creamy, sweet beverage. Vitamin fizz vs creamy indulgence — very different experiences.'),
        ]
    if 'jayone' in slug:
        return [
            ('chagee-boya-jasmine-tea', 'CHAGEE BOYA Jasmine Tea',
             f'Jayone is a concentrated fruit tea jam — sweet, tangy, and mixable with water or soda. CHAGEE BOYA is a premium jasmine green tea — pure, floral, no added sugar. Jayone for sweet fruit drinks; BOYA for traditional tea.'),
            ('marukyu-koyamaen-matcha-powder-1-41oz', 'Marukyu Koyamaen Matcha',
             f'Jayone is a Korean fruit tea jam — sweet, versatile, and fruity. Marukyu Koyamaen is Japanese ceremonial matcha — earthy, umami, and pure. Jayone for sweet fruit drinks; matcha for traditional tea ceremony.'),
        ]
    if 'wanlaoji' in slug or 'wanglaoji' in slug:
        return [
            ('binggrae-banana-flavored-milk-drink-6-packs', 'Binggrae Banana Milk',
             f'Wanglaoji is a traditional Chinese herbal tea — slightly bitter, cooling, and believed to reduce internal heat. Binggrae banana milk is a sweet, creamy Korean treat. Herbal wellness vs creamy indulgence.'),
            ('mizuho-ramune-drink-7-flavors-combo-pack', 'Mizuho Ramune',
             f'Wanglaoji is a Chinese herbal tea with a distinctive herbal, slightly bitter taste. Ramune is a Japanese sweet soda — fun and refreshing. Wanglaoji for traditional wellness; Ramune for fizzy enjoyment.'),
        ]
    if 'fanta' in slug:
        return [
            ('mizuho-ramune-drink-7-flavors-combo-pack', 'Mizuho Ramune 7 Flavors',
             f'Fanta melon is a Korean version of the classic soda — sweet, fizzy, with a distinct melon flavor. Ramune offers 7 different flavors in fun marble bottles. Fanta for a familiar soda taste; Ramune for Japanese variety and novelty.'),
            ('otsuka-oronamin-vitamin-c-soda-6-packs', 'Oronamin Vitamin C Soda',
             f'Fanta melon is a sweet, fruity soda — pure refreshment. Oronamin is a vitamin C fortified drink with a more complex, citrusy flavor. Fanta for sweet soda lovers; Oronamin for those wanting a vitamin boost with their fizz.'),
        ]
    return []


def compare_sauces_condiments(slug, name):
    if 'laoganma' in slug:
        if 'crispy' in slug and '7.4' in slug:
            return [
                ('laoganma-spicy-crispy-chili-oil-210g', 'Laoganma Chili Oil (210g)',
                 f'The 7.4oz jar is the standard size — great for regular use. The 210g version is smaller for trying it first. Same iconic chili crisp formula in both — choose based on how fast you go through it.'),
                ('sb-umami-topping-crunchy-garlic-chili-oil-mild', 'S&B Umami Garlic Chili Oil',
                 f'Laoganma is a Chinese chili crisp — chunky, spicy, with fermented soybean depth. S&B is a Japanese garlic chili oil — smoother, garlic-forward, and milder. Laoganma for bold Chinese heat; S&B for gentle Japanese umami.'),
            ]
        return [
            ('laoganma-spicy-chili-crispy-7-4oz', 'Laoganma Chili Crispy (7.4oz)',
             f'The 210g jar is a compact size — perfect for trying the formula. The 7.4oz jar offers more for regular users. Both contain the same beloved spicy chili oil with crispy bits.'),
            ('sb-umami-topping-crunchy-garlic-chili-oil-spicy', 'S&B Umami Chili Oil (Spicy)',
             f'Laoganma is a Chinese classic — chunky chili crisp with fermented soybean and intense heat. S&B is Japanese — smoother texture with garlic umami and controlled spice. Laoganma for authentic Chinese heat; S&B for Japanese garlic umami.'),
        ]
    if 'sb-umami' in slug:
        if '4-packs' in slug:
            return [
                ('sb-umami-topping-crunchy-garlic-chili-oil-mild', 'S&B Umami Garlic Chili Oil (Single)',
                 f'The 4-pack gives you better per-unit value if you use this regularly. The single jar is ideal for first-time users to test the flavor. Both come in Mild and Spicy variants.'),
                ('laoganma-spicy-chili-crispy-7-4oz', 'Laoganma Spicy Chili Crispy',
                 f'S&B is Japanese — smooth, garlic-forward, with mild umami heat. Laoganma is Chinese — chunky, bold, with fermented soybean depth. S&B for gentle garlic umami; Laoganma for intense Chinese chili crisp.'),
            ]
        if 'spicy' in slug:
            return [
                ('sb-umami-topping-crunchy-garlic-chili-oil-mild', 'S&B Umami Garlic Chili Oil (Mild)',
                 f'The Spicy version has a real kick with more chili heat. The Mild version focuses on garlic umami with gentle warmth. Spicy for chili lovers; Mild for those who prefer flavor over fire.'),
                ('laoganma-spicy-chili-crispy-7-4oz', 'Laoganma Spicy Chili Crispy',
                 f'S&B Spicy is Japanese — chili heat with garlic umami and a smoother texture. Laoganma is Chinese — chunky, intense, with fermented soybean complexity. S&B for Japanese garlic chili; Laoganma for Chinese chili crisp.'),
            ]
        return [
            ('sb-umami-topping-crunchy-garlic-chili-oil-spicy', 'S&B Umami Chili Oil (Spicy)',
             f'The Mild version focuses on garlic umami with gentle warmth. The Spicy version adds real chili heat. Mild for flavor-first cooking; Spicy for those who want a kick.'),
            ('laoganma-spicy-chili-crispy-7-4oz', 'Laoganma Spicy Chili Crispy',
             f'S&B is Japanese — smooth, garlic-forward, with controlled umami heat. Laoganma is Chinese — chunky, bold, with fermented soybean depth. S&B for gentle garlic oil; Laoganma for intense chili crisp.'),
        ]
    if 'kikkoman' in slug:
        if 'dispenser' in slug:
            return [
                ('kikkoman-hello-kitty-soy-sauce-5oz', 'Kikkoman Hello Kitty Soy Sauce',
                 f'The dispenser is an empty decorative bottle — fill it with your favorite soy sauce. The 5oz bottle contains actual Kikkoman soy sauce. Dispenser for table presentation; bottle for immediate use.'),
                ('laoganma-spicy-chili-crispy-7-4oz', 'Laoganma Spicy Chili Crispy',
                 f'Kikkoman is a Japanese soy sauce — salty, umami, essential for Japanese and Asian cooking. Laoganma is a Chinese chili condiment — spicy, chunky, used as a topping or cooking ingredient. Different purposes: seasoning base vs flavor booster.'),
            ]
        return [
            ('kikkoman-hello-kitty-soy-sauce-dispenser', 'Kikkoman Hello Kitty Dispenser',
             f'This is the actual soy sauce — 5oz of Kikkoman\'s brewed soy sauce in a Hello Kitty bottle. The dispenser is a decorative empty bottle. Buy the sauce for cooking; the dispenser for table decoration.'),
            ('sb-umami-topping-crunchy-garlic-chili-oil-mild', 'S&B Umami Garlic Chili Oil',
             f'Kikkoman soy sauce is a fundamental Japanese seasoning — salty, umami, versatile. S&B garlic chili oil is a finishing condiment — aromatic, garlicky, spicy. Soy sauce for cooking base; chili oil for finishing touch.'),
        ]
    if 'dongwon' in slug:
        return [
            ('laoganma-spicy-chili-crispy-7-4oz', 'Laoganma Spicy Chili Crispy',
             f'Dongwon tuna is a Korean canned seafood product — protein-rich, ready to eat. Laoganma is a Chinese chili condiment — used as a flavor booster. Tuna for meals; Laoganma for seasoning.'),
            ('samyang-buldak-carbonara-hot-chicken-flavor-ramen-5-packs', 'Samyang Buldak Carbonara',
             f'Dongwon tuna is a versatile Korean canned protein — eat straight, mix with rice, or cook. Samyang Buldak is spicy instant ramen — a complete meal. Tuna for quick protein; ramen for a satisfying spicy bowl.'),
        ]
    if 'zhou-hei-ya' in slug or 'zhouheiya' in slug:
        return [
            ('laoganma-spicy-chili-crispy-7-4oz', 'Laoganma Spicy Chili Crispy',
             f'Zhou Hei Ya is a Chinese braising sauce — a complete seasoning mix for making braised dishes. Laoganma is a chili condiment — used as a topping or flavor booster. Braising sauce for full meals; chili crisp for quick flavor.'),
            ('galan-lang-lanzhou-beef-flavor-noodles-5-packs', 'Ga Lan Lang Lanzhou Noodles',
             f'Zhou Hei Ya braising sauce is for cooking braised meat and vegetable dishes at home. Ga Lan Lang is an instant Lanzhou beef noodle soup. Braising sauce for cooking projects; instant noodles for quick meals.'),
        ]
    return []


def compare_snacks(slug, name):
    if 'bibizan' in slug:
        if 'sweet-potato-strips' in slug:
            return [
                ('bibizan-steaming-dried-sweet-potatoes-250g', 'BiBiZan Dried Sweet Potatoes',
                 f'The sweet potato strips are sugar-free and have a chewy, candy-like texture. The dried sweet potatoes are softer and naturally sweet. Strips for a chewy snack; whole pieces for a softer bite.'),
                ('jellyb-konjac-jelly-lychee-10pcs-sugar-free', 'Jelly.B Konjac Jelly',
                 f'BiBiZan strips are sugar-free sweet potato snacks — chewy and naturally filling. Jelly.B konjac jelly is a low-calorie, fruity alternative. Both are guilt-free snacks — sweet potato for satiety; konjac for lightness.'),
            ]
        return [
            ('bibizan-sweet-potato-strips-sugar-free-250g', 'BiBiZan Sweet Potato Strips',
             f'The dried sweet potatoes are soft, naturally sweet, and minimally processed. The strips are sugar-free with a chewier, candy-like texture. Whole pieces for natural sweetness; strips for chewy snacking.'),
            ('rice-crackers-classic-milk-flavor-8-53oz', 'Rice Crackers Milk Flavor',
             f'BiBiZan dried sweet potatoes are a Chinese health snack — fiber-rich, naturally sweet. Rice crackers are a Japanese crispy snack — light, crunchy, with milk flavor. Sweet potato for wholesome snacking; rice crackers for crispy indulgence.'),
        ]
    if 'honey-butter' in slug:
        return [
            ('rice-crackers-classic-milk-flavor-8-53oz', 'Rice Crackers Milk Flavor',
             f'Korean Honey Butter chips are sweet, savory, and addictive — a K-snack phenomenon. Rice crackers are lighter, crispier, with a subtle milk flavor. Honey butter for bold indulgence; rice crackers for light snacking.'),
            ('malawangzi-latiao-mala-extra-spicy-gluten-strips-3-17oz', 'Malawangzi Latiao',
             f'Honey butter chips are sweet and buttery — a Korean classic. Malawangzi latiao is intensely spicy and numbing — a Chinese street food snack. Sweet and mild vs fiery and bold — opposite ends of the snack spectrum.'),
        ]
    if 'rice-crackers' in slug:
        return [
            ('korean-honey-butter-potato-chips-2-11oz-3-value-pack', 'Korean Honey Butter Chips',
             f'Rice crackers are light, crispy, with a subtle milk flavor — a gentle Japanese snack. Honey butter chips are bold, sweet, and buttery — a Korean phenomenon. Rice crackers for light snacking; honey butter for indulgence.'),
            ('bibizan-steaming-dried-sweet-potatoes-250g', 'BiBiZan Dried Sweet Potatoes',
             f'Rice crackers are a Japanese crispy snack — light and airy. BiBiZan sweet potatoes are a Chinese health snack — soft, fiber-rich, naturally sweet. Crispy indulgence vs wholesome nutrition.'),
        ]
    if 'malawangzi' in slug:
        return [
            ('korean-honey-butter-potato-chips-2-11oz-3-value-pack', 'Korean Honey Butter Chips',
             f'Malawangzi latiao is intensely spicy and numbing — a bold Chinese street food snack. Honey butter chips are sweet and mild — a Korean crowd-pleaser. Latiao for heat seekers; honey butter for gentle snacking.'),
            ('jellyb-konjac-jelly-lychee-10pcs-sugar-free', 'Jelly.B Konjac Jelly',
             f'Malawangzi is a spicy, chewy gluten snack — bold, numbing, and addictive. Jelly.B is a sweet, fruity konjac jelly — light and refreshing. Spicy and savory vs sweet and cool.'),
        ]
    if 'jellyb' in slug or 'jelly-b' in slug or 'konjac' in slug:
        return [
            ('bibizan-sweet-potato-strips-sugar-free-250g', 'BiBiZan Sweet Potato Strips',
             f'Jelly.B konjac jelly is a low-calorie, fruity snack — light and refreshing. BiBiZan sweet potato strips are sugar-free but more filling and chewy. Both are guilt-free — konjac for lightness; sweet potato for satiety.'),
            ('korean-honey-butter-potato-chips-2-11oz-3-value-pack', 'Korean Honey Butter Chips',
             f'Jelly.B is a low-calorie konjac jelly — light, fruity, and guilt-free. Honey butter chips are indulgent, sweet, and buttery. Konjac for diet-friendly snacking; honey butter for treat-yourself moments.'),
        ]
    if 'egg-tarts' in slug:
        return [
            ('rice-crackers-classic-milk-flavor-8-53oz', 'Rice Crackers Milk Flavor',
             f'Egg tarts are a classic Chinese bakery treat — flaky pastry with creamy custard. Rice crackers are a Japanese crispy snack — light and crunchy. Bakery indulgence vs crispy snacking.'),
            ('korean-honey-butter-potato-chips-2-11oz-3-value-pack', 'Korean Honey Butter Chips',
             f'Egg tarts are a Chinese pastry — soft custard in flaky crust, best enjoyed fresh. Honey butter chips are a Korean crispy snack — sweet, salty, and shelf-stable. Fresh bakery vs packaged snacking.'),
        ]
    return []


def compare_acne_treatment(slug, name):
    if 'donga' in slug:
        return [
            ('lion-pair-acne-cream-13g-3', 'LION PAIR Acne Cream',
             f'DONGA Acnon is a Korean pharmaceutical acne treatment — targeted spot treatment with antibacterial ingredients. LION PAIR is a Japanese gentle formula — works on both acne and prevention. DONGA for active breakouts; PAIR for gentle, ongoing care.'),
            ('pair-acne-creamy-face-wash-foam-80g', 'PAIR Acne Face Wash',
             f'DONGA Acnon is a leave-on cream treatment — apply directly to blemishes. PAIR Face Wash is a cleanser — washes away oil and bacteria preventively. Cream for targeted treatment; face wash for daily prevention.'),
        ]
    if 'lion-pair' in slug and 'cream' in slug and '14g' in slug:
        return [
            ('donga-pharm-acnon-cream-13g', 'DONGA Acnon Cream',
             f'LION PAIR is a Japanese gentle acne cream — suitable for sensitive skin, works on acne and prevention. DONGA Acnon is a Korean pharmaceutical treatment — more targeted for active breakouts. PAIR for gentle daily use; DONGA for active spot treatment.'),
            ('pair-acne-creamy-face-wash-foam-80g', 'PAIR Acne Face Wash',
             f'The PAIR Cream is a leave-on treatment — apply to clean skin on blemishes. The Face Wash is a cleanser that preps skin and prevents breakouts. Use together: wash first, then cream for a complete PAIR routine.'),
        ]
    if 'pair-acne-creamy' in slug or 'face-wash' in slug:
        return [
            ('lion-pair-acne-cream-13g-3', 'LION PAIR Acne Cream',
             f'The Face Wash cleanses and preps skin — your first step. The Acne Cream is a leave-on treatment — apply after washing. Use together for the complete PAIR acne system.'),
            ('donga-pharm-acnon-cream-13g', 'DONGA Acnon Cream',
             f'PAIR Face Wash is a gentle Japanese cleanser for daily acne prevention. DONGA Acnon is a Korean pharmaceutical spot treatment for active breakouts. Prevention vs treatment — use the wash daily, DONGA as needed.'),
        ]
    if 'pair-acne-treatment' in slug:
        return [
            ('lion-pair-acne-cream-13g-3', 'LION PAIR Acne Cream (14g × 3)',
             f'This 24g tube is a single larger size. The 14g × 3 pack gives you the same total amount in three smaller tubes — more portable and longer-lasting supply. Choose based on your preference for tube size.'),
            ('donga-pharm-acnon-cream-13g', 'DONGA Acnon Cream',
             f'PAIR Treatment Cream is a Japanese gentle formula — works on acne and prevents new breakouts. DONGA Acnon is a Korean pharmaceutical treatment — more focused on active blemishes. PAIR for gentle care; DONGA for targeted treatment.'),
        ]
    return []


def compare_beauty_devices(slug, name):
    if 'medicube' in slug:
        return [
            ('yaman-sp-iii-star-edition-hertz-rf-beauty-device', 'YAMAN SPIII RF Beauty Device',
             f'Medicube Booster Pro uses electrical currents to enhance serum absorption. YAMAN SPIII uses RF (radio frequency) and Hertz vibration for skin tightening and lifting. Booster Pro for product absorption; SPIII for firming and lifting.'),
            ('fujiko-pon-pon-powder-natural-volume-8-5g', 'FUJIKO Pon Pon Powder',
             f'Medicube is an electronic beauty device for serum absorption and skin rejuvenation. FUJIKO is a simple powder puff for oil control and volume — no electronics needed. High-tech skincare vs quick touch-up tool.'),
        ]
    if 'yaman' in slug or 'sp-iii' in slug or 'spiii' in slug:
        return [
            ('medicube-age-r-booster-pro-pink', 'Medicube Age-R Booster Pro',
             f'YAMAN SPIII uses RF and Hertz vibration for skin tightening and anti-aging. Medicube Booster Pro uses electrical currents to boost serum absorption. SPIII for firming; Booster Pro for product penetration.'),
            ('fujiko-pon-pon-powder-natural-volume-8-5g', 'FUJIKO Pon Pon Powder',
             f'YAMAN is a premium Japanese RF beauty device for anti-aging treatments. FUJIKO is a simple powder puff for oil control. Professional skincare device vs everyday beauty accessory.'),
        ]
    if 'dr-arrivo' in slug or 'dr.arrivo' in slug or 'zeus' in slug:
        return [
            ('medicube-age-r-booster-pro-pink', 'Medicube Age-R Booster Pro',
             f'Dr.Arrivo Zeus III is a premium Japanese facial device with advanced EMS and RF technology. Medicube Booster Pro focuses on electrical serum absorption at a lower price point. Dr.Arrivo for comprehensive facial treatment; Medicube for absorption enhancement.'),
            ('yaman-sp-iii-star-edition-hertz-rf-beauty-device', 'YAMAN SPIII RF Beauty Device',
             f'Both are premium Japanese beauty devices. Dr.Arrivo Zeus III emphasizes EMS facial massage and lifting. YAMAN SPIII focuses on RF skin tightening and Hertz vibration. Dr.Arrivo for lifting and massage; YAMAN for tightening and firming.'),
        ]
    if 'fujiko' in slug:
        return [
            ('medicube-age-r-booster-pro-pink', 'Medicube Age-R Booster Pro',
             f'FUJIKO Pon Pon Powder is a simple, non-electronic powder puff for oil control and hair volume. Medicube Booster Pro is an electronic beauty device for serum absorption. Quick touch-up tool vs high-tech skincare device.'),
            ('yaman-sp-iii-star-edition-hertz-rf-beauty-device', 'YAMAN SPIII RF Beauty Device',
             f'FUJIKO is an affordable, non-electronic beauty accessory — powder puff for oil control. YAMAN SPIII is a premium RF device for skin tightening. Simple accessory vs advanced technology.'),
        ]
    return []


def compare_masks_sets(slug, name):
    if 'ilso' in slug:
        return [
            ('keana-nadeshiko-pore-care-rice-mask-10pcs', 'Keana Nadeshiko Rice Mask',
             f'ILSO uses a melting balm texture that dissolves sebum — a unique Korean approach to pore care. Keana Nadeshiko uses Japanese rice enzymes for gentle exfoliation and brightening. ILSO for deep sebum removal; Keana for gentle brightening.'),
            ('skin1004-madagascar-centella-tone-brightening-skincare-set-value-pack', 'SKIN1004 Brightening Set',
             f'ILSO targets pores and sebum with a melting balm formula. SKIN1004 focuses on overall skin tone brightening with centella asiatica. ILSO for pore-specific care; SKIN1004 for full-face radiance.'),
        ]
    if 'keana' in slug:
        return [
            ('ilso-super-melting-sebum-softener-value-pack', 'ILSO Sebum Softener',
             f'Keana Nadeshiko uses Japanese rice enzymes for gentle pore care and brightening. ILSO uses a melting balm that dissolves sebum directly. Keana for gentle, brightening pore care; ILSO for intensive sebum removal.'),
            ('skin1004-madagascar-centella-tone-brightening-skincare-set-value-pack', 'SKIN1004 Brightening Set',
             f'Keana Nadeshiko is a Japanese rice mask focused on pore refinement and gentle exfoliation. SKIN1004 is a Korean centella-based brightening skincare set. Keana for pore care; SKIN1004 for overall skin tone.'),
        ]
    if 'skin1004' in slug:
        if 'travel-kit' in slug:
            return [
                ('skin1004-madagascar-centella-tone-brightening-skincare-set-value-pack', 'SKIN1004 Brightening Set (Full Size)',
                 f'The travel kit includes mini sizes of SKIN1004\'s centella line — perfect for trying before committing to full sizes. The full-size set gives you the complete routine at better value.'),
                ('keana-nadeshiko-pore-care-rice-mask-10pcs', 'Keana Nadeshiko Rice Mask',
                 f'SKIN1004 focuses on centella asiatica for calming and brightening — a Korean approach. Keana Nadeshiko uses Japanese rice for pore care and gentle exfoliation. SKIN1004 for soothing; Keana for pore refinement.'),
            ]
        return [
            ('keana-nadeshiko-pore-care-rice-mask-10pcs', 'Keana Nadeshiko Rice Mask',
             f'SKIN1004 uses centella asiatica for calming, hydrating, and brightening. Keana Nadeshiko uses rice enzymes for pore care and gentle exfoliation. SKIN1004 for sensitive skin soothing; Keana for pore refinement.'),
            ('ilso-super-melting-sebum-softener-value-pack', 'ILSO Sebum Softener',
             f'SKIN1004 brightening set focuses on overall skin tone and hydration with centella. ILSO targets pores and sebum with a melting balm formula. SKIN1004 for radiance; ILSO for deep pore cleansing.'),
        ]
    return []


def compare_gift_boxes(slug, name):
    if 'blessings' in slug:
        return [
            ('isabelle-taiwan-pineapple-cakes-16-9oz', 'ISABELLE Taiwan Pineapple Cakes',
             f'The Blessings Abound box is a Chinese pastry gift set — assorted traditional pastries for celebrations. ISABELLE pineapple cakes are a Taiwanese specialty — buttery, with sweet pineapple filling. Chinese pastry variety vs Taiwanese specialty.'),
            ('godiva-x-labubu-hazelnut-milk-chocolate-gift-box-2-82oz', 'Godiva × Labubu Chocolate',
             f'Blessings Abound offers traditional Chinese pastries — great for Lunar New Year and cultural celebrations. Godiva × Labubu is a Belgian chocolate collaboration — modern, playful, universally appealing. Traditional vs contemporary gifting.'),
        ]
    if 'godiva' in slug:
        return [
            ('blessings-abound-pastry-gift-box-34-57oz', 'Blessings Abound Pastry Box',
             f'Godiva × Labubu is a Belgian chocolate gift — modern, playful, with a collectible Labubu theme. Blessings Abound is a traditional Chinese pastry set — classic and culturally significant. Chocolate fun vs traditional elegance.'),
            ('isabelle-taiwan-pineapple-cakes-16-9oz', 'ISABELLE Taiwan Pineapple Cakes',
             f'Godiva × Labubu is a premium chocolate gift with a trendy collaboration angle. ISABELLE pineapple cakes are a beloved Taiwanese specialty — buttery and comforting. International luxury vs Taiwanese tradition.'),
        ]
    if 'isabelle' in slug:
        return [
            ('blessings-abound-pastry-gift-box-34-57oz', 'Blessings Abound Pastry Box',
             f'ISABELLE pineapple cakes are a Taiwanese classic — buttery pastry with sweet pineapple filling. Blessings Abound offers a variety of traditional Chinese pastries. Single specialty vs assorted selection.'),
            ('godiva-x-labubu-hazelnut-milk-chocolate-gift-box-2-82oz', 'Godiva × Labubu Chocolate',
             f'ISABELLE pineapple cakes are a beloved Taiwanese treat — comforting and traditional. Godiva × Labubu is a modern Belgian chocolate gift — trendy and playful. Taiwanese heritage vs international contemporary.'),
        ]
    if 'new-year' in slug or 'candy' in slug:
        return [
            ('blessings-abound-pastry-gift-box-34-57oz', 'Blessings Abound Pastry Box',
             f'The New Year Candy Box is a festive mix of assorted candies — fun and colorful for celebrations. Blessings Abound offers traditional Chinese pastries — more formal and culturally significant. Casual festivity vs traditional elegance.'),
            ('godiva-x-labubu-hazelnut-milk-chocolate-gift-box-2-82oz', 'Godiva × Labubu Chocolate',
             f'New Year Candy Box is an assorted candy mix — great for sharing at parties. Godiva × Labubu is a premium chocolate gift — more personal and luxurious. Casual sharing vs premium gifting.'),
        ]
    return []


def compare_health_personal_care(slug, name):
    if 'apagard' in slug:
        return [
            ('okamoto-001-extra-lubricated-condoms-large-fit-6pcs-value-pack', 'OKAMOTO 001 Condoms',
             f'APAGARD is a Japanese toothpaste with hydroxyapatite — the same mineral as tooth enamel — for remineralization. OKAMOTO 001 is an ultra-thin condom. Completely different products — oral care vs personal protection.'),
            ('foodology-coleology-cutting-jelly-250g', 'Coleology Cutting Jelly',
             f'APAGARD uses hydroxyapatite for tooth enamel repair — a science-backed oral care product. Coleology Cutting Jelly is a Korean dietary supplement for body odor control. Oral health vs internal wellness.'),
        ]
    if 'coleology' in slug or 'cutting-jelly' in slug:
        return [
            ('apagard-premio-hydroxyapatite-toothpaste-3-7oz', 'APAGARD Toothpaste',
             f'Coleology Cutting Jelly is a Korean dietary supplement for internal body odor control. APAGARD is a Japanese hydroxyapatite toothpaste for enamel repair. Internal wellness vs oral care.'),
            ('okamoto-001-extra-lubricated-condoms-large-fit-6pcs-value-pack', 'OKAMOTO 001 Condoms',
             f'Coleology Cutting Jelly is a dietary supplement for body odor management. OKAMOTO 001 is an ultra-thin condom. Wellness supplement vs personal protection — different health categories.'),
        ]
    if 'okamoto' in slug:
        if 'extra-lubricated' in slug:
            return [
                ('okamoto-001-ultra-thin-condoms-15pcs-value-pack', 'OKAMOTO 001 (15pcs Value Pack)',
                 f'The Extra Lubricated version adds extra lubricant for enhanced comfort. The standard 001 focuses on ultra-thin sensitivity. Extra lubricated for comfort-first; standard for maximum sensation.'),
                ('sagami-001-original-condoms-10pcs-value-pack', 'SAGAMI 001 Original',
                 f'Both are premium Japanese 001 ultra-thin condoms. OKAMOTO uses polyurethane with extra lubrication. SAGAMI also uses polyurethane in a slightly different fit. OKAMOTO for lubrication; SAGAMI for the original 001 experience.'),
            ]
        return [
            ('okamoto-001-extra-lubricated-condoms-large-fit-6pcs-value-pack', 'OKAMOTO 001 Extra Lubricated',
             f'The 15-pack offers better per-unit value for regular use. The 6-pack is ideal for trying or occasional use. Same ultra-thin polyurethane technology in both.'),
            ('sagami-001-original-condoms-10pcs-value-pack', 'SAGAMI 001 Original',
             f'Both are Japanese 001 ultra-thin polyurethane condoms. OKAMOTO is known for a slightly snugger fit; SAGAMI for a more standard fit. Both offer exceptional thinness — choose based on fit preference.'),
        ]
    if 'sagami' in slug:
        return [
            ('okamoto-001-ultra-thin-condoms-15pcs-value-pack', 'OKAMOTO 001 (15pcs)',
             f'SAGAMI 001 is the original ultra-thin polyurethane condom from Japan. OKAMOTO 001 is a competing product with similar thinness. Both are premium — SAGAMI for the original; OKAMOTO for value in a larger pack.'),
            ('okamoto-001-extra-lubricated-condoms-large-fit-6pcs-value-pack', 'OKAMOTO 001 Extra Lubricated',
             f'SAGAMI 001 is the original Japanese ultra-thin condom — known for its standard fit. OKAMOTO Extra Lubricated adds extra lubricant for enhanced comfort. SAGAMI for the classic experience; OKAMOTO for added comfort.'),
        ]
    return []


def compare_dried_goods(slug, name):
    if 'ocm' in slug or 'organic' in slug.lower():
        return [
            ('dried-red-dates-jujubes-80oz', 'Sunshine Dried Red Dates',
             f'OCM offers organic Ningxia jujubes — a specific premium growing region known for quality. Sunshine Dried Red Dates offer a larger 80oz package. OCM for organic certification and Ningxia origin; Sunshine for bulk value.'),
            ('premium-dried-goji-berries-7-9-oz', 'Premium Dried Goji Berries',
             f'OCM jujubes (red dates) are used in Chinese cooking and tea — sweet, chewy, and warming. Goji berries are smaller, more tart, and packed with different nutrients. Jujubes for cooking and tea; goji for snacking and smoothies.'),
        ]
    if 'goji' in slug:
        return [
            ('ocm-organic-ningxia-jujube-16oz', 'OCM Organic Ningxia Jujube',
             f'Goji berries are small, tart, and nutrient-dense — great for snacking and smoothies. Jujubes (red dates) are larger, sweeter, and used in Chinese cooking and tea. Goji for nutrition snacking; jujube for traditional cooking.'),
            ('dried-red-dates-jujubes-80oz', 'Sunshine Dried Red Dates',
             f'Premium Goji Berries are a smaller 7.94oz package of nutrient-dense berries. Sunshine Dried Red Dates offer a massive 80oz of jujubes. Goji for concentrated nutrition; jujubes for bulk cooking and tea.'),
        ]
    if 'red-dates' in slug or 'jujubes' in slug:
        return [
            ('ocm-organic-ningxia-jujube-16oz', 'OCM Organic Ningxia Jujube',
             f'Sunshine offers 80oz of dried red dates — massive value for regular users. OCM offers 16oz of organic, Ningxia-origin jujubes — premium quality in a smaller package. Bulk value vs organic premium.'),
            ('premium-dried-goji-berries-7-9-oz', 'Premium Dried Goji Berries',
             f'Dried red dates (jujubes) are larger, sweeter, and used in Chinese soups and teas. Goji berries are smaller, more tart, and eaten as snacks or added to smoothies. Jujubes for cooking; goji for snacking.'),
        ]
    return []


def compare_kitchen_appliances(slug, name):
    if 'joyoung' in slug:
        if 'soy-milk' in slug.lower() or 'dj' in slug.lower():
            if 'dj12n' in slug.lower() or 'k7g' in slug.lower():
                return [
                    ('joyoung-soy-milk-maker-1-3l-dj13u-g91', 'Joyoung DJ13U-G91 (1.3L)',
                     f'The DJ12N-K7G is the low-purine model — designed for those watching purine intake. The DJ13U-G91 is a multi-functional model with more program options. Low-purine for health needs; multi-function for versatility.'),
                    ('joyoung-multi-functional-soy-milk-maker-dj10u-k1-brown', 'Joyoung DJ10U-K1',
                     f'The DJ12N-K7G focuses on low-purine soy milk — a specific health benefit. The DJ10U-K1 is a compact, stylish model with multiple functions. Low-purine for dietary needs; DJ10U-K1 for compact versatility.'),
                ]
            if 'dj13u' in slug.lower() or 'g91' in slug.lower():
                return [
                    ('joyoung-low-purine-soy-milk-machine-dj12n-k7g', 'Joyoung DJ12N-K7G (Low Purine)',
                     f'The DJ13U-G91 offers multiple functions (soy milk, rice paste, juice) with a 1.3L capacity. The DJ12N-K7G specializes in low-purine soy milk. Multi-function for variety; low-purine for specific health needs.'),
                    ('joyoung-multi-functional-soy-milk-maker-dj10u-k1-brown', 'Joyoung DJ10U-K1',
                     f'The DJ13U-G91 has a larger 1.3L capacity — better for families. The DJ10U-K1 is more compact with a modern brown design. Larger capacity for families; compact for individuals or small kitchens.'),
                ]
            if 'dj10u' in slug.lower() or 'k1' in slug.lower():
                return [
                    ('joyoung-soy-milk-maker-1-3l-dj13u-g91', 'Joyoung DJ13U-G91 (1.3L)',
                     f'The DJ10U-K1 is compact and stylish — great for smaller kitchens. The DJ13U-G91 has a larger 1.3L capacity for families. Compact design for small spaces; larger capacity for bigger households.'),
                    ('joyoung-low-purine-soy-milk-machine-dj12n-k7g', 'Joyoung DJ12N-K7G (Low Purine)',
                     f'The DJ10U-K1 is a multi-functional model with various program options. The DJ12N-K7G specializes in low-purine soy milk for health-conscious users. Versatility for variety; low-purine for specific dietary needs.'),
                ]
        if 'wellness-kettle' in slug.lower() or 'k08' in slug.lower():
            return [
                ('joyoung-soy-milk-maker-1-3l-dj13u-g91', 'Joyoung Soy Milk Maker',
                 f'The Wellness Kettle is a multi-function kettle for tea, boiling water, and light cooking. The Soy Milk Maker specializes in soy milk, nut milk, and pastes. Kettle for beverages; soy milk maker for plant-based milk production.'),
                ('joyoung-low-purine-soy-milk-machine-dj12n-k7g', 'Joyoung Low-Purine Soy Milk Machine',
                 f'The Wellness Kettle handles hot water, tea, and light cooking tasks. The Low-Purine Soy Milk Machine makes fresh soy milk with reduced purines. Kettle for daily hot beverages; soy milk machine for health-focused milk making.'),
            ]
    if 'olayks' in slug:
        return [
            ('zojirushi-gourmet-expert-electric-skillet-hot-pot-ep-pbc10', 'Zojirushi Electric Skillet',
             f'OLAYKS is a dish sterilizer and dryer — for cleaning and storing tableware hygienically. Zojirushi Electric Skillet is for cooking — hot pot, frying, and more. Kitchen hygiene vs cooking appliance.'),
            ('staub-round-dutch-oven-enamel-coated-cast-iron-peony-pink-4qt', 'Staub Dutch Oven',
             f'OLAYKS is an electric dish sterilizer — keeps your tableware clean and organized. Staub is a premium cast-iron Dutch oven for slow cooking and braising. Kitchen organization vs cooking performance.'),
        ]
    if 'zojirushi' in slug and 'skillet' in slug.lower():
        return [
            ('olayks-kitchen-dish-sterilizer-42l', 'OLAYKS Dish Sterilizer',
             f'Zojirushi Electric Skillet is for cooking — hot pot, frying, simmering. OLAYKS Dish Sterilizer is for cleaning and sanitizing tableware. Cooking appliance vs kitchen hygiene device.'),
            ('staub-round-dutch-oven-enamel-coated-cast-iron-peony-pink-4qt', 'Staub Dutch Oven',
             f'Zojirushi Electric Skillet is an electric cooking pot — precise temperature control for hot pot and more. Staub is a cast-iron Dutch oven — excellent heat retention for oven-to-table cooking. Electric precision vs cast-iron tradition.'),
        ]
    if 'staub' in slug:
        return [
            ('zojirushi-gourmet-expert-electric-skillet-hot-pot-ep-pbc10', 'Zojirushi Electric Skillet',
             f'Staub is a premium enameled cast-iron Dutch oven — oven-safe, stunning on the table, excellent for slow cooking. Zojirushi is an electric skillet — precise temperature control, no stovetop needed. Cast-iron tradition vs electric convenience.'),
            ('olayks-kitchen-dish-sterilizer-42l', 'OLAYKS Dish Sterilizer',
             f'Staub is a premium cooking vessel — enameled cast iron for slow cooking and braising. OLAYKS is a dish sterilizer for cleaning and storing tableware. Cooking performance vs kitchen hygiene.'),
        ]
    return []


def compare_canned_food(slug, name):
    if 'dongwon' in slug:
        return [
            ('dongwon-tuna-chili-sauce-5-29oz-4-packs', 'Dongwon Tuna with Chili Sauce',
             f'The BTS Jin Special Edition features collectible packaging with 12 cans. The chili sauce variant offers a spicy flavor twist. Collectible edition for fans; chili sauce for flavor variety.'),
            ('laoganma-spicy-chili-crispy-7-4oz', 'Laoganma Spicy Chili Crispy',
             f'Dongwon tuna is a Korean canned seafood — protein-rich, ready to eat. Laoganma is a Chinese chili condiment — used as a flavor booster. Tuna for meals and protein; Laoganma for seasoning and heat.'),
        ]
    return []


def compare_fragrance(slug, name):
    if 'tamburins' in slug:
        return [
            ('sulwhasoo-first-care-activating-serum-90ml', 'Sulwhasoo First Care Serum',
             f'TAMBURINS #CHAMO is a Korean niche fragrance — herbal, warm, and distinctly unique. Sulwhasoo is a Korean luxury skincare line. Fragrance for your signature scent; Sulwhasoo for your skincare ritual.'),
            ('medicube-age-r-booster-pro-pink', 'Medicube Age-R Booster Pro',
             f'TAMBURINS #CHAMO is a luxury Korean perfume by Jennie\'s brand — a fashion-meets-fragrance statement. Medicube is a Korean beauty device for serum absorption. Scent statement vs skincare technology.'),
        ]
    return []


def compare_makeup(slug, name):
    if 'suqqu' in slug:
        return [
            ('sulwhasoo-the-ultimate-s-cream-60ml', 'Sulwhasoo Ultimate S Cream',
             f'SUQQU Foundation is a luxury Japanese makeup product — coverage and luminosity. Sulwhasoo Ultimate S Cream is a luxury Korean skincare moisturizer — hydration and anti-aging. Makeup for appearance; skincare for skin health.'),
            ('beauty-of-joseon-revive-eye-serum-ginseng-retinal', 'Beauty of Joseon Eye Serum',
             f'SUQQU is a premium Japanese foundation — known for its luminous, skin-like finish. Beauty of Joseon Eye Serum is a Korean eye treatment with ginseng and retinal. Foundation for complexion; eye serum for targeted treatment.'),
        ]
    return []


def compare_marketplace(slug, name):
    return [
        ('asian-sunscreen-buying-guide', 'Asian Sunscreen Buying Guide',
         'Yami is the largest Asian e-commerce platform in North America — carrying everything from Korean skincare to Japanese snacks. The sunscreen buying guide helps you navigate the best Asian sunscreens available in the US.'),
        ('chagee-boya-jasmine-tea', 'CHAGEE BOYA Jasmine Tea',
         'Yami carries 10,000+ Asian products across food, beauty, and health categories. CHAGEE BOYA is one of the premium teas available — explore the full selection for more Asian favorites.'),
    ]


# ── Master dispatch ────────────────────────────────────────────────

COMPARE_MAP = {
    'Sunscreen': compare_sunscreen,
    'Rice Cookers': compare_rice_cookers,
    'Noodles & Ramen': compare_noodles_ramen,
    'Serums & Ampoules': compare_serums_ampoules,
    'Hair Care': compare_hair_care,
    'Beverages & Tea': compare_beverages_tea,
    'Sauces & Condiments': compare_sauces_condiments,
    'Snacks': compare_snacks,
    'Acne Treatment': compare_acne_treatment,
    'Beauty Devices': compare_beauty_devices,
    'Masks & Sets': compare_masks_sets,
    'Gift Boxes': compare_gift_boxes,
    'Health & Personal Care': compare_health_personal_care,
    'Dried Goods': compare_dried_goods,
    'Kitchen Appliances': compare_kitchen_appliances,
    'Canned Food': compare_canned_food,
    'Fragrance': compare_fragrance,
    'Makeup': compare_makeup,
    'Marketplace': compare_marketplace,
}


def build_compare_html(comparisons, product_name, slug):
    short_name = product_name.split('|')[0].strip()
    display_name = short_name[:45] + ('...' if len(short_name) > 45 else '')

    h = hashlib.md5(slug.encode()).hexdigest()
    heading_idx = int(h[:8], 16) % len(HEADING_VARIANTS)
    subtitle_idx = int(h[8:16], 16) % len(SUBTITLE_VARIANTS)

    heading = HEADING_VARIANTS[heading_idx].format(name=display_name)
    subtitle = SUBTITLE_VARIANTS[subtitle_idx]

    cards = []
    for target_slug, target_name, text in comparisons:
        cards.append(f'''        <div class="compare-card">
            <div class="vs-badge">VS</div>
            <h3>{display_name} vs {target_name}</h3>
            <p>{text}</p>
            <a href="/landing-pages/{target_slug}" class="compare-link">View {target_name} &rarr;</a>
        </div>''')

    cards_html = '\n'.join(cards)

    return f'''
    <!-- Compare Section -->
    <section class="compare-section" aria-label="Product comparison">
        <h2 class="section-title fade-in">{heading}</h2>
        <p class="section-subtitle fade-in">{subtitle}</p>
        <div class="compare-grid">
{cards_html}
        </div>
    </section>
'''


def inject_compare(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'class="compare-section"' in content:
        return False

    category = get_category(content)
    if not category or category not in COMPARE_MAP:
        print(f"  SKIP (no category match): {os.path.basename(filepath)}")
        return False

    slug = get_slug(filepath)
    product_name = get_product_name(content) or slug.replace('-', ' ').title()

    comparisons = COMPARE_MAP[category](slug, product_name)
    if not comparisons:
        print(f"  SKIP (no comparisons): {os.path.basename(filepath)}")
        return False

    section_html = build_compare_html(comparisons, product_name, slug)

    # Inject CSS
    head_end = content.find('</head>')
    if head_end == -1:
        print(f"  ERROR: no </head> found")
        return False
    style_end = content.rfind('</style>', 0, head_end)
    if style_end == -1:
        print(f"  ERROR: no </style> found")
        return False
    content = content[:style_end] + COMPARE_CSS + '\n' + content[style_end:]

    # Inject HTML - before FAQ, or before CTA
    faq_comment = content.find('    <!-- FAQ Section -->')
    faq_class = content.find('class="faq-section"')
    cta_comment = content.find('    <!-- CTA -->')
    final_cta = content.find('    <!-- Final CTA -->')

    inject_pos = -1
    if faq_comment != -1:
        inject_pos = faq_comment
    elif faq_class != -1:
        inject_pos = content.rfind('\n', 0, faq_class) + 1
    elif cta_comment != -1:
        inject_pos = cta_comment
    elif final_cta != -1:
        inject_pos = final_cta

    if inject_pos == -1:
        print(f"  ERROR: no injection point found")
        return False

    content = content[:inject_pos] + section_html + '\n' + content[inject_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = sorted(glob.glob(os.path.join(base_dir, '*.html')))

    skip = {'index.html', 'test-simple.html', 'kikkoman-fixed.html'}
    files = [f for f in files if os.path.basename(f) not in skip]

    success = 0
    for filepath in files:
        basename = os.path.basename(filepath)
        if args.dry_run:
            category = get_category(open(filepath).read())
            slug = get_slug(filepath)
            print(f"  {basename}: category={category}")
            continue

        if inject_compare(filepath):
            success += 1
            print(f"  OK: {basename}")

    print(f"\nDone: {success}/{len(files)} files injected")


if __name__ == '__main__':
    main()
