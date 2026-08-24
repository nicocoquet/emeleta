(() => {
  const normalize = (value) =>
    (value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase("fr")
      .trim();

  const initializeCatalogue = () => {
    const form = document.querySelector("[data-catalog-filters]");
    const grid = document.querySelector("[data-catalog-grid]");
    if (!form || !grid || form.dataset.ready === "true") return;
    form.dataset.ready = "true";

    const query = form.elements.q;
    const location = form.elements.location;
    const category = form.elements.category;
    const count = form.querySelector("[data-result-count]");
    const empty = document.querySelector("[data-catalog-empty]");
    const cards = [...grid.querySelectorAll(".catalog-card")];
    const parameters = new URLSearchParams(window.location.search);

    query.value = parameters.get("q") || "";
    location.value = parameters.get("location") || "";
    category.value = parameters.get("category") || "";

    const update = () => {
      const searchValue = normalize(query.value);
      let visible = 0;

      cards.forEach((card) => {
        const matchesQuery = !searchValue || normalize(card.textContent).includes(searchValue);
        const matchesLocation = !location.value || card.dataset.location === location.value;
        const matchesCategory = !category.value || card.dataset.category === category.value;
        const matches = matchesQuery && matchesLocation && matchesCategory;
        card.hidden = !matches;
        if (matches) visible += 1;
      });

      count.textContent = visible;
      empty.hidden = visible !== 0;
      form.classList.toggle("has-active-filters", Boolean(query.value || location.value || category.value));

      const nextParameters = new URLSearchParams();
      if (query.value) nextParameters.set("q", query.value);
      if (location.value) nextParameters.set("location", location.value);
      if (category.value) nextParameters.set("category", category.value);
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