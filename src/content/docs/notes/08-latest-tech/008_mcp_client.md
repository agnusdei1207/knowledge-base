---
sidebar:
  order: 8
  label: "008. MCP Client (모델 컨텍스트 프로토콜 클라이언트)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "MCP Client (모델 컨텍스트 프로토콜 클라이언트)"
date: "2026-08-31T15:08:00+09:00"
tags:
  - "notes-latest_tech"
weight: 8
extra:
  question_no: "008"
  source_status: "기출"
  source_history: "138회"
  priority: 30
  priority_note: "클라이언트 연결은 MCP 하위 구조"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **모델 컨텍스트 프로토콜 클라이언트(Model Context Protocol Client, MCP Client)**: 호스트 내부에서 하나의 MCP 서버 연결과 자기기술적 JSON-RPC 요청을 관리하는 구성요소이다.
- **자바스크립트 객체 표기법 원격 절차 호출(JavaScript Object Notation Remote Procedure Call, JSON-RPC)**: 요청•응답•알림•오류를 JSON 객체로 표현하는 메시지 형식으로 정의된다.
- **모델 컨텍스트 프로토콜 서버(Model Context Protocol Server, MCP Server)**: 도구•리소스•프롬프트 기능을 표준 메시지로 제공하는 외부 구성요소를 지칭한다.

</details>

- 정의: 서버 연결과 JSON-RPC를 관리하는 **MCP Client**이다.
- 배경/필요성: AI 호스트 애플리케이션이 다수의 이종 MCP 서버들과 직접 통신할 경우, 개별 서버의 프로세스 생명주기 관리, 비동기 JSON-RPC 요청-응답 매핑, 통신 오류 및 타임아웃 처리가 애플리케이션 비즈니스 로직과 강하게 결합되어 복잡도가 폭증하는 한계가 발생함에 따라, 각 MCP 서버 연결을 전담하여 1:1 세션 관리, 메시지 디스패칭, 비동기 Request ID 추적 및 기능 명세 변환을 독립적으로 수행하는 MCP Client 계층을 도입하여 **호스트와 서버 간의 느슨한 결합(Loose Coupling) 보장, 서버 장애 시 격리 및 재시도·취소 정책의 일원화된 통제, 다중 서버 기능의 단일 컨텍스트 통합 지원**을 달성할 필요

#### 한줄 요약
- **MCP Client**를 서버마다 하나씩 두면 연결 격리와 보안 경계를 얻지만, 그만큼 호스트가 서버 수에 비례하는 세션 상태를 떠안는다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **요청 식별자(Request Identifier, Request ID)**: 비동기 요청과 그에 대응하는 응답•취소를 연결하는 값으로 정의된다.
- **요청 축(Request Axis)**: 서버별 연결과 요청 메타데이터를 관리하는 기능 영역으로 정의된다.
- **추적 축(Tracking Axis)**: 요청 식별자•알림•취소로 비동기 상태를 추적하는 기능 영역을 뜻하며, 복잡한 문제 해결과 동적 환경 적응에 필수적인 역할을 수행한다.
- **중계 축(Relay Axis)**: 서버 기능 명세•실행 결과를 호스트에 전달하는 기능 영역으로 정의된다.

</details>

- **요청 축**: 서버별 연결과 JSON-RPC 요청 관리
- **추적 축**: Request ID•알림•취소 기반 상태 추적
- **중계 축**: 기능 명세•실행 결과를 호스트에 전달

#### 한줄 요약
- **Request ID·서버별 연결** 기반 결과 중계

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **기능 변환기(Feature Converter)**: 서버가 공개한 도구•리소스•프롬프트 명세를 호스트가 사용할 수 있는 형태로 전달하는 구성요소로 정의된다.
- **표준 입출력(Standard Input/Output, stdio)**: 로컬 클라이언트와 서버가 프로세스 입출력 스트림으로 메시지를 교환하는 전송 방식이다.
- **스트리밍 가능 하이퍼텍스트 전송 프로토콜(Streamable Hypertext Transfer Protocol, Streamable HTTP)**: 원격 요청을 HTTP POST와 메서드•기능 라우팅 헤더로 교환하는 전송 방식.

</details>

- **메시지 디스패처** JSON-RPC와 전송 연결 관리

```text
                    [메시지 중개기]
                   /       |       \
       [요청 메타 관리자] [기능 변환기] [전송 관리자]
```

선의 의미: 메시지 중개기는 요청 메타, 기능 명세, 서버 연결을 하나의 요청•응답 경계로 결합함.

| 구성요소 | 책임 |
|:---|:---|
| 요청 메타 관리자 | 요청 ID와 **취소·시간초과 상태** 관리 |
| 메시지 중개기 | Request ID 기반 **요청·응답 연결** |
| 기능 변환기 | 서버 **기능 명세·결과**를 호스트에 전달 |
| 전송 관리자 | **stdio·Streamable HTTP** 연결 관리 |

#### 한줄 요약
- **메시지 디스패처•전송 관리자** 연결 책임 분담

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **호출 식별자(Call Identifier)**: 비동기 JSON-RPC 요청과 나중에 도착한 응답을 정확히 연결하는 값.
- **모델 컨텍스트 프로토콜 호스트(Model Context Protocol Host, MCP Host)**: 사용자 정책과 여러 MCP Client 연결을 관리하는 AI 애플리케이션.
- **Request ID 기반 표준 요청 전송(Standard Request Transmission)**: 선택 기능과 구조화 인자를 식별자와 함께 보내는 단계.
- **서버 결과•오류 반환(Server Result Return)**: 실행 결과•오류를 요청 식별자와 연결해 받는 단계이다.
- **출처가 구분된 결과 전달(Differentiated Result Delivery)**: 서버 경계를 표시한 결과를 호스트에 중계하는 단계를 지칭한다.

</details>

- **MCP Host•Client** 사이 JSON-RPC 요청•응답 중계

```text
MCP 호스트
   │ 선택 기능•인자•정책 전달
   ▼
MCP 클라이언트
   │ 1. 요청 ID·구조화 인자 구성
   │ 2. JSON-RPC 요청 전송
   ▼
MCP 서버
   │ 서버 결과·오류 반환
   ▼
MCP 클라이언트
   │ 3. 요청 ID·응답 상관관계 확인
   │ 출처가 구분된 결과 반환
   ▼
MCP 호스트
```

### 동작 원리

1. 요청 ID·구조화 인자 구성: 선택 기능과 **호출 식별자** 결합
2. JSON-RPC 요청 전송: 서버별 연결로 **표준 요청** 전달
3. 요청 ID·응답 상관관계 확인: 결과·오류를 **원요청에 결합**

#### 한줄 요약
- **출처가 구분된 결과 전달** 기반 서버 경계 보존

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **스트리밍 가능 하이퍼텍스트 전송 프로토콜 클라이언트(Streamable Hypertext Transfer Protocol Client, Streamable HTTP Client)**: HTTP POST와 라우팅 헤더로 원격 MCP 서버와 통신하는 클라이언트.

</details>

- **MCP Client•Server** 활용 연결 중개와 기능 제공으로 구분

| 구분 | MCP Client | MCP Server |
|:---|:---|:---|
| 적용 기준 | 호스트의 **서버별 연결** | 백엔드 **기능 공개** |
| 핵심 특징 | **연결·메시지 중개** | **도구·리소스·프롬프트** 제공 |
| 한계 | 호스트의 **정책·실행 권한** 책임 | 서버의 **권한·입력 검증** 책임 |

> 요약: 연결 중개에는 **MCP Client**, 기능 제공에는 **MCP Server** 활용 적용함.

#### 한줄 요약
- **MCP Client** 기반 연결 중개, **MCP Server** 기반 기능 제공

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **재요청 정책(Retry Policy)**: 통신 장애 후 백오프•재시도 상한•멱등성으로 중복 실행을 통제하는 규칙.
- **호스트 중계(Host Relay)**: 클라이언트가 서버 기능 명세와 실행 결과를 호스트에 전달하고 최종 사용 여부는 호스트가 결정하게 하는 책임 분리로 정의된다.
</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 복수 서버 결과의 출처 오인 | 연결·결과에 **서버 출처 식별자** 유지 | **문맥·권한 경계** 보존 |
| 연결 중단과 미완료 요청 잔존 | **재요청·취소·시간초과 정책** | **유실·중복 실행** 방지 |
| 기능 변경과 허용 정책 불일치 | 목록 변경 후 **정책 재평가** | **변경 기능**의 안전한 반영 |

#### 한줄 요약
- **재요청 정책•서버별 허용 정책** 기반 기능 범위 통제

## Ⅶ. 결론

- AI 호스트의 복잡한 추론 로직과 외부 분산 MCP 서버들 간의 통신 복잡성을 완벽히 추상화하는 **세션 중개 및 메시지 라우팅 엔진(MCP Client / Request ID Tracking & Session Lifecycle / Message Dispatcher & Feature Converter / Timeout & Error Handling)의 핵심 클라이언트 아키텍처**로 확고히 자리 잡았으며, 다중 서버 동시 연결 및 동적 핫플러그(Hot-plug) 지원으로 발전하는 가운데, 실무 MCP Client 연동 설계 시에는 **고유 Request ID 기반의 비동기 응답-취소 매핑 및 지수 백오프 재시도 정책 수립, 복수 서버로부터 유입된 도구·리소스 명세의 네임스페이스 충돌 방지 및 출처 추적성(Provenance) 확보, 서버 프로세스 비정상 종료 시 호스트 안정성을 보장하는 서킷 브레이커 및 헬스체크 구현**을 결합하여 완벽한 연결 신뢰성과 세션 무결성을 완성

#### 한줄 요약
- **연결 책임•기능 제공 책임** 대상 따라 Client•Server 결정
