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

## More swag (`print/`, `digital/`)

Print items are drawn at 100 units per inch and rendered at 300 DPI. SVGs are outlined, so no fonts are needed.

| Item | Files | Size | Suggested printer |
| --- | --- | --- | --- |
| Buttons | `print/button-orange`, `print/button-black` | 2.25 in round (add the printer's bleed) | Sticker Mule |
| Enamel pin | `print/enamel-pin` | 1.25 in; black + orange enamel, gold metal | Sticker Mule or any pin maker |
| Tote bag | `print/tote-black-ink`, `print/tote-orange-ink` | 10 x 11 in, one ink | Bonfire, Custom Ink, Printful |
| Hat | `print/hat-front-embroidery`, `print/hat-back-embroidery` | 2.25 in front, 3 in back, one thread color | Custom Ink or any embroiderer |
| Pen | `print/pen-imprint` | 2 x 0.3 in, one ink | 4imprint, Vistaprint |
| Phone wallpaper | `digital/wallpaper-phone.png` | 1290 x 2796 | free download |
| Video call background | `digital/video-background-dark.png`, `-light.png` | 1920 x 1080 | free download |

Stickers use `Website/logo-final/extras/sticker-round`. Hoodies and long sleeves use the shirt files in `bonfire/`.
Regenerate with `python3 source/swag.py <print-dir> <digital-dir>` (fonts path set in `source/logo.py`), then `node source/render.js <dir> 3`.
