---
title: "DevSecOps (DevSecOps)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 285
---

# 📖 【암기용】 개념 완전 이해

> 목적: DevSecOps를 보안팀 검토를 마지막에 붙이는 방식이 아니라 개발·배포·운영 전 과정에 보안 검증과 책임을 내장하는 방식으로 이해하게 만든다.

## 한눈에
- **개요**: 개발, 보안, 운영이 협업해 SDLC 전반에 자동 보안 검증과 보안 guardrail을 내장하는 문화·프로세스·도구 체계
- **왜 필요한가**: 배포 직전 보안 점검은 취약점 수정 비용이 크고, 클라우드 네이티브 배포 속도를 따라가기 어렵다.
- **핵심 직관**: 완성품 출고 직전에만 불량 검사를 하는 것이 아니라 설계, 부품, 조립, 출고 단계마다 검사 장치를 두는 방식이다.

## 깊이 이해
- **배경·문제의식**: 배포 빈도 증가와 오픈소스 의존성 확대는 취약점, secret 노출, misconfiguration 위험을 개발 초기부터 관리해야 하는 상황을 만들었다.
- **작동 원리**: threat modeling, secure coding, SAST, SCA, IaC scan, container scan, DAST, runtime detection을 pipeline과 운영에 연결한다.
- **비유**: 건물 안전을 준공 검사 한 번에 맡기지 않고 설계 검토, 자재 인증, 시공 점검, 사용 중 소방 점검을 모두 수행하는 것과 같다.
- **구체 예시**: PR 생성 시 SAST와 dependency CVE scan을 실행하고, container image는 critical CVE가 있으면 registry promotion을 차단한다.
- **흔한 오해·주의점**: DevSecOps는 보안 도구를 많이 붙이는 일이 아니다. 위험 기준, 예외 승인, false positive 처리, 개발자 workflow 통합이 있어야 한다.

## 연결 개념
- SSDF — NIST의 안전한 소프트웨어 개발 실천 프레임워크
- SBOM — 공급망 의존성 식별 근거
- GitOps — 보안 정책을 선언형 배포 흐름에 결합

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: DevSecOps는 shift-left 도구 도입이 아니라 보안 요구사항을 SDLC와 운영 guardrail에 통합하는 체계다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DevSecOps는 개발·보안·운영 책임을 통합해 코드부터 runtime까지 보안 검증을 자동화하는 SDLC 운영 방식임.
> 2. **가치**: 취약점 발견 시점을 앞당기고 배포 gate, 정책 검증, runtime 탐지를 통해 보안 리스크를 변경 흐름 안에서 통제함.
> 3. **판단 포인트**: SAST, SCA, secret scan, IaC scan, container scan, DAST, policy as code, 예외 관리가 함께 필요함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 보안 내재화 이해 확인 | shift-left, shift-right, pipeline gate | 보안팀 승인 절차만 설명 |
| 공급망 보안 판단 확인 | SCA, SBOM, image scan, signing | 코드 취약점 검사에만 한정 |
| 운영 통제 확인 | policy as code, runtime detection, audit | 도구명 나열로 끝냄 |

> 요약: 이 문제는 보안 검증을 개발 흐름에 넣고 운영 정책으로 지속 통제하는 설계를 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 보안 내재화 SDLC
- 배경: 클라우드 네이티브와 오픈소스 의존성 확대로 배포 후 보안 점검만으로 취약점과 설정 오류를 통제하기 어려움.
- 필요성: 코드, 의존성, 인프라, 컨테이너, runtime 단계에 자동 검증과 정책 gate를 배치해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Plan -> Threat Modeling / Security Requirement
Code -> SAST / Secret Scan / SCA
Build -> SBOM / Image Scan / Signing
Deploy -> IaC Policy / Admission Control
Run -> Runtime Detection / Audit / Incident Response
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Secure SDLC | 요구사항과 설계 단계 보안 반영 | threat modeling |
| Pipeline Security | 코드·의존성·이미지 자동 검증 | SAST, SCA, SBOM |
| Policy as Code | 배포 전 정책 검증 | OPA, admission control |
| Runtime Security | 운영 중 탐지와 대응 | EDR, CWPP, audit log |

> 요약: DevSecOps는 설계, 코드, 빌드, 배포, 운영 단계별 보안 통제를 pipeline과 runtime에 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요구사항 정의 -> 위협 모델링 -> 코드 작성 / PR
-> SAST / SCA / Secret Scan -> Build / SBOM / Image Scan
-> Policy Gate -> Deploy -> Runtime Detection -> Feedback
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 보안 요구사항과 위협 시나리오 정의 | threat coverage |
| 2 | PR에서 코드·secret·의존성 검증 수행 | critical finding count |
| 3 | build에서 SBOM, image scan, signing 수행 | unsigned image count |
| 4 | 배포와 운영에서 정책 위반·행위 이상 탐지 | policy violation, MTTD |

> 요약: DevSecOps는 보안 결함을 PR, build, deploy, runtime 단계에서 반복 검증하고 결과를 개발 backlog로 되돌린다.

---

## Ⅳ. 특징

| 구분 | 전통 AppSec | DevSecOps | 판단 기준 |
|:---|:---|:---|:---|
| 검증 시점 | 릴리스 전 점검 | PR부터 runtime까지 | 배포 빈도 |
| 책임 | 보안팀 중심 | 개발·보안·운영 공동 | ownership |
| 통제 방식 | 수동 진단 | pipeline gate와 policy | 자동화 범위 |
| 한계 | 늦은 발견 | false positive와 개발 마찰 | 예외 관리 |

> 요약: DevSecOps는 보안 책임을 배포 흐름에 내장하지만 탐지 품질과 예외 처리 체계가 없으면 개발 지연을 만든다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Shift-Left | Shift-Right | DevSecOps 적용 |
|:---|:---|:---|:---|
| 초점 | 개발 초기 결함 발견 | 운영 중 탐지·대응 | 양쪽을 pipeline으로 연결 |
| 도구 | SAST, SCA, secret scan | runtime detection, audit | 위험 기준별 gate |
| 판단 | PR 차단 | 운영 차단·격리 | CVSS, exploitability, asset criticality |

> 요약: DevSecOps는 shift-left와 shift-right를 분리하지 않고 위험 기준과 feedback loop로 연결한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 개발 마찰 | false positive 과다 | severity 기준과 suppress 절차 | false positive ratio |
| 공급망 취약점 | 오픈소스·이미지 관리 미흡 | SCA, SBOM, signing | critical CVE aging |
| 정책 우회 | emergency 배포 | break-glass 승인과 감사 | bypass count |

> 요약: DevSecOps 리스크는 탐지 품질, 공급망, 예외 우회에서 발생하며 기준과 감사 이력이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 취약점 처리 | critical CVE SLA 이내 조치 | vulnerability report |
| 공급망 | SBOM 생성률 100% 목표 | build artifact audit |
| 운영 통제 | policy violation 감소 | admission log |

> 요약: DevSecOps 성과는 취약점 조치 시간, SBOM 생성률, 정책 위반 감소로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. SDLC 초기에 threat modeling과 security requirement를 정의하고 PR 단계에 SAST, SCA, secret scan을 자동 실행함.
2. build 단계에서 SBOM 생성, image scan, artifact signing을 수행하고 critical 취약점 기준을 release gate로 둠.
3. Kubernetes admission control, runtime detection, audit log를 적용하고 예외 승인은 기간·사유·승인자를 기록함.

**결론 (2줄):**
- 기술사 판단: DevSecOps는 보안 도구 수보다 위험 기준, pipeline gate, 예외 관리, runtime feedback의 연결 수준으로 평가해야 함.
- 향후 방향: DevSecOps는 SSDF, SLSA, SBOM, AI 코드 검증과 결합되어 소프트웨어 공급망 보안 중심으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DevSecOps를 설명하시오" | SDLC 단계별 보안 검증 흐름 | 전통 AppSec 대비 차이 |
| 요구사항 명시형 | "보안 내재화 방안을 제시하시오" | pipeline gate와 runtime feedback 절차 | false positive, 공급망, 예외 리스크 |

> 요약: 설명형은 SDLC 통합, 방안형은 gate 기준과 공급망 통제를 중심으로 작성한다.
