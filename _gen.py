#!/usr/bin/env python3
"""One-shot static page generator for Elevate Views.
Stamps service + sector pages from data into pure static HTML (no runtime build).
Run once: python _gen.py   ->  writes services/*.html and sectors/*.html
Safe to re-run; it overwrites generated pages only.
"""
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))

# Web3Forms access key. Get a free one at https://web3forms.com (enter your email, copy the key).
# Replace the placeholder below, then run `python _gen.py` to restamp all generated pages.
WEB3FORMS_KEY = "ff64e992-4e9d-4074-a992-b469dbacce9f"

NAV = '''<header class="nav" id="top">
  <div class="wrap nav__inner">
    <a class="brand" href="/" aria-label="Elevate Views home">
      <span class="brand__mark" aria-hidden="true">/EV</span>
      <span class="brand__name">Elevate&nbsp;Views</span>
    </a>
    <nav class="nav__links" aria-label="Primary">
      <a href="/services/"{services_active}>Services</a>
      <a href="/sectors/"{sectors_active}>Sectors</a>
      <a href="/#systems">Systems</a>
      <a href="/resources/">Resources</a>
      <a href="/#faq">FAQ</a>
    </nav>
    <button class="nav__toggle" aria-label="Menu" aria-expanded="false">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>
    </button>
    <a class="btn btn--solid nav__cta" href="/#contact">Book a call</a>
  </div>
</header>'''

FOOTER = '''<footer class="footer">
  <div class="wrap footer__inner">
    <div>
      <span class="brand__mark" aria-hidden="true">/EV</span>
      <p class="footer__name">Elevate Views</p>
      <p class="footer__line">Custom operational systems and automation for UK businesses.</p>
    </div>
    <nav class="footer__nav" aria-label="Footer">
      <a href="/services/">Services</a>
      <a href="/sectors/">Sectors</a>
      <a href="/resources/">Resources</a>
      <a href="/#contact">Book a call</a>
    </nav>
  </div>
  <div class="wrap footer__base"><small>&copy; 2026 Elevate Views. All rights reserved.</small></div>
</footer>'''

CONTACT = '''<section class="band band--cta" id="contact">
    <div class="wrap">
      <div class="rail">
        <p class="rail__label reveal">Contact</p>
        <h2 class="section__h2 reveal">{cta_head}</h2>
      </div>
      <p class="section__lead reveal">A short call, an honest read on whether a system is worth it for you, and a fixed quote if it is.</p>
      <form class="form reveal" action="https://api.web3forms.com/submit" method="POST" data-web3form>
        <input type="hidden" name="access_key" value="''' + WEB3FORMS_KEY + '''" />
        <input type="hidden" name="subject" value="New enquiry from Elevate Views" />
        <input type="hidden" name="from_name" value="Elevate Views website" />
        <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" />
        <div class="form__row">
          <label>Name<input type="text" name="name" required autocomplete="name" /></label>
          <label>Email<input type="email" name="email" required autocomplete="email" /></label>
        </div>
        <div class="form__row">
          <label>Business / sector<input type="text" name="business" autocomplete="organization" /></label>
          <label>Phone<input type="tel" name="phone" autocomplete="tel" /></label>
        </div>
        <label>What is eating your time right now?<textarea name="message" rows="4" required></textarea></label>
        <button class="btn btn--solid" type="submit">Book a call</button>
        <p class="form__note" data-form-status>No spam. We reply within one working day.</p>
      </form>
    </div>
  </section>'''


def page(title, desc, canonical, jsonld, body, services_active=False, sectors_active=False):
    sa = ' class="is-active"' if services_active else ''
    ka = ' class="is-active"' if sectors_active else ''
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{canonical}" />
<meta name="theme-color" content="#0f1115" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:site_name" content="Elevate Views" />
<meta property="og:locale" content="en_GB" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet" />
{jsonld}
<link rel="stylesheet" href="/css/styles.css" />
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{NAV.format(services_active=sa, sectors_active=ka)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="/js/main.js"></script>
</body>
</html>
'''


def service_jsonld(name, desc, url):
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","name":"{name}","description":"{desc}","provider":{{"@type":"ProfessionalService","name":"Elevate Views","url":"https://elevateviews.co.uk/"}},"areaServed":"GB","url":"{url}"}}
</script>'''


def faq_jsonld(faqs):
    items = ",".join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (q, a)
        for q, a in faqs
    )
    return '<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + items + ']}\n</script>'


def chips(kws):
    return '<div class="chips">' + "".join(
        f'<span class="chip{" chip--on" if i==0 else ""}">{html.escape(k)}</span>' for i, k in enumerate(kws)
    ) + '</div>'


def prose_blocks(blocks):
    out = []
    for b in blocks:
        if b[0] == 'h2': out.append(f'<h2>{b[1]}</h2>')
        elif b[0] == 'h3': out.append(f'<h3>{b[1]}</h3>')
        elif b[0] == 'p': out.append(f'<p>{b[1]}</p>')
        elif b[0] == 'ul': out.append('<ul>' + "".join(f'<li>{li}</li>' for li in b[1]) + '</ul>')
    return "\n".join(out)


# ---------- RENDERED UI MOCKUPS (CSS only, no external images) ----------
def mock_rows(title, rows):
    """rows: list of (id_or_none, text, (pill_class, pill_text))"""
    body = ""
    for rid, txt, pill in rows:
        idspan = f'<span class="mrow__id">{rid}</span>' if rid else ''
        pc, pt = pill
        body += f'<div class="mrow"><div class="mrow__l">{idspan}<span class="mrow__txt">{txt}</span></div><span class="pill {pc}">{pt}</span></div>'
    return f'''<div class="mock">
            <div class="mock__bar"><span class="mock__dot"></span><span class="mock__dot"></span><span class="mock__dot"></span><span class="mock__title">{title}</span></div>
            <div class="mock__body">{body}</div>
          </div>'''


def mock_bars(title, items):
    """items: list of (label, percent, low_bool, pill_class, pill_text)"""
    body = ""
    for lab, pct, low, pc, pt in items:
        cls = "sbar sbar--low" if low else "sbar"
        body += f'<div class="mrow"><div class="mrow__l"><span class="mrow__txt mrow__sub">{lab}</span></div><span class="{cls}"><i style="width:{pct}%"></i></span><span class="pill {pc}">{pt}</span></div>'
    return f'''<div class="mock">
            <div class="mock__bar"><span class="mock__dot"></span><span class="mock__dot"></span><span class="mock__dot"></span><span class="mock__title">{title}</span></div>
            <div class="mock__body">{body}</div>
          </div>'''


def mock_chart(title, cols, legend_hi="Peak", legend_lo="Projected"):
    """cols: list of (label, percent, hi_bool)"""
    bars = ""
    for lab, pct, hi in cols:
        bc = "chart__bar chart__bar--hi" if hi else "chart__bar"
        bars += f'<div class="chart__col"><span class="{bc}" style="height:{pct}%"></span><span class="chart__lab">{lab}</span></div>'
    return f'''<div class="mock">
            <div class="mock__bar"><span class="mock__dot"></span><span class="mock__dot"></span><span class="mock__dot"></span><span class="mock__title">{title}</span></div>
            <div class="mock__body"><div class="chart">{bars}</div>
            <div class="chart__legend"><span><i class="chart__key" style="background:var(--signal)"></i>{legend_hi}</span><span><i class="chart__key" style="background:rgba(74,134,196,0.32)"></i>{legend_lo}</span></div></div>
          </div>'''


def mock_flow(title, nodes):
    """nodes: list of (main_text, sub_text)"""
    ics = [
        '<path d="M12 2v20M2 12h20"/>',
        '<path d="M4 7h16M4 12h16M4 17h10"/>',
        '<path d="M4 4h16v12H8l-4 4z"/>',
    ]
    body = ""
    for i, (main, sub) in enumerate(nodes):
        ic = ics[i % len(ics)]
        body += f'<div class="flow__node"><span class="flow__ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2">{ic}</svg></span><span class="flow__txt">{main}<small>{sub}</small></span></div>'
        if i < len(nodes) - 1:
            body += '<div class="flow__line"></div>'
    return f'''<div class="mock">
            <div class="mock__bar"><span class="mock__dot"></span><span class="mock__dot"></span><span class="mock__dot"></span><span class="mock__title">{title}</span></div>
            <div class="mock__body"><div class="flow">{body}</div></div>
          </div>'''


def sector_showcase(slug, mock_html, caption):
    """Wraps a sector mockup in a showcase band for the dedicated page."""
    return f'''  <section class="band band--alt" id="example">
    <div class="wrap">
      <div class="rail">
        <p class="rail__label reveal">Example system</p>
        <h2 class="section__h2 reveal">What it looks like in practice.</h2>
      </div>
      <div class="showcase reveal">
        <div class="showcase__art" aria-label="Example {slug.replace('-', ' ')} system interface">{mock_html}</div>
        <p class="showcase__cap">{caption}</p>
      </div>
    </div>
  </section>'''


def faq_html(faqs):
    items = "".join(
        f'<details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs
    )
    return f'''<section class="band band--alt" id="faq">
    <div class="wrap">
      <div class="rail"><p class="rail__label reveal">FAQ</p><h2 class="section__h2 reveal">Common questions.</h2></div>
      <div class="faq__list">{items}</div>
    </div>
  </section>'''


def related_html(links):
    items = "".join(
        f'<a href="{href}"><span>{label}</span><small>{tag}</small></a>' for href, label, tag in links
    )
    return f'''<section class="band">
    <div class="wrap">
      <div class="rail"><p class="rail__label reveal">Related</p><h2 class="section__h2 reveal">Keep exploring.</h2></div>
      <div class="related reveal">{items}</div>
    </div>
  </section>'''


# ---------- SERVICES DATA ----------
SERVICES = [
    {
        "slug": "custom-operational-systems",
        "title": "Custom Operational Systems for UK Businesses | Elevate Views",
        "desc": "Bespoke ordering, stock control and operational systems built around how your business actually works. Custom software for UK businesses, not generic SaaS.",
        "h1": "Custom operational systems, built around your business.",
        "sub": "Ordering, stock control and the day-to-day operations that run your business, built as one system instead of five disconnected tools.",
        "kws": ["custom operational systems", "bespoke business software UK", "custom software development", "inventory management system", "order management system"],
        "blocks": [
            ("h2", "Generic software makes you work its way. We build around yours."),
            ("p", "Off-the-shelf SaaS is built for the average business, so every real business ends up bending its process to fit the tool, paying for features it never uses, and gluing three subscriptions together with spreadsheets. A custom operational system does the opposite: it maps to how your team already works, and removes the steps that waste time."),
            ("h2", "What a custom operational system covers"),
            ("ul", ["Order capture across every channel you sell through, in one place",
                     "Live stock control that updates as things move, not at month end",
                     "Reordering driven by real usage, with supplier details built in",
                     "Roles and permissions so the right people see the right screens",
                     "Reports that answer the questions you actually ask"]),
            ("h2", "Built on a proven core, then tailored"),
            ("p", "We do not start from a blank page for every client. We build on a tested core and tailor it to your workflow, which keeps the cost down and the first working version close. You get something live and earning in weeks, then we extend it."),
            ("h3", "Who this is for"),
            ("p", "Owners and operators who have outgrown spreadsheets and paper, who lose hours to admin, or who are paying for several tools that still do not talk to each other."),
        ],
        "faqs": [
            ("How is this different from buying software off the shelf?", "Off-the-shelf software forces your process to match the tool. A custom system matches the tool to your process, so there is nothing to work around and nothing you pay for but never use."),
            ("Is custom software expensive?", "Less than most owners expect. We build on a proven core and tailor it, rather than starting from scratch, so a focused system costs far less than a full bespoke build."),
            ("Can it connect to tools I already use?", "Usually yes. Part of the mapping stage is deciding what stays, what connects by integration, and what the new system replaces."),
        ],
        "related": [
            ("/services/business-automation.html", "Workflow automation", "service"),
            ("/services/demand-forecasting.html", "Demand forecasting", "service"),
            ("/sectors/", "All sectors", "sectors"),
        ],
    },
    {
        "slug": "business-automation",
        "title": "Business Automation & Workflow Automation, UK | Elevate Views",
        "desc": "Workflow automation for UK small businesses: remove repetitive admin across quotes, invoices, rotas, reorders and reporting. Business process automation that pays for itself.",
        "h1": "Workflow automation that removes the admin no one should be doing.",
        "sub": "Quotes, invoices, rotas, reminders, reorders and reports that run themselves, so your team spends time on the work that actually earns.",
        "kws": ["business automation", "workflow automation", "business process automation", "automation agency UK", "small business automation"],
        "blocks": [
            ("h2", "Most small businesses run on hidden admin"),
            ("p", "Re-typing the same details between tools. Chasing the same payments. Building the same report every Monday. None of it is hard, but it adds up to hours a week and it is the first thing to slip when you are busy. Automation removes the work, not the control."),
            ("h2", "What we automate"),
            ("ul", ["Quote and invoice generation from a single set of inputs",
                     "Payment chasing and reminders, sent on a schedule, stopped when paid",
                     "Stock reorders triggered by real levels, not memory",
                     "Onboarding sequences for new customers or clients",
                     "Weekly and monthly reports built and sent automatically"]),
            ("h2", "It connects the tools you already pay for"),
            ("p", "You do not need to rip out your stack. We connect the tools you already use so data flows between them without anyone copying and pasting. Where a tool is missing, we add a small piece rather than a whole new platform."),
            ("h3", "What it is worth"),
            ("p", "If automation saves one person five hours a week, that is most of a working day back, every week, that goes into selling, serving customers, or simply going home earlier."),
        ],
        "faqs": [
            ("What can realistically be automated?", "Anything repetitive and rule-based: data entry between tools, reminders, invoicing, reordering, reporting and onboarding. If a person follows the same steps each time, it can usually be automated."),
            ("Do I have to change all my software?", "No. We connect what you already use first. New tools come in only where there is a genuine gap."),
            ("How quickly does automation pay back?", "Often within the first month or two, because the time saved is immediate and recurring."),
        ],
        "related": [
            ("/services/custom-operational-systems.html", "Custom systems", "service"),
            ("/services/web-and-ai.html", "Web and AI", "service"),
            ("/sectors/accountants.html", "For accountants", "sector"),
        ],
    },
    {
        "slug": "demand-forecasting",
        "title": "Demand Forecasting Systems for UK Businesses | Elevate Views",
        "desc": "Demand forecasting built from your real sales history. Reduce waste and stockouts in restaurants, retail and ecommerce by reordering to a number, not a guess.",
        "h1": "Demand forecasting, so you reorder to a number not a guess.",
        "sub": "Forecasts built from your own sales history, the calendar and seasonality, turning ordering from a gut feel into a decision you can trust.",
        "kws": ["demand forecasting", "demand forecasting software", "inventory forecasting", "sales forecasting tool", "stock forecasting UK"],
        "blocks": [
            ("h2", "Guessing your orders costs money twice"),
            ("p", "Order too much and you write off waste and tie up cash in stock. Order too little and you lose the sale and the customer. Most businesses swing between both because ordering relies on memory and gut feel. Forecasting replaces the guess with a number drawn from what actually happened."),
            ("h2", "What goes into a forecast"),
            ("ul", ["Your real sales history, at the level of individual items",
                     "Day of week, seasonality and known trends",
                     "Calendar events, holidays and local factors",
                     "Lead times, so you order in time to restock"]),
            ("h2", "Where it pays off most"),
            ("p", "Restaurants and food businesses cutting spoilage. Retail and ecommerce avoiding both stockouts and overstock. Any business where what you hold has a cost and what you miss has a cost."),
            ("h3", "Forecasting on its own, or built in"),
            ("p", "We can add forecasting to your existing stock process, or build it into a full operational system so the forecast becomes the reorder, automatically."),
        ],
        "faqs": [
            ("How much sales history do I need?", "The more the better, but useful forecasts start with a few months of clean sales data. We help get your data into shape as part of the build."),
            ("Is this AI?", "Where it helps, yes. The point is accuracy, not buzzwords. We use the simplest method that gives reliable numbers for your business."),
            ("Can it trigger reordering automatically?", "Yes, when forecasting is built into an operational system the forecast can become a reorder with a click, or fully automatically."),
        ],
        "related": [
            ("/services/custom-operational-systems.html", "Custom systems", "service"),
            ("/sectors/restaurants.html", "For restaurants", "sector"),
            ("/sectors/ecommerce.html", "For ecommerce", "sector"),
        ],
    },
    {
        "slug": "web-and-ai",
        "title": "Web Development & AI Integration for UK Businesses | Elevate Views",
        "desc": "Fast, credible business websites plus the AI layer on top: assistants, smart search and forecasting. Web and AI that connects to the systems your business runs on.",
        "h1": "Web and AI, connected to the system underneath.",
        "sub": "A fast, credible site is the entry point. The AI layer on top turns the data in your systems into answers, assistants and decisions.",
        "kws": ["AI integration for business", "business website development UK", "AI automation", "custom web development", "AI assistant for business"],
        "blocks": [
            ("h2", "A website is the front door, not the building"),
            ("p", "Most agencies sell you the front door and stop there. We build the door so it is fast, credible and converts, then connect it to the systems that actually run the business, so a booking, an order or an enquiry flows straight into your operations instead of an inbox."),
            ("h2", "Where AI earns its place"),
            ("ul", ["Assistants that answer customer questions from your real data",
                     "Smart search across your products, services or documents",
                     "Forecasting and pattern-spotting on your own numbers",
                     "Drafting and summarising the repetitive writing your team does"]),
            ("h2", "Built to be found"),
            ("p", "Every site we build is structured to rank: clean semantic markup, fast loading, proper metadata and structured data. The system underneath is the moat; the site is how new customers find it."),
            ("h3", "No AI for the sake of it"),
            ("p", "We add AI where it removes work or wins a customer, and nowhere it does not. The goal is a business that runs easier, not a demo."),
        ],
        "faqs": [
            ("Do I need AI at all?", "Not always. We add it where it removes real work or wins customers. If it would not, we say so and skip it."),
            ("Will the website actually rank?", "We build for search from the start with clean markup, speed and structured data. Ranking also needs content over time, which we can help plan."),
            ("Can the AI use my own data safely?", "Yes. The AI layer works on your data with access controlled, so it answers from what is true for your business."),
        ],
        "related": [
            ("/services/business-automation.html", "Workflow automation", "service"),
            ("/services/demand-forecasting.html", "Demand forecasting", "service"),
            ("/sectors/", "All sectors", "sectors"),
        ],
    },
]

# ---------- SECTORS DATA ----------
SECTORS = [
    {
        "slug": "restaurants",
        "title": "Restaurant Ordering & Stock Systems UK | Elevate Views",
        "desc": "Custom restaurant systems: unified ordering across counter, phone and delivery apps, live stock control and demand forecasting to cut waste. Built for UK hospitality.",
        "h1": "Systems for restaurants that stop the guesswork.",
        "sub": "Unify your orders, see your stock as it moves, and forecast next week so you reorder to a number. Less waste, fewer stockouts, hours back.",
        "kws": ["restaurant ordering system", "restaurant stock management", "restaurant inventory software UK", "hospitality management system", "restaurant demand forecasting"],
        "blocks": [
            ("h2", "The three places a restaurant leaks money"),
            ("p", "Orders scattered across the counter, the phone and three delivery apps. Stock counted by eye and reordered on memory. Prep planned on a gut feel about how busy it will be. Each one is a small leak. Together they are your margin."),
            ("h2", "What we build for restaurants"),
            ("ul", ["One order queue across counter, phone and every delivery app",
                     "Live stock that updates as ingredients are used",
                     "Reorder suggestions based on real usage and supplier lead times",
                     "Demand forecasts from sales history, day of week and the calendar",
                     "Waste tracking so you can see what is being thrown away and why"]),
            ("h2", "A worked example"),
            ("p", "A single site connects its order channels, tracks stock as it moves, and forecasts next week from real sales history and the calendar. The owner reorders to a number, not a guess. Spoilage drops, stockouts drop, and the manager gets hours back every week."),
        ],
        "faqs": [
            ("Does it work with delivery apps?", "Yes. Pulling orders from delivery platforms into one queue alongside counter and phone orders is one of the most common things we build."),
            ("Can it reduce food waste?", "That is often the biggest win. Forecasting plus live stock means you buy closer to what you will actually use."),
            ("Do I need to replace my till?", "Not necessarily. We connect to what you have where we can, and only replace what is holding you back."),
        ],
    },
    {
        "slug": "salons",
        "title": "Salon & Clinic Booking and Stock Systems UK | Elevate Views",
        "desc": "Systems for salons and clinics: smart bookings, reduced no-shows, product stock control and automated reminders. Custom software for UK beauty and wellness businesses.",
        "h1": "Systems for salons and clinics that protect the diary.",
        "sub": "Fewer no-shows, product stock that never runs dry, and the rebooking and reminders handled automatically so your team stays on the floor.",
        "kws": ["salon booking system", "salon management software", "clinic booking system UK", "salon stock management", "appointment reminder system"],
        "blocks": [
            ("h2", "Empty chairs and dead stock are the same problem"),
            ("p", "A no-show is a slot you can never sell again. A product that runs out mid-treatment is a sale lost and a client let down. Both come from running bookings and stock on memory and goodwill. A system makes both reliable."),
            ("h2", "What we build for salons and clinics"),
            ("ul", ["Online booking that fills cancellations automatically",
                     "Automated reminders and confirmations to cut no-shows",
                     "Deposits and policies handled at the point of booking",
                     "Product and consumable stock tracked per treatment",
                     "Rebooking prompts so regulars never fall through the gaps"]),
            ("h2", "The point is the floor, not the desk"),
            ("p", "Every minute your team spends chasing confirmations or counting stock is a minute off the floor. Automating the admin keeps them on chargeable work."),
        ],
        "faqs": [
            ("Will it reduce no-shows?", "Reminders, confirmations and deposits at booking are the proven levers, and we build all three in."),
            ("Can it track product use per treatment?", "Yes, so stock reflects what is actually being used and reordering becomes automatic."),
            ("Does it replace my booking tool?", "Only if yours is holding you back. Otherwise we build around it and add what is missing."),
        ],
    },
    {
        "slug": "dentists",
        "title": "Dental Practice Systems: Recalls, Scheduling, Supplies | Elevate Views",
        "desc": "Custom systems for UK dental practices: automated recall management, smarter scheduling, and supply and stock control. Reduce gaps in the book and manual admin.",
        "h1": "Systems for dental practices that keep the book full.",
        "sub": "Automated recalls, scheduling that fills gaps, and supply control that never leaves a surgery short. The admin runs itself, the diary stays full.",
        "kws": ["dental practice management system", "dental recall system", "dental scheduling software UK", "dental supply management", "patient recall automation"],
        "blocks": [
            ("h2", "Recalls are revenue, and they slip"),
            ("p", "Every patient due a check-up is booked revenue, but recalls slip when they depend on someone remembering to send them. Gaps in the book go unfilled. Surgeries run short on supplies at the worst moment. All three are systems problems."),
            ("h2", "What we build for dental practices"),
            ("ul", ["Automated recall reminders that bring patients back on time",
                     "Scheduling that fills cancellations from a waiting list",
                     "Supply and consumable stock tracked across surgeries",
                     "Reordering tied to real usage and lead times",
                     "Reporting on book utilisation and recall performance"]),
            ("h2", "Quiet, reliable, in the background"),
            ("p", "The best practice systems are invisible. Patients get reminded, gaps get filled, supplies arrive before they run out, and the front desk is freed from chasing."),
        ],
        "faqs": [
            ("Can it handle patient recalls automatically?", "Yes. Automated, timed recall reminders are one of the highest-value things we build for practices."),
            ("Does it work alongside our practice software?", "Usually. We connect to what you have and add the missing automation and stock control."),
            ("Is patient data handled properly?", "Access is controlled and data is handled to UK standards. We scope compliance as part of the build."),
        ],
    },
    {
        "slug": "law-firms",
        "title": "Law Firm Systems: Client Intake, Matters, Documents | Elevate Views",
        "desc": "Custom systems for UK law firms: streamlined client intake, matter management and document automation. Reduce admin and onboarding friction for solicitors.",
        "h1": "Systems for law firms that cut the intake friction.",
        "sub": "Faster client intake, matters tracked in one place, and document generation that takes minutes not hours, so fee earners spend time on fee-earning work.",
        "kws": ["law firm case management", "legal client intake system", "document automation for law firms", "legal practice management UK", "matter management system"],
        "blocks": [
            ("h2", "Fee earners doing admin is the most expensive admin there is"),
            ("p", "Re-keying client details, assembling the same documents by hand, hunting for the current version of a matter. Every hour a solicitor spends on it is an hour not billed. Systems give that time back."),
            ("h2", "What we build for law firms"),
            ("ul", ["Client intake that captures details once and reuses them everywhere",
                     "Matter management with status, deadlines and documents in one place",
                     "Document automation from templates and intake data",
                     "Conflict and deadline checks built into the workflow",
                     "Reporting on matters, time and pipeline"]),
            ("h2", "Built around how firms actually work"),
            ("p", "Legal workflows are specific and they vary by firm. We map yours before building, so the system fits your practice areas and your way of working rather than a generic template."),
        ],
        "faqs": [
            ("Can it automate document generation?", "Yes. Generating standard documents from intake data and templates is one of the biggest time savers we build."),
            ("Will it fit our practice areas?", "We map your workflows first, so the system reflects how your firm actually runs."),
            ("Is client data kept secure?", "Access is role-controlled and data handled to UK standards, scoped with you during the build."),
        ],
    },
    {
        "slug": "accountants",
        "title": "Accountancy Practice Systems & Automation UK | Elevate Views",
        "desc": "Custom systems for UK accountants: client onboarding, deadline tracking and automated chasing of records. Reduce manual admin across the practice and never miss a deadline.",
        "h1": "Systems for accountants that chase so you do not have to.",
        "sub": "Client onboarding that runs itself, deadlines tracked across every client, and records chased automatically so nothing slips and no one spends the day on email.",
        "kws": ["accounting practice management", "client onboarding automation", "deadline tracking software", "accountancy workflow automation UK", "automated record chasing"],
        "blocks": [
            ("h2", "The practice tax: chasing"),
            ("p", "Onboarding each new client by hand. Tracking dozens of deadlines across dozens of clients. Chasing records that arrive late, by email, one reminder at a time. It is the work that fills a practice's week and adds nothing a system could not do better."),
            ("h2", "What we build for accountants"),
            ("ul", ["Client onboarding sequences that collect everything up front",
                     "A single view of every client deadline and its status",
                     "Automated, escalating chasers for missing records",
                     "Document collection portals so clients self-serve",
                     "Capacity and workflow reporting across the team"]),
            ("h2", "Quiet weeks instead of crunch"),
            ("p", "When chasing and onboarding run automatically, deadline season stops being a scramble. The team works on the accounts, not the admin around them."),
        ],
        "faqs": [
            ("Can it chase clients for records automatically?", "Yes. Automated, escalating reminders for missing records are one of the most requested builds, and they free up real time."),
            ("Does it track deadlines across all clients?", "Yes, in one view with status, so nothing slips through and crunch periods are calmer."),
            ("Does it work with our existing software?", "Usually. We connect to your tools and add the onboarding, chasing and tracking around them."),
        ],
    },
    {
        "slug": "ecommerce",
        "title": "Ecommerce Inventory & Fulfilment Systems UK | Elevate Views",
        "desc": "Custom systems for UK ecommerce: unified inventory across channels, fulfilment automation and demand forecasting. Avoid stockouts and overstock, ship faster.",
        "h1": "Systems for ecommerce that keep inventory honest.",
        "sub": "One source of truth for stock across every channel, fulfilment that runs without copy-paste, and forecasting that prevents both stockouts and overstock.",
        "kws": ["ecommerce inventory management", "multichannel inventory system", "ecommerce fulfilment automation", "ecommerce demand forecasting", "order management system UK"],
        "blocks": [
            ("h2", "Selling on three channels, guessing on all of them"),
            ("p", "When stock lives in separate places for your store, your marketplace and your warehouse, the numbers drift. You oversell what you do not have and sit on what will not move. Fulfilment turns into copy-paste between tabs. One system makes inventory a single, honest number."),
            ("h2", "What we build for ecommerce"),
            ("ul", ["Unified inventory across your store and every marketplace",
                     "Fulfilment that flows from order to dispatch without re-keying",
                     "Low-stock alerts and automatic reordering",
                     "Demand forecasting to avoid stockouts and overstock",
                     "Returns and exchange handling built into the flow"]),
            ("h2", "Speed and accuracy compound"),
            ("p", "Accurate stock means fewer cancellations and better listings. Faster fulfilment means happier customers and better reviews. Both feed back into more sales."),
        ],
        "faqs": [
            ("Can it sync stock across marketplaces?", "Yes. A single, accurate inventory across your store and marketplaces is the core of what we build for ecommerce."),
            ("Does it handle fulfilment too?", "Yes, from order through to dispatch, removing the manual copy-paste between systems."),
            ("Can it forecast demand?", "Yes, from your sales history, so you order ahead of demand instead of reacting to stockouts."),
        ],
    },
    {
        "slug": "warehousing",
        "title": "Warehouse Stock, Picking & Reordering Systems UK | Elevate Views",
        "desc": "Custom warehouse systems for UK businesses: accurate stock control, faster picking and automated reordering. Reduce errors and keep inventory moving.",
        "h1": "Systems for warehousing that keep stock moving.",
        "sub": "Stock you can trust to the unit, picking that is faster and harder to get wrong, and reordering that triggers itself before you run short.",
        "kws": ["warehouse management system", "stock control system UK", "warehouse picking system", "automated reordering", "inventory management software"],
        "blocks": [
            ("h2", "Inaccurate stock breaks everything downstream"),
            ("p", "If the number in the system does not match the number on the shelf, every order, every reorder and every promise to a customer is built on sand. Picking slows down, mistakes go out, and reordering becomes guesswork. Accurate, live stock is the foundation everything else sits on."),
            ("h2", "What we build for warehousing"),
            ("ul", ["Live stock accurate to the unit, updated as things move",
                     "Picking workflows that are faster and harder to get wrong",
                     "Location and bin management so stock is found, not hunted",
                     "Automatic reordering tied to levels and lead times",
                     "Reporting on accuracy, throughput and slow movers"]),
            ("h2", "Built for the floor, not just the office"),
            ("p", "Warehouse systems have to work on the floor, on whatever devices your team uses, at the speed of the work. We build for the reality of the warehouse, not a tidy demo."),
        ],
        "faqs": [
            ("Can it work on handheld devices?", "Yes. We build the warehouse-floor screens to work on the devices your team already uses, at working speed."),
            ("Does it handle reordering?", "Yes, automatically, based on real levels and supplier lead times so you reorder before running short."),
            ("Can it improve picking accuracy?", "Yes. Guided picking workflows and location management reduce errors and speed the work up."),
        ],
    },
]


# ---------- PER-SECTOR MOCKUPS + CAPTIONS ----------
SECTOR_MOCKS = {
    "restaurants": (
        mock_rows("order queue", [
            ("#208", "Counter &middot; 3 items", ("pill--prep", "In prep")),
            ("#209", "Uber Eats &middot; 1", ("pill--new", "New")),
            ("#210", "Phone &middot; 2 items", ("pill--new", "New")),
            ("#207", "Just Eat &middot; out", ("pill--live", "Done")),
        ]),
        "A unified order queue pulling counter, phone and every delivery app into one screen, with live status and prep timing.",
    ),
    "salons": (
        mock_rows("today's diary", [
            ("09:30", "Colour &middot; Aisha K.", ("pill--live", "Confirmed")),
            ("11:00", "Cut &amp; finish &middot; Tom R.", ("pill--prep", "Reminder sent")),
            ("13:15", "Open slot", ("pill--new", "Fill from waitlist")),
            ("15:00", "Treatment &middot; Priya S.", ("pill--ok", "Deposit paid")),
        ]),
        "A live diary that confirms appointments, sends reminders to cut no-shows, and fills cancellations from the waitlist automatically.",
    ),
    "dentists": (
        mock_rows("recalls due", [
            ("", "J. Powell &middot; 6mo check", ("pill--low", "Overdue")),
            ("", "M. Hadid &middot; hygiene", ("pill--prep", "Reminder sent")),
            ("", "S. Okoro &middot; 6mo check", ("pill--new", "Due this week")),
            ("", "Surgery 2 &middot; gloves", ("pill--low", "Reorder")),
        ]),
        "Automated recalls that bring patients back on time, gaps filled from a waiting list, and surgery supplies tracked so nothing runs short.",
    ),
    "law-firms": (
        mock_rows("active matters", [
            ("M-204", "Conveyancing &middot; Hale", ("pill--prep", "Docs due")),
            ("M-205", "New enquiry &middot; intake", ("pill--new", "Auto-drafted")),
            ("M-201", "Probate &middot; Stevens", ("pill--ok", "On track")),
            ("M-198", "Deadline &middot; Friday", ("pill--low", "Action")),
        ]),
        "Client intake captured once and reused everywhere, matters tracked with deadlines, and standard documents generated from templates.",
    ),
    "accountants": (
        mock_rows("client records", [
            ("", "Bright Ltd &middot; VAT", ("pill--low", "Chasing")),
            ("", "North Cafe &middot; payroll", ("pill--prep", "Reminder 2")),
            ("", "Lumen Co &middot; year end", ("pill--ok", "Received")),
            ("", "Filing deadline", ("pill--low", "7 days")),
        ]),
        "Onboarding that collects everything up front, deadlines tracked across every client, and missing records chased automatically.",
    ),
    "ecommerce": (
        mock_bars("inventory &middot; all channels", [
            ("Store SKU-441", 72, False, "pill--ok", "OK"),
            ("Amazon SKU-441", 18, True, "pill--low", "Sync low"),
            ("eBay SKU-220", 54, False, "pill--ok", "OK"),
            ("Store SKU-209", 9, True, "pill--low", "Reorder"),
        ]),
        "One accurate inventory across your store and every marketplace, with low-stock alerts and reordering before you oversell.",
    ),
    "warehousing": (
        mock_bars("stock accuracy", [
            ("Bin A-12 &middot; widgets", 88, False, "pill--ok", "Verified"),
            ("Bin B-04 &middot; cables", 31, True, "pill--low", "Reorder"),
            ("Bin C-19 &middot; boxes", 64, False, "pill--ok", "OK"),
            ("Pick list &middot; #4821", 100, False, "pill--prep", "Ready"),
        ]),
        "Live stock accurate to the unit, guided picking that is harder to get wrong, and reordering triggered by real levels and lead times.",
    ),
}


def build_service(s):
    url = f"https://elevateviews.co.uk/services/{s['slug']}.html"
    jsonld = service_jsonld(s["h1"], s["desc"], url) + "\n" + faq_jsonld(s["faqs"])
    body = f'''  <section class="subhero">
    <div class="wrap subhero__grid">
      <p class="crumb reveal"><a href="/">Home</a> / <a href="/services/">Services</a> / {s['slug'].replace('-', ' ')}</p>
      <div class="reveal">
        <h1 class="subhero__h1">{s['h1']}</h1>
        <p class="subhero__sub">{s['sub']}</p>
        {chips(s['kws'])}
        <div class="subhero__cta">
          <a class="btn btn--solid" href="/#contact">Book a call</a>
          <a class="btn btn--ghost" href="/#systems">See example systems</a>
        </div>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="prose reveal">
        {prose_blocks(s['blocks'])}
      </div>
    </div>
  </section>

  {faq_html(s['faqs'])}

  {related_html(s['related'])}

  {CONTACT.format(cta_head="Want this built for your business?")}'''
    out = page(s["title"], s["desc"], url, jsonld, body, services_active=True)
    path = os.path.join(ROOT, "services", f"{s['slug']}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    return path


def build_sector(s):
    url = f"https://elevateviews.co.uk/sectors/{s['slug']}.html"
    jsonld = service_jsonld(s["h1"], s["desc"], url) + "\n" + faq_jsonld(s["faqs"])
    related = [
        ("/sectors/", "All sectors", "sectors"),
        ("/services/custom-operational-systems.html", "Custom systems", "service"),
        ("/services/demand-forecasting.html", "Demand forecasting", "service"),
    ]
    mock_html, caption = SECTOR_MOCKS[s['slug']]
    body = f'''  <section class="subhero">
    <div class="wrap subhero__grid">
      <p class="crumb reveal"><a href="/">Home</a> / <a href="/sectors/">Sectors</a> / {s['slug'].replace('-', ' ')}</p>
      <div class="reveal">
        <h1 class="subhero__h1">{s['h1']}</h1>
        <p class="subhero__sub">{s['sub']}</p>
        {chips(s['kws'])}
        <div class="subhero__cta">
          <a class="btn btn--solid" href="/#contact">Book a call</a>
          <a class="btn btn--ghost" href="#example">See an example system</a>
        </div>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="prose reveal">
        {prose_blocks(s['blocks'])}
      </div>
    </div>
  </section>

  {sector_showcase(s['slug'], mock_html, caption)}

  {faq_html(s['faqs'])}

  {related_html(related)}

  {CONTACT.format(cta_head="Tell us where your " + s['slug'].replace('-', ' ').rstrip('s') + " business leaks time.")}'''
    out = page(s["title"], s["desc"], url, jsonld, body, sectors_active=True)
    path = os.path.join(ROOT, "sectors", f"{s['slug']}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    return path


def build_services_index():
    cards = ""
    for i, s in enumerate(SERVICES, 1):
        short = s["h1"]
        cards += f'''        <a class="linkcard reveal" href="/services/{s['slug']}.html">
          <span class="linkcard__no">{i:02d} / Service</span>
          <h3>{s['slug'].replace('-', ' ').title()}</h3>
          <p>{s['sub']}</p>
          <span class="linkcard__go">Explore &rsaquo;</span>
        </a>
'''
    body = f'''  <section class="subhero">
    <div class="wrap subhero__grid">
      <p class="crumb reveal"><a href="/">Home</a> / Services</p>
      <div class="reveal">
        <h1 class="subhero__h1">What we build.</h1>
        <p class="subhero__sub">Four services that make a business run easier: custom systems, automation, forecasting, and the web and AI layer on top.</p>
        <div class="subhero__cta"><a class="btn btn--solid" href="/#contact">Book a call</a></div>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="linkgrid">
{cards}      </div>
    </div>
  </section>

  {CONTACT.format(cta_head="Not sure which you need?")}'''
    out = page(
        "Services | Business Systems, Automation & Forecasting | Elevate Views",
        "Elevate Views services: custom operational systems, business automation, demand forecasting and web and AI for UK businesses.",
        "https://elevateviews.co.uk/services/",
        '', body, services_active=True)
    path = os.path.join(ROOT, "services", "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    return path


def build_sectors_index():
    cards = ""
    for i, s in enumerate(SECTORS, 1):
        cards += f'''        <a class="linkcard reveal" href="/sectors/{s['slug']}.html">
          <span class="linkcard__no">{i:02d} / Sector</span>
          <h3>{s['slug'].replace('-', ' ').title()}</h3>
          <p>{s['sub']}</p>
          <span class="linkcard__go">Explore &rsaquo;</span>
        </a>
'''
    body = f'''  <section class="subhero">
    <div class="wrap subhero__grid">
      <p class="crumb reveal"><a href="/">Home</a> / Sectors</p>
      <div class="reveal">
        <h1 class="subhero__h1">Built for trades with real operations.</h1>
        <p class="subhero__sub">The same engine, tuned to how each sector works. Pick yours to see the systems we build for it.</p>
        <div class="subhero__cta"><a class="btn btn--solid" href="/#contact">Book a call</a></div>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="linkgrid">
{cards}      </div>
    </div>
  </section>

  {CONTACT.format(cta_head="Sector not listed?")}'''
    out = page(
        "Sectors We Build For | Restaurants, Salons, Dental, Legal & More | Elevate Views",
        "Custom operational systems by sector: restaurants, salons, dental practices, law firms, accountants, ecommerce and warehousing across the UK.",
        "https://elevateviews.co.uk/sectors/",
        '', body, sectors_active=True)
    path = os.path.join(ROOT, "sectors", "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    return path


if __name__ == "__main__":
    made = []
    for s in SERVICES: made.append(build_service(s))
    for s in SECTORS: made.append(build_sector(s))
    made.append(build_services_index())
    made.append(build_sectors_index())
    for m in made:
        print("wrote", os.path.relpath(m, ROOT))
    print(f"\n{len(made)} pages generated.")
