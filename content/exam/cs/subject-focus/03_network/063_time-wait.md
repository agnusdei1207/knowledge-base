---
title: "TIME_WAIT (TIME_WAIT, 2MSL)"
date: "2026-06-30"
weight: 63
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> TCP 연결을 능동 종료(Active Close)한 측이 마지막 ACK 전송 후 2MSL(Maximum Segment Lifetime) 동안 소켓을 유지하는 상태로, 지연 패킷 처리와 정상 종료를 보장한다.

## Ⅱ. 구성요소 / 원리
- 능동 종료 측 진입: 마지막 ACK를 보낸 쪽이 TIME_WAIT 상태로 전이
- 2MSL 대기: 세그먼트 최대 생존시간의 2배(왕복) 동안 유지
- 마지막 ACK 보장: ACK 유실 시 상대의 FIN 재전송에 재응답 가능
- 지연 패킷 소멸: 이전 연결의 잔존 세그먼트가 신규 연결에 혼입 방지
- 종료: 2MSL 경과 후 CLOSED, 동일 4-tuple 재사용 가능

## Ⅲ. 흐름도 / 구조
```text
[FIN_WAIT] --수신 FIN--> 마지막 ACK 송신
                              |
                        [TIME_WAIT] (2MSL 대기)
                              |
   (상대 FIN 재전송 시 ACK 재응답 / 지연패킷 소멸)
                              v
                          [CLOSED]
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 마지막 ACK 신뢰 전달과 이전 연결 패킷의 신규 혼입 차단 |
| 장점 | 연결 종료 신뢰성·데이터 무결성 보장 |
| 한계 | 다수 단기 연결 시 포트/소켓 고갈, 자원 점유 |

## Ⅴ. 기술사적 적용
- 고부하 서버 포트고갈 대응: SO_REUSEADDR, tcp_tw_reuse 튜닝
- 능동 종료 주체를 서버→클라이언트로 설계해 서버 TIME_WAIT 분산
- 커넥션 풀·Keep-Alive로 종료 빈도 감소, 자원 효율화
