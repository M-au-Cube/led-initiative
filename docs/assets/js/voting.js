(function () {
  "use strict";

  const config = window.LED_VOTING_CONFIG || { mode: "local" };
  const locale = document.documentElement.lang?.startsWith("en") ? "en" : "fr";
  const dataUrl = "/assets/data/measures.json";

  const labels = {
    fr: {
      like: "Pour",
      dislike: "Contre",
      likes: "pour",
      dislikes: "contre",
      pdf: "PDF détaillé",
      loading: "Chargement du programme…",
      error: "Impossible de charger les mesures.",
      voteSaved: "Votre avis a été enregistré.",
      voteChanged: "Votre avis a été mis à jour.",
    },
    en: {
      like: "For",
      dislike: "Against",
      likes: "for",
      dislikes: "against",
      pdf: "Detailed PDF",
      loading: "Loading program…",
      error: "Unable to load measures.",
      voteSaved: "Your opinion has been recorded.",
      voteChanged: "Your opinion has been updated.",
    },
  };

  const t = labels[locale];

  function storageKey(measureId) {
    return `led-vote-${measureId}`;
  }

  function getLocalVote(measureId) {
    return localStorage.getItem(storageKey(measureId));
  }

  function setLocalVote(measureId, voteType) {
    localStorage.setItem(storageKey(measureId), voteType);
  }

  function getLocalCounts(measureId) {
    const key = `led-vote-counts-${measureId}`;
    try {
      return JSON.parse(localStorage.getItem(key) || '{"like":0,"dislike":0}');
    } catch {
      return { like: 0, dislike: 0 };
    }
  }

  function updateLocalCounts(measureId, previous, next) {
    const counts = getLocalCounts(measureId);
    if (previous === "like") counts.like = Math.max(0, counts.like - 1);
    if (previous === "dislike") counts.dislike = Math.max(0, counts.dislike - 1);
    if (next === "like") counts.like += 1;
    if (next === "dislike") counts.dislike += 1;
    localStorage.setItem(`led-vote-counts-${measureId}`, JSON.stringify(counts));
    return counts;
  }

  async function fetchMeasures() {
    const response = await fetch(dataUrl);
    if (!response.ok) throw new Error(t.error);
    return response.json();
  }

  function titleFor(measure) {
    return locale === "en" ? measure.title_en : measure.title_fr;
  }

  function summaryFor(measure) {
    return locale === "en" ? measure.summary_en : measure.summary_fr;
  }

  function sectionTitle(section) {
    return locale === "en" ? section.title_en : section.title_fr;
  }

  function pdfFor(measure) {
    return locale === "en" ? measure.pdf_en : measure.pdf_fr;
  }

  function renderMeasure(measure, options) {
    const { showVote = false, showSummary = true } = options || {};
    const article = document.createElement("article");
    article.className = "led-measure";
    article.dataset.measureId = measure.id;

    const heading = document.createElement("h3");
    heading.textContent = titleFor(measure);
    article.appendChild(heading);

    if (showSummary) {
      const summary = document.createElement("p");
      summary.textContent = summaryFor(measure);
      article.appendChild(summary);
    }

    const actions = document.createElement("div");
    actions.className = "led-measure-actions";

    const pdfLink = document.createElement("a");
    pdfLink.href = `/${pdfFor(measure)}`;
    pdfLink.target = "_blank";
    pdfLink.rel = "noopener";
    pdfLink.textContent = `📄 ${t.pdf}`;
    actions.appendChild(pdfLink);

    article.appendChild(actions);

    if (showVote) {
      const votePanel = document.createElement("div");
      votePanel.className = "led-vote-panel";

      const controls = document.createElement("div");
      controls.className = "led-vote-controls";

      const likeBtn = document.createElement("button");
      likeBtn.type = "button";
      likeBtn.className = "led-vote-btn led-vote-like";
      likeBtn.innerHTML = `👍 ${t.like}`;

      const dislikeBtn = document.createElement("button");
      dislikeBtn.type = "button";
      dislikeBtn.className = "led-vote-btn led-vote-dislike";
      dislikeBtn.innerHTML = `👎 ${t.dislike}`;

      controls.appendChild(likeBtn);
      controls.appendChild(dislikeBtn);
      votePanel.appendChild(controls);

      const counts = document.createElement("div");
      counts.className = "led-vote-counts";
      votePanel.appendChild(counts);

      article.appendChild(votePanel);

      const current = getLocalVote(measure.id);
      const localCounts = getLocalCounts(measure.id);

      function refreshUI() {
        likeBtn.classList.toggle("active-like", current === "like");
        dislikeBtn.classList.toggle("active-dislike", current === "dislike");
        counts.textContent = `${localCounts.like} ${t.likes} · ${localCounts.dislike} ${t.dislikes}`;
      }

      function castVote(voteType) {
        const previous = getLocalVote(measure.id);
        if (previous === voteType) return;

        const updated = updateLocalCounts(measure.id, previous, voteType);
        setLocalVote(measure.id, voteType);
        localCounts.like = updated.like;
        localCounts.dislike = updated.dislike;
        refreshUI();
      }

      likeBtn.addEventListener("click", () => castVote("like"));
      dislikeBtn.addEventListener("click", () => castVote("dislike"));
      refreshUI();
    }

    return article;
  }

  function renderSections(container, data, options) {
    container.innerHTML = "";
    data.sections.forEach((section) => {
      const sectionTitleEl = document.createElement("h2");
      sectionTitleEl.className = "led-section";
      sectionTitleEl.textContent = sectionTitle(section);
      container.appendChild(sectionTitleEl);

      section.measures.forEach((measure) => {
        container.appendChild(renderMeasure(measure, options));
      });
    });
  }

  async function initProgramList() {
    const container = document.getElementById("led-program-list");
    if (!container) return;

    container.innerHTML = `<p class="led-loading">${t.loading}</p>`;
    try {
      const data = await fetchMeasures();
      renderSections(container, data, { showVote: false, showSummary: true });
    } catch {
      container.innerHTML = `<p>${t.error}</p>`;
    }
  }

  async function initVotePage() {
    const container = document.getElementById("led-vote-list");
    if (!container) return;

    container.innerHTML = `<p class="led-loading">${t.loading}</p>`;
    try {
      const data = await fetchMeasures();
      renderSections(container, data, { showVote: true, showSummary: true });
    } catch {
      container.innerHTML = `<p>${t.error}</p>`;
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    initProgramList();
    initVotePage();
  });
})();
