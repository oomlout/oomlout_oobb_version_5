from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

# oobb_arch lives in old/ after the restructure; add it to the path so the
# import below works regardless of the working directory.
sys.path.insert(0, str(Path(__file__).parent.parent / "old"))

from oobb_arch.catalog.object_discovery import discover_objects
from oobb_arch.catalog.part_set_discovery import discover_part_sets


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _normalize_variables(raw_variables: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_variables, list):
        return []

    normalized: list[dict[str, Any]] = []
    for item in raw_variables:
        if isinstance(item, dict):
            name = _coerce_text(item.get("name"))
            if not name:
                continue
            normalized.append(
                {
                    "name": name,
                    "description": _coerce_text(item.get("description", "")),
                    "type": _coerce_text(item.get("type", "")),
                    "default": item.get("default", ""),
                }
            )
        elif isinstance(item, str):
            name = item.strip()
            if not name:
                continue
            normalized.append({"name": name, "description": "", "type": "", "default": ""})
    return normalized


def _extract_variable_names(raw_variables: Any) -> list[str]:
    return [item["name"] for item in _normalize_variables(raw_variables)]


def _build_summary(description: str, variable_names: list[str], returns_text: str) -> str:
    if description:
        first_sentence = description.split(".")[0].strip()
        if first_sentence:
            return first_sentence + ("." if not first_sentence.endswith(".") else "")
    if variable_names:
        return f"Inputs: {', '.join(variable_names)}"
    if returns_text:
        return f"Returns: {returns_text}"
    return "No summary available."


def _normalize_doc_entry(command: str, metadata: dict[str, Any]) -> dict[str, Any]:
    name_long = _coerce_text(metadata.get("name_long") or metadata.get("name") or command)
    description = _coerce_text(metadata.get("description"))
    category = _coerce_text(metadata.get("category") or "General")
    returns_text = _coerce_text(metadata.get("returns"))
    name_short = metadata.get("name_short")

    if isinstance(name_short, str):
        aliases = [name_short.strip()] if name_short.strip() else []
    elif isinstance(name_short, list):
        aliases = [item.strip() for item in name_short if isinstance(item, str) and item.strip()]
    else:
        aliases = []

    variables = _normalize_variables(metadata.get("variables", []))
    variable_names = [item["name"] for item in variables]
    summary = _build_summary(description, variable_names, returns_text)

    return {
        "command": command,
        "name_long": name_long,
        "name_short_options": aliases,
        "description": description,
        "summary": summary,
        "variables": variables,
        "variable_names": variable_names,
        "category": category,
        "returns": returns_text,
        "aliases": aliases,
    }


def get_all_objects_documentation(objects_root: str | Path | None = None) -> list[dict[str, Any]]:
    discovered = discover_objects(objects_root=objects_root)
    docs: list[dict[str, Any]] = []
    for object_name in sorted(discovered.keys()):
        discovered_object = discovered[object_name]
        docs.append(_normalize_doc_entry(object_name, discovered_object.metadata))
    return docs


def get_all_part_sets_documentation(sets_root: str | Path | None = None) -> list[dict[str, Any]]:
    discovered = discover_part_sets(sets_root=sets_root)
    docs: list[dict[str, Any]] = []
    for set_name in sorted(discovered.keys()):
        discovered_set = discovered[set_name]
        docs.append(_normalize_doc_entry(set_name, discovered_set.metadata))
    return docs


def export_documentation_json(
    output_file: str | Path,
    objects_root: str | Path | None = None,
    sets_root: str | Path | None = None,
):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = _build_documentation_payload(objects_root=objects_root, sets_root=sets_root)

    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _build_documentation_payload(
    objects_root: str | Path | None = None,
    sets_root: str | Path | None = None,
) -> dict[str, Any]:
    objects = get_all_objects_documentation(objects_root=objects_root)
    part_sets = get_all_part_sets_documentation(sets_root=sets_root)
    return {
        "objects": objects,
        "part_sets": part_sets,
        "generated_date": str(date.today()),
        "total_objects": len(objects),
        "total_part_sets": len(part_sets),
    }


def export_documentation_html(
    template_file: str | Path,
    output_file: str | Path,
    objects_root: str | Path | None = None,
    sets_root: str | Path | None = None,
):
    template_path = Path(template_file)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = _build_documentation_payload(objects_root=objects_root, sets_root=sets_root)
    template_content = template_path.read_text(encoding="utf-8")

    placeholder = "<!-- DOCUMENTATION_DATA_PLACEHOLDER -->"
    if placeholder in template_content:
        # The placeholder is inside an existing <script> block — inject raw JS only
        data_block = f"window.DOCUMENTATION_DATA = {json.dumps(payload)};"
        html = template_content.replace(placeholder, data_block)
    else:
        # No placeholder — append a full <script> block at the end
        data_block = f"<script>window.DOCUMENTATION_DATA = {json.dumps(payload)};</script>"
        html = template_content + "\n" + data_block

    output_path.write_text(html, encoding="utf-8")


def _render_variables_table(variables: list[dict[str, Any]]) -> list[str]:
    lines = ["| Name | Description | Type | Default |", "|------|-------------|------|---------|"]
    if not variables:
        lines.append("| - | - | - | - |")
        return lines

    for variable in variables:
        name = _coerce_text(variable.get("name"))
        description = _coerce_text(variable.get("description"))
        var_type = _coerce_text(variable.get("type"))
        default = variable.get("default", "")
        default_text = _coerce_text(default)
        lines.append(f"| {name} | {description} | {var_type} | {default_text} |")
    return lines


def _write_entity_readme(folder: Path, entry: dict[str, Any]):
    lines = [
        f"# {entry['command']}",
        "",
        f"**{entry['name_long']}**",
        "",
        entry.get("description", ""),
        "",
        "## Variables",
        "",
    ]
    lines.extend(_render_variables_table(entry.get("variables", [])))
    lines.extend(
        [
            "",
            "## Category",
            "",
            entry.get("category", "General"),
            "",
        ]
    )
    (folder / "README.md").write_text("\n".join(lines), encoding="utf-8")


def _write_index_readme(root: Path, title: str, entries: list[dict[str, Any]]):
    lines = [
        f"# {title}",
        "",
        "| Name | Description | Category |",
        "|------|-------------|----------|",
    ]
    for entry in entries:
        lines.append(
            f"| [{entry['command']}]({entry['command']}/) | {entry.get('description', '')} | {entry.get('category', 'General')} |"
        )
    lines.append("")
    (root / "README.md").write_text("\n".join(lines), encoding="utf-8")


def export_documentation_markdown(
    objects_root: str | Path | None = None,
    sets_root: str | Path | None = None,
):
    objects_map = discover_objects(objects_root=objects_root)
    sets_map = discover_part_sets(sets_root=sets_root)

    if not objects_map and not sets_map:
        return

    objects_base = Path(objects_root).resolve() if objects_root is not None else None
    sets_base = Path(sets_root).resolve() if sets_root is not None else None

    object_entries: list[dict[str, Any]] = []
    for name in sorted(objects_map.keys()):
        item = objects_map[name]
        entry = _normalize_doc_entry(name, item.metadata)
        object_entries.append(entry)
        _write_entity_readme(item.path.parent, entry)
        if objects_base is None:
            objects_base = item.path.parent.parent

    set_entries: list[dict[str, Any]] = []
    for name in sorted(sets_map.keys()):
        item = sets_map[name]
        entry = _normalize_doc_entry(name, item.metadata)
        set_entries.append(entry)
        _write_entity_readme(item.path.parent, entry)
        if sets_base is None:
            sets_base = item.path.parent.parent

    if objects_base is not None:
        _write_index_readme(objects_base, "OOBB Objects", object_entries)
    if sets_base is not None:
        _write_index_readme(sets_base, "OOBB Part Sets", set_entries)


def cli() -> int:
    parser = argparse.ArgumentParser(description="OOBB Documentation Generator")
    parser.add_argument("--json", default="", help="Output path for JSON documentation")
    parser.add_argument("--html-template", default="", help="Path to HTML template file")
    parser.add_argument("--html-output", default="", help="Output path for HTML documentation")
    parser.add_argument("--markdown", action="store_true", help="Generate Markdown README files")
    parser.add_argument("--objects-root", default=None)
    parser.add_argument("--sets-root", default=None)
    args = parser.parse_args()

    if args.json:
        export_documentation_json(args.json, objects_root=args.objects_root, sets_root=args.sets_root)
    if args.html_template and args.html_output:
        export_documentation_html(
            args.html_template,
            args.html_output,
            objects_root=args.objects_root,
            sets_root=args.sets_root,
        )
    if args.markdown:
        export_documentation_markdown(objects_root=args.objects_root, sets_root=args.sets_root)

    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
