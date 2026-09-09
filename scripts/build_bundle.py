#!/usr/bin/env python3
from __future__ import annotations

import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "package-src"
BUILD_ROOT = ROOT / "build"
PACKAGE = BUILD_ROOT / "claude-marketing-unified"
DIST = ROOT / "dist"
ZIP_PATH = DIST / "claude-marketing-unified.zip"

SOURCES = [
    {
        "name": "Corey Haines — Marketing Skills",
        "repo": "coreyhaines31/marketingskills",
        "commit": "5b2c0007766c6a1cf1d53fd8fc73e979e0821022",
        "namespace": "corey",
        "license_name": "corey-haines-MIT.txt",
        "modules": [
            ("skills/product-marketing", "product-marketing"),
            ("skills/customer-research", "customer-research"),
            ("skills/marketing-plan", "marketing-plan"),
            ("skills/marketing-ideas", "marketing-ideas"),
            ("skills/content-strategy", "content-strategy"),
            ("skills/social", "social"),
            ("skills/marketing-psychology", "marketing-psychology"),
            ("skills/copywriting", "copywriting"),
            ("skills/copy-editing", "copy-editing"),
            ("skills/ads", "ads"),
            ("skills/ad-creative", "ad-creative"),
            ("skills/offers", "offers"),
            ("skills/launch", "launch"),
        ],
    },
    {
        "name": "Rebecca Rae Barton — Claude Marketing",
        "repo": "thatrebeccarae/claude-marketing",
        "commit": "a8a63ec1341f05ec9c1e9cb52b4edeb14e3bdcba",
        "namespace": "rebecca",
        "license_name": "rebecca-rae-MIT.txt",
        "modules": [
            ("skills/brand-voice-guidelines", "brand-voice-guidelines"),
            ("skills/copywriting-frameworks", "copywriting-frameworks"),
        ],
    },
    {
        "name": "Rob Palmer — Claude Code Copywriting Skills",
        "repo": "robpalmer99/claude-code-copywriting-skills",
        "commit": "7dbfd61e0f283ca09c20b3eca3657365e00e991d",
        "namespace": "rob",
        "license_name": "rob-palmer-CC-BY-4.0.txt",
        "modules": [
            ("ad-copy", "ad-copy"),
            ("copychief", "copychief"),
        ],
    },
]


def download_archive(repo: str, commit: str, target: Path) -> None:
    url = f"https://github.com/{repo}/archive/{commit}.zip"
    req = urllib.request.Request(url, headers={"User-Agent": "claude-marketing-unified-builder/1.0"})
    with urllib.request.urlopen(req, timeout=90) as response, target.open("wb") as fh:
        shutil.copyfileobj(response, fh)


def extracted_repo_root(extract_dir: Path) -> Path:
    roots = [p for p in extract_dir.iterdir() if p.is_dir()]
    if len(roots) != 1:
        raise RuntimeError(f"Expected one repository root after extraction, found {len(roots)}")
    return roots[0]


def require_skill(path: Path) -> None:
    skill_file = path / "SKILL.md"
    if not skill_file.is_file():
        raise FileNotFoundError(f"Missing SKILL.md in {path}")
    text = skill_file.read_text(encoding="utf-8", errors="strict")
    if not text.startswith("---") or "name:" not in text or "description:" not in text:
        raise ValueError(f"Invalid skill frontmatter: {skill_file}")


def write_manifest() -> None:
    lines = [
        "# Upstream Manifest",
        "",
        "This file is generated from pinned upstream revisions. The builder fails if a selected module disappears or lacks `SKILL.md`.",
        "",
    ]
    for source in SOURCES:
        lines += [
            f"## {source['name']}",
            f"- Repository: https://github.com/{source['repo']}",
            f"- Pinned commit: `{source['commit']}`",
            f"- Namespace: `modules/{source['namespace']}/`",
            "- Modules:",
        ]
        for _, target_name in source["modules"]:
            lines.append(f"  - `{target_name}`")
        lines.append("")

    manifest = PACKAGE / "references" / "UPSTREAM_MANIFEST.md"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text("\n".join(lines), encoding="utf-8")


def build() -> None:
    if not (SRC / "SKILL.md").is_file():
        raise FileNotFoundError("package-src/SKILL.md is required")

    shutil.rmtree(BUILD_ROOT, ignore_errors=True)
    shutil.rmtree(DIST, ignore_errors=True)
    BUILD_ROOT.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SRC, PACKAGE)

    require_skill(PACKAGE)

    with tempfile.TemporaryDirectory(prefix="marketing-skill-build-") as tmp:
        tmpdir = Path(tmp)
        for index, source in enumerate(SOURCES, start=1):
            archive = tmpdir / f"source-{index}.zip"
            extract_dir = tmpdir / f"source-{index}"
            extract_dir.mkdir()
            print(f"Downloading {source['repo']} @ {source['commit']}")
            download_archive(source["repo"], source["commit"], archive)
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(extract_dir)
            repo_root = extracted_repo_root(extract_dir)

            license_src = repo_root / "LICENSE"
            if not license_src.is_file():
                raise FileNotFoundError(f"Missing LICENSE in {source['repo']}")
            license_dst = PACKAGE / "licenses" / source["license_name"]
            license_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(license_src, license_dst)

            namespace_root = PACKAGE / "modules" / source["namespace"]
            namespace_root.mkdir(parents=True, exist_ok=True)

            for source_dir, target_name in source["modules"]:
                src_module = repo_root / source_dir
                if not src_module.is_dir():
                    raise FileNotFoundError(
                        f"Pinned module missing: {source['repo']}:{source_dir} @ {source['commit']}"
                    )
                require_skill(src_module)
                dst_module = namespace_root / target_name
                if dst_module.exists():
                    raise RuntimeError(f"Duplicate module target: {dst_module}")
                shutil.copytree(src_module, dst_module)

    require_skill(PACKAGE / "modules" / "custom" / "anti-ai-quality")
    write_manifest()

    expected = 1 + sum(len(source["modules"]) for source in SOURCES)
    discovered = list(PACKAGE.glob("modules/*/*/SKILL.md"))
    if len(discovered) != expected:
        raise RuntimeError(f"Expected {expected} specialist SKILL.md files, found {len(discovered)}")

    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(PACKAGE.rglob("*")):
            if path.is_file():
                arcname = Path(PACKAGE.name) / path.relative_to(PACKAGE)
                zf.write(path, arcname.as_posix())

    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = zf.namelist()
        required_root = "claude-marketing-unified/SKILL.md"
        if required_root not in names:
            raise RuntimeError("Built ZIP does not contain the required root SKILL.md")
        if any(not name.startswith("claude-marketing-unified/") for name in names):
            raise RuntimeError("ZIP contains files outside the single skill root folder")

    print(f"Built: {ZIP_PATH}")
    print(f"Specialist modules: {expected}")


if __name__ == "__main__":
    build()
