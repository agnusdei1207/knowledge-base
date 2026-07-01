---
title: "TCAM 삼진 CAM 고속 검색 (TCAM)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 94
---

# 📖 【암기용】 개념 완전 이해

> 목적: TCAM을 라우터·스위치가 ACL, 라우팅, QoS 규칙을 한 클럭 수준으로 찾는 하드웨어 검색 구조로 이해하게 만든다.

## 한눈에
- **개요**: 0, 1, don't care 세 상태를 저장해 와일드카드 매칭을 수행하는 고속 검색 메모리
- **왜 필요한가**: L3/L4 ACL, longest prefix match, QoS classification은 수천 규칙을 패킷당 수 마이크로초 안에 찾아야 한다.
- **핵심 직관**: 주소록을 순서대로 찾지 않고 모든 항목을 동시에 비춰 맞는 줄을 즉시 찾는 회로다.

## 깊이 이해
- **배경·문제의식**: 일반 RAM은 주소를 넣으면 해당 위치 값만 읽는다. 네트워크 장비는 목적지 IP, 포트, 프로토콜이 규칙과 맞는지 찾아야 하므로 "값으로 주소를 찾는" CAM이 필요하다.
- **작동 원리**: TCAM entry는 bit 0, bit 1, X(don't care)를 저장한다. 검색 키와 모든 entry를 병렬 비교하고, 우선순위 인코더가 가장 높은 priority match를 선택한다.
- **비유**: 출입 심사에서 모든 조건표를 동시에 대조하고, 더 구체적인 규칙을 먼저 적용하는 방식이다.
- **구체 예시**: `10.10.0.0/16`은 뒤 16비트를 X로 저장한다. 패킷 목적지 `10.10.5.7`은 /16 entry와 /24 entry에 동시에 맞을 수 있어 priority 또는 LPM 규칙으로 선택한다.
- **흔한 오해·주의점**: TCAM은 검색 지연을 낮추지만 면적·전력 비용이 크다. 규칙 폭과 entry 수가 늘면 TCAM bank 분할, 압축, 우선순위 설계가 필요하다.

## 연결 개념
- ACL — permit/deny 규칙을 TCAM entry로 매핑
- LPM — IP prefix 중 가장 긴 prefix 선택
- SDN 스위치 — flow table 매칭에 TCAM 자원 사용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: TCAM 출제 시 CAM과의 차이, don't care 매칭, 네트워크 장비 적용, 자원 한계를 답안화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TCAM(Ternary CAM)은 0·1·X 값을 저장해 와일드카드 기반 병렬 검색을 수행하는 네트워크 장비용 고속 메모리다.
> 2. **가치**: ACL, QoS, LPM, flow table을 수천 entry 규모로 패킷 라인레이트에서 매칭한다.
> 3. **판단 포인트**: TCAM entry 수, key width, priority, power budget, overflow 시 software path 전환을 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 하드웨어 검색 구조 이해 확인 | CAM vs TCAM, 0/1/X, 병렬 비교 | RAM처럼 주소 기반 조회로 설명 |
| 네트워크 적용 판단 확인 | ACL, LPM, QoS, OpenFlow match | 적용 사례 없이 회로 구조만 서술 |
| 운영 리스크 인식 확인 | TCAM exhaustion, rule ordering, power | entry 한계와 우선순위 누락 |

> 요약: 이 문제는 TCAM의 삼진 매칭 원리와 네트워크 장비 자원 관리까지 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

TCAM은 와일드카드 조건을 병렬 검색하는 하드웨어 메모리다. 라우터와 스위치는 패킷마다 ACL, 라우팅 prefix, QoS class를 즉시 결정해야 한다. 소프트웨어 순차 검색으로는 100Gbps 라인레이트 처리가 어려워 TCAM 기반 매칭이 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Packet Header -> Search Key -> TCAM Entries 0/1/X
              -> Parallel Match -> Priority Encoder -> Action SRAM
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Search Key | IP, port, protocol, VLAN 등 추출 | key width 160b·320b 등 |
| TCAM Entry | 0/1/X로 규칙 저장 | prefix와 wildcard 표현 |
| Priority Encoder | 다중 match 중 우선순위 선택 | ACL 순서, LPM 연계 |
| Action SRAM | match 결과의 next-hop·permit·QoS 저장 | TCAM은 index, SRAM은 action |

> 요약: TCAM은 패킷 헤더를 삼진 entry와 병렬 비교하고 action SRAM에서 처리 결과를 읽는다.

---

## Ⅲ. 동작원리 및 흐름도

```text
헤더 파싱 -> 검색 키 생성 -> 모든 TCAM entry 병렬 비교
-> match vector 생성 -> 우선순위 선택 -> action 실행
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | L2~L4 헤더 필드 추출 | key width 초과 여부 |
| 2 | TCAM entry와 0/1/X 비교 | don't care bit 정상 처리 |
| 3 | match vector 생성 | 다중 match 검출 |
| 4 | priority encoder로 최종 entry 선택 | ACL 순서·LPM 우선순위 |
| 5 | action SRAM에서 permit, drop, next-hop 실행 | 라인레이트 유지 |

> 요약: TCAM은 순차 탐색 없이 모든 entry를 동시에 비교하고 우선순위 규칙으로 최종 action을 결정한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | TCAM | 수치 컬럼 |
|:---|:---|:---|:---|
| 검색 방식 | RAM hash, trie | 병렬 와일드카드 매칭 | 1~수 클럭 검색 |
| 표현력 | exact match 중심 | prefix·range·mask 표현 | 0/1/X 3상태 |
| 적용 영역 | CPU software path | ACL, LPM, QoS, flow table | 수천~수십만 entry |
| 한계 | 전력 낮음 | 면적·전력·entry 한계 | TCAM overflow 위험 |

> 요약: TCAM은 와일드카드 검색 지연을 낮추지만 entry 자원과 전력 예산이 설계 제약이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 검색 구조 | Hash table | TCAM wildcard | prefix·mask 조건 다수 |
| 라우팅 | Software trie | TCAM LPM | 100Gbps line-rate 필요 |
| 정책 처리 | CPU ACL | TCAM ACL | ACL 1,000개 이상, pps 증가 |

> 요약: TCAM은 조건 매칭이 복합적이고 패킷당 처리 시간이 제한될 때 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| TCAM 고갈 | ACL·QoS·route entry 증가 | rule compression, bank 분리 | TCAM usage 80% 이하 |
| 우선순위 오류 | ACL 순서·overlap | shadow rule 분석, hit counter | shadowed rule 0건 |
| software punt | TCAM miss·overflow | default route, capacity 증설 | CPU punt pps 1% 이하 |

> 요약: TCAM 운영은 entry 용량, 규칙 중복, software punt를 지속 점검해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 자원 사용률 | TCAM entry 80% 이하 | switch ASIC show command |
| 매칭 정확도 | ACL hit counter 기대값 일치 | packet test, counter |
| 처리 경로 | punt packet 1% 이하 | CPU queue, ASIC counter |

> 요약: 도입 효과는 TCAM 사용률, 규칙 hit, CPU punt 감소로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. ACL·QoS·route 정책을 entry 수와 key width로 산정하고 TCAM usage 80% 이하 기준 설정
2. 중복·shadow ACL을 정리해 TCAM entry를 압축하고 hit counter 0인 규칙을 월 1회 제거
3. overflow 발생 시 software punt rate를 감시하고 ASIC profile, 장비 증설, 정책 분할을 적용

**결론 (2줄):**
- 기술사 판단: line-rate ACL·LPM·QoS가 필요한 스위치/라우터는 TCAM을 선택하되 entry 용량과 전력 예산을 함께 검토해야 함
- 향후 방향: P4 programmable pipeline과 TCAM/SRAM hybrid 구조로 유연한 match-action 처리가 확대됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | 0/1/X 병렬 매칭 원리 | CAM·RAM 대비 차이와 적용 |
| 요구사항 명시형 | "비교하시오", "방안을 제시하시오", "설계하시오" | ACL·LPM 처리 흐름 설계 | TCAM 고갈·우선순위·punt 대응 |

> 요약: 포괄형은 삼진 검색 원리, 요구사항 명시형은 entry 자원 관리와 정책 처리 기준을 강조한다.
