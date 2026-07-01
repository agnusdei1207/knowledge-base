---
title: "DID 분산신원 (Decentralized Identifier)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 350
---

# 📖 【암기용】 개념 완전 이해

> 목적: DID를 중앙 ID 제공자에 종속되지 않는 식별자와 공개키 문서 체계로 이해하게 만든다.

## 한눈에
- **개요**: W3C DID Core 기반의 분산형 식별자 체계
- **왜 필요한가**: 기존 로그인은 플랫폼 계정과 중앙 ID 제공자에 의존해 계정 이동성, 프라이버시, 자격증명 검증에 제약이 있다.
- **핵심 직관**: 주민등록번호처럼 기관이 부여한 번호가 아니라, 사용자가 관리하는 식별자와 공개키 주소록을 통해 신원을 증명한다.

## 깊이 이해
- **배경·문제의식**: 중앙집중 ID는 유출 시 피해가 크고, 서비스 간 계정 이동성과 자격증명 상호운용이 낮다. DID는 식별자와 DID Document를 분리해 공개키, 서비스 엔드포인트, 검증 방법을 표현한다.
- **작동 원리**: DID는 `did:method:specific-id` 형식을 가지며, resolver가 DID Document를 조회한다. 검증자는 문서의 공개키로 서명 또는 VC presentation을 검증한다.
- **비유**: 전화번호부가 중앙 회사 서버에만 있는 것이 아니라, 각 사용자가 검증 가능한 명함과 공개키 위치를 제시하는 방식이다.
- **구체 예시**: `did:web:example.com:user:alice`는 웹 도메인을 방법(method)으로 사용하고, HTTPS 위치의 DID Document에서 공개키를 조회할 수 있다.
- **흔한 오해·주의점**: DID 자체가 신원 보증을 의미하지 않는다. 누가 어떤 사실을 보증했는지는 VC의 issuer와 신뢰 정책으로 판단해야 한다.

## 연결 개념
- Verifiable Credential — DID로 식별되는 주체와 발급자를 연결
- DID Document — 공개키와 검증 방법을 담는 문서
- Self-Sovereign Identity — 사용자 중심 신원 관리 관점

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: DID는 식별자, DID Document, resolver, method로 구성되며, 신원 보증은 VC와 신뢰 프레임워크에서 완성된다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DID는 중앙 ID 제공자와 분리된 식별자이며 DID Document를 통해 공개키와 검증 방법을 제공한다.
> 2. **가치**: 사용자·기관·사물 식별자를 서비스 밖에서도 검증 가능하게 만들어 VC와 전자지갑 생태계의 기반이 된다.
> 3. **판단 포인트**: DID method, key rotation, resolver 신뢰성, 개인정보 노출, issuer 신뢰 정책을 함께 검토한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분산신원 구조 이해 확인 | DID, DID Document, resolver, method | 블록체인 주소로만 설명 |
| VC와 관계 확인 | DID는 식별, VC는 주장·자격 증명 | DID가 신원 사실을 보증한다고 단정 |
| 운영 리스크 확인 | 키 분실, 회전, method 폐기 | 사용자 주권을 구호로만 작성 |

> 요약: 이 문제는 DID 자체와 VC 기반 신원 보증을 분리해 설명하는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- 개요: 분산형 식별자
- 배경: 중앙 ID 제공자 기반 로그인은 계정 종속, 유출, 서비스 간 자격증명 재사용 제약을 가짐.
- 필요성: W3C DID Core 기반 식별자와 공개키 검증 체계로 사용자 중심 신원과 기관 발급 자격증명을 연결해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
DID Subject -> DID -> DID Method -> Resolver -> DID Document
                                  +-> Verification Method / Service Endpoint
Issuer / Holder / Verifier -> VC Presentation Verification
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| DID | 주체를 식별하는 URI | did:method:id |
| DID Method | 생성·조회·갱신·폐기 규칙 | did:web, did:key |
| DID Document | 공개키·검증 방법·서비스 정보 표현 | JSON-LD/JSON |
| Resolver | DID를 DID Document로 해석 | method별 구현 |

> 요약: DID는 문자열 식별자만이 아니라 method와 resolver를 통해 검증 문서로 연결되는 체계다.

---

## Ⅲ. 동작원리 및 흐름도

```text
DID 생성 -> DID Document 등록/게시 -> Resolver 조회
-> 공개키·검증방법 확인 -> 서명/VC 검증 -> 키 회전·폐기 관리
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 주체가 DID method에 따라 식별자를 생성함 | method specification |
| 2 | 공개키와 service endpoint를 DID Document에 기록함 | document validity |
| 3 | 검증자가 resolver로 DID Document를 조회함 | resolution result |
| 4 | 공개키로 서명 또는 VC presentation을 검증함 | signature verification |

> 요약: DID 검증은 resolver가 가져온 DID Document의 공개키를 기준으로 서명 소유를 확인하는 절차다.

---

## Ⅳ. 특징

| 구분 | 중앙집중 ID | DID | 판단 기준 |
|:---|:---|:---|:---|
| 식별자 관리 | IDP 계정 | controller 관리 | 계정 이동성 |
| 검증 정보 | IDP API | DID Document | resolver 신뢰 |
| 자격 증명 | 서비스 내부 속성 | VC와 결합 | issuer 신뢰 |
| 위험 | IDP 장애·유출 | 키 분실·method 중단 | 복구 모델 |

> 요약: DID는 중앙 IDP 의존을 줄이지만 키 복구와 method 운영 신뢰를 별도로 설계해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 로그인 | OAuth/OIDC | DIDAuth, VC presentation | 자격증명 이동성 |
| 식별자 | 이메일·계정 ID | DID URI | 프라이버시 요구 |
| 신뢰 근거 | IDP 약관 | issuer trust framework | 검증자 정책 |

> 요약: DID는 기존 OAuth를 무조건 대체하기보다 VC 기반 자격증명 제출이 필요한 업무에서 결합한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 키 분실 | 개인키 단독 보관 | social recovery, hardware wallet | recovery success |
| 개인정보 노출 | DID 재사용 추적 | pairwise DID, selective disclosure | correlation test |
| method 종속 | 특정 ledger·도메인 의존 | method risk review, portability | resolver availability |

> 요약: DID 운영 리스크는 개인키 복구, 식별자 상관분석, method 지속성에서 발생한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 표준 준수 | W3C DID Core 표현 사용 | conformance test |
| 검증성 | resolver 정상 응답 | resolution monitoring |
| 프라이버시 | 서비스별 DID 분리 | wallet policy audit |

> 요약: DID 도입은 식별자 발급 수보다 표준 준수, resolver 가용성, 상관분석 방지로 평가한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 업무별 DID method를 선정하고 생성, 갱신, 폐기, 키 회전, resolver 운영 책임을 문서화함.
2. DID는 식별과 공개키 검증에 사용하고, 학력·자격·권한 같은 사실은 VC issuer 신뢰 정책으로 검증함.
3. 지갑에서 pairwise DID, key backup, recovery 절차를 제공하고 개인정보가 DID Document에 직접 노출되지 않게 함.

**결론 (2줄):**
- 기술사 판단: 서비스 간 자격증명 이동성과 사용자 통제가 필요하면 DID+VC를 적용하고, 단일 조직 내부 인증은 OIDC가 단순함.
- 향후 방향: DID는 VC 2.0, selective disclosure, mobile wallet과 결합해 신원확인·자격증명 제출 인프라로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DID를 설명하시오" | DID resolution과 서명 검증 흐름 | 중앙 ID와 차이 |
| 요구사항 명시형 | "분산신원 구축 방안을 제시하시오" | method 선정과 키 회전 절차 | VC 신뢰·프라이버시 통제 |

> 요약: 설명형은 구조를, 구축형은 method 운영과 VC 신뢰 정책을 중심으로 작성한다.
