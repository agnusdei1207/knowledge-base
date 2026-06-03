+++
title = "5. 아호-코라식 (Aho-Corasick) — 다중 패턴 동시 매칭"
date = 2026-04-21

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 아호-코라식 (Aho-Corasick) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 여러 패턴을 하나의 유한 자동자 (Finite Automaton)로 컴파일하여, 텍스트를 단 한 번 순회하면서 O(n + m + z) 시간에 모든 패턴의 등장 위치를 동시에 찾는 다중 패턴 매칭 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **가치**: k개의 패턴 각각에 KMP를 적용하면 O(k×n + m)이지만, 아호-코라식은 텍스트 순회 비용이 패턴 수와 무관하게 O(n)이므로 수천 개의 패턴이 있는 백신 엔진·네트워크 침입 탐지에서 압도적 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 낸다.
> 3. **판단 포인트**: 단일 패턴이면 [KMP](/knowledge-base/studynote/08_algorithm_stats/05_string/094_kmp_algorithm/)/Z [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/), 다중 패턴 동시 매칭이면 아호-코라식, 접두사 기반 자동 완성이면 [트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/)가 1순위 선택이다.

---

## Ⅰ. 개요 및 필요성

악성코드 탐지 엔진은 수만 개의 시그니처 패턴을 텍스트에서 찾아야 한다. 각 패턴에 KMP를 적용하면 O(k×n)으로 수만 배 느려진다. 아호-코라식은 모든 패턴을 <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/">트라이</a> (<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/066_trie/">Trie</a>)</strong> 로 합치고, KMP의 실패 함수 아이디어를 [트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/)의 **실패 링크 (Failure Link)** 로 확장하여 텍스트를 한 번만 순회하게 한다.

### [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)

| 단계 | 복잡도 |
|:---|:---:|
| 자동자 구성 | O(m) — m = 모든 패턴 총 길이 |
| 텍스트 매칭 | O(n + z) — n = 텍스트 길이, z = 총 매칭 수 |
| 전체 | O(n + m + z) |

📢 **섹션 요약 비유**: 아호-코라식은 수천 개의 단어를 동시에 찾는 "워드서치 챔피언"—단어마다 텍스트를 따로 보지 않고, 자동자 하나가 텍스트를 한 번 훑으면서 모든 단어를 동시에 발견한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 단계 1: [트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/) 구축



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">패턴: {"he", "she", "his", "hers"}</div>
<div class="kb-diagram-note">트라이 구조:</div>
<div class="kb-diagram-note">(root)</div>
<div class="kb-diagram-note">h s</div>
<div class="kb-diagram-note">e h</div>
<div class="kb-diagram-note">* r e</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(he)</div></div>
<div class="kb-diagram-note">s *+s→ "she"</div>
<div class="kb-diagram-note">*</div>
<div class="kb-diagram-note">(hers)</div>
<div class="kb-diagram-note">h → i → s → * (his)</div>
</div>
</div>



### 구성 단계 2: 실패 링크 (Failure Link)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">실패 링크: 현재 노드에서 매칭 실패 시 이동할 가장 긴 진짜 접미사 노드</div>
<div class="kb-diagram-note">BFS 순서로 계산:</div>
<div class="kb-diagram-note">node "he" → 실패 링크 → root("e"가 없으면 root)</div>
<div class="kb-diagram-note">node "she" → "he" (접미사 "he" 존재)</div>
<div class="kb-diagram-note">node "hers" → root</div>
<div class="kb-diagram-note">실패 링크 다이어그램 (점선):</div>
<div class="kb-diagram-note">"she" ----→ "he" (she의 접미사 "he" 매칭 가능)</div>
<div class="kb-diagram-note">"his" ----→ "is"→root</div>
</div>
</div>



### 구성 단계 3: 출력 링크 (Output Link)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">출력 링크: 현재 노드 또는 실패 링크 체인에서 완성된 패턴이 있으면 기록</div>
<div class="kb-diagram-note">node "she"의 출력: {"she", "he"} ← 실패 링크로 "he"도 포함</div>
<div class="kb-diagram-note">→ 텍스트 "she"를 처리하면 "she"와 "he" 두 패턴 동시 보고</div>
</div>
</div>



### 텍스트 매칭



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">텍스트: "ushers"</div>
<div class="kb-diagram-note">패턴: {"he", "she", "his", "hers"}</div>
<div class="kb-diagram-note">처리:</div>
<div class="kb-diagram-note">u → root</div>
<div class="kb-diagram-note">s → s 노드</div>
<div class="kb-diagram-note">h → sh 노드</div>
<div class="kb-diagram-note">e → she 노드 → 출력: "she"(위치2), "he"(위치2, 출력링크)</div>
<div class="kb-diagram-note">r → sher 노드</div>
<div class="kb-diagram-note">s → shers? 없음 → 실패링크 이동 → "hers" 노드</div>
<div class="kb-diagram-note">→ 출력: "hers"(위치4)</div>
<div class="kb-diagram-note">결과: "she"@1, "he"@1, "hers"@2 (0-based 시작 인덱스)</div>
</div>
</div>



📢 **섹션 요약 비유**: 실패 링크는 미로에서 막혔을 때 "가장 비슷한 다른 경로"로 순간이동하는 지름길—처음부터 다시 시작하지 않아도 돼.

---

## Ⅲ. 비교 및 연결

### 단일 vs 다중 패턴 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 패턴 수 | 전처리 | 매칭 |
|:---|:---:|:---:|:---:|
| [KMP](/knowledge-base/studynote/08_algorithm_stats/05_string/094_kmp_algorithm/) | 1 | O(m) | O(n) |
| Z [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 1 | O(m) | O(n) |
| [Rabin-Karp](/knowledge-base/studynote/08_algorithm_stats/05_string/096_rabin_karp_algorithm/) | 1~다수 | O(m) | O(n) avg |
| 아호-코라식 | k개 | O(Σm_i) | O(n+z) |
| 서픽스 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) | 임의 | O(n log n) | O(m log n) |

### 자동자 (Automaton) 관점

아호-코라식의 결과물은 DFA (Deterministic Finite Automaton)—각 상태([트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/) 노드)에서 입력 문자에 따른 전이(Transition)가 완전히 정의된 결정적 자동자다. 텍스트 처리 시 상태 전이만 따라가면 되므로 역추적([Backtracking](/knowledge-base/studynote/08_algorithm_stats/01_basics/010_backtracking/)) 없이 O(n) 매칭이 보장된다.

📢 **섹션 요약 비유**: 아호-코라식 자동자는 모든 규칙을 미리 학습한 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 심판—경기(텍스트) 중에 책(패턴 목록)을 찾아볼 필요 없이 즉각 판정한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 주요 활용 사례

- <strong>안티바이러스 (<a href="/knowledge-base/studynote/09_security/04_endpoint_security/323_antivirus/">Antivirus</a>) 엔진</strong>: ClamAV, 맥아피—수만 개 시그니처 동시 검색
- <strong>네트워크 침입 탐지 (<a href="/knowledge-base/studynote/03_network/13_network_security_basics/693_nids_network_intrusion_detection_system/">NIDS</a>)</strong>: [Snort](/knowledge-base/studynote/03_network/13_network_security_basics/694_snort_suricata_misuse_anomaly_detection/), [Suricata](/knowledge-base/studynote/09_security/05_web_app_security/240_suricata_multithreaded_nids_ids_ips_engine/)—패킷 페이로드에서 다중 룰 매칭
- **스팸 필터 (Spam Filter)**: 금칙어/패턴 목록 동시 검사
- **유전체 분석**: 다중 프라이머(Primer) 서열 동시 탐색
- **검색 엔진 하이라이팅**: 여러 검색어의 텍스트 내 위치 동시 표시

### 기술사 판단 기준



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">단일 패턴 + 단순 구현 → KMP 또는 Z 알고리즘</div>
<div class="kb-diagram-note">다중 패턴 동시 탐색 → 아호-코라식 (단 한 번의 텍스트 순회)</div>
<div class="kb-diagram-note">패턴이 사전에 고정 → 아호-코라식 자동자 미리 컴파일</div>
<div class="kb-diagram-note">패턴이 실시간으로 추가/삭제 → Aho-Corasick + 동적 트라이 갱신</div>
<div class="kb-diagram-note">임의 부분 문자열 탐색 → 서픽스 배열</div>
</div>
</div>



📢 **섹션 요약 비유**: 아호-코라식은 공항 세관의 금지 물품 스캐너—짐 하나를 한 번만 통과시켜 수천 가지 금지 물품을 동시에 검사하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

아호-코라식 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 [트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/) + 실패 링크 + 출력 링크의 삼위일체로 다중 패턴 매칭 문제를 O(n + m + z)에 해결한다. 수만 개 패턴이 있어도 텍스트 순회 비용은 O(n)으로 고정되므로, 실시간 트래픽 분석·[바이러스](/knowledge-base/studynote/02_operating_system/10_security/589_virus/) 탐지에서 필수 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 자동자 구성 비용이 O(m)이므로 패턴이 미리 알려진 시나리오에서 최대 효과를 발휘한다.

**결론**: 다중 패턴 동시 매칭이 필요한 모든 시스템—보안, 생물정보학, 검색—에서 아호-코라식이 1순위이며, 텍스트 길이에만 비례하는 O(n) 매칭이 핵심 가치다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| [트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/) ([Trie](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/066_trie/)) | 아호-코라식의 기반 자료구조 |
| [KMP](/knowledge-base/studynote/08_algorithm_stats/05_string/094_kmp_algorithm/) 실패 함수 | 실패 링크의 단일 패턴 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) |
| DFA (Deterministic Finite Automaton) | 완성된 아호-코라식 자동자 |
| 실패 링크 (Failure Link) | [KMP](/knowledge-base/studynote/08_algorithm_stats/05_string/094_kmp_algorithm/) π 함수의 [트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/) 확장 |
| 출력 링크 (Output Link) | 겹치는 패턴 동시 보고 메커니즘 |
| Z [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 단일 패턴 동등 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |

---

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">트라이 (Trie)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">KMP 실패 함수</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DFA (Deterministic Finite Automaton)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">실패 링크 (Failure Link)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">출력 링크 (Output Link)</div></div>
</div>
</div>



이 흐름도는 [트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/) ([Trie](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/066_trie/))에서 출발해 출력 링크 (Output Link)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 아호-코라식은 숨은 그림 찾기를 한 번에 여러 개 동시에 찾는 방법이야—그림을 한 번만 쭉 훑으면 모든 숨은 그림이 동시에 발견돼.
2. 중간에 막히면 "실패 링크"라는 지름길로 이동해서 처음부터 다시 시작하지 않아도 돼.
3. [바이러스](/knowledge-base/studynote/02_operating_system/10_security/589_virus/) 백신이 파일을 스캔할 때 수만 개 [바이러스](/knowledge-base/studynote/02_operating_system/10_security/589_virus/) 시그니처를 동시에 찾는 게 바로 이 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이야!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 98 / 175

← **이전**: [4. Z 알고리즘 (Z-Algorithm) — 접두사 매칭 배열](/knowledge-base/studynote/08_algorithm_stats/05_string/097_z_algorithm/)
**다음**: [6. 런-길이 인코딩 (RLE, Run-Length Encoding) — 연속 반복 압축](/knowledge-base/studynote/08_algorithm_stats/05_string/099_rle/) →

---
