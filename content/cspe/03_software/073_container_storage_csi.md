---
title: "컨테이너 스토리지 CSI (Container Storage)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 73
---

## Ⅰ. 개요
- **정의**: 컨테이너 오케스트레이터와 스토리지 시스템 간 볼륨 관리를 표준화한 인터페이스임
- **배경/필요성**: 스토리지 드라이버가 오케스트레이터 코드에 내장되면 드라이버 추가·업데이트마다 코어 릴리스가 필요하므로 분리가 필요함
- **비유**: USB 규격처럼, 어떤 외장 디스크든 동일 포트에 꽂으면 인식되게 하는 표준임

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CSI 아키텍처와 볼륨 라이프사이클 이해 | Controller/Node 2-tier, PV/PVC/SC 연계 | in-tree 드라이버와 CSI 외부 드라이버 차이 구분 |

> 요약: CSI는 스토리지 드라이버를 오케스트레이터 외부 플러그인으로 분리한 표준 인터페이스임

## Ⅱ. 구성요소
```text
K8s API Server
      |
+-----v------+      gRPC      +-----------+
| Controller  | <-----------> | CSI Driver |
| Plugin      |               | (vendor)   |
+-------------+               +-----------+
      |                             |
+-----v------+      gRPC      +----v------+
| Node Plugin | <-----------> | Storage   |
+-------------+               +-----------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Controller Plugin | 볼륨 Create/Delete/Snapshot을 담당하는 중앙 제어부 | 물류 본사 |
| Node Plugin | 노드에서 볼륨 Mount/Unmount를 수행하는 에이전트 | 현장 설치 기사 |
| CSI Driver | 벤더별 스토리지 API를 gRPC로 구현한 바이너리 | USB 드라이버 |
| External Provisioner | PVC 생성 시 CSI Driver에 CreateVolume 호출을 위임하는 사이드카 | 자동 주문 시스템 |

> 요약: Controller/Node 2계층 플러그인과 gRPC 기반 CSI Driver로 구성됨

## Ⅲ. 절차
```text
PVC 생성 --> Provisioner --> CreateVolume --> Attach --> Mount
```
- 1단계: 사용자가 PVC 생성 시 External Provisioner가 StorageClass 확인함
- 2단계: Controller Plugin이 CSI Driver의 `CreateVolume` gRPC 호출로 볼륨 생성함
- 3단계: External Attacher가 `ControllerPublishVolume`으로 볼륨을 노드에 Attach함
- 4단계: Node Plugin이 `NodeStageVolume`/`NodePublishVolume`으로 Pod 경로에 Mount함

> 요약: PVC→볼륨 생성→Attach→Mount 4단계로 동적 프로비저닝이 수행됨

## Ⅳ. 문제점
- 드라이버 품질 편차: 벤더별 CSI Driver 성숙도 차이로 Snapshot·Resize 미지원 사례 존재함
- 장애 전파: Controller Plugin 단일 장애 시 전체 볼륨 프로비저닝 중단됨
- 성능 가시성 부족: CSI 계층의 I/O 지연이 별도 메트릭 없이는 식별 불가함

> 요약: 드라이버 품질, 단일 장애점, 성능 가시성이 주요 문제임

## Ⅴ. 개선방안
1. 단기: CSI Driver 선정 시 Capability 매트릭스(Snapshot/Resize/Clone) 사전 검증함
2. 중기: Controller Plugin HA 구성(Leader Election)으로 단일 장애점 제거함
3. 장기: CSI 메트릭 Exporter 연동으로 볼륨별 IOPS·지연 모니터링 체계 구축함

> 요약: 드라이버 검증, HA 구성, 메트릭 연동으로 개선 가능함

## Ⅵ. 전망
- 발전 방향: CSI Ephemeral Volume·Generic Ephemeral Volume으로 임시 스토리지 표준화 확장 중임
- 기술사적 판단: Stateful 워크로드 컨테이너 전환의 핵심 기반이므로 PV/PVC/SC 연계 흐름 숙지 필요함
- 기술사 제언: 데이터 보호를 위해 CSI Snapshot + Velero 백업 파이프라인 설계를 권고함
