---
title: "Intent-Based Networking (Intent-Based Networking)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 74
---

# 📖 【암기용】 개념 완전 이해

> 목적: Intent-Based Networking을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 사람이 원하는 네트워크 목표를 정책으로 입력하면 시스템이 설계·배포·검증·수정을 반복하는 폐루프 네트워크
- **왜 필요한가**: 장비 설정을 직접 입력하는 방식은 의도와 실제 상태가 어긋나기 쉽다. IBN은 "개발망은 DB망에 TCP 5432만 접근" 같은 목표를 정책, 구성, 검증으로 변환한다.
- **핵심 직관**: 내비게이션에 목적지를 입력하면 경로 계산, 주행 안내, 정체 회피를 계속 수행하듯 네트워크도 의도를 지속 검증한다.

## 깊이 이해
- **배경·문제의식**: 네트워크 자동화는 명령 실행을 자동화하지만, 변경 결과가 의도와 맞는지 계속 확인하지 않으면 구성 편류가 생긴다. 클라우드·캠퍼스·데이터센터 통합 환경에서는 정책 일관성이 운영 난도와 직결된다.
- **작동 원리**: 사용자는 비즈니스 의도를 정책으로 입력한다. 컨트롤러는 정책을 장비 설정으로 변환하고 배포한다. Telemetry는 실제 상태를 수집하며, assurance 엔진은 의도와 실제 상태 차이를 분석해 수정 작업을 생성한다.
- **비유**: 항공 관제에서 목적지와 안전 간격을 입력하면, 관제 시스템이 항로·고도·충돌 회피를 계속 계산하는 구조와 같다.
- **구체 예시**: "POS 단말은 결제 서버 TCP 443만 허용" 의도를 입력하면, 시스템은 VLAN/SGT/ACL을 생성하고 flow telemetry로 비허용 포트 통신 0건을 확인한다.
- **흔한 오해·주의점**: IBN은 제품명이나 단순 자동화 스크립트가 아니다. 의도 모델, 정책 변환, 상태 수집, 검증, 자동 수정의 폐루프가 있어야 IBN이라 부를 수 있다.

## 연결 개념
- 네트워크 자동화 — IBN의 실행 계층
- SDN Controller — 정책 변환과 중앙 제어 기반
- Network Telemetry — 의도와 실제 상태 차이를 측정하는 데이터

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: IBN은 자동화 도구가 아니라 의도, 변환, 배포, 검증, 수정의 폐루프 운영 모델임을 드러낸다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Intent-Based Networking은 비즈니스 의도를 네트워크 정책과 장비 설정으로 변환하고 실제 상태를 지속 검증하는 폐루프 네트워크 운영 모델이다.
> 2. **가치**: CLI 명령 중심 운영을 목표 상태 중심 운영으로 전환해 정책 위반, 구성 편류, 장애 전파를 telemetry 기준으로 탐지한다.
> 3. **판단 포인트**: intent capture, policy translation, automation, assurance, remediation의 연결이 답안 핵심이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| IBN 개념 구분 확인 | 의도 입력, 정책 변환, 자동 배포, 검증, 폐루프 | 네트워크 자동화와 동일시 |
| 운영 효과 판단 | telemetry, assurance, drift detection, remediation | 의도 검증 없이 설정 자동화만 서술 |
| 적용 한계 인식 | 모델 품질, 벤더 종속, false positive, 승인 절차 | 완전 자율망으로 과장 |

> 요약: 이 문제는 네트워크 자동화 위에 검증과 수정 루프를 추가하는 IBN 구조와 적용 한계를 묻는다.

---

## Ⅰ. 개요 및 필요성

IBN은 네트워크 목표 상태를 의도로 입력하고 실제 상태와 비교해 운영하는 모델이다. 클라우드·캠퍼스·데이터센터는 정책 수와 장비 수가 증가해 수동 설정 검증이 어렵다. IBN은 정책을 구성으로 변환하고 telemetry로 의도 위반을 탐지해 반복 수정한다.

---

## Ⅱ. 구조 및 구성요소

```text
Business Intent -> Intent Model -> Policy Translation -> Automation Controller
-> Network Device Config -> Telemetry Collection -> Assurance Engine
-> Remediation Workflow
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Intent Model | 사용자 목표를 구조화 | 접근정책, 성능목표, 세그먼트 |
| Policy Translator | 의도를 ACL/QoS/VLAN/VRF로 변환 | 모델 충돌 검출 필요 |
| Automation Controller | 장비 설정 배포 | NETCONF/RESTCONF, API, Ansible |
| Telemetry | 실제 상태 수집 | flow, SNMP, gNMI, syslog |
| Assurance Engine | 의도와 실제 상태 비교 | drift, SLA violation, root cause |

> 요약: IBN은 목표 입력부터 실제 상태 검증까지 이어지는 폐루프 구성요소가 모두 있어야 한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Intent Input -> Validate Policy -> Translate to Config -> Deploy
-> Collect Telemetry -> Compare Desired vs Actual
-> Detect Violation -> Recommend/Execute Remediation
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 의도 입력과 정책 충돌 검사 | duplicate/conflict rule 0건 |
| 2 | 의도를 장비 설정과 API 호출로 변환 | config diff 승인 |
| 3 | staged deployment로 적용 | canary group success 100% |
| 4 | flow, latency, error, route 상태 수집 | telemetry freshness 30초 이하 |
| 5 | 위반 탐지 후 승인 기반 수정 | policy violation MTTR 10분 이하 |

> 요약: IBN은 의도와 실제 상태를 계속 비교하고, 차이가 발생하면 권고 또는 자동 수정으로 폐루프를 완성한다.

---

## Ⅳ. 특징

| 구분 | 전통 운영/자동화 | Intent-Based Networking | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 입력 단위 | CLI 명령, playbook | 비즈니스 의도와 정책 | app to DB TCP 5432 허용 |
| 검증 방식 | 작업 후 수동 확인 | desired vs actual 지속 비교 | violation MTTR 10분 이하 |
| 데이터 | 장비 설정 중심 | telemetry + config + flow | gNMI, NetFlow, syslog |
| 수정 | 장애 후 티켓 처리 | 권고·승인·자동 remediation | false positive 1% 이하 목표 |

> 요약: IBN은 자동 실행보다 의도 검증과 폐루프 수정 능력이 차별점이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 운영 방식 | 장비 중심 자동화 | 의도 중심 폐루프 | 정책 수 1,000개 이상 |
| 검증 | 사후 점검표 | assurance engine | telemetry coverage 95% 이상 |
| 운영/위험 | 사람 승인 중심 | 자동 권고와 승인 결합 | change risk 등급별 자동화 범위 |

> 요약: IBN은 정책 규모와 상태 수집 범위가 충분할 때 적용하고, 고위험 변경은 승인 기반으로 제한한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 의도 오해석 | 추상 정책을 잘못 변환 | intent schema, policy simulation | policy conflict 0건 |
| 자동 수정 사고 | remediation 조건 오류 | human-in-the-loop, blast radius 제한 | auto-change failure 0건 |
| 벤더 종속 | 컨트롤러 전용 모델 | OpenConfig, RESTCONF, export API | portability test pass |

> 요약: IBN 리스크는 의도 모델과 자동 수정 범위에서 발생하므로 시뮬레이션과 승인 체계가 필수이다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 의도 준수율 | policy compliance 99% 이상 | assurance dashboard |
| 상태 수집 범위 | telemetry coverage 95% 이상 | device inventory mapping |
| 복구 시간 | policy violation MTTR 10분 이하 | incident timestamp 분석 |

> 요약: IBN 성과는 설정 수보다 정책 준수율, telemetry 범위, 위반 복구 시간으로 측정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 접근정책, 세그먼트, QoS, SLA를 intent schema로 표준화하고 충돌 검사를 CI gate에 배치함
2. SDN/자동화 컨트롤러가 NETCONF/RESTCONF, Ansible, API로 설정을 배포하고 canary 적용 후 전체 확산함
3. gNMI, NetFlow, syslog, synthetic test로 desired vs actual 차이를 30초~1분 단위로 수집해 승인 기반 remediation을 수행함

**결론 (2줄):**
- 기술사 판단: 정책 규모가 크고 변경 빈도가 높으며 telemetry coverage가 95% 이상이면 IBN 도입 타당성이 있음
- 향후 방향: IBN은 AI 운영 분석과 결합해 의도 충돌 예측, 장애 원인 추정, 자동 복구 승인 흐름으로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | 의도 입력부터 폐루프 검증까지 단계 | 자동화 대비 assurance 차이 |
| 요구사항 명시형 | "방안을 제시하시오", "운영하시오", "설계하시오" | 정책 모델, telemetry, remediation 설계 | false positive, 승인, MTTR 지표 |

> 요약: 설명형은 IBN 구성요소, 운영형은 의도 위반 탐지와 복구 지표 중심으로 전환한다.
