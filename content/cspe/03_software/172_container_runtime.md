---
title: "컨테이너 런타임 — containerd·CRI-O (Container Runtime)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 172
extra:
  question_no: "172"
  exam_status: "미출제"
---

## 미리 알고가기

- 컨테이너 런타임은 이미지 관리와 컨테이너 생성·시작·중지·삭제를 수행하는 노드 소프트웨어임
- CRI는 kubelet과 컨테이너 런타임 사이의 gRPC 기반 RuntimeService·ImageService 규약임
- OCI 이미지 사양은 이미지 매니페스트·구성·파일시스템 계층 형식을 정의함
- OCI 런타임 사양은 번들과 실행 설정으로 컨테이너 프로세스를 생성하는 방식을 정의함
- PodSandbox는 한 Pod의 네트워크·IPC 등 공통 실행 경계를 나타내는 CRI 객체임
- CNI는 PodSandbox의 네트워크 인터페이스·IP·경로를 구성하는 플러그인 규약임
- 컨테이너 모니터는 실행 프로세스의 종료 코드·I/O·수명주기 상태를 런타임에 전달함
- 스냅샷터는 이미지 계층으로 컨테이너 루트 파일시스템을 준비함
- 런타임 shim은 컨테이너 작업을 런타임 데몬과 분리해 실행·감시함

## 작성 근거(검토용)

- 런타임 선택은 공통 OCI 실행보다 CRI 통합 범위와 이미지·수명주기 관리 구조가 핵심이므로 이를 대비함
- containerd·CRI-O 비교를 kubelet·CRI·OCI 런타임·CNI의 호출 구조와 Pod 실행 절차로 연결함
- 제목부터 결론까지 5회 전수 검수하여 런타임·인터페이스·하위 실행기의 역할을 구분함

## Ⅰ. 개요

- **정의/개념**: 컨테이너 런타임은 CRI 요청에 따라 이미지를 준비하고 OCI 실행기로 PodSandbox·컨테이너를 관리하는 노드 구성요소임
- **배경/필요성**: 오케스트레이터와 실행 구현을 분리하기 위해 표준 CRI·OCI 경계와 노드 런타임이 필요함

## Ⅱ. 특징

- kubelet은 CRI RuntimeService와 ImageService를 통해 런타임 구현과 분리됨
- 런타임은 이미지 계층·스냅샷·컨테이너 메타데이터와 실행 상태를 노드에서 관리함
- OCI 실행기와 커널 네임스페이스·cgroup을 사용해 실제 컨테이너 프로세스를 시작함
- kubelet과 런타임의 CRI 버전·cgroup 드라이버가 맞지 않으면 노드 등록이나 Pod 생성이 실패함

## Ⅲ. 종류 및 비교

| 판단 기준 | containerd | CRI-O |
|:---|:---|:---|
| 설계 범위 | 여러 클라이언트가 사용할 수 있는 범용 컨테이너 런타임 | Kubernetes CRI 제공에 집중한 런타임 |
| CRI 통합 | 내장 CRI 플러그인이 kubelet 요청 처리 | CRI 서버가 핵심 인터페이스로 요청 처리 |
| 이미지 관리 | 콘텐츠 저장소·이미지 메타데이터·스냅샷터 관리 | OCI 이미지 라이브러리·저장 드라이버로 계층 관리 |
| 실행 연결 | 런타임 shim을 통해 runc·다른 OCI 실행기 호출 | 구성된 OCI 실행기와 모니터를 호출 |
| 외부 사용 | CRI 외 API로 비 Kubernetes 작업도 지원 | Kubernetes Pod 실행 범위에 집중 |
| 적합 조건 | 범용 런타임과 Kubernetes CRI를 함께 사용 | Kubernetes 전용의 CRI·OCI 경계가 필요 |

> 요약: containerd는 범용 런타임에 CRI를 통합하고 CRI-O는 Kubernetes CRI 제공에 집중함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 역할 |
|:---|:---|
| kubelet | Pod 명세를 기준으로 CRI에 샌드박스·이미지·컨테이너 요청을 보냄 |
| CRI 엔드포인트 | RuntimeService·ImageService gRPC를 제공함 |
| 이미지·스냅샷 계층 | OCI 이미지 계층을 가져오고 컨테이너 루트 파일시스템을 준비함 |
| PodSandbox 관리 | Pod 단위 네임스페이스와 공통 실행 경계를 생성함 |
| OCI 실행기 | 번들과 실행 설정으로 컨테이너 프로세스를 생성함 |
| CNI | Pod 네트워크 인터페이스·IP·경로를 구성함 |
| cgroup | 컨테이너의 CPU·메모리 자원 경계를 적용함 |

```text
kubelet -> CRI -> containerd 또는 CRI-O -> OCI 실행기 -> 컨테이너 프로세스
                    |                    |
                 이미지 계층          CNI·cgroup
```

> 요약: CRI 런타임이 이미지와 PodSandbox를 준비하고 OCI 실행기·CNI를 호출함.

## Ⅴ. Pod 실행 흐름

```text
Pod 명세 확인 -> PodSandbox 생성 -> 이미지 확보 -> 컨테이너 생성·시작 -> 상태 보고
```

1. **Pod 명세 확인**: kubelet이 원하는 Pod와 노드의 실제 실행 상태를 비교함
2. **PodSandbox 생성**: 런타임이 Pod 네임스페이스를 만들고 CNI를 호출함
3. **이미지 확보**: ImageService가 이미지 다이제스트와 계층을 확인해 노드에 준비함
4. **컨테이너 생성·시작**: 런타임이 루트 파일시스템과 자원 설정을 OCI 실행기에 전달함
5. **상태 보고**: 런타임 상태와 종료 코드를 kubelet이 API 서버에 반영함

> 요약: kubelet의 CRI 요청이 샌드박스·이미지·OCI 실행 단계를 거쳐 컨테이너 상태로 반환됨.

## Ⅵ. 실무 사례

1. Kubernetes 노드는 containerd CRI v1을 활성화하고 노드 등록 실패·Pod 시작시간을 확인함
2. CRI-O 노드는 kubelet과 cgroup 드라이버를 맞추고 샌드박스 오류·자원 제한 위반을 확인함

## Ⅶ. 결론

- 컨테이너 런타임은 CRI 호환성·cgroup 구성·운영 범위를 기준으로 containerd와 CRI-O를 선택해야 함
