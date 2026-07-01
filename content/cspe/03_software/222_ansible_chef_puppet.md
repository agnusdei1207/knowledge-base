---
title: "Ansible·Chef·Puppet (Ansible Chef Puppet)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 222
---

# 📖 【암기용】 개념 완전 이해

> 목적: Ansible·Chef·Puppet을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 서버 OS, 패키지, 설정 파일, 서비스 상태를 코드로 맞추는 구성관리 도구
- **왜 필요한가**: 서버 100대의 패치·계정·보안 설정을 수작업으로 맞추면 구성 편류와 감사 누락이 발생한다
- **핵심 직관**: Terraform이 인프라를 만들면 Ansible·Chef·Puppet은 서버 안의 상태를 표준 구성으로 맞춘다

## 깊이 이해
- **배경·문제의식**: VM과 물리 서버는 생성 후에도 OS 패치, 미들웨어 설정, 인증서 교체, 계정 통제가 필요하다. 서버별 수동 변경은 장애 원인 추적을 어렵게 만든다.
- **작동 원리**: Ansible은 agentless SSH push 방식으로 playbook을 실행한다. Chef와 Puppet은 agent가 주기적으로 중앙 서버와 통신해 recipe/manifest 기준으로 상태를 수렴시킨다.
- **비유**: Ansible은 관리자가 체크리스트를 들고 각 방을 방문하는 방식, Chef·Puppet은 각 방에 설치된 점검기가 본부 기준표를 주기적으로 받아 고치는 방식임
- **구체 예시**: CIS benchmark 기준으로 SSH root login 금지, NTP 설정, nginx 패키지 버전, logrotate 정책을 200대 서버에 배포한다.
- **흔한 오해·주의점**: 구성관리는 IaC와 겹치지만 동일하지 않다. VM 생성은 Terraform, OS 내부 설정과 지속 보정은 구성관리 도구가 담당한다.

## 연결 개념
- Infrastructure as Code - 인프라 목표 상태 관리
- Immutable Infrastructure - 서버를 고치지 않고 새 이미지로 교체
- Patch Management - OS·미들웨어 취약점 보정

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 도구 이름보다 push/pull, agent 유무, idempotency, drift 보정, 보안 기준 준수를 기준으로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Ansible·Chef·Puppet은 서버 구성 상태를 코드로 정의하고 반복 실행해 목표 상태로 수렴시키는 구성관리 도구이다.
> 2. **가치**: 패치, 계정, 설정, 서비스 기동 상태를 감사 가능한 코드와 실행 로그로 통제한다.
> 3. **판단 포인트**: 단순 배포와 임시 작업은 Ansible, 대규모 지속 수렴은 Chef·Puppet의 agent 모델을 검토한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 구성관리 원리 이해 확인 | idempotency, push/pull, agent, drift 보정 | 단순 원격 명령 실행으로 설명 |
| 도구 선택 기준 확인 | Ansible agentless, Chef recipe, Puppet manifest | 시장 도구명 나열로 끝냄 |
| 운영·보안 통제 확인 | CIS 설정, 패치율, 실행 로그, 승인 절차 | 보안 baseline과 감사 지표 누락 |

> 요약: 이 문제는 서버 설정 자동화가 아니라 목표 구성 수렴과 표준 준수 운영을 묻는다.

---

## Ⅰ. 개요 및 필요성

Ansible·Chef·Puppet은 서버 구성을 코드로 관리하는 도구이다. VM 생성 이후 OS 패치, 계정, 서비스, 설정 파일은 지속적으로 바뀐다. 구성관리 없이는 100대 서버의 drift와 취약 설정을 감사 시점에만 발견하게 된다.

---

## Ⅱ. 구조 및 구성요소

```text
Git Repo -> Playbook/Recipe/Manifest -> Inventory/Node
-> Execution Engine -> Target Server
-> Report/Log -> Compliance Dashboard
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Ansible Playbook | YAML 기반 작업 순서와 목표 상태 정의 | SSH, agentless, push |
| Chef Recipe | Ruby DSL 기반 구성 정책 | chef-client, pull |
| Puppet Manifest | 선언형 리소스와 카탈로그 정의 | puppet agent, pull |
| Inventory/Node DB | 대상 서버와 속성 관리 | group, role, environment |

> 요약: 구성관리 구조는 코드, 대상 목록, 실행 엔진, 리포트로 구성되며 agent 유무가 운영 방식을 가른다.

---

## Ⅲ. 동작원리 및 흐름도

```text
구성 요구 -> 코드 작성 -> 대상 서버 식별
-> Dry Run/Check -> 실행 -> 결과 수집
-> 실패 재시도 -> Drift/Compliance 보고
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | baseline과 역할별 구성을 코드화 | CIS 항목 매핑 100% |
| 2 | inventory와 변수 분리 | prod/dev 변수 충돌 0건 |
| 3 | dry-run 또는 noop 실행 | 변경 예상 항목 승인 |
| 4 | 실행 후 리포트 수집 | 실패 노드 0건, 패치율 95% 이상 |

> 요약: 구성관리는 실행 전 변경 예측과 실행 후 리포트를 통해 목표 상태 수렴 여부를 확인한다.

---

## Ⅳ. 특징

| 구분 | Ansible | Chef | Puppet |
|:---|:---|:---|:---|
| 실행 방식 | SSH push | agent pull | agent pull |
| 언어 | YAML | Ruby DSL | Puppet DSL |
| 적합 영역 | 빠른 작업, 소규모 자동화 | 복잡한 정책 코드화 | 대규모 표준 구성 수렴 |
| 판단 수치 | 서버 200대 이하 시작 용이 | recipe 테스트 80% 이상 | agent 보고 주기 30분 |

> 요약: Ansible은 진입 장벽, Chef·Puppet은 지속 수렴과 정책 관리에서 선택 기준이 갈린다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Ansible·Chef·Puppet | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 수동 SSH 작업 | 코드 기반 구성 수렴 | 서버 50대 이상 또는 감사 대상 시스템 |
| 비용/성능 | 작업자별 편차 | 반복 실행과 리포트 | 월 패치 작업 8시간 이하 목표 |
| 운영/위험 | drift 누적 | agent 장애·권한 과다 | 실패 노드 0건 관리 |

> 요약: 서버 수와 감사 요구가 늘면 구성관리 도구로 drift와 패치 누락을 측정 가능하게 만들어야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 장애 전파 | 잘못된 playbook 일괄 실행 | canary 5%, batch limit, rollback | 실패율 1% 이하 |
| 권한 오남용 | root 권한 자동화 | sudoers 최소권한, vault secret | privileged task 승인 100% |
| 구성 편류 | 수동 긴급 변경 | scheduled compliance scan | drift 미해결 0건 |

> 요약: 구성관리 리스크는 일괄 변경, 권한, drift이며 단계 배포와 준수 점검으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 패치 준수 | 중요 CVE 패치 7일 이내 95% | patch report |
| 실행 신뢰도 | job success 99% 이상 | AWX, Chef Automate, Puppet report |
| 보안 기준 | CIS fail 항목 0건 | compliance scan |

> 요약: 도입 효과는 패치 기한, 실행 성공률, CIS 준수율로 평가한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. OS baseline을 CIS benchmark 항목으로 분해하고 SSH, NTP, auditd, logrotate, 계정 정책을 role별 코드로 관리
2. prod 배포는 canary 5% -> batch 25% -> 전체 적용 순서로 실행하고 실패율 1% 초과 시 자동 중단
3. secret은 Ansible Vault, Chef Encrypted Data Bag, Puppet Hiera eyaml로 분리하고 실행 로그를 180일 이상 보존

**결론 (2줄):**
- 기술사 판단: 임시 작업과 빠른 도입은 Ansible, 수천 노드 지속 수렴은 Chef·Puppet agent 모델 선택
- 향후 방향: 구성관리는 immutable image, Kubernetes, GitOps와 결합되어 OS baseline과 정책 준수 자동 점검으로 확장

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "구성관리 도구를 설명하시오" | idempotency와 push/pull 흐름 | Ansible·Chef·Puppet 차이 |
| 요구사항 명시형 | "서버 구성 표준화 방안을 제시하시오" | baseline, dry-run, 단계 배포 절차 | 패치·권한·drift 리스크 대응 |

> 요약: 설명형은 도구 구조, 방안형은 표준 구성·단계 배포·준수 지표 중심으로 전환한다.
