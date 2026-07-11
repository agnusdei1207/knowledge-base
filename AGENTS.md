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
| `01_basic_theory` | 001~080 전체 writing-method 기준 재작성 및 교정 완료 | 완료 |
| `02_hardware` | 001~110 전체 교정 완료(현재 미커밋 작업) | 완료 |
| `03_software` | 001~135 교정 완료, 136~222 신규 작성 상태(현재 미커밋·최종 검증 전) | 136~222 검증 후 223 |
| `04_network` | 001~015, legacy quality varies | 016 |
| `05_security` | 001~015, legacy quality varies | 016 |
| `06_evaluation` | 001~015, legacy quality varies | 016 |
| `07_law_policy` | 001~015, legacy quality varies | 016 |
| `08_latest_tech` | 001~035, legacy quality varies | 036 |

The tracker records historical progress only. New or rewritten files must follow `writing-method.md`.

### Current Pause Memo (2026-07-11 13:30:42 KST)

사용자 요청에 따라 이 지점에서 작업을 중단했다. 현재 변경 사항은 커밋하거나 푸시하지 않았으며, dirty worktree를 그대로 보존해야 한다.

- 진행·중단·재개 메모에는 특별한 사유가 없으면 `YYYY-MM-DD HH:mm:ss KST` 형식으로 초 단위 시각을 기록한다.

- 실행 중이던 병렬 작업은 모두 중단됨:
  - `software_137_160`
  - `software_161_180`
  - `software_181_198`
- 완료 및 확인 상태:
  - `01_basic_theory` `001~080`: 전체 교정 완료, Docker Zola 빌드 통과
  - `02_hardware` `001~110`: 전체 교정 완료, Docker Zola 빌드 통과
  - `03_software` `001~135`: 교정 완료 및 구조 검증 완료
  - `03_software` `136`: 신규 작성 완료
  - `03_software` `137~198`: 중단된 병렬 작업 결과가 파일로 존재하나 범위 전체의 최종 검수는 미완료
  - `03_software` `199~222`: 신규 작성 및 기본 구조 검증 완료
- 재개 순서:
  1. `03_software` `136~222`를 `_keywords.md`와 대조하여 제목·번호·핵심 내용·문장 자연스러움·표 비교축·절 구성·실무 사례를 최종 검수한다.
  2. 특히 중단된 병렬 범위 `137~198`은 누락·절단·형식 불일치 여부를 먼저 확인한다.
  3. 이상이 없으면 `03_software` `223`부터 직접 작성·교정을 재개한다.
  4. `03_software` 완료 후 나머지 과목을 같은 관점으로 교정한다.
  5. 전체 작업 완료 시 `git diff --check`, Docker Zola 전체 빌드, `git fetch origin`, divergence 확인 후 한 번만 커밋·푸시한다.
- 보존 주의 사항:
  - 같은 번호의 기존 중복 파일은 삭제·이름 변경·병합하지 않는다.
  - `.claude/`는 사용자 소유 미추적 항목이므로 건드리지 않는다.
  - `04_network/129~132`의 기존 미커밋 변경은 보존하되 이번 완료 범위로 계산하지 않는다.
  - `writing-method.md`, `writing-examples.md`에는 이번 문장 교정 원칙과 예시가 미커밋 상태로 반영되어 있다.

현재의 안전한 재개 지점은 **`03_software` 136~222 최종 검수**, 이후 신규 작성 시작 번호는 **223**이다.

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
