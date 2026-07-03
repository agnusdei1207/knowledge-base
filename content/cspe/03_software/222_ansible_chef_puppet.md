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
- **개요**: Ansible·Chef·Puppet은 이미 생성된 서버 **내부**의 OS 설정·패키지·서비스 상태를 코드로 정의하고 반복 실행해 목표 상태로 수렴시키는 **구성관리(Configuration Management)** 도구다.
- **왜 필요한가**: 서버 200대의 SSH 설정, 계정, 패치 버전을 사람이 수작업으로 맞추면 서버마다 조금씩 달라지고(구성 편류), 어느 서버가 보안 기준을 어겼는지 감사로 확인하기 어렵다.
- **핵심 직관**: Terraform(IaC, 220·221)이 서버라는 "건물"을 짓는다면, Ansible·Chef·Puppet은 그 건물 "안"의 가구 배치·전등 상태를 계속 점검해 기준대로 맞춘다 — 역할이 다르다.

## 핵심 용어 정리

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 구성관리(Configuration Management) | 이 개념이 속한 상위 범주 — 서버 내부 설정을 코드·정책으로 관리하는 것 전반 | 건물 내부 시설 관리 |
| Push 방식 | 관리 서버가 대상 서버에 접속해 즉시 작업을 밀어넣음(Ansible) | 관리자가 직접 각 방을 찾아가 점검 |
| Pull 방식 | 대상 서버의 agent가 주기적으로 중앙 서버에 접속해 최신 기준을 받아옴(Chef, Puppet) | 각 방의 점검기가 스스로 본부에 접속해 기준표를 받아옴 |
| Agentless | 대상 서버에 상시 실행 프로그램을 설치하지 않고 SSH 등 기존 프로토콜만 사용(Ansible) | 방문 점검 — 상주 인력 불필요 |
| Agent | 대상 서버에 상시 설치되어 중앙과 통신하는 실행 프로그램(Chef의 chef-client, Puppet agent) | 각 방에 상주하는 점검기 |
| Playbook(Ansible) | YAML로 작성한 "무엇을 어떤 순서로 맞출지"의 작업 정의 | 방문 점검 체크리스트 |
| Recipe(Chef) | Ruby DSL로 작성한 구성 정책 단위 | 점검기에 입력된 세부 규정집 |
| Manifest(Puppet) | Puppet DSL로 작성한 선언형 리소스 정의 | 점검기에 등록된 표준 설계도 |
| Idempotency(멱등성) | 220 참조 — 같은 코드를 여러 번 실행해도 결과가 항상 동일함 | 이미 켜진 스위치를 다시 눌러도 상태 그대로 |
| Convergence(수렴) | 실행할 때마다 현재 상태를 목표 상태로 조금씩 맞춰가는 것 | 온도조절기가 설정 온도로 계속 맞춰가는 동작 |

## 깊이 이해

### IaC(Terraform)와의 역할 분리 — "만든다" vs "안을 맞춘다"
- Terraform은 "EC2 인스턴스가 존재해야 한다"까지만 책임진다. 인스턴스가 만들어진 뒤 그 안에 nginx를 설치하고, SSH 설정에서 root 로그인을 막고, NTP 시간 동기화를 설정하는 것은 Terraform의 역할이 아니다. 이 "인스턴스 내부" 작업을 코드화하는 것이 Ansible·Chef·Puppet이다. 실무에서는 Terraform이 인스턴스를 만든 직후 Ansible playbook을 자동 실행해 초기 설정을 완료하는 식으로 두 도구를 함께 쓴다.

### Push(Ansible) vs Pull(Chef·Puppet) — 동작 방식의 차이(수치 예)
- Ansible은 관리 서버에서 `ansible-playbook`을 실행하는 즉시 SSH로 대상 서버 200대에 접속해 playbook을 순차/병렬 실행한다. 실행 시점을 사람이 직접 정하므로 "지금 당장 200대에 패치를 배포"하는 긴급 작업에 적합하다. 별도 agent 설치가 필요 없어(agentless) 도입이 빠르다.
- Chef와 Puppet은 각 서버에 설치된 agent가 예를 들어 **30분마다** 자동으로 중앙 서버(Chef Server, Puppet Master)에 접속해 최신 recipe/manifest를 받아 스스로 적용한다. 사람이 실행을 트리거하지 않아도 지속적으로 기준을 재적용하므로, 누군가 수동으로 설정을 바꿔도 최대 30분 안에 원래 기준으로 자동 복구(수렴)된다 — 이 지속 보정이 Push 방식보다 강력한 지점이다.

### Idempotency와 Convergence — 왜 "여러 번 실행해도 안전"한가(수치 예)
- Ansible playbook에 "nginx 패키지를 설치하라"는 task가 있다고 하자. 처음 실행하면 nginx가 없으므로 설치(changed)하고, 이미 설치된 서버에서 같은 playbook을 다시 실행하면 "이미 설치돼 있음"을 확인하고 아무 것도 하지 않는다(ok, changed=0). 이 성질 덕분에 같은 playbook을 매일 자동 실행해도 안전하다.
- Puppet agent가 30분마다 실행되며 "SSH root 로그인 금지"라는 manifest를 지속 적용하는 도중, 누군가 콘솔에서 수동으로 root 로그인을 다시 열어도, 다음 30분 주기 실행에서 Puppet이 이를 감지하고 다시 금지 상태로 되돌린다 — 이것이 수렴(Convergence)이다. 사람이 매번 재점검할 필요 없이 "기준"이 스스로 유지된다.

### 실제 적용 예시 — CIS 벤치마크 배포(수치 예)
- CIS(Center for Internet Security) 벤치마크 기준으로 "SSH root 로그인 금지, 8자리 이상 비밀번호 정책, NTP 서버 지정, logrotate 30일 보관"을 서버 200대에 적용한다고 하자. Ansible이라면 이 4개 항목을 하나의 playbook으로 작성해 한 번에 200대에 push한다(예상 실행 시간 수 분). Chef/Puppet이라면 같은 항목을 recipe/manifest로 등록해두면 30분 주기마다 자동으로 재확인·재적용되어, 새로 추가되는 서버도 부트스트랩만 하면 자동으로 같은 기준에 수렴한다.

### 비유와 흔한 오해
- **비유**: Ansible은 관리자가 체크리스트를 들고 직접 각 방을 찾아가 점검하는 방식이고, Chef·Puppet은 각 방에 설치된 점검기가 본부의 최신 기준표를 스스로 주기적으로 받아와 알아서 고치는 방식이다.
- **오해**: "구성관리 도구가 있으면 IaC(Terraform)가 필요 없다"는 오해가 흔하다. 구성관리는 "이미 존재하는 서버 내부"만 다루므로, 서버·네트워크·DB 리소스 자체를 만들고 지우는 것은 여전히 IaC의 몫이다. 또한 "불변 인프라(219)와 구성관리는 반대 철학"이라는 점도 중요하다 — 불변 인프라는 서버를 고치지 않고 새 이미지로 교체하는 반면, 구성관리는 떠 있는 서버를 지속적으로 "고쳐서" 기준에 맞춘다. 두 접근을 섞어 쓸 때는(예: 이미지 빌드 시점에만 Ansible로 초기 설정을 굽고, 운영 중에는 손대지 않는 방식) 역할 경계를 분명히 해야 한다.

## 연결 개념
- Infrastructure as Code(220) — 서버·네트워크 자체를 만드는 상위 자동화, 이 도구들은 그 "내부"를 담당
- Immutable Infrastructure(219) — 서버를 지속 보정하는 이 접근과 반대로, 서버를 고치지 않고 새 이미지로 교체하는 접근
- Patch Management — CVE 대응 등 OS·미들웨어 취약점 보정을 구성관리 도구로 자동화하는 실무 응용

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

- 개요: 서버 구성 코드 관리 도구
- 배경: VM 생성 이후 OS 패치, 계정, 서비스, 설정 파일은 지속적으로 바뀐다.
- 필요성: 100대 서버의 drift와 취약 설정을 변경 시점에 탐지해야 한다.

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
