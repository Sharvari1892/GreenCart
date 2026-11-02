import sys
import os

# Set up python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.category import Category
from app.models.product import Product
from app.models.sustainability_evidence import SustainabilityEvidence
from app.models.product_replacement import ProductReplacement

def seed_data():
    """
    Seed or update the GreenCart database with 33 real Indian-market products across 5 categories,
    17 structured replacement relationships, accurate source verification statuses, and verified evidence.
    """
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # 1. Categories
        categories_data = [
            {"name": "Personal Care", "description": "Conscious oral care, hair care, and personal grooming essentials."},
            {"name": "Kitchen & Home", "description": "Reusable, non-toxic cookware, food storage, and cleaning alternatives."},
            {"name": "Clothing", "description": "Organic cotton, upcycled, and ethically produced conscious apparel."},
            {"name": "Electronics & Accessories", "description": "Biodegradable accessories, rechargeable power, and repairable hardware."},
            {"name": "Everyday Essentials", "description": "Sustainable everyday swaps for plastic bags, pens, liners, and hygiene."},
        ]

        cat_map = {}
        for cdata in categories_data:
            cat = db.query(Category).filter(Category.name == cdata["name"]).first()
            if not cat:
                cat = Category(name=cdata["name"], description=cdata["description"])
                db.add(cat)
                db.flush()
            else:
                cat.description = cdata["description"]
            cat_map[cdata["name"]] = cat

        db.commit()

        # 2. Curated Products (33 Real Indian-market products with audited sources)
        # source_verification_status options:
        # - "verified_exact_source": Direct official product purchase/listing page with exact model, price, and specs verified.
        # - "manufacturer_info_only": Official manufacturer informational/catalogue page (specs provided, direct purchase not on that URL).
        # - "retailer_source": Authorized Indian retailer listing (Amazon.in / Nykaa / Croma / Brown Living).
        # - "unverified": Commodity or generic item with no direct branded product page.
        products_data = [
            # ══════════════════════════════════════════════════════
            # Personal Care (9 products: 4 conventional, 5 sustainable)
            # ══════════════════════════════════════════════════════
            {
                "key": "colgate_toothbrush",
                "name": "Colgate Extra Clean Toothbrush",
                "brand": "Colgate",
                "category": "Personal Care",
                "description": "Mass-market manual toothbrush with non-recyclable virgin plastic handle and synthetic nylon bristles.",
                "price": 30.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1559591937-e62fb330bc1f?w=600&auto=format&fit=crop&q=80",
                "materials": "100% virgin polypropylene (PP) handle with rubber grip, nylon-6 bristles",
                "purchase_url": "https://www.colgate.com/en-in/products/toothbrush/colgate-extra-clean",
                "source_verification_status": "manufacturer_info_only",
                "is_sustainable": False,
                "durability_score": 35,
                "packaging_score": 20,
                "repairability_score": None, # Disposable single-use dental consumable; repairability not applicable
                "evidence": []
            },
            {
                "key": "bamboo_toothbrush",
                "name": "Bamboo India Natural Bamboo Toothbrush",
                "brand": "Bamboo India",
                "category": "Personal Care",
                "description": "Handcrafted toothbrush from sustainably harvested Indian Moso bamboo with soft charcoal-infused bristles.",
                "price": 45.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=600&auto=format&fit=crop&q=80",
                "materials": "100% natural biodegradable Moso bamboo handle, charcoal-infused nylon-6 bristles",
                "purchase_url": "https://bambooindia.com/products/adult-bamboo-toothbrush",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 70,
                "packaging_score": 95,
                "repairability_score": None, # Consumable bristles require 3-month dental replacement
                "evidence": [
                    {"criterion": "packaging", "description": "100% plastic-free unbleached recycled kraft paper box.", "source_url": "https://bambooindia.com/products/adult-bamboo-toothbrush", "verification_status": "manufacturer_reported"},
                ]
            },
            {
                "key": "millnmint_toothbrush",
                "name": "Mill & Mint Stainless Steel Reusable Toothbrush",
                "brand": "Mill & Mint",
                "category": "Personal Care",
                "description": "Permanent 316L medical surgical stainless steel handle designed in India with replaceable click-on bristle heads.",
                "price": 1210.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&auto=format&fit=crop&q=80",
                "materials": "316L surgical stainless steel handle, recyclable thermoplastic elastomer (TPE) click-on head",
                "purchase_url": "https://millnmint.com/products/the-toothbrush",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 98,
                "packaging_score": 90,
                "repairability_score": 95,
                "evidence": [
                    {"criterion": "durability", "description": "316L medical surgical stainless steel specification verified by material testing standards.", "source_url": "https://millnmint.com/products/the-toothbrush", "verification_status": "verified"},
                    {"criterion": "repairability", "description": "Modular click-on replaceable cartridge head design eliminates whole-brush disposal.", "source_url": "https://millnmint.com/products/the-toothbrush", "verification_status": "verified"},
                    {"criterion": "packaging", "description": "Zero-plastic cardboard packaging.", "source_url": "https://millnmint.com/products/the-toothbrush", "verification_status": "verified"},
                ]
            },
            {
                "key": "vega_comb",
                "name": "Vega Round Plastic Hair Comb",
                "brand": "Vega",
                "category": "Personal Care",
                "description": "Conventional injection-molded polystyrene hair comb prone to snapping and static generation.",
                "price": 65.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1590159763121-7c9ff3149e0a?w=600&auto=format&fit=crop&q=80",
                "materials": "Molded polystyrene (plastic)",
                "purchase_url": "https://www.vega.co.in/grooming-accessories/hair-combs/dressing-combs.html",
                "source_verification_status": "manufacturer_info_only",
                "is_sustainable": False,
                "durability_score": 40,
                "packaging_score": 25,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "bamboobae_comb",
                "name": "The Bamboo Bae Detangling Neem Wood Comb",
                "brand": "The Bamboo Bae",
                "category": "Personal Care",
                "description": "Handcrafted Indian herbal comb made from pure seasoned medicinal neem wood with anti-static detangling wide teeth.",
                "price": 179.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&auto=format&fit=crop&q=80",
                "materials": "100% natural seasoned neem wood (Azadirachta indica), natural herbal oil coat",
                "purchase_url": "https://thebamboobae.com/products/detangling-neem-wood-comb-with-handle",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 85,
                "packaging_score": 90,
                "repairability_score": None,
                "evidence": [
                    {"criterion": "packaging", "description": "Brown kraft paper packaging; plastic-free sleeve.", "source_url": "https://thebamboobae.com/products/detangling-neem-wood-comb-with-handle", "verification_status": "manufacturer_reported"},
                ]
            },
            {
                "key": "gillette_razor",
                "name": "Gillette Presto Disposable Razor",
                "brand": "Gillette",
                "category": "Personal Care",
                "description": "Ultra-popular single-use twin blade disposable plastic razor with non-detachable cartridge.",
                "price": 25.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1599351431202-1e0f0137899a?w=600&auto=format&fit=crop&q=80",
                "materials": "Polystyrene plastic handle, embedded twin steel blades",
                "purchase_url": "https://www.gillette.co.in/en-in/products/razors-and-blades/disposable-razors/presto-readyshaver-disposable-razor",
                "source_verification_status": "manufacturer_info_only",
                "is_sustainable": False,
                "durability_score": 15,
                "packaging_score": 20,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "pearl_razor",
                "name": "Pearl Shaving L-55 Double Edge Safety Razor",
                "brand": "Pearl Shaving",
                "category": "Personal Care",
                "description": "All-metal mechanical safety razor crafted in Gujarat from solid brass with chrome finish for lifetime zero-waste shaving.",
                "price": 699.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1508746829417-e6f548d8d6ed?w=600&auto=format&fit=crop&q=80",
                "materials": "100% solid brass body, chrome plating, standard stainless steel razor blade",
                "purchase_url": "https://pearlshaving.in/product/l-55-close-comb-chrome/",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 95,
                "packaging_score": 85,
                "repairability_score": 90,
                "evidence": [
                    {"criterion": "durability", "description": "Solid brass precision-machined build verified for lifetime multi-decade durability.", "source_url": "https://pearlshaving.in/product/l-55-close-comb-chrome/", "verification_status": "verified"},
                    {"criterion": "repairability", "description": "3-piece disassemblable mechanical head uses universally recyclable double-edge stainless steel blades.", "source_url": "https://pearlshaving.in/product/l-55-close-comb-chrome/", "verification_status": "verified"},
                    {"criterion": "packaging", "description": "Cardboard gift box packaging with zero plastic shrink wrap.", "source_url": "https://pearlshaving.in/product/l-55-close-comb-chrome/", "verification_status": "verified"},
                ]
            },
            {
                "key": "headandshoulders_shampoo",
                "name": "Head & Shoulders Anti-Dandruff Liquid Shampoo",
                "brand": "Head & Shoulders",
                "category": "Personal Care",
                "description": "Mass-market liquid shampoo formulated with synthetic surfactants in an HDPE non-refillable plastic bottle.",
                "price": 175.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=600&auto=format&fit=crop&q=80",
                "materials": "High-density polyethylene (HDPE) bottle (#2), polypropylene flip cap (#5), liquid surfactant formulation",
                "purchase_url": "https://www.headandshoulders.co.in/en-in/shop-products/anti-dandruff-shampoo/smooth-and-silky-shampoo",
                "source_verification_status": "manufacturer_info_only",
                "is_sustainable": False,
                "durability_score": 50,
                "packaging_score": 35,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "rusticart_shampoobar",
                "name": "Rustic Art Amla Shikakai Organic Shampoo Bar",
                "brand": "Rustic Art",
                "category": "Personal Care",
                "description": "Certified organic, zero-waste solid hair cleanser made in Maharashtra using cold-process saponified plant oils and Ayurvedic herbs.",
                "price": 342.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1608248597359-5481d4512e23?w=600&auto=format&fit=crop&q=80",
                "materials": "Certified organic coconut & sesame oils, amla, shikakai, reetha; unbleached paper wrap",
                "purchase_url": "https://rusticart.in/product/amla-shikakai-shampoo-bar/",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 75,
                "packaging_score": 98,
                "repairability_score": None,
                "evidence": [
                    {"criterion": "packaging", "description": "100% post-consumer recycled paper box, zero plastic bottles.", "source_url": "https://rusticart.in/product/amla-shikakai-shampoo-bar/", "verification_status": "manufacturer_reported"},
                ]
            },

            # ══════════════════════════════════════════════════════
            # Kitchen & Home (6 products: 3 conventional, 3 sustainable)
            # ══════════════════════════════════════════════════════
            {
                "key": "bisleri_bottle",
                "name": "Bisleri 1L Packaged Drinking Water Bottle",
                "brand": "Bisleri",
                "category": "Kitchen & Home",
                "description": "Everyday single-use packaged drinking water in a disposable polyethylene terephthalate (PET) plastic bottle.",
                "price": 20.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=600&auto=format&fit=crop&q=80",
                "materials": "Polyethylene terephthalate (PET) bottle, HDPE cap, BOPP plastic label",
                "purchase_url": "https://www.bisleri.com/product/packaged-drinking-water-1-litre",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": False,
                "durability_score": 10,
                "packaging_score": 15,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "milton_bottle",
                "name": "Milton Duo DLX 1000ml Thermosteel Bottle",
                "brand": "Milton",
                "category": "Kitchen & Home",
                "description": "Double-walled vacuum insulated SUS 304 food-grade stainless steel bottle keeping beverages hot or cold for 24 hours.",
                "price": 750.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&auto=format&fit=crop&q=80",
                "materials": "Inner & outer SUS 304 food-grade 18/8 stainless steel, food-grade silicone ring",
                "purchase_url": "https://www.milton.in/products/duo-deluxe-thermosteel-water-bottle-1000-ml",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 95,
                "packaging_score": 80,
                "repairability_score": 80,
                "evidence": [
                    {"criterion": "durability", "description": "Certified SUS 304 (18/8) food-contact-grade stainless steel body with vacuum thermal seal.", "source_url": "https://www.milton.in/products/duo-deluxe-thermosteel-water-bottle-1000-ml", "verification_status": "verified"},
                    {"criterion": "repairability", "description": "Silicone gaskets and replacement caps are replaceable through Milton customer service.", "source_url": "https://www.milton.in/products/duo-deluxe-thermosteel-water-bottle-1000-ml", "verification_status": "verified"},
                    {"criterion": "packaging", "description": "Recyclable corrugated cardboard box.", "source_url": "https://www.milton.in/products/duo-deluxe-thermosteel-water-bottle-1000-ml", "verification_status": "verified"},
                ]
            },
            {
                "key": "signoraware_container",
                "name": "Signoraware Classic Plastic Food Container",
                "brand": "Signoraware",
                "category": "Kitchen & Home",
                "description": "Conventional plastic tiffin and food storage container made of virgin polypropylene.",
                "price": 120.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=600&auto=format&fit=crop&q=80",
                "materials": "Virgin polypropylene (PP) plastic body and clips",
                "purchase_url": "https://signoraware.com/collections/lunch-boxes",
                "source_verification_status": "manufacturer_info_only",
                "is_sustainable": False,
                "durability_score": 55,
                "packaging_score": 30,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "borosil_container",
                "name": "Borosil Klip N Store Glass Food Container",
                "brand": "Borosil",
                "category": "Kitchen & Home",
                "description": "100% pure borosilicate glass storage dish resistant to thermal shocks up to 400°C with airtight locking lid.",
                "price": 395.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1614735241165-6756e1df61ab?w=600&auto=format&fit=crop&q=80",
                "materials": "100% borosilicate glass vessel, BPA-free PP lid with removable food-grade silicone ring",
                "purchase_url": "https://myborosil.com/collections/klip-n-store-containers/products/klip-n-store-microwavable-glass-storage-containers-square",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 90,
                "packaging_score": 85,
                "repairability_score": 75,
                "evidence": [
                    {"criterion": "durability", "description": "100% borosilicate thermal shock tested up to 400 deg C; non-porous glass complies with food contact standards.", "source_url": "https://myborosil.com/collections/klip-n-store-containers/products/klip-n-store-microwavable-glass-storage-containers-square", "verification_status": "verified"},
                    {"criterion": "repairability", "description": "Lid clip assemblies and silicone seals can be replaced independently without discarding the glass base.", "source_url": "https://myborosil.com/collections/klip-n-store-containers/products/klip-n-store-microwavable-glass-storage-containers-square", "verification_status": "verified"},
                    {"criterion": "packaging", "description": "Corrugated unbleached recyclable protective carton.", "source_url": "https://myborosil.com/collections/klip-n-store-containers/products/klip-n-store-microwavable-glass-storage-containers-square", "verification_status": "verified"},
                ]
            },
            {
                "key": "scotchbrite_sponge",
                "name": "Scotch-Brite Heavy Duty Scrub Sponge",
                "brand": "Scotch-Brite",
                "category": "Kitchen & Home",
                "description": "Dual-action synthetic kitchen sponge combining polyurethane foam and nylon scouring abrasive.",
                "price": 25.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1585670270677-3acce32799d4?w=600&auto=format&fit=crop&q=80",
                "materials": "Polyurethane foam backing, nylon abrasive mesh",
                "purchase_url": "https://www.scotch-brite.com.in/3M/en_IN/scotch-brite-in/products/all-products/~/Scotch-Brite-Heavy-Duty-Scrub-Sponge/",
                "source_verification_status": "manufacturer_info_only",
                "is_sustainable": False,
                "durability_score": 30,
                "packaging_score": 20,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "bamboobae_scrub",
                "name": "The Bamboo Bae Natural Coconut Coir Dish Scrub",
                "brand": "The Bamboo Bae",
                "category": "Kitchen & Home",
                "description": "100% natural, biodegradable kitchen scrubber made from coconut husk coir fiber bound with natural rubber latex.",
                "price": 37.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=600&auto=format&fit=crop&q=80",
                "materials": "100% coconut coir fiber, natural rubber tree latex binder, cotton stitching",
                "purchase_url": "https://thebamboobae.com/products/coconut-coir-scrub-pad-pack-of-4",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 75,
                "packaging_score": 95,
                "repairability_score": None,
                "evidence": [
                    {"criterion": "packaging", "description": "Paper sleeve band packaging, zero plastic wrap.", "source_url": "https://thebamboobae.com/products/coconut-coir-scrub-pad-pack-of-4", "verification_status": "manufacturer_reported"},
                ]
            },

            # ══════════════════════════════════════════════════════
            # Clothing (4 products: 2 conventional, 2 sustainable)
            # ══════════════════════════════════════════════════════
            {
                "key": "fastfashion_tee",
                "name": "Fast Fashion Polyester-Blend T-Shirt",
                "brand": "Max Fashion",
                "category": "Clothing",
                "description": "Mass-produced blended crew-neck tee made from petroleum-derived virgin polyester and conventional cotton.",
                "price": 499.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600&auto=format&fit=crop&q=80",
                "materials": "65% virgin polyester, 35% conventional cotton with AZO dyes",
                "purchase_url": "https://www.maxfashion.in/in/en/department/maxmen-clothing-tops-tshirts",
                "source_verification_status": "retailer_source",
                "is_sustainable": False,
                "durability_score": 45,
                "packaging_score": 25,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "nonasties_tee",
                "name": "No Nasties Classic Organic Cotton T-Shirt",
                "brand": "No Nasties",
                "category": "Clothing",
                "description": "Fairtrade and GOTS certified 100% organic cotton classic t-shirt produced in Goa, India with zero toxic pesticides.",
                "price": 1499.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=600&auto=format&fit=crop&q=80",
                "materials": "100% GOTS certified organic fairtrade cotton, certified non-toxic organic dyes",
                "purchase_url": "https://www.nonasties.in/collections/mens-t-shirts/products/classic-organic-cotton-t-shirt",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 85,
                "packaging_score": 95,
                "repairability_score": 60,
                "evidence": [
                    {"criterion": "durability", "description": "GOTS (Global Organic Textile Standard) Certified Organic Cotton fabric verified.", "source_url": "https://www.nonasties.in/collections/mens-t-shirts/products/classic-organic-cotton-t-shirt", "verification_status": "verified"},
                    {"criterion": "repairability", "description": "Single-origin pure cotton weave supports standard textile mending and eventual mechanical circular recycling.", "source_url": "https://www.nonasties.in/collections/mens-t-shirts/products/classic-organic-cotton-t-shirt", "verification_status": "verified"},
                    {"criterion": "packaging", "description": "Reusable organic cotton drawstring cloth pouch packaging.", "source_url": "https://www.nonasties.in/collections/mens-t-shirts/products/classic-organic-cotton-t-shirt", "verification_status": "verified"},
                ]
            },
            {
                "key": "fastfashion_jeans",
                "name": "Fast Fashion Synthetic Stretch Denim Jeans",
                "brand": "Spykar",
                "category": "Clothing",
                "description": "Commercial stretch jeans containing petroleum-based elastane and polyester fibers that prevent circular recycling.",
                "price": 1499.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1542272604-780c96856592?w=600&auto=format&fit=crop&q=80",
                "materials": "78% conventional cotton, 20% polyester, 2% elastane",
                "purchase_url": "https://www.spykar.com/collections/men-jeans",
                "source_verification_status": "manufacturer_info_only",
                "is_sustainable": False,
                "durability_score": 60,
                "packaging_score": 30,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "doodlage_jeans",
                "name": "Doodlage Ember Upcycled Patchwork Denim Trousers",
                "brand": "Doodlage",
                "category": "Clothing",
                "description": "Designer conscious trousers reconstructed in New Delhi entirely from post-consumer and factory cut-waste denim remnants.",
                "price": 6750.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1582552938357-32b906df40cb?w=600&auto=format&fit=crop&q=80",
                "materials": "100% upcycled post-consumer & factory deadstock cotton denim",
                "purchase_url": "https://doodlage.in/products/ember-denim-panelled-pants",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 90,
                "packaging_score": 90,
                "repairability_score": 85,
                "evidence": [
                    {"criterion": "durability", "description": "Heavyweight upcycled denim with industrial bar-tack reinforced panelling.", "source_url": "https://doodlage.in/products/ember-denim-panelled-pants", "verification_status": "manufacturer_reported"},
                    {"criterion": "repairability", "description": "Patchwork assembly format is designed for continuous creative visible repair.", "source_url": "https://doodlage.in/products/ember-denim-panelled-pants", "verification_status": "manufacturer_reported"},
                ]
            },

            # ══════════════════════════════════════════════════════
            # Electronics & Accessories (6 products: 3 conventional, 3 sustainable)
            # ══════════════════════════════════════════════════════
            {
                "key": "generic_phonecase",
                "name": "Generic Clear TPU Silicone Phone Case",
                "brand": "Generic",
                "category": "Electronics & Accessories",
                "description": "Mass-produced clear protective smartphone case made from non-biodegradable thermoplastic polyurethane.",
                "price": 199.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=600&auto=format&fit=crop&q=80",
                "materials": "100% thermoplastic polyurethane (TPU) / petroleum silicone",
                "purchase_url": "https://www.amazon.in/dp/B09G96TFF7",
                "source_verification_status": "retailer_source",
                "is_sustainable": False,
                "durability_score": 45,
                "packaging_score": 15,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "agreenco_phonecase",
                "name": "A Green Co Wheat Straw Compostable Phone Case",
                "brand": "A Green Co",
                "category": "Electronics & Accessories",
                "description": "Certified shockproof case crafted from agricultural wheat straw residue and PBAT plant-based biopolymers.",
                "price": 749.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1586105251261-72a756497a11?w=600&auto=format&fit=crop&q=80",
                "materials": "70% PBAT biopolymer, 30% natural agricultural wheat straw fiber",
                "purchase_url": "https://brownliving.in/collections/eco-friendly-phone-cases/products/wheat-straw-phone-case",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 80,
                "packaging_score": 95,
                "repairability_score": None,
                "evidence": [
                    {"criterion": "packaging", "description": "100% recycled unbleached kraft paper packaging.", "source_url": "https://brownliving.in/collections/eco-friendly-phone-cases/products/wheat-straw-phone-case", "verification_status": "manufacturer_reported"},
                ]
            },
            {
                "key": "portronics_laptopstand",
                "name": "Portronics My Buddy K ABS Plastic Laptop Stand",
                "brand": "Portronics",
                "category": "Electronics & Accessories",
                "description": "Everyday foldable portable desk laptop stand molded from synthetic ABS plastic.",
                "price": 499.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&auto=format&fit=crop&q=80",
                "materials": "Virgin ABS plastic body with silicone friction pads",
                "purchase_url": "https://www.portronics.com/products/my-buddy-k",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": False,
                "durability_score": 60,
                "packaging_score": 40,
                "repairability_score": 20,
                "evidence": []
            },
            {
                "key": "bamboobae_laptopstand",
                "name": "The Bamboo Bae Ergonomic Natural Cork Laptop Stand",
                "brand": "The Bamboo Bae",
                "category": "Electronics & Accessories",
                "description": "Ergonomic desk riser harvested from natural Portuguese cork bark; naturally heat insulating and shock absorbing.",
                "price": 849.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=600&auto=format&fit=crop&q=80",
                "materials": "100% naturally harvested cork oak bark (renewable)",
                "purchase_url": "https://thebamboobae.com/products/cork-laptop-stand",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 85,
                "packaging_score": 90,
                "repairability_score": None,
                "evidence": [
                    {"criterion": "packaging", "description": "Plastic-free corrugated paper envelope.", "source_url": "https://thebamboobae.com/products/cork-laptop-stand", "verification_status": "manufacturer_reported"},
                ]
            },
            {
                "key": "duracell_batteries",
                "name": "Duracell Chota Power AA Alkaline Batteries",
                "brand": "Duracell",
                "category": "Electronics & Accessories",
                "description": "Single-use disposable alkaline AA batteries that create hazardous chemical landfill waste after single discharge.",
                "price": 160.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1619725002198-6a689b72f41d?w=600&auto=format&fit=crop&q=80",
                "materials": "Steel casing, zinc anode, manganese dioxide cathode, potassium hydroxide electrolyte",
                "purchase_url": "https://www.duracell.in/product/chota-power/",
                "source_verification_status": "manufacturer_info_only",
                "is_sustainable": False,
                "durability_score": 15,
                "packaging_score": 20,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "panasonic_eneloop",
                "name": "Panasonic Eneloop Rechargeable AA Ni-MH Batteries",
                "brand": "Panasonic",
                "category": "Electronics & Accessories",
                "description": "Pre-charged solar-powered rechargeable AA batteries engineered in Japan for up to 2,100 recharge cycles.",
                "price": 1299.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1585338107529-13afc5f02586?w=600&auto=format&fit=crop&q=80",
                "materials": "Nickel-metal hydride (Ni-MH) chemistry, steel casing, solar-precharged",
                "purchase_url": "https://panasonic.eneloop.com.in/products/eneloop-aa-4-pack.html",
                "source_verification_status": "manufacturer_info_only",
                "is_sustainable": True,
                "durability_score": 95,
                "packaging_score": 80,
                "repairability_score": 85,
                "evidence": [
                    {"criterion": "durability", "description": "JIS C8708 certified standard for 2,100 recharge-discharge life cycles.", "source_url": "https://panasonic.eneloop.com.in/products/eneloop-aa-4-pack.html", "verification_status": "verified"},
                    {"criterion": "repairability", "description": "Rechargeable electrochemical design replaces thousands of single-use disposable batteries.", "source_url": "https://panasonic.eneloop.com.in/products/eneloop-aa-4-pack.html", "verification_status": "verified"},
                    {"criterion": "packaging", "description": "Cardboard blister pack with recyclable PET insert.", "source_url": "https://panasonic.eneloop.com.in/products/eneloop-aa-4-pack.html", "verification_status": "verified"},
                ]
            },

            # ══════════════════════════════════════════════════════
            # Everyday Essentials (8 products: 4 conventional, 4 sustainable)
            # ══════════════════════════════════════════════════════
            {
                "key": "generic_plasticbag",
                "name": "Single-Use HDPE Plastic Carry Bag",
                "brand": "Generic",
                "category": "Everyday Essentials",
                "description": "Common disposable thin plastic carry bag distributed at retail stalls and street markets.",
                "price": 5.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1597484661643-2f5fef640dd1?w=600&auto=format&fit=crop&q=80",
                "materials": "Virgin high-density polyethylene (HDPE) thin film",
                "purchase_url": "https://cpcb.nic.in/plastic-waste-rules/",
                "source_verification_status": "unverified",
                "is_sustainable": False,
                "durability_score": 5,
                "packaging_score": 0,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "ecoright_tote",
                "name": "EcoRight Organic Cotton Canvas Zipper Tote Bag",
                "brand": "EcoRight",
                "category": "Everyday Essentials",
                "description": "Heavy-duty reusable grocery tote handcrafted in Ahmedabad from GOTS certified organic cotton canvas with zip closure.",
                "price": 699.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=600&auto=format&fit=crop&q=80",
                "materials": "100% GOTS certified organic cotton canvas (10 oz), metal zipper pull",
                "purchase_url": "https://ecoright.com/collections/tote-bags/products/large-zipper-canvas-tote-bag",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 92,
                "packaging_score": 95,
                "repairability_score": 80,
                "evidence": [
                    {"criterion": "durability", "description": "GOTS Certified 10oz organic cotton canvas, load-tested to 15kg with reinforced stitching.", "source_url": "https://ecoright.com/collections/tote-bags/products/large-zipper-canvas-tote-bag", "verification_status": "verified"},
                    {"criterion": "packaging", "description": "Shipped in certified biodegradable cornstarch mailer.", "source_url": "https://ecoright.com/collections/tote-bags/products/large-zipper-canvas-tote-bag", "verification_status": "verified"},
                    {"criterion": "repairability", "description": "100% woven cotton material can be patched, re-sewn, and dyed over multi-year life.", "source_url": "https://ecoright.com/collections/tote-bags/products/large-zipper-canvas-tote-bag", "verification_status": "verified"},
                ]
            },
            {
                "key": "reynolds_pen",
                "name": "Reynolds 045 Fine Carbure Ballpoint Pen",
                "brand": "Reynolds",
                "category": "Everyday Essentials",
                "description": "Standard disposable ballpoint pen with non-refillable ink reservoir and plastic barrel.",
                "price": 10.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=600&auto=format&fit=crop&q=80",
                "materials": "Polystyrene transparent barrel, polypropylene plug & cap",
                "purchase_url": "https://www.reynolds-pens.com/product/045-carbure/",
                "source_verification_status": "manufacturer_info_only",
                "is_sustainable": False,
                "durability_score": 25,
                "packaging_score": 25,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "bioq_pen",
                "name": "BioQ Plantable Recycled Paper Seed Pens",
                "brand": "BioQ",
                "category": "Everyday Essentials",
                "description": "Eco-friendly pen barrel made from 100% recycled paper embedded with a non-GMO herb seed capsule at the bottom.",
                "price": 25.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1585336261026-66f916698dc9?w=600&auto=format&fit=crop&q=80",
                "materials": "100% post-consumer recycled kraft paper barrel, water-soluble seed capsule",
                "purchase_url": "https://bioq.in/products/plantable-pens-pack-of-5",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 70,
                "packaging_score": 95,
                "repairability_score": None,
                "evidence": [
                    {"criterion": "packaging", "description": "100% recycled paperboard packaging.", "source_url": "https://bioq.in/products/plantable-pens-pack-of-5", "verification_status": "manufacturer_reported"},
                ]
            },
            {
                "key": "dettol_handwash",
                "name": "Dettol Original Liquid Handwash Pump Bottle",
                "brand": "Dettol",
                "category": "Everyday Essentials",
                "description": "Common liquid antibacterial handwash in single-use HDPE plastic bottle with spring pump.",
                "price": 99.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&auto=format&fit=crop&q=80",
                "materials": "High-density polyethylene (HDPE) bottle, mixed plastic-metal spring pump",
                "purchase_url": "https://www.dettol.co.in/products/hand-wash/dettol-original-liquid-handwash/",
                "source_verification_status": "manufacturer_info_only",
                "is_sustainable": False,
                "durability_score": 40,
                "packaging_score": 30,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "godrej_magic_handwash",
                "name": "Godrej Magic Protekt Powder-to-Liquid Handwash",
                "brand": "Godrej Protekt",
                "category": "Everyday Essentials",
                "description": "Zero-waste refill system where a 9g powder sachet dissolves into 200ml liquid handwash inside a permanent dispenser bottle.",
                "price": 40.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1608248597359-5481d4512e23?w=600&auto=format&fit=crop&q=80",
                "materials": "Permanent reusable PET bottle, concentrated powder sachet",
                "purchase_url": "https://godrejprotekt.com/product/godrej-magic-powder-to-liquid-handwash/",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 85,
                "packaging_score": 85,
                "repairability_score": 80,
                "evidence": [
                    {"criterion": "repairability", "description": "Modular powder sachet refills extend bottle system lifecycle indefinitely.", "source_url": "https://godrejprotekt.com/product/godrej-magic-powder-to-liquid-handwash/", "verification_status": "manufacturer_reported"},
                ]
            },
            {
                "key": "generic_trashbags",
                "name": "Generic Virgin Plastic Black Garbage Bags",
                "brand": "Generic",
                "category": "Everyday Essentials",
                "description": "Non-biodegradable virgin low-density polyethylene black trash bags that persist in landfills for centuries.",
                "price": 150.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1618477461853-cf6ed80faba5?w=600&auto=format&fit=crop&q=80",
                "materials": "100% virgin low-density polyethylene (LDPE)",
                "purchase_url": "https://cpcb.nic.in/plastic-waste-rules/",
                "source_verification_status": "unverified",
                "is_sustainable": False,
                "durability_score": 20,
                "packaging_score": 10,
                "repairability_score": None,
                "evidence": []
            },
            {
                "key": "beco_trashbags",
                "name": "Beco 100% Compostable Cornstarch Garbage Bags",
                "brand": "Beco",
                "category": "Everyday Essentials",
                "description": "Certified plant-based compostable garbage bags made in Mumbai from cornstarch and natural plant polymers.",
                "price": 180.00,
                "currency": "INR",
                "image_url": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=600&auto=format&fit=crop&q=80",
                "materials": "Cornstarch extract and biodegradable polyesters (PBAT/PLA)",
                "purchase_url": "https://letsbeco.com/products/compostable-garbage-bags-medium-30-bags",
                "source_verification_status": "verified_exact_source",
                "is_sustainable": True,
                "durability_score": 70,
                "packaging_score": 95,
                "repairability_score": None,
                "evidence": [
                    {"criterion": "durability", "description": "Certified compostable under ISO 17088 and approved by Central Pollution Control Board (CPCB) India.", "source_url": "https://letsbeco.com/products/compostable-garbage-bags-medium-30-bags", "verification_status": "verified"},
                    {"criterion": "packaging", "description": "Recycled cardboard core roll and outer paper wrap.", "source_url": "https://letsbeco.com/products/compostable-garbage-bags-medium-30-bags", "verification_status": "verified"},
                ]
            },
        ]

        # Insert or update products
        product_map = {}
        for pdata in products_data:
            cat = cat_map[pdata["category"]]
            prod = db.query(Product).filter(Product.name == pdata["name"]).first()
            if not prod:
                prod = Product(
                    name=pdata["name"],
                    brand=pdata["brand"],
                    category_id=cat.id,
                    description=pdata["description"],
                    price=pdata["price"],
                    currency=pdata["currency"],
                    image_url=pdata["image_url"],
                    materials=pdata["materials"],
                    purchase_url=pdata["purchase_url"],
                    source_verification_status=pdata["source_verification_status"],
                    is_sustainable=pdata["is_sustainable"],
                    durability_score=pdata["durability_score"],
                    packaging_score=pdata["packaging_score"],
                    repairability_score=pdata["repairability_score"]
                )
                db.add(prod)
                db.flush()
            else:
                prod.brand = pdata["brand"]
                prod.category_id = cat.id
                prod.description = pdata["description"]
                prod.price = pdata["price"]
                prod.currency = pdata["currency"]
                prod.image_url = pdata["image_url"]
                prod.materials = pdata["materials"]
                prod.purchase_url = pdata["purchase_url"]
                prod.source_verification_status = pdata["source_verification_status"]
                prod.is_sustainable = pdata["is_sustainable"]
                prod.durability_score = pdata["durability_score"]
                prod.packaging_score = pdata["packaging_score"]
                prod.repairability_score = pdata["repairability_score"]

            product_map[pdata["key"]] = prod

            # Clear old evidence for product and insert audited evidence records
            db.query(SustainabilityEvidence).filter(SustainabilityEvidence.product_id == prod.id).delete()
            for ev in pdata.get("evidence", []):
                db.add(SustainabilityEvidence(
                    product_id=prod.id,
                    criterion=ev["criterion"],
                    source_url=ev["source_url"],
                    description=ev["description"],
                    verification_status=ev.get("verification_status", "verified")
                ))

        db.commit()

        # 3. Product Replacement Relationships
        replacements_data = [
            {
                "orig": "colgate_toothbrush",
                "rep": "bamboo_toothbrush",
                "type": "composition_change",
                "reason": "Replaces petroleum virgin plastic with sustainably farmed natural bamboo, reducing plastic handle footprint.",
                "main_change": "Handle material changed from virgin polypropylene to biodegradable Indian Moso bamboo.",
                "limitations": "Nylon-6 bristles still require removal before composting; bamboo handle must dry between uses."
            },
            {
                "orig": "colgate_toothbrush",
                "rep": "millnmint_toothbrush",
                "type": "design_change",
                "reason": "Transitions from whole-brush disposal to a lifetime surgical steel handle where only small bristle heads are swapped.",
                "main_change": "Modular 316L medical stainless steel handle with replaceable click-on TPE heads, cutting plastic waste by 8x.",
                "limitations": "Higher initial purchase cost (₹1,210); requires specific brand refill heads."
            },
            {
                "orig": "vega_comb",
                "rep": "bamboobae_comb",
                "type": "composition_change",
                "reason": "Replaces static-inducing, brittle polystyrene with seasoned Indian medicinal neem wood.",
                "main_change": "Material switched from molded polystyrene plastic to handcrafted natural neem wood.",
                "limitations": "Wooden combs should not be soaked in water or kept wet for prolonged periods."
            },
            {
                "orig": "gillette_razor",
                "rep": "pearl_razor",
                "type": "design_change",
                "reason": "Eliminates multi-component plastic cartridge waste with a solid metal razor using recyclable steel blades.",
                "main_change": "Single-piece plastic construction upgraded to durable solid brass with universally available double-edge blades.",
                "limitations": "Requires careful shaving technique without applying heavy pressure; careful blade handling required."
            },
            {
                "orig": "headandshoulders_shampoo",
                "rep": "rusticart_shampoobar",
                "type": "entire_product_replacement",
                "reason": "Completely eliminates rigid plastic shampoo bottle waste and shipping water weight using a solid herbal bar.",
                "main_change": "Formulation format transformed from liquid shampoo in an HDPE bottle to waterless solid bar in paper.",
                "limitations": "Must be kept in a well-drained soap dish to avoid melting; hair may experience a brief transition period."
            },
            {
                "orig": "bisleri_bottle",
                "rep": "milton_bottle",
                "type": "entire_product_replacement",
                "reason": "Replaces single-use disposable PET plastic bottles with a lifetime durable double-walled thermal flask.",
                "main_change": "Thin single-use PET plastic replaced with food-grade SUS 304 double-walled stainless steel.",
                "limitations": "Heavier carrying weight (approx 450g empty); requires manual daily cleaning."
            },
            {
                "orig": "signoraware_container",
                "rep": "borosil_container",
                "type": "composition_change",
                "reason": "Prevents microplastic and chemical leaching into warm food with 100% pure inert borosilicate glass.",
                "main_change": "Container vessel changed from petroleum polypropylene plastic to thermal shock-resistant borosilicate glass.",
                "limitations": "Heavier than plastic containers and subject to breakage if dropped onto stone surfaces."
            },
            {
                "orig": "scotchbrite_sponge",
                "rep": "bamboobae_scrub",
                "type": "composition_change",
                "reason": "Halts drain microplastic shedding from synthetic sponges by utilizing natural coconut husk coir.",
                "main_change": "Synthetic polyurethane foam replaced with 100% biodegradable coconut coir fiber bound with natural latex.",
                "limitations": "Slightly firmer feel when dry until soaked in warm water."
            },
            {
                "orig": "fastfashion_tee",
                "rep": "nonasties_tee",
                "type": "composition_change",
                "reason": "Eliminates non-biodegradable synthetic polyester and toxic chemical dyes with certified organic cotton.",
                "main_change": "Material switched from 65% polyester / 35% conventional cotton to 100% GOTS certified organic fairtrade cotton.",
                "limitations": "Higher retail price point reflecting ethical fair wages and chemical-free agriculture."
            },
            {
                "orig": "fastfashion_jeans",
                "rep": "doodlage_jeans",
                "type": "entire_product_replacement",
                "reason": "Diverts textile cut-waste and discarded denim from Indian landfills into durable circular designer trousers.",
                "main_change": "Virgin cotton-elastane fabric replaced with 100% post-consumer and factory cut-waste denim remnants.",
                "limitations": "Artisanal designer pricing; unique patchwork variations between individual garments."
            },
            {
                "orig": "generic_phonecase",
                "rep": "agreenco_phonecase",
                "type": "composition_change",
                "reason": "Replaces non-biodegradable yellowing TPU with agricultural wheat straw and plant-based biopolymers.",
                "main_change": "Material changed from synthetic petroleum TPU to agricultural wheat straw fiber and PBAT biopolymer.",
                "limitations": "Matte speckled appearance rather than crystal clear transparency; composts best in industrial facilities."
            },
            {
                "orig": "portronics_laptopstand",
                "rep": "bamboobae_laptopstand",
                "type": "composition_change",
                "reason": "Replaces brittle virgin petroleum ABS plastic with renewable, shock-absorbing harvested cork oak bark.",
                "main_change": "Molded ABS plastic replaced with 100% harvested natural cork oak bark.",
                "limitations": "Fixed ergonomic incline rather than multi-stage mechanical angle adjustments."
            },
            {
                "orig": "duracell_batteries",
                "rep": "panasonic_eneloop",
                "type": "design_change",
                "reason": "Eliminates disposable hazardous battery waste by offering cells that recharge up to 2,100 times.",
                "main_change": "Single-use zinc-alkaline chemistry replaced with solar-precharged reusable Ni-MH chemistry.",
                "limitations": "Requires dedicated Ni-MH battery charger; higher initial purchase price."
            },
            {
                "orig": "generic_plasticbag",
                "rep": "ecoright_tote",
                "type": "entire_product_replacement",
                "reason": "Eliminates hundreds of flimsy single-use plastic carry bags each year with a washable organic cotton canvas tote.",
                "main_change": "Single-use thin HDPE film replaced with durable 10oz GOTS certified organic cotton canvas.",
                "limitations": "Must be remembered and brought along when leaving home; requires occasional washing."
            },
            {
                "orig": "reynolds_pen",
                "rep": "bioq_pen",
                "type": "composition_change",
                "reason": "Replaces disposable plastic pen barrels with recycled paper containing non-GMO seeds that sprout after use.",
                "main_change": "Virgin polystyrene barrel replaced with 100% post-consumer recycled paper and water-soluble seed capsule.",
                "limitations": "Thin internal refill reservoir is still plastic; paper barrel should be kept dry until planting."
            },
            {
                "orig": "dettol_handwash",
                "rep": "godrej_magic_handwash",
                "type": "design_change",
                "reason": "Reduces plastic bottle waste and shipping carbon emissions by shipping 9g concentrated powder refills.",
                "main_change": "Disposal of single-use bottles replaced with a reusable permanent dispenser bottle and 9g powder refill sachets.",
                "limitations": "Requires user to add water and shake for 5 minutes to dissolve powder."
            },
            {
                "orig": "generic_trashbags",
                "rep": "beco_trashbags",
                "type": "composition_change",
                "reason": "Replaces petroleum plastic garbage bags that remain in landfills with certified compostable cornstarch bags.",
                "main_change": "Virgin petroleum LDPE replaced with natural cornstarch extract and biodegradable polyesters.",
                "limitations": "Less puncture resistant against sharp metallic items; best suited for wet organic kitchen waste."
            },
        ]

        for rdata in replacements_data:
            orig_prod = product_map.get(rdata["orig"])
            rep_prod = product_map.get(rdata["rep"])
            if orig_prod and rep_prod:
                existing_rel = db.query(ProductReplacement).filter(
                    ProductReplacement.original_product_id == orig_prod.id,
                    ProductReplacement.replacement_product_id == rep_prod.id
                ).first()
                if not existing_rel:
                    db.add(ProductReplacement(
                        original_product_id=orig_prod.id,
                        replacement_product_id=rep_prod.id,
                        replacement_type=rdata["type"],
                        reason=rdata["reason"],
                        main_change=rdata["main_change"],
                        known_limitations=rdata.get("limitations")
                    ))
                else:
                    existing_rel.replacement_type = rdata["type"]
                    existing_rel.reason = rdata["reason"]
                    existing_rel.main_change = rdata["main_change"]
                    existing_rel.known_limitations = rdata.get("limitations")

        db.commit()

        # Audit tally
        exact_count = sum(1 for p in products_data if p["source_verification_status"] == "verified_exact_source")
        mfg_count = sum(1 for p in products_data if p["source_verification_status"] == "manufacturer_info_only")
        retailer_count = sum(1 for p in products_data if p["source_verification_status"] == "retailer_source")
        unverified_count = sum(1 for p in products_data if p["source_verification_status"] == "unverified")

        print("=== GreenCart Seed Audit Summary ===")
        print(f"Total Products: {len(products_data)}")
        print(f"- Verified exact product sources: {exact_count}")
        print(f"- Manufacturer information sources only: {mfg_count}")
        print(f"- Retailer sources: {retailer_count}")
        print(f"- Unverified commodity sources: {unverified_count}")
        print(f"Replacement Relationships: {len(replacements_data)}")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
