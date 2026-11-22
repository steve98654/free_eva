# Swag

## Bonfire (online shirt fundraiser)

Upload files for the rally shirt, made to Bonfire's artwork guidance (PNG, transparent background,
300 DPI, under 10 MB, inside the 11.5 x 14 in print area, 2 ink colors):

| File | Size | Prints at |
| --- | --- | --- |
| `bonfire/bonfire-front.png` | 3312 x 1712 px | about 11 x 5.7 in, chest |
| `bonfire/bonfire-back.png` | 3300 x 3312 px | about 11 x 11 in, upper back |

- Shirt color: black. Inks: orange #E77500 and white.
- The Princeton shield and fountain icons from the rally shirt are left off, because the university's
  marks can't be sold on merchandise without a license.
- `bonfire/shirt-mockup.png` is the front and back preview used on the site's Shop page.
- `bonfire/print-source.html` + `bonfire/render.js` regenerate the files (`node render.js`).

Once the campaign is live, put its URL in `site/src/data/site.ts` as `links.shop`.
