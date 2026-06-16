# ClawHub setup notes for open-novel-writing

Verified from ClawHub skill page: https://clawhub.ai/softmeng/open-novel-writing

## Metadata

- Skill name: `open-novel-writing`
- Publisher: `@softmeng`
- Version shown: `1.0.0`
- Latest version tag shown: `k978k74w8f8eye6bg887zgzm0s82vyfn`
- License shown: `MIT-0`
- Install command shown: `openclaw skills install open-novel-writing`
- Security scans shown: VirusTotal Benign, ClawScan Benign, Static analysis Benign
- Updated: 4d ago, as displayed on 2026-05-06

## Verified file manifest shown by ClawHub search/page snippets

- `SKILL.md` — 12 KB
- `scripts/check_quality.py` — 3.2 KB
- `scripts/auto_write.py` — 12 KB
- `references/novel_template.md` — 2.0 KB
- `references/review_criteria.md` — 2.3 KB
- `references/writing_principles.md` — 2.4 KB

## Setup status

- Installed a scoped `SKILL.md` using only content and metadata visible from the ClawHub page.
- No additional environment variables, credentials, binaries, or global package installs were visible in the verified ClawHub metadata.
- ClawHub metadata mentions optional/supporting scripts and reference files, but the environment could not fetch the ZIP or raw file API through the shell proxy. Those files were not recreated here because their contents were not independently available from ClawHub in this session.
- If you want the full script/reference bundle, run the verified ClawHub install command in an environment where ClawHub downloads are allowed, then inspect the files before enabling automated chapter generation.

## User-facing setup guidance

- Restart Codex to pick up new skills.
- To use this skill safely, start in a dedicated novel project directory before asking it to create or modify `设定/`, `大纲/`, `规格/`, `正文/`, or `评审/` files.
- Ask before installing optional dependencies such as YAML libraries or before making broader environment changes.
