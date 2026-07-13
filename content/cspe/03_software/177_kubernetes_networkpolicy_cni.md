---
title: "쿠버네티스 NetworkPolicy·CNI (Kubernetes NetworkPolicy CNI)"
date: "2026-07-14T02:30:00+09:00"
tags:
  - "cspe-software"
weight: 177
extra:
  question_no: "177"
  exam_status: "기출"
  exam_history: "127회, 130회, 137회"
---

## 미리 알고가기

- CNI는 런타임이 플러그인에 컨테이너 네트워크 ADD·DEL·CHECK를 요청하는 규약임
- CNI 플러그인은 Pod 네트워크 인터페이스·IP·경로를 구성함
- NetworkPolicy는 Pod selector와 peer·port 규칙으로 허용할 Ingress·Egress 트래픽을 선언함
- 선택된 Pod는 지정 방향에서 격리되고 여러 NetworkPolicy의 허용 규칙은 합집합으로 적용됨
- Pod 간 통신은 송신 Pod의 Egress와 수신 Pod의 Ingress 정책이 모두 허용해야 함
- NetworkPolicy API가 있어도 네트워크 플러그인이 정책을 구현하지 않으면 규칙은 적용되지 않음
- IPAM은 Pod 네트워크 주소를 할당·회수하고 중복 주소를 관리하는 기능임
- IPBlock은 NetworkPolicy가 CIDR 형식으로 허용할 외부 주소 범위를 지정함

## 작성 근거(검토용)

- CNI는 연결 생성 규약이고 NetworkPolicy는 허용 흐름 선언이므로 두 역할과 실행 시점을 분리함
- 핵심 목적·입력과 실행·실패 영향의 정확히 3개 축으로 비교하고 Pod 연결과 패킷 판정 흐름으로 연결함
- 제목부터 결론까지 5회 전수 검수하여 CNI와 NetworkPolicy를 같은 기능처럼 설명하지 않도록 교정함

## Ⅰ. 개요

- **정의/개념**: CNI는 Pod 연결 플러그인 규약이고 NetworkPolicy는 Pod 간 L3·L4 허용 트래픽을 선언하는 객체임
- **배경/필요성**: Pod에 연결성을 제공하면서 업무별 통신 범위를 제한하기 위해 네트워크 구성과 정책 집행 경계가 필요함

### 쉽게 이해하기 (학습용)
- CNI는 Pod에 통신 길을 만들고 NetworkPolicy는 그 길에서 허용할 통신 상대와 포트를 정함

## Ⅱ. 특징

- 런타임은 PodSandbox의 네트워크 네임스페이스를 만든 뒤 CNI ADD를 호출함
- CNI 플러그인은 인터페이스·IPAM·경로·노드 간 전달 경로를 구성함
- NetworkPolicy가 선택하지 않은 방향은 기본 허용이며 선택된 방향은 명시한 규칙만 허용됨
- 정책은 선언형 API이고 실제 패킷 필터링 방식은 CNI·네트워크 구현에 따라 달라짐

### 쉽게 이해하기 (학습용)
- 정책 객체를 작성해도 사용 중인 네트워크 구현이 이를 집행해야 실제 패킷이 제한됨

## Ⅲ. 역할 비교

| 판단 기준 | CNI | NetworkPolicy |
|:---|:---|:---|
| 핵심 목적 | Pod 네트워크 인터페이스·IP·경로를 연결·해제 | 선택된 Pod의 Ingress·Egress 허용 범위를 선언 |
| 입력과 실행 | 런타임이 네임스페이스·ID·구성으로 CNI 플러그인 호출 | Controller가 selector·IPBlock·Port를 데이터 경로 규칙으로 반영 |
| 실패 영향 | PodSandbox 네트워크 생성·정리 실패 | 미지원 구현이나 누락 규칙에서는 의도한 통신 제한이 적용되지 않음 |

> 요약: CNI는 Pod 연결을 만들고 NetworkPolicy는 그 연결에서 허용할 패킷 범위를 정함.

### 쉽게 이해하기 (학습용)
- 연결을 만드는 기능과 연결을 제한하는 정책 기능은 서로 다른 역할임

## Ⅳ. 구성요소 및 구조

| 구성요소 | 역할 |
|:---|:---|
| 컨테이너 런타임 | PodSandbox 생성 후 CNI 명령과 네트워크 네임스페이스를 전달함 |
| CNI 구성·플러그인 | 인터페이스·IPAM·경로·포트 매핑을 순서대로 적용함 |
| Pod·Namespace Label | NetworkPolicy가 보호 대상과 통신 상대를 선택하게 함 |
| NetworkPolicy 객체 | Ingress·Egress 방향별 peer·port 허용 조건을 선언함 |
| 정책 Controller | 정책 객체와 Endpoint 변경을 데이터 경로 규칙으로 변환함 |
| 패킷 데이터 경로 | 송신·수신 정책을 확인하고 허용 패킷만 전달함 |

```text
Pod 생성 -> 런타임 -> CNI ADD -> Pod IP·경로
                            |
NetworkPolicy -> 정책 Controller -> 패킷 허용 규칙
```

> 요약: CNI가 만든 Pod 연결 위에 정책 Controller가 selector 기반 허용 규칙을 반영함.

### 쉽게 이해하기 (학습용)
- 런타임·CNI·정책 Controller·패킷 경로가 연결 생성부터 허용 판정까지 이어짐

## Ⅴ. 연결·정책 적용 흐름

```text
네임스페이스 생성 -> CNI ADD -> IP·경로 구성 -> 정책 대상 선택 -> Egress·Ingress 판정 -> 전달
```

1. **네임스페이스 생성**: 런타임이 PodSandbox의 네트워크 격리 공간을 준비함
2. **CNI ADD**: 플러그인이 인터페이스를 연결하고 IPAM에서 주소를 할당함
3. **경로 구성**: Pod·노드·외부망 통신에 필요한 경로와 데이터 경로를 적용함
4. **정책 대상 선택**: Controller가 Pod·Namespace label과 정책 변경을 대조함
5. **양방향 판정**: 송신 Egress와 수신 Ingress 규칙이 모두 허용하는지 확인함
6. **패킷 전달**: 허용 흐름은 전달하고 일치하지 않는 격리 방향의 패킷은 차단함

> 요약: Pod 연결을 구성한 뒤 송신·수신 정책을 모두 통과한 패킷만 전달함.

### 쉽게 이해하기 (학습용)
- Pod에 IP를 준 뒤 보내는 쪽과 받는 쪽의 허용 조건을 모두 확인함

## Ⅵ. 실무 사례

1. 업무 Namespace는 기본 거부 후 DB 포트만 허용하고 차단 흐름 수·정책 적용 Pod 수를 확인함
2. 클러스터 노드는 CNI IPAM을 점검하고 Pod IP 할당 시간·Sandbox 생성 오류를 확인함

### 쉽게 이해하기 (학습용)
- 연결 실패는 CNI·IPAM에서, 예상 밖 통신은 정책 선택자와 양방향 규칙에서 원인을 찾음

## Ⅶ. 결론

- Pod 네트워크는 CNI 연결 기능과 NetworkPolicy 지원 여부·양방향 허용 규칙을 함께 검토해야 함

### 쉽게 이해하기 (학습용)
- 네트워크가 연결되는 것과 필요한 통신만 허용되는 것을 각각 검증해야 함
