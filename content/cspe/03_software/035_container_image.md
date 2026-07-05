---
title: 컨테이너 이미지 및 레이어 구조 (Container Image)
date: 2026-07-05
tags: ["cspe-software"]
weight: 35
---

## Ⅰ. 개요
- 정의: 서비스 실행에 필요한 모든 파일과 설정을 포함하는 읽기 전용 템플릿 및 계층적 구조.
- 출제 의도: 효율적인 저장 및 전송을 위한 Copy-on-Write 방식과 레이어 캐싱 원리 이해 여부 확인.

## Ⅱ. 구성요소
- ASCII 구조도
  [ Container Layer (Writable)  ] <- Container 1
  [-----------------------------]
  [ Image Layer 3 (Read Only)   ] <- App Code
  [ Image Layer 2 (Read Only)   ] <- Dependencies
  [ Image Layer 1 (Read Only)   ] <- OS/Library
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Read-only Layers | 변경 불가능한 이미지의 구성 단위, 레이어 간 공유 가능 | 책의 페이지 |
| Writable Layer | 컨테이너 실행 시 생성되는 최상단 쓰기 가능 레이어 | 포스트잇 메모 |
| Manifest | 이미지 구성 레이어 및 메타데이터를 정의한 JSON 파일 | 목차 |
> 요약: 하위 레이어는 공유하고 변경사항만 상단 레이어에 기록하여 효율성 극대화함.

## Ⅲ. 절차
- ASCII 흐름도
  [Base Image] -> [Run Command] -> [New Layer] -> [Commit/Push]
- 4단계 설명
1. Dockerfile의 각 명령(FROM, RUN 등)마다 새로운 레이어 생성됨.
2. 이전 레이어와 차이점(Diff)만 저장하여 저장 공간 절약함.
3. 레이어 캐싱을 통해 변경되지 않은 단계는 재사용하여 빌드 속도 향상함.
4. 최종 이미지 전송 시 중복 레이어는 제외하고 누락된 레이어만 다운로드함.
> 요약: 증분식 레이어 생성 및 캐싱을 통한 배포 효율성 확보함.

## Ⅳ. 문제점
- 레이어 비대화: 불필요한 임시 파일이나 도구 포함 시 이미지 크기 급증하여 전송 지연됨.
- 보안 취약점: 오래된 베이스 이미지 사용 시 알려진 취약점이 모든 파생 이미지에 전파됨.

## Ⅴ. 개선방안
- Multi-stage Build: 빌드 시 필요한 도구와 실행 시 필요한 결과물을 분리하여 크기 최소화함.
- Distroless Image: 쉘이나 패키지 매니저를 제거한 최소 실행 환경 이미지 사용하여 보안 강화함.

## Ⅵ. 전망
- 공급망 보안 강화를 위한 이미지 서명(Notary) 및 SBOM(S/W Bill of Materials) 포함 의무화됨.
- 빌드 속도 개선을 위해 eStargz 등 레이어 지연 로딩 기술을 적용한 이미지 표준 확산될 것임.
- 컨테이너 이미지 스캐닝이 CI/CD 파이프라인의 필수 단계로 정착되어 DevSecOps 구현 핵심 역할 수행함.
