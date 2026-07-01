---
title: "IDS·IPS — 탐지 vs 차단 (IDS IPS)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 24
---

# 📖 【암기용】 개념 완전 이해

> 목적: IDS와 IPS를 처음 봐도 탐지 장비와 차단 장비의 위치, 동작, 오탐 영향 차이를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: IDS는 공격 징후를 탐지·경보하고, IPS는 트래픽 경로에서 공격 패킷을 차단하는 보안 장비
- **왜 필요한가**: 방화벽이 허용한 `TCP 80/443` 내부에서도 SQL Injection, C2, 취약점 exploit이 발생한다. IDS·IPS는 패턴, 행위, 이상 징후를 분석해 보안 관제와 실시간 차단을 지원한다.
- **핵심 직관**: IDS는 CCTV 관제실, IPS는 출입문 검색대처럼 동작한다. CCTV는 사후 확인에 유리하고, 검색대는 통과 자체를 막을 수 있다.

## 깊이 이해
- **배경·문제의식**: 방화벽은 주로 접근 허용 여부를 판단하지만 허용된 세션의 payload를 충분히 해석하지 못한다. IDS·IPS는 signature, protocol anomaly, behavior rule로 공격 징후를 찾는다.
- **작동 원리**: IDS는 SPAN/TAP으로 복제된 트래픽을 분석하고 event를 SIEM으로 보낸다. IPS는 inline 경로에 배치되어 패킷을 검사한 뒤 allow, drop, reset, rate-limit 같은 action을 수행한다.
- **비유**: IDS는 도로 위반을 촬영해 과태료를 보내는 단속 카메라이고, IPS는 차단봉을 내려 차량 진입을 막는 검문소다.
- **구체 예시**: 웹 서버로 들어오는 `GET /?id=1 OR 1=1` payload가 SQL Injection signature와 매칭되면 IDS는 alert를 생성하고, IPS는 해당 TCP 세션을 reset하거나 패킷을 drop한다.
- **흔한 오해·주의점**: IPS를 inline에 넣으면 모든 공격이 차단되는 것이 아니다. signature 미탐, TLS 암호화, 오탐으로 인한 정상 업무 차단, 처리량 병목을 함께 관리해야 한다.

## 연결 개념
- 방화벽 — 접근 제어와 IDS·IPS 연계 경계 장비
- SIEM·SOAR — IDS 경보 수집, 상관분석, 대응 자동화
- WAF — HTTP 애플리케이션 공격 특화 차단

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: IDS·IPS 답안은 탐지 위치, inline 여부, signature·anomaly 방식, 오탐·미탐 관리, 관제 연계를 명확히 구분한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IDS는 네트워크 공격 징후를 탐지·경보하는 장비이고, IPS는 inline 경로에서 악성 트래픽을 차단하는 장비이다.
> 2. **가치**: 허용된 세션 내부의 exploit, scanning, malware C2를 탐지하고 보안 관제 이벤트로 전환한다.
> 3. **판단 포인트**: IDS는 가시성·관제, IPS는 실시간 차단·오탐 영향, 둘 다 signature update와 TLS 가시성 확보가 필요하다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| IDS와 IPS 차이 확인 | out-of-band 탐지 vs inline 차단 | IDS도 직접 차단한다고 서술 |
| 탐지 방식 이해 확인 | signature, anomaly, behavior, protocol decoding | 시그니처만 쓰고 미탐·오탐 언급 누락 |
| 운영 관제 역량 확인 | SIEM 연계, tuning, false positive 관리 | 차단률만 쓰고 업무 영향 분석 누락 |

> 요약: 이 문제는 탐지와 차단의 위치 차이를 기준으로 오탐·미탐 리스크와 관제 연계를 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: IDS·IPS는 네트워크 트래픽에서 공격 징후를 탐지하거나 차단하는 보안 통제 기술
- 배경: 방화벽이 허용한 업무 포트 내부에서도 exploit과 C2가 발생해 payload·프로토콜·행위 분석이 필요함
- 필요성: IDS는 관제 중심, IPS는 inline 차단 중심으로 운영 목적이 다름

---

## Ⅱ. 구조 및 구성요소

```text
Network Traffic -> Sensor
  / IDS: SPAN/TAP Copy -> Detection -> Alert
  / IPS: Inline Traffic -> Detection -> Drop/Reset
  -> Signature/Rule Engine -> SIEM/SOAR
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Sensor | 트래픽 수집·검사 | TAP, SPAN, inline mode |
| Detection Engine | 공격 징후 판단 | signature, anomaly, behavior |
| Policy Action | 경보 또는 차단 수행 | alert, drop, reset, rate-limit |
| Management Console | 정책·시그니처 관리 | update, tuning, exception |
| SIEM 연계 | 이벤트 상관분석 | EPS, severity, ticket |

> 요약: IDS·IPS는 센서, 탐지 엔진, 정책 action, 관리 콘솔, 관제 연계로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Packet Capture -> Protocol Decode -> Rule Match
  -> Severity Score -> Action Decide
  -> Alert/Drop/Reset -> Log Correlate
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 패킷 또는 flow를 수집하고 프로토콜을 해석 | packet loss, decode error |
| 2 | signature, anomaly, behavior rule과 비교 | rule hit, confidence score |
| 3 | severity와 정책에 따라 alert 또는 drop 결정 | false positive rate |
| 4 | 이벤트를 SIEM으로 전송하고 대응 ticket 생성 | EPS, MTTD, MTTR |

> 요약: IDS·IPS는 패킷 해석, 탐지 규칙 매칭, action 결정, 관제 연계 순서로 동작한다.

---

## Ⅳ. 특징

| 구분 | IDS | IPS | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 배치 위치 | SPAN/TAP, out-of-band | inline bridge 또는 routed path | packet drop 영향 여부 |
| action | alert, log, packet capture | drop, reset, shun, rate-limit | TCP RST, block duration |
| 장점 | 업무 트래픽 영향 제한 | 공격 패킷 실시간 차단 | MTTD, block count |
| 한계 | 탐지 후 대응 지연 | 오탐 시 업무 차단 | false positive, bypass mode |

> 요약: IDS는 관제 가시성, IPS는 inline 차단 능력이 중심이며 오탐 영향 범위가 다르다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | IDS | IPS | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 복제 트래픽 분석 | 실경로 트래픽 검사 | 업무 영향 허용도와 차단 필요성 |
| 비용/성능 | packet loss와 저장 용량 관리 | latency와 throughput 용량 필요 | 링크 10Gbps, p95 latency 목표 |
| 운영/위험 | 경보 과다, 미대응 | 오탐 차단, fail-close 위험 | false positive와 bypass 정책 |

> 요약: 탐지 우선 구간은 IDS, 공격 차단이 필요한 인터넷 경계·DMZ는 IPS를 우선 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 차단 | signature 범위 과대 | IPS alert-only 검증 후 block 전환 | false positive rate |
| 미탐 | 암호화 트래픽, signature 미갱신 | TLS inspection, rule update | missed incident count |
| 경보 폭주 | scan, noisy rule | severity tuning, suppression | alert EPS, analyst backlog |

> 요약: IDS·IPS 운영 리스크는 오탐, 미탐, 경보 폭주이며 tuning과 가시성 확보가 핵심 통제이다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 탐지 품질 | high severity alert 정탐률 목표 준수 | 샘플링 분석, incident review |
| 처리 용량 | packet loss 0건, 장비 CPU 70% 이하 | sensor metric, interface counter |
| 대응 시간 | MTTD 10분 이하, MTTR 목표 준수 | SIEM ticket, SOAR log |

> 요약: IDS·IPS 성과는 정탐률, packet loss, MTTD·MTTR로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 인터넷 경계는 IPS inline, 내부 east-west traffic은 IDS/TAP 기반으로 배치해 차단과 가시성을 분리함
2. 신규 signature는 7일간 alert-only로 정탐·오탐을 검증한 뒤 high confidence rule만 block action으로 전환함
3. IDS·IPS 이벤트를 SIEM, EDR, 방화벽 로그와 correlation하고 MTTD, MTTR, false positive rate를 월 단위로 점검함

**결론 (2줄):**
- 기술사 판단: 업무 영향이 큰 구간은 IDS 관제, 외부 공격면과 DMZ는 IPS 차단을 적용함
- 향후 방향: 암호화 트래픽 증가에 따라 TLS inspection 범위, NDR, EDR telemetry를 결합한 탐지 체계가 필요함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "IDS와 IPS를 설명하시오" | 탐지 엔진, action 흐름 | IDS·IPS 배치와 action 차이 |
| 요구사항 명시형 | "침입 차단 방안을 제시하시오" | inline 배치, tuning, SIEM 연계 | 오탐·미탐 리스크 대응 |

> 요약: 설명형은 탐지·차단 차이, 방안형은 배치와 운영 지표 중심으로 답안을 전환한다.
