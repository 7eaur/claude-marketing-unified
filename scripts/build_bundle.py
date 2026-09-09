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
PACKAGE = BUILD_ROOT / "chatgpt-marketing-unified"
DIST = ROOT / "dist"
ZIP_PATH = DIST / "chatgpt-marketing-unified.zip"

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
        "name": "Rebecca Rae Barton — Marketing Skills",
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
        "name": "Rob Palmer — Copywriting Skills",
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
    req = urllib.request.Request(url, headers={"User-Agent": "chatgpt-marketing-unified-builder/2.0"})
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


def convert_entry_to_playbook(module_dir: Path) -> None:
    entry = module_dir / "SKILL.md"
    if not entry.is_file():
        raise FileNotFoundError(f"Missing module SKILL.md before conversion: {module_dir}")
    playbook = module_dir / "PLAYBOOK.md"
    if playbook.exists():
        raise RuntimeError(f"PLAYBOOK.md already exists: {playbook}")
    entry.rename(playbook)


def write_manifest() -> None:
    lines = [
        "# Upstream Manifest",
        "",
        "This file is generated from pinned upstream revisions. The builder fails if a selected upstream module disappears or lacks its original `SKILL.md` entry file.",
        "",
        "In the final ChatGPT package, each selected upstream entry file is renamed to `PLAYBOOK.md` so the ZIP exposes only one installable root `SKILL.md`.",
        "",
    ]
    for source in SOURCES:
        lines += [
            f"## {source['name']}",
            f"- Repository: https://github.com/{source['repo']}",
            f"- Pinned commit: `{source['commit']}`",
            f"- Packaged path: `references/playbooks/{source['namespace']}/`",
            "- Playbooks:",
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

    # Move the original local quality module into ChatGPT supporting resources.
    custom_src = PACKAGE / "modules" / "custom" / "anti-ai-quality"
    require_skill(custom_src)
    custom_dst = PACKAGE / "references" / "playbooks" / "custom" / "anti-ai-quality"
    custom_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(custom_src), str(custom_dst))
    convert_entry_to_playbook(custom_dst)
    shutil.rmtree(PACKAGE / "modules", ignore_errors=True)

    with tempfile.TemporaryDirectory(prefix="chatgpt-marketing-skill-build-") as tmp:
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

            namespace_root = PACKAGE / "references" / "playbooks" / source["namespace"]
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
                    raise RuntimeError(f"Duplicate playbook target: {dst_module}")
                shutil.copytree(src_module, dst_module)
                convert_entry_to_playbook(dst_module)

    write_manifest()

    expected_playbooks = 1 + sum(len(source["modules"]) for source in SOURCES)
    discovered_playbooks = list(PACKAGE.glob("references/playbooks/*/*/PLAYBOOK.md"))
    if len(discovered_playbooks) != expected_playbooks:
        raise RuntimeError(
            f"Expected {expected_playbooks} specialist PLAYBOOK.md files, found {len(discovered_playbooks)}"
        )

    # ChatGPT upload should expose one installable Skill manifest only.
    skill_manifests = list(PACKAGE.rglob("SKILL.md"))
    if skill_manifests != [PACKAGE / "SKILL.md"]:
        raise RuntimeError(
            "Final ChatGPT package must contain exactly one SKILL.md at the skill root. "
            f"Found: {[str(p.relative_to(PACKAGE)) for p in skill_manifests]}"
        )

    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(PACKAGE.rglob("*")):
            if path.is_file():
                arcname = Path(PACKAGE.name) / path.relative_to(PACKAGE)
                zf.write(path, arcname.as_posix())

    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = zf.namelist()
        required_root = "chatgpt-marketing-unified/SKILL.md"
        if required_root not in names:
            raise RuntimeError("Built ZIP does not contain the required ChatGPT root SKILL.md")
        if any(not name.startswith("chatgpt-marketing-unified/") for name in names):
            raise RuntimeError("ZIP contains files outside the single skill root folder")
        nested_manifests = [name for name in names if name.endswith("/SKILL.md") and name != required_root]
        if nested_manifests:
            raise RuntimeError(f"ZIP contains nested SKILL.md manifests: {nested_manifests}")

    print(f"Built: {ZIP_PATH}")
    print(f"Specialist playbooks: {expected_playbooks}")
    print("Installable SKILL.md manifests: 1")


if __name__ == "__main__":
    build()
