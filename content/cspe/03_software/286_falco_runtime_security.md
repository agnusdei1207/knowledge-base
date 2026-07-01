---
title: "Falco 런타임 보안 (Falco Runtime Security)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 286
---

# 📖 【암기용】 개념 완전 이해

> 목적: Falco 런타임 보안을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 컨테이너와 호스트의 시스템 콜을 감시해 이상 행위를 탐지하는 런타임 보안 도구
- **왜 필요한가**: 이미지 스캔은 배포 전 취약점을 찾지만, 실행 중 쉘 실행, 권한 상승, 민감 파일 접근 같은 침해 행위는 런타임에서 탐지해야 한다.
- **핵심 직관**: Falco는 서버의 CCTV와 같다. 프로세스가 어떤 파일을 열고 어떤 네트워크 연결을 만드는지 실시간으로 관찰한다.

## 깊이 이해
- **배경·문제의식**: Kubernetes 환경에서는 pod가 짧게 생성·삭제되고, 공격자는 컨테이너 내부에서 쉘을 열거나 hostPath를 악용할 수 있다. 사전 스캔만으로 실행 중 행위를 알 수 없다.
- **작동 원리**: Falco는 kernel module, eBPF, audit log 등을 통해 system call 이벤트를 수집하고 rule 조건과 대조한다. 위반 시 stdout, webhook, SIEM, Slack 등으로 alert를 보낸다.
- **비유**: 건물 도면 검사는 이미지 스캔이고, 출입문과 금고 앞 감시는 Falco 런타임 탐지다.
- **구체 예시**: 운영 pod에서 `/bin/sh`가 실행되거나 `/etc/shadow` 접근이 발생하면 Falco rule이 `Terminal shell in container` 또는 `Read sensitive file` 이벤트로 탐지한다.
- **흔한 오해·주의점**: Falco는 차단 도구가 아니라 탐지 중심 도구다. 차단은 Kubernetes policy, network policy, response automation과 연계해야 한다.

## 연결 개념
- 컨테이너 이미지 스캔 - 배포 전 취약점 탐지
- eBPF - 커널 이벤트 수집 기술
- SIEM/SOAR - 탐지 이벤트 상관분석과 대응 자동화

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Falco를 단순 모니터링 도구로 쓰지 말고 system call 기반 탐지, rule, alert, 대응 연계를 답안 축으로 삼는다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Falco는 system call 이벤트를 규칙과 대조해 컨테이너·호스트 런타임 이상 행위를 탐지하는 도구이다.
> 2. **가치**: 배포 후 발생하는 쉘 실행, 권한 상승, 민감 파일 접근, 비정상 네트워크 행위를 실시간 경보로 전환한다.
> 3. **판단 포인트**: 사전 스캔은 취약점, Falco는 실행 행위, 대응 자동화는 격리·차단을 담당하도록 계층화한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 런타임 보안 이해 확인 | system call, rule, alert, response | 이미지 스캔과 런타임 탐지 혼동 |
| Kubernetes 운영 보안 판단 확인 | pod 행위, hostPath, privileged, shell 탐지 | 컨테이너 격리만 설명 |
| 탐지·대응 체계 설계 확인 | Falco -> SIEM/SOAR -> 격리 | Falco가 직접 모든 차단을 수행한다고 작성 |

> 요약: Falco 답안은 실행 중 행위 탐지와 후속 대응 연계를 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

Falco는 런타임 행위 탐지 도구이다. 컨테이너 보안은 이미지 빌드 시점 점검만으로 끝나지 않으며 실행 중 권한 상승과 민감 파일 접근을 탐지해야 한다. Falco는 system call 이벤트를 rule로 평가해 침해 징후를 경보화한다.

---

## Ⅱ. 구조 및 구성요소

```text
Kernel/System Call -> Falco Driver/eBPF -> Rule Engine -> Alert Output -> SIEM/SOAR
                              +-> Kubernetes Metadata
                              +-> Custom Rule
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Event Source | system call, audit, Kubernetes event 수집 | kernel module 또는 eBPF |
| Rule Engine | 조건식 기반 이상 행위 판정 | YAML rule, macro, list |
| Metadata | pod, namespace, image, user 정보 보강 | Kubernetes audit와 연계 |
| Alert Output | 탐지 결과 전송 | stdout, webhook, gRPC, SIEM |
| Response | 격리·삭제·티켓 생성 | SOAR, admission policy와 연계 |

> 요약: Falco는 커널 이벤트를 규칙으로 평가하고 Kubernetes 메타데이터를 붙여 대응 시스템으로 전달한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
프로세스 행위 -> system call 수집 -> rule 조건 평가 -> severity 부여 -> alert 전송 -> 대응 실행
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 컨테이너·호스트 system call 수집 | 이벤트 손실률 1% 이하 |
| 2 | pod, namespace, image 메타데이터 결합 | metadata 누락 0건 |
| 3 | rule 조건과 이벤트 비교 | rule syntax test 100% 통과 |
| 4 | priority와 alert message 생성 | critical alert 전달 100% |
| 5 | SIEM/SOAR에서 격리·조사 | MTTD 5분 이하 |

> 요약: Falco는 커널 이벤트와 Kubernetes 메타데이터를 결합해 규칙 기반 경보를 생성한다.

---

## Ⅳ. 특징

| 구분 | 사전 이미지 스캔 | Falco 런타임 보안 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 시점 | 빌드·배포 전 | 실행 중 | real-time alert |
| 탐지 대상 | CVE, secret, misconfig | 쉘 실행, 파일 접근, 권한 상승 | system call |
| 대응 방식 | 배포 차단 | 경보와 후속 격리 | SIEM/SOAR 연동 |
| 한계 | 실행 행위 미탐지 | 오탐 rule tuning 필요 | false positive rate 관리 |

> 요약: Falco는 실행 중 행위 탐지에 맞는 도구이며 배포 전 취약점 스캔과 상호 보완 관계이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 로그 기반 사후 분석 | system call 기반 실시간 탐지 | Kubernetes 운영 workload |
| 비용/성능 | 에이전트 없는 관측 | node 단위 Falco daemonset | CPU overhead 5% 이하 검증 |
| 운영/위험 | 침해 후 수동 조사 | alert, SIEM, SOAR 연결 | MTTD 5분 이하 목표 |

> 요약: Falco는 실시간 탐지 요구가 있고 node 단위 에이전트 운영이 가능한 Kubernetes 환경에 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 증가 | 기본 rule과 업무 행위 불일치 | namespace별 allowlist, rule tuning | false positive 10건/일 이하 |
| 이벤트 누락 | 드라이버 오류 또는 과부하 | eBPF driver 검증, sampling 점검 | event drop rate 1% 이하 |
| 대응 지연 | alert만 생성하고 조치 미연계 | SOAR playbook, pod quarantine | MTTR 30분 이하 |

> 요약: Falco 운영은 오탐, 이벤트 누락, 대응 지연을 별도 지표로 관리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 탐지 시간 | MTTD 5분 이하 | alert timestamp, incident ticket |
| 탐지 품질 | false positive 10건/일 이하 | SOC triage 결과 |
| 커버리지 | node daemonset 적용률 100% | Kubernetes node inventory |

> 요약: 런타임 보안 효과는 탐지 시간, 오탐률, node 커버리지로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Falco를 Kubernetes DaemonSet으로 배포하고 eBPF driver를 사용해 node별 system call 이벤트를 수집함
2. 운영 namespace별로 shell 실행, sensitive file read, privileged container rule을 조정하고 CI에서 rule syntax test를 수행함
3. Falco alert를 SIEM과 SOAR로 전송해 pod quarantine, network policy 차단, incident ticket 생성을 자동화함

**결론 (2줄):**
- 기술사 판단: 이미지 스캔은 배포 전, Falco는 실행 중 탐지, 정책 엔진은 차단 역할로 조합해야 함
- 향후 방향: Falco는 eBPF 기반 클라우드 네이티브 탐지와 Kubernetes audit 연계 중심으로 확대됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Falco 런타임 보안을 설명하시오" | system call 수집과 rule 평가 흐름 | 이미지 스캔과 런타임 탐지 차이 |
| 요구사항 명시형 | "컨테이너 침해 탐지 방안을 제시하시오" | alert, SIEM, SOAR 대응 흐름 | MTTD, 오탐률, node 커버리지 기준 |

> 요약: 설명형은 탐지 구조, 방안형은 운영 대응과 지표 중심으로 전개한다.
