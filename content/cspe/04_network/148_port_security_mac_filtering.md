---
title: "포트 보안 - MAC Filtering (Port Security MAC Filtering)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 148
---

# 📖 【암기용】 개념 완전 이해

> 목적: 포트 보안과 MAC Filtering을 스위치 설정 옵션이 아니라 접속 포트에서 허용 단말을 제한하는 2계층 통제로 이해하게 만든다.

## 한눈에
- **개요**: 스위치 포트에서 허용 MAC 주소와 개수를 제한해 미승인 단말 접속을 통제하는 방식
- **왜 필요한가**: 회의실, 공장, 사무실 벽면 포트에 임의 장비를 연결하면 내부망에 바로 접근할 수 있다.
- **핵심 직관**: 특정 주차 구역에 등록 차량 번호만 들어오게 하고, 등록되지 않은 차량은 차단하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 유선 포트는 물리 접근만 가능하면 네트워크 접속이 가능하므로, 공용 공간 포트와 미사용 포트가 내부망 진입점이 될 수 있다.
- **작동 원리**: 스위치가 포트별 허용 MAC 주소, 최대 MAC 수, 위반 시 동작(shutdown, restrict, protect)을 설정해 프레임을 제어한다.
- **비유**: 출입문에 등록된 카드 1개만 허용하고 다른 카드는 경보 또는 차단하는 출입 통제와 유사하다.
- **구체 예시**: 사무실 프린터 포트에 sticky MAC을 설정하고 최대 MAC 수를 1로 제한하면 다른 노트북 연결 시 violation 로그가 발생한다.
- **흔한 오해·주의점**: MAC 주소는 위조 가능하므로 포트 보안은 NAC/802.1X 보완책이지 사용자 신원 인증을 대체하지 않는다.

## 연결 개념
- NAC - 포트 보안을 신원·상태 기반 접근 제어로 확장
- 802.1X - MAC 주소 대신 인증서 또는 계정으로 접속 인증
- DHCP Snooping - MAC/IP 바인딩과 연계해 2계층 통제 보완

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 포트 보안 답안은 통제 대상, 위반 동작, 운영 한계, NAC 연계를 분리해 작성한다.
> 핵심: 출제자는 MAC Filtering을 단독 보안 대책으로 쓰지 않고 계층형 접속 통제의 위치를 설명하는지 확인한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 포트 보안은 스위치 포트별 허용 MAC 주소와 개수를 제한해 미승인 2계층 접속을 제어하는 기능이다.
> 2. **가치**: 미사용 포트, 프린터 포트, 회의실 포트에서 임의 단말 연결과 허브 연결을 탐지·차단한다.
> 3. **판단 포인트**: MAC 위조 가능성, 운영 예외, violation 모드, 802.1X/NAC 병행 여부를 함께 판단해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| L2 접속 통제 이해 확인 | MAC filtering, sticky MAC, maximum MAC, violation mode | MAC Filtering을 사용자 인증으로 설명 |
| 운영 한계 판단 확인 | MAC spoofing, 단말 교체, 예외 처리 | 단독 대책으로 내부망 보호가 완결된다고 단정 |
| 보완 대책 제시 확인 | 802.1X, NAC, DHCP Snooping, 로그 모니터링 | 위반 로그와 운영 지표 누락 |

> 요약: 포트 보안 문제는 MAC 기반 통제의 적용 위치와 한계를 쓰고 NAC/802.1X와 연계하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 스위치 포트별 MAC 접속 제한
- 배경: 벽면 포트와 장비 포트에 미승인 단말이 연결되면 내부 VLAN으로 직접 진입할 수 있음.
- 필요성: 허용 MAC 수, sticky MAC, violation mode를 사용해 임의 단말 연결과 소형 허브 연결을 통제해야 함.
- 판단 기준: 포트 용도, 허용 MAC 수, 위반 로그, 단말 교체 절차, 802.1X 적용 가능성을 기준으로 설계함.

---

## Ⅱ. 구조 및 구성요소

```text
Endpoint MAC -> Switch Port -> Port Security Table
              -> Allowed MAC / Max Count Check
              -> Permit / Protect / Restrict / Shutdown
              -> Syslog / SNMP Trap / NAC Alert
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Switch Port | 프레임 수신과 MAC 학습 수행 | access port 중심 적용 |
| Allowed MAC Table | 허용 MAC 주소와 최대 개수 저장 | static 또는 sticky MAC |
| Violation Mode | 위반 시 처리 방식 결정 | protect, restrict, shutdown |
| Monitoring | 위반 이벤트 기록과 알림 | syslog, SNMP trap, SIEM |

> 요약: 포트 보안은 포트에서 학습된 MAC을 허용 목록과 비교하고 위반 시 정책 모드에 따라 차단·알림을 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
프레임 수신 -> Source MAC 확인 -> 허용 MAC / 최대 개수 비교
-> 정상 프레임 전달 / 위반 프레임 처리 -> 로그 기록 -> 운영자 조치
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 스위치 포트가 프레임의 Source MAC을 확인 | learned MAC count |
| 2 | 허용 MAC 주소 또는 sticky MAC 목록과 비교 | secure MAC match |
| 3 | 최대 MAC 수 초과 여부를 판단 | maximum violation count |
| 4 | violation mode에 따라 protect, restrict, shutdown 수행 | violation action log |
| 5 | 운영자가 단말 교체 또는 침해 여부를 확인 | ticket, SIEM alert |

> 요약: MAC Filtering은 Source MAC과 포트 정책을 비교해 위반 프레임을 처리하고 로그로 운영 판단을 지원한다.

---

## Ⅳ. 특징

| 구분 | 미적용 포트 | Port Security MAC Filtering | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 통제 대상 | 모든 연결 단말 | 허용 MAC과 최대 MAC 수 | max 1~N 설정 |
| 위반 처리 | 정상 forwarding | protect, restrict, shutdown | violation mode |
| 운영 방식 | 장애 후 발견 | syslog, SNMP trap, SIEM 알림 | violation count |
| 한계 | 임의 단말 접속 가능 | MAC spoofing에 취약 | 802.1X/NAC 병행 필요 |

> 요약: 포트 보안은 물리 포트 남용을 줄이는 2계층 통제이나 신원 기반 인증은 802.1X와 NAC로 보완해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 포트 미통제 | 허용 MAC 기반 통제 | 프린터, CCTV, 고정 장비 포트에 적합 |
| 비용/성능 | 별도 인증 서버 불필요 | 스위치 설정과 운영 절차 필요 | 단말 이동성이 낮은 구간부터 적용 |
| 운영/위험 | 미승인 단말 탐지 지연 | MAC 위반 즉시 탐지 | MAC 위조와 단말 교체 예외 절차 필요 |

> 요약: 포트 보안은 고정 단말 포트에서 효과가 크고, 사용자 이동 단말에는 802.1X가 더 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오차단 | 단말 NIC 교체 또는 도킹스테이션 사용 | 변경 승인 절차, sticky MAC 갱신 | false violation count |
| MAC 위조 | 공격자가 허용 MAC을 복제 | 802.1X, DHCP Snooping, DAI 병행 | duplicate MAC alert |
| 운영 누락 | 위반 로그 미수집 | syslog/SIEM 연동, 주기 점검 | violation log coverage |

> 요약: 포트 보안 운영은 오차단, MAC 위조, 로그 누락을 보완 통제와 운영 절차로 관리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정책 적용 | 보안 대상 포트 설정률 관리 | switch config audit |
| 위반 탐지 | violation count와 조치 이력 추적 | syslog, SNMP trap |
| 보완 통제 | 802.1X, DHCP Snooping 적용 구간 확인 | NAC report, switch feature audit |

> 요약: 포트 보안의 성공 여부는 설정률, 위반 조치, 보완 통제 적용 여부로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 프린터, CCTV, 출입통제 장비 포트는 최대 MAC 수 1과 sticky MAC을 적용하고 violation mode를 restrict 또는 shutdown으로 설정함.
2. 사용자 포트는 802.1X 우선 적용 후 예외 단말에만 MAC Filtering을 보완적으로 적용함.
3. violation 로그를 SIEM으로 수집하고 단말 교체, 오차단, 침해 의심 이벤트를 티켓으로 추적함.

**결론 (2줄):**
- 기술사 판단: 고정 단말 포트에는 Port Security를 적용하고, 사용자 신원 확인이 필요한 구간은 802.1X/NAC를 기본 통제로 선택함.
- 향후 방향: 포트 보안은 DHCP Snooping, Dynamic ARP Inspection, NAC와 결합된 L2 접근 통제의 보조 수단으로 유지됨.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "포트 보안을 설명하시오" | MAC 학습과 violation 처리 흐름 | sticky MAC, maximum, violation mode |
| 요구사항 명시형 | "내부망 접속 통제 방안을 제시하시오" | 위반 탐지와 조치 흐름 | 802.1X/NAC 대비 한계와 보완책 |

> 요약: 설명형은 L2 기능 동작을, 방안형은 적용 대상과 보완 통제를 중심으로 목차를 전환한다.
