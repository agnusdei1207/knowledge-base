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
- **개요**: 컨테이너 보안은 이미지 공급망부터 커널 syscall, Linux 접근 제어, Kubernetes 배포 정책까지를 계층적으로 통제하는 **다층 방어(Defense in Depth)** 체계다.
- **왜 필요한가**: 컨테이너는 격리 단위가 프로세스 수준(namespace/cgroup)이라 VM보다 얕다 — 호스트 커널을 여러 컨테이너가 공유하므로, 취약한 이미지나 과도한 권한(privileged, hostPath) 하나가 커널 취약점과 결합하면 호스트 전체·클러스터 전체로 침해가 번질 수 있다.
- **핵심 직관**: 문 앞 신원 검사(이미지 스캔), 방 안에서 열 수 있는 문 제한(seccomp/AppArmor), 입주 전 규정 위반 여부 심사(OPA admission)를 겹겹이 두는 구조다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 다층 방어(Defense in Depth) | 하나의 통제가 뚫려도 다음 계층이 막도록 여러 방어선을 겹치는 원칙 — 이 개념 전체의 상위 원리 | 성벽 + 해자 + 내성 |
| syscall(시스템 콜) | 프로세스가 커널 기능(파일 열기, 네트워크 소켓 생성 등)을 요청하는 인터페이스 | 창구에 제출하는 요청서 |
| seccomp(Secure Computing Mode) | 컨테이너 프로세스가 호출 가능한 syscall 목록을 커널 레벨에서 제한하는 리눅스 기능 | 창구에서 처리 가능한 요청서 종류 제한 |
| AppArmor | 프로세스별로 접근 가능한 파일·네트워크·capability를 프로파일로 제한하는 리눅스 강제 접근 제어(LSM) | 방마다 붙은 출입 규정표 |
| Linux capability | root 권한을 `CAP_NET_ADMIN`, `CAP_SYS_ADMIN` 등 세분화한 단위 권한 | 마스터키를 기능별 열쇠로 쪼갠 것 |
| Admission Control | Pod가 스케줄링되기 전 API 서버 단계에서 정책 위반 여부를 검사·차단하는 지점 | 입주 심사 창구 |
| OPA(Open Policy Agent)/Gatekeeper | Rego 언어로 정책을 정의해 admission 단계에서 manifest를 검사·거부하는 정책 엔진 | 규정 위반 서류를 자동 반려하는 심사관 |
| Pod Security Standards | privileged·baseline·restricted 3단계로 Pod의 허용 권한 수준을 정의한 Kubernetes 표준 | 보안등급 3단계(자유/기본/제한) |

## 깊이 이해

### 왜 다층으로 방어해야 하나 (배경)
- 컨테이너는 배포 단위가 작고 변경이 잦다 — 하루에도 수십 번 이미지가 바뀌는 환경에서는 취약한 base 이미지 하나가 수백 개 서비스에 순식간에 퍼질 수 있다. 동시에 VM과 달리 커널을 공유하므로, privileged 컨테이너 하나가 뚫리면 namespace 격리를 우회해 호스트 프로세스나 다른 컨테이너까지 접근할 수 있는 구조적 위험이 있다.
- 그래서 "이미지가 안전한가(공급망)", "실행 중 권한이 최소인가(런타임)", "배포 자체가 정책을 지키는가(admission)"를 각각 별도 계층으로 통제한다 — 어느 하나만 믿지 않는다.

### seccomp가 syscall을 막는 원리 (구체 수치)
- 리눅스 커널은 대략 300~400개의 syscall을 제공하지만, 일반 웹 애플리케이션 컨테이너가 실제로 쓰는 syscall은 그중 일부(대략 40~70개 수준)뿐이다. `seccompProfile: RuntimeDefault`는 컨테이너 런타임이 제공하는 기본 allowlist를 적용해 `mount()`, `reboot()`, `ptrace()`처럼 컨테이너가 쓸 이유가 없는 위험 syscall을 원천 차단한다.
- 예: 컨테이너 탈출 공격 상당수는 `mount()`나 커널 모듈 조작 syscall을 필요로 하는데, seccomp가 이를 막으면 애플리케이션 취약점이 있어도 탈출까지 이어지는 경로 자체가 커널 단에서 끊긴다.

### AppArmor와 seccomp의 역할 분담
- seccomp는 "어떤 syscall을 호출할 수 있는가"(행위의 종류)를 제한하고, AppArmor는 "그 행위를 어떤 대상(파일 경로·네트워크)에 할 수 있는가"(행위의 대상)를 제한한다 — 서로 보완 관계다.
- 예: seccomp가 `open()` syscall 자체는 허용하되, AppArmor 프로파일이 `/etc/shadow` 경로에 대한 read를 거부하면, 컨테이너 프로세스는 파일을 여는 행위는 할 수 있어도 민감 경로는 열지 못한다.

### admission 단계 차단을 워크플로 수치로 이해
- 이미지 빌드 -> CI에서 Trivy 같은 스캐너로 CVE 검사(critical/high 0건 기준) -> cosign 서명 -> `kubectl apply` 순간 OPA Gatekeeper가 manifest를 검사 -> `privileged: true`나 `hostPath` 마운트가 있으면 API 서버 단계에서 즉시 reject.
- 이 단계가 없으면 "위험한 설정이 이미 Pod로 떠서 실행된 뒤"에야 알아채는데, admission control은 그 이전, 즉 스케줄링 자체를 막아 위험이 클러스터에 들어오지 못하게 한다 — 사후 탐지가 아니라 사전 차단이라는 점이 핵심이다.

### capability drop을 구체 예시로 이해
- 리눅스 root는 원래 하나의 거대한 권한이지만, capability로 40여 개(커널 버전에 따라 다름)의 세부 권한으로 쪼갤 수 있다. 컨테이너 런타임 기본값은 약 14개 정도의 capability를 컨테이너에 부여한다.
- `capabilities.drop: ALL`로 전부 제거한 뒤 필요한 것만 `add`하는 방식(예: 웹 서버가 1024 미만 포트를 bind해야 하면 `CAP_NET_BIND_SERVICE`만 추가)을 쓰면, 설령 컨테이너가 뚫려도 공격자가 쓸 수 있는 권한이 애초에 최소화되어 있다.

### 비유와 흔한 오해
- **비유**: 이미지 스캔은 건물 입주 전 신원조회, AppArmor는 방마다 붙은 "이 문은 열 수 없음" 팻말, seccomp는 "이 도구는 사용 금지" 목록, OPA admission은 입주 규정 위반 여부를 최종 확인하는 관리사무소 심사다.
- **오해 1**: "이미지에 CVE가 없으면 안전하다" — 틀렸다. CVE 0건인 이미지도 `privileged: true`로 실행하면 호스트 디바이스·커널 모듈에 직접 접근할 수 있어 런타임 권한이 더 큰 위험 요인이 된다.
- **오해 2**: "seccomp/AppArmor를 켜면 성능이 크게 떨어진다" — RuntimeDefault 수준은 syscall당 수 마이크로초 단위 오버헤드로 실무 영향이 미미하다. 오히려 꺼두면 침해 시 피해 반경이 훨씬 커진다.

## 연결 개념
- Rootless Container (181) - 컨테이너가 애초에 호스트 root 권한 없이 실행되도록 만드는 별도 축의 통제
- Pod Security Standards - privileged/baseline/restricted 등급으로 이 통제들을 묶은 Kubernetes 표준
- Supply Chain Security - SBOM·서명·provenance로 "이미지 자체의 신뢰"를 검증하는 앞단 계층

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
