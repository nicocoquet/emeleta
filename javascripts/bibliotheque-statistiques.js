(() => {
  const STRINGS = {
    fr: {
      works: "ouvrages", volumes: "volumes", low: "estimation basse", high: "estimation haute",
      median: "valeur médiane", mapped: "lieux cartographiés", count: "Nombre d’ouvrages",
      value: "Valeur estimée", period: "Période", language: "Langue", subject: "Thème",
      document_type: "Type de document", heritage: "Intérêt patrimonial", all: "Tous",
      noMap: "Aucun lieu doté de coordonnées ne correspond aux filtres.", noData: "Aucune donnée disponible.",
      places: "lieux", estimate: "Estimation", years: "Période couverte", uncertain: "Localisation à confirmer",
      completeness: "Complétude", illustrated: "Illustration", marks: "Marques d’exemplaire"
    },
    en: {
      works: "works", volumes: "volumes", low: "low estimate", high: "high estimate",
      median: "median value", mapped: "mapped places", count: "Number of works",
      value: "Estimated value", period: "Period", language: "Language", subject: "Subject",
      document_type: "Document type", heritage: "Heritage interest", all: "All",
      noMap: "No geocoded place matches the filters.", noData: "No data available.",
      places: "places", estimate: "Estimate", years: "Covered period", uncertain: "Location to confirm",
      completeness: "Completeness", illustrated: "Illustration", marks: "Copy marks"
    },
    it: {
      works: "opere", volumes: "volumi", low: "stima minima", high: "stima massima",
      median: "valore mediano", mapped: "luoghi cartografati", count: "Numero di opere",
      value: "Valore stimato", period: "Periodo", language: "Lingua", subject: "Tema",
      document_type: "Tipo di documento", heritage: "Interesse patrimoniale", all: "Tutti",
      noMap: "Nessun luogo geocodificato corrisponde ai filtri.", noData: "Nessun dato disponibile.",
      places: "luoghi", estimate: "Stima", years: "Periodo coperto", uncertain: "Localizzazione da confermare",
      completeness: "Completezza", illustrated: "Illustrazione", marks: "Segni d’esemplare"
    }
  };

  const lang = (document.documentElement.lang || "fr").slice(0, 2);
  const t = STRINGS[lang] || STRINGS.fr;
  const money = new Intl.NumberFormat(lang, { style: "currency", currency: "EUR", maximumFractionDigits: 0 });
  const integer = new Intl.NumberFormat(lang, { maximumFractionDigits: 0 });
  const esc = value => String(value ?? "").replace(/[&<>'"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[c]));
  const averageEstimate = record => {
    const low = Number.isFinite(record.estimateLow) ? record.estimateLow : null;
    const high = Number.isFinite(record.estimateHigh) ? record.estimateHigh : null;
    if (low !== null && high !== null) return (low + high) / 2;
    return low ?? high ?? 0;
  };

  async function init(root) {
    if (root.dataset.ready) return;
    root.dataset.ready = "true";
    const url = new URL(root.dataset.dataUrl, window.location.href);
    let data;
    try { data = await fetch(url).then(response => { if (!response.ok) throw new Error(response.status); return response.json(); }); }
    catch (error) { root.querySelector("[data-stat-empty]").hidden = false; return; }
    const records = data.records || [];

    let metric = "count";
    const metricHost = root.querySelector("[data-map-metric]");
    metricHost.innerHTML = `<button type="button" class="is-active" data-metric="count">${esc(t.count)}</button><button type="button" data-metric="value">${esc(t.value)}</button>`;
    metricHost.addEventListener("click", event => {
      const button = event.target.closest("button[data-metric]");
      if (!button) return;
      metric = button.dataset.metric;
      metricHost.querySelectorAll("button").forEach(item => item.classList.toggle("is-active", item === button));
      render();
    });

    const mapNode = root.querySelector("[data-library-map]");
    const map = window.L ? L.map(mapNode, { scrollWheelZoom: false }).setView([46.8, 6.5], 4) : null;
    let layer = null;
    if (map) {
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      }).addTo(map);
      layer = L.layerGroup().addTo(map);
      setTimeout(() => map.invalidateSize(), 0);
    } else {
      mapNode.innerHTML = `<p>${esc(t.noMap)}</p>`;
    }

    function aggregatePlaces(filtered) {
      const places = new Map();
      filtered.forEach(record => {
        const name = record.city || record.cityHistorical || "—";
        const key = `${name}|${record.country || ""}`;
        if (!places.has(key)) places.set(key, { city: name, country: record.country || "", latitude: record.latitude, longitude: record.longitude, count: 0, value: 0, low: 0, high: 0, years: [], uncertain: false });
        const place = places.get(key);
        place.count += 1;
        place.value += averageEstimate(record);
        place.low += Number(record.estimateLow) || 0;
        place.high += Number(record.estimateHigh) || 0;
        if (record.year) place.years.push(record.year);
        place.uncertain ||= Boolean(record.locationUncertain);
        if (Number.isFinite(record.latitude)) place.latitude = record.latitude;
        if (Number.isFinite(record.longitude)) place.longitude = record.longitude;
      });
      return [...places.values()].sort((a, b) => b[metric] - a[metric] || a.city.localeCompare(b.city, lang));
    }

    function renderKpis(filtered, places) {
      const lows = filtered.map(r => r.estimateLow).filter(Number.isFinite);
      const highs = filtered.map(r => r.estimateHigh).filter(Number.isFinite);
      const mids = filtered.map(averageEstimate).filter(Boolean).sort((a, b) => a - b);
      const median = mids.length ? mids[Math.floor(mids.length / 2)] : 0;
      const cards = [
        [integer.format(filtered.length), t.works],
        [integer.format(filtered.reduce((sum, r) => sum + (Number(r.volumes) || 1), 0)), t.volumes],
        [money.format(lows.reduce((a, b) => a + b, 0)), t.low],
        [money.format(highs.reduce((a, b) => a + b, 0)), t.high],
        [money.format(median), t.median],
        [integer.format(places.filter(p => Number.isFinite(p.latitude) && Number.isFinite(p.longitude)).length), t.mapped],
      ];
      root.querySelector("[data-kpis]").innerHTML = cards.map(([value, label]) => `<article><strong>${esc(value)}</strong><span>${esc(label)}</span></article>`).join("");
    }

    function renderMap(places) {
      if (!map || !layer) return;
      layer.clearLayers();
      const mapped = places.filter(p => Number.isFinite(p.latitude) && Number.isFinite(p.longitude));
      const max = Math.max(1, ...mapped.map(p => p[metric]));
      const bounds = [];
      mapped.forEach(place => {
        const radius = 7 + 22 * Math.sqrt((place[metric] || 0) / max);
        const period = place.years.length ? `${Math.min(...place.years)}–${Math.max(...place.years)}` : "—";
        const circle = L.circleMarker([place.latitude, place.longitude], { radius, weight: 1.5, color: "#7c3028", fillColor: "#b85a49", fillOpacity: .72 });
        circle.bindPopup(`<strong>${esc(place.city)}</strong>${place.country ? `<br>${esc(place.country)}` : ""}<br>${integer.format(place.count)} ${esc(t.works)}<br>${esc(t.years)} : ${period}<br>${esc(t.estimate)} : ${money.format(place.low)}–${money.format(place.high)}${place.uncertain ? `<br><em>${esc(t.uncertain)}</em>` : ""}`);
        circle.addTo(layer);
        bounds.push([place.latitude, place.longitude]);
      });
      const empty = root.querySelector("[data-map-empty]");
      empty.hidden = mapped.length > 0;
      empty.textContent = t.noMap;
      if (mapped.length === 1) map.setView(bounds[0], 6);
      else if (mapped.length > 1) map.fitBounds(bounds, { padding: [30, 30], maxZoom: 7 });
    }

    function renderRanking(places) {
      const host = root.querySelector('[data-ranking="cities"]');
      const max = Math.max(1, ...places.map(p => p[metric]));
      host.innerHTML = places.length ? places.slice(0, 12).map((place, index) => {
        const value = metric === "count" ? `${integer.format(place.count)} ${t.works}` : money.format(place.value);
        return `<article><span class="rank">${index + 1}</span><div><strong>${esc(place.city)}</strong><small>${esc(place.country || "")}</small><span class="rank-bar"><i style="width:${Math.max(4, place[metric] / max * 100)}%"></i></span></div><b>${esc(value)}</b></article>`;
      }).join("") : `<p>${esc(t.noData)}</p>`;
    }

    function distribution(filtered, key) {
      const counter = new Map();
      filtered.forEach(record => {
        const list = Array.isArray(record[key]) ? record[key] : record[key] ? [record[key]] : ["À préciser"];
        list.forEach(value => counter.set(value, (counter.get(value) || 0) + 1));
      });
      return [...counter].sort((a, b) => b[1] - a[1]).slice(0, 10);
    }

    function renderDistribution(selector, filtered, key) {
      const host = root.querySelector(selector);
      const entries = distribution(filtered, key);
      const max = Math.max(1, ...entries.map(item => item[1]));
      host.innerHTML = entries.length
        ? entries.map(([name, count]) => `<li><span>${esc(name)}</span><i><b style="width:${count / max * 100}%"></b></i><strong>${integer.format(count)}</strong></li>`).join("")
        : `<li>${esc(t.noData)}</li>`;
    }

    function renderPublishers(filtered) {
      const host = root.querySelector('[data-ranking="publishers"]');
      const entries = distribution(filtered, "publishers");
      const max = Math.max(1, ...entries.map(item => item[1]));
      host.innerHTML = entries.length ? entries.map(([name, count], index) =>
        `<article><span class="rank">${index + 1}</span><div><strong>${esc(name)}</strong><span class="rank-bar"><i style="width:${count / max * 100}%"></i></span></div><b>${integer.format(count)}</b></article>`
      ).join("") : `<p>${esc(t.noData)}</p>`;
    }

    function render() {
      const places = aggregatePlaces(records);
      renderKpis(records, places);
      renderMap(places);
      renderRanking(places);
      renderDistribution('[data-chart="periods"]', records, "period");
      renderDistribution('[data-chart="languages"]', records, "languages");
      renderDistribution('[data-chart="categories"]', records, "subjects");
      renderPublishers(records);
    }
    render();
  }

  function boot() { document.querySelectorAll("[data-library-statistics]").forEach(init); }
  document.addEventListener("DOMContentLoaded", boot);
  if (window.document$) window.document$.subscribe(boot);
})();
