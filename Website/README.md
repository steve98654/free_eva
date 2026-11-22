# Free Eva website graphics

Matches the rally shirt: black #151515, Princeton orange #E77500, white. Fonts: Black Ops One, Big Shoulders Stencil Display, Noto Serif TC, VT323, Inter (all Google Fonts).

## Logo (`logo/`)
All SVG text is converted to outlines, so the SVGs render the same everywhere with no fonts installed.

| File | Use |
| --- | --- |
| `mark-dark` / `mark-light` | Icon only: an open orange ring (the door that should open) around a graduation cap. For dark / light backgrounds. |
| `app-icon` | Rounded black square with the mark. Favicon, social avatar, apple-touch-icon. |
| `logo-horizontal-dark` / `-light` | Site header lockup: mark + FREE EVA + 釋放謝翌 + WE ARE EVA. |
| `logo-stacked-dark` / `-light` | Square-ish lockup for posters, profile images, footers. |

## Hero graphics (`hero/`, 2400×1260, also work as 1.91:1 social share images)
- `hero-1-the-story.png`: "She went to a conference. She came home to detention." with a four-step timeline ending in "Detained by ICE".
- `hero-2-do-better.png`: "A student is not a threat. ICE: do better." with the three asks (release Eva, enforce with judgment, treat people with respect) and the line that we support the mission of immigration enforcement.
- `hero-3-we-are-eva.png`: 釋放謝翌 / FREE EVA with CHINA ⇄ US, 中美相互尊重, MUTUAL RESPECT, WE ARE EVA, evaxie.us.

## Source (`source/`)
`logo.py` builds the logo SVGs (needs fonttools and the font files); the hero `.html` files are 1600×840 pages rendered at 1.5× with `render.js` (Playwright). Font paths in `base.css` point at a local folder; swap them for Google Fonts links to edit elsewhere.
