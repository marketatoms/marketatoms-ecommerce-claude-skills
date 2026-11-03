#!/usr/bin/env python3
"""Structural check for the library. Fails (exit 1) if:

- the 8 category folders don't each hold exactly 5 skills;
- a skill is missing its front matter, or its name doesn't match its folder;
- a skill is missing a required section, or has them out of order;
- a skill cites a threshold key that doesn't exist in references/thresholds.md;
- a skill cites a relative path (../../references/..., ../../scripts/...) that
  doesn't exist;
- a description duplicates another skill's;
- a new skill (not one of the 12 carried over from shopify-revenue-leak-skills
  1.0.0 unchanged) has no `needs_data` rule, no labelled made-up example, or no
  "Never" guardrail;
- a threshold has no [platform] or [heuristic] tag, or is used nowhere;
- a threshold quoted in the launch post no longer has the value the post states;
- a skill is missing from AGENTS.md or README.md.

It cannot judge whether a skill's advice is right; selftest.py checks the maths.
Usage: python3 scripts/validate_skills.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from leakkit import ROOT, load_thresholds  # noqa: E402

SECTIONS = ["## Use this skill when", "## Required input", "## Live data (MarketAtoms MCP)",
            "## Analysis workflow", "## Decision rules", "## Output format",
            "## Practical example", "## Guardrails"]

FOLDERS = ["01-meta-ads", "02-google-shopping", "03-tracking", "04-conversion",
           "05-basket-pricing", "06-retention", "07-profit-ops", "08-reporting"]
SKILLS_PER_FOLDER = 5

# Copied unchanged (apart from relative paths) from shopify-revenue-leak-skills 1.0.0.
# The newer rules below apply to every other skill.
CARRIED_OVER = {
    "tracking-gap-leak", "wasted-ad-spend-leak", "stockout-ad-spend-leak", "discount-leak",
    "refund-and-return-leak", "checkout-drop-leak", "mobile-conversion-gap-leak",
    "product-page-conversion-leak", "basket-value-gap-leak", "second-order-gap-leak",
    "contribution-margin-leak", "weekly-revenue-leak-readout",
}

# Numbers quoted in the launch post. If one changes here, the post must change too.
POST_VALUES = {
    "ads.wasted_cpa_multiple": 1.5,
    "feed.zero_impression_days": 14,
    "tracking.gap_flag": 0.15,
    "pdp.atc_ratio_floor": 0.5,
    "aov.near_threshold_band": 0.15,
    "repeat.window_days": 90,
    "margin.contribution_floor": 0.10,
}


def skill_folders() -> list[Path]:
    return sorted(p.parent for p in ROOT.glob("[0-9][0-9]-*/*/SKILL.md"))


def main() -> int:
    values = load_thresholds()
    keys = set(values)
    errors: list[str] = []
    descriptions: dict[str, str] = {}
    cited: set[str] = set()

    present = sorted(p.name for p in ROOT.glob("[0-9][0-9]-*") if p.is_dir())
    if present != FOLDERS:
        errors.append(f"category folders are {present}, expected {FOLDERS}")
    for f in FOLDERS:
        n = len(list((ROOT / f).glob("*/SKILL.md")))
        if n != SKILLS_PER_FOLDER:
            errors.append(f"{f}: {n} skills, expected {SKILLS_PER_FOLDER}")

    skills = skill_folders()
    names = [s.name for s in skills]
    for dup in {n for n in names if names.count(n) > 1}:
        errors.append(f"skill name {dup} used in more than one folder")
    missing_carried = CARRIED_OVER - set(names)
    if missing_carried:
        errors.append(f"carried-over skills missing: {', '.join(sorted(missing_carried))}")

    for folder in skills:
        label = f"{folder.parent.name}/{folder.name}"
        text = (folder / "SKILL.md").read_text(encoding="utf-8")
        fm = re.match(r"^---\nname: (.+)\ndescription: (.+)\n---\n", text)
        if not fm:
            errors.append(f"{label}: front matter missing or malformed")
            continue
        name, desc = fm.group(1).strip(), fm.group(2).strip()
        if name != folder.name:
            errors.append(f"{label}: name '{name}' doesn't match folder")
        if len(desc) > 1024:
            errors.append(f"{label}: description over 1024 characters")
        if desc in descriptions.values():
            errors.append(f"{label}: duplicate description")
        descriptions[name] = desc
        positions = [text.find(s) for s in SECTIONS]
        for s, pos in zip(SECTIONS, positions):
            if pos < 0:
                errors.append(f"{label}: missing section '{s}'")
        found = [p for p in positions if p >= 0]
        if found != sorted(found):
            errors.append(f"{label}: sections out of order")
        for key in set(re.findall(r"`([a-z]+\.[a-z_]+)`", text)):
            if key.endswith((".md", ".py")):
                continue
            cited.add(key)
            if key not in keys:
                errors.append(f"{label}: cites unknown threshold `{key}`")
        for rel in set(re.findall(r"`(\.\./[^`]+)`", text)):
            if not (folder / rel).resolve().exists():
                errors.append(f"{label}: path {rel} does not exist")
        if name not in CARRIED_OVER and all(p >= 0 for p in positions):
            example = text[positions[6]:positions[7]]
            guardrails = text[positions[7]:]
            if "needs_data" not in text:
                errors.append(f"{label}: no needs_data rule")
            if "Made-up numbers for illustration" not in example:
                errors.append(f"{label}: practical example not labelled as made-up")
            if "Never" not in guardrails:
                errors.append(f"{label}: guardrails have no 'Never' line")

    # Threshold file hygiene.
    for line in (ROOT / "references" / "thresholds.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*`([a-z_]+\.[a-z_]+)`\s*\|", line)
        if m and not re.search(r"\|\s*\[(platform|heuristic)\]\s*\|", line):
            errors.append(f"thresholds.md: `{m.group(1)}` has no [platform] or [heuristic] tag")
    for script in (ROOT / "scripts").glob("*.py"):
        cited.update(re.findall(r'"([a-z]+\.[a-z_]+)"', script.read_text(encoding="utf-8")))
    for key in sorted(keys - cited):
        errors.append(f"thresholds.md: `{key}` is not used by any skill or script")
    for key, expected in POST_VALUES.items():
        if key not in values or abs(values[key] - expected) > 1e-9:
            errors.append(f"thresholds.md: `{key}` is {values.get(key)}, the launch post says {expected}")

    # Every skill is placed in the system and listed for users.
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for name in names:
        if name not in agents:
            errors.append(f"AGENTS.md doesn't mention {name}")
        if name not in readme:
            errors.append(f"README.md doesn't list {name}")

    if errors:
        print("FAIL")
        print("\n".join(f"  - {e}" for e in errors))
        return 1
    print(f"OK: {len(skills)} skills in {len(FOLDERS)} folders, {len(keys)} thresholds; "
          "all sections, keys, paths and launch-post values check out")
    return 0


if __name__ == "__main__":
    sys.exit(main())
