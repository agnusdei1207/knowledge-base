---
sidebar:
  order: 6
  label: "006. 모델 컨텍스트 프로토콜 (Model Context Protocol, MCP)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "모델 컨텍스트 프로토콜 (Model Context Protocol, MCP)"
date: "2026-08-31T15:08:00+09:00"
tags:
  - "notes-latest_tech"
weight: 6
extra:
  question_no: "006"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "표준형 AI 도구 연계가 최신 출제축"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **모델 컨텍스트 프로토콜(Model Context Protocol, MCP)**: AI 호스트와 외부 서버 간 도구·리소스·프롬프트 발견 및 교환을 표준화한 연결 프로토콜. 시스템의 자율적 기능 발견과 일관된 상호작용을 매개하는 핵심 아키텍처.

</details>

- 개념: AI 호스트와 서버가 기능을 교환하는 **JSON-RPC 프로토콜**
- 배경/필요성: 다양한 AI 애플리케이션(Claude Desktop, IDE, 챗봇 등)과 외부 데이터 소스 및 도구(DB, GitHub, 로컬 파일 등) 간의 연동이 파편화된 개별 API로 구현됨에 따라, 클라이언트와 서버의 추가마다 연동 복잡도가 $M \times N$으로 기하급수적으로 폭증하고 유지보수가 불가능해지는 생태계 고립 문제가 발생함에 따라, 앤트로픽(Anthropic)이 주도하여 AI 모델과 외부 시스템 간의 표준 개방형 연결 규격인 모델 컨텍스트 프로토콜(MCP: Model Context Protocol)을 정립하여 **JSON-RPC 2.0 기반의 도구(Tools)·리소스(Resources)·프롬프트(Prompts) 표준 인터페이스 확립, $M+N$ 복잡도의 개방형 AI 확장 생태계 구축 및 로컬(stdio)·원격(SSE/Streamable HTTP) 전송 계층 통일**을 달성할 필요

#### 한줄 요약
- **MCP**는 조합별 최적화 여지를 포기하는 대신 호스트와 서버가 서로를 모른 채 붙게 하여, 연동 비용을 조합 수가 아니라 참여자 수에 비례시킨다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **요청 자기기술성(Self-Descriptive Request)**: 요청이 프로토콜 버전·클라이언트 식별·기능 메타데이터를 자체적으로 전달하는 성질.
- **서버 발견(Server Discovery)**: 클라이언트가 호출 전 서버 기능을 선택적으로 조회하는 원격 프로시저 호출 절차.
- **JSON-RPC**: 요청·응답·알림·오류를 JSON 객체로 표현하는 메시지 표준 형식.
- **메시지 축(Message Axis)**: JSON-RPC 기반 도구·리소스·프롬프트를 교환하는 메시지 데이터 교환 영역.
- **책임 축(Responsibility Axis)**: 호스트·클라이언트·서버 간 정책·연결·기능 책임을 명확히 구분하는 아키텍처 영역.

</details>

- **협상 축**: 초기화로 버전·기능·식별 정보 교환
- **메시지 축**: JSON-RPC로 도구•리소스•프롬프트 교환
- **책임 축**: 호스트•클라이언트•서버 책임 분리

#### 한줄 요약
- **요청 자기기술성•서버 발견** 기반 연동 방식 통일

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **모델 컨텍스트 프로토콜 호스트(Model Context Protocol Host, MCP Host)**: 사용자 동의•보안 정책과 여러 MCP 클라이언트 연결을 관리하는 인공지능 애플리케이션.
- **MCP 클라이언트(MCP Client)**: 서버별 연결과 프로토콜 메시지 교환을 관리하는 호스트 내부 구성요소를 뜻하며, 복잡한 문제 해결과 동적 환경 적응에 필수적인 역할을 수행한다.
- **MCP 서버(MCP Server)**: 도구•리소스•프롬프트 기능을 표준 메시지로 제공하는 외부 구성요소.
- **표준 입출력(Standard Input/Output, stdio)**: 로컬 MCP 프로세스가 표준 입력•출력 스트림으로 메시지를 교환하는 전송 방식을 지칭한다.
- **스트리밍 가능 하이퍼텍스트 전송 프로토콜(Streamable Hypertext Transfer Protocol, Streamable HTTP)**: HTTP POST와 요청 라우팅 헤더로 원격 MCP 메시지를 교환하는 방식.

</details>

```text
                  [MCP 호스트]
                       |
                [MCP 클라이언트]
                       |
                  [MCP 서버]
                       |
             [JSON-RPC·전송 계층]
```

선의 의미: MCP 호스트 내부의 클라이언트가 MCP 서버와 연결되고, JSON-RPC•전송 계층이 양측 메시지 교환 경계를 제공하는 프로토콜 구조를 나타냄.

| 구성요소 | 책임 |
|:---|:---|
| MCP 호스트 | 사용자 동의·정책·**복수 서버 연결** 관리 |
| MCP 클라이언트 | 서버별 연결과 **메시지 교환** 관리 |
| MCP 서버 | **도구·리소스·프롬프트** 제공 |
| JSON-RPC·전송 계층 | **stdio·Streamable HTTP** 메시지 전달 |

#### 한줄 요약
- **MCP Host** 서버별 연결•보안 경계 관리

## Ⅳ. 흐름도

```text
MCP 클라이언트
   │ 1. initialize 요청
   ▼
MCP 서버
   │ 초기화 결과 반환
   ▼
MCP 클라이언트
   │ 2. initialized 알림
   │ 3. tools/list 요청
   ▼
MCP 서버
   │ 도구 목록 반환
   ▼
MCP 클라이언트
   │ 4. tools/call 요청
   ▼
MCP 서버
   │ 도구 결과·오류 반환
   ▼
MCP 클라이언트
```

### 동작 원리

1. **initialize 요청**: 버전·기능·클라이언트 정보 전달
2. **initialized 알림**: 초기화 완료 상태 통지
3. **tools/list 요청**: 서버의 사용 가능 도구 조회
4. **tools/call 요청**: 선택 도구와 구조화 인자 전달

#### 한줄 요약
- 초기화와 기능 목록 조회 후 선택한 도구를 호출한다.


## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **개방형 응용 프로그래밍 인터페이스 명세(OpenAPI Specification, OpenAPI)**: 고정된 하이퍼텍스트 전송 프로토콜(Hypertext Transfer Protocol, HTTP) API 계약을 기술하는 명세를 뜻하며, 복잡한 문제 해결과 동적 환경 적응에 필수적인 역할을 수행한다.

</details>

| 구분 | MCP | OpenAPI | 맞춤형 API |
|:---|:---|:---|:---|
| 적용 기준 | **모델 도구·컨텍스트 연계** | **고정 HTTP 계약** | **단일 시스템 연동** |
| 핵심 특징 | **기능 목록·호출·컨텍스트** 교환 | **HTTP API 계약** 기술 | 구현별 **직접 연동** |
| 한계 | **호스트·서버 보안** 필요 | **동적 기능 목록** 부재 | **재사용·상호운용성** 부족 |

> 요약: **MCP** 기반 기능 발견, **OpenAPI** 기반 고정 HTTP 계약에 초점을 둠.

#### 한줄 요약
- 기능 목록 기반 연계는 **MCP**, 고정 HTTP 계약은 **OpenAPI**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **신뢰 경계(Trust Boundary)**: 호스트•클라이언트•서버 사이에서 인증•권한•입력 검증 책임이 달라지는 보안 경계.
- **전송 계층 보안(Transport Layer Security, TLS)**: 원격 전송 메시지의 기밀성•무결성과 서버 인증을 제공하는 보안 프로토콜.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 과도한 기능 공개와 권한 확산 | 경계별 **허용 목록·최소 권한** | **서버 보안 경계** 유지 |
| 원격 전송의 토큰 탈취·오용 | **TLS·토큰 대상·범위 검증** | **비인가 요청** 방지 |
| 도구 호출의 실제 업무 부작용 | 동의·인자·대상·**승인 검증** | **연결·실행 권한** 분리 |

#### 한줄 요약
- 서버별 **신뢰 경계•최소 권한** 기반 기능 공개 제한

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **MCP 적용 구분(MCP Application Division)**: AI 호스트가 모델의 기능 발견•컨텍스트 교환이 필요할 때 MCP를 적용하고, 고정 HTTP 계약만 필요하면 OpenAPI를 적용하는 구분.

</details>

- AI 애플리케이션과 외부 데이터·도구를 레고 블록처럼 유연하고 안전하게 연결하여 개방형 AI 에이전트 생태계를 완성하는 **개방형 연결 프로토콜 표준(Model Context Protocol: MCP / Host-Client-Server Architecture / Tools·Resources·Prompts / JSON-RPC 2.0 & stdio/SSE)의 사실상 표준(De Facto Standard)**으로 확고히 자리 잡았으며, 엔터프라이즈 AI 허브 및 원격 멀티 에이전트 상호운용성으로 영역을 확장하는 가운데, 실무 MCP 기반 AI 시스템 설계 시에는 **서버의 능력을 동적으로 탐색하는 tools/list 및 resources/list 기반 기능 디스커버리 구현, 데이터 읽기(Resource)와 상태 변경(Tool) 간의 엄격한 역할 분리 및 최소 권한(Least Privilege) 원칙 적용, 로컬 프로세스(stdio)와 원격 보안 통신(Streamable HTTP/TLS & OAuth 2.0) 환경에 맞춘 최적 전송 계층 구성**을 결합하여 완벽한 상호운용성과 확장성을 완성

#### 한줄 요약
- **기능 발견 필요성•계약 고정성** 대상 따라 프로토콜 결정
