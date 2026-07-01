---
title: "TIME_WAIT 상태 (TIME_WAIT State)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 36
---

# 📖 【암기용】 개념 완전 이해

> 목적: TIME_WAIT가 왜 남는지와 무작정 줄이면 안 되는 이유를 이해하게 만든다. 시험 답안 양식이 아니라, TCP 종료와 2MSL 대기를 직관적으로 잡기 위한 설명이다.

## 한눈에
- **개요**: TIME_WAIT는 TCP 능동 종료자가 마지막 ACK 후 2MSL 동안 연결 식별자를 보존하는 상태
- **왜 필요한가**: 지연된 세그먼트가 새 연결에 섞이는 것을 막고, 마지막 ACK 유실 시 상대의 FIN 재전송에 응답하기 위함.
- **핵심 직관**: 통화를 끊은 뒤에도 상대가 "끊겼나요?"라고 다시 물을 수 있어 일정 시간 회선 기록을 남겨두는 절차임.

## 깊이 이해
- **배경·문제의식**: TCP는 네트워크에 오래 남아 있는 중복 세그먼트를 고려함. 같은 5-tuple이 즉시 재사용되면 이전 연결의 지연 패킷이 새 연결 데이터로 오인될 수 있음.
- **작동 원리**: 4-way handshake에서 마지막 ACK를 보낸 능동 종료자가 TIME_WAIT에 들어감. 2MSL 동안 같은 5-tuple 재사용을 제한하고, 상대 FIN 재전송 시 ACK를 재전송함.
- **비유**: 택배 반품 완료 문자를 보낸 뒤에도 고객센터 재확인 전화가 올 수 있어 접수번호를 일정 시간 보관하는 것임.
- **구체 예시**: 클라이언트가 짧은 HTTP 연결을 초당 수천 개 생성하면 클라이언트 측 TIME_WAIT와 ephemeral port 사용률이 상승함.
- **흔한 오해·주의점**: TIME_WAIT 자체는 오류가 아님. 대량 발생 시 짧은 연결, keepalive 미사용, 클라이언트 포트 고갈을 점검해야 함.

## 연결 개념
- TCP 4-way Handshake: 연결 종료 절차
- 포트 번호·소켓 통신: 5-tuple과 ephemeral port 고갈
- Load Balancer: SNAT 포트 고갈과 connection reuse

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: TIME_WAIT는 제거 대상이 아니라 TCP 안전장치이며, 포트 고갈 문제는 연결 재사용·포트 범위·LB 구조로 대응해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TIME_WAIT는 능동 종료자가 마지막 ACK 후 2MSL 동안 5-tuple을 보존해 지연 세그먼트와 FIN 재전송을 처리하는 TCP 상태이다.
> 2. **가치**: 새 연결과 이전 연결의 세그먼트 혼입을 방지하고, 마지막 ACK 유실 시 상대 FIN에 다시 ACK할 수 있다.
> 3. **판단 포인트**: TIME_WAIT 수, ephemeral port 범위, connection reuse, NAT/SNAT 포트 사용률을 함께 봐야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TCP 종료 상태 이해 확인 | active close, 2MSL, 마지막 ACK, 5-tuple 보존 | TIME_WAIT를 장애로만 설명 |
| 운영 이슈 판단 확인 | port exhaustion, short-lived connection, keepalive | 커널 파라미터 축소만 제시 |
| 구조적 대응 역량 확인 | connection pool, HTTP keepalive, LB SNAT 분산 | `tcp_tw_reuse` 단편 처방 |

> 요약: TIME_WAIT 문제는 TCP 정확성 보장과 대량 짧은 연결 운영의 균형을 묻는 문제임.

---

## Ⅰ. 개요 및 필요성

TIME_WAIT는 TCP 연결 종료 후 남는 대기 상태이다. 능동 종료자는 마지막 ACK 이후 2MSL 동안 5-tuple을 보존한다. 이는 지연 패킷 혼입과 마지막 ACK 유실에 따른 FIN 재전송을 처리하기 위한 TCP 안전장치이다.

---

## Ⅱ. 구조 및 구성요소

```text
Established -> FIN_WAIT_1 -> FIN_WAIT_2 -> TIME_WAIT -> Closed
                       / Last ACK sent
                       / 2MSL timer
                       / 5-tuple protection
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 능동 종료자 | 먼저 FIN을 보낸 측 | 주로 클라이언트 또는 프록시 |
| 2MSL Timer | 지연 세그먼트 소멸 대기 | OS별 기본값 상이 |
| 5-tuple | 연결 식별자 보존 | 같은 조합 즉시 재사용 제한 |
| 마지막 ACK | 상대 FIN에 대한 확인응답 | 유실 시 FIN 재전송에 ACK 재전송 |

> 요약: TIME_WAIT는 마지막 ACK 이후 2MSL 동안 연결 식별자를 보호하는 TCP 종료 상태임.

---

## Ⅲ. 동작원리 및 흐름도

```text
Active Close -> FIN 전송 -> FIN ACK 수신 -> 상대 FIN 수신
-> 마지막 ACK 전송 -> TIME_WAIT 2MSL 대기 -> Closed
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 애플리케이션 close로 FIN 전송 | FIN_WAIT_1 count |
| 2 | 상대 ACK 수신 후 FIN_WAIT_2 진입 | state transition |
| 3 | 상대 FIN 수신 후 마지막 ACK 전송 | packet capture |
| 4 | TIME_WAIT에서 2MSL timer 유지 | TIME_WAIT count |
| 5 | timer 만료 후 socket 자원 해제 | port reuse 가능 |

> 요약: TIME_WAIT는 능동 종료자가 마지막 ACK를 보낸 뒤 지연 세그먼트와 FIN 재전송을 흡수하는 단계임.

---

## Ⅳ. 특징

| 구분 | 일반 종료 | TIME_WAIT 대량 발생 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 상태 목적 | 정확한 종료 | 5-tuple 보존 누적 | 2MSL 대기 |
| 발생 위치 | 능동 종료자 | 클라이언트, 프록시, LB | short-lived TCP |
| 영향 | 정상 자원 보존 | ephemeral port 고갈 가능 | port range 0~65535 |
| 대응 | 기본값 유지 | keepalive, pooling, SNAT 분산 | reuse 전 안전성 검토 |

> 요약: TIME_WAIT는 정상 상태이나 짧은 연결이 많으면 포트와 NAT 자원 고갈로 나타남.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | TIME_WAIT 대응 | 선택 기준 |
|:---|:---|:---|:---|
| 애플리케이션 | 매 요청 새 연결 | keepalive, connection pool | 요청 빈도와 upstream 수 |
| OS 설정 | timer 축소 | port range 확대, reuse 조건 검토 | 지연 패킷 위험 수용 여부 |
| 네트워크 | 단일 SNAT IP | SNAT IP 분산, LB scale-out | NAT port 사용률 70% 초과 |

> 요약: TIME_WAIT 대응은 timer 축소보다 연결 재사용과 포트 자원 확장이 우선임.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 포트 고갈 | 짧은 연결 폭증 | HTTP keepalive, connection pool | `EADDRNOTAVAIL` |
| NAT 고갈 | 단일 SNAT IP 집중 | NAT gateway 확장, IP 분산 | conntrack usage |
| 세그먼트 혼입 | 5-tuple 조기 재사용 | 2MSL 준수, timestamp 확인 | reset, checksum anomaly |

> 요약: TIME_WAIT 리스크는 포트 고갈과 조기 재사용 위험이며, 운영 지표와 TCP 안전성을 함께 봐야 함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| TIME_WAIT 수 | 전체 연결의 추세 기준 관리 | `ss -tan state time-wait` |
| ephemeral port | 사용률 70% 이하 | OS port range, conntrack |
| 재사용 실패 | connect error 0.1% 이하 | application log |

> 요약: TIME_WAIT 관리는 개수 자체보다 포트 사용률과 연결 실패율로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 애플리케이션: HTTP keepalive, DB connection pool, gRPC channel reuse로 짧은 연결 생성을 줄임
2. OS·네트워크: ephemeral port range 확대, NAT/SNAT IP 분산, conntrack table 사용률 70% 이하 유지
3. 장애 분석: `ss`, pcap, LB 로그로 active close 주체를 확인하고 서버·클라이언트 중 조치 위치를 결정

**결론 (2줄):**
- 기술사 판단: TIME_WAIT는 TCP 정확성 상태이므로 삭제보다 연결 재사용·포트 확장·SNAT 분산을 우선함
- 향후 방향: HTTP/2·HTTP/3, connection pooling 확산으로 짧은 TCP 연결 수를 줄이는 구조가 표준 운영 방식이 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TIME_WAIT 상태를 설명하시오" | TCP 4-way 종료와 2MSL 흐름 | active close와 5-tuple 보호 |
| 요구사항 명시형 | "TIME_WAIT 증가 대응 방안을 제시하시오" | active close 주체 진단 | keepalive, port range, NAT 분산 |

> 요약: 설명형은 TCP 상태 전이, 운영형은 포트 고갈 진단과 연결 재사용 대책으로 전환함.
