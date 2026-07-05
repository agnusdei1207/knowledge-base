---
title: "112. W3C DID 표준 (W3C DID Standard)"
date: 2026-07-05
tags: [cspe-security]
weight: 112
---

## Ⅰ. 개요
| 항목 | 내용 |
|---|---|
| **정의** | W3C가 정의한 분산 식별자(Decentralized Identifier) 표준으로, 중앙 기관 없이 사용자가 자신의 식별자를 생성·소유·제어하는 URI 체계임 |
| **배경/필요성** | 기존 식별자(이메일·전화번호)는 중앙 서비스에 종속되어 사용자 통제가 불가하며, 자기주권 기반 탈중앙 식별자가 필요함 |
| **출제 의도** | DID Document의 구조와 DID Method의 다양성·해석(Resolution) 과정을 이해하는지 평가함 |

## Ⅱ. 구성요소
```
+----------+     +----------+     +----------+
|   DID    | --> |  DID     | --> | Verifiable|
| (식별자) |     | Document |     | Data Reg |
+----------+     +----------+     +----------+
```

| 구성요소 | 설명 | 비유 |
|---|---|---|
| DID | `did:method:specific-id` 형식의 URI로, 특정 Method에 의해 해석됨 | 전 세계 고유 여권 번호 |
| DID Document | 공개키·인증 방법·서비스 엔드포인트를 포함하는 JSON-LD 문서임 | 여권 내 인적사항 페이지 |
| VDR | DID Document를 저장하는 분산 원장·블록체인·웹 서버 등 검증 가능한 데이터 레지스트리임 | 여권 발급 기관의 원본 DB |

> 요약: DID(식별자) → DID Document(공개키·메타데이터) → VDR(저장·해석)로 탈중앙 식별을 구현함.

## Ⅲ. 절차
```
+------------+     +------------+
| DID생성    | --> | Document  |
| (키쌍생성) |     | VDR등록   |
+------------+     +------------+
                        |
+------------+     +----+-------+
| 공개키획득  | <-- | DID해석   |
| 서명검증   |     | (Resolve) |
+------------+     +------------+
```

1. DID 생성: 사용자가 키쌍을 생성하고 DID Method 규칙에 따라 DID를 구성함
2. Document 등록: DID Document(공개키·서비스 엔드포인트)를 VDR에 등록함
3. DID 해석(Resolution): 검증자가 DID를 Universal Resolver에 전달하여 DID Document를 조회함
4. 서명 검증: DID Document의 공개키로 VC·VP의 서명을 검증하여 신원을 확인함

> 요약: 생성 → 등록 → 해석 → 검증으로 중앙 기관 없이 식별자 기반 신원 확인을 수행함.

## Ⅳ. 문제점
- Method 파편화: did:web·did:ion·did:ethr 등 50+개 Method가 난립하여 상호운용성이 부족함
- 키 회전 복잡성: DID Document의 키를 업데이트할 때 기존 서명 검증과의 호환이 어려움
- 분산 원장 의존: 블록체인 기반 VDR은 비용·성능·환경 문제가 있음

## Ⅴ. 개선방안
- (단기) did:web 활용: 기존 웹 인프라를 활용하는 did:web으로 블록체인 의존을 줄임
- (중기) Universal Resolver: 다양한 DID Method를 통합 해석하는 표준 리졸버를 보급함
- (장기) DID Method 통합: W3C·DIF 주도로 핵심 Method를 표준화하여 파편화를 해소함

## Ⅵ. 전망
- W3C DID 1.0이 정식 권고안(Recommendation)으로 채택되며, EU eIDAS 2.0·국내 DID 프레임워크와 연계하여 글로벌 디지털 신원의 기반 표준이 될 전망임
