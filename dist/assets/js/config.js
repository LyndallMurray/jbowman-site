/* ===========================================================================
 * J BOWMAN — site configuration
 * THE ONLY FILE THAT NEEDS EDITING TO GO LIVE.
 * ======================================================================== */
window.JB_CONFIG = {

  /* REQUIRED — where professional enquiries should land. Until this is set,
     the Connect form says so plainly rather than swallowing an enquiry. */
  contactEmail: '',          // e.g. 'management@jbowman.com'

  /* OPTIONAL — a POST endpoint (Formspree, Basin, Netlify Forms, your own).
     Set: the form posts there and the visitor stays on the page.
     Empty: falls back to opening their mail client, pre-filled. */
  formEndpoint: '',

  /* OPTIONAL — profiles. Any left empty render as plain text, never dead links. */
  social: { instagram: '', spotify: '', imdb: '', linkedin: '' },

  /* -------------------------------------------------------------------------
   * TRACK VIDEOS
   *
   * Paste the whole YouTube URL — any form works, the ID is pulled out of it:
   *   https://www.youtube.com/watch?v=XXXXXXXXXXX
   *   https://youtu.be/XXXXXXXXXXX
   *   https://www.youtube.com/embed/XXXXXXXXXXX
   *
   * The key is the catalogue number shown on the left of each row on the Work
   * page. A row left empty grows no Watch control and renders exactly as it
   * does now, so the page is never half-built.
   *
   * Use the OFFICIAL artist or label upload, not a fan re-upload: those get
   * taken down and the embed dies silently with them. Open each link once
   * before pasting and check the channel is Michael Franti & Spearhead (or
   * their label), not a lyric-video or reaction channel.
   * ---------------------------------------------------------------------- */
  tracks: {
    'JBM—001': '',   // "Say Hey (I Love You)"        — Michael Franti & Spearhead
    'JBM—002': '',   // "The Sound of Sunshine"       — Michael Franti & Spearhead
    'JBM—003': '',   // "Life Is Better With You"     — Michael Franti & Spearhead
    'JBM—004': '',   // "I'm Alive (Life Sounds Like)"— Michael Franti & Spearhead
    'JBM—005': ''    // Prolonging the Magic          — Cake (album, not a single)
  }
};
