---
sidebar:
  order: 67
  label: "067. 검증가능 자격증명 VC (Verifiable Credential)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "위변조 불가능한 디지털 자격증명 표준 : W3C Verifiable Credentials (VC Data Model 2.0 & Bitstring Status List)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-security"
weight: 67
extra:
  question_no: "067"
  source_status: "기출"
  source_history: "132회"
  priority: 50
  priority_note: "W3C VC Data Model 2.0(JSON-LD/JWT), VC(자격증명) vs VP(프레젠테이션), 암호학적 증명(Proof/Signature), W3C Bitstring Status List 1.0(초고속 폐기 검증), ZKP 기반 선택적 공개"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **VC(Verifiable Credential, 검증 가능 자격증명 / W3C 표준)**: 신뢰할 수 있는 발급 기관(Issuer)이 특정 주체(Subject)의 자격, 신원, 권한에 관한 속성 주장(Claims)을 JSON-LD 또는 JWT 표준 데이터 구조로 작성하고, 발급자의 개인키로 암호학적 전자서명(Proof)을 부착하여 위변조를 원천 방지한 기계 판독형 디지털 증명서.
- **중앙 실시간 검증의 프라이버시 침해(Issuer Phone-Home Problem)**: 전통적인 증명 방식은 검증자가 발급 기관 서버에 실시간 API를 호출하여 진위 여부를 확인해야 하므로, 발급 기관이 사용자가 언제 어디서 자격을 사용하는지 온라인 동선을 100% 감시·추적할 수 있는 구조적 결함.

</details>

- 정의/개념: W3C VC Data Model 2.0 표준에 기반하여 **발급자 서명(VC) $\rightarrow$ 보유자 지갑 저장 $\rightarrow$ 목적 맞춤형 선택적 공개(VP) $\rightarrow$ 분산 원장/Bitstring Status List 1.0을 통한 비실시간 자격/폐기 상태 검증** 을 집행하는 **오프라인 검증 가능 디지털 신원 규격**
- 배경/필요성: 기존의 디지털 증명 방식은 검증자가 발급 기관 서버에 실시간 API를 직접 호출하여 진위를 확인해야 하므로, 발급 기관의 서버 부하 및 단일 장애점(SPOF) 유발, 발급 기관에 의한 사용자의 서비스 이용 동선 추적(Phone-Home 문제), 기관별 비표준 데이터 포맷 파편화라는 한계가 존재함에 따라, 암호학적 전자서명(Proof)이 포함된 기계 판독형 JSON-LD/JWT 표준 데이터 구조를 정의한 W3C Verifiable Credentials(VC) Data Model 2.0 및 Bitstring Status List 1.0 표준을 도입하여 **발급 기관 실시간 통신 없는 독립적 오프라인 자격 검증, 선택적 공개(Selective Disclosure / VP)를 통한 프라이버시 보호 및 초고속 비트맵 기반 자격 폐기(Revocation) 검증**을 달성할 필요

#### 한줄 요약
- VC의 이득은 위조 방지 자체가 아니라 검증 비용을 발급 기관의 실시간 응답에서 떼어내 검증자 쪽 서명 연산으로 옮긴 데 있다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **W3C Bitstring Status List 1.0**: 수백만 건의 VC 폐기(Revocation) 및 정지 상태를 1비트 단위(`0`: 유효, `1`: 폐기)로 매핑하고 압축하여 분산 원장 또는 CDN에 호스팅함으로써, 검증자가 발급 서버 부하 없이 밀리초 단위로 폐기 여부를 검증하도록 지원하는 글로벌 표준.
- **선택적 공개(Selective Disclosure / BBS+ 서명)**: 단일 VC 내의 여러 속성 중 검증자가 요구하는 최소 속성만 추출하여 VP를 구성하더라도, 원본 발급자의 암호학적 서명 무결성이 깨지지 않도록 보장하는 영지식 서명 기법.

</details>

- **3자 비연계성 (Issuer-Verifier Decoupling)**: 검증 시 발급 기관의 실시간 API 호출이 불필요하여 발급 기관의 장애(SPOF)와 사용자 추적 위험 완전 해소
- **기계 판독성 및 상호운용성 (Machine-Readable JSON-LD)**: 표준화된 온톨로지 컨텍스트(`@context`)를 통해 서로 다른 시스템 간 자격증명 데이터 자동 파싱
- **프라이버시 중심의 VP 변환 (Data Minimization)**: 원본 VC를 그대로 제출하지 않고 필요한 최소 주장만 추출하여 Verifiable Presentation(VP)으로 제출

#### 한줄 요약
- 발급자와의 실시간 연결을 끊은 대가로 폐기 사실이 즉시 반영되지 않으므로, 상태 목록의 갱신 주기만큼 폐기 지연을 감수하게 된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **VC Data Model 2.0 핵심 데이터 필드**:
  - `@context`: 데이터 스키마 정의 URI.
  - `id`: 자격증명 고유 URI.
  - `type`: 자격증명 유형 (예: `VerifiableCredential`, `DriversLicenseCredential`).
  - `issuer`: 발급자 DID URI.
  - `credentialSubject`: 주체의 속성 집합 (이름, 면허종별 등).
  - `credentialStatus`: 폐기 목록 확인 엔드포인트.
  - `proof`: 암호학적 서명 알고리즘, 생성일자, 서명값(JWS / Ed25519Signature2020).

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. Verifiable Credential (VC: 발급자 전자서명 원본 데이터) ]          │
│  ├─ `@context`: `https://www.w3.org/ns/credentials/v2`                 │
│  ├─ `issuer`: `did:example:police-department` (발급자 DID)              │
│  ├─ `credentialSubject`: { `id`: `did:holder`, `license`: "Class-1" }   │
│  ├─ `credentialStatus`: { `type`: "BitstringStatusListEntry", ... }     │
│  └─ `proof`: Ed25519 비대칭 전자서명 블록 (위변조 100% 방어)            │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (보유자 지갑에 저장 및 선택적 가공)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. Verifiable Presentation (VP: 검증자 제출용 프레젠테이션) ]         │
│  ├─ `type`: `VerifiablePresentation`                                    │
│  ├─ `verifiableCredential`: [ 선택적 추출된 VC 속성 블록 ]              │
│  └─ `proof`: 보유자(Holder)의 챌린지 Nonce 서명 (재전송 공격 방어)     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (검증자 전송)
                                     ▼
[ 검증자 (Verifier) ➔ 발급자 공개키 및 Bitstring Status List 조회 후 최종 인가 ]
```

선의 의미: 발급자의 서명이 포함된 VC가 보유자 지갑에서 검증자 요구에 맞춘 VP로 조립되어, 분산 원장의 공개키/폐기 목록 조회를 통해 인가되는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **발급자 (Issuer)** | 주체의 원천 자격을 확인하고 W3C 규격에 따라 서명(Proof)을 포함한 VC 발행 | Issuer |
| **VC (자격증명 데이터)** | 주체의 자격 주장(Claims), 발급자 식별자, 폐기 포인터, 전자서명이 결합된 표준 구조 | Credential Spec |
| **보유자 지갑 (Holder)** | 스마트폰 보안 영역에 VC를 저장하고, 사용자 동의 하에 최소 속성만 추출하여 VP 생성 | Edge Wallet |
| **VP (프레젠테이션)** | 검증자의 챌린지(Nonce)와 최소 요구 속성을 결합하고 보유자가 직접 서명한 제출 객체 | Presentation |
| **Bitstring Status List** | 수백만 건의 자격 폐기 상태를 비트 단위로 압축 호스팅하여 초고속 폐기 조회 지원 | Revocation List |

#### 한줄 요약
- VC와 VP를 분리한 덕에 원본은 지갑에 남고 제출본만 목적에 맞게 깎이므로, 검증자가 보관하게 되는 개인정보의 양 자체가 구조적으로 줄어든다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **VC 발급부터 VP 검증까지의 5단계 수명주기**:
  1. 발급자가 원천 DB 실사 후 서명된 VC 발행
  2. 보유자가 모바일 지갑에 VC 암호화 저장
  3. 검증자의 Proof Request(Nonce 포함) 수신
  4. 보유자가 필요한 클레임만 추출하여 VP 서명 생성
  5. 검증자가 발급자 공개키 및 Bitstring 폐기 상태 확인 후 인가

</details>

```text
1. [자격 심사 및 VC 발행] 발급 기관이 원천 데이터를 대조하고 발급자 개인키로 서명된 VC(JSON-LD) 발급
            │
            ▼
2. [지갑 저장] 보유자가 수신된 VC를 스마트폰 보안 영역(Secure Storage)에 암호화 보관
            │
            ▼
3. [검증 요청 수신] 서비스 검증자가 일회용 난수(Challenge)와 함께 특정 자격(예: 성인 여부) 증명 요구
            │
            ▼
4. [VP 조립 및 보유자 서명]
    ├─ 보유자 지갑이 VC에서 불필요한 속성을 마스킹하고 필수 속성만 추출
    └─ 검증자의 Challenge 값과 함께 보유자의 개인키로 서명하여 Verifiable Presentation(VP) 생성
            │
            ▼
5. [무결성 및 폐기 상태 검증]
    ├─ 검증자가 발급자 DID 문서의 공개키로 VC 서명 무결성 검증
    ├─ Bitstring Status List를 조회하여 해당 자격증명의 폐기/정지 여부(Bit 0/1) 대조
    └─ [이상 없음 확인 ➔ 발급 서버 호출 없이 독립적으로 서비스 인가 완료]
```

**동작 원리**

1. **암호학적 자립성(Self-Contained Trust)**: 증명서 자체에 발급자의 디지털 서명이 내장되어 독립 검증 가능
2. **동적 프레젠테이션 바인딩**: 보유자가 검증자의 일회용 챌린지에 직접 서명하여 VP 도용 및 Replay 차단
3. **초고밀도 상태 조회**: Bitstring Status List를 통해 수백만 사용자의 폐기 상태를 수 KB의 비트맵으로 검증
4. **발급자 통신 부재**: 검증 시 발급 기관의 실시간 트래픽 유입이 없어 시스템 장애 전파 및 병목 차단
5. **목적 제한적 정보 제공**: 검증자의 비즈니스 요구에 부합하는 최소 속성(Data Minimization)만 전달

#### 한줄 요약
- 검증자의 일회용 챌린지에 보유자가 직접 서명하는 단계가 없으면 VP는 복사만으로 재사용되므로, 그 한 단계가 오프라인 검증을 성립시키기 위해 치르는 대가다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **자격증명 증명 포맷 3대 비교**: 종이/PDF(레거시), 중앙 API 실시간 검증(과도기), W3C VC/VP 표준(미래)의 비교.

</details>

| 비교 항목 | 종이 / PDF 증명서 (Legacy) | 중앙 API 실시간 조회 (Federated) | W3C Verifiable Credentials (VC) |
|:---|:---|:---|:---|
| **위변조 검증 방식** | 육안 직인 확인 (포토샵 위조 취약) | 발급 서버 중앙 DB 실시간 API 조회 | **암호학적 디지털 서명(Proof) 수학적 검증** |
| **발급 기관 의존도** | 없음 (사후 수동 확인) | **100% 실시간 의존 (발급 서버 다운 시 마비)**| **완전 독립적 검증 (분산 원장/CDN 활용)**|
| **사용자 프라이버시** | 전체 서류 제출로 개인정보 과다 노출 | **발급 기관이 사용자의 서비스 이용 동선 추적**| **선택적 공개(VP)로 프라이버시 완벽 보호** |
| **자격 폐기 검증** | 불가능 (유효기간 경과 전 회수 불가)| 실시간 DB 조회로 즉시 확인 | **Bitstring Status List로 초고속 독립 확인**|
| **글로벌 상호운용성** | 수작업 처리 | 벤더/기관별 자체 API 규격 파편화 | **W3C VC Data Model 2.0 국제 표준 호환** |

#### 한줄 요약
- 종이/PDF는 위조에 취약, 중앙 API는 추적과 장애 종속, W3C VC는 독립 검증과 프라이버시를 보장한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **신뢰 레지스트리 매핑(Trust Registry Mapping)**: 암호학적 서명이 유효하더라도, 해당 발급자(DID)가 특정 자격(예: 의사면허, 공인회계사)을 발행할 법적/비즈니스 권한을 가진 공인 기관인지 거버넌스 프레임워크 상에서 대조하는 검증 체계.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 기관별 상이한 데이터 스키마로 인해 **발급된 모바일 자격증명(VC)이 타 서비스 검증기에서 파싱 거부되는 장애** | **W3C Verifiable Credentials Data Model 2.0 및 JSON-LD 표준 온톨로지 전면 강제 채택** | 이기종 지갑 및 서비스 검증기 간의 100% 글로벌 상호운용성 확보 |
| 대규모 트래픽 발생 시 검증자들의 실시간 폐기 조회로 인해 **발급 기관의 중앙 API 서버가 다운되는 병목 사고** | **W3C Bitstring Status List 1.0 규격 적용 및 분산 원장/글로벌 CDN 기반의 비트맵 폐기 목록 캐싱** | 발급 서버 부하(SPOF) 100% 해소 및 밀리초 단위의 초고속 자격 폐기 검증 달성 |
| 유효한 암호 서명이지만 권한 없는 임의 단체가 발행한 **가짜 자격증명(VC)을 검증자가 정상 승인하는 거버넌스 결함** | **비즈니스 검증 로직에 공인 신뢰 등록부(Trust Registry) 매핑 및 발급자 자격 적합성 심사 의무화** | 비인가 기관의 무단 VC 발행 및 사기 자격증명 수용 100% 원천 차단 |

#### 한줄 요약
- 서명이 유효하다는 사실은 발급자가 그 자격을 발행할 권한을 가졌다는 뜻이 아니므로, 암호 검증을 자동화할수록 신뢰 등록부라는 별도의 판단 계층이 더 필요해진다.

## Ⅶ. 결론

- 오프라인 종이 증명서와 중앙 API 실시간 조회 모델의 한계를 극복하고 글로벌 상호운용 가능한 차세대 기계 판독형 디지털 신뢰를 구현하는 **W3C 국제 표준 검증 가능 자격증명(VC Data Model 2.0) 규격**으로 확고히 자리 잡았으며, W3C Bitstring Status List 1.0 및 BBS+ 기반 영지식 증명(ZKP) 서명으로 전면 진화하는 가운데, 실무 엔터프라이즈 VC/VP 시스템 구축 시에는 **W3C VC 2.0 표준 JSON-LD 스키마 준수, 개인정보 유출을 방어하는 최소 속성 선별 추출 및 Holder 서명 기반의 VP(Verifiable Presentation) 조립, 분산 원장/CDN 기반 Bitstring Status List 캐싱을 통한 1ms 이내 초고속 폐기 확인, 발급자 권한을 대조하는 공인 신뢰 등록부(Trust Registry) 거버넌스 연동**을 결합하여 완벽한 디지털 자격증명 무결성을 완성

#### 한줄 요약
- VC는 발급 기관 의존을 프라이버시·가용성과 맞바꾼 설계이므로, 폐기가 즉시 반영되어야 하는 자격에는 여전히 실시간 조회 방식이 유리하다.
