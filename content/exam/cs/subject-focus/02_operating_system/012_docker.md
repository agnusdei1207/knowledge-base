---
title: "도커 (Docker)"
date: "2026-06-30"
weight: 12
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 도커(Docker)는 Linux의 네임스페이스(Namespace)와 cgroups(Control Groups)를 기반으로 애플리케이션을 컨테이너로 빌드·배포·실행하는 플랫폼으로, 이미지·컨테이너·레지스트리를 통해 일관된 실행 환경을 제공한다.

## Ⅱ. 구성요소 / 원리
- **이미지(Image)**: 실행에 필요한 파일시스템·의존성을 담은 읽기 전용 템플릿
- **컨테이너(Container)**: 이미지를 실행한 인스턴스(쓰기 가능 레이어 추가)
- **레지스트리(Registry)**: 이미지를 저장·배포하는 저장소(Docker Hub 등)
- **Union(Layered) File System**: 이미지를 계층으로 쌓아 공유·재사용(OverlayFS)
- **격리 기반**: namespace(가시성 격리) + cgroups(자원 제한) 활용

## Ⅲ. 흐름도 / 구조
```text
Dockerfile ─build→ Image ─push→ Registry
                     │            │ pull
                     │            ▼
                     └──run──→ Container 실행
                                 │
   [Layered FS]  R/W Layer (컨테이너)
                 ─────────────
                 R/O Layer (앱)
                 R/O Layer (라이브러리)
                 R/O Layer (베이스 OS)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | "Build once, Run anywhere" 일관된 컨테이너 배포 환경 제공 |
| 장점 | 레이어 공유로 경량·빠른 배포, 이식성·재현성, DevOps 표준 |
| 한계 | 커널 공유로 격리·보안 한계, 단일 호스트(오케스트레이션 별도) |

## Ⅴ. 기술사적 적용
- namespace + cgroups를 사용자 친화 인터페이스로 추상화한 대표 구현
- 이미지 레이어 캐싱으로 빌드·전송·저장 효율 극대화
- Kubernetes(컨테이너 런타임 CRI)와 연계해 대규모 오케스트레이션 실현
