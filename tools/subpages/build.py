"""Builds the GLOBAL PETRO subpages into the site folder (argv[1]). Run: python3 -I build.py "<site dir>"."""
from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).parent))
from pages import COMMON_FAQ, EMAIL, OBORY, PHONE, PHONE_TEL, SITE, STEPS  # noqa: E402

CSS = """
:root{--ink:#0E1518;--ink-soft:#28333A;--paper:#FBFAF9;--stone:#EDEAE4;--muted:#646C72;--line:#DFDCD5;--accent:#2F5D62;
--gut:clamp(20px,5vw,72px);--sans:'Manrope',system-ui,-apple-system,'Segoe UI',sans-serif}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:15.5px;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{display:block;max-width:100%;height:auto}a{color:inherit}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.container{max-width:1160px;margin:0 auto;padding:0 var(--gut)}
h1,h2,h3{margin:0;font-weight:300;letter-spacing:-.02em;line-height:1.15}
h1{font-size:clamp(30px,4.6vw,54px)}h2{font-size:clamp(23px,2.6vw,34px);margin-bottom:22px}h3{font-size:18px;font-weight:500;letter-spacing:0}
.eyebrow{margin:0 0 18px;font-size:10.5px;letter-spacing:.19em;text-transform:uppercase;color:var(--muted)}
.lede{font-size:clamp(16px,1.5vw,18.5px);color:var(--ink-soft);max-width:58ch;margin:22px 0 30px}
.btn{display:inline-flex;align-items:center;gap:10px;padding:15px 26px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);
font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;transition:background .25s,border-color .25s}
.btn:hover{background:var(--accent);border-color:var(--accent)}
.btn--ghost{background:transparent;color:var(--ink)}.btn--ghost:hover{background:var(--ink);color:var(--paper);border-color:var(--ink)}
header{position:sticky;top:0;z-index:20;background:rgba(251,250,249,.95);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
header .container{display:flex;align-items:center;justify-content:space-between;gap:20px;padding-top:14px;padding-bottom:14px}
.brand{display:flex;align-items:center;gap:11px;text-decoration:none}
.brand b{font-weight:500;font-size:15px}.brand small{display:block;font-size:9.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}
.mark{width:28px;height:28px;border:1px solid currentColor;display:grid;place-items:center;font-weight:500;font-size:14px}
header nav ul{display:flex;gap:26px;list-style:none;margin:0;padding:0}
header nav a{font-size:13px;color:var(--ink-soft);text-decoration:none}header nav a:hover{color:var(--ink)}
header .btn{padding:11px 18px}
.crumbs{font-size:12.5px;color:var(--muted);padding-top:22px}.crumbs ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.crumbs li+li:before{content:"/";margin-right:6px;color:var(--line)}.crumbs a{text-decoration:none}.crumbs a:hover{text-decoration:underline}
.hero{padding:clamp(28px,5vw,64px) 0 clamp(40px,6vw,80px)}
.hero-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(28px,5vw,72px);align-items:center}
.hero-img{aspect-ratio:4/3;object-fit:cover;width:100%;background:var(--stone)}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 30px;padding:0;list-style:none}
.tags li{font-size:12px;border:1px solid var(--line);padding:6px 12px;border-radius:99px;color:var(--ink-soft)}
section.block{padding:clamp(48px,6vw,88px) 0;border-top:1px solid var(--line)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,72px)}
ul.list{margin:0;padding:0;list-style:none}ul.list li{padding:12px 0;border-bottom:1px solid var(--line);display:flex;gap:12px}
ul.list li:before{content:"→";color:var(--accent)}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:0;padding:0;list-style:none;counter-reset:s}
.steps li{background:#fff;border:1px solid var(--line);padding:24px 22px;counter-increment:s}
.steps li:before{content:"0" counter(s);display:block;font-size:30px;font-weight:300;color:var(--accent);margin-bottom:12px}
.steps p{margin:8px 0 0;color:var(--ink-soft);font-size:14.5px}
.faq details{border-bottom:1px solid var(--line);padding:18px 0}.faq summary{cursor:pointer;font-weight:500;font-size:16.5px;list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::-webkit-details-marker{display:none}.faq summary:after{content:"+";font-weight:300;font-size:22px;line-height:1}
.faq details[open] summary:after{content:"–"}.faq p{margin:12px 0 0;color:var(--ink-soft);max-width:70ch}
.cta{background:var(--ink);color:var(--paper);padding:clamp(52px,7vw,96px) 0}
.cta h2{max-width:22ch}.cta p{color:rgba(255,255,255,.75);max-width:56ch}
.cta .btn{background:var(--paper);color:var(--ink);border-color:var(--paper)}.cta .btn:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.cta-row{display:flex;flex-wrap:wrap;gap:14px 28px;align-items:center;margin-top:28px}
.cta-row a.plain{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.35);padding-bottom:3px}
.related{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.related a{display:block;border:1px solid var(--line);background:#fff;padding:18px;text-decoration:none;font-size:14.5px;transition:border-color .2s}
.related a:hover{border-color:var(--ink)}
footer{padding:48px 0 36px;font-size:13px;color:var(--muted)}
.foot{display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:32px}
footer h3{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink);margin-bottom:12px}
footer ul{list-style:none;margin:0;padding:0}footer li{padding:3px 0}footer a{text-decoration:none}footer a:hover{color:var(--ink)}
.foot-bot{margin-top:32px;padding-top:20px;border-top:1px solid var(--line)}
@media (max-width:900px){header nav{display:none}.hero-grid,.two,.foot{grid-template-columns:1fr}.steps,.related{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.steps,.related{grid-template-columns:1fr}.brand small{display:none}header .btn{padding:10px 14px;font-size:10.5px}}
"""

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Manrope:wght@200..600&display=swap" onload="this.onload=null;this.rel=\'stylesheet\'">'
        '<noscript><link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200..600&display=swap" rel="stylesheet"></noscript>')

ORG = {"@type": "EmploymentAgency", "@id": SITE + "/#firma", "name": "GLOBAL PETRO s.r.o.", "url": SITE + "/", "telephone": PHONE_TEL, "email": EMAIL}


def e(text: str) -> str:
    return escape(text, quote=True)


def poptat_href(select: str | None) -> str:
    return "/?obor=" + quote(select) + "#contact" if select else "/#contact"


def ld(obj: dict) -> str:
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def breadcrumbs(trail: list[tuple[str, str]]) -> tuple[str, dict]:
    items = "".join(f'<li><a href="{u}">{e(n)}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{e(n)}</li>'
                    for i, (n, u) in enumerate(trail))
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(trail)]}
    return f'<nav class="crumbs container" aria-label="Drobečková navigace"><ol>{items}</ol></nav>', data


def faq_block(items: list[tuple[str, str]], heading: str = "Časté dotazy") -> tuple[str, dict]:
    html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in items)
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return f'<section class="block"><div class="container"><h2>{e(heading)}</h2><div class="faq">{html}</div></div></section>', data


def steps_block() -> str:
    lis = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in STEPS)
    return ('<section class="block"><div class="container"><p class="eyebrow">Jak to funguje</p>'
            f'<h2>Od poptávky po nástup — čtyři kroky a jeden kontakt</h2><ol class="steps">{lis}</ol></div></section>')


def cta_block(select: str | None) -> str:
    return ('<section class="cta" id="poptavka"><div class="container">'
            '<h2>Potřebujete lidi? Napište nám, koho hledáte</h2>'
            '<p>Sestavíme jednotlivce i celé pracovní skupiny podle požadavků vaší firmy. Ozveme se co nejdříve — obvykle ještě týž pracovní den.</p>'
            f'<div class="cta-row"><a class="btn" href="{poptat_href(select)}">Vyplnit poptávku →</a>'
            f'<a class="plain" href="tel:{PHONE_TEL}">{PHONE}</a><a class="plain" href="mailto:{EMAIL}">{EMAIL}</a></div>'
            "</div></section>")


def related_block(current: str | None) -> str:
    links = "".join(f'<a href="/{o["slug"]}">{e(o["select"])}</a>' for o in OBORY if o["slug"] != current)
    return f'<section class="block"><div class="container"><h2>Další obory</h2><div class="related">{links}</div></div></section>'


def header(select: str | None) -> str:
    return ('<header><div class="container"><a class="brand" href="/"><span class="mark">G</span>'
            '<span><b>GLOBAL PETRO</b><small>Pracovní síla · Česko</small></span></a>'
            '<nav aria-label="Hlavní menu"><ul><li><a href="/#about">O nás</a></li><li><a href="/#projects">Obory</a></li>'
            '<li><a href="/jak-to-funguje">Jak to funguje</a></li><li><a href="/caste-dotazy">Časté dotazy</a></li></ul></nav>'
            f'<a class="btn" href="{poptat_href(select)}">Poptat pracovníky</a></div></header>')


def footer() -> str:
    obory = "".join(f'<li><a href="/{o["slug"]}">{e(o["select"])}</a></li>' for o in OBORY)
    return ('<footer><div class="container"><div class="foot">'
            '<div><a class="brand" href="/"><span class="mark">G</span><span><b>GLOBAL PETRO</b><small>Pracovní síla · Česko</small></span></a>'
            '<p>GLOBAL PETRO s.r.o.<br>Kpt. Stránského 998/3, 198 00 Praha 9<br>IČO 07446969</p></div>'
            f'<div><h3>Obory</h3><ul>{obory}</ul></div>'
            f'<div><h3>Kontakt</h3><ul><li><a href="tel:{PHONE_TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li>'
            '<li><a href="/jak-to-funguje">Jak to funguje</a></li><li><a href="/caste-dotazy">Časté dotazy</a></li></ul></div></div>'
            '<div class="foot-bot">© 2026 GLOBAL PETRO s.r.o. Pracovníky zajišťujeme firmám po celé České republice.</div></div></footer>')


def page(*, slug: str, title: str, desc: str, body: str, schemas: list[dict], select: str | None, og_img: str | None) -> str:
    url = f"{SITE}/{slug}"
    og = f'<meta property="og:image" content="{SITE}/img/{og_img}">' if og_img else ""
    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="GLOBAL PETRO s.r.o.">
<meta property="og:locale" content="cs_CZ"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">{og}
<meta name="twitter:card" content="summary">
<link rel="icon" href="favicon.ico" sizes="32x32"><link rel="apple-touch-icon" href="apple-touch-icon.png"><meta name="theme-color" content="#0E1518">
{FONT}
<style>{CSS}</style>
{"".join(ld(s) for s in schemas)}
</head>
<body>
{header(select)}
<main>
{body}
</main>
{footer()}
</body>
</html>
"""


def obor_page(o: dict) -> str:
    crumbs_html, crumbs_ld = breadcrumbs([("Úvod", "/"), ("Obory", "/#projects"), (o["select"], "/" + o["slug"])])
    faq_html, faq_ld = faq_block(o["faq"] + COMMON_FAQ[:2])
    roles = "".join(f"<li>{e(r)}</li>" for r in o["roles"])
    need = "".join(f"<li>{e(n)}</li>" for n in o["need"])
    body = (crumbs_html +
            '<section class="hero"><div class="container hero-grid"><div>'
            f'<p class="eyebrow">Obor · Celá ČR</p><h1>{e(o["h1"])}</h1><p class="lede">{e(o["lede"])}</p>'
            '<ul class="tags"><li>Jednotlivci i skupiny</li><li>Celá Česká republika</li><li>Jeden kontakt pro celé obsazení</li></ul>'
            f'<a class="btn" href="{poptat_href(o["select"])}">Poptat pracovníky →</a></div>'
            f'<img class="hero-img" src="img/{o["img"]}" alt="{e(o["alt"])}" width="640" height="480" fetchpriority="high"></div></section>'
            '<section class="block"><div class="container two">'
            f'<div><p class="eyebrow">Koho zajišťujeme</p><h2>Pozice, které pro vás obsadíme</h2><ul class="list">{roles}</ul></div>'
            f'<div><p class="eyebrow">Pro koho</p><h2>Komu pomáháme</h2><p>{e(o["for"])}</p>'
            f'<p class="eyebrow" style="margin-top:34px">Do poptávky uveďte</p><ul class="list">{need}</ul></div>'
            '</div></section>' + steps_block() + faq_html + related_block(o["slug"]) + cta_block(o["select"]))
    service = {"@context": "https://schema.org", "@type": "Service", "name": o["select"], "serviceType": "Zajištění pracovníků — " + o["select"],
               "description": o["desc"], "url": f'{SITE}/{o["slug"]}', "areaServed": {"@type": "Country", "name": "Česká republika"},
               "provider": ORG}
    return page(slug=o["slug"], title=o["title"], desc=o["desc"], body=body, schemas=[service, crumbs_ld, faq_ld],
                select=o["select"], og_img=o["img"])


def how_page() -> str:
    crumbs_html, crumbs_ld = breadcrumbs([("Úvod", "/"), ("Jak to funguje", "/jak-to-funguje")])
    need = ["profese nebo pracovní pozice", "počet lidí — jednotlivec, nebo celá skupina", "místo výkonu práce", "termín nástupu a délku zakázky",
            "pracovní dobu a směnný režim", "požadavky na kvalifikaci, praxi a oprávnění"]
    why = [("Jeden kontakt", "Nemusíte obvolávat desítky lidí ani skládat partu po jednom. Řeknete, koho potřebujete, a my vám pracovníky zajistíme."),
           ("Rychlé sestavení", "Dokážeme rychle sestavit jednotlivce i celé pracovní skupiny, když potřebujete posílit provoz nebo stavbu."),
           ("Podle vašich požadavků", "Profese, počet lidí, místo výkonu práce i termín nástupu — tým skládáme přesně pro konkrétní zakázku."),
           ("Dlouholeté zkušenosti", "Zajišťování pracovníků se věnujeme dlouhodobě a známe potřeby stavebních, výrobních i zemědělských firem.")]
    faq_html, faq_ld = faq_block(COMMON_FAQ)
    steps = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in STEPS)
    body = (crumbs_html +
            '<section class="hero"><div class="container"><p class="eyebrow">Jak to funguje</p>'
            '<h1>Jak zajistíme pracovníky pro vaši firmu</h1>'
            '<p class="lede">Od poptávky po nástup na pracoviště — čtyři kroky a jeden kontakt. Takhle probíhá spolupráce s GLOBAL PETRO.</p>'
            f'<a class="btn" href="{poptat_href(None)}">Poptat pracovníky →</a></div></section>'
            f'<section class="block"><div class="container"><h2>Čtyři kroky ke spolupráci</h2><ol class="steps">{steps}</ol></div></section>'
            '<section class="block"><div class="container two">'
            '<div><p class="eyebrow">Poptávka</p><h2>Co nám napsat, abychom mohli rychle začít</h2>'
            f'<ul class="list">{"".join(f"<li>{e(n)}</li>" for n in need)}</ul></div>'
            '<div><p class="eyebrow">Proč GLOBAL PETRO</p><h2>Na čem stavíme</h2>'
            + "".join(f"<h3 style='margin-top:22px'>{e(t)}</h3><p>{e(d)}</p>" for t, d in why) +
            '</div></div></section>' + faq_html + related_block(None).replace("Další obory", "Obory, pro které zajišťujeme pracovníky")
            + cta_block(None))
    how = {"@context": "https://schema.org", "@type": "HowTo", "name": "Jak zajistit pracovníky přes GLOBAL PETRO",
           "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": d} for i, (t, d) in enumerate(STEPS)]}
    return page(slug="jak-to-funguje", title="Jak funguje zajištění pracovníků — 4 kroky | GLOBAL PETRO",
                desc="Jak probíhá zajištění pracovníků a pracovních skupin s GLOBAL PETRO: poptávka, upřesnění, výběr lidí a nástup. Co uvést do poptávky.",
                body=body, schemas=[how, crumbs_ld, faq_ld], select=None, og_img=None)


def faq_page() -> str:
    crumbs_html, crumbs_ld = breadcrumbs([("Úvod", "/"), ("Časté dotazy", "/caste-dotazy")])
    general = COMMON_FAQ + [
        ("Pro které obory pracovníky zajišťujete?",
         "Pro stavebnictví a rekonstrukce, zednické práce, pily a zpracování dřeva, výrobní a automobilové závody, potravinářský průmysl, zemědělství, svářečské a řemeslné profese a pro sklady a logistiku."),
        ("Co mám uvést v poptávce?",
         "Profesi, počet lidí, místo výkonu práce a termín nástupu. Pomůže i pracovní doba, směnný režim a požadavky na kvalifikaci."),
        ("Jak vás můžu kontaktovat?",
         f"Zavolejte na {PHONE}, napište na {EMAIL}, nebo vyplňte poptávkový formulář na webu."),
    ]
    by_obor = [(q, a) for o in OBORY for q, a in o["faq"]]
    all_items = general + by_obor
    gen_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in general)
    obor_html = "".join(
        f'<details><summary>{e(q)}</summary><p>{e(a)} <a href="/{o["slug"]}">Více o oboru {e(o["select"].lower())} →</a></p></details>'
        for o in OBORY for q, a in o["faq"])
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in all_items]}
    body = (crumbs_html +
            '<section class="hero"><div class="container"><p class="eyebrow">Časté dotazy</p>'
            '<h1>Časté dotazy k zajištění pracovníků</h1>'
            '<p class="lede">Odpovědi na otázky, které firmy kladou nejčastěji, než u nás poptají pracovníky nebo celou pracovní skupinu.</p></div></section>'
            f'<section class="block"><div class="container"><h2>Obecně</h2><div class="faq">{gen_html}</div></div></section>'
            f'<section class="block"><div class="container"><h2>Podle oboru</h2><div class="faq">{obor_html}</div></div></section>'
            + cta_block(None))
    return page(slug="caste-dotazy", title="Časté dotazy k zajištění pracovníků a skupin | GLOBAL PETRO",
                desc="Odpovědi na časté dotazy firem: jednotlivci i celé party, působnost po celé ČR, rychlost reakce a co uvést do poptávky pracovníků.",
                body=body, schemas=[data, crumbs_ld], select=None, og_img=None)


def main(site_dir: str) -> None:
    out = Path(site_dir)
    files = {o["slug"]: obor_page(o) for o in OBORY}
    files["jak-to-funguje"] = how_page()
    files["caste-dotazy"] = faq_page()
    for slug, html in files.items():
        (out / f"{slug}.html").write_text(html, encoding="utf-8")
        print(f"{slug}.html  {len(html.encode()) // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1])
