---
title: "네트워크 자동화 — Ansible·RESTCONF·NETCONF (Network Automation)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 73
---

# 📖 【암기용】 개념 완전 이해

> 목적: 네트워크 자동화를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 장비 설정·검증·복구를 코드와 API로 반복 실행하는 운영 방식
- **왜 필요한가**: 수백 대 스위치와 라우터를 CLI로 수동 변경하면 오타, 순서 오류, 변경 이력 누락이 발생한다. 자동화는 동일 절차를 Ansible playbook, NETCONF, RESTCONF, YANG 모델로 실행한다.
- **핵심 직관**: 사람이 장비마다 명령을 치는 방식에서, 검증된 작업지시서를 시스템이 장비 API에 맞춰 실행하는 방식으로 바뀐다.

## 깊이 이해
- **배경·문제의식**: 전통 네트워크 운영은 장비 벤더별 CLI와 수동 승인에 의존했다. 클라우드와 SDN 환경에서는 VLAN, ACL, BGP, QoS 변경이 애플리케이션 배포 속도와 맞물려 분 단위로 처리되어야 한다.
- **작동 원리**: Ansible은 agentless SSH/API 방식으로 선언형 playbook을 실행한다. NETCONF는 SSH 기반 RPC와 XML, RESTCONF는 HTTP 기반 REST와 JSON/XML을 사용한다. YANG은 장비 설정과 상태 데이터를 모델로 정의한다.
- **비유**: 수기로 전기 배선을 바꾸는 대신, 표준 도면과 점검표를 입력하면 자동 장비가 같은 순서로 배선하고 전압을 측정하는 구조와 같다.
- **구체 예시**: 신규 VLAN 120과 VXLAN VNI 10120을 40대 ToR에 반영할 때, Git MR 승인 후 Ansible playbook이 NETCONF edit-config를 실행하고, get-config와 ping test로 결과를 검증한다.
- **흔한 오해·주의점**: 자동화는 CLI 명령을 반복 실행하는 스크립트가 아니다. 입력 검증, 변경 전 백업, dry-run, rollback, 관측 지표가 없으면 오류 전파 속도만 커진다.

## 연결 개념
- IaC — 네트워크 상태를 코드 저장소와 변경 승인 절차로 관리
- YANG — 장비 설정·상태 데이터 모델 표준
- Intent-Based Networking — 자동화 위에 의도 해석과 검증 루프를 추가한 모델

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 자동화 도구 나열이 아니라, 모델 기반 설정·검증·롤백 체계를 제시해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 네트워크 자동화는 Ansible, NETCONF/RESTCONF, YANG을 사용해 구성 변경과 상태 검증을 코드 기반 절차로 실행하는 운영 체계이다.
> 2. **가치**: 변경 시간 45분 수동 작업을 5분 playbook 실행으로 줄이고, 설정 drift와 미승인 변경을 Git diff로 추적한다.
> 3. **판단 포인트**: 선언형 모델, 장비 API, 검증 테스트, rollback, 감사로그를 하나의 파이프라인으로 묶어야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 자동화 구조 이해 확인 | Ansible, NETCONF, RESTCONF, YANG, GitOps | 단순 스크립트 실행으로 축소 |
| 운영 통제 역량 확인 | dry-run, config backup, rollback, change window | 장애 전파와 승인 절차 누락 |
| 검증 중심 사고 확인 | pre-check/post-check, idempotency, drift detection | 자동 변경 후 결과 검증 생략 |

> 요약: 이 문제는 도구 이름보다 변경 전·중·후 검증과 롤백이 포함된 네트워크 운영 파이프라인을 요구한다.

---

## Ⅰ. 개요 및 필요성

네트워크 자동화는 장비 구성과 검증을 코드·API 기반으로 처리하는 운영 방식이다. 수동 CLI 변경은 오타, 순서 불일치, 변경 이력 누락을 만든다. Ansible, NETCONF/RESTCONF, YANG을 적용하면 반복 변경을 표준화하고 승인·검증·복구 절차를 자동 실행할 수 있다.

---

## Ⅱ. 구조 및 구성요소

```text
Git Change Request -> CI Validation -> Automation Engine Ansible
-> Device API NETCONF/RESTCONF -> Network Device Config/State
-> Post-check Telemetry -> Rollback/Approval Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Git Repository | 의도한 설정과 변경 이력 저장 | MR/PR 승인, diff 추적 |
| Ansible | playbook 기반 실행 엔진 | agentless, idempotent task |
| NETCONF | XML RPC 기반 설정 관리 | SSH 830, candidate datastore |
| RESTCONF | HTTP REST 기반 설정·상태 API | JSON/XML, YANG data tree |
| YANG Model | 설정·상태 데이터 스키마 | vendor-neutral, vendor-specific 병행 |

> 요약: 자동화 구조는 Git 변경 요청을 API 기반 장비 설정으로 반영하고, telemetry와 rollback으로 결과를 통제한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Intent/Config Change -> Syntax/Policy Lint -> Pre-check
-> Dry-run -> Commit via NETCONF/RESTCONF -> Post-check
-> Drift Detection -> Rollback if KPI Violation
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 변경 요청을 YAML/JSON 변수와 playbook으로 작성 | schema validation 통과 |
| 2 | 사전 점검으로 장비 상태·백업 확보 | reachability, config backup 100% |
| 3 | dry-run과 diff로 변경 영향 확인 | unexpected diff 0건 |
| 4 | NETCONF edit-config 또는 RESTCONF PATCH 실행 | API status 2xx, RPC ok |
| 5 | 사후 점검과 필요 시 rollback 실행 | packet loss, BGP state, config drift |

> 요약: 네트워크 자동화는 작성, 검증, 실행, 사후 확인, 복구를 한 흐름으로 연결해야 운영 사고를 줄인다.

---

## Ⅳ. 특징

| 구분 | 수동 CLI 운영 | 네트워크 자동화 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 변경 방식 | 장비별 직접 입력 | playbook/API 일괄 실행 | 40대 장비 45분에서 5분 목표 |
| 데이터 모델 | 벤더별 명령어 | YANG schema | RFC 7950, OpenConfig |
| 검증 | 작업자 눈검사 | pre/post-check 자동 수집 | BGP Established 100%, drift 0건 |
| 감사 | 터미널 로그 의존 | Git commit, job log | 변경자·승인자·시간 추적 |

> 요약: 네트워크 자동화는 속도보다 모델 기반 검증, 변경 이력, 롤백 가능성을 답안의 중심에 둔다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 실행 방식 | CLI 스크립트 | Ansible + NETCONF/RESTCONF | 장비 20대 이상 반복 변경 |
| 모델 | 텍스트 명령 | YANG/OpenConfig | 벤더 혼합 환경 |
| 운영/위험 | 작업자 숙련도 의존 | 승인·검증·rollback 파이프라인 | 변경 실패 허용 시간 10분 이하 |

> 요약: 자동화는 장비 수와 변경 빈도가 증가하고, 벤더 혼합과 감사 요구가 존재할 때 우선 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오류 일괄 전파 | 잘못된 변수·템플릿 | staged rollout, canary device | 실패 장비 비율 0% 목표 |
| Drift 누락 | 수동 변경과 코드 불일치 | scheduled get-config diff | drift count 0건 |
| API 호환성 | 벤더 YANG 차이 | OpenConfig 우선, vendor module mapping | RPC error rate 1% 이하 |

> 요약: 자동화 리스크는 속도보다 오류 전파이며, 단계 배포와 drift 검출로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 변경 성공률 | job success 99% 이상 | CI/CD job result |
| 롤백 시간 | MTTR 10분 이하 | rollback playbook timestamp |
| 설정 일치 | desired vs running diff 0건 | NETCONF get-config, Git diff |

> 요약: 네트워크 자동화 성과는 성공률, 롤백 시간, 설정 일치율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. VLAN, BGP, ACL, VXLAN 변경을 Git 변수 파일과 Ansible role로 표준화하고 schema lint를 필수 gate로 둠
2. NETCONF candidate datastore와 confirmed-commit, RESTCONF PATCH, 사전 백업으로 변경 실패 시 10분 내 rollback 수행
3. post-check에 BGP state, interface error, packet loss, config drift를 포함해 변경 전후 자동 비교 보고서를 생성함

**결론 (2줄):**
- 기술사 판단: 장비 20대 이상 반복 변경과 감사 요구가 있으면 CLI 수동 운영보다 API·YANG 기반 자동화 체계를 선택함
- 향후 방향: 자동화는 Intent-Based Networking과 결합해 의도 입력, 정책 검증, 폐루프 복구 구조로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | Git, Ansible, NETCONF/RESTCONF, YANG 흐름 | 수동 CLI 대비 변경·검증·감사 차이 |
| 요구사항 명시형 | "방안을 제시하시오", "운영하시오", "설계하시오" | dry-run, staged rollout, rollback 절차 | drift, API 호환성, MTTR 지표 |

> 요약: 설명형은 도구와 API 관계, 운영형은 변경 실패 통제와 검증 지표를 중심으로 구성한다.
