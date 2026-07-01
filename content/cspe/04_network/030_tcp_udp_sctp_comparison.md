---
title: "TCP vs UDP vs SCTP 비교 (TCP UDP SCTP Comparison)"
date: "2026-07-02"
tags:
  - "cspe-network"
weight: 30
---

# 📖 【암기용】 개념 완전 이해

> 목적: 전송 계층 프로토콜 3대장의 차이점과 진화 배경을 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 애플리케이션 데이터를 목적지까지 전송하는 방식을 결정하는 4계층 프로토콜. 신뢰성의 TCP, 속도의 UDP, 두 장점을 결합한 차세대 SCTP
- **왜 필요한가**: 통신 특성(신뢰 최우선 vs 속도 최우선 vs 다중 경로 확보)이 애플리케이션마다 다르므로 획일적인 전송 방식으로는 요구를 맞출 수 없음
- **핵심 직관**: TCP는 수령 확인 서명을 받는 '등기 우편', UDP는 답장을 기대 안 하는 '일반 우편 엽서', SCTP는 여러 배송 경로를 통해 묶음 상품 중 하나가 분실되어도 나머지는 정상 배송하는 '프리미엄 멀티 채널 택배'다.

## 깊이 이해
- **배경·문제의식**: 인터넷은 신뢰성 있는 TCP와 빠른 UDP로 양분되어 왔다. 하지만 통신 장비(이동통신망, SIGTRAN)가 IP망으로 넘어오면서, TCP의 "하나 잃어버리면 전부 대기(Head-of-Line Blocking)" 문제와 "랜선 하나 끊기면 연결 죽음(단일 호밍)" 문제가 발목을 잡았다. 이를 극복하고자 SCTP가 등장했다.
- **작동 원리**:
  - **TCP (Transmission Control Protocol)**: 1:1 연결 지향. 바이트 스트림 방식이라 경계가 없고, 패킷 순서를 엄격히 맞추며, 하나라도 유실되면 뒤 패킷은 기다려야 함.
  - **UDP (User Datagram Protocol)**: 비연결 지향. 독립된 데이터그램 단위로 쏘고 잊음. 순서나 유실을 보장하지 않아 빠름.
  - **SCTP (Stream Control Transmission Protocol)**: 연결 지향적(TCP처럼 신뢰성 보장)이되 메세지(UDP처럼 경계 존재) 지향. 여러 개의 스트림을 독립적으로 전송(Multi-streaming)해 한 스트림 유실이 다른 스트림을 막지 않으며, 여러 IP를 묶어(Multi-homing) 한 망이 끊겨도 연결을 유지함.
- **비유**: TCP는 1줄 서기로 1번 손님 계산이 늦어지면 뒷사람 다 멈춤(HOLB). UDP는 줄 안 서고 알아서 들어감. SCTP는 계산대 4개를 열고(Multi-streaming), 입구도 2개(Multi-homing) 뚫어놓은 구조.
- **구체 예시**: 웹/파일(HTTP, FTP)은 무결성이 중요해 TCP. 실시간 영상(WebRTC)이나 DNS는 지연 회피가 중요해 UDP. 통신사망(5G 코어 시그널링)이나 망 무중단이 필수인 금융 시스템은 SCTP를 쓴다.
- **흔한 오해·주의점**: "SCTP가 완벽하니까 웹 브라우저도 다 이걸로 바꿔야 한다"는 것은 비현실적이다. 전 세계 수많은 방화벽과 NAT 장비가 L4 헤더로 TCP/UDP만 인식하도록 하드웨어 파싱되어 있어, SCTP 패킷을 보면 그냥 버린다(Middlebox 문제). 이 때문에 구글은 아예 UDP 위에서 동작하는 QUIC을 만들었다.

## 연결 개념
- HOLB (Head-of-Line Blocking) — 앞선 패킷 유실 시 뒤 패킷이 멀쩡히 도착해도 대기해야 하는 TCP의 치명적 단점
- Multi-Homing — 단말이 여러 IP 주소를 가져 물리적 회선 장애 시에도 즉각(Failover) 우회하는 SCTP 특성
- QUIC — SCTP의 장점(멀티스트리밍)을 흡수하되 방화벽을 통과하기 위해 UDP 기반으로 설계된 HTTP/3 핵심 프로토콜

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TCP는 신뢰성(바이트 스트림), UDP는 신속성(데이터그램), SCTP는 두 장점을 융합한 차세대 멀티 채널(메시지 지향) 전송 계층 프로토콜이다.
> 2. **가치**: SCTP는 Multi-Homing으로 망 장애에 대한 생존성을 높이고, Multi-Streaming으로 TCP의 HOLB(Head-of-Line Blocking) 병목을 제거하여 무중단 고속 통신을 실현한다.
> 3. **판단 포인트**: 프로토콜 선택은 '지연(Latency)'과 '무결성(Integrity)'의 트레이드오프이며, SCTP의 방화벽 통과(Middlebox) 한계로 인해 최근 퍼블릭 망은 UDP 기반의 QUIC으로 수렴 중이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| L4 프로토콜 동작 원리 분별력 확인 | 바이트 스트림(TCP) vs 데이터그램(UDP) vs 메시지(SCTP) 전송 차이 | TCP, UDP만 비교하고 SCTP는 누락 또는 명칭만 기재 |
| TCP 한계 및 SCTP 극복 기법 이해 | HOLB 해결(Multi-streaming), 네트워크 단절 해결(Multi-homing) | SCTP를 단순한 TCP 업그레이드로 치부 |
| 최신 인터넷 프로토콜 트렌드 인지 | 미들박스(NAT/FW) 문제와 QUIC(HTTP/3) 프로토콜로의 진화 | 폐쇄망(SCTP)과 퍼블릭망(QUIC)의 적용 분리 판단 누락 |

> 요약: TCP/UDP 비교라는 기본 논점에 SCTP의 "Multi-homing", "Multi-streaming"이라는 2가지 키워드를 핵심 대조 축으로 올려야 득점한다.

---

## Ⅰ. 개요 및 필요성

- 정의: 애플리케이션의 요구(신뢰성, 속도, 다중 경로 등)에 맞춰 종단 간(End-to-End) 데이터 전송 방식을 제공하는 L4 규약
- 배경: TCP의 회선 단절 취약성(단일 경로)과 패킷 유실 시 대기 병목(HOLB)으로 인하여 무중단 고속 병렬 처리 한계 노출
- 필요성: 모바일/클라우드 환경의 잦은 IP 변경 및 5G 코어망 등 미션 크리티컬 환경의 99.999% 생존성 확보를 위해 다중 채널(SCTP) 필수

---

## Ⅱ. 구조 및 구성요소 (SCTP 아키텍처)

```text
[SCTP Association 구조]
IP A1 (Primary)   ----\               /---- IP B1 (Primary)
                       SCTP Association (Multi-homing)
IP A2 (Secondary) ----/               \---- IP B2 (Secondary)
  -> 내부적으로 Stream 1, Stream 2, Stream 3 병렬 큐 (Multi-streaming)
```

| 기능 요소 | SCTP 핵심 동작 | 해결하는 TCP의 한계점 |
|:---|:---|:---|
| Multi-Homing | 송수신 단말 간 다중 IP 주소 바인딩으로 경로 이중화 | 단일 회선 장애 시 TCP 세션 끊김 (SPOF) 방지 |
| Multi-Streaming | 단일 연관(Association) 내에 다수의 독립적 스트림 구성 | 1개 패킷 유실 시 전체 전송 멈춤 (HOLB) 극복 |
| 4-way Handshake | 초기 연결 시 쿠키(Cookie) 기반 상태 정보 교환 | SYN Flood (서버 리소스 선점) 보안 취약점 해결 |
| Message-Oriented | 애플리케이션 데이터 경계(Boundary) 보존 | 바이트 스트림 분리 파싱을 위한 앱 계층 오버헤드 |

> 요약: SCTP는 "세션과 IP의 분리(Multi-homing)"와 "전송과 흐름의 분리(Multi-streaming)"를 아키텍처 레벨에서 구현한 진보적 프로토콜이다.

---

## Ⅲ. 동작원리 및 흐름도 (흐름 제어 방식)

```text
TCP: Data A 유실 -> Data B 대기 -> Data C 대기 (직렬 병목, HOLB 발생)
SCTP: Stream 1 (Data A 유실 -> 대기) | Stream 2 (Data B 도착 -> 앱 전달) | Stream 3 (Data C 도착 -> 앱 전달)
```

| 단계 | 비교 대상 | 동작 특성 및 검증 기준 |
|:---:|:---|:---|
| 1 | TCP 전송 | 패킷 순서 보장 및 1개 유실 시 후속 패킷 커널 버퍼 큐 대기 강제 (HOLB) |
| 2 | UDP 전송 | 순서 상관없이 독립적 큐잉, 도착 즉시 애플리케이션으로 올려 보냄 (신뢰성 없음) |
| 3 | SCTP 병렬 전송 | 스트림 간 독립 큐 운영, 1번 스트림 유실되어도 2번 스트림은 정상 앱 처리 |
| 4 | 장애 우회 (Failover)| TCP는 타임아웃 및 세션 재시작, SCTP는 즉시 Secondary IP로 무중단 경로 우회 |

> 요약: SCTP는 TCP처럼 패킷 도달을 보장(신뢰성)하면서도, 스트림을 여러 갈래로 쪼개어 UDP와 같은 실시간 병렬 처리 이점을 취한다.

---

## Ⅳ. 특징 (3대 프로토콜 총괄 비교)

| 비교 축 | TCP | UDP | SCTP |
|:---|:---|:---|:---|
| 전송 단위 | Byte-Stream (경계 없음) | Datagram (경계 유지) | Message (경계 유지) |
| 연결 방식 | 1:1 연결형 (Single IP) | 비연결형 | 연결형 (Multi-Homing, 다중 IP) |
| 병목 한계 | Head-of-Line Blocking 발생 | 병목 없음 | Multi-Streaming으로 HOLB 제거 |
| 보안성 제어 | SYN Flood 구조적 취약 | 인증 과정 없음 | Cookie 기반 4-way로 방어 설계 |
| 주요 적용 | HTTP, FTP, Email | DNS, VoIP, WebRTC | SIGTRAN(이동통신), Diameter(5G 코어) |

> 요약: 범용성은 TCP가, 속도는 UDP가 우위이나, 통신사 인프라처럼 한 치의 끊김도 허용 안 되는 폐쇄망 환경에서는 SCTP가 표준이다.

---

## Ⅴ. 심화 비교 및 적용 판단 (SCTP의 퍼블릭망 한계)

| 이슈 축 | SCTP의 미들박스(Middlebox) 문제 | QUIC 프로토콜의 대안 적용 | 판단 기준 |
|:---|:---|:---|:---|
| 방화벽/NAT | 기존 인터넷 NAT/FW는 프로토콜 번호 6(TCP), 17(UDP)만 식별, 132(SCTP)는 Drop 처리 | 기존 통과가 보장된 UDP 위에서 동작하도록 페이로드 내에 제어 헤더 구현 | 퍼블릭 인터넷(Public 망) 호환성 여부 |
| OS 커널 | SCTP 지원을 위해 양 종단 커널 수정 필요 | User-space(애플리케이션 계층) 내 구현으로 커널 패치 불필요 | 신기술 배포 및 업데이트 속도 |
| 결론 | 5G 핵심망 등 폐쇄적인 사설망에만 제한적 적용 | 웹(HTTP/3) 등 대고객 퍼블릭 서비스의 차세대 표준으로 등극 | 서비스 대상 통제 가능 여부 |

> 요약: SCTP는 기술적으로 가장 완벽하나, 이미 TCP/UDP로 굳어진 레거시 인터넷 인프라(미들박스)를 뚫지 못해 QUIC에게 범용 표준의 자리를 내주었다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| TCP HOLB 지연 | 1 패킷 유실이 윈도우 전체 처리 지연 | HTTP/2 환경 시 다중화 한계, HTTP/3(QUIC) 전환 | TCP 재전송률 대비 앱 응답 지연(RTT) 델타 |
| UDP 증폭 공격 | Source IP 위조 가능, 상태 유지 부재 | L4 방화벽 UDP 포트 화이트리스트 차단, Rate Limit | DNS/NTP 트래픽 비정상 In/Out 비율 |
| 망 전환 단절 | Mobile 기기 Wi-Fi <-> LTE IP 전환 시 TCP 단절 | Multi-path TCP(MPTCP) 적용 또는 QUIC 연결 식별자(CID) 사용 | 세션 유지(Session Persistence)율 |

> 요약: 현대 트래픽의 핵심 과제인 '무중단 로밍'과 'HOLB 제거'를 위해 MPTCP와 QUIC이 전송 계층 트렌드를 주도하고 있다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 코어망(SCTP 적용): 5G 핵심망(SBA) 및 Diameter 시그널링 등 폐쇄망 구간에 SCTP Multi-homing을 구성해 물리적 회선 장애 시 지연 0초의 Failover 체계 구축
2. 퍼블릭망(QUIC 전환): 대고객 B2C 웹 서비스(HTTP/3)는 HOLB 제거 및 모바일 로밍 시 세션 무중단을 위해 UDP 기반 QUIC(Connection ID 활용) 통신 스택 적용
3. 로드밸런싱 최적화: UDP/QUIC 환경 도입 시 기존 L4 스위치의 IP/Port 해싱이 아닌 Connection ID 기반 라우팅을 지원하는 차세대 L7/Proxy 도입

**결론 (2줄):**
- 기술사 판단: 프로토콜의 선택은 "가용성(Multi-homing) vs 통과성(Middlebox NAT) vs 신뢰성"의 트레이드오프이며, 용도와 인프라 통제권에 따라 결정된다.
- 향후 방향: SCTP의 훌륭한 아키텍처 철학(Multi-streaming, Homing)은 버려지지 않고 차세대 UDP 기반 QUIC 프로토콜의 뼈대로 그대로 계승되어 발전하고 있다.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ/Ⅴ 강조 |
|:---|:---|:---|:---|
| 설명형 | "TCP, UDP, SCTP를 비교 설명하시오" | 스트림 큐잉(HOLB) 흐름도 대조 | 3개 프로토콜 특징(단위, 멀티스트리밍 유무) 비교표 |
| 방안형 | "이동통신망 또는 고신뢰망 전송 프로토콜 방안" | SCTP Multi-homing에 의한 회선 우회(Failover) 흐름도 | 4-way(SYN Flood 방어), 메시지 지향 이점 |
| 트렌드/융합 | "SCTP의 한계와 QUIC 등 차세대 동향" | 통신 스택 내 Middlebox (NAT/FW) Drop 이슈 시각화 | 커널 독립성, 퍼블릭 망 적용 제약 극복 비교 |

> 요약: SCTP를 묻는 것은 결국 TCP의 약점(HOLB, 단일회선)을 정확히 알고 있는지, 그리고 현장의 미들박스 한계를 인지하는지 묻는 것이다.
