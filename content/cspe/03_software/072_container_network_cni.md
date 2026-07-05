---
title: "컨테이너 네트워크 CNI (Container Network)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 72
---

## Ⅰ. 개요
- **정의**: 컨테이너 런타임과 네트워크 플러그인 간 인터페이스를 표준화한 규격임
- **배경/필요성**: 컨테이너별 격리된 네트워크 네임스페이스에 IP 할당·라우팅을 런타임 독립적으로 처리할 표준이 필요함
- **비유**: 전화기(컨테이너)와 통신사(네트워크 플러그인) 사이의 SIM 카드 규격과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CNI 동작 원리와 플러그인 체이닝 이해 | ADD/DEL/CHECK 3개 명령, 플러그인 체이닝 | CNI와 Docker 내장 네트워크(libnetwork) 혼동 금지 |

> 요약: CNI는 컨테이너 네트워크 설정을 플러그인 방식으로 표준화한 인터페이스 규격임

## Ⅱ. 구성요소
```text
Container Runtime ---> CNI Binary ---> Network Plugin
       |                   |                |
   netns 생성         config.json 파싱    veth/bridge 생성
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| CNI Plugin | ADD/DEL/CHECK 명령을 구현한 실행 바이너리 | 설치 기사 |
| Network Config | JSON으로 서브넷·게이트웨이·플러그인 체인 정의 | 시공 설계도 |
| Plugin Chaining | 여러 플러그인을 순차 실행하여 복합 네트워크 구성 | 배관-전기-도배 순차 시공 |
| IPAM Plugin | IP 주소 할당·회수를 전담하는 하위 플러그인 | 주소 배정 담당자 |

> 요약: CNI는 플러그인 바이너리, JSON 설정, 체이닝, IPAM으로 구성됨

## Ⅲ. 절차
```text
Pod 생성 --> netns 생성 --> CNI ADD 호출 --> IPAM 할당 --> veth 연결
```
- 1단계: kubelet이 Pod Sandbox 생성 시 네트워크 네임스페이스를 생성함
- 2단계: CRI가 CNI 설정 파일을 읽어 지정된 플러그인 체인의 첫 번째 바이너리 호출함
- 3단계: IPAM 플러그인이 서브넷에서 IP 할당 후 결과를 JSON으로 반환함
- 4단계: Bridge/Overlay 플러그인이 veth pair 생성·연결하여 Pod 간 통신 경로 확보함

> 요약: netns 생성-플러그인 호출-IP 할당-veth 연결 4단계로 Pod 네트워크가 구성됨

## Ⅳ. 문제점
- IP 고갈: 대규모 클러스터에서 서브넷 크기 부족 시 Pod 스케줄링 실패함
- 네트워크 정책 복잡성: 플러그인별 NetworkPolicy 지원 범위가 달라 일관성 확보 어려움
- 성능 오버헤드: Overlay(VXLAN) 방식은 캡슐화/역캡슐화로 패킷당 50byte 이상 추가됨

> 요약: IP 고갈, 정책 비일관성, Overlay 오버헤드가 주요 문제임

## Ⅴ. 개선방안
1. 단기: IPAM을 `host-local`에서 Cluster-scope IPAM으로 전환하여 IP 풀 확장함
2. 중기: Cilium 등 eBPF 기반 플러그인으로 NetworkPolicy 일관성 확보함
3. 장기: eBPF 데이터플레인 전환으로 Overlay 캡슐화 제거하여 성능 개선함

> 요약: IPAM 확장, eBPF 기반 정책, 캡슐화 제거로 개선 가능함

## Ⅵ. 전망
- 발전 방향: eBPF·XDP 기반 데이터플레인이 기존 iptables 방식을 대체하는 추세임
- 기술사적 판단: K8s 네트워크 모델 이해의 핵심이므로 Flannel/Calico/Cilium 차이 숙지 필요함
- 기술사 제언: 서비스 메시(071 참조) 연계 시 CNI와 사이드카 프록시 역할 분담 설계를 권고함
