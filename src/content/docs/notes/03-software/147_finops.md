---
sidebar:
  order: 147
  label: "147. FinOps 클라우드 비용 최적화 (FinOps)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "FinOps 클라우드 비용 최적화 (FinOps)"
date: "2026-08-14T01:40:00+09:00"
tags: ["notes-software"]
weight: 147
extra:
  question_no: "147"
  source_status: "기출"
  source_history: "123회, 135회"
  priority: 70
  priority_note: "비용 가시화•최적화•운영 순환이 반복 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **FinOps (Financial Operations / 핀옵스)**: 기술(DevOps), 재무(Finance), 비즈니스(Business) 조직이 결합하여 클라우드 비용을 투명하게 가시화(Inform), 최적화(Optimize), 자동화 운영(Operate)하는 지속적 재무 거버넌스 및 비용 최적화 체계.
- **Unit Economics (단위 경제성)**: 총비용 절감이 아닌, '고객 1명당 클라우드 서비스 원가' 또는 '주문 1건당 인프라 비용' 지표를 측정해 비즈니스 수익성과 비용을 연결하는 핵심 지표.
- **RI / Savings Plans (예약 인스턴스 & 절약 플랜)**: 1년/3년 단위 장기 사용 약정을 통해 클라우드 컴퓨팅 단가를 최대 70% 이상 할인받는 요율 최적화 제도.

</details>

- 정의/개념: 기술•재무•사업이 Cloud 가치를 운영하는 **FinOps**
- 배경/필요성: 종량제 자원의 분산 소유로 **비용 귀속•가치 판단** 곤란

#### 한줄 요약

- 공동 수도 계량기만 보고 물을 줄이지 않고 가구별 사용량과 생산량을 함께 보듯, 비용 소유자와 업무 성과를 연결해 낭비와 투자 가치를 구분한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Inform, Optimize, Operate**: 가시성 확보(Inform), 리소스/요율 최적화(Optimize), 자동화 및 문화 정착(Operate) 3단계 지속 순환.

</details>

- **Inform**은 태깅•할당으로 비용과 단위 경제성 가시화
- **Optimize**는 사용량•요율•구조를 비용 대비 개선
- **Operate**는 정책•자동화와 공동 책임을 운영에 정착

#### 한줄 요약

- 전기 사용량, 요금제, 기계 구조를 차례로 바꾸듯 자원 사용량을 줄이고 안정 수요의 단가를 낮춘 뒤 처리 구조까지 반복해서 개선한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Cost Allocation Tagging**: 모든 EC2, S3 자원에 `Team:Checkout, Env:Prod` 태그를 부착해 전사 공유 인프라 비용을 부서별로 100% 투명하게 정산(Cost Attribution)하는 기법.

</details>

| 구성요소 | 책임 |
|---|---|
| Inform | **비용 할당•예측**과 Unit Economics 산출 |
| Optimize | **Right-sizing**•**요율**과 구조 개선 |
| Operate | **정책**•**자동화**와 조직 의사결정 정착 |

#### 한줄 요약

- 여러 가게의 영수증 단위를 맞춰 상품별로 나눈 뒤 판매 한 건당 원가를 계산하고, 개선 순서와 예산 규칙을 한 장부에 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Right-Sizing**: CPU/메모리 평균 사용률이 10% 미만인 EC2 인스턴스를 한 단계 아래 사양(t3.xlarge $\rightarrow$ t3.medium)으로 다운사이징.

</details>

```text
[비용•사용량 자료]
        │
        ▼
1. 비용 귀속
        │
        ▼
2. 단위 경제성 측정
        │
        ▼
3. 개선 후보 평가
        │
        ▼
4. 최적화 실행
        │
        ▼
5. 효과•위험 검증
        │
        └──────── 반복
```

### 동작 원리

1. **비용 귀속**: 태그•계정으로 팀•제품별 비용 할당
2. **단위 경제성 측정**: 거래•고객당 비용과 품질 연결
3. **개선 후보 평가**: 절감액•변경 비용•SLO 위험 비교
4. **최적화 실행**: 사용량•요율•아키텍처 순으로 개선
5. **효과•위험 검증**: 단위 비용과 서비스 품질 재측정

#### 한줄 요약

- 영수증을 팀과 상품에 나눠 판매 한 건당 원가를 계산하고, 절감액과 서비스 위험을 비교해 고칠 순서를 정한 뒤 같은 기준으로 다시 측정한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CAPEX Budget vs OPEX FinOps**: 년 1회 고정 이월 예산(CAPEX)과 일단위 실시간 변동 종량제 절감(OPEX FinOps).

</details>

| 비교 항목 | Traditional IT Cost Management | Modern FinOps Architecture |
|:---|:---|:---|
| 비용 측정 주기 | 정기 사후 정산 중심 | **사용량 기반 지속 관측** |
| 비용 주체 | 재무 부서 중심 | **기술•재무•사업 협업** |
| 핵심 목표 | 예산 이월 방지 및 한도 통제 | **Unit Economics 기반 비즈니스 가치 극대화** |
| 절감 기술 메커니즘 | 인프라 구매 억제 | **Right-sizing, RI/SP, Spot, Auto-Shutdown** |

#### 한줄 요약

- 빈 방을 먼저 없애고 계속 쓸 방은 장기 계약으로 단가를 낮추며, 방 배치 자체가 비싸면 건물 구조를 바꾸듯 세 최적화의 적용 순서와 비용이 다르다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Untagged Resources (태그 미부착 자원)**: 인프라에 소유자 태그가 없어 어느 팀 비용인지 알 수 없는 공백 자원.

</details>

| 3대 FinOps 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Untagged Cloud Resource | 개발자가 태그 없이 EC2 무단 생성 | **IaC (Terraform) 에서 Tag 미입력 시 생성 차단** |
| 2. Dev Server Running 24/7 | 주말/야간에도 개발용 EC2가 계속 켜짐 | **Auto-Shutdown 스크립트 (주말 자동 끄기)** |
| 3. RI Commitment Risk | 3년 약정 후 서비스 철수로 약정 날림 | **Flexible Savings Plans (유연한 SP) 전환** |

> 사례: **토스 / 당근마켓 / 쿠팡 FinOps 팀 신설 및 전사 AWS 클라우드 비용 30% 이상 절감**

#### 한줄 요약

- 밤에 빈 사무실 전기를 끈 뒤 업무가 느려지지 않았는지 확인하고, 장기 계약은 매일 쓰는 최소 전력만큼만 사듯 단위 비용과 안정 수요를 함께 본다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **FinOps 수립 기준(FinOps Architecture Standards)**: Inform-Optimize-Operate 3대 라이프사이클, Tagging 100%, Savings Plans, Right-sizing 및 Unit Economics 지표성에 의거한 체계.

</details>

- 변동 수요는 **Right-sizing**, 안정 수요만 약정 요율 적용

#### 한줄 요약

- 매출이 줄어 전기료만 내려간 경우를 절감으로 보지 않고, 주문 한 건당 비용과 서비스 속도를 확인한 뒤 매일 쓰는 양만 장기 계약한다.
