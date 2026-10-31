#!/usr/bin/env python3
"""Rigenera le pagine del sito (italiano in docs/, inglese in docs/en/) e docs/sitemap.xml.

    python3 tools/build.py

I testi fissi stanno qui in TEXT (il form e la sua informativa arrivano dal
widget di ../mindcontact-forms); servizi, installazioni e progetti
in tools/content.json.
"""
import json
import os
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"
DATA = json.loads((ROOT / "tools" / "content.json").read_text())

URL = "https://www.mindcontact.net/"

# The contact form is the widget served by ../mindcontact-forms; FORMS_URL=http://localhost:3300 for local previews.
FORMS_URL = os.environ.get("FORMS_URL", "https://forms.mindcontact.net")

TEXT = {
    "it": dict(
        base="",
        title="MindContact — sviluppo software e sistemi interattivi",
        description="MindContact progetta e sviluppa software su misura, app e sistemi interattivi per musei, mostre ed eventi. Roberto Luttino, Torino.",
        nav=[("software", "Software"), ("interattivi", "Sistemi interattivi"), ("progetti", "Progetti"), ("chi-sono", "Chi sono"), ("contatti", "Contatti")],
        menu="Menu",
        kicker="Sviluppo software e sistemi interattivi",
        h1="Soluzioni verticali<br>per un mondo orizzontale",
        lede="Progetto e sviluppo software su misura, app e sistemi interattivi. Dall'analisi del problema al codice, fino all'elettronica: una persona sola che segue tutto, dall'inizio alla fine.",
        cta="Raccontami il tuo progetto",
        cta2="Guarda i progetti",
        sw_kicker="Software su misura",
        sw_h2="Il software che segue il tuo modo di lavorare",
        sw_lede="Quando i fogli Excel e gli strumenti standard non bastano più, serve un software costruito sul tuo processo, non il contrario. E che cresca con te.",
        stack="Con cosa lavoro",
        ix_kicker="Sistemi interattivi",
        ix_h2="Installazioni che rispondono",
        ix_lede="Per musei, mostre ed eventi rendo interattivi gli oggetti normali: una scrivania, un insieme di meccanismi, un tabellone. Il pubblico non guarda soltanto, tocca, apre, muove, e l'oggetto risponde. Progetto tutta la catena, dai sensori agli attuatori, passando per elettronica, firmware e software. Chi visita si porta a casa un ricordo difficile da dimenticare e facile da condividere.",
        ix_where="Dove li ho portati",
        pj_kicker="Progetti",
        pj_h2="Software che ho sviluppato",
        pj_lede="Prodotti in uso ogni giorno, costruiti per aziende e startup.",
        dev="Sviluppo",
        devs=dict(fullstack="Full-stack", backend="Backend", frontend="Frontend", frontend_backend="Frontend e backend", mobile="App mobile"),
        client="Cliente",
        partner="Con",
        used_by="Usato da",
        own="Prodotto MindContact",
        visit="Visita il sito",
        more="Scopri di più",
        profile="Vedi il profilo",
        pt_kicker="Partner",
        pt_h2="Con chi lavoro",
        pt_lede="Quando un progetto chiede più mani o altri mestieri, lavoro con persone e studi di cui mi fido: amici ed ex compagni dell'ITIS Olivetti di Ivrea.",
        lab_kicker="Il lato sperimentale",
        lab_h2="Giochi, musica e piccole app",
        lab=[("mindcontact.io", "https://mindcontact.io/", "Giochi, strumenti musicali e librerie che girano nel browser, con l'anima a 8 bit."),
             ("mindcontact.app", "https://mindcontact.app/", "Piccole app Android che fanno una cosa sola: si aprono e funzionano, senza account.")],
        me_kicker="Chi sono",
        me_h2="Roberto Luttino",
        me=["Ho iniziato a programmare sul Commodore 64 e a saldare componenti nel mio “laboratorio di elettronica” da ragazzino. Poi MS-DOS, Amiga, Windows, e infine Linux e i sistemi embedded.",
            "Al MultiDams di Torino, tra musica e teatro, ho incontrato i sistemi interattivi: il punto in cui elettronica, musica e informatica stanno insieme. MindContact è nata lì. Oggi sviluppo soprattutto software su misura, con lo stesso approccio sperimentale."],
        me_link="Di più su di me",
        contact=dict(
            kicker="Contatti", h2="Parliamone",
            lede="Un software da costruire, un processo da automatizzare, un'installazione da progettare: scrivimi, rispondo io.",
            noscript="Il modulo di contatto ha bisogno di JavaScript.",
        ),
        foot_links="Privacy",
    ),
    "en": dict(
        base="../",
        title="MindContact — software development and interactive systems",
        description="MindContact designs and builds custom software, apps and interactive systems for museums, exhibitions and events. Roberto Luttino, Turin, Italy.",
        nav=[("software", "Software"), ("interattivi", "Interactive systems"), ("progetti", "Projects"), ("chi-sono", "About"), ("contatti", "Contact")],
        menu="Menu",
        kicker="Software development and interactive systems",
        h1="Vertical solutions<br>for a horizontal world",
        lede="I design and build custom software, apps and interactive systems. From the analysis of the problem to the code, down to the electronics: one person following everything from start to finish.",
        cta="Tell me about your project",
        cta2="See the projects",
        sw_kicker="Custom software",
        sw_h2="Software that follows the way you work",
        sw_lede="When spreadsheets and off-the-shelf tools are no longer enough, you need software built around your process, not the other way round. Software that grows with you.",
        stack="What I work with",
        ix_kicker="Interactive systems",
        ix_h2="Installations that respond",
        ix_lede="For museums, exhibitions and events I make ordinary objects interactive: a desk, a set of mechanisms, a board. Visitors don't just look, they touch, open, move, and the object responds. I design the whole chain, from sensors to actuators, through electronics, firmware and software. Visitors take home a memory that is hard to forget and easy to share.",
        ix_where="Where they have been",
        pj_kicker="Projects",
        pj_h2="Software I have built",
        pj_lede="Products in daily use, built for companies and startups.",
        dev="Development",
        devs=dict(fullstack="Full-stack", backend="Backend", frontend="Frontend", frontend_backend="Frontend and backend", mobile="Mobile app"),
        client="Client",
        partner="With",
        used_by="Used by",
        own="MindContact product",
        visit="Visit the site",
        more="Find out more",
        profile="See the profile",
        pt_kicker="Partners",
        pt_h2="Who I work with",
        pt_lede="When a project needs more hands or other crafts, I work with people and studios I trust: friends and former classmates from the ITIS Olivetti technical school in Ivrea.",
        lab_kicker="The experimental side",
        lab_h2="Games, music and small apps",
        lab=[("mindcontact.io", "https://mindcontact.io/en/", "Games, music tools and libraries that run in the browser, with an 8-bit soul."),
             ("mindcontact.app", "https://mindcontact.app/en/", "Small Android apps that do one thing: they open and work, with no account.")],
        me_kicker="About",
        me_h2="Roberto Luttino",
        me=["I started programming on the Commodore 64 and soldering components in my teenage “electronics lab”. Then MS-DOS, Amiga, Windows, and finally Linux and embedded systems.",
            "At the MultiDams in Turin, between music and theatre, I came across interactive systems: the place where electronics, music and computing meet. That is where MindContact began. Today I mostly build custom software, with the same experimental approach."],
        me_link="More about me",
        contact=dict(
            kicker="Contact", h2="Let's talk",
            lede="Software to build, a process to automate, an installation to design: write to me, I answer myself.",
            noscript="The contact form needs JavaScript.",
        ),
        foot_links="Privacy",
    ),
}

STACK = [".NET", "Angular", "Flutter", "FlutterFlow", "Kotlin", "SQL Server", "PostgreSQL", "Linux", "Microcontrollori e firmware"]
STACK_EN = [s.replace("Microcontrollori e firmware", "Microcontrollers and firmware") for s in STACK]

# Line icons for the service tiles (24×24, stroked with currentColor).
ICONS = {
    "web": '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4M3 9h18"/>',
    "mobile": '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
    "integrations": '<path d="M4 8h13l-3-3M20 16H7l3 3"/>',
    "analysis": '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M8.5 11h5M11 8.5v5"/>',
}



def software(lang, t):
    cards = "\n".join(
        f'      <li class="tile"><svg class="tile-icon" viewBox="0 0 24 24" aria-hidden="true">{ICONS[s["icon"]]}</svg>'
        f'<h3>{escape(s[lang][0])}</h3><p>{escape(s[lang][1])}</p></li>'
        for s in DATA["software"]
    )
    stack = "".join(f"<li>{escape(s)}</li>" for s in (STACK if lang == "it" else STACK_EN))
    return f"""  <section class="section" id="software">
    <p class="kicker">{t["sw_kicker"]}</p>
    <h2>{escape(t["sw_h2"])}</h2>
    <p class="section-lede">{escape(t["sw_lede"])}</p>
    <ul class="tiles">
{cards}
    </ul>
    <h3 class="stack-title">{t["stack"]}</h3>
    <ul class="chips">{stack}</ul>
  </section>"""


def venues(lang):
    return "\n".join(
        f'        <li><strong>{escape(i[lang])}</strong>'
        + (f'<span>{escape(i["where"])}</span>' if i["where"] else "")
        + "</li>"
        for i in DATA["installations"]
    )


def interactive(lang, t):
    items = venues(lang)
    return f"""  <section class="band" id="interattivi">
    <div class="band-inner">
      <p class="kicker">{t["ix_kicker"]}</p>
      <h2>{escape(t["ix_h2"])}</h2>
      <p class="section-lede">{escape(t["ix_lede"])}</p>
      <h3>{t["ix_where"]}</h3>
      <ul class="venues">
{items}
      </ul>
      <p class="band-more"><a class="link" href="{PAGES["interactive"][lang]}">{t["more"]} <span aria-hidden="true">→</span></a></p>
    </div>
  </section>"""


def project(p, lang, t):
    # A page of our own wins over an external site.
    if p.get("page"):
        link = f'<a class="link" href="{PAGES[p["page"]][lang]}">{t["more"]} <span aria-hidden="true">→</span></a>'
    elif p.get("href"):
        link = f'<a class="link" href="{p["href"]}" rel="noopener">{t["visit"]} <span aria-hidden="true">→</span></a>'
    else:
        link = "<span></span>"
    # Own products name who uses them; work for others names the client.
    who = t["used_by"] if p.get("own") else t["client"]
    # The part of the stack built, first in the details.
    dev = f'<dt>{t["dev"]}</dt><dd>{t["devs"][p["role"]]}</dd>'
    # Only the owner's products carry a label above the name. Every card keeps six children,
    # empty where missing, so the rows of its subgrid line up with the cards beside it.
    own = f'<p class="role">{t["own"]}</p>' if p.get("own") else "<span></span>"
    wide = " card--wide" if p.get("wide") else ""
    return f"""      <li class="card card--lead{wide}">
        {own}
        <h3>{escape(p["name"])}</h3>
        <p>{escape(p[lang])}</p>
        <dl class="meta">{dev}{f'<dt>{who}</dt><dd>{escape(p["client"])}</dd>' if p.get("client") else ""}{f'<dt>{t["partner"]}</dt><dd>{escape(p["partner"])}</dd>' if p.get("partner") else ""}</dl>
        <dl class="meta"><dt class="sr-only">Tech</dt><dd class="tech">{escape(p["tech"])}</dd></dl>
        {link}
      </li>"""


def projects(lang, t):
    # The main products in two rows of their own (3 + 2 on desktop), then the smaller ones.
    major = "\n".join(project(p, lang, t) for p in DATA["projects"] if p.get("major"))
    minor = "\n".join(project(p, lang, t) for p in DATA["projects"] if not p.get("major"))
    return f"""  <section class="section" id="progetti">
    <p class="kicker">{t["pj_kicker"]}</p>
    <h2>{escape(t["pj_h2"])}</h2>
    <p class="section-lede">{escape(t["pj_lede"])}</p>
    <ul class="cards cards--major">
{major}
    </ul>
    <ul class="cards">
{minor}
    </ul>
  </section>"""


def partners(lang, t):
    items = "\n".join(
        f'      <li><a href="{escape(p["href"])}"><strong>{escape(p["name"])}</strong><span>{escape(p[lang])}</span>'
        f'<span class="go">{t["profile"] if p.get("profile") else t["visit"]} <span aria-hidden="true">→</span></span></a></li>'
        for p in DATA["partners"]
    )
    return f"""  <section class="section lab" id="partner">
    <p class="kicker">{t["pt_kicker"]}</p>
    <h2>{escape(t["pt_h2"])}</h2>
    <p class="section-lede">{escape(t["pt_lede"])}</p>
    <ul class="sites{' sites--five' if len(DATA["partners"]) == 5 else ''}">
{items}
    </ul>
  </section>"""


def lab(lang, t):
    items = "\n".join(
        f'      <li><a href="{href}"><strong>{name}</strong><span>{escape(text)}</span>'
        f'<span class="go">{t["visit"]} <span aria-hidden="true">→</span></span></a></li>'
        for name, href, text in t["lab"]
    )
    return f"""  <section class="section lab">
    <p class="kicker">{t["lab_kicker"]}</p>
    <h2>{escape(t["lab_h2"])}</h2>
    <ul class="sites">
{items}
    </ul>
  </section>"""


def about(lang, t):
    paras = "\n".join(f"      <p>{escape(p)}</p>" for p in t["me"])
    return f"""  <section class="section about" id="chi-sono">
    <img class="about-mark" src="{t["b"]}assets/img/mark.svg" alt="" width="96" height="49" loading="lazy">
    <div>
      <p class="kicker">{t["me_kicker"]}</p>
      <h2>{t["me_h2"]}</h2>
{paras}
      <p><a class="link" href="https://robertoluttino.it/">{t["me_link"]}: robertoluttino.it <span aria-hidden="true">→</span></a></p>
    </div>
  </section>"""


def contact(lang, t):
    c = t["contact"]
    return f"""  <section class="section contact" id="contatti">
    <p class="kicker">{c["kicker"]}</p>
    <h2>{escape(c["h2"])}</h2>
    <p class="section-lede">{escape(c["lede"])}</p>
    <div data-mc-contact data-site="mindcontact.net" data-lang="{lang}"></div>
    <noscript><p>{c["noscript"]}</p></noscript>
  </section>"""


def page(lang, path, title, description, hero, body):
    """One page of the site. path is relative to the language root: "" for the home,
    "sistemi-interattivi/" for a page one level down."""
    t = dict(TEXT[lang])
    up = "../" * path.count("/")
    # b leads from this page to the site root (assets), home to the home of the same language.
    t["b"] = b = t["base"] + up
    home = up or "./"
    # The same page in the other language, found through PAGES.
    other = next((v for v in PAGES.values() if v[lang] == path), {"it": "", "en": ""})
    if lang == "it":
        switch = f'<strong>IT</strong><a href="{up}en/{other["en"]}" hreflang="en" lang="en">EN</a>'
    else:
        switch = f'<a href="{b}{other["it"]}" hreflang="it" lang="it">IT</a><strong>EN</strong>'
    url = URL + ("" if lang == "it" else "en/") + path
    # Menu entries with a page of their own lead there; the others to their section of the home.
    def target(i):
        if i in NAV_PAGES:
            return up + PAGES[NAV_PAGES[i]][lang]
        if i == "contatti":  # every page ends with the contact form
            return "#contatti"
        return f'{"" if not path else home}#{i}'
    nav = "".join(f'<a href="{target(i)}">{escape(n)}</a>' for i, n in t["nav"])
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{escape(description)}">
<meta name="theme-color" content="#296DC1">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="it" href="{URL}{other["it"]}">
<link rel="alternate" hreflang="en" href="{URL}en/{other["en"]}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<link rel="icon" href="{b}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{b}assets/img/apple-touch-icon.png">
<link rel="preload" href="{b}assets/fonts/SourceSansPro-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{b}assets/site.css">
</head>
<body>
<!-- Generata da tools/build.py: non modificarla a mano, si riscrive. -->
<header class="top">
  <div class="top-inner">
    <a class="brand" href="{home}"><img src="{b}assets/img/mark-white.svg" alt="" width="44" height="23"><span>MindContact</span></a>
    <p class="lang">{switch}</p>
    <details class="menu">
      <summary>{t["menu"]}</summary>
      <nav>{nav}</nav>
    </details>
  </div>
</header>
<main>
  <section class="hero{" hero--page" if path else ""}">
    <div class="hero-inner">
      <p class="kicker">{hero["kicker"]}</p>
      <h1>{hero["h1"]}</h1>
      <p class="lede">{escape(hero["lede"])}</p>
      <p class="hero-actions"><a class="button" href="#contatti">{escape(hero["cta"])}</a>{f'<a class="button button--ghost" href="{hero["cta2_href"]}">{escape(hero["cta2"])}</a>' if hero.get("cta2") else ""}</p>
    </div>
    <img class="hero-mark" src="{b}assets/img/mark-white.svg" alt="" width="776" height="396">
  </section>
{body(lang, t)}
{contact(lang, t)}
</main>
<footer class="foot">
  <div class="foot-inner">
    <img src="{b}assets/img/logo-white.svg" alt="MindContact" width="110" height="75">
    <div>
      <p>MindContact di Luttino Roberto · Via Ivrea 41, 10016 Montalto Dora (TO)</p>
      <p>P.IVA 10699860010 · REA TO-1229762</p>
      <p><a href="https://mindcontact.io/">mindcontact.io</a> · <a href="https://mindcontact.app/">mindcontact.app</a> · <a href="https://robertoluttino.it/">robertoluttino.it</a> · <a href="#privacy-form">{t["foot_links"]}</a></p>
    </div>
  </div>
</footer>
<script src="{FORMS_URL}/v1/widget.js" defer></script>
<script src="{b}assets/js/site.js" defer></script>
</body>
</html>
"""


def prose(sec, id_=""):
    """A section of running text: kicker, title, paragraphs."""
    paras = "\n".join(f"    <p>{escape(x)}</p>" for x in sec["paras"])
    return f"""  <section class="section prose"{f' id="{id_}"' if id_ else ""}>
    <p class="kicker">{sec["kicker"]}</p>
    <h2>{escape(sec["h2"])}</h2>
{paras}
  </section>"""


def features(sec, id_, kind="tiles--text"):
    items = "\n".join(f"      <li class=\"tile\"><h3>{escape(h)}</h3><p>{escape(x)}</p></li>" for h, x in sec["items"])
    return f"""  <section class="section" id="{id_}">
    <p class="kicker">{sec["kicker"]}</p>
    <h2>{escape(sec["h2"])}</h2>
    <p class="section-lede">{escape(sec["lede"])}</p>
    <ul class="tiles {kind}">
{items}
    </ul>
  </section>"""


def facts(sec):
    items = "\n".join(f"        <li><strong>{escape(h)}</strong><span>{escape(x)}</span></li>" for h, x in sec["items"])
    return f"""  <section class="band">
    <div class="band-inner">
      <p class="kicker">{sec["kicker"]}</p>
      <h2>{escape(sec["h2"])}</h2>
      <ul class="venues facts">
{items}
      </ul>
    </div>
  </section>"""


def hagal(lang):
    c = DATA["hagal"][lang]
    def body(lang, t):
        return "\n".join([prose(c["problem"]), features(c["features"], "funzioni"), facts(c["facts"]), prose(c["custom"])])
    return page(lang, PAGES["hagal"][lang], c["title"], c["description"], c["hero"], body)


def reads(sec):
    def item(author, title, where, href):
        cite = f'<a href="{href}">{escape(title)}</a>' if href else escape(title)
        return f"      <li>{escape(author)}, <cite>{cite}</cite>, {escape(where)}</li>"
    items = "\n".join(item(*r) for r in DATA["interactive"]["reads"])
    return f"""  <section class="section">
    <p class="kicker">{sec["kicker"]}</p>
    <h2>{escape(sec["h2"])}</h2>
    <p class="section-lede">{escape(sec["lede"])}</p>
    <ul class="reads">
{items}
    </ul>
  </section>"""


def interactive_page(lang):
    c = DATA["interactive"][lang]
    def body(lang, t):
        where = f"""  <section class="band" id="lavori">
    <div class="band-inner">
      <p class="kicker">{c["where"]["kicker"]}</p>
      <h2>{escape(c["where"]["h2"])}</h2>
      <ul class="venues">
{venues(lang)}
      </ul>
    </div>
  </section>"""
        return "\n".join([prose(c["what"]), prose(c["roots"]), features(c["how"], "come", "tiles--text tiles--steps"),
                          where, reads(c["reads"])])
    return page(lang, PAGES["interactive"][lang], c["title"], c["description"], c["hero"], body)


def home_body(lang, t):
    return "\n".join(f(lang, t) for f in (software, interactive, projects, partners, lab, about))


def home(lang):
    t = TEXT[lang]
    hero = dict(kicker=t["kicker"], h1=t["h1"], lede=t["lede"], cta=t["cta"], cta2=t["cta2"], cta2_href="#progetti")
    return page(lang, "", t["title"], t["description"], hero, home_body)


# Every page: the same key in both languages, with each language's path.
PAGES = {
    "home": {"it": "", "en": ""},
    "hagal": {"it": "hagalclinic/", "en": "hagalclinic/"},
    "interactive": {"it": "sistemi-interattivi/", "en": "interactive-systems/"},
}

# Menu anchors replaced by a dedicated page.
NAV_PAGES = {"interattivi": "interactive"}

# Builders of the pages below the home, by key.
SUBPAGES = {"hagal": hagal, "interactive": interactive_page}


def sitemap():
    locs = "".join(f"  <url><loc>{URL}{'' if lang == 'it' else 'en/'}{v[lang]}</loc></url>\n"
                   for v in PAGES.values() for lang in ("it", "en"))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{locs}</urlset>
"""

ANCHOR = re.compile(r'<a\b([^>]*?)\bhref="(https?://[^"]*)"([^>]*)>')


def new_tab(html):
    """Absolute links open in a new tab; in-page and relative links stay (owner rule, 2026-10-29).
    Same logic as ../mindcontact-identity/tools/link_nuova_scheda.py."""
    def fix(m):
        attrs = m.group(1) + m.group(3)
        if "target=" in attrs:
            return m.group(0)
        if 'rel="' in attrs:
            return m.group(0)[:-1] + ' target="_blank">'
        return m.group(0)[:-1] + ' target="_blank" rel="noopener">'
    return ANCHOR.sub(fix, html)


if __name__ == "__main__":
    written = []
    for key, paths in PAGES.items():
        for lang in ("it", "en"):
            rel = ("" if lang == "it" else "en/") + paths[lang] + "index.html"
            html = home(lang) if key == "home" else SUBPAGES[key](lang)
            (SITE / rel).parent.mkdir(parents=True, exist_ok=True)
            (SITE / rel).write_text(new_tab(html))
            written.append("docs/" + rel)
    (SITE / "sitemap.xml").write_text(sitemap())
    print("rigenerate: " + ", ".join(written) + ", docs/sitemap.xml")
