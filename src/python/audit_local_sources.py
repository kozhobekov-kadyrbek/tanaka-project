"""Create private source hashes and safe chart metadata for an authorized source holder.

The output is intentionally outside the repository unless the caller explicitly
chooses otherwise. It never copies source files or exports slide/workbook images.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile

CHART_NS = {
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def source_role(relative: Path) -> str:
    value = relative.as_posix()
    if value == "本論/本論.docx":
        return "canonical_academic_thesis_narrative"
    if value == "本論/4章/結果表.xlsx":
        return "canonical_final_chapter4_results"
    if value == "本論データ/本論データ.xlsx":
        return "alternate_main_data_workbook"
    if value == "卒論発表/発表資料Vo.7.pptx":
        return "final_presentation"
    if value == "電気学会/電気学会グラフ.xlsx":
        return "conference_graph_workbook"
    if value.startswith("New folder/"):
        return "local_derived_analysis_or_inventory"
    if value.startswith(("本論/", "卒論発表/", "電気学会/", "ゼミ発表資料/")):
        return "primary_draft_result_or_presentation"
    return "background_reference_or_unrelated_material"


def write_private_inventory(source_root: Path, output: Path, excluded: tuple[Path, ...] = ()) -> int:
    excluded_paths = {output.resolve(), *(path.resolve() for path in excluded)}
    files = sorted(p for p in source_root.rglob("*") if p.is_file() and p.resolve() not in excluded_paths)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        fields = ["relative_path", "extension", "bytes", "modified_utc", "sha256", "role", "public_handling"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for path in files:
            relative = path.relative_to(source_root)
            writer.writerow({
                "relative_path": relative.as_posix(),
                "extension": path.suffix.lower(),
                "bytes": path.stat().st_size,
                "modified_utc": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
                "sha256": sha256_file(path),
                "role": source_role(relative),
                "public_handling": "metadata_only; do_not_commit_source_file",
            })
    return len(files)


def _chart_text(root: ET.Element, path: str) -> str:
    element = root.find(path, CHART_NS)
    return element.text if element is not None and element.text else ""


def chart_metadata(source: Path, source_id: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with ZipFile(source) as archive:
        names = sorted(
            (name for name in archive.namelist() if re.search(r"(^|/)charts/chart\d+\.xml$", name)),
            key=lambda value: int(re.search(r"chart(\d+)", value).group(1)),  # type: ignore[union-attr]
        )
        for name in names:
            root = ET.fromstring(archive.read(name))
            title = "".join(item.text or "" for item in root.findall(".//c:title//a:t", CHART_NS))
            series = root.findall(".//c:ser", CHART_NS)
            references = []
            for item in series:
                title_ref = _chart_text(item, ".//c:tx//c:f") or _chart_text(item, ".//c:tx//c:v")
                category_ref = _chart_text(item, ".//c:cat//c:f")
                value_ref = _chart_text(item, ".//c:val//c:f") or _chart_text(item, ".//c:yVal//c:f")
                references.append(" | ".join((title_ref, category_ref, value_ref)))
            rows.append({
                "source_id": source_id,
                "chart_id": Path(name).stem,
                "chart_title": title or "title_not_stored_in_chart_xml",
                "series_count": len(series),
                "source_references": "; ".join(references),
                "evidence_status": "source_chart_metadata_observed",
            })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--private-inventory", type=Path, required=True)
    parser.add_argument("--chart-audit", type=Path)
    args = parser.parse_args()
    excluded = (args.chart_audit,) if args.chart_audit else ()
    count = write_private_inventory(args.source_root, args.private_inventory, excluded)
    print(f"Wrote private inventory for {count} source files: {args.private_inventory}")
    if args.chart_audit:
        rows = []
        rows.extend(chart_metadata(args.source_root / "卒論発表" / "発表資料Vo.7.pptx", "final_presentation"))
        rows.extend(chart_metadata(args.source_root / "電気学会" / "電気学会グラフ.xlsx", "conference_graph_workbook"))
        args.chart_audit.parent.mkdir(parents=True, exist_ok=True)
        with args.chart_audit.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader(); writer.writerows(rows)
        print(f"Wrote metadata for {len(rows)} source charts: {args.chart_audit}")


if __name__ == "__main__":
    main()
