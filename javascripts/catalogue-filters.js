(() => {
  const normalize = (value) =>
    (value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase("fr")
      .trim();

  const splitFacetValues = (value) =>
    (value || "").split("||").map((item) => item.trim()).filter(Boolean);

  const initializeCatalogue = () => {
    const form = document.querySelector("[data-catalog-filters]");
    const grid = document.querySelector("[data-catalog-grid]");
    if (!form || !grid || form.dataset.ready === "true") return;
    form.dataset.ready = "true";

    const query = form.elements.q;
    const count = form.querySelector("[data-result-count]");
    const empty = document.querySelector("[data-catalog-empty]");
    const cards = [...grid.querySelectorAll(".catalog-card")];
    const parameters = new URLSearchParams(window.location.search);

    const filters = [...form.querySelectorAll("select[name]")]
      .filter((field) => field.name !== "q")
      .map((field) => ({ field, name: field.dataset.filter || field.name }));

    if (query) query.value = parameters.get("q") || "";
    filters.forEach(({ field, name }) => {
      field.value = parameters.get(name) || "";
    });

    const update = () => {
      const searchValue = query ? normalize(query.value) : "";
      let visible = 0;

      cards.forEach((card) => {
        const searchableText = `${card.textContent || ""} ${card.dataset.search || ""}`;
        const matchesQuery = !searchValue || normalize(searchableText).includes(searchValue);
        const matchesFacets = filters.every(({ field, name }) => {
          if (!field.value) return true;
          const attributeName = `data-${name.replaceAll("_", "-")}`;
          const values = splitFacetValues(card.getAttribute(attributeName));
          return values.includes(field.value);
        });
        const matches = matchesQuery && matchesFacets;
        card.hidden = !matches;
        if (matches) visible += 1;
      });

      if (count) count.textContent = visible;
      if (empty) empty.hidden = visible !== 0;
      const active = Boolean((query && query.value) || filters.some(({ field }) => field.value));
      form.classList.toggle("has-active-filters", active);

      const nextParameters = new URLSearchParams();
      if (query && query.value) nextParameters.set("q", query.value);
      filters.forEach(({ field, name }) => {
        if (field.value) nextParameters.set(name, field.value);
      });
      const nextUrl = `${window.location.pathname}${nextParameters.size ? `?${nextParameters}` : ""}${window.location.hash}`;
      window.history.replaceState({}, "", nextUrl);
    };

    form.addEventListener("input", update);
    form.addEventListener("change", update);
    form.addEventListener("reset", () => window.setTimeout(update));
    update();
  };

  document.addEventListener("DOMContentLoaded", initializeCatalogue);
  if (typeof document$ !== "undefined") document$.subscribe(initializeCatalogue);
})();
