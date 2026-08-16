---
sidebar:
  order: 155
  label: "155. 쿠버네티스 서비스•인그레스 (Kubernetes Service Ingress)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "쿠버네티스 서비스•인그레스 (Kubernetes Service Ingress)"
date: "2026-08-14T02:12:00+09:00"
tags:
  - "notes-software"
weight: 155
extra:
  question_no: "155"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "서비스 노출과 경로 제어가 최근 설계축임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **쿠버네티스 서비스(Kubernetes Service)**: IP가 수시로 변경되는 파드(Pod)들에 단일 가상 IP(VIP)를 부여하여 로드밸런싱 및 서비스 디스커버리(Service Discovery)를 제공하는 객체.
- **쿠버네티스 인그레스(Kubernetes Ingress)**: 외부 HTTP/HTTPS 트래픽을 도메인 및 경로(URL Path) 기반으로 백엔드 서비스로 분기 라우팅하는 L7 계층 로드밸런서.
- **인그레스 컨트롤러(Ingress Controller)**: 인그레스(Ingress) 규칙을 감지하여 NGINX나 AWS ALB 등 실체 엔진의 설정을 변경하고 TLS(Transport Layer Security) 인증서 처리를 수행하는 엔진.

</details>

- 정의/개념: Pod 접점을 제공하는 **Service•Ingress** Network 객체
- 배경/필요성: 가변 Pod IP 직접 호출은 **발견•외부 노출•경로 분기** 곤란

#### 한줄 요약

- 파드가 교체돼 주소가 바뀌어도 서비스라는 대표번호는 유지되고 Ingress는 외부 요청의 주소와 경로를 보고 대표번호를 선택한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Service Types**: ClusterIP(내부 전용 VIP), NodePort(노드 포트 오픈), LoadBalancer(CSP 클라우드 ELB 연동), ExternalName(외부 CNAME 맵핑).

</details>

- **서비스**: ClusterIP, NodePort, LoadBalancer, ExternalName 4대 노출 옵션 제공.
- **인그레스**: L7 경로 기반 분기(URL Path) 및 호스트 기반 라우팅 제공.
- **TLS 종료(TLS Termination)**: cert-manager 기반 SSL/TLS 인증서 자동 관리 및 종료 처리.

#### 한줄 요약

- 서비스는 준비된 파드 목록을 한 주소 뒤에 모으고 인그레스 컨트롤러는 선언된 웹 규칙을 실제 프록시 설정으로 바꾼다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **kube-proxy & iptables/IPVS**: kube-proxy가 Node마다 상주하며 Service Virtual IP로 유입된 L4 패킷을 실제 Pod IP로 iptables/IPVS 환원 라우팅.

</details>

```text
[외부 Client] ─── [Ingress•Controller]
                         │
                    [Service]
                    ┌────┴────┐
                  [Pod A]   [Pod B]
```

| 구성요소 | 책임 |
|---|---|
| 외부 Client | **Host•Path 요청**과 TLS Session 생성 |
| Ingress•Controller | Ingress 규칙을 **L7 Proxy 설정**으로 구현 |
| Service | 안정된 **VIP•DNS**와 Endpoint 집합 제공 |
| Pod | Readiness를 통과한 **Application Process** 실행 |

#### 한줄 요약

- DNS와 인증서가 건물 이름과 신분을 보장하면 인그레스가 안내하고 서비스가 준비된 파드 중 한 곳으로 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Path-based Routing**: `app.com/api` $\rightarrow$ API Service 로, `app.com/pay` $\rightarrow$ Pay Service 로 L7 URL 경로 분기 처리.

</details>

```text
[HTTPS 요청]
     │
     ▼
1. TLS 종료•Host 확인
     │
     ▼
2. Path Rule 대조
     │
     ▼
3. Service 선택
     │
     ▼
4. 준비 Endpoint 선택
     │
     ▼
5. Pod로 전달
     │
     ▼
[HTTP 응답]
```

### 동작 원리

1. **TLS 종료•Host 확인**: 인증서와 요청 Domain 검증
2. **Path Rule 대조**: Host•URL에 맞는 Ingress Rule 선택
3. **Service 선택**: Rule이 가리키는 Backend Service 확인
4. **준비 Endpoint 선택**: Readiness 통과 Pod 중 대상 결정
5. **Pod로 전달**: 선택 Endpoint에 요청 전달

#### 한줄 요약

- 외부 요청은 인그레스에서 호스트와 경로로 서비스가 정해지고 그 서비스의 준비된 파드에만 전달된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ClusterIP vs NodePort vs LoadBalancer**: ClusterIP는 클러스터 내부용, NodePort는 노드 IP:Port 개방, LoadBalancer는 Cloud ELB 맵핑.

</details>

| Service 타입 | 네트워크 노출 범위 | 주요 용도 및 특징 |
|:---|:---|:---|
| **ClusterIP (기본값)** | **클러스터 내부 접점** | 내부 Service Discovery와 통신 |
| **NodePort** | **모든 Node의 동일 포트(30000~32767) 개방**| 온프레미스 노드 테스트, 간단한 외부 노출 |
| **LoadBalancer** | **AWS/Azure Cloud 외부 ELB 자동 프로비저닝**| 대국민 운영 서비스 L4 노출 표준 |
| **ExternalName** | **외부 DNS CNAME 맵핑 제공** | 외부 오라클 DB를 서비스 이름으로 내부 연동 |

#### 한줄 요약

- 서비스는 파드 교체를 숨기는 내부 접점이고 Ingress는 여러 접점을 하나의 외부 주소와 인증서 뒤에 배치하는 규칙이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **AWS ALB Ingress Controller Target-Type**: `instance` 방식(NodePort 경유) 대신 `ip` 방식(Pod IP 직접 타겟팅)으로 설정하여 L4 노드포트 병목 레이턴시 50% 절감.

</details>

| 3대 네트워크 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Extra Node Hop Latency** | ALB $\rightarrow$ NodePort $\rightarrow$ Pod 2번 점프 | **ALB target-type: ip 로 Pod 직접 타겟팅 튜닝** |
| **2. ELB Cost Surge** | Service 20개마다 LoadBalancer 생성해 비용 폭발| **Ingress 1개로 통합하고 Path-based 라우팅** |
| **3. SSL Certificate Expire**| HTTPS SSL 인증서 만료로 접속 장애 | **cert-manager 연동 Let's Encrypt 자동 갱신** |

> 사례: **카카오 / 당근마켓 / 쿠팡 AWS ALB Ingress Controller & cert-manager 기반 L7 트래픽 통합**

#### 한줄 요약

- 배포 중 파드가 바뀌어도 내부 호출은 서비스 이름을 사용하고 준비 해제와 연결 배출을 묶어 기존 요청이 끝날 시간을 확보해야 한다.

## Ⅶ. 결론

- 내부 L4 접점은 **Service**, 외부 HTTP 분기는 Ingress 선택

#### 한줄 요약

- 파드 집합의 안정된 내부 주소는 서비스로, 웹 경로와 인증서 통합은 Ingress로 제공한다.
