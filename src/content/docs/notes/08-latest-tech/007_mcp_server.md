---
sidebar:
  order: 7
  label: "007. MCP Server (모델 컨텍스트 프로토콜 서버)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "MCP Server (모델 컨텍스트 프로토콜 서버)"
date: "2026-09-07T15:40:00+09:00"
tags:
  - "notes-latest-tech"
weight: 7
extra:
  question_no: "007"
  source_status: "기출"
  source_history: "138회"
  priority: 30
  priority_note: "서버 기능•책임은 MCP 하위 구조"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **MCP Server(Model Context Protocol Server)**: 도구·리소스·프롬프트를 표준 기능으로 노출하고 백엔드 접근과 실행을 통제하는 프로그램. 시스템 자율적 기능 발견과 일관된 상호작용을 매개하는 핵심 아키텍처.
- **인공지능(Artificial Intelligence, AI)**: 학습•추론으로 기능을 선택하고 결과를 생성하는 기술.

</details>

- 개념: 표준 기능을 노출하고 백엔드 실행을 통제하는 **MCP Server**
- 배경/필요성: 엔터프라이즈 백엔드 시스템(데이터베이스, SaaS API, 내부 마이크로서비스)의 기능과 데이터를 AI 에이전트에 노출할 때, 비표준 맞춤형 래퍼(Wrapper)로 구현하면 호스트마다 중복 개발이 발생하고 데이터 접근 제어 및 비인가 명령 실행을 방어할 중앙화된 보안 경계가 부재한 결함이 발생함에 따라, MCP 표준 규약에 따라 백엔드 리소스와 실행 도구를 정형화된 JSON-RPC 인터페이스로 캡슐화한 MCP Server를 구축하여 **표준화된 기능 발견(Discovery) 및 실행 중개 제공, 세분화된 테넌트 격리 및 인가 정책 집행(Policy Enforcement), 백엔드 API 변경에 영향을 받지 않는 독립적 AI 서비스 계층 확립**을 달성할 필요

#### 한줄 요약
- **MCP Server**는 백엔드 권한을 한 곳에 모아 통제 지점을 단순화하는 대신 그 지점이 단일 침해 지점이 되므로, 노출 목록을 최소로 좁히는 것이 곧 보안 설계다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **기능 발견(Function Discover)**: 클라이언트가 서버의 도구•리소스•프롬프트 목록과 명세를 조회하는 과정을 뜻하며, 복잡한 문제 해결과 동적 환경 적응에 필수적인 역할을 수행한다.
- **검증 축(Validation Axis)**: 인증•인가•입력 검증으로 서버 실행 경계를 통제하는 관점.
- **구조화 결과(Structured Result)**: 클라이언트가 후속 처리할 수 있도록 정해진 필드와 형식으로 반환한 실행 결과를 지칭한다.

</details>

- **기능 발견**: 도구·리소스·프롬프트 목록과 명세 제공
- **검증 축**: 인증•인가•입력 기반 실행 경계 통제
- **결과 축**: 구조화 결과•오류 기반 후속 추론

#### 한줄 요약
- 서버는 **권한•입력 검증** 후 구조화 결과•오류 반환

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **도구 제공자(Tool Provider)**: 스키마와 실행 결과를 공개하고 권한 검증 후 백엔드 동작을 수행하는 핵심 서버 모듈.
- **기능 레지스트리(Function Registry)**: 도구·리소스·프롬프트 명세와 처리기를 등록·관리하는 통합 관리소.
- **백엔드 어댑터(Backend Adapter)**: 검증된 MCP 요청을 내부 API 또는 업무 시스템 호출로 변환하는 변환 모듈.
- **표준 입출력(Standard Input/Output, stdio)**: 로컬 클라이언트와 서버 프로세스가 메시지를 교환하는 전송 방식.
- **스트리밍 가능 하이퍼텍스트 전송 프로토콜(Streamable Hypertext Transfer Protocol, Streamable HTTP)**: 원격 MCP 요청을 HTTP POST와 라우팅 헤더로 교환하는 전송 방식을 뜻하며, 복잡한 문제 해결과 동적 환경 적응에 필수적인 역할을 수행한다.
- **자바스크립트 객체 표기법 원격 절차 호출(JavaScript Object Notation Remote Procedure Call, JSON-RPC)**: MCP 요청•응답•알림•오류를 표현하는 메시지 형식.
- **표현 상태 전송 응용 프로그래밍 인터페이스(Representational State Transfer Application Programming Interface, REST API)**: 백엔드 자원을 고정 HTTP 계약으로 호출하는 인터페이스.

</details>

```text
[MCP Server 내부 아키텍처]
├── [전송 및 프로토콜 계층]
│   ├── 전송 리스너 (stdio / HTTP-SSE)
│   └── JSON-RPC 2.0 프로토콜 파서
├── [기능 관리 및 노출]
│   ├── Tools Provider (도구 실행 명세)
│   ├── Resources Provider (데이터/URI)
│   └── Prompts Provider (프롬프트 템플릿)
├── [보안 및 정책 집행]
│   ├── 인증/인가 및 입력 스키마 검증
│   └── 테넌트 격리 및 감사 로깅
└── [백엔드 연동 계층]
    ├── 내부 서비스 REST/gRPC 어댑터
    └── DB/파일시스템 드라이버
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 전송 계층 | **stdio·Streamable HTTP** 연결 수신 |
| 프로토콜 처리기 | **JSON-RPC** 요청·응답·오류 처리 |
| 기능 레지스트리 | **도구·리소스·프롬프트 명세** 관리 |
| 정책 집행기 | **인증·인가·입력·테넌트** 검증 |
| 백엔드 어댑터 | REST API·**업무 시스템 호출** 변환 |

#### 한줄 요약
- **정책 집행기** 권한 검증 후 백엔드 호출 통제

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **요청•응답 상관관계(Request/Response Correlation)**: JSON-RPC 식별자를 이용해 각 실행 요청과 성공•오류 결과를 연결하는 관계.
- **모델 컨텍스트 프로토콜 클라이언트(Model Context Protocol Client, MCP Client)**: 서버의 기능 목록•명세를 발견하고 실행 결과를 교환하는 구성요소를 뜻하며, 복잡한 문제 해결과 동적 환경 적응에 필수적인 역할을 수행한다.
- **버전•메타•기능 목록 요청(List Request)**: 요청별 프로토콜 버전•클라이언트 식별과 목록 조회를 전달하는 단계.
- **기능 명세•캐시 힌트 제공(Spec/Hint Provision)**: 기능 설명•입력 스키마•유지 시간•공유 범위를 반환하는 단계를 지칭한다.
- **기능명•구조화 인자 요청(Function/Argument Request)**: 선택한 기능과 검증할 인자를 서버에 전달하는 단계.
- **권한•입력 검증 후 백엔드 실행(Backend Execution)**: 허용된 주체와 입력의 작업만 업무 시스템에서 수행하는 단계.

</details>

- **MCP Client•Server** 기반 JSON-RPC 식별자로 결과 연결

```text
MCP 클라이언트
   │ 1. 기능 목록 요청
   ▼
MCP 서버
   │ 기능 명세 반환
   ▼
MCP 클라이언트
   │ 2. 기능명•구조화 인자 요청
   ▼
MCP 서버
   │ 3. 권한•입력 검증 후 백엔드 실행
   ▼
업무 시스템
   │ 백엔드 결과•오류 반환
   ▼
MCP 서버
   │ 서버 변환 결과•오류 반환
   ▼
MCP 클라이언트
```

### 동작 원리

1. 기능 목록 요청: 도구·리소스·프롬프트 **목록 조회**
2. 기능명•구조화 인자 요청: 선택 기능과 **검증 인자** 전달
3. 권한•입력 검증 후 백엔드 실행: 허용 작업만 **업무 위임**

#### 한줄 요약
- **권한•입력 검증 후 백엔드 실행** 및 결과 반환

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Local MCP Server**: 호스트가 시작한 프로세스로 실행되고 stdio를 통해 한 클라이언트와 메시지를 교환하는 서버.
- **REST API Server**: 고정된 HTTP 메서드•자원 계약으로 기능을 제공하는 서버이다.
- **통합 자원 식별자(Uniform Resource Identifier, URI)**: 웹 자원을 식별하는 표준 문자열.

</details>

- **MCP Server•REST API Server** 활용 발견•계약으로 비교

| 구분 | MCP Server | REST API 서버 |
|:---|:---|:---|
| 적용 기준 | AI의 **동적 기능 선택** | **고정 API 계약** 제공 |
| 핵심 특징 | **기능 목록·명세** 제공 | HTTP 메서드·**URI 계약** |
| 한계 | **권한·입력 검증** 책임 | **모델용 기능 목록** 부재 |

> 요약: **MCP 서버 기반 모델 기능 발견**, **REST API 기반 고정 HTTP 계약** 핵심임.

#### 한줄 요약
- 동적 기능 목록은 **MCP**, 고정 웹 자원은 **REST**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **서버 최소 권한(Server Least Privilege)**: MCP Server가 제공 기능에 필요한 백엔드 자원과 작업만 접근하도록 계정•경로•명령을 제한하는 원칙.
- **구조화 오류(Structured Error)**: 실패 원인과 재시도 가능 여부를 클라이언트가 판정하도록 코드와 데이터로 표현한 실행 결과.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 과도한 공개로 공격 표면 확대 | **서버 최소 권한·허용 목록** | **고권한 기능 오용** 차단 |
| 테넌트 식별 누락과 교차 접근 | 주체·백엔드 쿼리에 **테넌트 강제** | **데이터 경계** 보장 |
| 불명확한 오류와 복구 혼선 | 재시도 여부를 담은 **구조화 오류** | **안전한 복구 경로** 선택 |

#### 한줄 요약
- 사용자별 **테넌트•최소 권한** 기반 자료 범위 제한

## Ⅶ. 결론

- 기업의 분산된 데이터 자산과 비즈니스 로직을 표준화된 방식으로 AI 에이전트에 안전하게 노출하는 **기능 제공 및 실행 통제 게이트웨이(MCP Server / JSON-RPC Protocol Handler / Tool·Resource Registry / Policy Enforcement & Backend Adapter)의 핵심 아키텍처**로 확고히 자리 잡았으며, 서버리스 및 컨테이너 기반 마이크로서비스 배포로 진화하는 가운데, 실무 엔터프라이즈 MCP Server 구축 시에는 **제공 기능의 목적과 파라미터 제약조건을 명문화한 JSON Schema 기반 레지스트리 관리, 백엔드 호출 전 클라이언트 인증 토큰 및 테넌트 식별자를 검증하는 정책 집행기(PEP) 구성, 로컬(stdio)과 원격(Streamable HTTP) 클라이언트 동시 지원 및 오류 발생 시 재시도 가능 여부를 포함한 구조화된 오류(Structured Error) 반환**을 결합하여 완벽한 백엔드 보안성과 서비스 안정성을 완성

#### 한줄 요약
- **발견 필요성•계약 고정성** 대상 따라 서버 방식을 결정
