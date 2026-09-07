---
sidebar:
  order: 107
  label: "107. 글로벌 CDN 아키텍처"
  badge:
    text: "미출 · 50%"
    variant: note
title: "글로벌 엣지 콘텐츠 분산 전송 : CDN 아키텍처"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-network"
weight: 107
extra:
  question_no: "107"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "Anycast BGP / GeoDNS 라우팅, 계층형 엣지 캐싱(Edge PoP + Origin Shield), RFC 9111 HTTP 캐시 및 DDoS 완화"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **CDN (Content Delivery Network)**: 전 세계 분산 배치된 엣지 서버(Edge PoP)를 통해 원본 서버를 대신하여 사용자에게 초저지연 캐싱을 제공하는 네트워크.
- **Origin Shield (오리진 쉴드)**: 전 세계 PoP의 캐시 미스 트래픽을 중간에서 병합(Collapsing)하여 원본 서버의 부하를 보호하는 계층형 캐시.

</details>

- 정의/개념: BGP Anycast와 PoP로 **최근접 캐싱·전송**하는 분산망
- 배경/필요성: 글로벌 사용자에게 웹 서비스, 스트리밍 미디어, 대용량 정적 에셋 및 API를 제공할 때, 모든 트래픽을 단일 중앙 오리진(Origin) 서버로 집중시키는 구조는 물리적 거리에 따른 대륙 간 왕복 지연(RTT), 국제 인터넷 백본 혼잡 및 트래픽 폭증 시 오리진 서버 다운을 초래함에 따라, 전 세계 주요 거점에 분산 배치된 엣지(Edge PoP) 서버와 BGP Anycast 라우팅 및 계층형 캐싱(Edge + Origin Shield)을 결합한 CDN(Content Delivery Network) 아키텍처를 도입하여 **사용자 최단 거리 초저지연($\le 20ms$) 콘텐츠 서빙, 오리진 서버 부하 90% 이상 절감 및 글로벌 테라비트급 트래픽 폭증 흡수**를 달성할 필요

#### 한줄 요약
- BGP Anycast와 계층형 엣지 캐싱을 통해 초저지연 전송과 원본 서버 부하 보호를 달성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Anycast BGP Routing**: 전 세계 모든 PoP가 동일한 단일 IP를 BGP로 광고하여 사용자가 물리적/네트워크적으로 가장 가까운 PoP로 자동 연결되는 기술.
- **Request Collapsing (요청 병합)**: 동일 객체에 대한 동시 다발적인 캐시 미스 요청을 1건으로 묶어 원본에 질의하는 부하 방지 기법.

</details>

- **BGP Anycast**: 사용자를 최단 경로 PoP로 유입
- **계층형 캐싱**: PoP와 Origin Shield로 원본 부하 절감
- **엣지 컴퓨팅**: QUIC 종단·서버리스 연산 수행

#### 한줄 요약
- Anycast 최단 라우팅, 계층형 캐싱을 통한 원본 보호, 엣지 서버리스 연산을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Edge PoP vs Origin Shield**: 사용자와 직접 통신하며 L1 캐시를 서빙하는 Edge PoP와 전역 미스 트래픽을 집약하는 L2 Origin Shield.

</details>

```text
[글로벌 CDN 아키텍처]
  │
  ├─ [글로벌 라우팅 계층]
  │    ├─ Anycast BGP 라우터
  │    └─ GeoDNS 지능형 라우팅
  │
  ├─ [분산 캐시 패브릭]
  │    ├─ 엣지 PoP (L1 캐시)
  │    └─ 오리진 쉴드 (L2 캐시 병합)
  │
  └─ [제어 및 최적화]
       ├─ 전역 캐시 무효화 엔진
       └─ 동적 콘텐츠 최적화기
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| **Anycast BGP 라우터** | **최단 경로** PoP 유입 |
| **엣지 캐시 노드** | L1 캐시·**TLS·WAF** |
| **오리진 쉴드** | 미스 집약과 **요청 병합** |
| **캐시 무효화 엔진** | 전역 객체 **무효화** |
| **동적 콘텐츠 최적화기** | 전용 백본 **프록시** |

#### 한줄 요약
- 엣지 PoP가 사용자 앞의 1차 사본을, 오리진 쉴드가 전역 미스를 모으는 2차 사본을 맡으므로, 원본이 감당하는 요청 수는 PoP 수와 무관해진다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Stale-While-Revalidate (RFC 5861)**: 백그라운드에서 원본과 캐시를 재검증하는 동안 클라이언트에게는 만료된 캐시를 즉시 반환하여 0ms 응답을 보장하는 지시자.

</details>

```text
사용자 요청
    |
1. Anycast 최단 PoP 인입
    |
2. L1 캐시 검색
    +-- Hit: 즉시 응답
    |
3. 미스 요청 병합
    |
4. 조건부 원본 질의
    |
5. 계층형 캐시 동기화
    |
콘텐츠 응답
```

- 1. Anycast 최단 PoP 인입
- 2. L1 캐시 검색
- 3. 미스 요청 병합
- 4. 조건부 원본 질의
- 5. 계층형 캐시 동기화

#### 한줄 요약
- L1 캐시 적중과 미스에서 응답 경로가 갈리며, 미스는 요청 병합으로 원본 부하를 아끼는 대신 병합 대기 지연을 지불한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Legacy CDN** vs **Programmable Edge CDN**.

</details>

| 비교 항목 | 전통적 정적 CDN (Legacy CDN) | 차세대 엣지 컴퓨팅 CDN (Programmable CDN) |
|:---|:---|:---|
| 주요 역할 | **정적 에셋 캐싱** | **캐싱·서버리스 연산** |
| 라우팅 메커니즘 | Geo-IP DNS | **BGP Anycast** |
| 캐시 무효화 속도 | 수 분 이상 | **150ms 이하** |
| 동적 콘텐츠 처리 | 원본 프록시 | **A/B·JWT·개인화** |
| 대표 플랫폼 | Akamai·CloudFront | **Workers·Compute@Edge** |

#### 한줄 요약
- 레거시 CDN은 정적 파일 캐싱에 집중하며, 차세대 엣지 CDN은 Anycast와 엣지 컴퓨팅 연산을 융합한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cache Stampede (캐시 스탬피드)**: 인기 콘텐츠 만료 순간 수만 건의 동시 요청이 원본으로 직격하여 원본 서버를 다운시키는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 민감 정보의 공유 캐시 유출 | **private·no-store** | 개인정보 캐싱 차단 |
| 배포 후 구버전 캐시 잔존 | **파일명 해싱·Fast Purge** | 최신 버전 반영 |
| 만료 순간 캐시 스탬피드 | **Request Collapsing·SWR** | 원본 부하 절감 |
| 캐시 키 조작·포이즈닝 | **비표준 헤더 키 제외** | 콘텐츠 무결성 확보 |

#### 한줄 요약
- Cache-Control로 정보 유출을 막고, 파일명 해싱으로 최신성을 보장하며, 요청 병합으로 캐시 스탬피드를 방어한다.

## Ⅶ. 결론

- 단순한 정적 파일 캐싱 프록시를 넘어 전 세계 인터넷 트래픽의 80% 이상을 수용하며 웹 보안(WAF/DDoS)과 서버리스 연산을 현지에서 집행하는 **글로벌 엔터프라이즈 인터넷 인프라의 가장 핵심적인 분산 엣지 플랫폼**으로 확고히 자리매김하였으며, WebAssembly(WASM) 기반 엣지 컴퓨팅 및 QUIC/HTTP/3와의 결합으로 진화하는 가운데, 실무 CDN 아키텍처 설계 시에는 **인기 콘텐츠 만료 시 오리진 서버 다운을 방지하는 요청 병합(Request Collapsing) 및 Stale-While-Revalidate(RFC 5861) 전략 수립, 전 세계 PoP의 미스 트래픽을 집약하여 백엔드를 보호하는 계층형 오리진 쉴드(Origin Shield) 구축, 신규 배포 시 구버전 잔존을 방지하는 정적 자산 해시 네이밍 및 150ms 이내 초고속 전역 캐시 무효화(Fast Purge) 체계**를 결합하여 완벽한 글로벌 웹 서비스 가용성을 완성

#### 한줄 요약
- CDN 아키텍처는 BGP Anycast 라우팅과 계층형 엣지 캐싱 및 오리진 쉴드를 결합하여 글로벌 초저지연 콘텐츠 전송을 보장하는 인프라다.
