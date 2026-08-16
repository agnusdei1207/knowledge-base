---
sidebar:
  order: 68
  label: "068. W3C DID 표준 (W3C DID Standard)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "W3C DID 표준 (W3C DID Standard)"
date: "2026-08-13T20:18:00+09:00"
tags:
  - "notes-security"
weight: 68
extra:
  question_no: "068"
  source_status: "기출"
  source_history: "132회"
  priority: 50
  priority_note: "132회 기출이며 DID 문서•해석 표준으로 보존함"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **월드 와이드 웹 컨소시엄(World Wide Web Consortium, W3C)**: 웹 표준 및 분산 신원 생태계 기술 표준을 제정하는 국제 웹 규격 제정 기구이다.
- **분산 식별자(Decentralized Identifier, DID)**: 중앙화된 등록기관 없이 자기주권형 암호키 쌍과 바인딩되어 고유 식별 및 검증이 가능한 URI 표준 식별자이다.
- **W3C DID 표준(W3C DID Specification Core 1.0)**: DID 식별자 구문 구조, DID 문서 Schema, 검증 관계 및 DID 해석기(Resolver) 동작 알고리즘을 정의한 표준 권고안이다.
- **통합 자원 식별자(Uniform Resource Identifier, URI)**: 인터넷 자원을 식별하기 위한 표준 문자열 형식으로 `did:method:method-specific-id` 구조를 갖는다.

</details>

- 정의/개념: DID 구문•문서•해석을 정의한 **W3C DID 표준**
- 배경/필요성: 방법별 구현은 **식별자 해석•키 검증 호환성** 저하

#### 한줄 요약

- did:method:id 형식의 표준 URI를 기반으로 암호화 공개키와 검증 관계를 기술하는 W3C 분산 식별자 데이터 모델 및 해석 규격이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DID 문서(DID Document)**: DID 주체의 공개키, 인증(Authentication) 메커니즘, 검증 관계 및 서비스 엔드포인트를 담은 JSON-LD 데이터 문서이다.
- **검증 관계(Verification Relationship)**: 공개키가 서명 검증(assertionMethod), 신원 인증(authentication), 키 합의(keyAgreement) 중 어떤 용도로 사용 가능한지 명시하는 목적 제약 매핑이다.
- **DID 방법(DID Method)**: 특정 블록체인, DLT, 또는 네트워크 저장소 상에서 DID 및 DID 문서를 CRUD 처리하는 구현 규격 명세이다.

</details>

- **URI** 구문 형식(`did:method:id`)을 준수하여 전역 식별자의 유일성과 방법별 독립적 해석 알고리즘을 보장한다.
- **DID 문서** 내 **검증 관계**를 세분화하여 단일 키 타격을 방지하고, 기능별(인증, 자격서명 등) 용도 제한 보안을 집행한다.
- **DID 방법** 레벨에서 저장소 거버넌스를 분리 정의하여 이기종 DLT 및 PKI 체계와의 유연한 수용성을 제공한다.

#### 한줄 요약

- did:method:id 체계를 기반으로 DID 문서 내 검증 관계(Verification Relationship)를 정의하여 용도별 공개키를 엄격 제어한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DID 주체(DID Subject)**: 해당 DID 식별자가 나타내는 사람, 조직, 기기, 개체 또는 데이터 대상이다.
- **제어자(DID Controller)**: DID 문서의 갱신, 키 회전 및 비활성화 권한을 가짐을 암호학적으로 증명할 수 있는 주체이다.
- **DID 해석기(DID Resolver)**: DID URI 문자를 파싱하고 해당 DID 방법에 맞춰 분산 저장소에서 최신 DID 문서를 해소(Resolution)해 반환하는 소프트웨어이다.
- **해석 메타데이터(Resolution Metadata)**: DID 문서 해소 결과, 조회 에러 코드, Content-Type 및 비활성화(Deactivated) 상태 메타정보이다.

</details>

```text
                     [DID 주체·제어자]
                              |
                            [DID]
                              |
                         [DID 방법]
                              |
                         [DID 해석기] -- [DID 문서·검증 관계]
```

선의 의미: DID 주체/제어자가 소유한 DID 식별자를 DID 방법 명세에 따라 DID 해석기가 바인딩하여 최신 DID 문서를 반환하는 파이프라인 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| DID 주체·제어자 | **DID 주체**의 식별 대상 지정 및 **제어자**의 비밀키 기반 DID 문서 변경 통제 권한 보유 |
| DID | `did:method:id` 고유 문자열 구조로 식별 및 방법 지정 |
| DID 방법 | **DID 방법** 명세에 정의된 바에 따라 저장소별 생성•조회•갱신•비활성화 (CRUD) 집행 |
| DID 해석기 | **DID 해석기**가 입력을 받아 최신 **DID 문서** 및 **해석 메타데이터** 해소 반환 |
| DID 문서·검증 관계 | 공개키, 서비스 엔드포인트 및 목적별(assertion, auth 등) **검증 관계** 제공 |

#### 한줄 요약

- DID 식별자를 입력받은 해석기가 DID 방법 명세에 따라 분산 저장소를 조회하여 최신 DID 문서 및 검증 관계를 도출한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **현재 DID 문서(Active DID Document)**: 해소 시점에 특정 DID 저장소에서 추출된 활성 상태의 최신 암호키 및 검증 관계 문서이다.
- **키 용도 판정(Key Purpose Verification)**: 검증에 사용된 공개키가 DID 문서 내 명시된 목적(assertionMethod 등)과 정확히 일치하는지 심사하는 과정이다.
- **DID URI•방법 구문 해석(DID URI & Method Syntax Resolution)**: 식별자 문자열에서 URI Prefix, Method 이름, 고유 ID 구문을 분리 파싱하는 단계이다.
- **최신 DID 문서•상태 해석(Active DID Document & Status Resolution)**: 대상 저장소에서 최신 DID 문서 데이터 및 비활성화 여부를 수집하는 단계이다.
- **문서•해석 메타데이터 검증(Document & Resolution Metadata Verification)**: 반환된 문서의 JSON-LD 구문 정합성 및 에러 상태를 확인하는 단계이다.
- **키 용도•제어 상태 판정(Key Purpose & Controller State Determination)**: 전자서명에 사용된 키가 올바른 검증 관계에 속해 있는지 및 제어권 만료 여부를 판정하는 단계이다.

</details>

```text
[검증자]
      |
      `-- 검증 대상 DID 해석 요청
                  |
                  v
[DID 해석기]
      |
      v
1. DID URI·방법 구문 해석
      |
      `-- 현재 상태 조회
                  |
                  v
[DID 방법]
      |
      v
2. 최신 DID 문서·상태 해석
      |
      `-- DID 문서·상태
                  |
                  v
[DID 해석기]
      |
      v
3. 문서·해석 메타데이터 검증
      |
      `-- 문서·해석 메타데이터
                  |
                  v
[검증자]
      |
      v
4. 키 용도·제어 상태 판정
      |
      v
[검증 결과]
```

### 동작 원리

1. DID URI•방법 구문 해석: 식별자•방법명 분리
2. 최신 DID 문서•상태 해석: 최신 문서•비활성 상태 조회
3. 문서•해석 메타데이터 검증: 모델 정합성•오류 상태 확인
4. 키 용도•제어 상태 판정: 검증 관계•제어권 평가

#### 한줄 요약

- DID 구문 파싱, 방법 기반 최신 DID 문서 해소, 데이터 모델 정합성 확인 및 키 용도/제어 상태 판정으로 검증을 집행한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **중앙 식별자(Centralized Identifier)**: 서비스 제공자가 자체 서버 DB에 사용자 아이디와 패스워드를 발급·관리하는 방식이다.
- **연합 식별자(Federated Identifier)**: Google, Naver 등 SSO 인가 서버가 사용자 식별 토큰을 발행 및 통제하는 중앙집중형 연동 방식이다.

</details>

| 식별자 관리 방식 | W3C DID 표준 | 중앙 식별자 (DB) | 연합 식별자 (OAuth/IdP) |
|:---|:---|:---|:---|
| 적용 기준 | 글로벌 독립 자격 검증 및 주권 보장 | 단일 기관 내부 계정 관리 | 타사 간 통합 로그인 및 SSO |
| 핵심 특징 | **W3C DID 표준** 기반 비대칭 암호키 제어자 수립 | 서비스 제공자의 단일 식별자 DB 종속 | IdP 중심 토큰 발행 및 식별자 통제 |
| 한계 | DID 방법별 거버넌스 파편화 및 키 복구 관리 | 데이터 유출 시 전면 침해 및 계정 차단 위험 | IdP 중앙 장애 영향 및 계정 추적 문제 |

#### 한줄 요약

- 서비스 DB 종속 및 IdP 중앙 통제를 탈피하여, W3C 표준 규격에 따라 제어자가 직접 공개키 및 검증 관계를 동적 관리한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **W3C DID Core 1.0**: W3C의 분산 식별자 아키텍처 및 데이터 모델 최고 표준 권고안 명세이다.
- **키 회전(Key Rotation)**: 노출 위험 및 유효기간 만료에 대비해 DID 문서 내 검증 공개키를 안전하게 새 키로 교체 업데이트하는 절차이다.
- **키 복구(Key Recovery)**: 단말 비밀키 상실 시 복구용 사전에 정의된 멀티시그 또는 사회적 복구(Social Recovery)로 제어권을 재획득하는 기법이다.
- **쌍별 DID(Pairwise DID)**: 검증 서비스별 전용 DID를 개별 발행하여 서비스 간 사용자 행동 상관 추적을 원천 차단하는 기법이다.
- **검증 가능 자격증명(Verifiable Credential, VC)**: 발급자 DID로 서명되어 사용자의 신원 자격을 증명하는 W3C 데이터 규격이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이기종 저장소 간 DID 구문/문서 연동 실패 | **W3C DID Core 1.0** 글로벌 표준 준수 | 글로벌 식별자 해소 호환성 및 상호운용성 완전 확보 |
| 식별자 상반 추적(Correlation) 프라이버시 침해 | **쌍별 DID (Pairwise DID)** 기법 적용 | 서비스 간 사용자 식별자 결합 추적 무력화 |
| 암호키 노출 및 단말 분실로 인한 제어권 상실 | **키 회전** 및 **키 복구** 알고리즘 적용 | DID 제어권 무단 탈취 차단 및 개인키 분실 시 안전한 복구 |

#### 한줄 요약

- W3C DID Core 1.0 규격을 준수하고, 프라이버시 보호를 위한 Pairwise DID와 안전한 키 회전/복구 메커니즘을 상호 적용한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **DID 수용 조건(DID Acceptance Criteria)**: DID 방법의 거버넌스 신뢰성, 최신 DID 문서 활성 여부, 공개키의 검증 관계 적합성이 모두 만족되어야 검증을 승인하는 판단 지침이다.

</details>

- **DID 수용 조건**에 입각하여 DID 방법의 신뢰성, DID 문서 활성화 상태, 검증 관계의 목적 적합성을 정밀 검증한다.

#### 한줄 요약

- **방법 신뢰•문서 활성•키 용도** 확인 후 DID 수용
