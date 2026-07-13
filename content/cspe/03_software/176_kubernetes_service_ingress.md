---
title: "쿠버네티스 서비스·인그레스 (Kubernetes Service Ingress)"
date: "2026-07-14T02:30:00+09:00"
tags:
  - "cspe-software"
weight: 176
extra:
  question_no: "176"
  exam_status: "기출"
  exam_history: "130회, 137회"
---

## 미리 알고가기

- Service는 교체되는 Pod 집합에 고정 IP·DNS·포트를 제공하는 네트워크 추상화임
- EndpointSlice는 Service가 전달할 준비된 Pod IP·포트를 분할 저장함
- ClusterIP는 클러스터 내부, NodePort는 노드 포트, LoadBalancer는 외부 로드밸런서로 노출함
- Ingress는 HTTP(S) 호스트·경로 규칙을 Service 백엔드에 연결하는 API 객체임
- Ingress Controller는 Ingress 객체를 감시해 프록시나 로드밸런서 설정으로 구현함
- Ingress 객체만 생성하면 트래픽 경로가 생기지 않으며 해당 IngressClass의 Controller가 필요함
- Gateway API는 역할별 객체로 HTTP와 확장 라우팅 구성을 분리하는 후속 네트워크 API임

## 작성 근거(검토용)

- Service와 Ingress는 모두 노출 기능이지만 계층·대상·규칙이 다르므로 고정 접근점과 L7 라우팅을 구분함
- 처리 계층·연결 구조·적합 조건의 정확히 3개 축으로 비교하고 실제 HTTP 전달 경로로 연결함
- 제목부터 결론까지 5회 전수 검수하여 Service 유형과 Ingress 역할의 중복 설명을 제거함

## Ⅰ. 개요

- **정의/개념**: Service는 Pod 집합의 고정 L4 접근점이고 Ingress는 HTTP(S) 호스트·경로를 Service에 연결하는 L7 규칙임
- **배경/필요성**: Pod IP 변경과 다중 웹 서비스의 외부 접근을 분리해 처리하기 위해 서비스 발견·라우팅 계층이 필요함

### 쉽게 이해하기 (학습용)
- Service는 변하는 Pod의 고정 접점이고 Ingress는 외부 웹 요청을 여러 Service로 나누는 규칙임

## Ⅱ. 특징

- Service selector와 EndpointSlice가 준비된 Pod 주소를 연결해 Pod 교체와 접근 주소를 분리함
- ClusterIP·NodePort·LoadBalancer·ExternalName으로 내부·외부 접근 범위를 구분함
- Ingress는 하나의 외부 접점에서 호스트·경로·TLS 규칙으로 여러 Service를 선택함
- Ingress API는 기능이 동결됐으며 새 라우팅 요구는 Gateway API와 Controller 지원을 검토함

### 쉽게 이해하기 (학습용)
- Service가 안정적인 내부 목적지를 만들고 Ingress Controller가 호스트·경로 규칙을 실제 프록시에 반영함

## Ⅲ. Service와 Ingress 비교

| 판단 기준 | Service | Ingress |
|:---|:---|:---|
| 처리 계층 | TCP·UDP·SCTP 포트 중심 접근 | HTTP(S) 호스트·URI 경로 중심 접근 |
| 연결 구조 | 가상 IP·포트를 EndpointSlice의 준비된 Pod로 전달 | Controller가 호스트·경로·TLS 규칙을 Service 백엔드로 전달 |
| 적합 조건 | 변하는 Pod 집합에 고정 접근점과 서비스 발견 필요 | 여러 HTTP(S) 서비스를 한 외부 접점에서 분기·TLS 종료 |

> 요약: Service는 Pod 집합의 고정 접근점이고 Ingress는 HTTP(S) 요청을 Service별로 분기함.

### 쉽게 이해하기 (학습용)
- Service는 내부 대표번호, Ingress는 외부 주소와 경로를 대표번호에 연결하는 안내 데스크와 비슷함

## Ⅳ. 구성요소 및 구조

| 구성요소 | 역할 |
|:---|:---|
| Service 객체 | selector·가상 IP·포트·노출 유형을 선언함 |
| EndpointSlice | Service가 사용할 준비된 백엔드 IP·포트를 제공함 |
| 서비스 데이터 경로 | 가상 IP나 노드 포트 트래픽을 백엔드로 전달함 |
| Ingress 객체 | 호스트·경로·TLS와 Service 백엔드를 선언함 |
| IngressClass·Controller | 규칙 담당 구현을 선택하고 프록시 설정으로 반영함 |
| Secret·DNS | TLS 인증서와 외부 호스트 이름을 제공함 |

```text
외부 요청 -> Ingress Controller -> Service -> EndpointSlice -> Ready Pod
내부 요청 -----------------------> Service -> EndpointSlice -> Ready Pod
```

> 요약: 외부 HTTP 요청은 Ingress를 거치고 내부 요청은 Service에서 Ready Pod로 전달됨.

### 쉽게 이해하기 (학습용)
- Ingress 규칙·Service·EndpointSlice가 외부 요청을 실제 준비된 Pod까지 연결함

## Ⅴ. HTTP 요청 전달 흐름

```text
DNS·외부 주소 -> TLS·호스트 확인 -> 경로 규칙 선택 -> Service 조회 -> Endpoint 선택 -> Pod 전달
```

1. **외부 접점 도착**: DNS가 Ingress Controller의 외부 주소를 반환함
2. **TLS·호스트 확인**: Controller가 인증서를 선택하고 HTTP Host를 규칙과 비교함
3. **경로 규칙 선택**: Host·Path가 일치하는 Service 이름과 포트를 찾음
4. **Service·Endpoint 조회**: Service에 연결된 준비 상태 EndpointSlice를 확인함
5. **Pod 전달**: 선택한 Pod IP·포트로 요청을 전달하고 응답을 반환함

> 요약: Ingress의 호스트·경로 판정 결과가 Service와 준비된 Pod 선택의 입력이 됨.

### 쉽게 이해하기 (학습용)
- 호스트와 경로를 고른 뒤 Service가 살아 있는 백엔드 중 하나로 요청을 전달함

## Ⅵ. 실무 사례

1. 내부 API는 ClusterIP와 EndpointSlice를 사용하고 준비 Endpoint 수·p99 지연을 확인함
2. 웹 서비스는 Ingress 호스트·경로를 분리하고 인증서 만료일·백엔드 5xx 비율을 확인함

### 쉽게 이해하기 (학습용)
- 내부 접근 안정성과 외부 웹 라우팅 품질은 서로 다른 계층의 지표로 확인함

## Ⅶ. 결론

- Pod의 고정 접근점은 Service로, HTTP(S) 외부 라우팅은 Ingress로 구성해야 함

### 쉽게 이해하기 (학습용)
- Service와 Ingress의 역할을 겹치게 보지 말고 내부 접점과 외부 웹 규칙으로 분리함
