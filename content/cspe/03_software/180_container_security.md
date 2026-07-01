---
title: "컨테이너 보안 - Seccomp·AppArmor·OPA (Container Security)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 180
---

# 📖 【암기용】 개념 완전 이해

> 목적: 컨테이너 보안을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 이미지, 런타임, 커널 호출, 권한, 정책, 감사 로그를 통제해 컨테이너 침해 경로를 줄이는 보안 체계
- **왜 필요한가**: 컨테이너는 호스트 커널을 공유하므로 취약 이미지, privileged 실행, 과도한 capability가 클러스터 전체 위험으로 이어질 수 있다.
- **핵심 직관**: 컨테이너 보안은 문 앞 검문(image scan), 실내 행동 제한(seccomp/AppArmor), 입주 규칙 검사(OPA)를 함께 두는 방식이다.

## 깊이 이해
- **배경·문제의식**: 컨테이너는 배포 단위가 작고 변경이 잦아 취약 이미지가 빠르게 퍼질 수 있다. 또한 root 권한, hostPath, hostNetwork, privileged 옵션은 호스트 경계 침해로 이어질 수 있다.
- **작동 원리**: seccomp는 허용 syscall을 제한하고, AppArmor는 파일·네트워크·capability 접근 프로파일을 적용한다. OPA Gatekeeper나 Kyverno는 admission 단계에서 정책 위반 manifest를 차단한다.
- **비유**: 건물 입주 전 신원 확인이 image scan이고, 방 안에서 열 수 있는 문을 제한하는 것이 AppArmor, 사용할 수 있는 도구를 제한하는 것이 seccomp이다.
- **구체 예시**: `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `seccompProfile: RuntimeDefault`를 적용하고 OPA로 privileged Pod 생성 0건을 강제한다.
- **흔한 오해·주의점**: 이미지 스캔만으로 충분하지 않다. 취약점이 없는 이미지도 runtime 권한이 과다하면 hostPath mount나 capability로 위험 경로가 생긴다.

## 연결 개념
- Pod Security Standards - privileged, baseline, restricted 정책 기준
- Admission Control - 배포 전 정책 검사 지점
- Supply Chain Security - SBOM, 서명, provenance 검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 컨테이너 보안 답안은 이미지 스캔, 런타임 격리, admission 정책, 감사 로그를 방어 계층으로 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 컨테이너 보안은 이미지 공급망부터 커널 syscall, Linux profile, Kubernetes admission까지 통제하는 다계층 체계임.
> 2. **가치**: seccomp, AppArmor, OPA로 실행 권한과 배포 정책을 제한해 호스트 침해와 정책 위반 배포를 차단함.
> 3. **판단 포인트**: image CVE 0건, privileged 0건, RuntimeDefault seccomp, audit log 보관을 기준으로 검증해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 컨테이너 위협 이해 확인 | image, registry, runtime, kernel, admission | 방화벽만 언급 |
| 통제 기술 매핑 확인 | seccomp, AppArmor, OPA, RBAC | 도구 이름만 나열 |
| 운영 검증 역량 확인 | scan, policy violation, audit log | 보안 기준 수치 누락 |

> 요약: 이 문제는 위협면별 통제 기술과 검증 지표를 연결해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 컨테이너 보안은 이미지부터 런타임까지의 통제 체계임.
- 배경: 컨테이너는 호스트 커널을 공유하고 이미지 배포가 잦아 취약점과 권한 과다가 확산될 수 있다.
- 필요성: 이미지 서명, 취약점 스캔, Pod Security, 런타임 감사 계층을 함께 설계한다.

---

## Ⅱ. 구조 및 구성요소

```text
Source/Image -> Registry Scan -> Admission OPA -> Runtime Policy -> Audit/Detection
  / seccomp: syscall 제한
  / AppArmor: profile 기반 접근 제한
  / OPA: manifest 정책 검사
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Image Scan | CVE, secret, SBOM 점검 | Trivy, Grype |
| seccomp | syscall allowlist 적용 | RuntimeDefault |
| AppArmor | 파일, 네트워크, capability 접근 제한 | profile 지정 |
| OPA/Gatekeeper | admission 정책 검사 | Rego constraint |

> 요약: 컨테이너 보안은 공급망, admission, runtime, 감사 계층으로 나누어 통제함.

---

## Ⅲ. 동작원리 및 흐름도

```text
이미지 빌드 -> CVE/SBOM 검사 -> 서명 검증 -> OPA 정책 검사 -> 런타임 profile 적용 -> 로그 감사
  / 정책 위반 -> admission reject
  / 런타임 위반 -> kernel deny/event
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 이미지 취약점과 secret 검사 | critical CVE 0건 |
| 2 | 서명, digest, SBOM 확인 | unsigned image 0건 |
| 3 | OPA가 manifest 정책 검사 | privileged, hostPath 차단 |
| 4 | seccomp/AppArmor profile 적용 | RuntimeDefault, profile loaded |
| 5 | audit, runtime detection 수집 | Falco alert, audit log |

> 요약: 컨테이너 보안은 배포 전 차단과 실행 중 제한을 함께 적용해야 함.

---

## Ⅳ. 특징

| 구분 | 단일 이미지 스캔 | 다계층 컨테이너 보안 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 공급망 | CVE 확인 | SBOM, 서명, digest pinning | critical 0건 |
| 권한 | 기본 설정 의존 | non-root, capability drop | privileged 0건 |
| 커널 | syscall 전체 허용 | seccomp RuntimeDefault | syscall deny event |
| 정책 | 수동 리뷰 | OPA admission reject | 위반 배포 0건 |

> 요약: 컨테이너 보안은 이미지 검사만이 아니라 권한, syscall, admission 정책을 함께 통제해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 배포 후 점검 | admission 전 차단 | CI/CD 자동 배포 |
| 비용/처리 | 수동 보안 리뷰 | policy as code | 배포 일 10회 이상 |
| 운영/위험 | root/privileged 허용 | restricted profile | 다중 테넌트 cluster |

> 요약: 배포 빈도와 테넌트 수가 늘면 OPA 기반 사전 차단과 런타임 profile 적용이 필요함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 취약 이미지 배포 | scan 누락 | CI scan, registry policy | critical CVE 0건 |
| 호스트 침해 | privileged, hostPath, capability | Pod Security restricted, OPA deny | privileged 0건 |
| 정책 우회 | 예외 남발 | exception TTL, audit review | 예외 만료율 100% |

> 요약: 컨테이너 보안 리스크는 취약 이미지, 권한 과다, 정책 예외로 관리함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 이미지 | critical/high CVE 0건 | Trivy, registry scan |
| 런타임 | RuntimeDefault seccomp 100% | kube audit, node scan |
| 정책 | OPA violation 배포 차단 100% | Gatekeeper audit |

> 요약: 보안 통제는 이미지 잔여 취약점, seccomp 적용률, admission 차단률로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 공급망 통제: CI에서 SBOM 생성, Trivy critical/high 0건, cosign 서명, digest pinning을 배포 조건으로 설정
2. 런타임 제한: `runAsNonRoot`, `allowPrivilegeEscalation: false`, `capabilities.drop: ALL`, `seccompProfile: RuntimeDefault` 적용
3. 정책 자동화: OPA Gatekeeper로 privileged, hostPath, latest tag, unsigned image를 admission 단계에서 reject

**결론 (2줄):**
- 기술사 판단: 컨테이너 보안은 이미지 스캔보다 admission 정책과 런타임 권한 제한을 함께 적용할 때 유효함
- 향후 방향: SBOM, 서명 검증, eBPF runtime detection, Policy as Code가 Kubernetes 보안 운영 기준으로 정착함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "컨테이너 보안을 설명하시오" | 이미지, admission, runtime, audit 흐름 | seccomp, AppArmor, OPA 역할 |
| 요구사항 명시형 | "보안 방안을 제시하시오", "설계하시오" | 정책 차단과 런타임 제한 흐름 | CVE, privileged, RuntimeDefault 지표 |

> 요약: 설명형은 방어 계층, 보안형은 정책 위반 차단과 검증 지표 중심으로 전환함.
