import { defineConfig, fontProviders } from 'astro/config';

export default defineConfig({
  site: 'https://joefazio.dev',

  // Astro downloads these at build time and serves them from joefazio.dev.
  // No request ever goes to Google's servers from a visitor's browser.
  fonts: [
    {
      provider: fontProviders.google(),
      name: 'Gabarito',
      cssVariable: '--font-display',
      weights: [500, 600, 700],
      styles: ['normal'],
      subsets: ['latin'],
    },
    {
      provider: fontProviders.google(),
      name: 'Inter',
      cssVariable: '--font-body',
      weights: [400, 500, 600],
      styles: ['normal'],
      subsets: ['latin'],
    },
  ],
});
