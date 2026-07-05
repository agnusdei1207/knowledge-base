---
title: "W3C DID 표준 (Decentralized Identifier Standard)"
date: "2026-07-05"
tags:
  - "cspe-security"
weight: 112
---

## Ⅰ. 개요
- **정의**: 중앙 기관 없이 사용자가 스스로 생성·관리할 수 있는 글로벌 고유 식별자 체계 표준임
- **배경/필요성**: 기존 ID 체계(이메일, 주민번호)는 발급 기관에 종속되어 자기주권 신원관리가 불가능하므로 탈중앙 식별자가 필요함
- **비유**: 이름표를 학교가 만들어주는 대신, 본인이 직접 만들고 공증소에 등록해두는 것과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DID 구조와 Resolution 메커니즘 이해 | DID Document에 공개키·서비스 엔드포인트 포함 | DID Method별 원장 차이 구분 |

> 요약: DID는 중앙 의존 없이 사용자가 자체 생성하고 분산 원장에 등록하는 글로벌 식별자 표준임

## Ⅱ. 구성요소
```text
DID Subject --> DID --> DID Document
                 |           |
            did:method:id   +-- publicKey
                            +-- authentication
                            +-- serviceEndpoint
                            |
                       DID Registry (분산 원장)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| DID | `did:method:specific-id` 형식의 URI 기반 고유 식별자 | 자체 발급 여권 번호 |
| DID Document | 공개키, 인증 방식, 서비스 엔드포인트를 포함하는 JSON-LD 문서 | 여권 내 인적사항 페이지 |
| DID Method | DID 생성·조회·갱신·비활성화 규칙을 정의하는 구현 명세 | 여권 발급 규정 |
| DID Resolver | DID를 입력받아 DID Document를 반환하는 조회 서비스 | 여권 진위 조회 시스템 |
| DID Registry | DID Document가 저장되는 분산 원장 또는 저장소 | 공증 기록 보관소 |

> 요약: DID는 URI 형식 식별자이며 DID Document와 Registry, Resolver로 탈중앙 식별 체계를 구성함

## Ⅲ. 절차
```text
키쌍 생성 -> DID 생성 -> DID Document 등록 -> DID Resolution
```
- 1단계: 사용자가 공개키-개인키 쌍을 로컬에서 생성함
- 2단계: 선택한 DID Method 규칙에 따라 `did:method:specific-id` 형식의 DID를 생성함
- 3단계: 공개키와 서비스 엔드포인트를 포함한 DID Document를 DID Registry에 등록함
- 4단계: 검증자가 DID Resolver를 통해 DID를 조회하고 DID Document의 공개키로 서명을 검증함

> 요약: 키쌍 생성, DID 생성, Document 등록, Resolution 조회의 4단계로 탈중앙 식별이 완료됨

## Ⅳ. 문제점
- DID Method 난립: 150개 이상의 Method가 존재하여 상호운용성 확보가 어려움
- 키 복구 불가: 개인키 분실 시 DID에 대한 통제권을 영구적으로 상실할 수 있음
- 원장 의존성: 블록체인 기반 DID는 트랜잭션 비용과 확장성 제약이 존재함

> 요약: Method 파편화, 키 복구 한계, 원장 확장성이 DID 보급의 주요 과제임

## Ⅴ. 개선방안
1. 단기: did:web, did:key 등 경량 Method를 우선 도입하여 블록체인 의존도를 낮춤
2. 중기: Key Recovery 프로토콜(Social Recovery, 다중서명)을 DID Method 명세에 내장함
3. 장기: W3C DID WG에서 Universal Resolver 표준화를 통해 Method 간 호환성을 확보함

> 요약: 경량 Method 도입, 키 복구 표준화, Universal Resolver로 DID 생태계를 통합해야 함

## Ⅵ. 전망
- 발전 방향: VC(111 참조)와 결합하여 공공·민간 디지털 신원 인프라의 기반 기술로 확산될 전망임
- 기술사적 판단: DID는 자기주권 신원(SSI) 패러다임 전환의 핵심 축으로 정착할 것임
- 기술사 제언: 조직은 DID Method 선정 시 거버넌스 모델과 규제 준수 요건을 함께 검토해야 함
