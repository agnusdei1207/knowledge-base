---
title: "Container Runtime (Docker and containerd)"
date: 2026-07-05
tags: ["cspe-software"]
weight: 247
---

## Ⅰ. 개요
- 정의: 컨테이너를 생성, 실행 및 관리하는 소프트웨어 구성 요소임
- 배경: OCI 이미지와 실행 규격을 기준으로 컨테이너 생성·격리·수명주기를 일관되게 관리할 필요
- 출제 의도
| 대상 | 주요 포인트 | 비중 |
|------|------------|------|
| Docker | Image, Client-Server | 높음 |
| containerd | 표준화(CRI), 경량화 | 매우높음 |

## Ⅱ. 구성요소
- ASCII 구조도
  [ 사용자/K8s ] -> [ Docker Engine ] -> [ containerd ] -> [ runc ]
                                             |           |
                                         (Life Cycle) (Container)

- 구성요소 표
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Docker | 개발/빌드/배포 기능을 갖춘 올인원 컨테이너 도구 | 복합기 |
| containerd | 컨테이너 실행 및 관리 기능만 분리한 경량 런타임 | 프린터 엔진 |
| runc | OCI 표준에 맞춰 컨테이너를 직접 구동하는 저수준 툴 | 인쇄 헤드 |

> 요약: 고수준 도구(Docker)에서 실행 엔진(containerd)이 분리되어 표준화됨

## Ⅲ. 절차
- ASCII 흐름도
  [이미지 빌드] -> [이미지 저장] -> [컨테이너 생성] -> [실행 및 격리]
    (Docker)         (Registry)        (containerd)       (Namespace)

- 4단계 설명
1. 빌드: Dockerfile을 사용하여 앱과 환경을 포함한 이미지를 생성함
2. 전송: 생성된 이미지를 중앙 저장소(Registry)로 Push하여 공유함
3. 실행요청: K8s 등이 런타임에 컨테이너 구동을 요청(CRI 호출)함
4. 격리구동: 리눅스 커널의 Namespace와 Cgroups를 통해 자원을 분리하여 실행함

> 요약: 이미지를 가져와 파일 시스템과 실행 설정을 준비하고 Namespace·Cgroup으로 프로세스를 격리함

## Ⅳ. 문제점
- Docker 데몬 장애 시 모든 컨테이너가 영향을 받는 구조적 한계 있었음
- 쿠버네티스에서 Docker 지원 중단(Deprecation)으로 인한 마이그레이션 부담 발생함

## Ⅴ. 개선방안
- (단기) CRI(Container Runtime Interface) 호환 런타임(containerd, CRI-O)으로 전환함
- (중기) 루트 권한 없이 구동되는 Rootless 컨테이너 기술을 적용하여 보안 강화함
- (장기) WebAssembly(Wasm)와 결합하여 더 작고 빠른 실행 환경을 탐색함

## Ⅵ. 전망
- 클라우드 네이티브 환경의 표준 런타임으로서 containerd의 입지가 공고해짐
- 보안 하드웨어(TEE)와 결합한 컨피덴셜 컨테이너(Confidential Container) 수요 증가됨
