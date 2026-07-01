---
title: "IDS·IPS 탐지 vs 차단 (IDS IPS)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 33
---

# 📖 【암기용】 개념 완전 이해

> 목적: IDS와 IPS의 차이를 배치 방식과 대응 동작 기준으로 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: IDS는 침입 의심 행위를 탐지·경보하고, IPS는 inline 위치에서 탐지 후 패킷을 차단한다.
- **왜 필요한가**: 방화벽이 허용한 포트 안에서도 취약점 공격, 스캔, C2 통신이 발생한다. IDS/IPS는 허용 트래픽의 위협 패턴을 분석한다.
- **핵심 직관**: IDS는 CCTV 관제센터, IPS는 자동 차단 기능이 있는 출입 게이트와 같다.

## 깊이 이해
- **배경·문제의식**: 방화벽 정책은 포트와 세션 허용 여부를 판단하지만, 허용된 웹·DB 트래픽 내부의 공격 행위를 모두 판별하지 못한다. IDS/IPS는 서명과 이상 행위 기준으로 침입 징후를 찾는다.
- **작동 원리**: IDS는 TAP/SPAN으로 복제 트래픽을 받아 경보를 생성한다. IPS는 inline으로 트래픽 경로에 놓여 악성 패킷을 drop, reset, rate limit 처리한다. 둘 다 signature, anomaly, protocol validation을 사용함.
- **비유**: IDS는 범죄 장면을 발견해 신고하는 관제요원이고, IPS는 위험 출입을 즉시 막는 자동문이다. 즉시 차단은 업무 중단 리스크를 함께 가진다.
- **구체 예시**: `CVE-2021-44228` Log4Shell 패턴이 탐지되면 IDS는 SIEM 알림을 만들고, IPS는 해당 HTTP 요청을 drop하거나 TCP reset을 전송함.
- **흔한 오해·주의점**: IPS가 항상 IDS보다 우월한 것은 아님. 오탐이 3%만 되어도 결제·로그인 트래픽 차단 사고가 발생할 수 있어 탐지 모드 검증 후 차단 모드 전환이 필요함.

## 연결 개념
- 방화벽: 접근 허용 이후 트래픽을 IDS/IPS가 심층 검사
- 침입 탐지: signature와 anomaly 방식의 기반 개념
- SIEM/SOAR: IDS/IPS 이벤트를 사고 대응 절차로 연결

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: IDS/IPS는 제품 명칭이 아니라 out-of-band와 inline, 탐지와 차단, 오탐과 미탐의 균형으로 답해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IDS/IPS는 네트워크 트래픽에서 침입 징후를 탐지하고, IPS는 inline 차단까지 수행하는 보안 통제 시스템이다.
> 2. **가치**: 방화벽이 허용한 통신 내부의 취약점 공격, 스캔, C2, 정책 위반을 signature·anomaly 기반으로 식별한다.
> 3. **판단 포인트**: IDS는 가시성, IPS는 실시간 차단을 제공하므로 업무 영향도와 오탐율 기준으로 배치해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 탐지와 차단 차이 확인 | IDS=out-of-band alert, IPS=inline block | IDS와 IPS를 동일 장비명으로 처리 |
| 탐지 방식 이해 확인 | signature, anomaly, protocol validation | 시그니처만 쓰고 미탐·오탐을 누락 |
| 운영 판단 확인 | 탐지 모드 검증, 차단 룰 승격, SIEM 연계 | IPS 차단만 강조하고 업무 중단 리스크 누락 |

> 요약: IDS/IPS 문제는 배치 방식과 오탐·미탐 통제 기준을 함께 평가함.

---

## Ⅰ. 개요 및 필요성

- 개요: 침입 징후 탐지와 inline 차단 체계
- 배경: 방화벽이 허용한 웹·DB 트래픽 안에서도 취약점 공격, 스캔, C2 통신이 발생할 수 있음.
- 필요성: IDS/IPS는 탐지 모드 2주 검증, 오탐률 3% 이하, SIEM 상관분석 기준으로 차단 룰 승격 여부를 판단해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Network TAP/SPAN -> IDS Sensor -> Alert -> SIEM/SOAR
Client -> IPS Inline Sensor -> Rule Engine -> Allow/Drop/Reset -> Server
Threat Intel -> Signature Update -> Policy Tuning
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Sensor | 패킷 수집·세션 재조립 | TAP/SPAN 또는 inline 배치 |
| Detection Engine | signature, anomaly, protocol validation 수행 | CVE·MITRE ATT&CK 매핑 |
| Response Module | alert, drop, reset, quarantine 처리 | IPS는 지연시간과 가용성 고려 |
| Management/SIEM | 룰 배포, 이벤트 상관분석 | 티켓, SOAR playbook 연계 |

> 요약: IDS/IPS는 센서, 탐지 엔진, 대응 모듈, 관리·로그 체계로 구성됨.

---

## Ⅲ. 동작원리 및 흐름도

```text
Packet Capture -> Session Reassembly -> Rule/Anomaly 검사
-> Severity 산정 -> IDS Alert / IPS Drop·Reset -> SIEM Ticket
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 패킷 캡처와 세션 재조립 | packet loss 0.1% 이하 |
| 2 | 시그니처·행위 기준 매칭 | CVE, Snort/Suricata rule, threshold |
| 3 | 심각도와 자산 중요도 산정 | CVSS, asset criticality |
| 4 | 경보 또는 차단 수행 | false positive 3% 이하, block 성공률 |

> 요약: IDS/IPS는 패킷을 세션 단위로 재구성한 뒤 탐지 기준과 자산 중요도를 결합해 대응함.

---

## Ⅳ. 특징

| 구분 | IDS | IPS | 판단 포인트 |
|:---|:---|:---|:---|
| 배치 | TAP/SPAN out-of-band | inline in-path | IPS 장애 시 bypass 설계 필요 |
| 동작 | alert, log | drop, reset, rate limit | 차단 전 탐지 모드 검증 2주 이상 |
| 장점 | 업무 영향 없이 가시성 확보 | 공격 패킷 즉시 차단 | 고위험 룰부터 단계 적용 |
| 한계 | 사후 대응 | 오탐 시 서비스 중단 | false positive와 business impact 측정 |

> 요약: IDS는 관측, IPS는 차단이 핵심이며 inline 배치가 운영 리스크를 결정함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 방화벽 로그 중심 | IDS/IPS 심층 탐지 | 허용 포트 내부 공격 탐지 필요 시 적용 |
| 비용/성능 | TAP 기반 IDS | inline IPS | 업무 p95 지연 20ms 이하, HA bypass 필요 |
| 운영/위험 | 경보만 생성 | 경보·차단·격리 | 오탐율 3% 이하 검증 후 차단 승격 |

> 요약: IDS/IPS 적용은 차단 효과보다 업무 지연, 우회 구성, 오탐 통제 기준으로 판단해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 차단 | 룰 민감도 과다, 정상 패턴 미학습 | 탐지 모드 2주, 예외 승인, 단계적 block | false positive 3% 이하 |
| 미탐 | 신규 공격, 암호화 트래픽 | Threat Intel, TLS inspection, EDR 연계 | missed detection case 월 0건 목표 |
| 패킷 손실 | 센서 용량 초과 | 40Gbps 이상 NIC, flow sampling 기준 | packet drop 0.1% 이하 |

> 요약: 운영 리스크는 오탐, 미탐, 패킷 손실이며 탐지 모드 검증과 용량 지표로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 탐지 품질 | 탐지율 95% 이상, 오탐율 3% 이하 | 모의공격, purple team |
| 차단 영향 | p95 추가 지연 20ms 이하 | APM, packet broker |
| 대응 연계 | critical alert 5분 이내 티켓 생성 | SIEM/SOAR 로그 |

> 요약: IDS/IPS 성과는 탐지 품질, 지연시간, 사고 대응 자동화 시간으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 배치 전략: 인터넷 경계는 IPS inline HA, 내부 lateral movement 관측은 IDS TAP/SPAN으로 분리
2. 룰 운영: high severity CVE 룰은 즉시 탐지, 2주 오탐 검증 후 차단 승격, 업무 예외는 만료일 필수
3. 로그 연계: IDS/IPS alert를 SIEM에서 방화벽, EDR, IAM 로그와 묶고 critical 사건은 SOAR 티켓 5분 이내 생성

**결론 (2줄):**
- 기술사 판단: 업무 중단 비용이 큰 구간은 IDS 우선, 인터넷 경계 고위험 공격은 IPS inline 차단을 선택함
- 향후 방향: 암호화 트래픽 증가에 따라 TLS 복호화 범위와 프라이버시 예외를 정책으로 분리한 IDS/IPS 운영이 필요함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "IDS와 IPS를 설명하시오" | 패킷 수집, 탐지 엔진, 경보·차단 흐름 | out-of-band와 inline, 오탐·미탐 차이 |
| 요구사항 명시형 | "비교하시오", "운영 방안을 제시하시오", "설계하시오" | 탐지 모드에서 차단 모드로 승격 절차 | false positive, p95 지연, bypass 기준 |

> 요약: 설명형은 탐지 원리, 비교·운영형은 배치 방식과 오탐 통제 지표를 중심으로 작성함.
