---
title: "서비스 디스커버리 (Service Discovery)"
date: "2026-07-04"
tags:
  - "cspe-software"
weight: 213
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: 마이크로서비스 환경에서 동적으로 변경되는 서비스 인스턴스의 네트워크 위치(IP, 포트)를 자동으로 찾아주는 메커니즘
- **왜 필요한가**: 클라우드와 컨테이너 환경에서는 인스턴스가 수시로 생성·소멸하여 IP 주소가 계속 변하므로, 하드코딩된 IP로는 서비스 간 호출이 불가능하기 때문
- **핵심 직관**: 114 전화번호부. 친구 이사(IP 변경) 갈 때마다 내 수첩(하드코딩)을 고치는 대신, 114(서비스 레지스트리)에 물어봐서 현재 주소를 알아낸다.

## 핵심 용어 정리

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| Service Registry | 모든 서비스 인스턴스의 현재 위치 정보를 저장하는 중앙 데이터베이스 | 114 전화번호부, Eureka, Consul |
| Client-Side Discovery | 클라이언트가 레지스트리에서 주소를 받아 직접 로드밸런싱하여 호출 | "내가 번호부 보고 직접 찾아갈게" |
| Server-Side Discovery | 클라이언트가 로드밸런서(API Gateway)로 요청하면, 로드밸런서가 주소를 찾아 라우팅 | "프론트 데스크에 말하면 연결해줌" |

## 깊이 이해
- **배경·문제의식**: 레거시 환경에서는 서버 IP가 고정되어 L4/L7 스위치나 DNS로 충분했다. MSA 및 Auto-Scaling 환경에서는 인스턴스의 IP 동적 할당되며 수명이 짧아 기존 방식으로는 라우팅 최신화가 불가능하다.
- **작동 원리**:
  1. **등록(Registration)**: 서비스가 구동되면 자신의 위치(IP/Port)를 Service Registry에 등록한다 (주기적 Heartbeat 전송).
  2. **조회(Discovery)**: 다른 서비스(클라이언트)가 API를 호출할 때 Registry를 조회하여 사용 가능한 인스턴스 목록을 얻는다.
  3. **해제(Deregistration)**: 서비스가 종료되거나 Heartbeat가 끊기면 Registry에서 삭제된다.
- **비유**: 배달 기사가 식당을 찾을 때, 식당이 매일 자리를 옮기는 푸드트럭이다. 푸드트럭이 본부에 '나 오늘 여기 있음' 등록(Heartbeat)하고, 기사는 본부 앱(Registry)을 보고 찾아간다.
- **구체 예시**: Spring Cloud Eureka를 사용하면 각 마이크로서비스가 30초마다 Eureka Server에 Heartbeat를 보낸다. 클라이언트(FeignClient)는 이 목록을 캐싱하여 라운드 로빈으로 호출한다.
- **흔한 오해·주의점**: 서비스 디스커버리가 완벽한 실시간일 수는 없다. 인스턴스가 비정상 종료된 후 Registry가 이를 감지하기 전(수십 초)까지는 클라이언트가 잘못된 IP로 요청할 수 있으므로 재시도(Retry) 로직이 반드시 병행되어야 한다.

## 연결 개념
- 마이크로서비스 아키텍처 MSA
- 로드 밸런싱 전략 (Load Balancing)
- 쿠버네티스 서비스·인그레스 (Kubernetes Service)

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 동적 인프라 환경에서 마이크로서비스 간의 통신을 위해 인스턴스의 네트워크 주소를 등록하고 조회하는 라우팅 메커니즘이다.
> 2. **가치**: 인스턴스의 Auto-Scaling 및 장애 복구에 따른 IP 변동을 애플리케이션 계층에서 투명하게 처리하여 고가용성과 확장성을 확보한다.
> 3. **판단 포인트**: 클라이언트 언어 종속성이 강한 Client-Side 방식과, 인프라 중심의 Server-Side(Kubernetes 등) 방식 중 환경에 맞는 패턴을 선택해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 동적 인프라 라우팅 문제 해결 역량 | Service Registry, Heartbeat, 등록/조회 흐름 | 단순 DNS 라우팅과의 차이점 누락 |
| 디스커버리 패턴의 트레이드오프 판별 | Client-Side vs Server-Side Discovery 비교 | 쿠버네티스 환경(Server-Side)의 대세 흐름 간과 |

> 요약: 정적 IP 환경의 한계를 짚고, 동적 등록·조회 메커니즘과 패턴별(클라이언트 vs 서버) 선택 기준을 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 클라우드 및 MSA 환경에서 동적으로 할당되는 마이크로서비스 인스턴스의 네트워크 위치를 자동으로 등록·관리·조회하는 기술
- 배경: Auto-Scaling, 컨테이너화로 인해 서비스 IP가 빈번히 변경되어 정적(Static) 환경의 DNS/L4 기반 라우팅 한계 직면
- 필요성: 서비스 간 결합도 최소화, 무중단 배포 및 확장성 지원, 장애 인스턴스 자동 격리

---

## Ⅱ. 구조 및 구성요소

```text
Service Provider -> (등록/Heartbeat) -> Service Registry
                                           ^
Service Consumer -> (위치 조회 및 캐싱) ----+
         |
         +-> (직접 호출) -> Service Provider 인스턴스
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Service Registry | 서비스 인스턴스의 상태(Health) 및 네트워크 정보 중앙 저장소 | 고가용성 구성 필수 (Eureka, Consul, Zookeeper) |
| Registration | Provider 기동 시 자신의 정보를 Registry에 등록 | 주기적 Heartbeat로 활성 상태 증명 |
| Discovery Client | Consumer가 Registry를 조회하여 가용 인스턴스 목록 확보 | 병목 방지를 위해 클라이언트 로컬 캐싱 수행 |

> 요약: 디스커버리는 상태 저장소인 Registry를 중심으로, 서비스 제공자의 '등록'과 소비자의 '조회' 사이클로 동작한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
인스턴스 기동 -> Registry에 IP 등록 -> Heartbeat 전송 유지 -> Consumer가 IP 목록 조회 -> 라우팅 호출
```

- 1단계 [서비스 등록]: Service Provider가 부트스트랩 단계에서 Service Registry에 IP/Port 등록
- 2단계 [상태 갱신]: Provider는 TTL(Time To Live) 갱신을 위해 주기적 Heartbeat 전송
- 3단계 [위치 조회]: Service Consumer가 API 호출 전 Registry에서 가용 인스턴스 목록을 조회 및 캐싱
- 4단계 [로드밸런싱 및 호출]: Consumer 측 로드밸런서가 선택한 특정 인스턴스로 실제 트래픽 전송
- 5단계 [등록 해제]: 비정상 종료 시 Heartbeat 누락으로 Registry에서 인스턴스 정보 Eviction(퇴출)

> 요약: 등록과 헬스체크로 가용성을 유지하고, 클라이언트는 확보된 동적 목록을 기반으로 서비스를 호출한다.

---

## Ⅳ. 특징
- 유연한 확장성: 설정 파일(Config) 수정 없이 신규 인스턴스가 클러스터에 자동 합류 및 트래픽 분산
- 가용성 향상: 장애 발생 인스턴스를 즉각 감지하여 라우팅 풀에서 제외시켜 호출 실패 방지
- 단일 장애점 리스크: Service Registry 자체가 SPOF가 될 수 있어 클러스터링 기반 고가용성 구성 요구

> 요약: 인프라의 동적 변화를 애플리케이션 논리와 분리하지만, Registry 운영이라는 관리 비용이 추가된다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Client-Side Discovery | Server-Side Discovery | 선택 기준 |
|:---|:---|:---|:---|
| 라우팅 주체 | 클라이언트 내장 로드밸런서 | 인프라 로드밸런서 (API Gateway, Proxy) | 언어 종속성 수용 여부 |
| 언어/프레임워크 | 클라이언트마다 구현 로직 필요 | 애플리케이션과 무관하게 독립적 | 이기종 폴리글랏 환경 |
| 홉(Hop) 수 | 1-Hop (클라이언트 -> 인스턴스) | 2-Hop (클라이언트 -> 프록시 -> 인스턴스) | 네트워크 지연 민감도 |
| 대표 솔루션 | Spring Cloud (Eureka) | AWS ELB, Kubernetes Service (Kube-proxy) | 클라우드 네이티브 성숙도 |

> 요약: 동일 프레임워크 락인 환경이면 Client-Side가 빠르지만, 이기종 마이크로서비스와 쿠버네티스 환경에서는 Server-Side가 표준이다.

**리스크·대응 (기본은 불릿):**
- Registry 장애 (SPOF): Registry 다운 시 전체 서비스 간 통신 마비 → Registry 노드 다중화(클러스터링) 및 클라이언트 로컬 캐시 사용 (지표: Registry 응답 지연)
- 헬스체크 딜레이 (Ghost Instance): 인스턴스 다운부터 Eviction까지의 간극 동안 호출 실패 발생 → 클라이언트 사이드 Retry/Circuit Breaker 결합 (지표: Connection Refused 오류 비율)
- 네트워크 파티션 (Split Brain): Registry 노드 간 통신 단절 시 데이터 불일치 발생 → CAP 정리 기반 가용성(AP) 모델(Eureka) 선택으로 라우팅 유지 (지표: 노드 간 동기화 지연)

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Kubernetes 네이티브 통합: 별도의 Eureka 서버 운영 대신, Kube-DNS와 Service 리소스를 활용한 Server-Side Discovery 기반 아키텍처 전환
2. 클라이언트 복원력 강화: Registry 캐시 갱신 지연 시 오작동을 막기 위해 FeignClient에 Resilience4j(Retry, Circuit Breaker) 필수 적용
3. Service Mesh 결합: Istio 등 서비스 메시를 도입하여 디스커버리와 로드밸런싱 기능을 사이드카 프록시로 완전히 위임(추상화)

**결론:**
- 기술사 판단: 과거 Spring Cloud 중심의 애플리케이션 레벨 디스커버리에서, 현재는 쿠버네티스와 서비스 메시 기반의 인프라 레벨 디스커버리로 아키텍처 패러다임이 진화하였다.
- 향후 방향: 클라우드 네이티브 환경에서는 단순 위치 조회를 넘어, 트래픽 가중치 기반 라우팅과 멀티 클러스터 디스커버리(Multi-Cluster Service)로 기능이 확장되고 있다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | Registry와 Heartbeat 작동 원리 | Client-side와 Server-side 비교 |
| 요구사항 명시형 | "설계 방안을 제시하시오" | 무중단 라우팅을 위한 동적 등록 절차 | Kubernetes 기반 적용 방안 및 Registry SPOF 해소 대책 |
