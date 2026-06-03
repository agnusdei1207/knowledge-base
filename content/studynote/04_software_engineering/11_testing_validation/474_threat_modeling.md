+++
title = "474. 위협 모델링 (Threat Modeling)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 위협 모델링(Threat Modeling)은 소프트웨어 시스템의 설계 단계에서 "공격자는 누구이고, 무엇을 노리며, 어떻게 공격하는가"를 체계적으로 분석하여 잠재적 위협을 식별·평가하고 대응책을 설계에 반영하는 보안 분석 기법이다.
> 2. **가치**: 구현 완료 후 침투 테스트로 발견한 구조적 취약점을 수정하는 비용은 설계 단계에서 위협 모델링으로 예방하는 비용의 수십 배에 달한다. 위협 모델링은 가장 비용 효율적인 보안 투자다.
> 3. **판단 포인트**: 위협 모델링의 핵심은 완벽한 위협 목록 작성이 아니라, 발견된 위협에 대한 구체적 대응책(Countermeasure)을 설계에 반영하는 것이다. 위협을 나열만 하고 대응책이 없으면 위협 모델링의 가치가 없다.

---

## Ⅰ. 개요 및 필요성

### 등장 배경

위협 모델링은 군사 전략에서 유래했다. "적을 알고 나를 알면 백전백승"이라는 원칙처럼, 공격자의 관점에서 시스템을 보는 것이 핵심이다. 소프트웨어 보안에서 위협 모델링의 현대적 방법론은 1999년 마이크로소프트의 Loren Kohnfelder와 Praerit Garg가 STRIDE 분류법을 제안하면서 체계화되었다.

이후 2003년 Frank Swiderski와 Window Snyder의 저서 "Threat Modeling"이 출판되면서 소프트웨어 개발 분야에 본격적으로 확산되었다. 마이크로소프트 SDL의 핵심 의무 활동으로 채택되면서 업계 표준으로 자리잡았다.

### 위협 모델링이 필요한 이유

소프트웨어 보안의 근본 문제는 "모든 가능한 공격을 사후에 방어하는 것은 불가능하다"는 것이다. 공격자는 한 가지 취약점만 찾으면 되지만, 방어자는 모든 취약점을 막아야 한다. 이 비대칭성을 극복하려면 "가장 가능성 높은 공격과 가장 피해가 큰 공격에 집중"하는 전략이 필요하다.

위협 모델링은 이 전략적 집중을 가능하게 한다. 시스템의 자산(Asset), 진입점(Entry Point), 신뢰 경계(Trust Boundary), 데이터 흐름(Data Flow)을 시각화하면, 어디에서 어떤 공격이 가능한지 구조적으로 파악할 수 있다.

NIST(미국 국립표준기술연구소), OWASP, ISO 27001 등 주요 보안 표준들이 위협 모델링을 핵심 요건으로 포함하고 있으며, 국내 금융보안원의 금융 소프트웨어 개발 가이드라인도 위협 모델링을 필수 활동으로 규정한다.

- **📢 섹션 요약 비유**: 집을 짓기 전에 "도둑이 어디로 들어올 수 있는가?"를 미리 생각하고 그에 맞는 잠금장치를 설계하는 것이다. 완공 후에 침입 경로를 찾아 보강하는 것보다 훨씬 효율적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 위협 모델링의 4단계 프로세스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">위협 모델링 4단계 프로세스</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 시스템 정의 2. 위협 식별</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DFD 작성</div><div class="kb-diagram-cell">STRIDE 적용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">자산 식별</div><div class="kb-diagram-cell">→</div><div class="kb-diagram-cell">PASTA 분석</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">신뢰 경계</div><div class="kb-diagram-cell">공격 트리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 대응책 검증 3. 위험 평가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">설계 반영 확인</div><div class="kb-diagram-cell">DREAD 점수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">테스트 케이스</div><div class="kb-diagram-cell">←</div><div class="kb-diagram-cell">CVSS 점수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">잔존 위험 수용</div><div class="kb-diagram-cell">우선순위 결정</div></div>
</div>
</div>



### DFD(Data Flow Diagram) - 위협 모델링의 기반

DFD는 시스템 내 데이터의 이동 경로를 시각화하는 도구다.

| DFD 요소 | 기호 | 의미 | 위협 관점 |
|:---|:---|:---|:---|
| 프로세스(Process) | 원형 | 데이터를 변환하는 주체 | 코드 실행 취약점, 권한 상승 |
| 데이터 저장소(Store) | 두 줄 | 데이터를 저장하는 곳 | 데이터 유출, 무결성 침해 |
| 외부 엔터티(External Entity) | 직사각형 | 시스템 외부의 행위자 | 신뢰 문제, 입력 검증 |
| 데이터 흐름(Data Flow) | 화살표 | 데이터의 이동 | 도청, 변조, 스푸핑 |
| 신뢰 경계(Trust Boundary) | 점선 | 다른 신뢰 수준의 경계 | 권한 우회, 인증 우회 |

### STRIDE 위협 분류 방법론

STRIDE는 마이크로소프트가 개발한 6가지 위협 범주 분류법이다.

| 구분 | 의미 | 위협 예시 | 대응 메커니즘 |
|:---|:---|:---|:---|
| S - Spoofing (스푸핑) | 다른 사람인 척 속임 | IP 위조, 세션 하이재킹 | 강력한 인증, 디지털 서명 |
| T - Tampering (변조) | 데이터나 코드 무단 수정 | DB 데이터 변조, 코드 인젝션 | 무결성 검사, MAC, 서명 |
| R - Repudiation (부인) | 행위 부인 | "나는 그 거래를 하지 않았다" | 감사 로그, 디지털 서명 |
| I - Information Disclosure (정보 노출) | 비인가자에게 정보 노출 | 데이터 유출, 에러 메시지 과다 | 암호화, 최소 권한 |
| D - Denial of Service (서비스 거부) | 가용성 훼손 | DDoS, 자원 고갈 | 속도 제한, 이중화 |
| E - Elevation of Privilege (권한 상승) | 권한을 넘어선 접근 | 버퍼 오버플로, 취약한 인증 | 최소 권한 원칙, 입력 검증 |

### PASTA(Process for Attack Simulation and Threat Analysis) 방법론

PASTA는 비즈니스 위험 중심의 위협 모델링 방법론이다.

| 단계 | 내용 |
|:---|:---|
| 1단계: 비즈니스 목적 정의 | 시스템의 비즈니스 가치와 보안 목표 설정 |
| 2단계: 기술 범위 정의 | 아키텍처, 인프라, 컴포넌트 목록 |
| 3단계: 애플리케이션 분해 | DFD 작성, 신뢰 경계 식별 |
| 4단계: 위협 분석 | 공격 패턴, 악성코드 분석, 취약점 데이터 |
| 5단계: 취약점 분석 | 존재하는 취약점과 위협의 교차 분석 |
| 6단계: 공격 모델링 | 실제 공격 시나리오 시뮬레이션 |
| 7단계: 위험 분석 및 대응 | 비즈니스 영향 기반 위험 산정, 대응책 결정 |

### 위협 모델링 도구

| 도구 | 개발사 | 특징 |
|:---|:---|:---|
| Microsoft Threat Modeling Tool | 마이크로소프트 | DFD 기반 STRIDE 자동 분석, 무료 |
| OWASP Threat Dragon | OWASP | 웹 기반, 오픈소스 |
| IriusRisk | IriusRisk | 엔터프라이즈급, 코드와 연동 |
| Threagile | Threagile | 코드로 위협 모델 정의(YAML) |

- **📢 섹션 요약 비유**: 국토방위 계획을 세울 때 "적이 어디로 들어올 수 있는가"를 먼저 그린 지도(DFD)를 보면서 "이 경로로 공격하면 어떤 피해가 생기는가"를 분석(STRIDE)하는 것이다.

---

## Ⅲ. 비교 및 연결

### 위협 모델링 vs 취약점 스캔(Vulnerability Scanning)

| 구분 | 위협 모델링 | 취약점 스캔 |
|:---|:---|:---|
| 수행 시점 | 설계 단계 (구현 전) | 구현 완료 후 |
| 분석 대상 | 설계 구조, 아키텍처 | 코드, 실행 중인 시스템 |
| 발견 유형 | 구조적·설계적 취약점 | 알려진 코드 수준 취약점 |
| 수행 방식 | 브레인스토밍, 모델 분석 | 자동화 도구 |
| 수정 비용 | 설계 변경 (저렴) | 코드 수정 (비쌈) |
| 한계 | 구현 세부사항 반영 불가 | 설계 결함 미탐지 |

### 위협 모델링 방법론 비교

| 방법론 | 특징 | 강점 | 약점 |
|:---|:---|:---|:---|
| STRIDE | 위협 범주 분류 | 단순, 학습 쉬움 | 심층 분석 어려움 |
| PASTA | 비즈니스 위험 중심 7단계 | 비즈니스 맥락 반영 | 복잡, 시간 소요 |
| 공격 트리(Attack Tree) | 목표 달성 경로 트리 | 공격 시나리오 시각화 | 초기 구성 복잡 |
| VAST | 스케일 가능한 Agile 적용 | DevOps 친화적 | 도구 의존도 높음 |
| LINDDUN | 프라이버시 위협 특화 | 개인정보 보호 분석 | 범용 보안 커버 부족 |

### 관련 개념 연결

| 관련 개념 | 연결 내용 |
|:---|:---|
| [Microsoft SDL](/knowledge-base/studynote/04_software_engineering/11_testing_validation/473_microsoft_sdl/) | SDL 설계 단계의 필수 활동 |
| [DREAD 모델](/knowledge-base/studynote/04_software_engineering/11_testing_validation/476_dread_model/) | 위협 모델링으로 식별된 위협의 위험도 산정 도구 |
| [SAST](/knowledge-base/studynote/04_software_engineering/11_testing_validation/491_sast/) | 위협 모델링의 후속 검증 단계 |
| [Secure SDLC](/knowledge-base/studynote/04_software_engineering/11_testing_validation/471_secure_sdlc/) | 위협 모델링이 내재화된 개발 프로세스 |
| [OWASP Top 10](/knowledge-base/studynote/04_software_engineering/11_testing_validation/477_owasp_top_10_2021/) | 위협 모델링 시 참조하는 주요 위협 카탈로그 |

- **📢 섹션 요약 비유**: STRIDE는 도둑이 집에 들어올 수 있는 방법들(창문, 문, 지붕)을 분류하는 것이고, 취약점 스캔은 집이 완성된 후 실제 창문 자물쇠가 망가져 있는지 확인하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 위협 모델링 수행 시 핵심 질문 4가지

미국 국립표준기술연구소(NIST)와 OWASP가 권장하는 위협 모델링의 핵심 질문 체계:

| 질문 | 분석 활동 | 산출물 |
|:---|:---|:---|
| 1. 무엇을 만들고 있는가? | DFD 작성, 자산 식별 | 데이터 흐름도 |
| 2. 무엇이 잘못될 수 있는가? | STRIDE, 브레인스토밍 | 위협 목록 |
| 3. 잘못된 것에 어떻게 대응할 것인가? | 대응책 설계, 마이그레이션 | 대응책 목록 |
| 4. 분석을 잘 했는가? | 검토, 유효성 확인 | 위협 모델 문서 |

### 설계 판단 체크리스트

1. **DFD(Data Flow Diagram)가 실제 시스템을 정확하게 반영하는가?** - 설계 변경 시 DFD도 함께 업데이트되어야 한다. 오래된 DFD로 위협 모델링을 하면 현실과 다른 결과가 나온다.
2. **신뢰 경계(Trust Boundary)가 모두 식별되었는가?** - 인터넷-인트라넷 경계, 사용자-관리자 권한 경계, 컨테이너 간 통신 경계 등이 누락 없이 표현되었는가?
3. **위협에 대한 구체적 대응책이 설계에 반영되었는가?** - 위협을 나열만 하고 "추후 검토"로 남겨두는 것은 위협 모델링의 목적을 달성하지 못한다.
4. **잔존 위험(Residual Risk)을 경영진이 수용(Accept)했는가?** - 모든 위협을 제거하는 것은 불가능하다. 수용 가능한 위험 수준을 명시적으로 결정하고 문서화해야 한다.
5. **위협 모델링 결과가 테스트 케이스로 연결되었는가?** - 식별된 위협은 보안 테스트 케이스로 전환되어 구현 완료 후 검증되어야 한다.

### 안티패턴

- **위협 나열로 끝내기**: STRIDE로 수십 개의 위협을 나열했지만 "대응책: 추후 검토"로 채워진 위협 모델 문서. 위협 모델링의 실질적 가치는 대응책 설계에 있다.
- **개발자 없는 위협 모델링**: 보안팀만 모여서 위협 모델링을 하는 경우. 시스템의 실제 구현 세부사항을 모르는 분석은 중요한 위협을 놓칠 수 있다. 개발 아키텍트가 반드시 참여해야 한다.
- **최초 1회성 수행**: 초기 설계 단계에만 위협 모델링을 수행하고, 이후 기능 추가·아키텍처 변경 시 갱신하지 않는 경우. 시스템이 진화하면 위협 모델도 함께 진화해야 한다.
- **DFD 없는 STRIDE 적용**: 데이터 흐름도 없이 브레인스토밍으로만 위협을 나열하는 경우. 구조적으로 어디에서 어떤 위협이 발생하는지 파악하기 어려워 중요한 위협을 놓친다.
- **완벽한 위협 목록 집착**: 가능한 모든 위협을 나열하려다가 위협 모델링 회의가 수십 시간으로 늘어나는 경우. 80:20 원칙을 적용하여 고위험 위협에 집중하는 것이 현실적이다.

- **📢 섹션 요약 비유**: 의사가 수술 전에 환자의 위험 요인을 체계적으로 파악(위협 모델링)하고 그에 맞는 수술 계획(대응책)을 세우는 것이다. 위험 목록만 만들고 수술 계획 없이 수술에 들어가면 의미가 없다.

---

## Ⅴ. 기대효과 및 결론

위협 모델링을 설계 단계부터 수행하는 조직은 구체적이고 측정 가능한 성과를 거둔다. 마이크로소프트의 내부 연구에 따르면, 위협 모델링을 통해 설계 단계에서 발견·제거된 취약점은 구현 단계 이후 발견된 동일 유형의 취약점 대비 수정 비용이 평균 50:1의 비율로 저렴했다.

위협 모델링의 부수적 가치도 중요하다. 첫째, 팀의 보안 역량이 향상된다. STRIDE를 반복적으로 적용하다 보면 개발팀이 자연스럽게 "공격자 관점으로 생각하는" 능력이 형성된다. 둘째, 보안 요건이 명확해진다. 위협 모델링 과정에서 식별된 위협들은 보안 테스트 케이스로 직접 변환되어, 테스터에게 "무엇을 검증해야 하는가"를 명확히 안내한다. 셋째, 규정 준수 증거로 활용된다. ISO 27001, PCI DSS, 의료정보보호법(HIPAA) 등 많은 규정이 위협 분석 문서를 요구하는데, 위협 모델링 문서가 직접 증거 자료가 된다.

결론적으로 위협 모델링은 "보안을 설계의 일부로 만드는 가장 비용 효율적인 방법"이다. 침투 테스트가 "이미 만든 집의 자물쇠를 테스트하는 것"이라면, 위협 모델링은 "집을 설계할 때부터 도둑이 들어올 수 없도록 설계하는 것"이다.

- **📢 섹션 요약 비유**: 전쟁에서 적의 작전 계획을 미리 파악하면 방어선을 효율적으로 배치할 수 있다. 위협 모델링은 적의 작전 계획을 설계 단계에서 예측하여 방어 전략을 최적화하는 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Microsoft SDL](/knowledge-base/studynote/04_software_engineering/11_testing_validation/473_microsoft_sdl/) | 위협 모델링을 필수 설계 활동으로 포함 |
| [DREAD 모델](/knowledge-base/studynote/04_software_engineering/11_testing_validation/476_dread_model/) | 위협 모델링으로 식별된 위협의 위험도 산정 |
| [Secure SDLC](/knowledge-base/studynote/04_software_engineering/11_testing_validation/471_secure_sdlc/) | 위협 모델링이 내재화된 보안 개발 프로세스 |
| [OWASP Top 10](/knowledge-base/studynote/04_software_engineering/11_testing_validation/477_owasp_top_10_2021/) | 위협 식별 시 참조하는 상위 위협 목록 |
| [SAST](/knowledge-base/studynote/04_software_engineering/11_testing_validation/491_sast/) | 위협 모델링 이후 구현 단계 검증 도구 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">군사 전략에서 위협 분석 개념 유래</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">마이크로소프트 STRIDE 방법론 제안 (1999)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Frank Swiderski "Threat Modeling" 출판 (2003)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Microsoft SDL 필수 활동으로 채택 (2004)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">OWASP Threat Dragon 등 오픈소스 도구 등장</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">PASTA, VAST, LINDDUN 등 다양한 방법론 확산</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Agile/DevOps 환경 위협 모델링 경량화 (Continuous Threat Modeling)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">자동화 도구 성숙 (Threagile, IriusRisk 등)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">AI 보조 위협 모델링 (LLM 활용 위협 탐지)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 보물 상자를 만들기 전에 "나쁜 사람이 어디로 열려고 할까?"를 미리 생각해서, 그 부분을 더 튼튼하게 만드는 것이 위협 모델링이에요.
2. 자물쇠, 경첩, 뚜껑 틈새 등 약한 부분을 미리 찾아내면, 완성된 후에 고치는 것보다 훨씬 쉽고 저렴하게 안전하게 만들 수 있어요.
3. 위협 모델링은 "미리 나쁜 사람 입장에서 생각하는 연습"이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 539 / 973

← **이전**: [473. Microsoft SDL (Security Development Lifecycle) - 7단계 보안 생명주기](/knowledge-base/studynote/04_software_engineering/11_testing_validation/473_microsoft_sdl/)
**다음**: [476. DREAD 모델 - 위협 리스크 산정 지표](/knowledge-base/studynote/04_software_engineering/11_testing_validation/476_dread_model/) →

---
