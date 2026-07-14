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
| `01_basic_theory` | 001~080 전체 writing-method 기준 재작성 및 교정 완료. 2026-07-14 세션에서 작성법에 '방향성'(작성 근거 최상단 트레이드오프 명제)·'적용 기준 필수화'(Ⅲ 비교표) 게이트를 신설하고 001~080 전체를 이 기준으로 재검수(위키형 결론 재작성, 비교표 요약을 구체적 분기 조건으로 교체, 고아 용어·표기 불일치 정리) | 완료 |
| `02_hardware` | 001~110 전체 정본 준수(쉽게 이해하기 학습용 포함) 재작성 완료, 커밋 `73da2e9f5` 푸시 완료 (2026-07-13) | 완료 |
| `03_software` | 001~135 교정 완료, 136~222 신규 작성 상태(현재 미커밋·최종 검증 전) | 136~222 검증 후 223 |
| `04_network` | 001~015, legacy quality varies | 016 |
| `05_security` | 001~015, legacy quality varies | 016 |
| `06_evaluation` | 001~015, legacy quality varies | 016 |
| `07_law_policy` | 001~015, legacy quality varies | 016 |
| `08_latest_tech` | 001~035, legacy quality varies | 036 |

The tracker records historical progress only. New or rewritten files must follow `writing-method.md`.

### Current Pause Memo (2026-07-12, 작업 계속 진행 중)

사용자가 "1과목부터 하세요. 다시 전체"로 지시해, 완료 표시를 신뢰하지 않고 01_basic_theory부터 순서대로 writing-method.md 기준 전수 재검수를 다시 시작했다. 배치당 10개 파일, 서브에이전트 위임 후 `zola build` 검증 → 커밋·푸시 패턴을 사용한다(로컬 zola 바이너리는 `.tools/zola.exe`에 다운로드해 사용, Docker 불필요 확인).

**재검수에서 반복 확인된 핵심 결함 패턴** (표본 조사 결과 거의 모든 기존 "완료" 파일에서 발견됨, 향후 모든 영역 재검수 시 기본 점검 항목으로 포함할 것):
1. Ⅲ절 비교표가 3축이 아니라 4~7축을 사용(writing-method.md 7절 "정확히 3개" 위반) — 압도적으로 가장 흔한 결함
2. `미리 알고가기` 불릿이 4개 미만(정본 최소 요구 위반)
3. Ⅴ절(원리 및 절차 흐름도) 통째로 누락 — 절차형 키워드에서 다수 발견
4. 근거-본문 정합성 위반(`작성 근거`가 언급한 축·용어가 본문에 없음)
5. 한글/영문 용어 혼용, `A·B 동사` 결합 오류(성격이 다른 두 명사를 한 서술어에 억지로 묶음)
6. 핵심 개념 자체가 본문에서 누락(제목이 명시한 개념인데 설명이 없음)

**완료 및 커밋·푸시 완료 상태 (2026-07-12 기준)**:
- `01_basic_theory` `001~080`: 전체 재검수·재교정 완료, 커밋 `1db6fbaa5` 푸시 완료 (49개 파일 수정)
- `02_hardware` `001~110`: 전체 재검수·재교정 완료, 커밋 `ce2345046` / `eff6d1dfb` / `4a448c43f` 푸시 완료
- `03_software` `135~165`: 재검수·3축 교정 완료, 커밋 `c824b97b1` 푸시 완료
- `03_software` `001~040`: 재검수·재교정 완료, 커밋 `297edb396` 푸시 완료

**미착수 상태**:
- `03_software` `041~135`: 과거 "교정 완료" 표시가 있으나 다른 영역과 동일한 결함 패턴이 있을 가능성이 높음 — 신뢰하지 말고 재검수 필요
- `03_software` `166~198`: 이전 세션에서 중단된 병렬 작업 결과가 파일로 존재하나(git status상 미커밋 M 상태) 이번 세션에서 검증하지 않음 — 그대로 보존, 손대지 않았음
- `03_software` `199~235`: 신규 작성 완료 상태였으나 이번 기준으로 최종 검수 안 됨
- `03_software` `236~320`: 미작성
- `04_network`, `05_security`, `06_evaluation`, `07_law_policy`, `08_latest_tech`: 전 영역 미착수(과거 부분 진행 이력은 아래 "Latest Continuation Memo" 참조, 단 신뢰하지 말고 재검수 대상으로 취급)

**재개 순서**:
1. `041~135`를 10개 단위 배치로 순서대로 재검수(위 6개 결함 패턴 기준 적용)
2. `166~320`을 같은 기준으로 검수·신규 작성
3. `03_software` 완료 후 우선순위대로 `04_network → 05_security → 06_evaluation → 07_law_policy → 08_latest_tech` 재검수(각 영역도 001부터 전수, 완료 표시 불신)
4. 전체 완료 후 `git diff --check`, 전체 `zola build`, `git fetch origin`, divergence 확인 후 최종 커밋·푸시

**보존 주의 사항**:
- 같은 번호의 기존 중복 파일은 삭제·이름 변경·병합하지 않는다. 확인된 중복: `03_software` 107(`_clustered_covering_index` vs `_software_quality_model`), 122·123·124번, 136~236 구간 다수(예: `136_file_system.md` 등 구식 OS/프로그래밍 잔존 파일)
- `.claude/`는 사용자 소유 미추적 항목이므로 건드리지 않는다
- `04_network/129~132`의 기존 미커밋 변경은 보존하되 완료 범위로 계산하지 않는다
- `03_software/166~198`의 기존 미커밋 변경도 이번 세션에서 검증 안 됐으므로 완료 범위로 계산하지 않는다

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
