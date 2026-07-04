---
title: "W3C DID 표준 (W3C DID Standard)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 112
---

# 📖 【암기용】 개념 완전 이해

> 목적: W3C DID 표준을 블록체인 주소가 아니라 식별자, DID 문서, 해석 절차로 구성된 분산 식별자 규격으로 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 중앙 등록기관 없이 주체가 제어하는 식별자와 공개키 문서를 연결하는 W3C 분산 식별자 표준
- **왜 필요한가**: 이메일·SNS·IdP 계정은 발급기관 정책에 묶이고 서비스별 추적 가능성이 생긴다. DID는 식별자 제어권을 주체가 갖고, 검증자는 DID Document로 키와 인증 방법을 확인한다.
- **핵심 직관**: 전화번호부를 한 회사가 독점하지 않고, 누구나 확인 가능한 방법으로 "이 식별자의 공개키는 이것"을 찾아가는 규칙임

## 깊이 이해
- **배경·문제의식**: 중앙 식별자는 계정 정지, 제공자 폐쇄, 데이터 결합 추적, 기관 간 이전 문제를 만든다. DID는 식별자 생성, 해석, 키 회전, 서비스 엔드포인트를 DID Method별 규칙으로 분리한다.
- **작동 원리**: DID는 `did:method:specific-id` 형식이다. Resolver가 DID Method 규칙에 따라 DID Document를 찾고, 문서의 verification method, controller, service를 통해 서명 검증과 통신 엔드포인트를 확인한다.
- **비유**: 주소는 사람이 정하지만, 우편물이 도착하려면 우편번호 체계와 주소 조회 규칙이 필요하다. DID는 주소 형식과 조회 규칙을 표준화한 것임
- **구체 예시**: `did:web:example.com`은 HTTPS 도메인에 게시한 DID 문서를 조회하고, 검증자는 문서의 공개키로 VC 발급 서명을 확인한다.
- **흔한 오해·주의점**: DID는 저장소를 강제하지 않는다. 블록체인 DID, 웹 DID, 피어 DID가 모두 가능하며, 개인정보를 DID Document에 직접 넣으면 추적과 노출 위험이 생긴다.

## 연결 개념
- Verifiable Credential — DID 공개키로 발급자 서명 검증
- DID Method — did:web, did:key, did:ion 등 해석 규칙
- DID Resolution — DID를 DID Document로 변환하는 절차
- Key Rotation — 장기 식별자 유지와 키 폐기·교체

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: W3C DID는 분산 신원 전체가 아니라 DID Syntax, DID Document, DID Method, Resolution으로 공개키 기반 식별자 검증을 가능하게 하는 표준임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: W3C DID(Decentralized Identifier)는 `did:method:id` 형식의 식별자를 DID Document의 공개키·인증 메서드와 연결하는 분산 식별자 표준이다.
> 2. **가치**: 중앙 IdP 조회 없이 서명 검증, 키 회전, 서비스 엔드포인트 확인을 수행해 VC·SSI·지갑 기반 신원 교환의 식별 계층을 제공한다.
> 3. **판단 포인트**: DID Method 선택, resolver 신뢰, 키 회전, 문서 개인정보 노출, 메서드 간 상호운용, 거버넌스가 도입 성패를 좌우한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DID 표준 구성 이해 확인 | DID Syntax, DID Document, DID Method, Resolver | 블록체인 주소로만 설명 |
| 신원 검증 구조 판단 확인 | verification method, controller, service endpoint | VC와 DID 역할 혼동 |
| 적용 리스크 인식 확인 | 키 회전, 메서드 선택, privacy by design | DID Document에 개인정보 저장 전제 |
> 요약: 이 문제는 DID를 분산 신원 식별 계층으로 설명하고, 메서드 선택과 키 관리 리스크를 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 주체 제어 분산 식별자
- 배경: 중앙 IdP 식별자는 제공자 정책, 계정 종속, 서비스 간 추적 가능성을 만들고 서비스 장애가 신원 확인 실패로 이어질 수 있다.
- 필요성: W3C DID Core는 DID Document의 공개키와 서비스 엔드포인트를 통해 VC 서명 검증과 지갑 기반 신원 교환 기준을 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
DID URI -> DID Method -> DID Resolver -> DID Document
             +-> Verification Method
             +-> Controller / Service Endpoint / Key Rotation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| DID Syntax | `did:method:specific-id` 식별자 형식 정의 | W3C DID Core v1.0 기반 |
| DID Method | 생성·해석·갱신·폐기 규칙 정의 | did:web, did:key, did:ion |
| DID Resolver | DID를 DID Document로 변환 | method driver 신뢰 필요 |
| DID Document | 공개키, controller, service 제공 | 개인정보 직접 기재 금지 |
| Verification Method | 서명 검증용 공개키와 인증 관계 | authentication, assertionMethod |
> 요약: DID 표준은 식별자 형식, 메서드 규칙, 해석기, DID 문서, 검증 메서드로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
DID 생성 -> DID Document 게시 -> Resolver 조회
-> 공개키/인증 메서드 추출 -> 서명 검증 -> 키 회전/폐기 반영
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 주체가 DID와 키쌍 생성 | method-specific-id 충돌 방지 |
| 2 | DID Document에 공개키·controller 등록 | 문서 무결성, service 최소화 |
| 3 | 검증자가 Resolver로 DID Document 조회 | resolver 응답 출처, 캐시 TTL |
| 4 | verification method로 서명 확인 | kid 매칭, 알고리즘 허용 목록 |
| 5 | 키 회전·폐기 상태 반영 | 이전 키 폐기, 갱신 로그 |
> 요약: DID 검증은 식별자 해석으로 공개키를 확보하고, 서명·키 상태·문서 무결성을 순차 확인하는 절차이다.

---

## Ⅳ. 특징

| 구분 | 중앙 식별자 | W3C DID | 정량·기술 포인트 |
|:---|:---|:---|:---|
| 제어권 | IdP·서비스 사업자 | DID controller | 키 회전 주기 90일 |
| 조회 방식 | 계정 DB, IdP API | DID Resolver, DID Document | resolver p95 300ms 이하 |
| 저장소 | 중앙 레지스트리 | DID Method별 저장소 | did:web, did:key, ledger |
| 개인정보 | 프로필 속성 결합 | 문서에 공개키 중심 기재 | 개인정보 필드 0개 목표 |
> 요약: DID는 식별자 제어와 공개키 확인을 분리하지만 DID Method와 Resolver 신뢰를 설계해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | W3C DID | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | IdP 계정, X.509 Subject | DID URI, DID Document | 사용자·기관·사물 식별자 독립성 필요 |
| 비용/성능 | 중앙 API 단순 조회 | resolver, method driver, 캐시 필요 | resolver p95 300ms, 가용성 99.9% |
| 운영/위험 | IdP 장애·계정 종속 | method 폐쇄, 키 분실, 문서 노출 | method governance, recovery plan |
> 요약: DID는 장기 식별자와 공개키 검증 독립성이 필요할 때 적합하고, 내부 계정 관리는 기존 IAM이 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 메서드 종속 | 특정 ledger·도메인 정책 의존 | did:web+did:key 이중 전략, export 절차 | method 전환 테스트 100% |
| 키 노출 | 개인키 유출, 회전 절차 부재 | HSM/TEE, 키 회전 90일, 폐기 로그 | 노출 신고 후 폐기 30분 이하 |
| 개인정보 노출 | DID Document에 속성 기재 | 공개키·service 최소 기재, pairwise DID | 문서 개인정보 필드 0개 |
> 요약: DID 리스크는 메서드 거버넌스, 키 회전, 문서 최소화를 지표로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 해석 품질 | resolver p95 300ms, 오류율 1% 이하 | resolver 로그, APM |
| 키 운영 | 키 회전 90일, 폐기 반영 30분 이하 | KMS/HSM 로그 |
| 프라이버시 | DID Document 개인정보 0개, pairwise DID 적용률 90% | 문서 스캔, DPIA |
> 요약: DID 도입 평가는 resolver 지연, 키 회전 이행, 공개 문서 개인정보 노출 여부로 수행한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Method 선정: 공공·기업은 did:web, 오프라인·임시 증명은 did:key, 대규모 공개 레지스트리는 governance 검토 후 ledger DID 적용
2. Resolver 운영: 허용 method whitelist, 캐시 TTL 10분, resolver p95 300ms, 장애 시 보조 resolver 전환 절차 수립
3. 키·문서 통제: KMS/HSM 연계, 키 회전 90일, DID Document 개인정보 0개, service endpoint 접근 로그 보존 1년 적용

**결론 (2줄):**
- 기술사 판단: DID는 VC 검증과 장기 식별자 제어가 필요한 경우 적용하고, 단일 조직 계정 인증은 OIDC·SAML 기반 IAM을 우선한다.
- 향후 방향: W3C DID Core, VC 2.0, OID4VC가 결합되어 지갑 기반 신원 교환의 상호운용 계층으로 정착한다.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DID 표준을 설명하시오" | DID 생성, resolver 조회, 공개키 검증 흐름 | 중앙 식별자 대비 제어권·조회 방식 차이 |
| 요구사항 명시형 | "설계하시오", "비교하시오" | Method 선정, resolver 캐시, 키 회전 설계 | method 종속, 개인정보 노출, 운영 지표 |
> 요약: 설명형은 DID 표준 구성, 설계형은 메서드·해석기·키 운영 통제를 중심으로 목차를 전환한다.
