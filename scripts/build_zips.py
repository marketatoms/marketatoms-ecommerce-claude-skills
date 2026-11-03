#!/usr/bin/env python3
"""Builds the downloads in dist/:

- dist/skill-folders/<skill>/   one self-contained folder per skill (SKILL.md,
                                its own references/, the scripts it needs, and
                                AGENTS.md for the reporting skills). This is
                                what Claude Code installs.
- dist/skills/<skill>.zip       one ZIP per skill (40), holding exactly that
                                skill folder: upload it to the Claude app as is.
- dist/<folder>.zip             one ZIP per category folder (8): the same five
                                skill ZIPs, for downloading a whole folder.
- dist/ecommerce-claude-skills-<version>.zip
                                the whole library in repository layout.

Usage: python3 scripts/build_zips.py
"""

from __future__ import annotations

import io
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SKIP = {".git", "dist", "__pycache__", ".DS_Store"}


def version() -> str:
    m = re.search(r"^## (\d+\.\d+\.\d+)", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else "dev"


def skill_files(folder: Path) -> dict[str, Path]:
    """Archive path (inside the skill folder) -> source file."""
    text = (folder / "SKILL.md").read_text(encoding="utf-8")
    files = {"SKILL.md": folder / "SKILL.md"}
    for ref in sorted((ROOT / "references").glob("*.md")):
        files[f"references/{ref.name}"] = ref
    scripts = sorted(set(re.findall(r"\.\./scripts/([a-z_]+\.py)", text)))
    if scripts:
        scripts.append("leakkit.py")
    for s in scripts:
        files[f"scripts/{s}"] = ROOT / "scripts" / s
    if "AGENTS.md" in text:
        files["AGENTS.md"] = ROOT / "AGENTS.md"
    return files


def skill_zip_bytes(name: str, files: dict[str, Path]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, src in files.items():
            z.write(src, f"{name}/{arc}")
    return buf.getvalue()


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "skill-folders").mkdir(parents=True)
    (DIST / "skills").mkdir()
    categories = sorted(p for p in ROOT.glob("[0-9][0-9]-*") if p.is_dir())
    total = 0
    for cat in categories:
        skills = sorted(p.parent for p in cat.glob("*/SKILL.md"))
        out = DIST / f"{cat.name}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr(f"{cat.name}/README.txt",
                       f"{cat.name}: {len(skills)} Claude Skills by MarketAtoms.\n\n"
                       "Each ZIP in this folder is one skill, ready to upload to the Claude app\n"
                       "(Settings > Capabilities > Skills). Upload them one by one.\n")
            for folder in skills:
                files = skill_files(folder)
                data = skill_zip_bytes(folder.name, files)
                z.writestr(f"{cat.name}/{folder.name}.zip", data)
                (DIST / "skills" / f"{folder.name}.zip").write_bytes(data)
                target = DIST / "skill-folders" / folder.name
                for arc, src in files.items():
                    (target / arc).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, target / arc)
                total += 1
        print(f"{out.relative_to(ROOT)}  ({len(skills)} skills)")

    full = DIST / f"ecommerce-claude-skills-{version()}.zip"
    with zipfile.ZipFile(full, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(ROOT.rglob("*")):
            rel = path.relative_to(ROOT)
            if path.is_file() and not (set(rel.parts) & SKIP) and path.suffix != ".pyc":
                z.write(path, f"ecommerce-claude-skills/{rel}")
    print(f"{full.relative_to(ROOT)}  (whole library)")
    print(f"dist/skills/  ({total} single-skill ZIPs for the Claude app)")
    print(f"dist/skill-folders/  ({total} self-contained skill folders for Claude Code)")


if __name__ == "__main__":
    main()
