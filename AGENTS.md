# Agent Rules

When you need company policy, process, architecture, project history, or document context, use the `knowledgebase` MCP server first.

- Use `search_docs` before guessing a filename.
- Use `get_doc` before summarizing any policy or workflow.
- Use `related_docs` when the current page may be a hub or partial view.
- Treat `content/*.md` as the canonical source of truth.
- If the MCP server has a relevant document, do not answer from memory alone.

---

## Repository Scope

This repository is for 컴퓨터시스템응용기술사(CSPE) study content.

- Main CSPE notes: `content/cspe/`
- Exam strategy, past questions, templates: `content/exam/cs/`
- Personal CS study notes: `content/studynote/`

Do not use `content/studynote/` as an authoritative source for CSPE keyword selection or CSPE answer writing. CSPE notes must be created under `content/cspe/`.

---

## Canonical Writing Method

The only canonical CSPE note writing method is:

- `content/exam/cs/writing-method.md`

Reference-only documents:

- `content/exam/cs/model-answer.md`
- `content/exam/cs/master-template.md`

If any instruction conflicts, follow `writing-method.md`. Do not maintain separate old writing-method variants in `AGENTS.md`.

---

## Current Progress

Keyword extraction is complete across all 8 CSPE areas. Total: 1,370 keywords.

| # | Area | Folder | Keywords |
|:--:|:---|:---|:--:|
| 1 | 컴퓨터 기초이론 | `01_basic_theory` | 80 |
| 2 | 하드웨어 시스템 | `02_hardware` | 110 |
| 3 | 시스템·응용 소프트웨어 | `03_software` | 320 |
| 4 | 컴퓨터 통신·네트워크 | `04_network` | 150 |
| 5 | 시스템 보안 | `05_security` | 240 |
| 6 | 컴퓨터 시스템 평가 | `06_evaluation` | 60 |
| 7 | 법규·정책·표준 | `07_law_policy` | 50 |
| 8 | 최신 기술 동향 | `08_latest_tech` | 360 |

Rewrite tracker:

| Area | Completed | Next Start |
|:---|:---|:---|
| `01_basic_theory` | 001~050, legacy quality varies | 051 |
| `02_hardware` | 001~015, legacy quality varies | 016 |
| `03_software` | 001~015, legacy quality varies | 016 |
| `04_network` | 001~015, legacy quality varies | 016 |
| `05_security` | 001~015, legacy quality varies | 016 |
| `06_evaluation` | 001~015, legacy quality varies | 016 |
| `07_law_policy` | 001~015, legacy quality varies | 016 |
| `08_latest_tech` | 001~035, legacy quality varies | 036 |

The tracker records historical progress only. New or rewritten files must follow `writing-method.md`.

---

## CSPE Work Rules

- Work from `content/cspe/{area}/_keywords.md`.
- File path: `content/cspe/{area}/{NNN}_{english_snake}.md`.
- Frontmatter `weight` must be an unquoted integer, not a zero-padded string.
- Use YAML frontmatter with `---`; do not introduce another build chain.
- Do not generate keyword files with scripts. Write each note directly.
- Existing duplicate `NNN` files require user confirmation before deletion, renumbering, or merge.
- Before pushing, run `zola build`.
- For rewrite batches, commit and push every 10 files.
- Push after `git fetch` and diverge check.

Priority order for large batches:

`08_latest_tech -> 05_security -> 03_software -> 04_network -> 02_hardware -> 01_basic_theory -> 06_evaluation -> 07_law_policy`

---

## Build And Deploy

Baseline build command:

```bash
zola build
```

If CI fails:

- `build` job failure means content/build issue; inspect and fix.
- `deploy`-only failure or `cancelled` is usually GitHub Pages deployment instability or concurrency cancellation; do not edit content for deploy-only failures.
- For deploy-only failure, rerun failed jobs with `gh run rerun <id> --failed`.

---

## Audit Backlog

Use these only to find old-file cleanup targets. They are not writing-method rules.

```bash
rg -n "【암기용】|【답안용】|Ⅴ\\. 심화|Ⅵ\\. 리스크|> 목적:" content/cspe
rg -n "비교 축|기존/대안 \\| 본 키워드" content/cspe
rg -n '"studynote-|^weight: *"?0[0-9]|[┌┐└┘│─▶├┤┬┴┼]' content/cspe
```

Known backlog:

- Duplicate `NNN` files: 105, user confirmation required before cleanup.
- Legacy files may still contain old split blocks, old section names, placeholder table headers, informal tone, or invalid frontmatter.
