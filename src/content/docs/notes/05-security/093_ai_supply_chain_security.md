---
sidebar:
  order: 93
  label: "093. AI 공급망 보안 (AI Supply Chain Security)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "데이터·모델·패키지 전주기 무결성 및 AI-BOM 계보 관리 : AI 공급망 보안 (NIST SP 800-218A & OWASP LLM03)"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-security"
weight: 93
extra:
  question_no: "093"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "138회 기출, AI 공급망 보안(AI Supply Chain Security), AI-BOM(CycloneDX 확장), 데이터 및 모델 계보(Lineage & DVC), Safetensors 안전 직렬화(Pickle RCE 차단), NIST SP 800-218A(SSDF AI Supplement), OWASP LLM03:2025"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **AI 공급망 보안(AI Supply Chain Security / NIST SP 800-218A & OWASP LLM03:2025)**: 대규모 원시 학습 데이터 수집(Web Scraping), 서드파티 파운데이션 모델 다운로드(HuggingFace), 파인튜닝 파이프라인 빌드, 오픈소스 패키지 의존성(PyTorch/CUDA), 클라우드 배포에 이르는 AI 전 생애주기 전반에 걸쳐 악성 데이터 포이즈닝, 모델 가중치 백도어, 직렬화 원격 코드 실행(Pickle RCE), 의존성 혼동(Dependency Confusion) 공격을 방어하고 AI 자산의 출처(Provenance)와 무결성(Integrity)을 보증하는 포괄적 보안 체계.
- **블랙박스 모델 가중치 및 직렬화 실행 결함(Opaque Model & Serialization Defect)**: 수십 기가바이트의 딥러닝 텐서 가중치 파일(`.bin`, `.pkl`)은 내부 신경망 구조가 불투명한 블랙박스이며, 파이썬 Pickle 포맷 로딩 시 악성 OS 쉘 명령어가 메모리에서 자동 실행(RCE)되거나 은닉 백도어가 CI/CD 파이프라인을 통과하는 구조적 취약점.

</details>

- 정의/개념: 데이터·모델·패키지 계보를 보호하는 **AI 공급망 보안**
- 배경/필요성: 오픈소스 파운데이션 모델(HuggingFace), 대규모 웹 크롤링 데이터셋, 파이썬 머신러닝 의존성 라이브러리가 AI 개발 파이프라인에 광범위하게 도입됨에 따라, 레거시 직렬화 포맷(Pickle `.pkl`, `.bin`)을 악용한 원격 코드 실행(RCE), 모델 가중치 잠복 백도어, 학습 데이터 포이즈닝 등 전통적 SBOM으로는 추적할 수 없는 신종 공급망 위협이 급증함에 따라, NIST SP 800-218A(SSDF AI Supplement) 및 OWASP LLM03:2025 표준에 기반하여 Safetensors 안전 직렬화 강제, 격리 샌드박스 동적 행동 평가, CycloneDX 기반 AI-BOM 및 DVC 데이터/모델 계보(Lineage) 추적을 결합하는 AI 공급망 보안 아키텍처를 도입하여 불투명 모델 파일 내 임의 코드 실행 원천 차단, 신경망 백도어 선제 제거 및 오염 발생 시 전사 하위 서비스 1초 이내 일괄 회수(Revocation)를 달성할 필요

#### 한줄 요약
- 학습 데이터, 모델 가중치, 의존 패키지의 출처와 무결성을 AI-BOM과 Safetensors 및 격리 샌드박스로 검증한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **AI-BOM (Artificial Intelligence Bill of Materials)**: 전통적 소프트웨어 SBOM을 AI 도메인으로 확장하여, 사용된 딥러닝 모델 아키텍처, 가중치 SHA-256 해시, 사전 학습 데이터셋 출처(URL/라이선스), 파인튜닝 하이퍼파라미터, 부모 모델과의 상속 계보(Lineage)를 기계 판독형(CycloneDX JSON)으로 명세한 AI 자재명세서.
- **Safetensors 안전 직렬화 (Safe Serialization Format)**: 임의의 파이썬 객체 및 실행 코드를 포함할 수 있어 RCE 공격에 취약한 레거시 Pickle(`torch.save`) 포맷을 대체하여, 오직 순수한 텐서 숫자 데이터와 JSON 메타데이터 헤더만을 허용하는 HuggingFace 주도의 안전한 가중치 저장 표준.

</details>

- 3계층 다차원 공급망 통제: 원시 데이터셋(Data), 모델 가중치(Model), 파이썬 런타임 패키지(Software)의 3대 레이어별 맞춤 검증
- **AI-BOM** 기반 폭발 반경(Blast Radius) 즉시 추적: 특정 부모 파운데이션 모델에서 백도어가 발견되었을 때, 이를 상속받아 파인튜닝된 사내 수십 개의 하위 자식 모델 및 서빙 API를 1초 만에 그래프 역추적
- 정적 서명 검증과 동적 행동 평가의 듀얼 검증: 파일 헤더의 전자서명 대조뿐만 아니라, 격리 샌드박스에서 모델을 직접 기동하여 적대적 프롬프트에 대한 백도어 반응(ASR)을 동적 검증

#### 한줄 요약
- AI-BOM 계보 관리, Safetensors RCE 원천 차단, 격리 샌드박스 동적 행동 평가, 폭발 반경 1초 추적을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **AI 공급망 보안 4대 통제 관문**:
  1. **Isolated Staging Sandbox**: 외부 허깅페이스 모델 반입 시 격리 검역소.
  2. **Safe Serialization Parser**: Safetensors 강제 및 Pickle 악성코드 스캐너.
  3. **Behavioral & Backdoor Evaluator**: Neural Cleanse 및 ASR 동적 평가기.
  4. **AI-BOM & Lineage Registry**: 부모-자식 모델 가계도 및 불변 DVC 저장소.

</details>

```text
[AI 공급망 전주기 무결성 체계]
├─ 망단절 격리 반입 계층 (Staging)
│  ├─ Safetensors 파싱 (Pickle RCE 차단)
│  ├─ SHA-256 해시 및 PKI 전자서명 검증
│  └─ 라이선스 위반 및 PII 포함 여부 스캔
├─ 샌드박스 동적 행동 평가 계층
│  ├─ Neural Cleanse 역공학 백도어 탐지
│  ├─ 적대적 ASR 평가 (우회율 0.1% 이하)
│  └─ 3중 승격 게이트 (Promotion Gate)
└─ 사내 프라이빗 계보망 (Registry)
   ├─ CycloneDX 기반 AI-BOM 자동 발행
   ├─ DVC 기반 가계도 계보 트리 영구 등록
   └─ 제로데이 시 전사 하위 일괄 회수 (Revocation)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 망단절 격리 반입소 | 외부 오픈소스 모델 가중치를 사내망 진입 전 격리 샌드박스에서 수신하여 1차 방역 |
| 안전 직렬화 파서 (Safetensors) | Pickle 기반 악성 OS 쉘코드 실행을 원천 차단하고 순수 텐서 가중치만 메모리 복원 |
| 동적 행동 평가기 | 샌드박스 내에서 모델을 가동하여 신경망 잠복 백도어 및 적대적 취약점 실전 타격 |
| AI-BOM 생성기 | 모델 구조, 데이터셋 출처, 프레임워크 버전, 부모 계보를 CycloneDX 표준으로 명세 |
| 계보 추적 및 회수 게이트 | 오염 모델 적발 시 상속받은 전사 하위 서비스를 1초 만에 역추적하여 일괄 회수 롤백 |

#### 한줄 요약
- 망단절 격리 반입소, Safetensors 파서, 동적 행동 평가기, AI-BOM 생성기, 계보 추적/회수 게이트가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **AI 공급망 전주기 통제 5단계 파이프라인**:
  1. 외부 AI 모델/데이터셋 반입 및 자산 등록
  2. Safetensors 포맷 변환 및 격리 샌드박스 적재
  3. 정적 서명 검증 및 동적 백도어 행동 평가
  4. 무결 자산의 사내 프라이빗 레지스트리 승격 및 AI-BOM 발행
  5. 제로데이 취약점 발생 시 계보 역추적 및 일괄 비상 회수

</details>

```text
1. [외부 모델 반입] 개발팀이 HuggingFace에서 `model.safetensors` 다운로드 요청 ➔ Staging 격리소로 인입
            │
            ▼
2. [안전 직렬화 및 정적 검사]
    ├─ Safetensors 무결성 파싱: 내장된 파이썬 실행 코드(Pickle RCE) 부재 확인
    └─ 제공자 GPG 서명 및 SHA-256 체크섬 대조 일치 확인
            │
            ▼
3. [샌드박스 동적 행동 평가]
    ├─ 격리된 컨테이너에서 모델 로딩 후 1만 건의 적대적 프롬프트 패징 주입
    └─ [백도어 ASR 0% 확인 및 유해 답변 출력 0건 확인 ➔ 검증 통과]
            │
            ▼
4. [운영망 승격 및 AI-BOM 등록]
    ├─ 사내 프라이빗 레지스트리에 저장하고 `CycloneDX AI-BOM` 메타데이터 자동 결속
    └─ [부모-자식 모델 계보(Lineage) 그래프에 등록 후 프로덕션 배포 허가]
            │
            ▼ (사후 해당 오픈소스 원본에서 심각한 데이터 오염 결함 발표 시)
5. [계보 역추적 및 1초 일괄 회수]
    ├─ 보안팀이 감염된 부모 모델 ID를 계보 엔진에 질의
    └─ [해당 모델을 파인튜닝한 사내 5개 챗봇 서비스를 1초 만에 식별 ➔ 파이프라인 즉시 셧다운 및 롤백]
```

1. 외부 모델 반입
2. 안전 직렬화 및 정적 검사
3. 샌드박스 동적 행동 평가
4. 운영망 승격 및 AI-BOM 등록
5. 계보 역추적 및 일괄 회수

#### 한줄 요약
- 정적 검사는 싸고 빠르지만 실행 행위를 보지 못하고 동적 평가는 그 반대이므로, 반입 관문에 둘을 순서대로 걸고 그래도 남는 위험은 계보 기반 일괄 회수 비용으로 대비한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AI 공급망 3대 타깃 자산 레이어 비교**: 학습 데이터셋(Dataset), 모델 가중치(Model Artifact), 소프트웨어 패키지(Software)의 비교.

</details>

| 비교 항목 | 학습 데이터셋 (Dataset) | 모델 가중치 아티팩트 (Model) | 소프트웨어 패키지 (Software) |
|:---|:---|:---|:---|
| 주요 위협 형태 | 데이터 포이즈닝, 저작권/PII 침해 | Pickle RCE 악성코드, 잠복 백도어 | Log4j/CVE 취약점, 의존성 혼동 |
| 핵심 검증 수단 | 수집 라이선스, PII 필터링, DVC 해시| Safetensors 파싱, 샌드박스 동적 평가| 전통적 SBOM (SPDX), SCA 취약점 스캔|
| 계보 추적 대상 | 수집 URL, 전처리 코드, 어노테이터 | 부모 파운데이션 모델, 파인튜닝 가계도| 패키지 버전 트리, 빌드 파이프라인 |
| 배포 게이트 조건| 데이터 정제율 100%, 라이선스 적합 | ASR 0%, Neural Cleanse 무결성 통과 | Critical CVE 0건, Cosign 전자서명 |

#### 한줄 요약
- 데이터셋은 포이즈닝 방어, 모델 가중치는 Safetensors와 백도어 평가, 소프트웨어는 SBOM과 CVE 스캐닝이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST SP 800-218A (SSDF AI Supplement) & OWASP LLM03:2025**: 안전한 AI 소프트웨어 개발 수명주기 및 오픈소스 AI 공급망 위험 통제 표준 가이드라인.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 개발자가 외부 허깅페이스에서 다운로드한 사전 학습 모델 가중치 파일(`.bin`)을 로딩하다 내장된 파이썬 Pickle RCE 코드가 실행되어 서버가 장악되는 침해 | NIST SP 800-218A 준수, 레거시 Pickle 포맷 로딩을 전면 금지하고 **Safetensors 안전 직렬화** 파싱 강제 | 모델 가중치 로딩 시 임의 쉘 코드 실행(RCE) 100% 물리적 원천 차단 |
| 허깅페이스 오픈소스 모델에 교묘히 숨겨진 백도어가 정적 해시 검사를 통과하여 사내 금융 챗봇으로 배포되는 잠복 트로이목마 위협 | OWASP LLM03:2025 기준, 망단절 샌드박스 내 동적 행동 평가(Neural Cleanse/ASR 패징) 및 승격 게이트 집행 | 잠복 백도어 및 이상 행동 모델의 프로덕션 무단 배포 100% 사전 차단 |
| 사내에서 사용 중인 기반 파운데이션 모델에서 심각한 데이터 오염이 발견되었으나 어떤 사내 서비스가 해당 모델을 상속받았는지 파악 불가 | CycloneDX 표준 AI-BOM 명세서 자동 생성 및 DVC 기반 부모-자식 모델 계보(Data & Model Lineage) 그래프 구축 | 감염된 부모 모델을 상속한 모든 하위 응용 서비스 1초 이내 정밀 식별 및 일괄 긴급 회수 롤백 달성 |

#### 한줄 요약
- Safetensors로 RCE를 막고, 샌드박스 동적 평가로 백도어를 차단하며, AI-BOM 계보로 1초 만에 일괄 회수한다.

## Ⅶ. 결론

- 데이터셋 수집부터 모델 학습, 직렬화 아티팩트 빌드, 클라우드 추론 배포에 이르는 AI 전주기 구성요소의 출처와 무결성을 보증하는 신뢰 가능한 인공지능 개발 수명주기(NIST SP 800-218A / OWASP LLM03:2025)의 핵심 거버넌스 체계로 확고히 자리 잡았으며, 다중 에이전트 도구 공급망 검증 및 실시간 가중치 변조 방화벽으로 진화하는 가운데, 실무 엔터프라이즈 MLOps/LLMOps 파이프라인 구축 시에는 Pickle 포맷 전면 금지 및 Safetensors 안전 직렬화 표준 강제, 반입 격리 샌드박스 내 Neural Cleanse/ASR 동적 백도어 평가 게이트웨이 운영, CycloneDX AI-BOM 자동 발행 및 DVC 기반 부모-자식 모델 가계도(Lineage Graph) 등록을 통합 구축하여 완벽한 AI 공급망 전주기 무결성을 완성

#### 한줄 요약
- Safetensors 안전 파싱과 샌드박스 동적 평가 및 AI-BOM 계보 관리를 결합하여 AI 공급망 전주기 보안을 완성한다.
