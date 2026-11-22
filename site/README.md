# evaxie.us — Free Eva campaign site

Astro static site. Four tabs: **Home**, **Free Eva** (`/free-eva/`), **Mutual Respect** (`/mutual-respect/`), **US–China** (`/us-china/`).

```sh
cd site
npm install
npm run dev      # http://localhost:4321
npm run build    # static output in site/dist/
```

## Before launch
- **Placeholders**: unconfirmed details about Eva's case render in a dashed orange "TO CONFIRM" box. Find them all with `grep -rn "<Placeholder" src`. Only fill them with confirmed, public facts.
- **Links**: petition, legal fund and rally links live in `src/data/site.ts` (`links`). While a link is `null`, the page shows a placeholder instead. Contact email is `weare@geo.partners`.
- **Logo**: not chosen yet. The header shows a text placeholder. To swap, put the file in `public/img/` and set `site.logo.src` in `src/data/site.ts`.
- **Social image**: `public/img/og-image.png` (hero 3, "We are Eva").

## Style
Black `#151515`, Princeton orange `#E77500`, white. Fonts from Google Fonts: Black Ops One and Big Shoulders Stencil Display (stencil), Noto Serif TC (Chinese), Inter (body). Tokens are in `src/styles/global.css`.

## Deploying
`site/dist/` is plain static files; any static host works (Netlify, Vercel, Cloudflare Pages, GitHub Pages) with base directory `site`, build command `npm run build`, output `dist`.
