---
title: "Private LTE 전용망 (Private LTE)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 143
---

# 📖 【암기용】 개념 완전 이해

> 목적: Private LTE를 일반 이동통신망의 축소판이 아니라 기업 전용 무선 인프라로 이해하게 만든다.

## 한눈에
- **개요**: 특정 기업·기관 구역에서 LTE 무선망과 코어망을 전용으로 구축하는 사설 이동통신망
- **왜 필요한가**: 공장, 항만, 발전소, 물류센터는 단말 이동성, 넓은 커버리지, QoS, 폐쇄망 운영이 동시에 필요하다.
- **핵심 직관**: 공용 도로 대신 사업장 내부 전용 도로를 만들어 차량·장비·센서 트래픽을 통제하는 방식이다.

## 깊이 이해
- **배경·문제의식**: Wi-Fi는 구축이 쉬우나 이동 중 핸드오버, 간섭, QoS 통제에서 산업 현장 요구를 모두 만족하기 어렵다.
- **작동 원리**: eNodeB가 단말 무선 접속을 제공하고 EPC가 인증, 이동성, 세션, 정책 제어를 수행한다.
- **비유**: 회사 내부 전화망이 외부 통신망과 분리된 내선 체계를 갖는 것처럼, Private LTE는 현장 무선 단말을 전용 코어로 수용한다.
- **구체 예시**: AGV 200대와 CCTV 500대를 운영하는 물류센터는 eNodeB, EPC, SIM 기반 인증, QoS Class Identifier로 업무별 트래픽을 분리한다.
- **흔한 오해·주의점**: Private LTE는 인터넷 차단만으로 완성되지 않고 주파수, EPC 위치, SIM 발급, 장애 대응 체계가 함께 필요하다.

## 연결 개념
- 5G 특화망 - LTE 전용망의 5G 확장 모델
- EPC - LTE 코어망으로 MME, SGW, PGW, HSS를 포함
- NAC - 유선·무선 단말 접근 통제와 정책 연동 가능

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: Private LTE 답안은 전용망 구성, 인증 흐름, QoS, 운영 지표를 분리해 작성한다.
> 핵심: 출제자는 Wi-Fi와 공중망 대비 Private LTE의 적용 조건과 산업 현장 통제 구조를 확인한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Private LTE는 eNodeB와 EPC를 기업 구역에 전용 구축하여 SIM 기반 인증, 이동성, QoS를 제공하는 사설 LTE망이다.
> 2. **가치**: 산업 단말, AGV, CCTV, 계측 장비를 공용망과 분리하고 업무별 QoS와 폐쇄망 정책을 적용한다.
> 3. **판단 포인트**: 주파수 확보, EPC 배치, SIM 관리, 단말 수, 핸드오버 성공률, 장애 시 우회 경로를 기준으로 설계한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 전용 무선망 구조 이해 확인 | eNodeB, EPC, SIM, APN, QoS Class Identifier | Private LTE를 Wi-Fi 보안 설정으로 오해 |
| 적용 분야 판단 확인 | 공장, 항만, 물류, 발전소, 폐쇄망 | 모든 기업에 일괄 적용한다고 단정 |
| 운영 통제 역량 확인 | 단말 인증, 주파수, SLA, 장애 대응 | 통제 대상과 인증 흐름을 분리하지 않음 |

> 요약: 이 문제는 LTE 기술 설명보다 전용망에서 단말·주파수·QoS·운영 책임을 어떻게 통제하는지 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 기업 구역 전용 LTE 무선망
- 배경: 산업 현장은 이동 단말, 넓은 커버리지, 간섭 통제, 폐쇄망 운용 요구가 동시에 발생함.
- 필요성: AGV, CCTV, 계측 센서, 작업자 단말을 SIM 기반으로 식별하고 업무별 QoS를 적용해야 함.
- 판단 기준: 주파수 사용권, eNodeB 수, EPC 이중화, 단말 인증, 핸드오버 성공률을 기준으로 설계함.

---

## Ⅱ. 구조 및 구성요소

```text
UE / Industrial Device -> eNodeB -> EPC(MME / SGW / PGW / HSS)
                         -> APN / QoS Policy -> Enterprise Network
                         -> NMS / SOC / Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| UE/SIM | 단말 식별과 가입자 인증 | USIM, eSIM, 단말 인증서 연계 가능 |
| eNodeB | LTE 무선 접속과 셀 커버리지 제공 | 셀 설계, 간섭, 핸드오버 품질 관리 |
| EPC | 인증, 이동성, 세션, 정책 제어 | MME, SGW, PGW, HSS 구성 |
| Enterprise Network | 업무 시스템과 폐쇄망 연동 | APN, 방화벽, 라우팅 정책 필요 |

> 요약: Private LTE는 단말-SIM-eNodeB-EPC-업무망을 하나의 전용 정책 도메인으로 묶어 운영한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
단말 전원 on -> 셀 탐색 -> Attach 요청 -> SIM / HSS 인증
-> EPS bearer 생성 -> APN 연결 -> 업무망 트래픽 전달
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 단말이 eNodeB 셀을 탐색하고 RRC 연결을 요청 | RRC setup success |
| 2 | EPC가 SIM과 HSS 정보를 대조해 가입자를 인증 | attach success rate |
| 3 | PGW가 APN과 IP 주소를 할당 | IP allocation failure |
| 4 | QoS 정책이 업무별 bearer에 적용됨 | QCI, packet loss, latency |
| 5 | 단말 이동 시 eNodeB 간 핸드오버 수행 | handover success rate |

> 요약: Private LTE는 SIM 인증 후 bearer와 APN을 생성하고, 이동성과 QoS를 EPC 정책으로 통제한다.

---

## Ⅳ. 특징

| 구분 | Wi-Fi/공중망 | Private LTE | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 인증 | PSK, 802.1X, 공중 가입자 | SIM/HSS 기반 가입자 인증 | USIM, eSIM, HSS |
| 커버리지 | AP 밀도와 간섭 영향 | 셀 설계 기반 광역 커버리지 | eNodeB, 핸드오버 |
| QoS | WLAN QoS 또는 공중망 정책 의존 | QCI와 APN 기반 업무 분리 | QCI, bearer, APN |
| 폐쇄성 | 인터넷·LAN 정책 결합 | 전용 EPC와 업무망 연동 | MME, SGW, PGW |

> 요약: Private LTE는 SIM 인증과 EPC 정책으로 산업 단말을 통제하며, 이동성과 QoS가 필요한 현장에서 Wi-Fi와 선택 기준이 달라진다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Wi-Fi AP + LAN | eNodeB + EPC + SIM | 이동 단말과 넓은 커버리지 요구 시 선택 |
| 비용/성능 | AP 밀집 배치 | 셀 설계와 EPC 구축 | 단말 수, 커버리지 면적, QoS 등급으로 산정 |
| 운영/위험 | IT 네트워크 운영 | 통신망 운영과 주파수 관리 | 주파수·SIM·EPC 운영 책임 확보 시 적용 |

> 요약: Private LTE는 이동성과 폐쇄망 QoS가 핵심 요구인 현장에서 Wi-Fi와 공중망 사이의 전용망 선택지이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 주파수 간섭 | 인접 시스템 또는 현장 구조물 영향 | RF survey, 셀 플래닝, 출력 조정 | SINR, RSRP, RSRQ |
| 인증 장애 | SIM 발급 오류 또는 HSS 정보 불일치 | SIM lifecycle 관리, HSS 동기화 | attach failure cause |
| EPC 장애 | 코어 단일 장애점 | MME/SGW/PGW 이중화, 백업 APN | EPC availability, failover time |

> 요약: 주요 위험은 무선 품질, 가입자 인증, EPC 가용성으로 분리해 설계와 운영 지표를 둔다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 접속 품질 | attach success, RRC success 기준 충족 | EPC log, eNodeB PM counter |
| 이동성 | handover success 기준 충족 | drive test, field KPI |
| 업무 품질 | APN별 지연, 손실, 처리량 기준 충족 | QoS monitoring, packet capture |

> 요약: Private LTE 운영은 접속 성공, 핸드오버, APN별 품질 지표로 전용망 효과를 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 현장 RF survey로 eNodeB 위치, 출력, 커버리지 중첩, 핸드오버 구간을 설계함.
2. EPC는 MME/SGW/PGW/HSS 이중화와 APN별 방화벽 정책을 구성해 업무망 접근을 분리함.
3. SIM 발급, 단말 등록, QoS Class Identifier, 장애 로그를 운영 절차로 표준화함.

**결론 (2줄):**
- 기술사 판단: 이동성·폐쇄망·QoS가 핵심이면 Private LTE를 선택하고, 저밀도 사무 구역이면 Wi-Fi 6/7과 비교 검토함.
- 향후 방향: Private LTE는 5G 특화망, MEC, 산업 IoT 플랫폼과 연계되어 현장 제어망으로 확장됨.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Private LTE를 설명하시오" | Attach, bearer, APN 흐름 | Wi-Fi·공중망 대비 특징 |
| 요구사항 명시형 | "구축 방안을 제시하시오", "비교하시오" | 인증·QoS·핸드오버 검증 흐름 | 주파수, EPC, SIM 운영 리스크 |

> 요약: 설명형은 LTE 전용망 구조를, 구축형은 주파수·EPC·SIM·QoS 운영 기준을 중심으로 작성한다.
