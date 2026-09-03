# J Bowman brand guidelines

_Started 2026-09-03 05:31 UTC_

---

## User

Create a brand guideline for J BOWMAN

## Assistant



## Assistant

Before I build — a few calls that change the shape of the deliverable.

_[tool: ask_user]_

_[tool: ask_user]_

Form's up — waiting on format, lead route, colour and how to treat the photos before I start building.

## User

Answered — format: Long-scroll interactive brand site; route: Show all three as moodboard routes, no single winner yet; sections: Positioning, Personality & voice, Logo architecture, Typography, Colour, Image world, Graphic language, Fashion extension, Digital wrap, Applications; logo: J BOWMAN in the logo and JB ... find the right colour lead colour is in the purple range build the rest off of that but get the purple right for a rockstar that leans into feminine but is still a bro

## Assistant

_[tool: list_files]_

_[tool: view_image]_

_[tool: view_image]_

_[tool: view_image]_

_[tool: view_image]_

_[tool: copy_files]_

_[tool: dc_write]_

_[tool: ready_for_verification]_

Long-scroll brand site, ink and bone, Belleza + Montserrat, with all three routes shown at moodboard level and no winner picked.

On the purple: I built a "getting the purple right" panel with three real candidates and a recommendation — **Bruised Plum #6E2A5C** as lead (violet with red under it: reads taste on cream, oxblood in low light), with Iris #4A2E86 and Ultra Magenta #96206A as the cooler and hotter alternates. Tell me which one and I'll rebuild the whole system around it.

Your photos are the image world — grayscale by default, colour on hover. Logo section uses J BOWMAN wordmark plus a JB monogram (switchable to JBM in tweaks).

## User

Found issues — fixing…

## User

Found issues — fixing…

## User

Page 3 image B is not J select another - image C replace first attachment,. Logo Love the font but can you illistrate slightly so there is some individuality to the typeface a hint of movement but not like a horror show type that would be too far. Page 07 image 3 from left put J in the frame more you have the lead singer mostly in the frame ... come up with a tage line based on the original bio

## Assistant

_[tool: copy_files]_

_[tool: dc_js_str_replace]_

_[tool: dc_js_str_replace]_

_[tool: run_script]_

_[tool: view_image]_

_[tool: run_script]_

_[tool: view_image]_

_[tool: run_script]_

_[tool: view_image]_

Good — J is now the subject. Updating the sheet and the social square.

_[tool: dc_js_str_replace]_

_[tool: dc_html_str_replace]_

_[tool: dc_html_str_replace]_

_[tool: dc_html_str_replace]_

_[tool: dc_set_props]_

_[tool: dc_js_str_replace]_

_[tool: dc_js_str_replace]_

_[tool: ready_for_verification]_

Four changes:

**Routes** — B is now the truck-jump frame, C is your new attachment. The frame that wasn't J is out of the document entirely.

**Wordmark** — letters rotated no more than 1.4° and shifted a fraction off the baseline, with two glyphs slightly narrowed. Straight and editorial at distance, moving slightly out of step up close. There's a before/after specimen next to it so you can judge the amount; say the word and I'll push it further or pull it back.

**Image world, third tile** — recropped onto J rather than the two of them.

**Tagline** — lead is *Written, played, recorded, mixed.* Four words taken straight from the bio: songwriter, musician, producer, engineer. Two alternates sit beside it (*Chicago instincts. Bay Area craft.* and *Decades inside the record. One point of view.*). The lead now runs in the hero too.

## User

Found issues — fixing…

## Assistant

_[tool: run_script]_

_[tool: view_image]_

_[tool: dc_js_str_replace]_

Now the wordmark word space and the hero line breaks.

_[tool: dc_html_str_replace]_

_[tool: dc_html_str_replace]_

_[tool: ready_for_verification]_

Fixed: word space restored between J and BOWMAN in both wordmark instances, hero name set to no-wrap at a smaller clamp so it reads as two lines, and the duplicated seated frame in the contact sheet replaced with a stage frame cropped onto J.

The two console messages are placeholder image requests the streaming loops make before values resolve — no visual effect, and removing them would cost the placeholder rows that make the page paint early. Leaving them.

## User

revert back to the original logo. Attached page 1  delete the background of the image so the background all blends and there is no line down the  middle of the image and the page of black or update the background to the same colour asd the image background so it is consistent. Do a run through of all the copy and make sure it links back to the bio ... replace Confidential creative direction with the tag line

## Assistant

_[tool: read_skill_prompt]_

_[tool: run_script]_

_[tool: run_script]_

_[tool: run_script]_

Now the hero, the reverted wordmark, and the copy pass.

_[tool: dc_html_str_replace]_

_[tool: dc_html_str_replace]_

Reverting the wordmark to plain Belleza and removing the letterform comparison.

_[tool: dc_html_str_replace]_

_[tool: dc_html_str_replace]_

_[tool: grep]_

_[tool: read_file]_

_[tool: dc_html_str_replace]_

_[tool: dc_html_str_replace]_

_[tool: ready_for_verification]_

Done:

**Logo** back to plain Belleza — the illustrated version and its comparison block are gone.

**Hero** — the divider line is removed and the portrait is now a processed PNG: shadows pulled down to match the page ink and the left edge feathered to transparent over 22%, so the photo dissolves into the background with no seam or colour step.

**Copy pass against the bio** — the proof band is rebuilt from it: origin (Chicago → Bay Area, Sandy Pearlman with his credits), the collaborator list corrected to Thievery Corporation / Rob Garza, the full screen list including Magnum PI, Hawaii Five-O, CMT Top 20, Ida Red, Kiss Kiss Bang Bang, Yogi Bear, Hall Pass and Cutlass, commercials including Slim Fast, LCBO/Crown Agency, Vegas Golden Knights and Denver Broncos, and records now carrying real chart peaks — Say Hey #18 Hot 100, Sound of Sunshine #1 Adult Alternative, Prolonging the Magic #33 Billboard 200.

**Hero eyebrow** is now the tagline.

## User

update the first page and update any other messaging through with this SOUND THAT MOVES THROUGH CULTURE.

J BOWMAN

Multi-platinum, Grammy-nominated songwriter, composer, producer, musician and engineer.

From charting records to film, television and global brands, J Bowman creates sound with feeling, identity and lasting cultural impact.

Written. Played. Produced. Scored. Recorded. Mixed.

## Assistant

_[tool: dc_html_str_replace]_

_[tool: dc_html_str_replace]_

Now the essence, tagline block and brand-line list.

_[tool: dc_html_str_replace]_

_[tool: dc_html_str_replace]_

_[tool: dc_html_str_replace]_

_[tool: dc_js_str_replace]_

_[tool: dc_set_props]_

_[tool: dc_html_str_replace]_

_[tool: dc_html_str_replace]_

_[tool: dc_set_props]_

_[tool: dc_js_str_replace]_

_[tool: ready_for_verification]_

Page one is now your copy verbatim: the tagline as the eyebrow, J BOWMAN, the credentials line, the records-to-brands sentence, and the six-word descriptor under the rule.

Carried through: brand essence is now *Sound that moves through culture*, the photo overlay matches it, the tagline block leads with it (with the six-word descriptor documented beneath as the lockup line), and it sits at 01 in the brand-lines list with *Sound with a point of view* held as the alternate.

## User

<pasted_text name="Pasted text (274 lines)">
WEBSITE STRATEGY &amp; CREATIVE BRIEF

J BOWMAN

A digital platform for sound, story and cultural collaboration

LEAD PROPOSITION

SOUND THAT MOVES THROUGH CULTURE.

Website objective: turn an exceptional body of work into a current, compelling and commercially effective global presence.

MASTER BRAND

J BOWMAN

Writer | Composer | Producer | Musician | Sound Engineer


CONFIDENTIAL CREATIVE DIRECTION  |  SEPTEMBER 2026

J BOWMAN  /  WEBSITE BRIEF

1. Project Overview

Create a premium, contemporary website that positions J Bowman as a multi-disciplinary creator working across records, film, television, advertising, brands and culture. The website must honour a multi-platinum, Grammy-nominated career while making the work feel active, relevant and ready for new commissions.

THE CHALLENGE  Much of J Bowman’s authority currently lives inside credits, relationships and past projects. The website must translate that authority into a concise digital experience that new decision-makers can understand immediately.

THE OPPORTUNITY  Build a platform that operates as portfolio, showreel, editorial world and business-development tool—without looking like a conventional recording-studio website.

THE SHIFT  From a career represented by a biography and credit list to a visible creative identity with an ownable point of view.

PRIMARY DESIGN TEST

Within 30 seconds, can a music supervisor, director, artist or creative lead understand who J Bowman is, feel the calibre of the work and know how to engage him?

2. Website Objectives

POSITION  Establish J Bowman as a current creative auteur with rare breadth across songwriting, composition, production, musicianship, engineering and sound for picture.

PROVE  Use carefully selected work, credible credits and role clarity to demonstrate experience without overwhelming visitors.

CONVERT  Generate qualified enquiries for original composition, sync, production, songwriting, engineering, mixing and cultural or fashion collaborations.

EXPAND  Open pathways into advertising, branded entertainment, sonic identity, runway, fashion film, installations and creative partnerships.

OWN  Create a direct audience and discovery platform that is not dependent on social algorithms or third-party music profiles.

3. Priority Audiences

PRIMARY COMMISSIONERS  Music supervisors, directors, producers, production companies, advertising creatives, agencies, networks, streaming platforms and brand content teams.

MUSIC INDUSTRY  Artists, managers, publishers, labels, producers and collaborators looking for writing, production, performance, engineering or mix expertise.

CULTURE &amp; FASHION  Fashion designers, creative directors, photographers, luxury and lifestyle brands, runway producers, experiential teams and cultural institutions.

MEDIA &amp; COMMUNITY  Journalists, curators, musicians, listeners, collectors and people discovering the person and process behind the work.

4. Brand and Messaging Hierarchy

HOMEPAGE HEADLINE

SOUND THAT MOVES THROUGH CULTURE.

MASTER WORDMARK  J BOWMAN. “Music” must not appear as part of the logo or master wordmark.

CREDENTIAL LINE  Multi-platinum, Grammy-nominated songwriter, composer, producer, musician and sound engineer.

SUPPORTING COPY  From charting records to film, television and global brands, J Bowman creates sound with feeling, identity and lasting cultural impact.

PROCESS LINE  Written. Played. Produced. Scored. Recorded. Mixed.

PRIMARY CTA  Explore the work.

SECONDARY CTA  Start a project.

VOICE  Assured, cultured, precise and human. Lead with creative value and emotion; use credits as proof. Avoid generic studio language, inflated superlatives and nostalgia-led positioning.

5. Recommended Site Architecture

HOME  Immersive introduction, hero reel, positioning, selected work, discipline pathways, cultural proof and direct enquiry.

WORK  Filterable portfolio organised around Records, Picture and Brands/Culture—not a chronological archive.

PROJECT  Individual case-study template with media, brief, idea, J Bowman’s precise role, collaborators, outcome and related work.

ABOUT  Concise current biography, portraiture, career arc, selected collaborators and a link to the full credit index.

SERVICES  Clear commissioning pathways for Original Composition, Songwriting, Production, Engineering &amp; Mix, Performance and Sonic/Creative Collaboration.

ARCHIVE / JOURNAL  Curated stories, process, artefacts, observations and selected historic material framed through a present-day perspective.

CONTACT  Short project enquiry with direct email alternative, representation details if applicable and links to professional channels.

OPTIONAL: LISTENING ROOM  A curated, rights-cleared collection of musical fragments, themes, alternate versions and experiments presented as an editorial experience.

6. Homepage Experience

01 / Opening Frame

Full-viewport cinematic opening with the J BOWMAN wordmark, the headline “Sound that moves through culture,” a concise credential line and immediate access to the hero reel. Sound must be opt-in, never autoplay unexpectedly.

02 / Hero Reel

A 60–90 second showreel moving across records, film, television, brands and performance. Show J Bowman’s role on-screen so the visitor never has to infer his contribution.

03 / Positioning

A short statement establishing the crossover between songwriting instinct, engineering craft and storytelling for image. Pair with one current portrait or studio sequence.

04 / Selected Work

Six to nine hero projects using strong imagery and video. Allow visitors to browse by Records, Picture and Brands/Culture while keeping the first experience editorial rather than database-like.

05 / Proof

A restrained selection of recognised collaborators, chart achievements, screen placements and brand work. Avoid a crowded logo wall; use names and projects with accurate role descriptions.

06 / Disciplines

Present the ways to work with J Bowman as creative outcomes, not a commodity service menu. Each pathway should lead to relevant proof and a specific enquiry prompt.

07 / Current Signal

Feature current work, an observation, an archive story or a new sonic experiment to demonstrate that the practice is active now.

08 / Conversion

Close with a confident invitation: “Bring me the idea. We’ll find its sound.” Link to a short, low-friction project enquiry.

7. Portfolio and Case-Study System

SELECTION  Launch with 6–10 hero projects. Choose for relevance, range, recognisability, visual material and clarity of J Bowman’s contribution—not fame alone.

CASE-STUDY FIELDS  Project title; client/artist; year; category; brief or context; creative idea; J Bowman’s role; collaborators; audio/video; outcome; credits; related work.

ROLE CLARITY  Use explicit role tags such as Songwriter, Composer, Producer, Engineer, Mixer, Guitarist or Sync. Do not imply authorship beyond the documented contribution.

MEDIA  Prioritise embedded video, high-quality audio, full-screen stills, annotated process materials and short written context. Provide captions and transcripts where relevant.

RIGHTS  Every asset must be rights-cleared. Establish an approval register for music, stems, video, stills, logos, press quotes, client names and collaborator references before publication.

8. Content Requirements

COPY  Homepage copy; short and long biographies; discipline descriptions; 6–10 project summaries; 3–5 full case studies; enquiry prompts; metadata; privacy and terms.

PHOTOGRAPHY  One art-directed portrait and studio shoot covering hero landscape, portrait, close detail, negative-space crops, vertical social and monochrome options.

VIDEO  Master reel, discipline-specific reel cuts, silent homepage loop, interview excerpts, studio process and vertical edits.

AUDIO  Rights-cleared stereo masters, consistent loudness, optional excerpts, waveform-free player design, track credits and accessible text alternatives.

ARCHIVE  Curated contact sheets, session images, handwritten material, studio artefacts, press and approved historic footage. Use selectively and contextualise in the present.

CREDITS DATABASE  A searchable or filterable full-credit index can sit below the editorial portfolio, keeping depth available without overwhelming the primary journey.

9. Visual and Interaction Direction

The website should feel like the intersection of an independent record imprint, a fashion editorial and a contemporary film studio. It must be visually confident, tactile and restrained—never a theme-driven “music website.”

TYPOGRAPHY  An expressive editorial display face paired with a highly legible contemporary sans serif. J BOWMAN must hold authority without decorative music references.

PALETTE  Black, bone, smoke and warm white, with one deep signature accent such as oxblood. The site must work beautifully in monochrome.

IMAGE  Cinematic portraiture, deep shadows, imperfect crops, hard flash used sparingly, studio texture, contact sheets and present-day fashion composition.

GRAPHIC SYSTEM  Negative space, catalogue numbering, track metadata, modular frames, controlled grain and subtle editing or signal-flow references—without literal waveforms.

MOTION  Slow confidence punctuated by sharp editorial cuts. Motion should support hierarchy and rhythm, never delay access or imitate a music visualiser.

FASHION READINESS  Layouts and imagery should translate naturally into lookbooks, garment labels, campaign treatments, event screens and physical editions.

10. Functional Requirements

CMS  Simple management of projects, credits, categories, journal entries, media and featured content without developer assistance.

MEDIA PERFORMANCE  Adaptive image and video delivery, poster frames, lazy loading, compressed audio and clear play controls. Protect Core Web Vitals and mobile performance.

FILTERING  Work filters by discipline and project type, with human-readable URLs and no dead-end results.

ENQUIRY  Short form capturing name, organisation, email, project type, timing, budget range and message. Route submissions reliably and include spam protection.

ANALYTICS  Privacy-conscious analytics for reel plays/completions, portfolio views, CTA clicks, enquiry starts/submissions, source channel and device.

SEO  Editable titles/descriptions, schema markup, Open Graph imagery, XML sitemap, canonical URLs, redirects, image alt text and indexable project copy.

SOCIAL  Platform-ready share cards, clean video thumbnails and consistent links to relevant professional profiles.

11. Accessibility, Privacy and Standards

ACCESSIBILITY  Target WCAG 2.2 AA: keyboard operation, visible focus, accessible contrast, scalable text, labelled controls, captions, transcripts, alt text and reduced-motion support.

SOUND  No forced audio. Clearly visible play/pause, mute and volume controls. The complete site must remain understandable without sound.

PRIVACY  Collect only necessary enquiry information; publish a clear privacy notice; configure consent appropriately for analytics and embeds.

RESPONSIVE  Design and test mobile-first across current iOS/Android devices, tablets, laptops and large displays.

OWNERSHIP  J Bowman must retain access to the domain, CMS, analytics, hosting, source files, font and media licences, and all approved design assets.

12. Search and Market Penetration

DISCOVERY THEMES  J Bowman songwriter; composer for film and television; music producer; sound engineer; sync composer; custom music for brands; sonic identity; fashion film music.

AUTHORITY CONTENT  Publish selective case studies and editorial pieces that demonstrate process, role and creative thinking—not generic SEO articles.

OUTREACH LANDING  Create campaign-ready project URLs and, if required, tailored private or public landing pages for screen, brands, records and fashion.

CROSS-CHANNEL SYSTEM  Ensure website, LinkedIn, Vimeo/YouTube, social profiles, EPK, email signature and pitch materials use the same wordmark, headline, role language and project taxonomy.

LEAD CAPTURE  Primary conversion is a qualified project enquiry. Newsletter capture is secondary and should only be used if there is a genuine editorial or release cadence.

13. Deliverables Expected from the Agency

STRATEGY  Discovery, competitor and category review, refined sitemap, audience journeys, content model, SEO framework and measurement plan.

UX  Wireframes for all core templates, mobile and desktop journeys, portfolio filtering, media behaviour and enquiry flow.

UI  High-fidelity responsive designs, component library, interaction and motion specifications, accessibility states and developer-ready source files.

DEVELOPMENT  CMS build, front-end implementation, media optimisation, integrations, analytics, technical SEO, testing, redirects and launch support.

CONTENT SUPPORT  Content matrix, asset specifications, migration, copy population and clear identification of missing or uncleared material.

HANDOVER  Training, documentation, source repository, licences, credentials, backups, warranty period and ongoing support options.

14. Acceptance Criteria

CLARITY  A first-time visitor understands J Bowman’s role, stature and creative offer within 30 seconds.

WORDMARK  The master logo is J BOWMAN. “Music” is never incorporated into the wordmark.

PROOF  All published credits and roles have been verified and approved.

CONVERSION  Every core page provides a relevant next action and the enquiry process works across devices.

PERFORMANCE  Media-rich pages remain fast, stable and usable on mobile connections.

ACCESSIBILITY  Keyboard, screen-reader, contrast, caption, transcript and reduced-motion checks pass before launch.

CONTROL  The owner can update projects, credits, media and editorial content without technical support.

15. Decisions Required Before Design

PRIORITY OFFER  Rank the first-year focus: screen composition and sync; records and artist work; brands and sonic identity; culture and fashion collaboration.

PUBLIC PERSONA  Confirm how visible J Bowman should be on camera and how much the experience should be personality-led versus work-led.

HERO MEDIA  Select whether launch leads with a new master reel, an original sonic/visual ident or a commissioned portrait film.

PORTFOLIO  Approve launch projects and establish the exact role, rights and available media for each.

CONTACT MODEL  Confirm direct contact, management or representation pathway and whether budget guidance is included in the form.

PLATFORM &amp; HOSTING  Agency to recommend based on editorial flexibility, media performance, owner control, security and total cost—not design preference alone.

16. Indicative Delivery Phases

PHASE 01 — FOUNDATION  Discovery, asset and rights audit, objectives, audience journeys, sitemap, content model and measurement plan.

PHASE 02 — EXPERIENCE  Messaging refinement, wireframes, portfolio architecture, content planning and technical definition.

PHASE 03 — DESIGN  Visual system, responsive interface, motion language, prototype and usability/accessibility review.

PHASE 04 — BUILD  CMS development, integrations, content population, media optimisation, SEO and analytics implementation.

PHASE 05 — LAUNCH  Quality assurance, approvals, redirects, training, deployment and a coordinated reel/content/outreach release.

PHASE 06 — GROWTH  Monthly content rhythm, performance reporting, conversion refinement, new case studies and targeted market landing pages.

FINAL MANDATE

Build a digital world that makes the career credible, the work immediate and the next collaboration easy to begin.
</pasted_text>

## Assistant



## Assistant

_[tool: grep]_

_[tool: run_script]_

_[tool: dc_set_props]_

_[tool: ready_for_verification]_

I applied the hard rulings from the new brief to the guideline: master wordmark is J BOWMAN with the word Music removed from every lockup, the descriptor is now Writer · Composer · Producer · Musician · Sound Engineer, the credential line says sound engineer, and the "open decision" on the name is now recorded as settled.

The rest of the website brief is a separate deliverable — before I build it:

_[tool: ask_user]_

Waiting on those three before I build the website brief.

## User

Answered — shape: Designed homepage screens — build section 6 as actual page mockups; depth: All 16 sections; audience: J Bowman to approve

## Assistant

_[tool: dc_write]_

_[tool: ready_for_verification]_

Built as a second document — **J Bowman Website Brief** — all sixteen sections, same system as the guidelines.

Section 6 is drawn rather than described: eight designed homepage frames in scroll order (opening, hero reel with role captions, positioning split, filterable work grid, proof table with real chart peaks, disciplines with enquiry prompts, journal signal, and the plum conversion frame carrying *Bring me the idea. We'll find its sound.*), each with the brief's guidance beside it.

Section 15 is the plum full-bleed moment since it's the part needing your decisions. The wordmark rule — J BOWMAN, never with Music — is stated in both the messaging hierarchy and the acceptance criteria.

