#!/usr/bin/env python3
"""Génère les pages MkDocs depuis inventaire_mobilier.xlsx."""

from __future__ import annotations

import html
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "inventaire_mobilier.xlsx"
SOURCE_PHOTOS = ROOT / "photos"
DOCS = ROOT / "docs"
CATALOG = DOCS / "catalogue"
SITE_IMAGES = DOCS / "assets" / "images"
STATISTICS = DOCS / "statistiques.fr.md"


def text(value) -> str:
    return "" if value is None else str(value).strip()


def slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    return value.strip("-")


def money(value) -> str:
    if value in (None, ""):
        return ""
    try:
        return f"{float(value):,.0f} €".replace(",", " ")
    except (TypeError, ValueError):
        return text(value)


def number(value) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def quantity(obj: dict) -> int:
    value = number(obj.get("Quantité"))
    return max(1, int(value)) if value is not None else 1


def unit_value(obj: dict, side: str) -> float | None:
    return number(obj.get(f"Estimation unitaire {side} (€)")) or number(obj.get(f"Estimation {side} (€)"))


def lot_value(obj: dict, side: str) -> float | None:
    """Retourne le total du lot, même si le moteur XLSX n'a pas mis en cache la formule."""
    total = number(obj.get(f"Estimation du lot {side} (€)"))
    if total is not None:
        return total
    unit = unit_value(obj, side)
    return unit * quantity(obj) if unit is not None else None


def estimate_range(low, high) -> str:
    return " – ".join(v for v in [money(low), money(high)] if v) or "Non renseignée"


def treemap(data: Counter, empty_label: str = "Aucune donnée") -> str:
    if not data:
        return f'<p class="empty-state">{html.escape(empty_label)}</p>'
    total = sum(data.values())
    tiles = []
    for index, (label, count) in enumerate(sorted(data.items(), key=lambda item: (-item[1], item[0]))):
        share = 100 * count / total
        tiles.append(
            f'<div class="stat-treemap-tile stat-color-{index % 10}" '
            f'style="--weight:{count};--share:{share:.2f}%" '
            f'title="{html.escape(label, quote=True)} : {count} lot(s), {share:.1f} %">'
            f'<span>{html.escape(label)}</span><small>{share:.0f} %</small>'
            '</div>'
        )
    return '<div class="stat-treemap">' + "\n".join(tiles) + '</div>'


def top_with_other(data: Counter, limit: int = 12) -> Counter:
    ordered = data.most_common()
    if len(ordered) <= limit:
        return data
    result = Counter(dict(ordered[:limit]))
    result["Autres catégories"] = sum(count for _, count in ordered[limit:])
    return result


def location_category_histogram(furniture: list[dict], category_limit: int = 9) -> str:
    """Histogramme horizontal empilé : une barre par pièce, segmentée par catégorie."""
    category_totals = Counter(text(obj.get("Catégorie")) or "Non classé" for obj in furniture)
    main_categories = [label for label, _ in category_totals.most_common(category_limit)]
    legend_labels = main_categories + (["Autres catégories"] if len(category_totals) > category_limit else [])
    color_by_label = {label: index % 10 for index, label in enumerate(legend_labels)}

    matrix: dict[str, Counter] = defaultdict(Counter)
    for obj in furniture:
        location = text(obj.get("Localisation")) or "Localisation à préciser"
        category = text(obj.get("Catégorie")) or "Non classé"
        bucket = category if category in main_categories else "Autres catégories"
        matrix[location][bucket] += 1

    rows = []
    for location, counts in sorted(matrix.items(), key=lambda item: (-sum(item[1].values()), item[0])):
        total = sum(counts.values())
        segments = []
        for label in legend_labels:
            count = counts.get(label, 0)
            if not count:
                continue
            share = 100 * count / total
            visible_label = html.escape(str(count)) if share >= 7 else ""
            segments.append(
                f'<span class="stat-stack-segment stat-color-{color_by_label[label]}" '
                f'style="width:{share:.3f}%" title="{html.escape(label, quote=True)} : {count}" '
                f'aria-label="{html.escape(label, quote=True)} : {count}">{visible_label}</span>'
            )
        rows.append(
            '<div class="stat-stack-row">'
            f'<div class="stat-stack-label"><span>{html.escape(location)}</span><strong>{total}</strong></div>'
            f'<div class="stat-stack">{"".join(segments)}</div></div>'
        )

    legend = "".join(
        f'<span><i class="stat-color-{color_by_label[label]}"></i>{html.escape(label)}</span>'
        for label in legend_labels
    )
    return f'<div class="stat-stack-chart">{"".join(rows)}</div><div class="stat-legend">{legend}</div>'


def generate_statistics(furniture: list[dict]) -> None:
    lows = [value for obj in furniture if (value := lot_value(obj, "basse")) is not None]
    highs = [value for obj in furniture if (value := lot_value(obj, "haute")) is not None]
    total_low = sum(lows)
    total_high = sum(highs)
    estimated_count = sum(
        1
        for obj in furniture
        if lot_value(obj, "basse") is not None
        or lot_value(obj, "haute") is not None
    )

    locations = Counter(text(obj.get("Localisation")) or "Localisation à préciser" for obj in furniture)
    categories = Counter(text(obj.get("Catégorie")) or "Non classé" for obj in furniture)
    location_chart = treemap(locations)
    category_chart = treemap(top_with_other(categories, limit=14))
    mixed_chart = location_category_histogram(furniture)
    coverage = (estimated_count / len(furniture) * 100) if furniture else 0
    item_count = sum(quantity(obj) for obj in furniture)

    page = f"""# Statistiques

## Mobilier & objets d’art

### Vue d’ensemble

<div class="stat-cards">
  <article class="stat-card stat-card-primary">
    <span>Estimation globale</span>
    <strong>{money(total_low)} – {money(total_high)}</strong>
    <small>Fourchette indicative cumulée</small>
  </article>
  <article class="stat-card">
    <span>Lots publiés</span>
    <strong>{len(furniture)}</strong>
    <small>{item_count} objet(s) inventorié(s)</small>
  </article>
  <article class="stat-card">
    <span>Objets estimés</span>
    <strong>{estimated_count}</strong>
    <small>{coverage:.0f} % du catalogue</small>
  </article>
  <article class="stat-card">
    <span>Catégories</span>
    <strong>{len(categories)}</strong>
    <small>Types renseignés</small>
  </article>
</div>

!!! note "Lecture des estimations"
    Les montants sont des estimations documentaires indicatives. Leur addition donne un ordre de grandeur patrimonial, non une valeur de vente garantie.

### Répartition par localisation

<div class="stat-chart" role="img" aria-label="Treemap des lots par localisation">
{location_chart}
</div>

### Répartition par catégorie

<div class="stat-chart" role="img" aria-label="Treemap des lots par catégorie">
{category_chart}
</div>

### Catégories par localisation

<div class="stat-chart" role="img" aria-label="Histogramme des catégories pour chaque localisation">
{mixed_chart}
</div>

"""
    STATISTICS.write_text(page.rstrip() + "\n", encoding="utf-8")


def rows_as_dicts(sheet, header_row: int = 3):
    headers = [text(cell.value) for cell in sheet[header_row]]
    for row in sheet.iter_rows(min_row=header_row + 1, values_only=True):
        values = {headers[i]: row[i] if i < len(row) else None for i in range(len(headers))}
        if any(value not in (None, "") for value in row):
            yield values


def require_columns(actual: set[str], expected: set[str], sheet_name: str):
    missing = expected - actual
    if missing:
        raise ValueError(f"Feuille {sheet_name}: colonnes manquantes: {', '.join(sorted(missing))}")


def main() -> int:
    if not WORKBOOK.exists():
        print(f"Classeur introuvable: {WORKBOOK}", file=sys.stderr)
        return 1

    wb = load_workbook(WORKBOOK, data_only=True)
    require_columns(
        {text(c.value) for c in wb["Mobilier"][3]},
        {"Identifiant", "Titre", "Catégorie", "Description", "Publié"},
        "Mobilier",
    )
    require_columns(
        {text(c.value) for c in wb["Photos"][3]},
        {"Identifiant objet", "Fichier", "Ordre", "Légende", "Image principale"},
        "Photos",
    )

    furniture = [r for r in rows_as_dicts(wb["Mobilier"]) if text(r["Publié"]).lower() in {"oui", "yes", "true", "1"}]
    photo_rows = list(rows_as_dicts(wb["Photos"]))
    photos_by_object = defaultdict(list)
    for photo in photo_rows:
        photos_by_object[text(photo["Identifiant objet"])].append(photo)
    for items in photos_by_object.values():
        items.sort(key=lambda p: (p["Ordre"] if isinstance(p["Ordre"], (int, float)) else 999, text(p["Fichier"])))

    CATALOG.mkdir(parents=True, exist_ok=True)
    SITE_IMAGES.mkdir(parents=True, exist_ok=True)
    # Migration ponctuelle depuis l'ancienne structure non localisée.
    for legacy in [DOCS / "index.md", CATALOG / "index.md", DOCS / "statistiques.md"]:
        if legacy.exists():
            legacy.unlink()
    for legacy in CATALOG.glob("MOB-*.md"):
        if not any(legacy.name.endswith(f".{locale}.md") for locale in ("fr", "en", "it")):
            legacy.unlink()
    # Ne régénérer que les fiches françaises : les futures traductions .en.md
    # et .it.md doivent rester intactes.
    for old in CATALOG.glob("MOB-*.fr.md"):
        old.unlink()

    cards = []
    categories = Counter()
    locations = Counter()
    warnings = []
    for obj in furniture:
        object_id = text(obj["Identifiant"])
        title = text(obj["Titre"])
        if not object_id or not title:
            warnings.append("Une ligne publiée sans identifiant ou sans titre a été ignorée.")
            continue

        photos = photos_by_object.get(object_id, [])
        available = []
        for photo in photos:
            raw_filename = text(photo["Fichier"]).strip()

            if not raw_filename:
                warnings.append(
                    f"{object_id}: nom de photographie vide ; ligne ignorée."
                )
                continue

            filename = Path(raw_filename).name
            source = SOURCE_PHOTOS / filename

            if source.is_file():
                shutil.copy2(source, SITE_IMAGES / filename)
                available.append(photo)
            elif source.is_dir():
                warnings.append(
                    f"{object_id}: le chemin photographique désigne un dossier : "
                    f"{raw_filename}"
                )
            else:
                warnings.append(
                    f"{object_id}: photographie introuvable : {filename}"
                )

        cover = next((p for p in available if text(p["Image principale"]).lower() in {"oui", "yes", "true", "1"}), available[0] if available else None)
        category = text(obj["Catégorie"]) or "Non classé"
        location = text(obj.get("Localisation")) or "Localisation à préciser"
        categories[category] += 1
        locations[location] += 1

        item_quantity = quantity(obj)
        quantity_label = f" · {item_quantity} items" if item_quantity > 1 else ""
        unit_estimate = estimate_range(unit_value(obj, "basse"), unit_value(obj, "haute"))
        lot_estimate = estimate_range(lot_value(obj, "basse"), lot_value(obj, "haute"))
        estimate = lot_estimate

        metadata = [
            ("Catégorie", category),
            ("Origine", text(obj.get("Origine"))),
            ("Matériaux", text(obj.get("Matériaux"))),
            ("Dimensions", text(obj.get("Dimensions"))),
            ("Localisation", text(obj.get("Localisation"))),
            ("Quantité", str(item_quantity)),
            ("Statut", text(obj.get("Statut"))),
        ]
        meta_html = "\n".join(
            f'<div class="record-field"><dt>{html.escape(label)}</dt><dd>{html.escape(value)}</dd></div>'
            for label, value in metadata if value
        )

        gallery = []
        for photo in available:
            filename = Path(text(photo["Fichier"])).name
            caption = text(photo["Légende"]) or title
            gallery.append(
                f'<figure><a href="../../assets/images/{html.escape(filename)}" target="_blank">'
                f'<img src="../../assets/images/{html.escape(filename)}" alt="{html.escape(caption)}" loading="lazy"></a>'
                f'<figcaption>{html.escape(caption)}</figcaption></figure>'
            )
        gallery_html = "\n".join(gallery) if gallery else '<p class="empty-state">Aucune photographie disponible.</p>'

        sources = []
        for key in ["Source 1", "Source 2"]:
            url = text(obj.get(key))
            if url:
                sources.append(f"- [{html.escape(url)}]({url})")
        source_block = "\n".join(sources) if sources else "_Aucune source renseignée._"

        association_ids = re.findall(r"MOB-\d{3}", text(obj.get("Associé à")), flags=re.IGNORECASE)
        association_block = " · ".join(
            f'<a href="../{associated.upper()}/">{html.escape(associated.upper())}</a>'
            for associated in association_ids
        ) or "_Aucun objet associé._"

        hero_visual = (
            f'<a href="../../assets/images/{html.escape(Path(text(cover["Fichier"])).name)}" target="_blank">'
            f'<img src="../../assets/images/{html.escape(Path(text(cover["Fichier"])).name)}" alt="{html.escape(title)}"></a>'
            if cover else '<div class="record-placeholder">Sans photographie</div>'
        )

        page = f"""<div class="lot-hero">
<div class="lot-visual">{hero_visual}</div>
<div class="lot-summary">
<p class="record-kicker">Lot {html.escape(object_id)} · {html.escape(category)}</p>
<h1>{html.escape(title)}</h1>
<p class="lot-dating">{html.escape(text(obj.get("Datation")) or "Datation à préciser")}</p>
<div class="lot-estimate"><span>Estimation du lot</span><strong>{html.escape(lot_estimate)}</strong></div>
<p class="lot-unit-estimate">Estimation unitaire : {html.escape(unit_estimate)}</p>

<dl class="record-grid">
{meta_html}
</dl>
</div>
</div>

## Description

{text(obj.get("Description")) or "_Description à compléter._"}

## État de conservation

{text(obj.get("État")) or "_État à compléter._"}

## Objets associés

{association_block}

## Photographies

<div class="gallery">
{gallery_html}
</div>

## Sources et comparaisons

{source_block}

<p class="notice">L’identification et l’estimation sont indicatives et peuvent évoluer avec de nouvelles mesures, photographies ou expertises.</p>
"""
        (CATALOG / f"{object_id}.fr.md").write_text(page, encoding="utf-8")

        cover_html = (
            f'<img src="assets/images/{html.escape(Path(text(cover["Fichier"])).name)}" alt="{html.escape(title)}">'
            if cover else '<div class="card-placeholder">Sans photographie</div>'
        )
        cards.append(
            f'<article class="catalog-card" data-location="{html.escape(location, quote=True)}" '
            f'data-category="{html.escape(category, quote=True)}"><a href="{object_id}/">'
            f'{cover_html.replace("assets/images/", "../assets/images/")}'
            f'<div class="catalog-card-body"><div class="card-lot"><span>Lot {html.escape(object_id)}</span>'
            f'<span>{html.escape(category)}</span></div><h2>{html.escape(title)}</h2>'
            f'<p class="card-date">{html.escape(text(obj.get("Datation")) or "Datation à préciser")}'
            f'{html.escape(quantity_label)}</p>'
            f'<p class="card-estimate"><span>Estimation</span><strong>{html.escape(estimate)}</strong></p></div></a></article>'
        )

    location_options = "\n".join(
        f'<option value="{html.escape(label, quote=True)}">{html.escape(label)} ({count})</option>'
        for label, count in sorted(locations.items())
    )
    category_options = "\n".join(
        f'<option value="{html.escape(label, quote=True)}">{html.escape(label)} ({count})</option>'
        for label, count in sorted(categories.items())
    )
    catalogue = f"""<div class="catalogue-heading">
  <p class="eyebrow">Collection complète</p>
  <h1>Catalogue</h1>
</div>

<form class="catalog-filters" data-catalog-filters>
  <div class="catalog-filter catalog-search">
    <label for="catalog-query">Rechercher</label>
    <input id="catalog-query" type="search" name="q" placeholder="Titre, lot, époque…" autocomplete="off">
  </div>
  <div class="catalog-filter">
    <label for="catalog-location">Localisation</label>
    <select id="catalog-location" name="location">
      <option value="">Toutes les pièces</option>
      {location_options}
    </select>
  </div>
  <div class="catalog-filter">
    <label for="catalog-category">Type d’objet</label>
    <select id="catalog-category" name="category">
      <option value="">Tous les types</option>
      {category_options}
    </select>
  </div>
  <button class="catalog-reset" type="reset">Réinitialiser</button>
  <p class="catalog-result" aria-live="polite"><strong data-result-count>{len(cards)}</strong> lots affichés</p>
</form>

<div class="catalog-grid" data-catalog-grid>
{''.join(cards) if cards else '<p class="empty-state">Aucun objet publié.</p>'}
</div>
<p class="empty-state catalog-empty" data-catalog-empty hidden>Aucun lot ne correspond à ces critères.</p>
"""
    (CATALOG / "index.fr.md").write_text(catalogue, encoding="utf-8")
    generate_statistics(furniture)

    if warnings:
        print("Avertissements:")
        for warning in warnings:
            print(f"- {warning}")
    print(f"Catalogue et statistiques générés: {len(cards)} objet(s), {sum(len(v) for v in photos_by_object.values())} photographie(s) référencée(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
