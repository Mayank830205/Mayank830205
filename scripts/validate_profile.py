from pathlib import Path
import re
import xml.etree.ElementTree as ET

from PIL import Image
import yaml


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
WORKFLOW = ROOT / ".github" / "workflows" / "snake.yml"
ALLOWED_PLACEHOLDERS = {
    "YOUR_GITHUB_USERNAME",
    "YOUR_LINKEDIN_URL",
    "YOUR_PORTFOLIO_URL",
    "YOUR_EMAIL",
}


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


markdown = README.read_text(encoding="utf-8")

placeholders = set(re.findall(r"YOUR_[A-Z_]+", markdown))
check(
    placeholders == ALLOWED_PLACEHOLDERS,
    f"Unexpected placeholder set: {sorted(placeholders)}",
)

local_refs = re.findall(r'(?:src|href)="(\./[^"?#]+)', markdown)
missing_refs = [ref for ref in local_refs if not (ROOT / ref[2:]).exists()]
check(not missing_refs, f"Missing local references: {missing_refs}")

banner = Image.open(ROOT / "assets" / "banner.png")
check(banner.size == (2560, 1440), f"Wrong banner size: {banner.size}")
banner.verify()

project_svgs = sorted((ROOT / "assets" / "projects").glob("*.svg"))
check(len(project_svgs) == 6, f"Expected six project SVGs, found {len(project_svgs)}")
for svg in project_svgs:
    ET.parse(svg)

required_sections = [
    "## Turning data into decisions",
    "## About me",
    "## Tech stack",
    "## Featured projects",
    "## GitHub analytics",
    "## Current focus",
    "## Learning roadmap",
    "## 2026 goals",
    "## Achievements",
    "## Certifications",
    "## Let’s connect",
]
missing_sections = [section for section in required_sections if section not in markdown]
check(not missing_sections, f"Missing README sections: {missing_sections}")

check(markdown.count("<table>") == markdown.count("</table>"), "Unbalanced table tags")
check(markdown.count("<div") == markdown.count("</div>"), "Unbalanced div tags")
check(markdown.count("<a ") == markdown.count("</a>"), "Unbalanced anchor tags")
check("href=\"#\"" not in markdown, "Found an empty anchor link")
check('src=""' not in markdown, "Found an empty image source")

workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
check("jobs" in workflow and "generate" in workflow["jobs"], "Missing generate job")
steps = workflow["jobs"]["generate"]["steps"]
check(len(steps) == 2, f"Expected two workflow steps, found {len(steps)}")
check(
    steps[0].get("uses") == "Platane/snk/svg-only@v3.5.0",
    "Unexpected snake action version",
)
check(
    steps[1].get("uses") == "crazy-max/ghaction-github-pages@v5",
    "Unexpected publishing action version",
)
check(
    steps[1].get("with", {}).get("target_branch") == "output",
    "Snake assets must publish to the output branch",
)

print("Profile validation passed")
print(f"- Banner: {banner.size[0]}x{banner.size[1]}")
print(f"- Project artwork: {len(project_svgs)} valid SVG files")
print(f"- Local references: {len(local_refs)} resolved")
print(f"- Placeholders: {', '.join(sorted(placeholders))}")
print("- README structure and workflow: valid")
