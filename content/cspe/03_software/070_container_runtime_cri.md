---
title: "컨테이너 런타임 CRI (Container Runtime)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 70
---

## Ⅰ. 개요
- **정의**: Kubelet과 컨테이너 런타임 간 통신을 표준화한 gRPC 인터페이스(CRI)와 이를 구현하는 런타임
- **배경/필요성**: K8s가 Docker에 강결합되면 런타임 교체가 불가하므로, 표준 인터페이스로 런타임을 플러그인화할 필요가 있음
- **비유**: 전원 콘센트 규격(CRI) — 규격만 맞으면 어떤 가전(런타임)이든 꽂아 사용 가능함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CRI 표준화 의의와 런타임 비교 | containerd, CRI-O, OCI 표준 | Docker ≠ 컨테이너 런타임 전체임을 명확히 할 것 |

> 요약: CRI는 Kubelet과 런타임 간 표준 인터페이스이며, containerd·CRI-O가 대표 구현체임

## Ⅱ. 구성요소
```text
Kubelet --gRPC(CRI)--> CRI Runtime --OCI spec--> runc/crun
                            |
                            v
                       Image Service
                      (pull/unpack)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| CRI (인터페이스) | Kubelet이 런타임에 Pod 생성·삭제를 요청하는 gRPC API 규격 | 콘센트 규격 |
| containerd | Docker에서 분리된 산업 표준 고수준 런타임 | 범용 멀티탭 |
| CRI-O | K8s 전용으로 경량 설계된 CRI 구현체 | 전용 어댑터 |
| OCI Runtime(runc) | 컨테이너 프로세스를 실제 생성하는 저수준 런타임 | 실제 전기 공급선 |

> 요약: CRI 인터페이스 위에 고수준 런타임(containerd/CRI-O)과 저수준 런타임(runc)이 계층화됨

## Ⅲ. 절차
```text
Kubelet --> CRI call --> Pull Image --> Create Sandbox --> Start Container
```
- 1단계: Kubelet이 CRI gRPC API로 Pod 생성을 요청함
- 2단계: 런타임이 Image Service를 통해 컨테이너 이미지를 Pull·Unpack함
- 3단계: Pod Sandbox(네트워크 네임스페이스)를 생성하여 격리 환경을 준비함
- 4단계: OCI Runtime(runc)을 호출하여 컨테이너 프로세스를 기동함

> 요약: CRI 호출-이미지 풀-샌드박스 생성-프로세스 기동의 4단계로 컨테이너가 실행됨

## Ⅳ. 문제점
- Docker 호환성 단절: K8s에서 dockershim 제거 후 Docker 직접 사용이 불가함
- 런타임 선택 기준 부재: containerd와 CRI-O 간 기능 차이에 대한 명확한 가이드라인이 부족함
- 보안 격리 한계: runc는 커널 공유 기반이므로 커널 취약점 공격 시 호스트 탈출 위험이 있음

> 요약: Docker 호환성 단절, 런타임 선택 기준 부재, 커널 공유 보안 한계가 주요 문제임

## Ⅴ. 개선방안
1. 단기: containerd 또는 CRI-O로 마이그레이션하고 기존 이미지 호환성을 검증함
2. 중기: 워크로드 특성별 런타임 선택 기준(범용: containerd, K8s 전용: CRI-O)을 수립함
3. 장기: gVisor·Kata Containers 등 샌드박스 런타임을 도입하여 커널 격리 수준을 강화함

> 요약: CRI 호환 런타임 전환, 선택 기준 수립, 샌드박스 런타임 도입으로 개선함

## Ⅵ. 전망
- 발전 방향: WebAssembly(Wasm) 런타임이 CRI와 통합되어 컨테이너 대안으로 부상함
- 기술사적 판단: OCI·CRI 표준이 런타임 생태계를 다양화하며, Docker 의존 탈피가 완료됨
- 기술사 제언: 보안 요구 수준에 따라 runc·gVisor·Kata 등 런타임 계층을 선택적으로 적용할 필요
