---
sidebar:
  order: 202
  label: "202. OPC UA 산업 표준 통신 (OPC Unified Architecture)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "OPC UA 산업 표준 통신 (OPC Unified Architecture)"
date: "2026-08-31T15:08:00+09:00"
tags:
  - "notes-latest-tech"
weight: 202
extra:
  question_no: "202"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "OPC UA 정보 모델•보안 통신이 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **OPC 통합 아키텍처(OPC Unified Architecture, OPC UA)**: 산업 데이터의 의미•통신•보안을 통합하여 이기종 설비의 상호운용을 지원하는 표준이다.

</details>

- 정의: 산업 데이터의 의미•통신•보안을 통합한 **OPC UA** 상호운용 표준
- 배경/필요성: 스마트 팩토리 및 스마트 제조 현장에서 지멘스(Siemens), 미쓰비시(Mitsubishi), 로크웰(Rockwell) 등 다수 벤더의 이기종 PLC, 센서, SCADA 장비가 각기 다른 독점(Proprietary) 필드버스 프로토콜과 단순 원시 데이터(Raw Tag Value)만을 사용하여, 상호 통신 시 복잡한 프로토콜 변환 게이트웨이가 필수적이고 데이터의 문맥적 의미(Contextual Semantics)가 상실되며 윈도우 OS 종속성(DCOM 취약점)에 노출되는 한계에 직면함에 따라, OPC Foundation에서 제정하고 IEC 62541 국제 표준으로 등록된 플랫폼 독립적 개방형 산업 상호운용성 표준인 OPC UA(OPC Unified Architecture / IEC 62541 Standard / AddressSpace Information Model: Object, Variable, Method, Reference, Semantic Typing / Client-Server & PubSub with TSN / Multi-layer Security: X.509 Certificate, Encryption, Signing, User Auth / Cross-platform: C, Java, .NET / Companion Specifications: Euromap, PackML) 규격을 도입하여 **노드 및 객체 지향 주소 공간(AddressSpace)을 통한 원시 데이터를 넘어선 풍부한 의미론적 메타데이터(Semantic Information)의 벤더 무관 표준 교환, 세션 기반 Client-Server 방식과 마이크로초 단위 초저지연 결정론적 통신(PubSub over TSN) 동시 지원, X.509 인증서 기반의 종단 간 강력한 암호화/무결성 검증을 통한 OT-IT 융합 보안**을 달성할 필요

#### 한줄 요약

- 서로 다른 제조사의 장비가 공통 사전과 통신 규칙을 사용하여 값뿐 아니라 값의 의미까지 교환하는 방식이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **의미 기반 정보 모델**: 설비 객체를 노드•속성•참조 관계로 표현해 값의 의미까지 교환하게 하는 모델이다.
- **클라이언트-서버(Client-Server)**: 클라이언트가 서버 기능을 호출하는 세션 기반 통신 모델이다.
- **발행-구독(Publish-Subscribe, PubSub)**: 게시자가 발행한 데이터셋을 다수 구독자가 수신하는 통신 모델이다.

</details>

- 노드•속성•참조로 설비를 표현하는 **의미 기반 정보 모델**
- 클라이언트-서버•**PubSub**를 지원하는 **복수 통신 모델**
- 인증•서명•암호화•권한 제어를 제공하는 **통합 보안**
#### 한줄 요약

- 제조사가 다른 설비도 같은 의미 체계와 보안 규칙으로 데이터를 주고받게 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **주소 공간(AddressSpace)**: 설비 객체와 그 관계를 노드•속성•참조로 표현하는 OPC 통합 아키텍처의 정보 공간이다.
- **클라이언트(Client)**: 서버의 주소 공간을 탐색하고 읽기•쓰기•구독을 요청하는 주체이다.
- **서버(Server)**: 주소 공간과 세션•서비스를 제공하는 주체이다.
- **발행자(Publisher)**: 데이터셋 메시지를 생성해 전송하는 주체이다.
- **구독자(Subscriber)**: 관심 데이터셋 메시지를 비동기로 수신하는 주체이다.
- **정보 모델**: 공통 타입•객체•변수•참조로 설비의 의미와 관계를 상호운용 가능하게 표현한 규약이다.
- **인증서•신뢰 체계**: 애플리케이션 신원과 보안 채널을 검증하고 메시지를 서명•암호화하는 보안 기반이다.

</details>

**AddressSpace 탐색**과 **PubSub 데이터셋 배포**를 지원하는 OPC UA 구조

```text
                    [Client]
                       |
                    [Server]
                       |
                 [AddressSpace]
                       |
              +--------+--------+
              |                 |
         [Publisher]       [Subscriber]
              |
       [인증서•신뢰 체계]
```

선의 의미: 정보 모델 공유•데이터셋 배포와 신원•보호 경계 관계

| 구성요소 | 책임 |
|:---|:---|
| Client | **탐색•읽기•쓰기•구독** 요청 |
| Server | **서비스**•**세션** 관리 |
| AddressSpace | **노드•속성•참조 관계** 표현 |
| Publisher | **DataSet 메시지 발행** |
| Subscriber | **DataSet 메시지 수신** |
| 인증서•신뢰 체계 | **인증서•키•권한** 관리 |

#### 한줄 요약

- AddressSpace가 값에 의미를 붙여 두기에 수신 측이 별도 매핑 없이 해석할 수 있고, **안전한 데이터셋 전달**은 그 의미를 훼손 없이 옮기는 통신 계층이 맡는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **보안 채널**: 인증서를 검증한 통신 주체 사이에서 메시지의 서명과 암호화를 제공하는 연결이다.

</details>

```text
[Client] ── Endpoint 탐색 요청 ──▶ [Server]
[Client] ◀──── Endpoint 목록 ────── [Server]
    │ 1. 보안 채널 요청
    └─────────────────────────────▶ [Server]
                                        │ 2. 인증서•정책 검증
                                        ▼
                              [인증서•신뢰 체계]
                                        │ 검증 결과
                                        ▼
[Client] ◀── 3. 보안 채널•세션 수립 ── [Server]
    │ 4. 탐색•읽기•구독 요청
    └─────────────────────────────▶ [Server]
                                        │ 5. 노드 조회•구독 등록
                                        ▼
                                  [AddressSpace]
[Client] ◀── 서비스 결과•변경 통지 ─── [Server]
```

### 동작 원리

1. 보안 채널 요청: 보안 정책과 메시지 보호 방식 제안
2. 인증서•정책 검증: 발급자•유효기간•폐기•신뢰 목록 확인
3. 보안 채널•세션 수립: 서명•암호화와 사용자 인증 적용
4. 탐색•읽기•구독 요청: 필요한 노드와 서비스 지정
5. 노드 조회•구독 등록: AddressSpace에서 값과 변경 통지 연결

#### 한줄 요약

- 설비 탐색 후 **보안 채널•상태 변경 통지** 구성

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **단순 태그 프로토콜**: 주소와 값 중심으로 설비 데이터를 교환하는 통신 방식이다.

</details>

| 구분 | OPC UA 클라이언트-서버 | OPC UA PubSub | 단순 태그 프로토콜 |
|:---|:---|:---|:---|
| 적용 기준 | **질의•명령•상태 구독** | 다수 대상 **실시간 배포** | **단순 값 교환** |
| 핵심 특징 | 세션 기반 **서비스 호출** | 송수신자 분리 **메시징** | **주소•값 중심 통신** |
| 한계 | **연결•세션 관리** 부담 | **배포•키 관리** 필요 | **의미•보안 표준** 부족 |

#### 한줄 요약

- 두 통신 패턴은 같은 정보 모델을 요청 응답과 일방 배포 중 어느 비용 구조로 실어 나를지의 차이이며, 수신자가 늘수록 **PubSub** 쪽이 전송 비용을 참여자 수와 분리한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **동반 명세(Companion Specification)**: 산업별 장비와 데이터의 공통 의미 모델을 정의해 공급사 간 해석 차이를 줄이는 명세이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공급사별 **Namespace•모델 차이** | **Companion Specification**•매핑 규칙 적용 | 의미 **상호운용성 향상** |
| 만료•미신뢰 **인증서 연결 중단** | **자동 갱신•신뢰 목록**과 폐기 절차 운영 | 안전한 **가용성 확보** |
| 과도한 **쓰기•Method 권한** | 역할별 **노드•서비스 최소 권한** | **설비 오조작 방지** |

#### 한줄 요약

- 공통 정보 모델과 **인증서 신뢰 체계** 기반 안전한 설비 연동

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **통신 패턴**: 질의•명령•다수 배포처럼 데이터 교환 주체와 방향을 구분하는 기준이다.

</details>

- OT(제조 운영기술)와 IT(정보기술) 영역의 프로토콜 사일로를 허물고 Industry 4.0 및 스마트 팩토리 상호운용성을 실현하는 **글로벌 산업용 통신 및 의미론적 데이터 상호운용성의 최고 표준(OPC UA / IEC 62541 International Standard / Semantic AddressSpace & Companion Specs / Client-Server & PubSub over TSN / End-to-End Security Architecture)의 확고한 표준**으로 확고히 자리 잡았으며, 클라우드 네이티브 MQTT 브로커 및 산업용 AI 데이터 파이프라인과 결합 발전하는 가운데, 실무 OPC UA 구축 시에는 **산업 도메인별 Companion Specification을 활용하여 표준 정보 모델을 설계하고, 제어 트래픽에는 PubSub over TSN을, 상위 시스템 연계에는 Client-Server를 최적 분리 적용하며, X.509 인증서 자동 갱신(GDS) 및 최소 권한 접근 제어**를 결합하여 완벽한 산업 상호운용성과 공장망 사이버 보안을 완성

#### 한줄 요약

- 정보 모델과 **통신 패턴•인증서 신뢰** 공동 표준화
