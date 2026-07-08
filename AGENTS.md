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
| `01_basic_theory` | 001~080, writing-method 기준 재작성 완료 | 완료 |
| `02_hardware` | 001~040, writing-method 기준 교정 완료 | 041 |
| `03_software` | 001~015, legacy quality varies | 016 |
| `04_network` | 001~015, legacy quality varies | 016 |
| `05_security` | 001~015, legacy quality varies | 016 |
| `06_evaluation` | 001~015, legacy quality varies | 016 |
| `07_law_policy` | 001~015, legacy quality varies | 016 |
| `08_latest_tech` | 001~035, legacy quality varies | 036 |

The tracker records historical progress only. New or rewritten files must follow `writing-method.md`.

### Latest Continuation Memo (2026-07-08)

Use this memo to continue `08_latest_tech` rewrite work without re-discovery.

- Recently rewritten and pushed in canonical `writing-method.md` format:
  - `08_latest_tech` `191~200` commit `6e7f0fd33`
  - `08_latest_tech` `201~210` commit `4288ae686`
  - `08_latest_tech` `211~220` commit `cd1f346a6`
  - `08_latest_tech` `221~230` commit `60c80df55`
  - `08_latest_tech` `231~240` commit `51db9f096`
  - `08_latest_tech` `241~250` commit `22e116c84`
  - `08_latest_tech` `251~260` commit `a71c967df`
  - `08_latest_tech` `261~270` commit `6639670ca`
  - `08_latest_tech` `271~280` commit `a0c857c38`
  - `08_latest_tech` `281~290` commit `87f88f6f8`
  - `08_latest_tech` `291~300` commit `e7736e835`
  - `08_latest_tech` `301~310` commit `8d6eba9ac`
  - `08_latest_tech` `311~320` commit `14525c8ea`
  - `08_latest_tech` `321~330` commit `2cdf4f2f1`
  - `08_latest_tech` `331~340` commit `0708b7b55`
  - `08_latest_tech` `341~350` commit `0c3f4217c`
- Current practical next start for `08_latest_tech`: `351`
- `351~360` file discovery already checked. Use these canonical files and leave duplicate same-`NNN` files untouched unless the user explicitly approves cleanup:
  - `351_verifiable_credential.md`
  - `352_zero_knowledge_proof.md`
  - `353_nft_non_fungible_token.md` not `353_nft.md`
  - `354_metaverse.md`
  - `355_spatial_computing.md`
  - `356_extended_reality.md`
  - `357_web3.md` not `357_digital_twin.md`
  - `358_decentralized_physical_infrastructure_network.md` not `358_hmi.md`
  - `359_confidential_ai.md` not `359_bci.md`
  - `360_ai_native_application.md` not `360_internet_of_behaviors.md`
- Additional duplicate-file choices already used in prior batches and should be kept consistent:
  - `315_change_data_capture.md` not `315_cdc.md`
  - `318_lakehouse_medallion_architecture.md` not `318_medallion_architecture.md`
  - `334_v2x_vehicle_to_everything.md` not `334_v2x.md`
  - `335_adas_advanced_driver_assistance_system.md` not `335_adas.md`
  - `336_ads_automated_driving_system.md` not `336_ads.md`
  - `337_iso_pas_8800_ai_safety.md` not `337_iso_pas_8800.md`
  - `347_qkd_quantum_key_distribution.md` not `347_qkd.md`
  - `350_did_decentralized_identifier.md` not `350_did.md`
- Validation loop used successfully for each 10-file batch:
  - rewrite 10 canonical files
  - run `zola build`
  - verify rendered metadata in `public/cspe/08_latest_tech/.../index.html` for `문제 번호`, `기출 여부`, `기출 회차`, `비고`
  - run `git fetch origin`
  - run `git rev-list --left-right --count origin/main...HEAD`
  - commit/push the 10 rewritten files only

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
