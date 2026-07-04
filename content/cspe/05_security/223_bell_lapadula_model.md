---
title: "Bell-LaPadula 기밀성 모델 (Bell-LaPadula Model)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 223
---

# 📖 【암기용】 개념 완전 이해

> 목적: Bell-LaPadula 모델을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 보안등급이 있는 환경에서 기밀 정보가 낮은 등급으로 흘러가지 않게 막는 모델
- **왜 필요한가**: 군사·정부·방산 시스템은 정보를 많이 쓰는 것보다 기밀 자료가 낮은 권한 영역으로 유출되지 않는 것이 우선이다. 등급 기반 규칙으로 정보흐름을 통제한다.
- **핵심 직관**: 낮은 계급은 높은 기밀 문서를 읽을 수 없고, 높은 계급은 낮은 등급 문서에 기밀을 적어 내려보낼 수 없다.

## 깊이 이해
- **배경·문제의식**: 임의 접근통제는 소유자가 권한을 줄 수 있어 기밀 정책을 일관되게 유지하기 어렵다. Bell-LaPadula는 중앙 정책이 보안등급을 강제하는 Mandatory Access Control 모델이다.
- **작동 원리**: Subject와 Object에 보안등급을 부여한다. Simple Security Property는 no read up, Star Property는 no write down을 요구한다.
- **비유**: 3급 비밀 문서는 2급 권한자가 읽을 수 없고, 1급 권한자가 3급 게시판에 내용을 쓰면 상위 기밀이 아래로 새므로 금지한다.
- **구체 예시**: `Top Secret > Secret > Confidential > Unclassified`에서 Secret 사용자는 Confidential 문서를 읽을 수 있지만 Top Secret 문서는 읽을 수 없다. Secret 사용자는 Unclassified 문서에 쓰기 금지 대상이다.
- **흔한 오해·주의점**: Bell-LaPadula는 기밀성 모델이다. 데이터 정확성·변조 방지는 Biba나 Clark-Wilson에서 다루는 무결성 관점이다.

## 연결 개념
- Mandatory Access Control — 중앙 정책으로 주체와 객체 등급을 강제
- Biba Integrity Model — 정보흐름 방향이 Bell-LaPadula와 반대인 무결성 모델
- Multilevel Security — 서로 다른 보안등급 사용자가 하나의 시스템을 공유하는 구조

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: no read up, no write down을 기밀 정보흐름 통제와 연결하고, Biba·Brewer-Nash와 보호 목표를 구분한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Bell-LaPadula Model은 주체·객체 보안등급을 기준으로 상위 기밀 읽기와 하위 등급 쓰기를 제한하는 기밀성 중심 MAC 모델이다.
> 2. **가치**: 군사·정부·방산의 다중등급 시스템에서 상위 기밀이 낮은 권한 영역으로 이동하는 경로를 정책으로 차단한다.
> 3. **판단 포인트**: no read up은 비인가 열람 방지, no write down은 기밀 하향 유출 방지이며 무결성 보호 모델과 혼동하지 않아야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 기밀성 정보흐름 통제 이해 확인 | subject, object, security level, no read up, no write down | 접근통제를 인증 절차로만 설명 |
| MAC 모델 적용 판단 확인 | 중앙 정책, 등급 라벨, 허가 등급 비교 | DAC/RBAC와 강제 정책 차이를 누락 |
| 모델 간 비교 역량 확인 | Biba는 무결성, Brewer-Nash는 이해상충 | 무결성 향상을 Bell-LaPadula 효과로 서술 |

> 요약: 이 문제는 기밀성 보호 목표와 등급 기반 읽기·쓰기 제한 규칙을 정확히 연결하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 기밀성 중심 등급 접근통제
- 배경: 다중등급 군사·정부 시스템은 객체 소유자 권한 위임보다 중앙 보안등급 정책으로 상위 기밀의 하향 흐름을 막아야 함
- 필요성: MAC 정책에서 subject clearance와 object classification 라벨을 100% 적용하고 no read up, no write down 위반 0건을 검증해야 함

---

## Ⅱ. 구조 및 구성요소

```text
Subject -> Security Level 비교 -> Object 접근 결정
            / Read: no read up
            / Write: no write down
            / Policy: MAC
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Subject | 정보에 접근하는 사용자·프로세스 | 사용자 clearance 필요 |
| Object | 보호 대상 파일·DB·메시지 | 객체 classification 필요 |
| Security Level | Top Secret, Secret, Confidential 등 등급 | 등급 순서와 범주 필요 |
| Simple Security Property | 상위 등급 객체 읽기 금지 | no read up |
| Star Property | 하위 등급 객체 쓰기 금지 | no write down |

> 요약: Bell-LaPadula는 주체 허가등급과 객체 분류등급을 비교해 읽기와 쓰기의 허용 방향을 결정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
접근 요청 -> Subject clearance 확인 -> Object classification 확인
-> Read/Write 동작 구분 -> 등급 규칙 적용 -> 허용/거부 로그
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자·프로세스의 보안 허가등급 확인 | clearance 라벨 누락 0건 |
| 2 | 파일·테이블·메시지의 분류등급 확인 | classification 라벨 100% |
| 3 | 읽기 요청이면 no read up 적용 | subject level >= object level |
| 4 | 쓰기 요청이면 no write down 적용 | subject level <= object level |
| 5 | 정책 결정과 사유 기록 | 감사로그 1년 보관 |

> 요약: 읽기는 상향 금지, 쓰기는 하향 금지 규칙으로 상위 기밀이 낮은 등급 영역으로 흐르지 않게 한다.

---

## Ⅳ. 특징

| 구분 | 임의 접근통제 | Bell-LaPadula | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 정책 주체 | 객체 소유자 권한 부여 | 중앙 보안정책 강제 | MAC 정책 변경 승인 2인 이상 |
| 보호 목표 | 사용 편의 중심 권한 공유 | 기밀성 정보흐름 차단 | Secret 이상 자료 하향 쓰기 0건 |
| 규칙 | ACL·소유자 권한 | no read up, no write down | 등급 라벨 100% 적용 |
| 적용 환경 | 일반 업무시스템 | 군사·정부·방산 다중등급 | MLS, Cross Domain Solution |

> 요약: Bell-LaPadula는 소유자 권한 위임보다 중앙 등급 정책을 우선하여 기밀 정보의 하향 흐름을 차단한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | DAC/RBAC | MAC 기반 등급 비교 | 상위 기밀 유출 방지가 최우선인 환경 |
| 비용/성능 | 라벨 없는 단순 권한 | 모든 객체 보안 라벨 관리 | 문서·DB row 라벨링 가능 여부 |
| 운영/위험 | 업무 공유 유연성 | 등급 간 데이터 이동 제한 | 하향 전송 승인 프로세스 필요 |

> 요약: 보안등급이 법·군사 정책으로 강제되는 시스템은 Bell-LaPadula가 적합하나, 라벨 관리와 하향 전송 절차가 필수다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 라벨 오류 | 객체 분류 누락·오분류 | 자동 분류, 2인 검토 | 라벨 누락 0건, 오분류 재심률 |
| 업무 지연 | 하위 등급 보고서 작성 제한 | 정제 절차, Cross Domain Solution | 하향 전송 승인 시간 |
| 은닉 채널 | 로그·타이밍·파일명으로 정보 노출 | covert channel 분석, rate limit | 채널 분석 결과, 이상 트래픽 |

> 요약: 라벨 오류, 하향 전송 지연, 은닉 채널이 주요 리스크이며 분류 검토와 전송 통제로 보완한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 라벨 완전성 | 주체·객체 보안 라벨 100% | IAM, 문서관리, DB 라벨 스캔 |
| 규칙 위반 | no read up/no write down 위반 0건 | 정책 테스트, 감사로그 분석 |
| 하향 전송 | 승인된 정제 절차 100% | Cross Domain Solution 로그 |

> 요약: 적용 성과는 라벨 완전성, 규칙 위반 건수, 하향 전송 승인 로그로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 등급 체계 수립: Top Secret, Secret, Confidential, Unclassified와 조직별 compartment를 라벨 표준으로 지정
2. 정책 엔진 구현: OS MAC, DB row label security, 문서 DRM에 no read up/no write down 규칙 적용
3. 감사·전송 통제: 하향 전송은 정제·승인·기록 절차를 거치고, 위반 이벤트는 SIEM 경보로 연계

**결론 (2줄):**
- 기술사 판단: 군사·정부 기밀처럼 기밀성 유출 피해가 큰 환경은 Bell-LaPadula 기반 MAC과 라벨 관리가 필요함
- 향후 방향: MLS와 Cross Domain Solution을 결합해 등급 간 협업 요구와 기밀성 통제를 동시에 처리함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Bell-LaPadula 모델을 설명하시오" | no read up/no write down 흐름 | DAC/RBAC, Biba와 보호 목표 차이 |
| 요구사항 명시형 | "기밀성 통제 방안을 제시하시오", "비교하시오" | 등급 라벨과 정책 엔진 설계 | 라벨 관리, 하향 전송, 은닉 채널 대응 |

> 요약: 설명형은 등급 기반 읽기·쓰기 규칙을, 비교·방안형은 기밀성 보호와 운영 통제 지표를 강조한다.
