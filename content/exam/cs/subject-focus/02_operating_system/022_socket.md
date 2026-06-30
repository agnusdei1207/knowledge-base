---
title: "소켓 (Socket)"
date: "2026-06-30"
weight: 22
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 네트워크 또는 동일 호스트 내 프로세스 간 양방향 통신을 위한 종단점(endpoint) 추상화로, IP 주소와 포트(또는 경로)로 식별되는 IPC(프로세스 간 통신) 인터페이스.

## Ⅱ. 구성요소 / 원리
- 종단점: (IP 주소 + 포트 번호) 또는 도메인 소켓 파일 경로
- TCP 소켓(SOCK_STREAM): 연결지향·신뢰성·순서보장
- UDP 소켓(SOCK_DGRAM): 비연결·비신뢰·저지연 데이터그램
- 유닉스 도메인 소켓(AF_UNIX): 동일 호스트 내 고속 IPC
- API: socket→bind→listen→accept(서버), connect(클라이언트)

## Ⅲ. 흐름도 / 구조
```text
 Server: socket()->bind()->listen()->accept() ──┐
                                                 | 양방향 stream
 Client: socket()-------------->connect() ───────┘
              |                                  |
            send()/recv() <==== 데이터 교환 ====> send()/recv()
                                close()
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 네트워크·로컬 프로세스 간 양방향 통신 표준화 |
| 장점 | 위치투명성(원격/로컬 동일 API), TCP/UDP 선택적 |
| 한계 | 도메인소켓 대비 네트워크 소켓 오버헤드, 프로토콜 설계 부담 |

## Ⅴ. 기술사적 적용
- TCP: 신뢰성 요구(HTTP·DB), UDP: 실시간(스트리밍·DNS) 선택
- 유닉스 도메인 소켓: 컨테이너·로컬 마이크로서비스 고속 통신
- 비교: 네트워크 IPC(소켓) vs 로컬 IPC(파이프·공유메모리)
