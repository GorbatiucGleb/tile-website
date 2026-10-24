"""Builds one page per service under services/<slug>/index.html for the Custom Tile Interiors site.
Header, footer and styles match the homepage. Run: python build_service_pages.py <site folder>"""
import json, os, sys, html
from PIL import Image

SITE = sys.argv[1]
BASE = "https://customtileinteriorsmn.com"
V_CSS, V_JS = "37", "37"

def size(img):
    with Image.open(os.path.join(SITE, "images", img)) as im:
        return im.size

SERVICES = [
  dict(slug="custom-showers", name="Large-Format Custom Showers", short="Custom Showers",
    title="Custom Tile Showers in the Twin Cities | Custom Tile Interiors",
    desc="Large-format custom tile showers across Minneapolis, St. Paul and the Twin Cities: walk-in showers, niches, benches and mitered edges. Free quotes: 612-991-7000.",
    h1="Large-format custom showers",
    lead="Walk-in showers built around large-format tile and slabs, for a clean, modern look with fewer grout lines. Planned and installed by hand across the Twin Cities.",
    sections=[
      ("What's included", [
        "A tile layout planned around your space, so cuts land in the right places and the pattern lines up across every wall.",
        "Large-format tile and porcelain slabs, plus mosaics, zellige-style and subway tile for accent walls and floors.",
        "Recessed niches and floating benches built into the tile, with clean, mitered corners instead of metal trim.",
        "Shower floors, curbs and linear drains finished to match the walls.",
      ]),
      ("Why large-format tile", [
        "Bigger tiles mean fewer grout lines, so the shower looks calmer and is easier to keep clean.",
        "Marble-look and onyx-look slabs give the feel of natural stone, and we carry the veining around corners so it looks like one solid piece.",
      ]),
    ],
    faq=[
      ("Can you build a niche or bench into the shower?", "Yes. Niches and floating benches are built in as part of the tile work and finished with mitered edges so they match the rest of the shower."),
      ("Do you work with large porcelain slabs?", "Yes, from large-format tile to full porcelain slabs, including marble-look and onyx-look designs."),
      ("How do I get a price?", "Send a few details through the free quote form or call 612-991-7000. Every shower is different, so we quote each project individually."),
    ],
    photos=["shower-porcelain-slabs.jpg", "shower-onyx-slab.jpg", "shower-green-tile.jpg", "shower-marble-oversized.jpg",
            "shower-charcoal-herringbone.jpg", "shower-sage-vertical-tile.jpg", "shower-marble-look.jpg", "shower-niche-floating-bench.jpg",
            "shower-zellige-cream.jpg", "shower-white-tile-window.jpg", "shower-marble-subway-black.jpg", "shower-blue-subway-ledge.jpg"],
    project="Custom shower"),
  dict(slug="steam-showers", name="Steam Showers", short="Steam Showers",
    title="Steam Shower Tile Installation in the Twin Cities | Custom Tile Interiors",
    desc="Tiled steam showers and spa bathrooms across Minneapolis, St. Paul and the Twin Cities. Fully enclosed, carefully detailed tile work. Free quotes: 612-991-7000.",
    h1="Steam showers",
    lead="Fully enclosed, tiled steam showers that turn a bathroom into a spa. Careful tile work on walls, ceilings, benches and floors, across the Twin Cities.",
    sections=[
      ("What's included", [
        "Tile on every surface inside the steam enclosure, including walls, benches and floor.",
        "Built-in benches and niches, finished with clean mitered edges.",
        "A layout planned so the tile pattern flows continuously around the space.",
      ]),
      ("Planning a steam shower", [
        "Steam showers need more planning than a regular shower, so we talk through the layout, tile choice and details with you before work starts.",
        "Large-format tile and slabs are a popular choice because fewer grout lines means a cleaner look and less to maintain.",
      ]),
    ],
    faq=[
      ("Can you add a bench to a steam shower?", "Yes. A built-in tile bench is one of the most popular steam shower features, and we finish it to match the walls."),
      ("What tile works best?", "Porcelain and large-format tile are common choices. We'll help you pick a tile that fits the look you want."),
      ("How do I get a price?", "Use the free quote form or call 612-991-7000 and tell us about your bathroom."),
    ],
    photos=["wet-room-tub-shower.jpg", "sauna-shower-room.jpg", "shower-onyx-slab.jpg", "shower-porcelain-slabs.jpg", "bathroom-moody-warm.jpg"],
    project="Steam shower"),
  dict(slug="backsplashes", name="Tile Backsplashes", short="Backsplashes",
    title="Kitchen & Bar Tile Backsplashes in the Twin Cities | Custom Tile Interiors",
    desc="Kitchen and bar tile backsplash installation across Minneapolis, St. Paul and the Twin Cities: subway, zellige, arabesque, mosaic and range hood tile. Free quotes: 612-991-7000.",
    h1="Kitchen & bar backsplashes",
    lead="Tile backsplashes for kitchens, wet bars and range walls, from classic subway to glossy handmade-look tile and mosaics.",
    sections=[
      ("What we install", [
        "Kitchen backsplashes around counters, windows and range walls.",
        "Floor-to-ceiling tile behind range hoods for a bold focal point.",
        "Wet bars and kitchenettes with mosaic, arabesque or glossy tile and floating shelves.",
      ]),
      ("The details that matter", [
        "Careful layout around outlets, windows and cabinets, so cuts are even and nothing looks squeezed.",
        "Clean edges where the tile ends, so the backsplash looks finished from every angle.",
      ]),
    ],
    faq=[
      ("What kinds of tile can you install?", "Subway, handmade-look and zellige-style tile, arabesque, mosaic, brick-style and more."),
      ("Can you tile all the way up behind a range hood?", "Yes. A full-height tiled range wall is a great way to make the kitchen stand out."),
      ("How do I get a price?", "Use the free quote form or call 612-991-7000 with your kitchen size and the tile you're considering."),
    ],
    photos=["kitchen-backsplash.jpg", "kitchen-green-backsplash.jpg", "bar-arabesque-backsplash.jpg", "kitchen-tile-range-hood.jpg",
            "kitchen-subway-backsplash.jpg", "basement-bar.jpg", "mosaic-wall-shelves.jpg"],
    project="Backsplash"),
  dict(slug="tile-floors", name="Tile Floors", short="Tile Floors",
    title="Tile Floor Installation in the Twin Cities | Custom Tile Interiors",
    desc="Tile floor installation across Minneapolis, St. Paul and the Twin Cities: large-format, marble-look, patterned and mosaic tile for bathrooms, kitchens and entryways. Free quotes: 612-991-7000.",
    h1="Tile floors",
    lead="Durable, level tile floors for bathrooms, kitchens, entryways and basements, from large polished porcelain to patterned and mosaic tile.",
    sections=[
      ("What we install", [
        "Large-format and polished marble-look porcelain floors.",
        "Patterned tile for entryways and mudrooms.",
        "Mosaic and herringbone accents, like a mosaic \"rug\" under a freestanding tub.",
      ]),
      ("Built to last", [
        "A flat, level floor starts with careful prep and layout, so large tiles sit evenly and grout lines stay straight.",
        "Tile floors can be paired with in-floor heating for warm floors all winter.",
      ]),
    ],
    faq=[
      ("Can you install large-format floor tile?", "Yes. Large-format porcelain is one of our specialties, for bathrooms and open living areas alike."),
      ("Can you add heated floors at the same time?", "Yes. Heated floors are installed under the tile, so it's best to plan them together. See our heated floors page."),
      ("How do I get a price?", "Use the free quote form or call 612-991-7000 with the room size and tile you have in mind."),
    ],
    photos=["floor-large-format.jpg", "bathroom-marble-floor-herringbone.jpg", "floor-patterned-entry.jpg", "bathroom-tub-mosaic.jpg", "bathroom-tub-shower.jpg"],
    project="Tile floor"),
  dict(slug="heated-floors", name="Heated Tile Floors", short="Heated Floors",
    title="Heated Tile Floor Installation in the Twin Cities | Custom Tile Interiors",
    desc="In-floor heating installed under new tile floors across Minneapolis, St. Paul and the Twin Cities. Warm bathroom and kitchen floors for Minnesota winters. Free quotes: 612-991-7000.",
    h1="Heated tile floors",
    lead="In-floor heating installed under your new tile, made for Minnesota winters. Warm floors in bathrooms, kitchens and basements.",
    sections=[
      ("How it works", [
        "Heating cables are laid in a membrane on the subfloor before any tile goes down, as you can see in the photos below.",
        "The tile is then installed right on top, so the heat warms the floor evenly.",
        "It's controlled by a thermostat on the wall.",
      ]),
      ("When to add it", [
        "Heated floors go under the tile, so the best time to add them is when new tile is going in.",
        "They're popular in bathrooms, kitchens and basements, where tile can feel cold in winter.",
      ]),
    ],
    faq=[
      ("Can heated floors be added under existing tile?", "No. The heating goes under the tile, so it's installed when the floor is being tiled."),
      ("Which rooms are best for heated floors?", "Bathrooms are the most popular, but kitchens, entryways and basements work well too."),
      ("How do I get a price?", "Use the free quote form or call 612-991-7000 and mention you'd like heated floors."),
    ],
    photos=["heated-floor-install.jpg", "heated-floor-install-2.jpg", "floor-large-format.jpg", "bathroom-marble-floor-herringbone.jpg"],
    project="Heated floor"),
  dict(slug="fireplaces", name="Tile Fireplaces", short="Fireplaces",
    title="Tile Fireplace Surrounds in the Twin Cities | Custom Tile Interiors",
    desc="Tile fireplace surrounds and floor-to-ceiling feature walls across Minneapolis, St. Paul and the Twin Cities. Free quotes: 612-991-7000.",
    h1="Tile fireplaces",
    lead="Tile fireplace surrounds and feature walls that become the centerpiece of the room, from a simple surround to a floor-to-ceiling statement wall.",
    sections=[
      ("What we install", [
        "Tile surrounds around gas and electric fireplaces.",
        "Floor-to-ceiling feature walls, including fluted and textured tile.",
        "Clean, mitered outside corners on fireplace bump-outs, so the tile wraps the corner without metal trim.",
      ]),
      ("Planning your fireplace", [
        "Tall feature walls need a careful layout so the pattern stays straight from floor to ceiling and lines up around the mantel and firebox.",
      ]),
    ],
    faq=[
      ("Can you tile a full floor-to-ceiling fireplace wall?", "Yes. Full-height fireplace walls are one of the most dramatic ways to use tile."),
      ("Do you install the mantel?", "We focus on the tile work and can plan around the mantel you choose. Ask us about your project."),
      ("How do I get a price?", "Use the free quote form or call 612-991-7000 with the size of the wall and the tile you like."),
    ],
    photos=["fireplace-fluted-tile-full.jpg"],
    project="Fireplace"),
  dict(slug="mitered-edges", name="Mitered Tile Edges", short="Mitered Edges",
    title="Mitered Tile Edges, No Metal Trim | Custom Tile Interiors, Twin Cities",
    desc="Precise 45° mitered tile edges with color-matched epoxy and continuous veining, instead of metal or plastic trim. Twin Cities tile contractor. Free quotes: 612-991-7000.",
    h1="Mitered edges, no metal trim",
    lead="The detail that sets high-end tile work apart: corners where two tiles meet in one clean edge, like a solid piece of stone.",
    sections=[
      ("How it's done", [
        "Each tile is cut at a precise 45° angle, so two pieces meet at the corner in one clean edge.",
        "The pieces are joined and the seam is filled with color-matched epoxy.",
        "On marble-look tile, the veining is carried right through the joint, so the pattern flows around the corner without a break.",
      ]),
      ("Where we use it", [
        "Shower niches, curbs and benches.",
        "Outside corners on walls, fireplaces and half walls.",
        "Corner shelves and window returns.",
      ]),
      ("Why it's better than trim", [
        "No plastic or metal strips, just the tile itself, for a seamless, built-in look.",
        "It takes more time and skill than trim, which is why you mostly see it on high-end work.",
      ]),
    ],
    faq=[
      ("Is a mitered edge as durable as trim?", "Yes. The joint is bonded and filled with epoxy, so it's solid and finished."),
      ("Can you miter marble-look tile so the veining lines up?", "Yes. We carry the veining through the epoxy so the pattern continues around the corner."),
      ("How do I get a price?", "Use the free quote form or call 612-991-7000. Mitered edges can be part of any shower, niche, fireplace or wall project."),
    ],
    photos=["mitered-corner-shelf.jpg", "shower-marble-look.jpg", "shower-niche-floating-bench.jpg", "shower-porcelain-slabs.jpg"],
    project="Other"),
]

SHARDS = None  # copied from the homepage so the logo C shatters on every page

def logo_html():
    global SHARDS
    if SHARDS is None:
        home = open(os.path.join(SITE, "index.html")).read()
        start = home.index('<span class="brand-c"')
        SHARDS = home[start:home.index("</span>", start) + len("</span>")]
    return SHARDS

def page(svc):
    url = f"{BASE}/services/{svc['slug']}/"
    first = svc["photos"][0]
    others = [s for s in SERVICES if s["slug"] != svc["slug"]]
    e = html.escape

    sections = "".join(
        f'''        <section class="svc-block">
          <h2>{e(h)}</h2>
          <ul class="svc-list">
{''.join(f"            <li>{e(item)}</li>{chr(10)}" for item in items)}          </ul>
        </section>
''' for h, items in svc["sections"])

    photos = "".join(
        f'          <figure><img src="/images/{p}" width="{size(p)[0]}" height="{size(p)[1]}" alt="{e(svc["name"])} by Custom Tile Interiors" loading="lazy"></figure>\n'
        for p in svc["photos"])

    faq = "".join(
        f'''          <details class="faq-item">
            <summary>{e(q)}</summary>
            <p>{e(a)}</p>
          </details>
''' for q, a in svc["faq"])

    more = "".join(f'          <a href="/services/{o["slug"]}/">{e(o["short"])}</a>\n' for o in others)

    ld = [
      {"@context": "https://schema.org", "@type": "Service", "name": svc["name"], "serviceType": svc["name"],
       "description": svc["desc"], "url": url,
       "provider": {"@type": "HomeAndConstructionBusiness", "@id": f"{BASE}/#business", "name": "Custom Tile Interiors",
                    "telephone": "+1-612-991-7000", "url": f"{BASE}/"},
       "areaServed": {"@type": "Place", "name": "Twin Cities metro, Minnesota"},
       "image": f"{BASE}/images/{first}"},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{BASE}/#services"},
        {"@type": "ListItem", "position": 3, "name": svc["short"], "item": url}]},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in svc["faq"]]},
    ]

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="{url}">
  <title>{e(svc["title"])}</title>
  <meta name="description" content="{e(svc["desc"])}">
  <link rel="icon" href="/images/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
  <meta name="theme-color" content="#ffffff">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(svc["title"])}">
  <meta property="og:description" content="{e(svc["desc"])}">
  <meta property="og:image" content="{BASE}/images/{first}">
  <meta property="og:url" content="{url}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Montserrat:wght@500;600&family=Inter:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css?v={V_CSS}">
  <!-- Business and page details for Google (not shown on the page) -->
  <script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
  </script>
</head>
<body class="svc-page">
  <!-- This page is made by build_service_pages.py. Edit tools/build_service_pages.py, not this file. -->

  <div class="top-bar">
    <div class="container top-bar-inner">
      <span>Serving the Twin Cities, Minnesota</span>
      <a href="tel:+16129917000">612-991-7000</a>
    </div>
  </div>

  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="brand" aria-label="Custom Tile Interiors home">
        <img src="/images/logo-light-text.png" alt="Custom Tile Interiors logo" width="336" height="238">
        {logo_html().replace('url("images/', 'url("/images/')}
      </a>
      <nav class="nav" aria-label="Main">
        <a href="/#services">Services</a>
        <a href="/#work">Our Work</a>
        <a href="/#reviews">Reviews</a>
        <a href="/#about">About</a>
        <a href="/#quote" class="btn btn-solid">Free Quote</a>
      </nav>
    </div>
    <nav class="nav-mobile" aria-label="Main">
      <a href="/#services">Services</a>
      <a href="/#work">Our Work</a>
      <a href="/#reviews">Reviews</a>
      <a href="/#about">About</a>
    </nav>
  </header>

  <main>
    <section class="svc-hero">
      <div class="container narrow">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span>›</span> <a href="/#services">Services</a> <span>›</span> <span aria-current="page">{e(svc["short"])}</span></nav>
        <p class="label">Twin Cities, MN</p>
        <h1>{e(svc["h1"])}</h1>
        <p class="svc-lead">{e(svc["lead"])}</p>
        <div class="svc-actions">
          <a href="/#quote" class="btn btn-solid">Get a Free Quote</a>
          <a href="tel:+16129917000" class="btn btn-outline">Call 612-991-7000</a>
        </div>
      </div>
    </section>

    <section class="section svc-body">
      <div class="container narrow">
{sections}      </div>
    </section>

    <section class="section section-stone">
      <div class="container">
        <div class="section-head">
          <p class="label">Our work</p>
          <h2>{e(svc["short"])} we've done</h2>
        </div>
        <div class="gallery{' gallery-solo' if len(svc['photos']) == 1 else ''}">
{photos}        </div>
      </div>
    </section>

    <section class="section">
      <div class="container narrow">
        <div class="section-head">
          <p class="label">Questions</p>
          <h2>Common questions</h2>
        </div>
        <div class="faq">
{faq}        </div>
      </div>
    </section>

    <section class="section section-stone svc-cta">
      <div class="container narrow">
        <h2>Ready to talk about your project?</h2>
        <p>Tell us what you're planning and we'll get back to you with a free, no-obligation quote.</p>
        <div class="svc-actions">
          <a href="/#quote" class="btn btn-solid">Get a Free Quote</a>
          <a href="tel:+16129917000" class="btn btn-outline">Call 612-991-7000</a>
        </div>
        <p class="label svc-more-label">More services</p>
        <div class="svc-more">
{more}        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <img src="/images/logo-light.png" alt="Custom Tile Interiors" class="footer-logo" width="336" height="238">
      <p>Tile Contractor · Twin Cities, MN</p>
      <p><a href="tel:+16129917000">612-991-7000</a> · <a href="mailto:agcustomtileinteriors@gmail.com">agcustomtileinteriors@gmail.com</a></p>
      <p class="copyright">© <span id="year">2026</span> Custom Tile Interiors</p>
    </div>
  </footer>

  <a href="tel:+16129917000" class="mobile-call">Call for a Free Quote</a>

  <script src="/script.js?v={V_JS}"></script>
</body>
</html>
'''

for svc in SERVICES:
    out = os.path.join(SITE, "services", svc["slug"])
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w") as f:
        f.write(page(svc))
    print("built", f"/services/{svc['slug']}/", len(svc["photos"]), "photos")

# Site map: homepage + every service page
urls = [f"{BASE}/"] + [f"{BASE}/services/{s['slug']}/" for s in SERVICES]
with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>2026-10-24</lastmod>\n  </url>\n")
    f.write("</urlset>\n")
print("sitemap:", len(urls), "pages")
