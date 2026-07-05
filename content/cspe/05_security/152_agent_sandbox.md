---
title: "에이전트 샌드박스 격리 (Agent Sandbox)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 152
---

# 📖 【암기용】 개념 완전 이해

> 목적: 에이전트 샌드박스 격리를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: AI 에이전트가 코드·명령·파일·네트워크를 실행하는 공간을 본 시스템과 분리하는 기술
- **왜 필요한가**: 에이전트는 코드 해석기, 브라우저, 셸, 업무 API를 호출한다. 악성 입력이 `rm`, 데이터 반출, 내부망 스캔으로 연결되지 않도록 실행 경계를 만들어야 한다.
- **핵심 직관**: 위험한 실험은 실험실에서 하고, 실험실 밖 문은 잠그는 구조임.

## 깊이 이해
- **배경·문제의식**: LLM은 명령 의도를 완전하게 판별하지 못한다. 문서 안의 악성 지시, 패키지 설치 스크립트, 브라우저 자동화가 결합되면 권한 상승, 비밀키 유출, 내부망 접근이 발생한다.
- **작동 원리**: 샌드박스는 프로세스, 파일시스템, 네트워크, 시스템 호출, 자원 사용량을 제한한다. 컨테이너, microVM, seccomp, AppArmor/SELinux, eBPF, ephemeral workspace를 조합한다.
- **비유**: 어린이가 과학 실험을 할 때 책상 위 보호매트, 장갑, 제한된 시약, 감독자를 두는 것과 같다. 실패해도 집 전체가 피해를 받지 않는다.
- **구체 예시**: 코드 실행 에이전트는 2 vCPU, 메모리 4GB, 실행시간 120초, outbound 도메인 allowlist 20개, `/tmp/work` 쓰기만 허용하고 실행 후 디스크를 폐기한다.
- **흔한 오해·주의점**: 컨테이너 하나만으로 충분하다고 보면 안 된다. 호스트 커널 공유, Docker socket 노출, privileged mode, hostPath mount는 격리 경계를 무너뜨린다.

## 연결 개념
- Zero Trust Workload - 실행 단위마다 신원·정책·네트워크 분리
- seccomp/AppArmor/SELinux - 시스템 호출과 파일 접근 제한
- 에이전트 보안 - 샌드박스는 권한 통제 체계의 실행 격리 계층

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 에이전트 샌드박스는 코드 실행 편의를 위한 컨테이너가 아니라 파일·네트워크·시스템 호출·비밀정보 접근을 제한하는 보안 경계임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 에이전트 샌드박스는 AI 에이전트의 코드 실행과 도구 호출을 격리된 런타임에서 제한하는 보안 통제임.
> 2. **가치**: 프롬프트 인젝션, 악성 패키지, 셸 명령 오남용이 호스트 파일·내부망·비밀키로 확산되는 경로를 차단함.
> 3. **판단 포인트**: 격리 강도는 컨테이너, microVM, 네트워크 egress, secret zero access, 실행 후 폐기 여부로 결정함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 에이전트 실행 위험 식별 | 코드 실행, 파일 조작, 브라우저 자동화, 내부망 접근 | 프롬프트 필터만 제시하고 런타임 격리 누락 |
| 샌드박스 설계 판단 | container vs microVM, seccomp, read-only FS, egress control | privileged container, hostPath, Docker socket 허용 |
| 운영 통제 확인 | ephemeral workspace, quota, log, artifact scan | 실행 후 데이터 폐기·로그 보존 기준 누락 |

> 요약: 이 문제는 에이전트의 실행권한을 격리 경계와 운영 지표로 제한하는 설계 능력을 확인함.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | AI 에이전트가 코드·명령·파일·네트워크를 실행하는 공간을 본 시스템과 분리하는 기술 | "학습하는 기계" |
| **왜 필요한가** | 에이전트는 코드 해석기, 브라우저, 셸, 업무 API를 호출한다 | "식당 메뉴판" |
| **핵심 직관** | 위험한 실험은 실험실에서 하고, 실험실 밖 문은 잠그는 구조임 | "이 개념의 핵심" |
| **배경·문제의식** | LLM은 명령 의도를 완전하게 판별하지 못한다 | "이 개념의 핵심" |
| **작동 원리** | 샌드박스는 프로세스, 파일시스템, 네트워크, 시스템 호출, 자원 사용량을 제한한다 | "이 개념의 핵심" |
| **비유** | 어린이가 과학 실험을 할 때 책상 위 보호매트, 장갑, 제한된 시약, 감독자를 두는 것과 같다 | "이 개념의 핵심" |
| **흔한 오해·주의점** | 컨테이너 하나만으로 충분하다고 보면 안 된다 | "이 개념의 핵심" |

---


## Ⅰ. 개요 및 필요성

- 개요: AI 실행 환경 격리 기술
- 배경: 에이전트가 코드·셸·브라우저·패키지 설치를 수행하면 악성 지시가 호스트 침해와 데이터 반출로 확산될 수 있다.
- 필요성: 컨테이너 네임스페이스, seccomp, 파일시스템 제한, 네트워크 egress allowlist로 실행 권한과 피해 반경을 통제해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Agent Planner -> Sandbox Orchestrator -> Isolated Runtime -> Tool Execution
                       +-> Policy Profile
                       +-> Network Egress Proxy
                       +-> Log/Artifact Collector
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Sandbox Orchestrator | 작업별 격리 런타임 생성·폐기 | Kubernetes Job, Firecracker, gVisor |
| Policy Profile | CPU·메모리·시간·시스템 호출 제한 | seccomp, AppArmor, cgroup v2 |
| File Boundary | read-only base image와 임시 작업공간 제공 | hostPath 금지, secret mount 금지 |
| Network Boundary | outbound 도메인·포트 allowlist 집행 | egress proxy, DNS logging |
| Evidence Collector | 실행 명령, 파일 해시, 산출물 스캔 | SBOM, malware scan, audit log |

> 요약: 샌드박스는 격리 런타임, 정책 프로파일, 파일·네트워크 경계, 증적 수집 계층으로 구성됨.

---

## Ⅲ. 동작원리 및 흐름도

```text
작업 요청 -> 위험도 분류 -> 샌드박스 생성 -> 코드/도구 실행
-> 리소스·네트워크 감시 -> 산출물 검사 -> 런타임 폐기
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 작업 유형과 필요 권한 분류 | 코드 실행, 브라우저, 파일 변환, API 호출 |
| 2 | 격리 런타임과 정책 프로파일 선택 | microVM 필요 여부, egress 도메인 수 |
| 3 | read-only 이미지와 임시 볼륨으로 실행 | privileged=false, rootless, TTL 설정 |
| 4 | 시스템 호출·네트워크·자원 사용 감시 | seccomp violation, CPU·메모리 quota |
| 5 | 산출물 검사 후 런타임 폐기 | hash 기록, 악성코드 탐지, 디스크 삭제 |

> 요약: 샌드박스는 실행 전 위험 분류와 실행 중 감시, 실행 후 폐기로 격리 수명주기를 완성함.

---

## Ⅳ. 특징

| 구분 | 일반 컨테이너 실행 | 에이전트 샌드박스 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 격리 경계 | 애플리케이션 배포 단위 | 불신 코드 실행 경계 | gVisor, Firecracker, Kata Containers |
| 파일 접근 | 영구 볼륨 사용 가능 | read-only image, ephemeral volume | 실행 후 0개 영구 파일 |
| 네트워크 | 기본 outbound 허용 | 도메인·포트 allowlist | egress domain 20개 이하 |
| 비밀정보 | 환경변수 주입 가능 | secret zero access 원칙 | secret mount 0건 |

> 요약: 에이전트 샌드박스는 배포 편의보다 불신 실행의 피해 반경을 파일·네트워크·비밀정보 기준으로 제한함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 격리 방식 | 프로세스 격리 | container + seccomp | 낮은 위험, 내부 데이터 없음 |
| 격리 방식 | microVM | Firecracker/Kata/gVisor | 외부 코드 실행, 민감 데이터 접근 |
| 비용/성능 | 상시 런타임 | 작업별 ephemeral runtime | 실행 시간 120초 이하 작업에 적합 |
| 운영 | 수동 점검 | 정책 프로파일과 로그 자동 수집 | 위반 이벤트 SIEM 전송 100% |

> 요약: 민감 데이터와 외부 코드가 결합되면 컨테이너 단독보다 microVM 또는 user-space kernel 격리를 선택해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Sandbox Escape | 커널 취약점, privileged mode | microVM, rootless, seccomp default deny | escape PoC 차단률 |
| Secret Leakage | 환경변수·볼륨에 키 노출 | secret zero access, token broker | secret mount 0건 |
| Data Exfiltration | outbound 기본 허용 | egress proxy, DNS allowlist, DLP | 차단된 외부전송 건수 |
| Resource Abuse | 무한 루프·대용량 처리 | cgroup quota, timeout, job kill | CPU 2 vCPU, TTL 120초 준수 |

> 요약: 샌드박스 리스크는 탈출·비밀키·외부전송·자원남용이며, 격리와 quota로 제한함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 격리 설정 | privileged=false, hostPath=0, Docker socket=0 | admission policy, IaC scan |
| 네트워크 통제 | outbound allowlist 100%, unknown DNS 차단 | proxy log, DNS query 분석 |
| 실행 증적 | 명령·파일해시·산출물 로그 100% | audit collector, object storage |
| 폐기 검증 | 작업 종료 후 볼륨·프로세스 0건 | namespace scan, volume inventory |

> 요약: 샌드박스 효과는 설정 점검, 네트워크 차단, 증적 수집, 폐기 검증 수치로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 격리 프로파일 표준화: low-risk는 rootless container, high-risk는 Firecracker/gVisor, 모든 작업은 privileged=false 적용
2. 파일·네트워크 경계 설정: read-only image, `/workspace` 임시 볼륨, outbound allowlist, secret mount 0건 정책 적용
3. 실행 증적 운영: 명령 로그, 파일 hash, egress log, 산출물 malware scan을 trace id로 묶고 1년 이상 보관

**결론 (2줄):**
- 기술사 판단: 단순 질의 에이전트는 guardrail로 충분하나 코드·브라우저·파일 실행 에이전트는 sandbox를 기본 경계로 둠
- 향후 방향: 에이전트 샌드박스는 microVM, eBPF 감시, 정책 기반 egress proxy를 결합한 실행 격리 플랫폼으로 발전함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "에이전트 샌드박스를 설명하시오", "기술하시오" | 생성, 실행, 감시, 폐기 흐름 | 컨테이너와 microVM의 격리 차이 |
| 요구사항 명시형 | "격리 방안을 설계하시오", "운영 방안을 제시하시오" | 정책 프로파일, egress, quota, 폐기 절차 | privileged 금지, hostPath 금지, 로그 100% |

> 요약: 설명형은 격리 원리를, 설계형은 실행 정책과 운영 지표를 중심으로 목차를 전환함.
