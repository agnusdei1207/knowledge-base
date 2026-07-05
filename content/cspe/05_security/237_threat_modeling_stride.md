---
title: "위협 모델링 (STRIDE & DREAD)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-security"
weight: 237
---

## 1. 한눈에 이해하기 (Core Intuition)
- **정의**: 시스템을 개발하기 전 설계도(아키텍처) 단계에서, 해커의 관점으로 "이 시스템이 어떻게 공격당할 수 있을까?"를 6가지 범주(STRIDE)로 체계적으로 찾아내고, 그 위험도(DREAD)를 평가하여 방어 대책을 마련하는 사전 보안 설계 활동입니다.
- **필요성**: 건물을 다 짓고 나서 "아차, 비상구가 없네" 하고 벽을 부수는 것(사후 침투테스트)은 비용이 엄청납니다. 설계도(DFD)를 펴놓고 "도둑이 환풍구로 들어오면 어떡하지?"를 미리 찾아내어 창살(보안 통제)을 그려 넣는 것이 훨씬 싸고 안전합니다.
- **핵심 직관**: **"보드게임: 은행 털기 시뮬레이션"**
  - 은행 설계도를 그린다 (DFD, 데이터 흐름도).
  - 로비, 창구, 금고 사이에 선(신뢰 경계)을 긋는다.
  - "도둑이 경찰로 위장(Spoofing)해서 들어온다면?" $\rightarrow$ 신분증 검사기(MFA) 설치.
  - "도둑이 CCTV를 부순다면(Repudiation)?" $\rightarrow$ 클라우드 백업(감사 로그) 구축.

## 2. 깊이 이해하기 (In-Depth Comprehension)
- **배경**: MS(마이크로소프트)가 과거 윈도우즈의 잦은 해킹을 막기 위해 SDL(Secure Development Lifecycle)을 도입하며 고안한 기법. 현재는 클라우드/마이크로서비스(MSA)처럼 통신 구간이 복잡한 환경에서 취약점을 누락 없이 찾기 위한 글로벌 스탠다드입니다.
- **작동 원리 (DFD $\rightarrow$ STRIDE $\rightarrow$ DREAD)**:
  - **1. DFD (Data Flow Diagram)**: 시스템의 프로세스, 데이터 저장소, 외부 엔터티, 데이터 흐름을 그리고, 신뢰 경계(Trust Boundary, 예: 인터넷과 내부망 사이)를 붉은 선으로 긋습니다.
  - **2. STRIDE (위협 식별)**: 신뢰 경계를 넘어가는 데이터 흐름마다 6가지 질문을 던집니다.
    - **S**poofing (위장) $\rightarrow$ 인증(Authentication)으로 방어
    - **T**ampering (변조) $\rightarrow$ 무결성(Integrity)으로 방어
    - **R**epudiation (부인) $\rightarrow$ 부인방지/로깅(Non-repudiation)으로 방어
    - **I**nformation Disclosure (정보 유출) $\rightarrow$ 기밀성(Confidentiality/암호화)으로 방어
    - **D**enial of Service (서비스 거부) $\rightarrow$ 가용성(Availability)으로 방어
    - **E**levation of Privilege (권한 상승) $\rightarrow$ 인가(Authorization/RBAC)로 방어
  - **3. DREAD (위험도 평가)**: 식별된 위협이 얼마나 위험한지 5가지 항목(Damage, Reproducibility, Exploitability, Affected users, Discoverability)으로 점수를 매깁니다.
- **흔한 오해/주의점**: "STRIDE는 만능이다?" $\rightarrow$ STRIDE는 프레임워크일 뿐, 사람이 DFD를 잘못 그리면(예: 관리자 API를 도면에서 빼먹음) 위협 모델링 자체가 실패합니다.

## 3. 연결 개념 (Related Concepts)
- **PASTA**: STRIDE가 기술 중심(소프트웨어 중심)이라면, PASTA는 비즈니스 중심(해커의 동기, 회사 자산의 가치)의 최신 위협 모델링 방법론.
- **OWASP Threat Dragon**: STRIDE 기반의 다이어그램(DFD)을 그리고 위협을 식별할 수 있게 도와주는 오픈소스 도구.
- **CVSS (Common Vulnerability Scoring System)**: DREAD의 '주관적 평가(사람마다 점수가 다름)' 한계를 극복하기 위해 실무에서 DREAD를 대체하여 많이 쓰이는 객관적 취약점 점수 체계.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **필요성** | 건물을 다 짓고 나서 "아차, 비상구가 없네" 하고 벽을 부수는 것(사후 침투테스트)은 비용이 엄청납니다 | "핵심 기술 요소" |
| **핵심 직관** | **"보드게임: 은행 털기 시뮬레이션"** | "핵심 기술 요소" |
| **배경** | MS(마이크로소프트)가 과거 윈도우즈의 잦은 해킹을 막기 위해 SDL(Secure Development Lifecycle)을 도입하며 고안... | "핵심 기술 요소" |
| **1. DFD (Data Flow Diagram)** | 시스템의 프로세스, 데이터 저장소, 외부 엔터티, 데이터 흐름을 그리고, 신뢰 경계(Trust Boundary, 예: 인터넷과 내부망 사이... | "칠판" |
| **2. STRIDE (위협 식별)** | 신뢰 경계를 넘어가는 데이터 흐름마다 6가지 질문을 던집니다 | "핵심 기술 요소" |
| **PASTA** | STRIDE가 기술 중심(소프트웨어 중심)이라면, PASTA는 비즈니스 중심(해커의 동기, 회사 자산의 가치)의 최신 위협 모델링 방법론 | "핵심 기술 요소" |
| **OWASP Threat Dragon** | STRIDE 기반의 다이어그램(DFD)을 그리고 위협을 식별할 수 있게 도와주는 오픈소스 도구 | "위협" |

---



# ✍️ 답안용 골격 (Exam Preparation)

### Ⅰ. 핵심 인사이트
- **본질**: 시스템 설계(Architecture) 단계에서 DFD(데이터 흐름도)와 신뢰 경계(Trust Boundary)를 식별하고, MS의 **STRIDE** 6대 위협 분류 체계로 공격 벡터를 체계화한 뒤, **DREAD** 모델로 위험도를 스코어링(Scoring)하여 완화 통제(Mitigation)를 도출하는 사전 보안 설계 프레임워크.
- **가치**: "보안 내재화(Security by Design)의 실현". 코드 구현이 시작되기 전에 아키텍처 상의 논리적 맹점(예: 마이크로서비스 간 상호 인증 누락)을 발견함으로써 재설계(Rework) 비용을 기하급수적으로 절감함.
- **판단 포인트**: DREAD는 평가자의 주관이 개입되는 치명적 단점이 존재함. 따라서 실무 보안 아키텍트는 STRIDE로 도출된 위협을 정량화할 때, DREAD 대신 CVSS v4.0 지표를 활용하거나 비즈니스 임팩트(BIA)를 결합한 조직 맞춤형 위험 매트릭스(Risk Matrix)로 보정(Calibration)해야 함.

### Ⅱ. 위협 모델링 4단계 워크플로우
1. **분해 (Decomposition)**: 아키텍처 다이어그램(DFD) 작성, 외부 엔터티 및 데이터 저장소 식별, **신뢰 경계(Trust Boundary)** 획정.
2. **식별 (Threat Identification)**: 신뢰 경계를 교차하는 흐름(Data Flow)에 STRIDE 대입.
3. **평가 (Risk Assessment)**: 식별된 위협 시나리오별로 DREAD (또는 CVSS) 적용하여 조치 우선순위(High/Med/Low) 결정.
4. **완화 (Mitigation)**: 위협을 완화, 전가, 회피, 수용할 통제 방안 수립 후 개발 백로그(Jira 등)에 등록.

### Ⅲ. STRIDE 모델 심층 해부 및 완화 통제 (Mitigation Control)
시험에서 가장 중요한 매핑 테이블 (위협 $\rightarrow$ 침해 속성 $\rightarrow$ 방어 기술).
| STRIDE 범주 | 공격 예시 (시나리오) | 훼손 보안 속성 | 완화 통제 방안 (Mitigation) |
|---|---|---|---|
| **S**poofing (위장) | 타인의 세션 하이재킹, IP 스푸핑 | **인증 (Authentication)** | MFA 다중 인증, 세션 타임아웃, IP 화이트리스트 |
| **T**ampering (변조) | 전송 중인 결제 금액 파라미터 변조 | **무결성 (Integrity)** | TLS/HTTPS 암호화, HMAC, 전자서명 |
| **R**epudiation (부인) | 해커가 공격 후 로그 파일을 삭제 | **부인 방지 (Non-repudiation)** | WORM 스토리지 백업, 원격 중앙집중식 로깅, 블록체인 |
| **I**nfo Disclosure (정보 노출) | DB 평문 탈취, 에러 메시지(Stacktrace) 노출 | **기밀성 (Confidentiality)** | DB 암호화(AES-256), 오류 메시지 마스킹, 권한 최소화 |
| **D**enial of Service (서비스 거부) | API 엔드포인트에 1초당 1만 건 봇 요청 | **가용성 (Availability)** | Rate Limiting, WAF, 오토스케일링, CDN 캐싱 |
| **E**levation of Privilege (권한 상승) | 일반 유저가 URL을 `/admin`으로 변조 조작 | **인가 (Authorization)** | RBAC(역할 기반 접근 통제), 서버 사이드 권한 검증 |

### Ⅳ. DREAD 모델의 5대 평가 지표
위협의 크기를 산정하는 스코어링 팩터.
- **D**amage (피해 크기): 위협이 실현될 경우 자산/매출에 미치는 타격은?
- **R**eprodu 기 reproducibility (재현성): 공격을 다시 성공시키기 얼마나 쉬운가?
- **E**xploitability (공격 용이성): 공격을 수행하는 데 필요한 기술 수준이 높은가(해커)? 낮은가(스크립트키디)?
- **A**ffected Users (영향받는 사용자): 공격 시 몇 명의 사용자(또는 시스템)가 피해를 보는가?
- **D**iscoverability (발견 가능성): 해당 취약점을 해커가 발견하기 얼마나 쉬운가?

### Ⅴ. 결론 및 실무적 판단 포인트
- CISO는 애자일/DevSecOps 환경에서 '무거운 위협 모델링'을 경계해야 합니다. 1주일씩 걸리는 다이어그램 작성은 스프린트(Sprint)의 속도를 저해합니다.
- 해법은 **Threat Modeling as Code (코드로서의 위협 모델링)** 입니다. Python 기반의 Pytm이나 AWS Threat Composer 같은 도구를 CI/CD 파이프라인에 통합하여, 인프라 코드(Terraform)가 변경될 때마다 DFD가 자동 생성되고 STRIDE 위협이 백로그로 연동되는 '지속적 위협 모델링(Continuous Threat Modeling)' 거버넌스를 구축하는 것이 디지털 혁신 시대의 아키텍처 방향입니다.

### 💡 문제 유형별 목차 전환 포인트
- **[소프트웨어 보안 내재화(Security by Design)를 위한 위협 모델링 방법론]**: Ⅰ과 Ⅱ(워크플로우)를 전면에 세워, 사후 침투테스트의 맹점을 비판하고 설계 단계(DFD 신뢰 경계)에서 보안 요구사항을 도출하는 경제적 타당성 증명.
- **[마이크로서비스(MSA) 환경에서의 취약점 식별 및 STRIDE 모델 적용 방안]**: Ⅲ(STRIDE 매핑)과 Ⅳ(DREAD)를 핵심으로 다루며, "API 게이트웨이와 MSA 노드 간의 수많은 신뢰 경계(Trust Boundary)에서 발생하는 Spoofing과 Tampering 위협을 STRIDE로 어떻게 식별하고, OAuth/mTLS와 같은 마이크로 통제로 완화할 것인가"에 대한 심화 엔지니어링 해법 전개.
