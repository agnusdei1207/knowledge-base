---
title: "Falco 런타임 보안 (Falco Runtime Security)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 125
---
# 📖 【암기용】 개념 완전 이해

> 목적: Falco 런타임 보안을 처음 보는 사람도 실행 중 컨테이너 위협 탐지가 어떻게 동작하는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.
## 한눈에
- **개요**: Falco는 Linux syscall, eBPF, 컨테이너·Kubernetes 메타데이터를 분석해 실행 중 비정상 행위를 탐지하는 런타임 보안 도구임
- **왜 필요한가**: 이미지 스캔과 Admission 정책은 배포 전 통제이다. 배포 후 웹셸 실행, 민감 파일 읽기, 패키지 설치, 컨테이너 탈출 시도는 런타임에서 탐지해야 한다.
- **핵심 직관**: 건물 출입 심사를 통과한 사람이 안에서 금고를 열거나 비상문을 조작하면 CCTV와 경보가 감지하는 방식임

## 깊이 이해
- **배경·문제의식**: Kubernetes 워크로드는 짧게 생성·삭제되고 컨테이너 내부 접근이 제한적이다. 침해가 발생해도 프로세스 실행, 파일 접근, 네트워크 연결을 실시간으로 보지 않으면 사고 시점을 놓친다.
- **작동 원리**: Falco는 kernel module 또는 eBPF probe로 syscall 이벤트를 수집하고 컨테이너 런타임과 Kubernetes 메타데이터를 붙인다. 규칙(rule)은 조건과 출력 메시지, 우선순위를 정의하며, 매칭 시 stdout, webhook, gRPC, SIEM으로 경보를 보낸다.
- **비유**: 공장 설비에 센서를 붙여 허가되지 않은 야간 작업, 위험 구역 접근, 금지 도구 사용을 즉시 알리는 방식임
- **구체 예시**: 운영 Pod 내부에서 `/bin/sh` 실행, `/etc/shadow` 읽기, `apk add curl` 실행이 감지되면 Falco가 namespace, pod, container, user, command를 포함한 경보를 발생시킴
- **흔한 오해·주의점**: Falco는 취약점 스캐너가 아니다. CVE를 직접 고치는 도구가 아니라 실행 중 행위를 탐지하고 대응 프로세스를 시작하는 탐지 계층임

## 연결 개념
- eBPF — 커널 이벤트 수집을 위한 저오버헤드 관측 기술
- CWPP — 워크로드 실행 보안과 런타임 위협 탐지 영역
- SIEM/SOAR — Falco 경보를 상관분석·자동 대응으로 확장

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Falco는 "컨테이너 이상행위 탐지"라고만 쓰지 말고 syscall 기반 이벤트, 규칙 엔진, Kubernetes 메타데이터, SIEM 대응 지표를 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Falco는 Linux syscall과 Kubernetes 메타데이터를 규칙 기반으로 분석해 컨테이너·호스트 런타임 위협을 탐지하는 클라우드 네이티브 보안 도구이다.
> 2. **가치**: 이미지 스캔·Admission 정책을 통과한 워크로드에서 셸 실행, 민감 파일 접근, 권한 상승, 비정상 네트워크 연결을 실행 시점에 탐지한다.
> 3. **판단 포인트**: eBPF/kernel module 수집, rule tuning, alert routing, false positive 관리, MTTD/MTTR 지표를 제시해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 런타임 보안 위치 이해 확인 | Build/Deploy 통제와 Run 탐지 구분 | Trivy, Gatekeeper와 동일 기능으로 설명 |
| 탐지 아키텍처 설계 확인 | syscall, eBPF, rules, Kubernetes metadata, output | "이상행위 탐지"만 쓰고 이벤트 원천 누락 |
| 운영 대응 역량 확인 | rule tuning, severity, SIEM/SOAR, triage SLA | 경보 발생 후 조치 절차 누락 |

> 요약: Falco 답안은 런타임 이벤트 원천, 규칙 평가, 경보 라우팅, 대응 지표를 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 클라우드 네이티브 런타임 탐지
- 배경: 배포 전 스캔과 정책 차단만으로는 운영 중 웹셸, 권한 상승, 민감 파일 접근을 식별하기 어려움.
- 필요성: Falco 규칙을 MITRE ATT&CK for Containers 전술에 매핑하고 syscall 이벤트를 SIEM·SOAR 대응으로 연결해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Host/Container Syscalls -> eBPF or Kernel Module -> Falco Engine
  / Rules, Macros, Lists, Exceptions
  / Kubernetes Metadata, Container Runtime Metadata
Falco Engine -> Alerts -> Falcosidekick/SIEM/SOAR -> Incident Response
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Event Source | syscall, k8s audit, cloud event 수집 | eBPF probe 또는 kernel module |
| Falco Engine | 이벤트를 rule 조건과 매칭 | rule, macro, list, exception 사용 |
| Metadata Enricher | namespace, pod, container, image, user 정보 결합 | Kubernetes API, container runtime |
| Output Channel | 경보를 stdout, webhook, gRPC, SIEM으로 전송 | Falcosidekick 연동 |
| Response Process | triage, 격리, 포렌식, 룰 튜닝 | SOAR playbook, ticket SLA |

> 요약: Falco는 커널 이벤트와 Kubernetes 메타데이터를 결합해 규칙 기반 경보를 생성하고 대응 체계로 전달한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
워크로드 실행 -> syscall 이벤트 수집 -> 메타데이터 보강
-> Falco rule 조건 평가 -> priority 산정
-> alert 출력 -> SIEM/SOAR triage -> 격리/조사/룰 튜닝
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | eBPF 또는 kernel module로 syscall 수집 | event drop rate 1% 이하 |
| 2 | Pod, namespace, image, user 메타데이터 부착 | 미매핑 이벤트 5% 이하 |
| 3 | rule, macro, list 조건으로 행위 평가 | 기본 룰+업무 룰 30개 이상 |
| 4 | priority 기반 경보 라우팅 | Critical 5분 내 triage |
| 5 | SOAR 조치와 rule tuning 반영 | 오탐률 10% 이하 |

> 요약: Falco는 syscall 수집부터 경보 triage까지 실행 행위를 규칙과 운영 지표로 통제한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | Falco 런타임 보안 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 탐지 시점 | 이미지 스캔·Admission 전 단계 | 운영 중 프로세스·파일·네트워크 행위 | Critical triage 5분 |
| 이벤트 원천 | 로그 중심 사후 분석 | syscall, k8s audit, cloud event | event drop 1% 이하 |
| 맥락 정보 | 호스트 프로세스 정보 | namespace, pod, image, user 결합 | 미매핑 5% 이하 |
| 한계 | 차단보다 탐지 중심 | 오탐 튜닝과 대응 자동화 필요 | 오탐률 10% 이하 |

> 요약: Falco는 실행 중 행위를 Kubernetes 맥락으로 탐지하지만 경보 품질과 대응 절차가 함께 설계되어야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Falco 런타임 보안 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Trivy·Gatekeeper 중심 사전 통제 | 실행 중 syscall 기반 탐지 | 운영 Pod 100개 이상, 침해 탐지 필요 |
| 비용/성능 | 로그 사후 분석 | 노드별 센서와 경보 파이프라인 | event drop 1% 이하, CPU overhead 5% 이하 |
| 운영/위험 | 사고 후 수동 조사 | 실시간 경보, SOAR 격리, 포렌식 | MTTD 5분, MTTR 30분 목표 |

> 요약: 배포 전 통제만으로 런타임 침해를 볼 수 없으므로 운영 클러스터에는 Falco 기반 탐지 계층이 필요하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 폭증 | 기본 룰과 업무 행위 충돌 | namespace별 exception, 튜닝 주기 | 오탐률 10% 이하 |
| 이벤트 손실 | 노드 부하, probe 설정 오류 | eBPF 설정 검증, buffer tuning | event drop 1% 이하 |
| 맥락 부족 | Kubernetes 메타데이터 연동 실패 | API 권한 점검, 캐시 모니터링 | 미매핑 이벤트 5% 이하 |
| 대응 지연 | 경보 라우팅 부재 | SIEM/SOAR, Slack, ticket 자동화 | Critical 5분 triage |

> 요약: Falco 운영 리스크는 오탐, 이벤트 손실, 맥락 부족, 대응 지연이며 튜닝·모니터링·자동화 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 탐지 품질 | 기본+업무 룰 30개 이상, 오탐률 10% 이하 | Falco rule metrics, triage 결과 |
| 수집 품질 | event drop rate 1% 이하, CPU overhead 5% 이하 | Falco metrics, node exporter |
| 대응 품질 | Critical MTTD 5분, MTTR 30분 | SIEM/SOAR incident timeline |
| 감사 증거 | 경보 원문, Pod 정보, command, user 보관 1년 | 로그 저장소, 티켓 첨부 |

> 요약: Falco 도입 효과는 탐지 품질, 수집 손실, 대응 시간, 감사 증거 보관으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 1단계: DaemonSet으로 Falco를 배포하고 eBPF 모드, event drop 1% 이하, Kubernetes 메타데이터 미매핑 5% 이하 기준 설정
2. 2단계: shell in container, sensitive file read, package manager run, outbound connection 등 업무 룰 30개 이상과 namespace별 exception 구성
3. 3단계: Falcosidekick으로 SIEM/SOAR 연동, Critical 5분 triage, MTTR 30분, 경보·command·pod 증거 1년 보관 운영

**결론 (2줄):**
- 기술사 판단: 개발 클러스터는 Admission 정책 중심으로 시작하고, 운영·규제 클러스터는 Trivy, Gatekeeper, Falco를 Build/Deploy/Run 3단계로 결합해야 함
- 향후 방향: eBPF 기반 관측, Kubernetes Audit, 클라우드 API 이벤트를 통합해 런타임 탐지와 자동 격리 플레이북을 함께 운영해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Falco 런타임 보안을 설명하시오", "컨테이너 런타임 탐지를 기술하시오" | syscall 수집, 룰 평가, 경보 라우팅 흐름 | 사전 통제와 런타임 탐지 차이 |
| 요구사항 명시형 | "Kubernetes 런타임 보안 방안을 제시하시오", "침해 탐지 체계를 설계하시오" | eBPF 수집, SIEM/SOAR 연동, triage SLA | MTTD 5분, event drop 1%, 오탐률 10% 기준 |

> 요약: 설명형은 런타임 탐지 원리를 쓰고, 설계형은 경보 품질·대응 시간·오탐 튜닝 지표를 중심으로 구성한다.
