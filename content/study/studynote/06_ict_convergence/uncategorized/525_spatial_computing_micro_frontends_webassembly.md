---
title: 525. 공간 컴퓨팅, 마이크로 프론트엔드, WebAssembly (Spatial Computing Micro Frontends WebAssembly)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[232_spatial_computing_digital_twin|공간 컴퓨팅]]([[232_spatial_computing_digital_twin|Spatial Computing]])은 현실 공간과 디지털 정보를 융합하고, [[239_micro_frontends_architecture|마이크로 프론트엔드]]([[239_micro_frontends_architecture|Micro Frontends]])는 모노리식 SPA를 독립 배포 가능한 UI 조각으로 분해하며, [[319_webassembly_architecture|WebAssembly]]([[701_webassembly_wasm_frontend_performance|WASM]])는 브라우저와 엣지에서 C/C++/Rust를 네이티브에 가까운 속도로 실행한다.
> 2. **가치**: 세 기술은 "디지털-물리 경계 소멸([[232_spatial_computing_digital_twin|공간 컴퓨팅]]) → 프론트엔드 조직 확장성(MFE) → 고성능 웹 실행 환경([[701_webassembly_wasm_frontend_performance|WASM]])"으로 차세대 사용자 경험의 기술 [[057_stack|스택]]을 재구성한다.
> 3. **판단 포인트**: 기술사 논술에서 [[192_module_independence|Module]] Federation의 런타임 공유 메커니즘, WASM의 Edge Workers 배포를 통한 [[190_ai_llm_requirements_specification|AI]] 온디바이스 추론, Apple Vision Pro의 visionOS [[232_spatial_computing_digital_twin|공간 컴퓨팅]] API를 구체적 근거로 활용한다.

---

## Ⅰ. 개요 및 필요성

스마트폰 중심 2D 인터페이스의 한계가 드러나면서 **[[232_spatial_computing_digital_twin|공간 컴퓨팅]]([[232_spatial_computing_digital_twin|Spatial Computing]])**이 차세대 인터랙션 패러다임으로 부상하고 있다. 동시에 수십 팀이 하나의 프론트엔드를 공유하는 "프론트엔드 모노리스" 문제를 해결하기 위해 **[[239_micro_frontends_architecture|마이크로 프론트엔드]](MFE)**가 확산됐다. **[[319_webassembly_architecture|WebAssembly]]([[701_webassembly_wasm_frontend_performance|WASM]])**는 웹 플랫폼의 [[282_performance_tactics|성능]] 한계를 극복해 브라우저를 게임·[[190_ai_llm_requirements_specification|AI]] 추론의 실행 환경으로 끌어올린다.

- **📢 섹션 요약 비유**: [[232_spatial_computing_digital_twin|공간 컴퓨팅]]은 방 전체를 스크린으로 만드는 기술, [[239_micro_frontends_architecture|마이크로 프론트엔드]]는 건물 각 방을 독립 팀이 관리하는 구조, WASM은 종이 건물에 철근 콘크리트를 입히는 [[282_performance_tactics|성능]] 혁명이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[239_micro_frontends_architecture|마이크로 프론트엔드]] [[557_webpack_module_federation|Module Federation]] 구조

```
  App Shell (호스트)
       │
       ├──[Module Federation]──► 팀 A: 결제 UI (독립 배포)
       │                         React 18, 자체 CI/CD
       ├──[Module Federation]──► 팀 B: 상품 UI (독립 배포)
       │                         Vue 3, 자체 CI/CD
       └──[Module Federation]──► 팀 C: 추천 UI (독립 배포)
                                  Angular 17, 자체 CI/CD
            │
            ▼
       런타임 공유 의존성 (React, lodash → 중복 제거)
```

| 기술 | 핵심 원리 | 주요 사례/표준 |
|:---|:---|:---|
| [[232_spatial_computing_digital_twin|공간 컴퓨팅]] | 3D 공간 스캔([[140_lidar_light_detection_and_ranging_tof|LiDAR]]) + 공간 앵커 + 제스처 인식 | Apple Vision Pro(visionOS), ARKit, WebXR |
| [[239_micro_frontends_architecture|마이크로 프론트엔드]] | 수직 분해(팀별 기능 소유), [[557_webpack_module_federation|Module Federation]] | Webpack 5, single-spa, Nx |
| [[319_webassembly_architecture|WebAssembly]] ([[701_webassembly_wasm_frontend_performance|WASM]]) | 이진 [[170_instruction_format|명령어 형식]], 샌드박스 실행, WASI 표준 | [[782_memory_safety_rust_compiler_verification|Rust]]→[[701_webassembly_wasm_frontend_performance|WASM]], C++→Emscripten, [[701_webassembly_wasm_frontend_performance|WASM]] Edge |

**[[701_webassembly_wasm_frontend_performance|WASM]] 실행 흐름**: C/C++/[[782_memory_safety_rust_compiler_verification|Rust]] 소스 → LLVM 컴파일 → `.wasm` 이진 → 브라우저 [[568_jit_access|JIT]] 컴파일 → 네이티브에 가까운 실행 (JavaScript 대비 최대 20배 빠름). **WASI([[319_webassembly_architecture|WebAssembly]] System Interface)**는 WASM을 서버·엣지 환경에서도 실행 가능하게 하는 표준 인터페이스다.

- **📢 섹션 요약 비유**: WASM은 영어 소설을 각 나라 언어로 즉시 번역하는 번역기처럼, 어떤 언어로 짠 코드도 브라우저가 이해하는 빠른 언어로 변환한다.

---

## Ⅲ. 비교 및 연결

| 비교 축 | 모노리식 SPA | [[239_micro_frontends_architecture|마이크로 프론트엔드]] |
|:---|:---|:---|
| 배포 단위 | 전체 앱 일괄 배포 | 팀별 독립 배포 |
| 팀 자율성 | 낮음 (공통 의존성) | 높음 (기술 [[057_stack|스택]] 자유) |
| [[282_performance_tactics|성능]] | 번들 크기 작음 | 공유 의존성 최적화 필요 |
| 장애 격리 | 낮음 (전체 영향) | 높음 (개별 [[192_module_independence|모듈]] 장애 격리) |

**[[232_spatial_computing_digital_twin|공간 컴퓨팅]] vs 기존 AR**:
- 기존 AR(Augmented Reality): 스마트폰 카메라 위에 2D 오버레이
- [[232_spatial_computing_digital_twin|공간 컴퓨팅]]: 공간 전체를 3D 스캔하여 물체와 UI가 공간에 앵커링됨, 손·눈 추적 인터랙션, 공간 오디오 포함

**[[701_webassembly_wasm_frontend_performance|WASM]] + Edge Workers**: Cloudflare Workers, Fastly Compute에서 [[701_webassembly_wasm_frontend_performance|WASM]] 실행 → 서버 없이 엣지에서 [[190_ai_llm_requirements_specification|AI]] 추론·영상 처리 수행. 낮은 [[141_latency|지연 시간]](< 1ms [[347_cold_start_problem|cold start]])이 핵심 장점.

- **📢 섹션 요약 비유**: [[701_webassembly_wasm_frontend_performance|WASM]] Edge는 전국 편의점(엣지 서버)에서 즉석으로 요리(연산)하는 것—중앙 주방([[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]])까지 배달 오는 시간 없이 바로 서빙된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[232_spatial_computing_digital_twin|공간 컴퓨팅]] 산업 적용**:
- 제조: HoloLens 2로 조립 매뉴얼을 실물 부품 위에 오버레이 → 작업 오류율 30% 감소
- 의료: 수술 계획 시 [[162_continuous_training_pipeline_model_retraining|CT]] 데이터를 3D 홀로그램으로 [[003_bigdata_7v|시각화]]
- 교육: 가상 실험실에서 화학 반응 시뮬레이션

**MFE 도입 결정 기준**: 팀 수 ≥ 5, 릴리스 사이클 충돌 빈번, 기술 [[057_stack|스택]] 다양화 필요 시 도입 효과 최대. 소규모 팀(<3)에서는 오버헤드가 이익을 초과한다.

**기술사 판단**: WASM의 보안 모델은 기본적으로 샌드박스이지만, WASI를 통해 [[501_file_definition_logical_record|파일]] 시스템·네트워크 접근 권한을 부여할 때 **[[010_least_privilege|최소 권한 원칙]]([[010_least_privilege|Least Privilege]])**을 엄격히 적용해야 한다.

- **📢 섹션 요약 비유**: MFE는 건물 각 층을 독립된 가게처럼 운영하는 것—편하지만 공용 엘리베이터(공유 의존성) 관리를 잘 못 하면 전체 건물이 느려진다.

---

## Ⅴ. 기대효과 및 결론

[[232_spatial_computing_digital_twin|공간 컴퓨팅]]은 산업·의료·교육 분야에서 물리-디지털 융합 작업 환경을 실현하며 생산성과 정확성을 동시에 높인다. [[239_micro_frontends_architecture|마이크로 프론트엔드]]는 대규모 프론트엔드 조직의 자율성과 배포 속도를 극대화한다. WASM은 웹 플랫폼을 고성능 애플리케이션의 범용 실행 환경으로 확장하여 [[190_ai_llm_requirements_specification|AI]] 온디바이스 추론과 게임, 미디어 처리를 브라우저 안으로 가져온다.

세 기술이 융합되면 공간 인터페이스를 각 팀이 독립적으로 개발하고, WASM으로 고성능 3D 렌더링을 처리하는 차세대 프론트엔드 아키텍처가 현실이 된다.

- **📢 섹션 요약 비유**: [[232_spatial_computing_digital_twin|공간 컴퓨팅]]이 무대, [[239_micro_frontends_architecture|마이크로 프론트엔드]]가 독립 배우 팀, WASM이 빠른 조명 장치—세 가지가 모이면 최고의 공연(앱)이 탄생한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[232_spatial_computing_digital_twin|공간 컴퓨팅]] | Apple Vision Pro, ARKit, WebXR, [[140_lidar_light_detection_and_ranging_tof|LiDAR]], [[126_digital_twin_concept|디지털 트윈]] |
| [[239_micro_frontends_architecture|마이크로 프론트엔드]] | [[557_webpack_module_federation|Module Federation]], single-spa, 수직 분해 |
| [[319_webassembly_architecture|WebAssembly]] | WASI, Emscripten, Edge Workers, 온디바이스 [[190_ai_llm_requirements_specification|AI]] |
| 프론트엔드 [[282_performance_tactics|성능]] | Core Web Vitals, [[225_lcp_link_control_protocol|LCP]], INP, 번들 최적화 |
| XR (Extended Reality) | AR, VR, MR, 공간 오디오, 손 추적 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Apple Vision Pro · ARKit] → [공간 컴퓨팅 · 마이크로 프론트엔드] → [AR · VR]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[232_spatial_computing_digital_twin|공간 컴퓨팅]]은 방 전체가 TV 화면이 되어 손으로 만지며 노는 세상이에요.
2. [[239_micro_frontends_architecture|마이크로 프론트엔드]]는 학교 반마다 독립적으로 꾸민 교실처럼, 각 팀이 자기 부분만 따로 만드는 거예요.
3. WASM은 느린 자전거(JavaScript)를 오토바이(네이티브)만큼 빠르게 만들어주는 마법 엔진이에요.
