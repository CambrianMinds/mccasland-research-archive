const timelineData = [
  {
    date: "1979-2013",
    category: "public-record",
    title: "McCasland's documented USAF career",
    detail: "Public records place McCasland inside the Office of Special Projects, Space-Based Laser, OSD special programs, SAPOC, and AFRL leadership before retirement."
  },
  {
    date: "Jan. 24-25, 2016",
    category: "public-record",
    title: "McCasland appears directly in the Podesta / DeLonge thread",
    detail: "WikiLeaks captures show direct replies from Neil McCasland and a separate invitation acceptance from Susan McCasland Wilkerson."
  },
  {
    date: "Dec. 30, 2023",
    category: "tmb",
    title: "KC-135 sketch enters the archive",
    detail: "The account posts a hand-drawn observation allegedly from 1998, using Crookes-dark-space plasma language and, later, a reverse-side component inventory."
  },
  {
    date: "Nov. 2024",
    category: "forbes",
    title: "Forbes says the schematic was sent to him",
    detail: "On camera, Ashton Forbes states the hand-drawn schematic was a direct message from the account and dates it to November 2024."
  },
  {
    date: "Aug. 24, 2025",
    category: "nuclear",
    title: "Yamantau / CTR post",
    detail: "The account claims a personal visit to Yamantau during the Threat Reduction Program and gives a highly specific Radioalumina timeline."
  },
  {
    date: "Nov. 17, 2025",
    category: "nuclear",
    title: "Induced-nuclear threat post",
    detail: "Replying to Ashton Forbes, the account says Russia has a major artificial induced-nuclear material production line with xenon leakage as a signature."
  },
  {
    date: "Feb. 13-27, 2026",
    category: "trail",
    title: "Disclosure sprint across propulsion, materials, and field geometry",
    detail: "The post stream compresses into a rapid sequence on local fields, pumpable plasma, electret coatings, ceramics, inertia-less equilibrium, and 'modern spacecraft.'"
  },
  {
    date: "Feb. 24, 2026",
    category: "trail",
    title: "Modern spacecraft post",
    detail: "One recovered image shows an unidentified green pod-like object in a hangar; the other is a book cover tied to electrostatic swarm-navigation literature."
  },
  {
    date: "Feb. 27, 2026",
    category: "disappearance",
    title: "Final posting window overlaps the disappearance window",
    detail: "The final standalone post lands at roughly 11:28 a.m. MST, inside the same public window in which McCasland's disappearance is being reconstructed."
  },
  {
    date: "Mar. 6-16, 2026",
    category: "disappearance",
    title: "Search reporting expands",
    detail: "KOAT, ABC, Fox, and others add repairman timing, missing items, FBI involvement, Silver Alert context, and a still-open search."
  },
  {
    date: "Apr. 15-16, 2026",
    category: "research",
    title: "Archive consolidation and Sentinel findings",
    detail: "The local archive, the LaTeX report, and the Sentinel investigations sharpen the public-record lane, the schematic lane, and the attribution caveats."
  }
];

const timelineFilters = [
  { id: "all", label: "All" },
  { id: "public-record", label: "Public Record" },
  { id: "disappearance", label: "Disappearance" },
  { id: "tmb", label: "TMB Account" },
  { id: "forbes", label: "Forbes" },
  { id: "nuclear", label: "Nuclear" },
  { id: "trail", label: "Trail Analysis" },
  { id: "research", label: "Archive Build" }
];

const claims = [
  {
    claim: "McCasland definitively operated @TMBSpaceships",
    assessment: "unproven",
    label: "Not established",
    reason: "No primary source in the archive ties McCasland's known accounts, devices, or official statements directly to the handle."
  },
  {
    claim: "McCasland had the kind of access envelope the account implies",
    assessment: "supported",
    label: "Strongly supported",
    reason: "Public records place him in SAPOC, OSD special programs, Space-Based Laser, AFRL, and the Harvard U.S.-Russia Security Program."
  },
  {
    claim: "The schematic reflects real engineering knowledge",
    assessment: "supported",
    label: "Supported",
    reason: "The materials, components, and operating concepts line up with recognizable plasma, MHD, and high-temperature-engineering ideas rather than empty jargon."
  },
  {
    claim: "The schematic proves the account belonged to McCasland",
    assessment: "unproven",
    label: "Not established",
    reason: "The schematic is a strong bridge document, but consistency of subject matter and handwriting style is not direct authorship proof."
  },
  {
    claim: "The final-post timing is relevant",
    assessment: "supported",
    label: "Supported",
    reason: "The final standalone post lands inside the same public window in which McCasland's movements are otherwise unaccounted for."
  },
  {
    claim: "The Feb. 24 images show two identifiable classified craft",
    assessment: "contested",
    label: "Not supported",
    reason: "Only one image is a craft-like object; the other is clearly bibliographic and tied to electrostatic spacecraft swarm literature."
  },
  {
    claim: "The xenon framing automatically verifies the Yamantau claim",
    assessment: "caution",
    label: "Not established",
    reason: "CTBTO noble-gas monitoring is real, but public-access material in this archive does not independently verify the specific production-line allegation."
  },
  {
    claim: "The KC-135 reverse-side parts list points to a specific known black program",
    assessment: "circumstantial",
    label: "Partially answerable",
    reason: "The components map well to pulsed-power, accelerator, and advanced-fusion hardware families, but not to one uniquely identified program."
  },
  {
    claim: "Forbes had direct evidence the account and McCasland were linked",
    assessment: "circumstantial",
    label: "Circumstantial",
    reason: "Forbes confirms the schematic came from the account, but that is not the same thing as confirming McCasland was the account owner."
  },
  {
    claim: "The spelling errors are evidence of technical ignorance",
    assessment: "contested",
    label: "Not supported",
    reason: "The corpus itself says the errors are purposeful, and the near-miss pattern usually preserves the technical term's meaning."
  }
];

const claimFilters = [
  { id: "all", label: "All" },
  { id: "supported", label: "Supported" },
  { id: "circumstantial", label: "Circumstantial" },
  { id: "unproven", label: "Unproven" },
  { id: "contested", label: "Contested" },
  { id: "caution", label: "Caution" }
];

const galleryItems = [
  {
    title: "Hand-drawn schematic",
    caption: "The most important bridge document in the archive: the plasma-alternator / ion-pumpy sketch Forbes says was sent to him directly.",
    src: "./assets/media/schematic.png",
    alt: "Hand-drawn schematic labeled closed cycle plasma amplifier and dynamic plasma alternator"
  },
  {
    title: "McCasland AFRL portrait",
    caption: "The public-record anchor image: McCasland in his AFRL commander role.",
    src: "./assets/media/mccasland-afrl.jpg",
    alt: "Official portrait of Neil McCasland in Air Force uniform"
  },
  {
    title: "Modern spacecraft image 1",
    caption: "Recovered from the Feb. 24 post. It has not been matched to a confirmed public program in this archive.",
    src: "./assets/media/modern-spacecraft.jpg",
    alt: "Green spherical or pod-like object in a hangar with a U.S. flag in the background"
  },
  {
    title: "Modern spacecraft image 2",
    caption: "Also from the Feb. 24 post, but actually a book cover tied to electrostatic swarm-navigation literature.",
    src: "./assets/media/modern-spacecraft-2.png",
    alt: "Book cover titled Electrostatic Forces for Swarm Navigation and Reconfiguration"
  },
  {
    title: "Magnetic stochastics",
    caption: "One of the image-only posts anchoring the materials / field-geometry thread in February 2026.",
    src: "./assets/media/magnetic-stochastics.jpg",
    alt: "Research image labeled magnetic stochastics"
  },
  {
    title: "Electro-acoustic waves",
    caption: "Part of the late-stage technical posting sequence on waves, polarization force, and plasma behavior.",
    src: "./assets/media/electro-acoustic-waves.jpg",
    alt: "Research image about electro-acoustic waves in presence of polarization force"
  },
  {
    title: "Muon-catalyzed fusion",
    caption: "A representative image from the fusion and nuclear cluster that appears in the final post sequence.",
    src: "./assets/media/muon-catalyzed-fusion.png",
    alt: "Research image about muon-catalyzed fusion and polarized nuclei"
  }
];

const sources = [
  {
    title: "Findings Report PDF",
    type: "Report",
    description: "The full 29-page compiled report synthesizing the local archive, timeline, schematic analysis, claim matrix, and source appendix.",
    href: "./assets/docs/findings-report.pdf"
  },
  {
    title: "Official Air Force biography",
    type: "Primary source",
    description: "The strongest public institutional anchor for McCasland's career.",
    href: "https://www.af.mil/About-Us/Biographies/Display/Article/104776/"
  },
  {
    title: "Wikipedia biographical article",
    type: "Context",
    description: "Useful for assembling the broader career chronology, including SAPOC, Space-Based Laser, and Harvard Kennedy School.",
    href: "https://en.wikipedia.org/wiki/Neil_McCasland"
  },
  {
    title: "WikiLeaks email 5078",
    type: "Primary source",
    description: "Direct McCasland reply in the DeLonge / Podesta meeting thread.",
    href: "https://wikileaks.org/podesta-emails/emailid/5078"
  },
  {
    title: "WikiLeaks email 51979",
    type: "Primary source",
    description: "Important for the Lockheed Skunk Works angle: Rob Weiss appears on the CC list under his corporate address.",
    href: "https://wikileaks.org/podesta-emails/emailid/51979"
  },
  {
    title: "ABC report on the disappearance timeline",
    type: "Reporting",
    description: "Adds the repairman, noon return, and missing-items detail to the public disappearance window.",
    href: "https://abcnews.com/US/fbi-assisting-search-retired-air-force-major-general/story?id=130995432"
  },
  {
    title: "Fox transcript on the third week of the search",
    type: "Reporting",
    description: "Adds Silver Alert context, Pagosa Springs, and the sheriff's remarks on the search.",
    href: "https://www.foxnews.com/us/search-missing-retired-air-force-general-enters-third-week-investigators-probe-new-clues.amp"
  },
  {
    title: "Sentinel: The Dead Drop",
    type: "Investigation",
    description: "A major independent investigation into the account, the post count, and the 38-vs-34-year discrepancy.",
    href: "https://thesentinel.network/p/the-dead-drop-an-anonymous-x-account"
  },
  {
    title: "Sentinel: The Ghost General",
    type: "Investigation",
    description: "The follow-up investigation connecting Tegnelia, Wilkerson, Rob Weiss, and the search architecture anomalies.",
    href: "https://thesentinel.network/p/the-ghost-general-every-news-outlet"
  },
  {
    title: "TwStalker profile capture",
    type: "Context capture",
    description: "Useful for the final reply orbit and the Paul B. thread context, but still a third-party mirror rather than a primary source.",
    href: "https://twstalker.com/TMBSPACESHIPS"
  },
  {
    title: "NRL Plasma Formulary",
    type: "Technical reference",
    description: "Used in the archive to anchor the 1.094 MHz discussion to hydrogen ion gyrofrequency rather than treating it as a free-floating number.",
    href: "https://www.nrl.navy.mil/Portals/38/PDF%20Files/NRL_Plasma_Formulary_2019.pdf"
  },
  {
    title: "CTBTO International Data Centre overview",
    type: "Technical reference",
    description: "The monitoring framework most relevant to the xenon-signature discussion, though not enough on its own to verify the claim.",
    href: "https://www.ctbto.org/our-work/international-data-centre"
  }
];

function createFilterChips(container, options, activeId, onChange) {
  container.innerHTML = "";

  options.forEach((option) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `chip${option.id === activeId ? " is-active" : ""}`;
    button.textContent = option.label;
    button.dataset.filter = option.id;
    button.addEventListener("click", () => onChange(option.id));
    container.appendChild(button);
  });
}

function renderTimeline(activeFilter = "all") {
  const timelineList = document.getElementById("timeline-list");
  const items = activeFilter === "all"
    ? timelineData
    : timelineData.filter((item) => item.category === activeFilter);

  timelineList.innerHTML = "";

  items.forEach((item) => {
    const article = document.createElement("article");
    article.className = "timeline-item";
    article.innerHTML = `
      <div class="timeline-meta">
        <span class="timeline-date">${item.date}</span>
        <span class="timeline-tag">${item.title}</span>
      </div>
      <p>${item.detail}</p>
    `;
    timelineList.appendChild(article);
  });
}

function badgeClass(assessment) {
  switch (assessment) {
    case "supported":
      return "claim-badge-supported";
    case "circumstantial":
      return "claim-badge-circumstantial";
    case "contested":
      return "claim-badge-contested";
    case "caution":
      return "claim-badge-caution";
    case "unproven":
    default:
      return "claim-badge-unproven";
  }
}

function renderClaims(activeFilter = "all") {
  const body = document.getElementById("claim-table-body");
  const rows = activeFilter === "all"
    ? claims
    : claims.filter((item) => item.assessment === activeFilter);

  body.innerHTML = "";

  rows.forEach((item) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="claim-name">${item.claim}</td>
      <td><span class="claim-badge ${badgeClass(item.assessment)}">${item.label}</span></td>
      <td>${item.reason}</td>
    `;
    body.appendChild(tr);
  });
}

function renderGallery() {
  const strip = document.getElementById("gallery-strip");
  const featureImage = document.getElementById("gallery-feature-image");
  const featureTitle = document.getElementById("gallery-feature-title");
  const featureCaption = document.getElementById("gallery-feature-caption");

  function selectItem(index) {
    const item = galleryItems[index];
    featureImage.src = item.src;
    featureImage.alt = item.alt;
    featureTitle.textContent = item.title;
    featureCaption.textContent = item.caption;

    Array.from(strip.children).forEach((button, buttonIndex) => {
      button.setAttribute("aria-selected", String(buttonIndex === index));
    });
  }

  galleryItems.forEach((item, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "gallery-thumb";
    button.setAttribute("role", "tab");
    button.setAttribute("aria-selected", String(index === 0));
    button.innerHTML = `
      <img src="${item.src}" alt="">
      <div>
        <strong>${item.title}</strong>
        <span>${item.caption}</span>
      </div>
    `;
    button.addEventListener("click", () => selectItem(index));
    strip.appendChild(button);
  });
}

function renderSources(searchTerm = "") {
  const list = document.getElementById("source-list");
  const normalized = searchTerm.trim().toLowerCase();
  const rows = normalized
    ? sources.filter((source) => `${source.title} ${source.type} ${source.description}`.toLowerCase().includes(normalized))
    : sources;

  list.innerHTML = "";

  rows.forEach((source) => {
    const card = document.createElement("article");
    card.className = "source-card";
    card.innerHTML = `
      <h3>${source.title}</h3>
      <p>${source.description}</p>
      <div class="source-meta">
        <span class="source-tag">${source.type}</span>
        <a href="${source.href}" target="_blank" rel="noreferrer">Open source</a>
      </div>
    `;
    list.appendChild(card);
  });

  if (!rows.length) {
    const empty = document.createElement("article");
    empty.className = "source-card";
    empty.innerHTML = `
      <h3>No matching sources</h3>
      <p>Try a broader search term like <em>WikiLeaks</em>, <em>Forbes</em>, <em>timeline</em>, or <em>CTBTO</em>.</p>
    `;
    list.appendChild(empty);
  }
}

function setupMenu() {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.getElementById("site-nav");

  toggle.addEventListener("click", () => {
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!expanded));
    nav.classList.toggle("is-open", !expanded);
  });

  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
}

function initFilterGroup(containerId, options, initialValue, renderFn) {
  let activeFilter = initialValue;
  const container = document.getElementById(containerId);

  const update = (nextFilter) => {
    activeFilter = nextFilter;
    createFilterChips(container, options, activeFilter, update);
    renderFn(activeFilter);
  };

  update(activeFilter);
}

function init() {
  initFilterGroup("timeline-filters", timelineFilters, "all", renderTimeline);
  initFilterGroup("claim-filters", claimFilters, "all", renderClaims);
  renderGallery();
  renderSources();
  setupMenu();

  document.getElementById("source-search").addEventListener("input", (event) => {
    renderSources(event.target.value);
  });
}

init();

