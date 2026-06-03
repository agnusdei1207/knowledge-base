---
title: 68. 도커 이미지 (Docker Image) - 불변(Immutable) 상태의 애플리케이션 실행 패키지 파일
date: '2026-04-07'
tags:
- studynote-cloud
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[063_docker_architecture|Docker]] Image는 애플리케이션과 실행 환경을 불변 형태로 패키징한 템플릿이다.
> 2. **가치**: 어디서나 같은 이미지로 실행해 배포 재현성과 이식성을 높인다.
> 3. **판단**: 이미지와 컨테이너를 구분해야 하며, 이미지는 빌드 산출물이라는 점이 핵심이다.

---

## Ⅰ. 개요 및 필요성

같은 프로그램도 환경이 다르면 다르게 동작할 수 있다. 이미지는 이 문제를 줄이기 위한 표준 패키지다.

불변 이미지를 쓰면 배포 결과를 예측하기 쉬워진다.

- **📢 섹션 요약 비유**: 밀봉된 도시락 상자처럼 어디서 열어도 같은 내용이 들어 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Dockerfile
  ↓ build
Image Layers
  ↓ run
Container
```

| 구성 요소 | 역할 |
| :-- | :-- |
| Image | 템플릿/패키지 |
| Layer | 변경 단위 |
| [[235_registry_immutable_tag|Registry]] | 저장/배포 |

이미지는 읽기 전용 형태의 층으로 구성된다. 컨테이너는 그 이미지 위에 [[289_cqrs_db|쓰기]] 가능한 얇은 계층을 덧댄 실행 상태다.

- **📢 섹션 요약 비유**: 레시피와 완성된 도시락은 다르다.

---

## Ⅲ. 비교 및 연결

| 구분 | Image | [[194_container_virtualization_docker_namespace|Container]] |
| :-- | :-- | :-- |
| 성격 | 불변 패키지 | 실행 인스턴스 |
| 상태 | 정적 | 동적 |
| 변경 | 다시 빌드 | [[087_process_state_transition|생성]]/삭제 |

| 장점 | 의미 |
| :-- | :-- |
| 재현성 | 같은 결과 |
| 이식성 | 어디서나 실행 |
| 배포 단순화 | 운영 안정 |

이미지는 배포의 기준점이다. 그래서 태그와 [[288_version_ihl_tos_total_length|버전]] 관리가 중요하다.

- **📢 섹션 요약 비유**: 포장된 상자는 바꾸지 않고, 필요하면 새 상자를 다시 만든다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 이미지가 불변으로 관리되는가?
2. 태그/[[288_version_ihl_tos_total_length|버전]] 정책이 있는가?
3. 이미지 크기를 줄였는가?
4. 비밀값을 넣지 않았는가?
5. [[235_registry_immutable_tag|레지스트리]] 보안을 적용했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- latest 태그만 쓰는 설계
- 이미지 내부를 실행 중 수정하는 설계
- 거대한 이미지로 배포하는 설계
- 실행 컨테이너와 이미지를 혼동하는 설계

기술사 관점에서는 [[063_docker_architecture|Docker]] Image를 "불변 배포 산출물"로 이해해야 한다.

- **📢 섹션 요약 비유**: 한 번 포장한 도시락은 그대로 전달하는 것이 안전하다.

---

## Ⅴ. 기대효과 및 결론

[[063_docker_architecture|Docker]] Image는 표준화된 배포와 재현성을 가능하게 한다. 그래서 현대 배포의 기본 단위가 되었다.

결론적으로 [[063_docker_architecture|Docker]] Image는 불변 상태의 애플리케이션 패키지다.

- **📢 섹션 요약 비유**: 같은 상자를 어디서 열어도 같은 내용이 나온다.

---

## 관련 개념 맵

```text
Dockerfile
  ↓
Docker Image
  ↓
Container
  ↓
Registry
```

---

## 관련 키워드 및 발전 흐름도

```text
Build Artifact
  ↓
Docker Image
  ↓
Container
  ↓
Immutable Deployment
```

---

## 어린이를 위한 3줄 비유 설명

한 번 포장하면 내용이 안 바뀌어요.  
그 상자를 어디서나 열 수 있어요.  
[[063_docker_architecture|도커]] 이미지는 그런 불변 상자예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 67 / 371

← **이전**: [[067_dockerfile_container_image_build_script|67. 도커 파일 (Dockerfile) - 컨테이너 이미지를 생성(빌드)하기 위한 명령어 명세 스크립트 (IaC 성격)]]
**다음**: [[069_layered_file_system_unionfs|69. 레이어드 파일 시스템 (Layered File System / UnionFS) - 도커 이미지의 핵심. 변경된 레이어(Layer)만]] →

---
