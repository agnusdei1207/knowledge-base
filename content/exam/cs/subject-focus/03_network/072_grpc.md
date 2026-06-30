---
title: "gRPC (gRPC Remote Procedure Call)"
date: "2026-06-30"
weight: 72
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 구글이 개발한 고성능 RPC(Remote Procedure Call) 프레임워크로, HTTP/2 전송과 Protocol Buffers 직렬화를 사용해 다양한 언어 간 효율적 서비스 호출을 제공한다.

## Ⅱ. 구성요소 / 원리
- HTTP/2 전송: 멀티플렉싱·헤더 압축·양방향 스트림 활용
- Protocol Buffers(protobuf): 바이너리 IDL(Interface Definition Language) 직렬화
- 4가지 스트리밍: 단방향, 서버 스트리밍, 클라이언트 스트리밍, 양방향 스트리밍
- 코드 생성: .proto 정의로 클라이언트·서버 스텁 자동 생성
- 다언어 지원: 언어 중립 계약으로 폴리글랏 환경 지원

## Ⅲ. 흐름도 / 구조
```text
 .proto(IDL) --codegen--> Stub
 Client Stub --HTTP/2 + protobuf--> Server Stub
   (단방향/서버/클라/양방향 스트리밍)
   바이너리 직렬화로 저지연·소형 페이로드
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 마이크로서비스 간 고성능·저지연 내부 통신 |
| 장점 | 바이너리·HTTP/2로 빠름, 강타입 계약, 스트리밍 |
| 한계 | 브라우저 직접 호출 제약, 사람이 읽기 어려움 |

## Ⅴ. 기술사적 적용
- MSA(Microservice Architecture) 내부 서비스 통신에 REST 대체로 채택
- 브라우저 연동 시 gRPC-Web 또는 게이트웨이로 REST 변환
- 서비스 메시·프로토콜 표준화와 결합해 관측성·보안 강화
