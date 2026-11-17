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
    /* THESE FOUR ARE UNVERIFIED. youtube.com is blocked from the session that
       added them, so each ID comes from an indexed search result (title +
       description), not from opening the video. Click each once and confirm
       it is the right song AND an official upload, then delete this note. */

    // "Michael Franti and Spearhead - Say Hey (I Love You) [Music Video] [HQ]"
    // Described as the video from the album All Rebel Rockers.
    'JBM—001': 'https://www.youtube.com/watch?v=MKHlXEVYOuY',

    // "Michael Franti & Spearhead - The Sound Of Sunshine"
    // Carries a 2010 Boo Boo Wax copyright line. Strongest of the four.
    'JBM—002': 'https://www.youtube.com/watch?v=KqgHosrqJ8o',

    // '"Life Is Better With You" - Official Music Video, Michael Franti'
    // Least certain: a separate upload (LFS4jaWlhrA) carries the Boo Boo
    // Wax / Capitol copyright line but is a LYRIC video, not the film.
    'JBM—003': 'https://www.youtube.com/watch?v=1XEOVl875d0',

    // "Michael Franti & Spearhead - I'm Alive (Life Sounds Like)"
    // 2013, first single from All People. Directed by Zach Merck.
    'JBM—004': 'https://www.youtube.com/watch?v=Fw0oOjZydZY',

    // Cake album, not a single — needs a specific track video, or leave empty.
    'JBM—005': ''
  }
};
