---
sidebar:
  order: 30
  label: "030. TCP TIME_WAIT 상태"
  badge:
    text: "기출 · 30%"
    variant: note
title: "TCP TIME_WAIT 상태 (TIME_WAIT State)"
date: "2026-08-26T13:47:24+09:00"
tags:
  - "notes-network"
weight: 30
extra:
  question_no: "30"
  source_status: "기출"
  source_history: "132회"
  priority: 30
  priority_note: "설명형: 132회 TCP 종료 상태 직접 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **TIME_WAIT**: TCP 4-Way Handshake에서 능동 종료(Active Close) 측이 최종 ACK를 송출한 후 2MSL 동안 소켓 정보를 보류하는 상태.
- **Ghost Packet (지연 패킷)**: 네트워크 경로 상에 지연되어 떠돌다가 이전 세션이 종료된 후 동일 소켓 튜플로 개설된 신규 세션에 뒤늦게 혼입되는 패킷.

</details>

- 정의/개념: TCP 4-Way Handshake에서 **능동 종료(Active Close) 측이 최종 ACK를 전송한 후 2MSL 동안 소켓 상태를 유지하는 대기 메커니즘**
- 배경/필요성: 즉시 소켓 해제 시 발생하는 **최종 ACK 유실에 따른 상대방 LAST_ACK 교착 및 신규 세션으로 지연 패킷 혼입 오염 방어 불가**

#### 한줄 요약
- 최종 ACK 유실 재전송과 지연 패킷 소멸을 위해 능동 종료 측이 2MSL 동안 세션을 안전 유지한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Active Close (능동 종료)**: 세션 해제를 먼저 호출(`close()`)하여 최초 FIN을 전송하고 TIME_WAIT 타이머를 감당하는 주체.
- **2MSL (2 * Maximum Segment Lifetime)**: 세그먼트가 네트워크에서 생존 가능한 최대 시간(MSL)의 2배(RFC 793 권고 2분, 리눅스 60초) 대기.

</details>

- **최종 ACK 유실 대응**: 상대방이 FIN을 재전송할 경우 정상적으로 ACK를 재응답하여 상대방 CLOSED 유도
- **지연 패킷(Ghost Packet) 격리**: 이전 세션의 잔존 세그먼트가 완전히 소멸될 때까지 동일 4-튜플 재할당 차단
- 빈번한 단기 연결(Short-lived HTTP) 발생 시 수만 개의 소켓이 누적되어 **임시 포트 고갈(Port Exhaustion) 유발**

#### 한줄 요약
- 최종 ACK 재응답 보장, 지연 패킷 소멸 대기, 대량 누적 시 임시 포트 고갈 리스크를 수반한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **4-Tuple (소켓 식별자)**: 출발지 IP, 출발지 포트, 목적지 IP, 목적지 포트로 구성되어 소켓 엔드포인트를 고유 식별하는 4가지 값.

</details>

```text
[TIME_WAIT 상태 제어 및 2MSL 타이머 구조]
|-- TIME_WAIT 상태 (능동 종료 대기)
|-- 2MSL 타이머 (지연 패킷 소멸)
|-- 4-튜플 식별자 (소켓 바인딩 유지)
`-- ACK 재전송기 (재수신 FIN 응답)
```

선의 의미: 계층 및 2MSL 타이머가 가동되는 동안 지연 패킷을 폐기하고 상대방 재전송 FIN에 ACK를 재회신하는 구조

| 구성요소 | 책임 |
|:---|:---|
| TIME_WAIT 상태 | 능동 종료 후 **2MSL 대기 유지** |
| 2MSL 타이머 | 지연 세그먼트의 **소멸 시간 보장** |
| 4-튜플 식별자 | 이전 소켓의 **바인딩 정보 유지** |
| ACK 재전송기 | 재수신 FIN에 **최종 ACK 재응답** |

#### 한줄 요약
- TIME_WAIT 상태, 2MSL 타이머, 4-튜플 식별자, ACK 재전송기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **LAST_ACK 탈출**: 수동 종료자가 최종 ACK를 수신하지 못해 FIN을 재전송할 때 TIME_WAIT 소켓이 ACK를 다시 응답하여 종료를 완료시키는 흐름.

</details>

```text
TIME_WAIT 생명주기 및 예외 복구 흐름
        │
   [최종 ACK 전송] 능동 종료 측이 서버의 FIN 수신 후 최종 ACK(Ack=v+1) 전송
        │
   [TIME_WAIT 진입] 능동 종료 측이 TIME_WAIT 전이 및 2MSL(60초) 타이머 가동
   ┌────┴───────────────────────────┐
  최종 ACK 유실 (서버의 FIN 재수신)  정상 종료 진행 (지연 세그먼트 도달)
   │                                 │
 [ACK 즉시 재전송]                   [지연 패킷 폐기 (Drop)]
   서버를 LAST_ACK에서 CLOSED로 구제     신규 세션 침범 방지
   │                                 │
   └────────────────┬────────────────┘
                    ▼
   [2MSL 타이머 만료] 소켓 자원 및 4-튜플 완전 해제 (CLOSED 전이)
```

#### 한줄 요약
- 최종 ACK 전송 → TIME_WAIT 진입 → 재전송 FIN에 ACK 재응답 / 지연 패킷 폐기 → 2MSL 만료 후 완전 해제 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **TIME_WAIT** vs **CLOSE_WAIT** vs **FIN_WAIT_2**: 타이머 대기(정상 능동), 애플리케이션 close() 지연 누수(비정상 수동), 상대 FIN 대기.

</details>

| 비교 항목 | TIME_WAIT (정상 대기) | CLOSE_WAIT (앱 누수) | FIN_WAIT_2 (상대 대기) |
|:---|:---|:---|:---|
| 발생 주체 및 조건 | **능동 종료 측** (최종 ACK 송출 후) | **수동 종료 측** (상대 FIN 수신 후) | 능동 종료 측 (최초 FIN에 대한 ACK 수신 후)|
| 상태 지속 원인 | **2MSL 타이머 만료 대기 (정상 동작)**| **애플리케이션이 `close()` 미호출 (버그)**| 상대방이 애플리케이션 잔여 송신 지연 |
| 운영상 주요 리스크 | 대량 발생 시 **임시 포트 고갈(Port Exhaustion)**| **FD 누수로 서버 프로세스 다운 (최악)**| 장시간 지속 시 소켓 커널 메모리 점유 |
| 해결 및 대응 방안 | **커넥션 풀링(Keep-Alive), `tcp_tw_reuse`** | **애플리케이션 소켓 반환 코드 전면 수정** | OS 커널 `tcp_fin_timeout` 단축 |

#### 한줄 요약
- TIME_WAIT은 타이머 기반 정상 대기이며, CLOSE_WAIT은 애플리케이션 close() 누수 버그다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **tcp_tw_reuse (RFC 1323 TCP Timestamp)**: TCP 타임스탬프 옵션을 활용하여 지연 패킷의 순서가 역전되지 않음을 수학적으로 보장하고 TIME_WAIT 포트를 신규 아웃바운드 연결에 즉시 재사용하는 커널 옵션.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NGINX 프록시에서 백엔드 단기 연결로 인한 **TIME_WAIT 수만 개 누적** | **백엔드 통신에 `HTTP Keep-Alive 커넥션 풀링` 적용** | 세션 재사용으로 TIME_WAIT 생성 원천 방지 |
| 아웃바운드 API 호출 급증으로 인한 **임시 포트 고갈(Port Exhaustion)** | 리눅스 커널 **`net.ipv4.tcp_tw_reuse=1` 및 타임스탬프 활성화** | 타임스탬프 검증 하에 안전한 포트 즉시 재사용 |
| 임시 포트 범위 부족으로 신규 소켓 바인딩 실패(EADDRNOTAVAIL) | **`net.ipv4.ip_local_port_range = 10240 65535` 범위 확장** | 사용 가능한 임시 포트 용량 55,000개로 증설 |
| 타이머 튜닝을 위해 무작정 `tcp_max_tw_buckets=0` 강제 삭제 | TIME_WAIT 강제 제거 금지 및 **정석적인 커넥션 풀링 아키텍처 준수** | 지연 패킷 혼입에 따른 세션 파괴 방어 |

#### 한줄 요약
- 커넥션 풀링(Keep-Alive), tcp_tw_reuse 활성화, ip_local_port_range 확장으로 포트 고갈을 방지한다.

## Ⅶ. 결론

- TIME_WAIT은 유지하고 포트 고갈은 **Keep-Alive**, 검증 후 **tcp_tw_reuse**

#### 한줄 요약
- TIME_WAIT은 지연 패킷을 격리하고 정상 세션 종료를 보장하는 필수 안전 상태이며, 커넥션 풀링과 tcp_tw_reuse를 통해 포트 고갈을 방어한다.
