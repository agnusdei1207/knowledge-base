---
sidebar:
  order: 107
  label: "107. 글로벌 CDN 아키텍처"
  badge:
    text: "미출 · 50%"
    variant: note
title: "글로벌 엣지 콘텐츠 분산 전송 : CDN 아키텍처"
date: "2026-08-25T12:00:00+09:00"
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

- 정의/개념: BGP Anycast 라우팅과 분산 엣지 PoP를 통해 **원본 서버의 콘텐츠를 사용자 최근접 위치에서 캐싱·전송하는 글로벌 분산 네트워크 인프라**
- 배경/필요성: 중앙 원본 서버 직접 접속 시의 **대륙 간 RTT 지연 폭증, 트래픽 폭주 시 원본 서버 마비 및 네트워크 대역폭 비용 과다**

#### 한줄 요약
- BGP Anycast와 계층형 엣지 캐싱을 통해 초저지연 전송과 원본 서버 부하 보호를 달성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Anycast BGP Routing**: 전 세계 모든 PoP가 동일한 단일 IP를 BGP로 광고하여 사용자가 물리적/네트워크적으로 가장 가까운 PoP로 자동 연결되는 기술.
- **Request Collapsing (요청 병합)**: 동일 객체에 대한 동시 다발적인 캐시 미스 요청을 1건으로 묶어 원본에 질의하는 부하 방지 기법.

</details>

- **BGP Anycast 기반 최단 엣지 연결**: 사용자를 지리적으로 가장 가까운 **PoP로 자동 유입시켜 네트워크 RTT 극소화**
- **계층형 다단 캐싱(Tiered Caching)**: L1 엣지 PoP와 L2 오리진 쉴드를 결합하여 **캐시 적중률(Cache Hit Ratio) 98% 이상 달성**
- **동적 가속 및 엣지 컴퓨팅**: 단순 캐싱을 넘어 **TCP 최적화, HTTP/3 QUIC 종단 및 V8 서버리스 연산 직접 수행**

#### 한줄 요약
- Anycast 최단 라우팅, 계층형 캐싱을 통한 원본 보호, 엣지 서버리스 연산을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Edge PoP vs Origin Shield**: 사용자와 직접 통신하며 L1 캐시를 서빙하는 Edge PoP와 전역 미스 트래픽을 집약하는 L2 Origin Shield.

</details>

```text
[글로벌 계층형 CDN 전송 아키텍처]
|-- Global Users (전 세계 클라이언트 브라우저 및 앱)
`-- Anycast Edge PoPs (Tier 1: 최단 PoP 연결, TLS 1.3/QUIC 종단, L1 NVMe 캐시 서빙)
    `-- Cache Miss 발생 시
`-- Origin Shield / Tiered Regional Cache (Tier 2: 전역 미스 요청 병합 Request Collapsing)
    `-- 병합된 단 1건의 원본 재검증 질의
`-- Origin Server Infrastructure (고객 중앙 원본 서버: Web/WAS/DB)
```

선의 의미: 사용자 요청이 최단 엣지 PoP에서 L1 캐시 처리되고 캐시 미스 시 오리진 쉴드에서 병합된 후 원본 서버로 단 1회 질의되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **Anycast BGP 라우터** | 전 세계 단일 Anycast IP를 통해 **최단 네트워크 경로 상의 엣지 PoP로 패킷 유입** | Network Layer |
| **엣지 캐시 노드 (Edge PoP)**| L7 프록시, TLS 종단, **L1 캐시 서빙, WAF 룰 검사 및 압축(Brotli) 전송** | L1 Cache / Envoy |
| **오리진 쉴드 (Origin Shield)**| 전역 엣지 노드의 미스 트래픽을 **중앙에서 집약하고 요청 병합(Collapsing) 수행** | Tiered Cache |
| **캐시 무효화 엔진 (Purge)**| API 호출 즉시 **150ms 내에 전 세계 엣지 노드의 만료 객체를 일괄 무효화** | Fast Purge |
| **동적 콘텐츠 최적화기** | 캐시 불가 트래픽을 **전용 백본망(TCP 최적화)으로 원본까지 고속 프록시** | Dynamic Routing |

#### 한줄 요약
- Anycast 라우터, 엣지 PoP, 오리진 쉴드, 캐시 무효화 엔진, 동적 최적화기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Stale-While-Revalidate (RFC 5861)**: 백그라운드에서 원본과 캐시를 재검증하는 동안 클라이언트에게는 만료된 캐시를 즉시 반환하여 0ms 응답을 보장하는 지시자.

</details>

```text
CDN Anycast 인입, L1 캐시 판정 및 오리진 쉴드 병합 파이프라인
        │
   1. [Anycast 최단 PoP 인입] BGP Anycast에 의해 가장 가까운 엣지 PoP로 인입 및 TLS 1.3 즉각 종단
        │
   2. [L1 캐시 키 해시 검색] 엣지 PoP가 캐시 키를 조회하여 L1 NVMe 캐시 스토리지 검색
        │
   ├─ [Cache Hit 시] ➔ 5ms 이내에 압축 콘텐츠를 사용자에게 즉시 응답
   ▼
3. [Cache Miss 발생] ➔ 오리진 쉴드로 요청 전달 ➔ 동일 URL 동시 요청들을 단 1건으로 병합(Collapsing)
        │
   4. [조건부 원본 질의] 오리진 쉴드가 원본 서버로 조건부 요청(If-None-Match) 전송
        │
   ▼
5. [계층형 캐시 동기화] 최신 객체를 수신하여 오리진 쉴드 및 엣지 PoP에 캐싱 후 클라이언트에 최종 반환
```

#### 한줄 요약
- Anycast 최단 PoP 접속 → TLS 종단 → L1 캐시 판정 → 오리진 쉴드 요청 병합 → 원본 재검증 반환 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Legacy CDN** vs **Programmable Edge CDN**.

</details>

| 비교 항목 | 전통적 정적 CDN (Legacy CDN) | 차세대 엣지 컴퓨팅 CDN (Programmable CDN) |
|:---|:---|:---|
| **주요 역할** | **정적 에셋(이미지, JS, CSS, 비디오) 단순 캐싱**| **정적 캐싱 + 엣지 서버리스 연산 (V8 Workers)** |
| **라우팅 메커니즘** | DNS 기반 Geo-IP 라우팅 (느린 페일오버) | **BGP Anycast 전역 단일 IP (초고속 자동 우회)** |
| **캐시 무효화 속도**| 수 분 ~ 수십 분 소요 (전역 전파 지연) | **150밀리초($\le 150\text{ms}$) 즉시 전역 무효화** |
| **동적 콘텐츠 처리**| 원본 서버로 바이패스 프록시 전달만 수행 | **엣지에서 A/B 테스팅, JWT 인증, 개인화 직접 수행** |
| **대표 플랫폼** | Akamai, Traditional CloudFront | **Cloudflare Workers, Fastly Compute@Edge** |

#### 한줄 요약
- 레거시 CDN은 정적 파일 캐싱에 집중하며, 차세대 엣지 CDN은 Anycast와 엣지 컴퓨팅 연산을 융합한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cache Stampede (캐시 스탬피드)**: 인기 콘텐츠 만료 순간 수만 건의 동시 요청이 원본으로 직격하여 원본 서버를 다운시키는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 개인화된 민감 사용자 정보가 공용 엣지에 캐싱되어 타인에게 유출 | **`Cache-Control: private, no-store` 명시 및 Set-Cookie 포함 시 캐시 제외** | 공유 캐시 개인정보 유출 원천 차단 및 규제 준수 |
| 신규 배포 후 엣지 캐시의 구버전 잔존으로 인한 웹 UI 깨짐 | **빌드 시 파일명 해싱(`app.[hash].js`) 적용 및 Fast Purge API 연동** | 배포 즉시 100% 최신 버전 반영 및 정적 에셋 무한 캐싱 |
| 인기 콘텐츠 만료 순간 수만 건의 요청이 원본으로 몰리는 **캐시 스탬피드** | **`오리진 쉴드 요청 병합(Request Collapsing)` 및 `stale-while-revalidate`** | 원본 부하 99% 절감 및 트래픽 스파이크 시 무중단 서빙 |
| CDN 캐시 키 조작을 통한 악성 스크립트 유포 (캐시 포이즈닝) | **비표준 HTTP 헤더(X-Forwarded-Host 등)의 캐시 키 포함 금지** | 캐시 오염 공격 무력화 및 웹 콘텐츠 무결성 보증 |

#### 한줄 요약
- Cache-Control로 정보 유출을 막고, 파일명 해싱으로 최신성을 보장하며, 요청 병합으로 캐시 스탬피드를 방어한다.

## Ⅶ. 결론

- 글로벌 비즈니스의 사용자 경험(UX) 극대화와 인프라 가용성을 보장하기 위해 **글로벌 CDN 아키텍처를 필수 엣지 전송 계층으로 구축**하되, 실무 적용 시 **Anycast BGP 기반 고탄력 라우팅, 오리진 쉴드 계층화, RFC 9111 기반 정밀 캐시 거버넌스, 엣지 서버리스 컴퓨팅 및 보안(WAF/DDoS) 통합**을 구현하여 완결성 높은 고성능 엣지 인프라 완성

#### 한줄 요약
- CDN 아키텍처는 BGP Anycast 라우팅과 계층형 엣지 캐싱 및 오리진 쉴드를 결합하여 글로벌 초저지연 콘텐츠 전송을 보장하는 인프라다.