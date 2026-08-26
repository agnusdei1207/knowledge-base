---
sidebar:
  order: 68
  label: "068. W3C DID 표준 (W3C DID Standard)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "분산 식별자 구문 및 데이터 모델 표준 : W3C DID Core 1.0 (DID Document & Resolution)"
date: "2026-08-26T14:48:04+09:00"
tags:
  - "notes-security"
weight: 68
extra:
  question_no: "068"
  source_status: "기출"
  source_history: "132회"
  priority: 50
  priority_note: "W3C DID v1.0 권고안, `did:method:method-specific-id` URI 구문, DID 문서(DID Document/JSON-LD), 검증 관계(assertionMethod, authentication 등), DID 해석기(Resolver) 및 쌍별 DID"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **W3C DID Core 1.0(Decentralized Identifiers v1.0)**: 중앙 등록 기관, 신원 확인 기관, 인증 기관(CA) 없이도 주체가 자신의 신원 식별자를 직접 생성·소유·제어하고 암호학적으로 증명할 수 있도록 W3C가 제정한 탈중앙화 식별자 URI 구문 및 데이터 모델 표준.
- **식별자 플랫폼 종속성(Identifier Platform Lock-in Defect)**: 전통적인 이메일 주소나 소셜 계정 ID는 특정 서비스 제공 기업의 도메인(DNS) 및 중앙 DB에 종속되어, 계정 정지나 서비스 종료 시 디지털 신원이 일방적으로 상실되는 구조적 결함.

</details>

- 정의/개념: `did:method:method-specific-id` 구조를 갖는 표준 URI 식별자를 통해 **블록체인/분산 원장에서 DID 문서(DID Document)를 동적으로 해소(Resolution)** 하고, **검증 관계(Verification Relationship)에 따라 암호학적 제어권을 행사** 하는 **글로벌 분산 신원 표준 아키텍처**
- 배경/필요성: 이종 블록체인 및 분산 저장소 간의 상이한 식별자 구현으로 인한 상호운용성 결여를 해결하고, 분산 신원 생태계 전반의 기술적 표준화 규격을 확립할 요구

#### 한줄 요약
- `did:method:id` 표준 URI와 JSON-LD 기반 DID 문서를 통해 중앙 기관 없는 독립적 암호 해소 체계를 구현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **검증 관계(Verification Relationship)**: DID 문서에 등록된 특정 공개키가 서명 검증(`assertionMethod`), 신원 인증(`authentication`), 키 합의(`keyAgreement`), 역량 위임(`capabilityDelegation`) 중 어떤 보안 목적에만 사용될 수 있는지를 명시적으로 제한하는 암호학적 용도 분리 메커니즘.
- **DID 방법(DID Method)**: 특정 블록체인(예: `did:ion`, `did:indy`, `did:ethr`)이나 분산 원장 상에서 DID와 DID 문서를 생성(Create), 조회(Read/Resolve), 갱신(Update), 비활성화(Deactivate)하는 CRUD 구현 명세.

</details>

- **URI 구문 표준화**: `did:<method-name>:<method-specific-id>` 표준 포맷을 통해 전역 유일성과 방법별 독립적 해석 보장
- **용도별 공개키 분리 (Verification Relationships)**: 단일 키 침해 시 전체 권한이 탈취되는 것을 방지하기 위해 인증용, 증명용, 통신 암호화용 공개키 목적 분리
- **하부 분산 저장소 추상화**: 블록체인 종류와 무관하게 상위 애플리케이션은 표준 DID Resolver 인터페이스를 통해 일관된 방식으로 DID 문서 획득

#### 한줄 요약
- 표준 URI 구문, 검증 관계 기반 공개키 용도 분리, 분산 저장소 추상화(DID Method)를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DID Document 핵심 JSON-LD 속성**:
  - `id`: 대상 DID URI.
  - `controller`: 문서를 갱신/폐기할 권한을 가진 주체의 DID.
  - `verificationMethod`: 공개키 암호 알고리즘(Ed25519VerificationKey2020 등) 및 키 데이터.
  - `authentication`: 주체 인증에 사용할 공개키 매핑.
  - `assertionMethod`: VC 등 자격증명 서명 검증에 사용할 공개키 매핑.
  - `service`: 상호작용 엔드포인트 URL.

</details>

```text
[ DID 주체 / 제어자 (Subject / Controller) ]
                      │ (1. DID 생성 및 개인키 제어)
                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. DID 식별자 표준 URI 구문 (did:method:method-specific-id) ]        │
│  ├─ `did`: 표준 URI 스킴 접두사                                        │
│  ├─ `method`: 특정 블록체인/DLT 구현체 식별자 (예: `ion`, `indy`, `key`)│
│  └─ `id`: 해당 분산 원장 내부의 고유 암호학적 식별자 문자열             │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (2. DID Resolution 질의)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. DID 해석기 (Universal DID Resolver) ]                              │
│  └─ DID Method 드라이버를 로드하여 대상 분산 원장(DLT)에서 상태 조회     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (3. DID Document 역직렬화 반환)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. DID 문서 (DID Document: W3C JSON-LD Data Model) ]                  │
│  ├─ `id`: `did:example:123456789abcdefghi`                              │
│  ├─ `verificationMethod`: [ 공개키 1, 공개키 2 ]                        │
│  ├─ `authentication`: [ "#key-1" ] (로그인 인증 전용)                   │
│  └─ `assertionMethod`: [ "#key-2" ] (VC 자격증명 서명 전용)              │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: DID 식별자가 Resolver를 통해 대상 DID Method 드라이버를 거쳐 분산 원장에서 조회된 후, 표준 DID Document로 해소되는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **DID 식별자 (URI)** | `did:method:id` 고유 문자열 구조로 전역 식별성 및 조회 방법 지정 매핑 | W3C URI Scheme |
| **제어자 (Controller)** | 개인키를 소유하여 DID 문서의 생성, 공개키 회전, 비활성화를 암호학적으로 통제 | Controller |
| **DID 방법 (Method)** | 특정 분산 원장(Ethereum, Sovrin 등) 상에서 DID 문서 CRUD 인터페이스 명세 정의 | Implementation |
| **DID 해석기 (Resolver)** | DID URI를 파싱하고 대상 Method 드라이버를 구동하여 최신 DID 문서를 반환 | Resolution Engine |
| **검증 관계 매핑** | `assertionMethod`, `authentication` 등 공개키의 구체적 보안 사용 목적을 한정 | Key Purpose Map |

#### 한줄 요약
- DID URI 식별자, 제어자(Controller), DID 방법(Method), DID 해석기(Resolver), DID Document가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **DID Resolution 4단계 실행 메커니즘**:
  1. 클라이언트/검증자가 DID 해석기에 `resolve(did)` 호출
  2. 해석기가 `method` 파싱 후 해당 분산 원장 전용 드라이버 호출
  3. 분산 원장 상태를 읽어 최신 활성 DID Document 추출
  4. 검증 관계(Verification Relationship)에 부합하는 공개키 반환

</details>

```text
1. [해석 요청] 검증자(Verifier)가 DID 해석기(Resolver)로 `resolve("did:example:12345")` 함수 호출
            │
            ▼
2. [URI 파싱 및 드라이버 라우팅]
    ├─ URI 접두사(`did`), 방법명(`example`), 고유 ID(`12345`) 분리
    └─ `example` 분산 원장 전용 Method 드라이버로 요청 라우팅
            │
            ▼
3. [분산 원장 상태 조회] Method 드라이버가 대상 블록체인 노드에 접속하여 최신 트랜잭션 및 상태 데이터 추출
            │
            ▼
4. [DID 문서 조립 및 검증]
    ├─ JSON-LD 스키마 정합성 검증 및 비활성화(Deactivated) 상태 플래그 확인
    └─ DID Document와 Resolution Metadata(Content-Type, 생성일시) 생성
            │
            ▼
5. [용도별 공개키 대조 및 인가] 검증자가 서명된 연산의 성격에 맞춰 `assertionMethod`에 매핑된 공개키를 추출하여 서명 검증
```

**동작 원리**

1. **스키마 기반 구문 분리**: 콜론(`:`) 구분자를 기준으로 표준 URI 문법을 엄격히 파싱
2. **드라이버 플러그인 아키텍처**: 신규 블록체인이 추가되어도 해석기 코어 수정 없이 Method 드라이버만 확장
3. **불변 상태 무결성 보증**: 분산 원장의 합의 알고리즘에 의해 조작되지 않은 최신 공개키 상태 보장
4. **키 오남용 방지**: 인증용 키로 전자문서를 서명하거나, 통신용 키로 인가를 시도할 경우 검증기에서 즉시 거절
5. **독립적 제어권 갱신**: 제어자가 개인키로 서명한 트랜잭션을 원장에 기록하여 중앙 승인 없이 키 회전(Rotation) 완결

#### 한줄 요약
- 해석 요청, URI 파싱/라우팅, 분산 원장 조회, DID 문서 조립, 용도별 공개키 검증 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **식별자 관리 모델 3대 비교**: 중앙 식별자(DB/DNS), 연합 식별자(IdP/OAuth), W3C DID 표준의 비교.

</details>

| 비교 항목 | 중앙 식별자 (Centralized DB) | 연합 식별자 (Federated IdP) | W3C DID 표준 (Decentralized) |
|:---|:---|:---|:---|
| **식별자 생성 및 제어**| 서비스 제공 기업이 발급 및 제어 | 거대 IdP(Google, Kakao)가 제어 | **사용자(Controller)가 직접 암호학적 제어** |
| **신뢰 및 공개키 검증**| 단일 중앙 DB 내 계정 조회 | IdP 중앙 JWKS 엔드포인트 질의 | **분산 원장(DLT) 기반 DID Resolution** |
| **플랫폼 종속성 (Lock-in)**| **최상 (서비스 탈퇴 시 식별자 소멸)** | **높음 (IdP 계정 정지 시 연동 차단)** | **전혀 없음 (특정 플랫폼에 비종속)** |
| **단일 장애점 (SPOF)** | **중앙 서버 다운 시 전면 인증 불가** | **IdP 장애 시 전 연동 서비스 마비** | **분산 원장 다중 노드로 완벽한 고가용성** |
| **프라이버시 추적성** | 기업 내부 데이터베이스 기록 | **빅테크가 사용자의 로그인 동선 추적** | **쌍별 DID(Pairwise)로 상호 추적 차단** |

#### 한줄 요약
- 중앙 식별자는 기업 종속, 연합 식별자는 IdP 추적 종속, W3C DID는 사용자가 직접 제어하는 비종속 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **쌍별 DID(Pairwise DID)**: 단일 전역 DID를 모든 웹사이트에 재사용할 경우 발생하는 사용자 활동 결합 추적(Correlation)을 방지하기 위해, 서비스 제공자마다 고유한 독립 DID를 동적 생성하는 프라이버시 보호 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이종 블록체인 기반 DID 구현체 간의 데이터 구조 불일치로 인한 **글로벌 신원 해석 및 연동 실패 장애** | **W3C DID Core 1.0 표준 데이터 모델 및 Universal Resolver 오픈소스 드라이버 통합 채택** | 이기종 분산 원장 간 100% 상호운용성(Interoperability) 및 식별자 해소 보장 |
| 고정된 단일 DID를 여러 서비스에서 재사용하여 **검증 기관들이 결탁하여 사용자의 활동을 교차 추적하는 프라이버시 침해** | **서비스마다 별도의 가변 식별자를 동적 발행하는 쌍별 DID(Pairwise DID) 아키텍처 의무화** | 검증자 간 사용자 데이터 상관 추적(Correlation) 100% 원천 차단 |
| 단말 분실이나 개인키 노출 시 중앙 비밀번호 초기화 채널 부재로 인한 **DID 제어권의 영구 상실 위험** | **DID Document 내 사전 정의된 다중 서명(Multisig) 기반 키 회전 및 소셜 복구(Social Recovery) 체계 구축** | 개인키 분실 시에도 안전한 제어권 복원 및 계정 탈취 위험 완벽 해소 |

#### 한줄 요약
- W3C 표준으로 상호운용성을 보장하고, 쌍별 DID로 상관 추적을 막으며, 소셜 복구로 제어권을 보존한다.

## Ⅶ. 결론

- 상호운용성에는 **DID Core**, 추적 방지에는 쌍별 DID와 키 회전 적용

#### 한줄 요약
- W3C DID Core 1.0 표준과 검증 관계 분리 및 Universal Resolver를 통해 자기주권 분산 신원을 완성한다.
