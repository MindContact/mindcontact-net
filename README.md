# mindcontact-net

Il sito www.mindcontact.net, la vetrina di MindContact. Statico, generato da
`tools/build.py`, pubblicato con GitHub Pages. Stato e decisioni in
`../mindcontact-identity/CONTEXT.md`.

## Struttura

```
docs/                 quello che va online (GitHub Pages)
  index.html, en/     home IT/EN, generate da tools/build.py
  hagalclinic/        pagina di Hagal+Clinic (en/hagalclinic/)
  sistemi-interattivi/  pagina dei sistemi interattivi (en/interactive-systems/)
  assets/             stile mobile-first, font, logo, site.js (menu)
  CNAME, .nojekyll    dominio e file serviti così come sono
tools/
  content.json        servizi, installazioni, progetti, testi delle pagine dedicate (IT/EN)
  build.py            rigenera tutte le pagine (elenco in PAGES) e sitemap.xml; testi fissi
```

## Lavorare in locale

```bash
python3 tools/build.py                 # dopo aver cambiato content.json o build.py
python3 -m http.server 8170 -d docs    # http://localhost:8170/
```

Controlla ogni modifica a 375, 768 e 1280 px nel Chrome "mc dev".

## Form di contatto

Il form è il widget di `../mindcontact-forms` (`<div data-mc-contact>` più
`https://forms.mindcontact.net/v1/widget.js`): modulo, informativa
(`#privacy-form`), anti-spam e registro dei consensi arrivano dal servizio.
I colori si impostano con le proprietà `--mcf-*` in `site.css`. Anteprima con
il servizio locale: `FORMS_URL=http://localhost:3300 python3 tools/build.py`.
Da dove vengono i progetti e cosa si può citare: `../mindcontact-identity/docs/portfolio.md`.

## Pubblicazione

GitHub Pages dal ramo `main`, cartella `docs/`: ogni push su `main` va online
da solo. Il dominio è in `docs/CNAME` (`www.mindcontact.net`, l'indirizzo
canonico del sito); `docs/.nojekyll` fa servire i file così come sono.

DNS (Cloudflare, solo DNS): `www` in CNAME verso `MindContact.github.io`,
`mindcontact.net` con i record A di GitHub Pages (GitHub lo reindirizza a
`www`).

Nessun indirizzo email nelle pagine.
