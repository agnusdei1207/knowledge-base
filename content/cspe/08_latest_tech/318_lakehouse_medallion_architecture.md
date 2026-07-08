---
title: "Lakehouse Medallion Architecture 메달리온 아키텍처 (Medallion Architecture)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 318
extra:
  question_no: "318"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Medallion Architecture는 Bronze와 Silver와 Gold 계층으로 데이터 신뢰 수준과 소비 목적을 분리하는 lakehouse 패턴임
- 원천 보존과 정제와 업무 제공 단계를 분리해 재처리와 품질 통제를 쉽게 만듦
- 계층 이름보다 승격 기준과 품질 규칙과 권한 분리가 더 중요함

## Ⅰ. 개요

- **정의/개념**: Medallion Architecture는 lakehouse 데이터를 Bronze와 Silver와 Gold 같은 계층으로 나누어 원천 보존과 정제 표준화와 업무 소비 모델을 단계적으로 분리하는 데이터 운영 패턴임
- **배경/필요성**: 원본과 정제본과 집계본이 한 공간에 섞이면 재처리 경로와 품질 책임과 접근 권한이 불명확해져 데이터 신뢰와 운영 효율이 떨어지므로 계층 구조가 필요해짐

## Ⅱ. 특징

- 원천 데이터와 소비 데이터를 분리해 재처리와 문제 추적이 쉬워짐
- 계층마다 품질 규칙과 접근 권한을 다르게 설정해 통제 수준을 높일 수 있음
- streaming과 batch를 함께 수용하면서도 신뢰 수준을 단계적으로 높이기 좋음
- 계층 수만 늘고 승격 기준이 모호하면 데이터 복제만 늘어 운영 비용이 커질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Bronze | Silver | Gold |
|:---|:---|:---|:---|
| 데이터 성격 | 원천 보존 | 정제와 표준화 | 업무 소비 모델 |
| 품질 수준 | 기본 완전성 | 정합성과 중복 제거 | KPI와 업무 규칙 충족 |
| 대표 사용자 | 엔지니어 | 분석가와 ML 팀 | BI와 서비스 팀 |
| 운영 목적 | 재처리 기반 | 공통 활용 기반 | 직접 소비 가치 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Bronze Layer | 원천 데이터를 거의 그대로 보존해 재처리와 감사 근거를 제공하는 원본 계층임 |
| Silver Layer | 타입 정리와 중복 제거와 표준화를 수행해 여러 소비자가 재사용할 수 있는 공통 정제 계층임 |
| Gold Layer | KPI와 mart와 feature 같은 목적형 모델을 제공해 업무와 AI 소비에 바로 연결되는 최종 활용 계층임 |
| Quality and Promotion Rules | 각 계층으로 승격될 조건과 검증 규칙을 정의해 신뢰 수준을 단계적으로 높이는 통제 장치임 |
| Lineage and Access Control | 계층 이동 경로와 권한 범위를 관리해 책임 추적과 보안 분리를 가능하게 하는 운영 계층임 |

```text
+-------------+    +-------------+    +-------------+
| Bronze      | -> | Silver      | -> | Gold        |
+-------------+    +-------------+    +-------------+
        \______________  |  ______________/
                       v
               +-----------------+
               | Quality / ACL   |
               +-----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 원천 적재     | -> | 정합성 검증   | -> | 표준화/정제    | -> | 업무 모델링   | -> | 소비/피드백    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **원천 적재**: 이벤트와 파일과 DB 추출 데이터를 Bronze에 적재함
2. **정합성 검증**: 기본 완전성과 스키마 조건을 점검함
3. **표준화와 정제**: Silver에서 중복 제거와 코드 표준화를 수행함
4. **업무 모델링**: Gold에서 KPI와 서비스 목적형 테이블을 구성함
5. **소비와 피드백**: BI와 ML과 애플리케이션이 활용하며 품질 피드백을 반환함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 계층 승격 기준이 모호하면 동일 데이터가 여러 층에 중복 저장되고 책임 경계도 흐려질 수 있음
   - 해결방안: promotion criteria standard와 layer purpose taxonomy를 적용하고 duplicate dataset ratio와 ambiguous ownership count로 검증함
2. 문제: Silver 정제 규칙이 도메인마다 달라지면 Gold 계층에서 동일 지표가 서로 다른 값으로 계산될 수 있음
   - 해결방안: shared transformation library와 canonical business rule governance를 적용하고 cross domain metric consistency rate와 rule drift count로 검증함
3. 문제: 계층별 보관 정책과 권한 정책이 없으면 원천 데이터 노출 위험과 저장 비용 증가가 함께 커질 수 있음
   - 해결방안: layer specific retention ACL policy를 적용하고 sensitive raw access count와 storage cost per layer로 검증함

## Ⅶ. 적용 사례

- lakehouse 운영팀이 계층 승격 기준을 표준화하며 확인 지표는 duplicate dataset ratio와 ambiguous ownership count임
- 전사 데이터 조직이 공통 변환 라이브러리를 운영하며 확인 지표는 cross domain metric consistency rate와 rule drift count임
- 보안 거버넌스가 계층별 보관과 권한 정책을 적용하며 확인 지표는 sensitive raw access count와 storage cost per layer임

## Ⅷ. 결론

Medallion Architecture는 계층 이름 자체보다 각 층의 책임과 승격 규칙을 분명히 할 때 lakehouse 운영 안정성과 재사용성이 함께 올라감.
