// Central place for campaign details and swappable pieces.
//
// Anything marked TODO is a placeholder. Replace it with confirmed,
// public information only; the site shows placeholders in a dashed
// orange box so they are easy to spot before launch.

export const site = {
  name: 'Free Eva',
  nameZh: '釋放謝翌',
  domain: 'evaxie.us',
  tagline: 'A student is not a threat. Mutual respect is the basis for collaboration.',
  respectZh: '中美相互尊重',

  // LOGO: 中 / US yin-yang with the 13-star ring (see Website/logo-final). To swap it, drop a file in
  // /public/img/ and set `src` (for example '/img/logo-horizontal-dark.svg').
  // Set `src` to null to show the text placeholder instead.
  logo: {
    src: '/img/logo-header.svg' as string | null,
    alt: 'Free Eva 釋放謝翌',
  },

  // Links the campaign has not published yet. Leave as null until real.
  links: {
    petition: null as string | null, // TODO: petition URL
    legalFund: null as string | null, // TODO: legal defense fund URL
    rally: null as string | null, // TODO: rally / event details URL
    shop: null as string | null, // TODO: Bonfire campaign or store URL (Shop page shows a placeholder until set)
    email: 'weare@geo.partners',
  },
};

export const tabs = [
  { href: '/', label: 'Home', zh: '首頁' },
  { href: '/free-eva/', label: 'Free Eva', zh: '釋放謝翌' },
  { href: '/mutual-respect/', label: 'Mutual Respect', zh: '相互尊重' },
  { href: '/us-china/', label: 'US–China', zh: '中美友誼' },
  { href: '/shop/', label: 'Shop', zh: '義賣' },
  { href: '/contact/', label: 'Contact', zh: '聯絡' },
];
