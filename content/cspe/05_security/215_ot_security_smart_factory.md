---
title: "스마트팩토리 OT 보안 (OT Security Smart Factory)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 215
---

# 📖 【암기용】 개념 완전 이해

> 목적: 스마트팩토리 OT 보안을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: PLC, SCADA, HMI, MES가 연결된 생산 현장에서 가용성·안전·품질을 해치지 않도록 사이버 위협을 통제하는 보안 체계
- **왜 필요한가**: 스마트팩토리는 IT와 OT가 연결되어 ERP·MES 침해가 PLC 제어값 변조와 생산중단으로 이어질 수 있다.
- **핵심 직관**: 사무실 네트워크 보안은 문서 유출 방지에 가깝고, OT 보안은 컨베이어 속도와 로봇 동작이 틀어지지 않게 공장 운전을 보호하는 일이다.

## 깊이 이해
- **배경·문제의식**: 기존 공장은 폐쇄망과 전용 프로토콜에 의존했다. 스마트팩토리는 MES, IIoT, 원격정비, 클라우드 분석을 위해 연결성이 늘어 Purdue Model 경계가 흐려진다.
- **작동 원리**: Purdue Level 0~5로 설비·제어·운영·기업망을 분리하고, OT DMZ, allowlist, 단방향 전송, 계정분리, 패치 윈도우를 통해 생산중단 없이 위협을 통제한다.
- **비유**: 병원 수술실 보안과 비슷하다. 문을 잠그는 것만으로 부족하고, 수술 중 장비를 멈추지 않으면서 외부 접근과 변경 이력을 통제해야 한다.
- **구체 예시**: MES 서버가 랜섬웨어에 감염되어 생산지시가 중단되면 PLC는 마지막 recipe로 계속 동작할 수 있으나 품질 lot 추적과 출하가 멈춘다. RTO 4시간, 수동운전 절차가 필요하다.
- **흔한 오해·주의점**: IT 보안 패치를 즉시 적용하는 방식은 OT에 맞지 않는다. PLC firmware 패치는 설비 인증, 라인 정지 시간, 벤더 검증을 거쳐 정해진 patch window에 수행해야 한다.

## 연결 개념
- Purdue Model: OT 네트워크 계층 분리 기준
- IEC 62443: 산업 자동화·제어 시스템 보안 표준
- OT DMZ: IT와 OT 사이의 완충 영역

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 스마트팩토리 보안은 기밀성보다 생산 가용성·안전·품질을 우선하는 운영 통제 문제로 작성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스마트팩토리 OT 보안은 PLC/SCADA/MES를 Purdue Model로 분리하고 IEC 62443 기반으로 접근·변경·탐지를 통제하는 체계이다.
> 2. **가치**: 랜섬웨어, 원격정비 계정 탈취, 제어값 변조가 생산중단·품질불량·안전사고로 이어지는 경로를 차단한다.
> 3. **판단 포인트**: OT는 패치보다 가용성·안전이 우선이므로 DMZ, allowlist, patch window, 수동운전 절차를 함께 판단해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| OT와 IT 보안 차이 확인 | Purdue model, PLC/SCADA/MES, 가용성·안전 우선 | 일반 망분리만 설명 |
| 표준 기반 설계 확인 | IEC 62443 zone/conduit, DMZ, allowlist | ISO 27001 통제만 나열 |
| 운영 리스크 판단 확인 | patch window, 생산중단, 원격정비 통제 | 즉시 패치만 대책으로 제시 |

> 요약: 이 문제는 스마트팩토리의 생산 연속성을 보존하면서 네트워크·계정·변경을 통제하는 설계 역량을 묻는다.

---

## Ⅰ. 개요 및 필요성

스마트팩토리 OT 보안은 생산 제어 시스템의 가용성·안전·무결성을 보호하는 체계이다. IT와 OT가 MES, IIoT, 원격정비로 연결되면서 랜섬웨어와 계정 탈취가 PLC 제어, 품질 lot, 생산계획에 영향을 준다. 생산중단 1시간이 수천만 원 손실로 이어질 수 있어 IEC 62443 기반 구역화와 운영 절차가 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Enterprise IT Level 4/5 -> OT DMZ -> MES Level 3
-> SCADA/HMI Level 2 -> PLC Level 1 -> Sensor/Actuator Level 0
Remote Vendor -> VPN/MFA -> Jump Server -> Allowlist
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| PLC/RTU | 설비 제어 로직 실행 | 실시간성, 변경 제한 |
| SCADA/HMI | 감시·제어 화면과 알람 | 운영자 계정 통제 |
| MES | 생산지시, lot, 품질 데이터 관리 | ERP와 OT 연결점 |
| OT DMZ | IT/OT 데이터 교환 완충 | historian, patch relay |
| 보안 통제 | allowlist, NAC, passive IDS | 생산 영향 최소화 |

> 요약: 스마트팩토리 OT 보안은 Purdue 계층과 OT DMZ를 기준으로 제어망 접근을 최소화한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
자산 식별 -> Purdue zone 분류 -> conduit 정책 수립
-> 계정/MFA/allowlist 적용 -> passive monitoring
-> patch window 계획 -> incident 시 수동운전/복구
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | PLC, HMI, SCADA, MES 자산 목록화 | asset coverage 95% 이상 |
| 2 | IEC 62443 zone/conduit로 통신 경로 분류 | 미승인 경로 0건 |
| 3 | 원격접속은 VPN/MFA/jump server 경유 | direct vendor access 0건 |
| 4 | IDS와 allowlist로 명령·프로토콜 관측 | Modbus write 이벤트 탐지 |
| 5 | patch window와 rollback 절차 수행 | 라인 정지 시간 내 완료 |

> 요약: OT 보안은 자산 식별, 계층 분리, 접근 통제, 수동 모니터링, 계획 정비 순서로 운영된다.

---

## Ⅳ. 특징

| 구분 | IT 보안 | 스마트팩토리 OT 보안 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 우선순위 | 기밀성 중심 | 가용성·안전·품질 중심 | RTO 4시간, 안전정지 절차 |
| 패치 방식 | 정기·긴급 패치 | patch window, 벤더 검증 | 월 1회 또는 정기 정지일 |
| 탐지 방식 | EDR, active scan | passive IDS, allowlist | active scan 금지 구간 |
| 표준 | ISO 27001, NIST CSF | IEC 62443, NIST SP 800-82 | zone/conduit 문서화 |

> 요약: OT 보안은 생산 영향 때문에 passive 관측과 계획 변경을 우선 적용한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단순 망분리 | Purdue+OT DMZ+zone/conduit | MES·원격정비 연결 존재 |
| 비용/성능 | 라인별 개별 관리 | 중앙 관제와 passive sensor | 라인 정지 비용과 탐지 범위 |
| 운영/위험 | 즉시 차단·패치 | 변경승인·patch window | 생산중단 리스크와 CVSS 동시 판단 |

> 요약: 연결형 스마트팩토리는 단순 망분리보다 계층화, DMZ, 운영 절차를 함께 적용해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 생산중단 | 랜섬웨어, MES 장애 | OT DMZ, 백업, 수동운전 | RTO 4시간 이하 |
| 제어값 변조 | PLC write 권한 탈취 | allowlist, RBAC, change approval | unauthorized write 0건 |
| 패치 지연 | 벤더 인증·정지 시간 부족 | risk-based patch window | critical CVE 처리일 |

> 요약: 생산중단, 제어값 변조, 패치 지연을 운영 지표로 관리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 자산 가시성 | OT asset coverage 95% 이상 | passive discovery, CMDB 대조 |
| 통신 통제 | 미승인 conduit 0건 | firewall rule, NetFlow 분석 |
| 복구 역량 | PLC logic backup 월 1회 | restore drill, checksum 검증 |

> 요약: OT 보안 성숙도는 자산 가시성, 통신 경로 통제, 복구 훈련으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Purdue Level 0~5 자산을 식별하고 IEC 62443 zone/conduit 문서화, OT DMZ, historian, jump server를 기준 구조로 설계
2. 원격정비는 VPN, MFA, 세션 녹화, 시간 제한 계정, 승인 기반 allowlist를 적용하고 direct PLC access 0건을 목표로 운영
3. 패치는 CVSS, exploitability, 라인 정지 비용을 반영해 patch window를 정하고 PLC logic backup, rollback, 수동운전 절차를 동시 준비

**결론 (2줄):**
- 기술사 판단: 스마트팩토리 OT 보안은 차단 위주보다 생산 지속과 안전정지를 보장하는 IEC 62443 기반 운영 통제가 적합함
- 향후 방향: IIoT, 디지털 트윈, AI 품질검사 확산에 따라 OT telemetry와 SOC 연계를 표준 운영으로 전환해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "스마트팩토리 OT 보안을 설명하시오" | Purdue 계층, zone/conduit, 운영 흐름 | IT 보안과 OT 보안 차이 |
| 요구사항 명시형 | "보안 대책을 제시하시오", "설계하시오" | DMZ, allowlist, patch window 절차 | 생산중단 리스크와 지표 기반 선택 |

> 요약: 설명형은 구조·표준, 방안형은 생산중단을 줄이는 운영 통제 중심으로 전환한다.
