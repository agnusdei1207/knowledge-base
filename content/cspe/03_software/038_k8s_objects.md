---
title: 쿠버네티스 객체 — Pod·Service·Deployment (K8s Objects)
date: 2026-07-05
tags: ["cspe-software"]
weight: 38
---

## Ⅰ. 개요
- 정의: 쿠버네티스 시스템에서 상태를 관리하기 위해 정의된 추상화된 기본 단위(객체).
- 출제 의도: 배포 단위(Pod), 관리 단위(Deployment), 네트워크 단위(Service)의 유기적 관계 이해도 확인.

## Ⅱ. 구성요소
- ASCII 구조도
  [ Service ] (Stable IP/DNS)
       | (Label Selector)
  [ Deployment ] (Replica Control)
       |
  [ Pod ] [ Pod ] [ Pod ] (Running Containers)
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Pod | 하나 이상의 컨테이너를 포함하는 최소 실행 단위 | 화물 컨테이너 상자 |
| Deployment | Pod의 개수 유지, 롤링 업데이트 등 배포 라이프사이클 관리 | 운송 계획서 |
| Service | 유동적인 Pod IP 대신 고정된 진입점 제공 (로드밸런싱) | 대표 전화번호 |
> 요약: Pod는 실행, Deployment는 운영, Service는 노출을 담당하는 계층 구조임.

## Ⅲ. 절차
- ASCII 흐름도
  [Deployment 생성] -> [ReplicaSet 생성] -> [Pod 생성] -> [Service 연결]
- 4단계 설명
1. Deployment 정의를 통해 목표하는 Pod 개수와 이미지를 설정함.
2. ReplicaSet이 설정된 개수만큼 Pod가 실행되도록 감시 및 유지함.
3. 개별 Pod가 노드에 할당되어 실제 비즈니스 로직 수행함.
4. Service 객체가 Label Selector를 통해 해당 Pod들을 묶어 외부 통신 허용함.
> 요약: 추상화 레이어를 통해 개별 컨테이너의 가변성을 극복하고 안정적 서비스 제공함.

## Ⅳ. 문제점
- Pod 가변성: Pod는 언제든 삭제/재생성될 수 있어 IP가 수시로 변경되어 직접 연결 불가함.
- 설정 오류: Label Selector 오타 발생 시 Service와 Pod 간 연결이 끊겨 서비스 장애 유발함.

## Ⅴ. 개선방안
- 고정 진입점 사용: 반드시 Service(ClusterIP, NodePort 등)를 통해서만 Pod에 접근하도록 설계함.
- 정적 분석 도구: Kube-linter, Datree 등을 활용해 배포 전 Manifest 설정 오류 자동 검증함.

## Ⅵ. 전망
- 커스텀 리소스(CRD)와 오퍼레이터(Operator) 패턴을 통한 도메인 특화 객체 정의가 대중화됨.
- 서비스 메쉬와 결합하여 Service 객체 이상의 세밀한 트래픽 제어(Canary, Blue-Green)가 기본사양화됨.
- Gateway API 도입으로 기존 Ingress의 한계를 넘는 표준화된 L7 라우팅 체계로 전환될 것임.
