#!/usr/bin/env python3
"""
Generator for the redesigned dugovic.com static site.
Produces clean, accessible, and performant HTML pages.
"""
import html
import json
import os

BASE_DIR = "/tmp/dugovic_redesign"
ASSETS_CSS = "assets/css/style.css"
ASSETS_JS = "assets/js/main.js?v=2"
ASSETS_IMG = "assets/images"
ASSETS_VIDEO = "assets/video"

with open(os.path.join(BASE_DIR, "cats.json")) as f:
    CATEGORIES = json.load(f)

with open(os.path.join(BASE_DIR, "comic_order.json")) as f:
    COMIC_PAGES = json.load(f)

# Slides for the About card on the home page. Starts with the current
# about-card portrait, then rotates through studio photos in which Peter
# himself is visible. Excluded: the About-page portrait (`img-1110_orig`),
# the hands-only detail shot, the duplicate `img-0009`, the empty-studio
# frame (no person), and the one frame showing a different person.
ABOUT_SLIDES = [
    "about-card.webp",
    "img-0898.webp", "img-7305.webp", "img-7306.webp",
    "img-0009-1.webp", "img-0644.webp", "img-4350.webp",
    "studio-shot-use-it1.webp",
]
PORTRAIT_IMAGE = "img-1110_orig.webp"

# How many leading images in each Studio column load eagerly; the rest load lazily.
EAGER_LOAD_COUNT = 3


def load_attrs(i):
    """Return loading/fetchpriority attributes: eager for the first item, lazy otherwise."""
    return 'loading="eager" fetchpriority="high"' if i == 0 else 'loading="lazy"'

def deck_slide(src, alt, active, load):
    """Return one deck-slide <img> tag."""
    return f"""
                        <img class="deck-slide {active}" src="{src}" alt="{alt}" {load}>"""

def deck_slides(slides):
    """Join deck slides from (src, alt, load) tuples; first slide is active."""
    return "".join(
        deck_slide(src, alt, "is-active" if i == 0 else "", load)
        for i, (src, alt, load) in enumerate(slides)
    )

# Studio page: three explicit columns, ordered so total height is
# left < middle < right (matching the Works masonry convention).
STUDIO_COLUMNS = [
    ["img-7131.webp", "img-2053.webp", "img-7214.webp",
     "img-0009-1.webp", "img-7281.webp", "img-2821.webp", "img-3775.webp"],
    ["img-2820.webp", "img-3970.webp", "img-4604.webp",
     "img-3444.webp", "img-4772.webp", "img-4350.webp", "img-0883.webp"],
    ["img-0898.webp", "img-7305.webp", "img-0644.webp",
     "img-7306.webp", "img-4ea2f192.webp", "img-3373.webp"],
]

# Navigation Structure
# Contact is intentionally kept out of the primary nav; it lives in the footer.
NAV_LINKS = [
    {"href": "index.html", "label": "Home", "current": False},
    {"href": "gallery.html", "label": "Works", "current": False, "dropdown": True},
    {"href": "about.html", "label": "About", "current": False},
]

# Footer carries the full set, including Contact.
FOOTER_NAV_LINKS = [
    {"href": "index.html", "label": "Home"},
    {"href": "gallery.html", "label": "Works"},
    {"href": "about.html", "label": "About"},
    {"href": "contact.html", "label": "Contact"},
]

# Category key -> generated page filename
CAT_PAGE_FILES = {
    "Trailers": "trailers.html",
    "Signs": "signs.html",
    "Cars": "cars.html",
    "Kitchen": "kitchen-series.html",
    "Playgrounds": "playgrounds.html",
    "Pop Victorian": "pop-victorian.html",
}

# Category keys whose display name differs from the data key
CAT_DISPLAY_NAMES = {
    "Kitchen": "Kitchen Series",
    "Playgrounds": "Playgrounds & Fairs",
}


def category_display_name(cat_key):
    """Return the user-facing display name for a category key."""
    return CAT_DISPLAY_NAMES.get(cat_key, cat_key)


DROPDOWN_LINKS = [
    {"href": filename, "label": category_display_name(cat_key)}
    for cat_key, filename in CAT_PAGE_FILES.items()
]

def render_link(link, extra_attrs=''):
    """Render a single nav/footer <a> tag from a link dict."""
    attrs = f' {extra_attrs}' if extra_attrs else ''
    return f'<a href="{link["href"]}"{attrs}>{html.escape(link["label"])}</a>'


def get_header(active_page, is_translucent=False):
    """Generate the site header."""
    menuitem_attr = 'role="menuitem"'
    dropdown_items = "\n".join(
        f'                        {render_link(link, menuitem_attr)}'
        for link in DROPDOWN_LINKS
    )
    mobile_links = "\n".join(
        f'                <li>{render_link(link)}</li>'
        for link in DROPDOWN_LINKS
    )
    mobile_other_links = "\n".join(
        f'            {render_link(link)}'
        for link in NAV_LINKS
        if not link.get("dropdown") and link["href"] != "index.html"
    )
    nav_items_html = ""
    for link in NAV_LINKS:
        aria_current = ' aria-current="page"' if link["current"] or (link["label"] == active_page) else ""
        if link.get("dropdown"):
            nav_items_html += f'''
                <li class="nav__dropdown">
                    <a href="{link['href']}" class="nav__link nav__dropdown-trigger" aria-haspopup="true" aria-expanded="false">
                        {link['label']}
                        <svg class="caret" width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </a>
                    <div class="nav__dropdown-menu" role="menu">
{dropdown_items}
                    </div>
                </li>'''
        else:
            nav_items_html += f'''
                <li>
                    <a href="{link['href']}" class="nav__link"{aria_current}>{link['label']}</a>
                </li>'''

    main_class = "has-hero" if is_translucent else ""
    header_class = "nav nav--solid" if not is_translucent else "nav"

    return f'''
<header class="{header_class}">
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <a href="index.html" class="site-title">Peter Scot <span>Dugovic</span></a>
    <nav class="nav__inner" aria-label="Primary navigation">
        <button class="nav__toggle" aria-label="Toggle navigation menu" aria-expanded="false" aria-controls="mobile-menu">
            <span class="nav__toggle-bar"></span>
            <span class="nav__toggle-bar"></span>
            <span class="nav__toggle-bar"></span>
        </button>
        <ul class="nav__links">
            {nav_items_html}
        </ul>
    </nav>
</header>
<div id="mobile-menu" class="nav__mobile">
    <div class="nav__mobile-section">
        <span class="nav__mobile-heading">Works</span>
        <ul>
{mobile_links}
        </ul>
    </div>
    <div class="nav__mobile-section">
{mobile_other_links}
    </div>
</div>
<main id="main-content" class="main-content {main_class}">'''


def get_footer():
    """Generate the site footer."""
    footer_nav_links = "\n".join(
        f'                {render_link(link)}'
        for link in FOOTER_NAV_LINKS
    )
    return f'''
</main>
<footer class="site-footer">
    <div class="container">
        <div class="footer__content">
            <div class="footer__brand">
                <h2 class="footer__name">Peter Scot Dugovic</h2>
                <p class="footer__tagline">Visual Artist</p>
            </div>
            <nav class="footer__nav" aria-label="Footer navigation">
{footer_nav_links}
            </nav>
        </div>
        <div class="footer__bottom">
            <p>&copy; 2026 Peter Scot Dugovic. All rights reserved.</p>
            <p class="footer__social">
                <a href="https://www.instagram.com/artofdugovic/" target="_blank" rel="noopener" aria-label="Instagram">Instagram</a>
                <a href="mailto:info@dugovic.com" aria-label="Email">Email</a>
            </p>
        </div>
    </div>
</footer>
<script src="{ASSETS_JS}" defer></script>
</body>
</html>'''


def get_head(title, description=""):
    """Generate the HTML head section."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Peter Scot Dugovic</title>
    <meta name="description" content="{description}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{ASSETS_CSS}">
    <link rel="icon" type="image/svg+xml" href="{ASSETS_IMG}/favicon.svg">
</head>
<body>'''


def render_page(title, description, header, content):
    """Assemble a full page: head + header + body content + footer."""
    return get_head(title, description) + header + content + get_footer()


def lightbox_html():
    """Return the shared lightbox markup used by the works and studio pages."""
    return """<div class="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer">
        <div class="lightbox__content">
            <button class="lightbox__close" aria-label="Close viewer">&times;</button>
            <img class="lightbox__img" src="" alt="">
            <div class="lightbox__caption">
                <div class="title"></div>
                <div class="meta"></div>
            </div>
            <button class="lightbox__nav lightbox__nav--prev" aria-label="Previous image">&larr;</button>
            <button class="lightbox__nav lightbox__nav--next" aria-label="Next image">&rarr;</button>
            <span class="lightbox__counter" aria-hidden="true"></span>
        </div>
    </div>"""


def generate_gallery_page(category_key, category_name):
    """Generate a gallery page for a specific category."""
    items = CATEGORIES.get(category_key, [])
    header = get_header(category_name)

    gallery_items_html = ""
    for item in items:
        thumb_src = f"{ASSETS_IMG}/{item['fn']}"
        full_src = f"{ASSETS_IMG}/{item['orig']}"
        caption = item.get('cap', '')
        alt_text = f"Painting: {caption} by Peter Scot Dugovic" if caption else f"Painting by Peter Scot Dugovic"

        lightbox_data = f'data-lightbox="{full_src}"'
        if caption:
            lightbox_data += f' data-lb-title="{caption}"'
        lightbox_data += f' data-lb-meta="From the {category_name} series"'

        gallery_items_html += f'''
            <a href="{full_src}" class="gallery__item" {lightbox_data}>
                <img src="{thumb_src}" alt="{alt_text}" loading="lazy" decoding="async">
                {f'<figcaption>{caption}</figcaption>' if caption else ''}
            </a>'''

    # Navigation to other categories
    cat_nav_html = ""
    for cat_key in CATEGORIES:
        if cat_key != category_key:
            cat_nav_html += (
                f'<a href="{CAT_PAGE_FILES[cat_key]}">{category_display_name(cat_key)}</a>'
                f'<span class="sep">&middot;</span>'
            )

    # Subtitle is derived from the display name; only names that don't fit
    # the "lowercased name with a trailing ' series' stripped" rule are overridden.
    series_overrides = {
        "Playgrounds & Fairs": "playgrounds and fairs",
        "Pop Victorian": "pop Victorian",
    }
    series_name = series_overrides.get(
        category_name,
        category_name.lower().removesuffix(" series"),
    )
    subtitle = f"Selected works from the {series_name} series."

    content = f'''
    <section class="page-header">
        <span class="eyebrow">Works</span>
        <h1>{category_name}</h1>
        <p class="lead">{subtitle}</p>
    </section>

    <section class="section">
        <div class="container">
            <div class="gallery">
                {gallery_items_html}
            </div>
            <nav class="gallery-nav" aria-label="Other works">
                {cat_nav_html}
            </nav>
        </div>
    </section>

    {lightbox_html()}
    '''

    return render_page(category_name, f"View {category_name} works by Peter Scot Dugovic", header, content)


def render_category_tile(href, display, items, count):
    """Render one category tile whose image stack cycles through every
    work in the category; CSS shows the first image by default."""
    img_tags = []
    for i, item in enumerate(items):
        thumb_filename = item['fn']
        cls = ' class="is-active"' if i == 0 else ''
        img_tags.append(
            f'<img{cls} src="{ASSETS_IMG}/{thumb_filename}" alt="" {load_attrs(i)}>'
        )
    stacked = "\n                ".join(img_tags)
    return f'''
            <a href="{href}" class="category-tile">
                {stacked}
                <div class="category-tile__label">
                    <h3 class="category-tile__name">{display}</h3>
                    <span class="category-tile__count">{count} works</span>
                </div>
            </a>'''


def category_tiles_html():
    """Build the category tile grid, used on the Works index."""
    tiles = ""
    for cat_key, filename in CAT_PAGE_FILES.items():
        items = CATEGORIES[cat_key]
        tiles += render_category_tile(
            filename, category_display_name(cat_key), items, len(items)
        )
    return tiles


def generate_index():
    """Generate the home page: the card-deck landing experience."""
    header = get_header("Home", is_translucent=True)

    # Slow slideshow: one representative work per series.
    work_slides = []
    for cat in CAT_PAGE_FILES:
        if cat in CATEGORIES and len(CATEGORIES[cat]) > 0:
            item = CATEGORIES[cat][0]
            work_slides.append((
                f"{ASSETS_IMG}/{item['orig']}",
                f"{item['series']} series painting by Peter Scot Dugovic",
                'loading="lazy"',
            ))
    slides_html = deck_slides(work_slides)

    # About card: starts on the current portrait, then rotates through the
    # studio photos in which Peter is present (see ABOUT_SLIDES).
    about_slides = [
        (f"{ASSETS_IMG}/{img}", "Peter Scot Dugovic in the studio", load_attrs(i))
        for i, img in enumerate(ABOUT_SLIDES)
    ]
    about_slides_html = deck_slides(about_slides)

    content = f'''
    <section class="deck" aria-label="Welcome">
        <div class="deck__stage">
            <button class="deck__card deck__card--hero" id="heroCard" aria-label="Open the deck">
                <span class="deck__card-inner">
                    <span class="deck__face deck__face--front"><img src="{ASSETS_IMG}/deck-front.webp" alt="" fetchpriority="high"></span>
                    <span class="deck__face deck__face--back"><img src="{ASSETS_IMG}/ace-card.webp" alt="The Ace of Art — Peter Scot Dugovic"></span>
                </span>
            </button>

            <div class="deck__dealt" id="dealtCards" aria-hidden="true">
                <a href="gallery.html" class="deck__card deck__card--works" aria-label="Works">
                    <span class="deck__face deck__face--slideshow">
{slides_html}
                    </span>
                    <span class="deck__label">Works</span>
                </a>
                <a href="about.html" class="deck__card deck__card--about" aria-label="About">
                    <span class="deck__face deck__face--about deck__face--slideshow">
{about_slides_html}
                    </span>
                    <span class="deck__label">About</span>
                </a>
            </div>

            <p class="deck__hint" id="deckHint" aria-live="polite"></p>
        </div>
    </section>
    '''

    return render_page("Home", "Portfolio and works of Peter Scot Dugovic, a painter.", header, content)


def generate_comic_bio():
    """Generate the comic bio page with pager."""
    header = get_header("Comic Bio")

    pages_html = ""
    thumbs_html = ""
    for i, page_id in enumerate(COMIC_PAGES):
        img_src = f"{ASSETS_IMG}/{page_id}.webp"
        active_class = "is-active" if i == 0 else ""
        pages_html += f'''
            <div class="comic__page {active_class}" role="tabpanel" aria-label="Page {i+1}">
                <img src="{img_src}" alt="Comic bio page {i+1}" {load_attrs(i)}>
            </div>'''

        thumbs_html += f'''
            <button class="comic__thumb {active_class}" aria-label="Go to page {i+1}">
                <img src="{img_src}" alt="" loading="lazy">
            </button>'''

    content = f'''
    <section class="comic">
        <div class="comic__stage">
            {pages_html}
        </div>
        <div class="comic__controls">
            <button class="comic__btn comic__btn--prev" aria-label="Previous page" disabled>&larr;</button>
            <span class="comic__counter" aria-live="polite">1 / {len(COMIC_PAGES)}</span>
            <button class="comic__btn comic__btn--next" aria-label="Next page">&rarr;</button>
        </div>
        <div class="comic__progress">
            <div class="comic__progress-bar" style="width: {100/len(COMIC_PAGES)}%"></div>
        </div>
        <div class="comic__thumbs" role="tablist" aria-label="Page thumbnails">
            {thumbs_html}
        </div>
    </section>
    '''

    return render_page("Comic Bio", "An illustrated biography of Peter Scot Dugovic.", header, content)


def generate_about():
    """Generate the about page: bio, consolidated exhibitions/collections, and studio links."""
    header = get_header("About")

    solo = [
        ("2018", "Arundel Farm Gallery", "Arundel, Maine"),
        ("2017", "Raiters Gallery", "Kennebunk, Maine"),
        ("2015", "Gallery 280", "Portsmouth, New Hampshire"),
        ("2014", "Whitney Gallery", "Wells, Maine"),
        ("2013", "Motorland America", "Biddeford, Maine"),
        ("2012", "CLIQ Gallery, Christiane Celle", "New York, New York"),
        ("2011", "CLIQ Gallery", "East Hampton, Long Island"),
    ]

    group = [
        ("2010–2018", "River Club Annual Invitational", "Kennebunkport, Maine"),
        ("2016–2018", "Cotes Gallery", "Newport, Rhode Island"),
        ("2015", "Hive Gallery", "Kennebunk, Maine"),
        ("2011", "River Tree Arts", "Skate Deck Show"),
        ("2010", "Gallery Couture", "Kennebunkport, Maine"),
    ]

    commissions = [
        ("Rith Kenmai", "Handmade oils on canvas, 48″ × 38″", "California"),
        ("Micheal Fixx", "Handmade oils on canvas, 48″ × 36″", "Boston"),
        ("Kate Farnam", "Handmade oils on canvas, 96″ × 52″", "Gibson, New York"),
        ("Tracy Thack", "Handmade oils on canvas, 42″ × 34″", "Alaska"),
        ("Matthews", "Handmade oils on canvas, 48″ × 36″", "Washington, DC"),
        ("Stefanie Posner", "Handmade oils on canvas, 48″ × 36″", "Bethesda, MD"),
    ]

    collectors = [
        "Japan", "Brazil", "Texas", "Connecticut",
        "New Jersey", "Maine", "New York",
    ]

    def rows(items):
        return "\n".join(
            f'                        <div class="exhibit-row">\n'
            f'                            <span class="exhibit-year">{when}</span>\n'
            f'                            <span class="exhibit-city">{title}</span>\n'
            f'                            <span class="exhibit-note">{note}</span>\n'
            f'                        </div>'
            for when, title, note in items
        )

    def collection_rows(items):
        return "\n".join(
            f'                        <div class="exhibit-row exhibit-row--collection">\n'
            f'                            <span class="exhibit-city">{loc}</span>\n'
            f'                        </div>'
            for loc in items
        )

    def exhibits_group(title, rows_html):
        return (
            f'                <div class="exhibits-group">\n'
            f'                    <h3 class="exhibits-group__title">{title}</h3>\n'
            f'                    <div class="exhibits-list">\n'
            f'{rows_html}\n'
            f'                    </div>\n'
            f'                </div>'
        )

    content = f'''
    <section class="page-header">
        <span class="eyebrow">Artist Statement</span>
        <h1>About</h1>
    </section>

    <section class="section">
        <div class="container">
            <div class="about-grid">
                <figure class="about-portrait">
                    <img src="{ASSETS_IMG}/{PORTRAIT_IMAGE}" alt="Portrait of Peter Scot Dugovic" fetchpriority="high">
                </figure>
                <div class="about-content">
                    <p>Born in Wells, Maine, Peter Scot Dugovic is a visual artist and sign maker whose work explores the intersection of nostalgia, urban decay, and American iconography. His paintings often feature muted palettes and atmospheric lighting, drawing influence from Edward Hopper's depictions of solitude and Gustav Klimt's ornate patterns.</p>
                    <p>Trained in both traditional oil painting and commercial sign making, Dugovic blends fine art techniques with the pragmatic precision of the signmaker's craft. His work has been exhibited in galleries across New England and New York, and he has been featured in American Artist Magazine.</p>

                    <div class="about-label">Experience</div>
                    <ul class="fact-list">
                        <li>
                            <span class="role">Visual Artist &amp; Sign Maker</span>
                            <span class="place">Wells, Maine &mdash; Independent</span>
                        </li>
                        <li>
                            <span class="role">Guest Artist</span>
                            <span class="place">Various Galleries, NYC &amp; Long Island</span>
                        </li>
                    </ul>

                    <div class="about-label">Education</div>
                    <ul class="fact-list">
                        <li>
                            <span class="role">MFA in Painting</span>
                            <span class="place">School of the Art Institute of Chicago</span>
                        </li>
                        <li>
                            <span class="role">BFA in Studio Art</span>
                            <span class="place">University of Maine</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <section class="section section-alt">
        <div class="container">
            <div class="section-head">
                <span class="eyebrow">Exhibitions</span>
                <h2>Exhibitions &amp; Collections</h2>
                <p class="lead">A record of gallery shows, public installations, commissions, and private collections.</p>
            </div>
            <div class="exhibits-two">
{exhibits_group("Solo Exhibitions", rows(solo))}

{exhibits_group("Group Exhibitions", rows(group))}
            </div>
{exhibits_group("Commissions", rows(commissions))}

{exhibits_group("Private Collections", collection_rows(collectors))}
        </div>
    </section>

    <section class="section">
        <div class="container text-center">
            <span class="eyebrow">Behind the Scenes</span>
            <h2>Studio &amp; Process</h2>
            <p class="lead" style="margin: 0 auto var(--sp-5);">Step inside the creative process. View studio shots and read the comic biography.</p>
            <div style="display: flex; gap: var(--sp-4); justify-content: center; flex-wrap: wrap;">
                <a href="studio-shots.html" class="btn">View Studio</a>
                <a href="comic-bio.html" class="btn" style="background: var(--gold); color: var(--ink);">Read Comic Bio</a>
            </div>
        </div>
    </section>
    '''

    return render_page("About", "Biography, exhibitions, and collections of Peter Scot Dugovic.", header, content)


def generate_contact():
    """Generate the contact page."""
    header = get_header("Contact")

    content = f'''
    <section class="page-header">
        <span class="eyebrow">Get in Touch</span>
        <h1>Contact</h1>
        <p class="lead">For inquiries regarding commissions, exhibitions, or private sales.</p>
    </section>

    <section class="section">
        <div class="container">
            <div class="contact-grid">
                <div class="contact-info">
                    <div class="contact-block">
                        <div class="label">Studio</div>
                        <div class="value">
                            Peter Scot Dugovic<br>
                            Wells, Maine<br>
                            USA
                        </div>
                    </div>
                    <div class="contact-block">
                        <div class="label">Email</div>
                        <div class="value">
                            <a href="mailto:info@dugovic.com">info@dugovic.com</a>
                        </div>
                    </div>
                    <div class="contact-block">
                        <div class="label">Social</div>
                        <div class="value">
                            <a href="https://www.instagram.com/artofdugovic/" target="_blank" rel="noopener">Instagram</a>
                        </div>
                    </div>
                </div>
                <div class="contact-form-wrapper">
                    <form class="contact-form" id="contactForm" novalidate>
                        <div class="form-row">
                            <div class="form-field">
                                <label for="name">Name <span class="req">*</span></label>
                                <input type="text" id="name" name="name" required autocomplete="name">
                            </div>
                            <div class="form-field">
                                <label for="email">Email <span class="req">*</span></label>
                                <input type="email" id="email" name="email" required autocomplete="email">
                            </div>
                        </div>
                        <div class="form-field">
                            <label for="subject">Subject</label>
                            <input type="text" id="subject" name="subject" autocomplete="off">
                        </div>
                        <div class="form-field">
                            <label for="message">Message <span class="req">*</span></label>
                            <textarea id="message" name="message" required></textarea>
                        </div>
                        <button type="submit" class="btn">Send Message <span class="arrow">&rarr;</span></button>
                    </form>
                    <div id="formSuccess" style="display: none; margin-top: var(--sp-4); padding: var(--sp-4); background: var(--gold-pale); border: 1px solid var(--gold); border-radius: var(--radius);">
                        <strong>Thank you!</strong> Your message has been sent. I will get back to you soon.
                    </div>
                </div>
            </div>
        </div>
    </section>
    '''

    script_js = '''
    <script>
    // Simple client-side validation and mailto fallback for static site
    document.getElementById('contactForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const form = this;
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        const name = form.name.value;
        const email = form.email.value;
        const subject = form.subject.value || "Website Inquiry";
        const message = form.message.value;
        const mailto = `mailto:info@dugovic.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(`From: ${name} (${email})\\n\\n${message}`)}`;
        window.location.href = mailto;
        document.getElementById('formSuccess').style.display = 'block';
        form.reset();
    });
    </script>
    '''

    return render_page("Contact", "Contact Peter Scot Dugovic for commissions or inquiries.", header, content + script_js)


def generate_studio_shots():
    """Generate the studio shots page with video background.

    The strip is three explicit columns (not CSS multi-column flow) so total
    column height follows the Works masonry convention: left < middle < right
    (see STUDIO_COLUMNS). Every shot is click-to-enlarge via the lightbox;
    where a full-size _orig asset exists it is the lightbox target.
    """
    header = get_header("Studio", is_translucent=True)

    def full_src(filename):
        """Full-size source for a studio thumbnail (falls back to the thumb)."""
        orig = filename.removesuffix(".webp") + "_orig.webp"
        return orig if os.path.exists(os.path.join(BASE_DIR, ASSETS_IMG, orig)) else filename

    def studio_item(filename, i):
        thumb = f"{ASSETS_IMG}/{filename}"
        full = f"{ASSETS_IMG}/{full_src(filename)}"
        lightbox_attrs = f'data-lightbox="{full}" data-lb-title="Studio" data-lb-meta="From the studio in Wells, Maine"'
        load = 'loading="eager"' if i < EAGER_LOAD_COUNT else 'loading="lazy"'
        return f'''
                <a href="{full}" class="gallery__item" {lightbox_attrs}>
                    <img src="{thumb}" alt="Studio shot — Peter Scot Dugovic, Wells, Maine" {load}>
                </a>'''

    columns_html = ""
    for col in STUDIO_COLUMNS:
        items = "".join(studio_item(filename, idx) for idx, filename in enumerate(col))
        columns_html += f'''
            <div class="studio-col">{items}
            </div>'''

    content = f'''
    <section class="studio-hero">
        <video autoplay muted loop playsinline data-observe poster="{ASSETS_VIDEO}/broadway-poster.webp">
            <source src="{ASSETS_VIDEO}/broadway.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        <div class="studio-hero__scrim"></div>
        <div class="studio-hero__content">
            <div class="container">
                <span class="eyebrow eyebrow--light">Behind the Scenes</span>
                <h1 class="studio-hero__title">Studio Shots</h1>
                <p class="studio-hero__text">A glimpse into the workshop where signs are crafted and paintings are composed. The constant hum of the city and the quiet focus of the canvas.</p>
            </div>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <div class="section-head">
                <span class="eyebrow">The Space</span>
                <h2>Inside the Studio</h2>
            </div>
            <div class="studio-strip">
                <div class="studio-masonry">
{columns_html}
                </div>
            </div>
        </div>
    </section>

    {lightbox_html()}
    '''

    return render_page("Studio Shots", "Photos and video from Peter Scot Dugovic's studio in Wells, Maine.", header, content)


def generate_gallery_index():
    """Generate the Works index page that lists all categories."""
    tiles = category_tiles_html()

    content = f'''
    <section class="page-header">
        <span class="eyebrow">Portfolio</span>
        <h1>All Works</h1>
    </section>
    <section class="section">
        <div class="container">
            <div class="categories">
                {tiles}
            </div>
        </div>
    </section>
    '''

    return render_page("Works", "All works by Peter Scot Dugovic.", get_header("Works"), content)


def write_page(filename, content):
    """Write a generated page to BASE_DIR and return its filename."""
    with open(os.path.join(BASE_DIR, filename), "w") as f:
        f.write(content)
    return filename


def main():
    """Generate all pages and return the filenames written, in order."""
    os.makedirs(BASE_DIR, exist_ok=True)

    pages = [
        ("index.html", generate_index()),
    ]
    pages.extend(
        (filename, generate_gallery_page(cat_key, category_display_name(cat_key)))
        for cat_key, filename in CAT_PAGE_FILES.items()
    )
    pages.extend([
        ("comic-bio.html", generate_comic_bio()),
        ("about.html", generate_about()),
        ("contact.html", generate_contact()),
        ("studio-shots.html", generate_studio_shots()),
        ("gallery.html", generate_gallery_index()),
    ])

    return [write_page(filename, content) for filename, content in pages]


if __name__ == "__main__":
    for filename in main():
        print(f"Generated {filename}")
    print("\nAll pages generated successfully.")
