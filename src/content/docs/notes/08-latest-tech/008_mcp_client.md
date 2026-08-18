---
sidebar:
  order: 8
  label: "008. MCP Client (모델 컨텍스트 프로토콜 클라이언트)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "MCP Client (모델 컨텍스트 프로토콜 클라이언트)"
date: "2026-08-14T02:26:00+09:00"
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
- 배경/필요성: 서버 직접 연동은 연결•추적 구현이 중복돼 보안 경계를 유지하기 어려움.

#### 한줄 요약
- **MCP Client**는 호스트•서버 간 연결•메시지 중개

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **요청 메타데이터(Request Metadata)**: 각 요청에 프로토콜 버전•클라이언트 식별•기능을 담아 독립 처리를 가능하게 하는 정보.
- **요청 식별자(Request Identifier, Request ID)**: 비동기 요청과 그에 대응하는 응답•취소를 연결하는 값으로 정의된다.
- **요청 축(Request Axis)**: 서버별 연결과 요청 메타데이터를 관리하는 기능 영역으로 정의된다.
- **추적 축(Tracking Axis)**: 요청 식별자•알림•취소로 비동기 상태를 추적하는 기능 영역을 뜻하며, 복잡한 문제 해결과 동적 환경 적응에 필수적인 역할을 수행한다.
- **중계 축(Relay Axis)**: 서버 기능 명세•실행 결과를 호스트에 전달하는 기능 영역으로 정의된다.

</details>

- **요청 축**: 서버별 연결•버전•식별 메타데이터 관리
- **추적 축**: Request ID•알림•취소 기반 상태 추적
- **중계 축**: 기능 명세•실행 결과를 호스트에 전달

#### 한줄 요약
- **요청 메타데이터•Request ID**로 결과 중계

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **기능 변환기(Feature Converter)**: 서버가 공개한 도구•리소스•프롬프트 명세를 호스트가 사용할 수 있는 형태로 전달하는 구성요소로 정의된다.
- **표준 입출력(Standard Input/Output, stdio)**: 로컬 클라이언트와 서버가 프로세스 입출력 스트림으로 메시지를 교환하는 전송 방식이다.
- **스트리밍 가능 하이퍼텍스트 전송 프로토콜(Streamable Hypertext Transfer Protocol, Streamable HTTP)**: 원격 요청을 HTTP POST와 메서드•기능 라우팅 헤더로 교환하는 전송 방식.

</details>

- **메시지 디스패처**가 JSON-RPC와 전송 연결 관리

```text
                    [메시지 중개기]
                   /       |       \
       [요청 메타 관리자] [기능 변환기] [전송 관리자]
```

선의 의미: 메시지 중개기는 요청 메타, 기능 명세, 서버 연결을 하나의 요청•응답 경계로 결합함.

| 구성요소 | 책임 |
|:---|:---|
| 요청 메타 관리자 | **요청 메타 관리자**가 **요청 메타데이터**를 구성함 |
| 메시지 중개기 | **메시지 디스패처**가 Request ID 기반 요청•응답을 연결함 |
| 기능 변환기 | **기능 변환기**가 서버 기능 명세를 호스트에 전달함 |
| 전송 관리자 | **전송 관리자**가 **stdio**•**Streamable HTTP** 연결을 관리함 |

#### 한줄 요약
- **메시지 디스패처•전송 관리자**가 연결 책임 분담

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **호출 식별자(Call Identifier)**: 비동기 JSON-RPC 요청과 나중에 도착한 응답을 정확히 연결하는 값.
- **모델 컨텍스트 프로토콜 호스트(Model Context Protocol Host, MCP Host)**: 사용자 정책과 여러 MCP Client 연결을 관리하는 AI 애플리케이션.
- **버전•식별•기능 메타 구성(Meta Composition)**: 요청마다 프로토콜 버전•클라이언트 식별•기능을 포함하는 단계이다.
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
   │ 1. 버전•식별•기능 메타 구성
   │ 2. Request ID 기반 표준 요청 전송
   ▼
MCP 서버
   │ 3. 서버 결과•오류 반환
   ▼
MCP 클라이언트
   │ 4. 출처가 구분된 결과 전달
   ▼
MCP 호스트
```

### 동작 원리

1. 버전•식별•기능 메타 구성: 요청마다 프로토콜 버전과 클라이언트 정보를 포함함.
2. Request ID 기반 표준 요청 전송: **호출 식별자**와 선택 기능•구조화 인자를 전달함.
3. 서버 결과•오류 반환: 요청 식별자와 실행 결과를 연결함.
4. 출처가 구분된 결과 전달: 서버 경계를 표시해 호스트에 중계함.

#### 한줄 요약
- **출처가 구분된 결과 전달**로 서버 경계 보존

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **스트리밍 가능 하이퍼텍스트 전송 프로토콜 클라이언트(Streamable Hypertext Transfer Protocol Client, Streamable HTTP Client)**: HTTP POST와 라우팅 헤더로 원격 MCP 서버와 통신하는 클라이언트.

</details>

- **MCP Client•Server**를 연결 중개와 기능 제공으로 구분

| 판단 기준 | MCP Client | MCP Server |
|:---|:---|:---|
| 적용 기준 | **MCP Client**는 호스트의 서버 연결임 | **MCP Server**는 백엔드 기능을 공개함 |
| 핵심 특징 | 서버별 연결•메시지를 중개함 | 도구•리소스•프롬프트를 제공함 |
| 한계 | 호스트의 사용자 정책•실행 권한 책임임 | 서버의 권한•입력 검증 책임임 |

> 요약: 연결 중개에는 **MCP Client**, 기능 제공에는 **MCP Server**를 적용함.

#### 한줄 요약
- **MCP Client**는 연결 중개, **MCP Server**는 기능 제공

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **재요청 정책(Retry Policy)**: 통신 장애 후 백오프•재시도 상한•멱등성으로 중복 실행을 통제하는 규칙.
- **호스트 중계(Host Relay)**: 클라이언트가 서버 기능 명세와 실행 결과를 호스트에 전달하고 최종 사용 여부는 호스트가 결정하게 하는 책임 분리로 정의된다.
</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 복수 서버 결과 혼합으로 출처 오인 | **호스트 중계**에서 서버별 연결•출처 식별자를 유지함 | 문맥•권한 경계를 보존함 |
| 연결 중단으로 미완료 요청 잔존 | **재요청 정책**과 Request ID•취소•시간초과로 정리함 | 유실•중복 실행을 방지함 |
| 기능 변경으로 허용 정책 불일치 | 목록 변경 알림 후 정책을 재평가함 | 변경 기능의 안전한 반영을 달성함 |

#### 한줄 요약
- **재요청 정책•서버별 허용 정책**으로 기능 범위 통제

## Ⅶ. 결론

- 연결•메시지 중계는 **MCP Client**, 기능 공개는 **MCP Server**

#### 한줄 요약
- **연결 책임•기능 제공 책임**에 따라 Client•Server 결정
