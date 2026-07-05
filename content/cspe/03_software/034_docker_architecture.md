---
title: 도커 Docker 엔진 및 아키텍처 (Docker Architecture)
date: 2026-07-05
tags: ["cspe-software"]
weight: 34
---

## Ⅰ. 개요
- 정의: 컨테이너 기반 애플리케이션의 빌드, 배포, 실행을 자동화하는 오픈소스 플랫폼 엔진.
- 출제 의도: Client-Server 구조의 도커 아키텍처와 주요 구성 요소 간의 상호작용 이해도 평가.

## Ⅱ. 구성요소
- ASCII 구조도
  [ Docker Client ]    [ Docker Host ]             [ Registry ]
  ( docker build ) --> [ Docker Daemon (dockerd) ] <-- [ Images ]
  ( docker pull  ) --> [ - Containers          ]
  ( docker run   ) --> [ - Images / Networks   ]
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Docker Daemon | 클라이언트 요청을 처리하고 객체(이미지 등) 관리 | 주방장 |
| Docker Client | CLI를 통해 사용자와 도커 엔진 간 인터페이스 제공 | 웨이터 |
| Images | 컨테이너 실행에 필요한 파일과 설정의 읽기 전용 템플릿 | 조리법(레시피) |
> 요약: Client-Server 모델을 기반으로 REST API를 통해 데몬과 통신하여 제어함.

## Ⅲ. 절차
- ASCII 흐름도
  [Dockerfile] -> [Build] -> [Image] -> [Run] -> [Container]
- 4단계 설명
1. Dockerfile에 애플리케이션 구성 환경 기술 및 작성함.
2. docker build 명령으로 레이어 구조의 이미지 생성함.
3. 생성된 이미지를 Docker Hub 등 레지스트리에 푸시함.
4. docker run 명령 시 이미지를 인스턴스화하여 컨테이너로 기동함.
> 요약: 명세서 기반의 이미지 제작과 실행을 통한 일관성 확보함.

## Ⅳ. 문제점
- 단일 지점 장애(SPOF): Docker Daemon 정지 시 관리 중인 모든 컨테이너 영향 받음.
- 보안 리스크: 기본적으로 루트 권한으로 실행되어 공격 노출 시 호스트 전권 탈취 위험함.

## Ⅴ. 개선방안
- Rootless 모드: 일반 사용자 권한으로 도커 데몬 실행하여 보안 위협 완화함.
- Containerd 분리: 데몬 의존성을 낮추고 표준 런타임(CRI)을 사용하여 안정성 강화함.

## Ⅵ. 전망
- OCI(Open Container Initiative) 표준 준수를 통한 타 런타임(Podman 등)과의 호환성 증대됨.
- 대규모 운영 환경에서는 단일 엔진을 넘어 쿠버네티스 등 오케스트레이션 도구와의 통합이 필수임.
- 데브옵스 도구를 넘어 AI 모델 배포 및 엣지 디바이스 환경의 핵심 배포 단위로 진화 중임.
