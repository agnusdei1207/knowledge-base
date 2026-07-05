---
title: "컨테이너 이미지 OCI (Container Image OCI)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 71
---

## Ⅰ. 개요
- **정의**: 컨테이너 이미지의 포맷·배포·런타임을 표준화한 개방형 규격임
- **배경/필요성**: Docker 독점 포맷에 종속되면 런타임·레지스트리 교체가 불가능하므로 벤더 중립 표준이 필요함
- **비유**: 국제 표준 컨테이너(ISO 668) 규격처럼, 어떤 선박·트럭이든 동일 규격 컨테이너를 운반할 수 있게 하는 것과 동일함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 표준화 목적과 구성 계층 이해 | Image Spec, Runtime Spec, Distribution Spec 3종 구분 | Docker Image와 OCI Image 차이를 혼동하지 말 것 |

> 요약: OCI는 컨테이너 이미지·런타임·배포를 벤더 중립으로 표준화한 개방 규격임

## Ⅱ. 구성요소
```text
+------------------+
| Distribution Spec| <-- 레지스트리 Push/Pull API
+------------------+
        |
+------------------+
|   Image Spec     | <-- Manifest + Config + Layers
+------------------+
        |
+------------------+
|  Runtime Spec    | <-- config.json 기반 실행
+------------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Image Spec | Manifest, Config JSON, Layer tar 묶음으로 이미지 포맷 정의 | 택배 포장 규격 |
| Runtime Spec | `config.json`으로 rootfs·네임스페이스·cgroup 등 실행 환경 정의 | 택배 개봉·설치 매뉴얼 |
| Distribution Spec | 레지스트리와 클라이언트 간 Push/Pull REST API 정의 | 택배 배송 프로토콜 |
| Layer | 파일시스템 변경분을 tar+gzip으로 적층한 불변 단위 | 투명 필름 겹치기 |

> 요약: OCI는 이미지 포맷·실행 규격·배포 API 3개 Spec으로 구성됨

## Ⅲ. 절차
```text
Dockerfile --> Build --> Push --> Pull --> Unpack --> Run
                |         |        |        |        |
              Layer생성  Registry  Client  rootfs   runc
```
- 1단계: `Dockerfile` 기반 빌드 시 각 명령어가 Layer로 변환됨
- 2단계: Manifest·Config·Layer를 OCI 포맷으로 패키징 후 레지스트리에 Push함
- 3단계: 클라이언트가 Manifest 조회 후 필요 Layer만 Pull하여 로컬 저장함
- 4단계: Layer를 OverlayFS로 합산해 rootfs 구성 후 `runc`가 컨테이너 실행함

> 요약: 빌드-Push-Pull-실행의 4단계를 OCI 3개 Spec이 각각 표준화함

## Ⅳ. 문제점
- 이미지 크기 비대: 불필요 패키지 포함 시 Layer 누적으로 Pull 시간 증가함
- 보안 취약점 내재: Base Image의 CVE가 파생 이미지 전체에 전파됨
- 레지스트리 호환성 편차: Distribution Spec 미준수 사설 레지스트리에서 Pull 실패 발생함

> 요약: 이미지 비대, 보안 전파, 레지스트리 호환성이 주요 문제임

## Ⅴ. 개선방안
1. 단기: Multi-stage Build·distroless 베이스로 이미지 크기 최소화함
2. 중기: Trivy·Grype 등 취약점 스캐너를 CI 파이프라인에 통합하여 CVE 차단함
3. 장기: OCI Artifact 확장으로 SBOM·서명·정책을 이미지와 함께 배포함

> 요약: 경량화, 취약점 스캔 자동화, Artifact 확장으로 개선 가능함

## Ⅵ. 전망
- 발전 방향: OCI Artifact로 Helm Chart·WASM 모듈 등 범용 패키징 표준으로 확장 중임
- 기술사적 판단: 컨테이너 생태계 이식성 확보의 핵심 기반이므로 Spec 버전별 차이 숙지 필요함
- 기술사 제언: 이미지 서명(cosign)·SBOM 연계를 통한 공급망 보안 체계 수립을 권고함
