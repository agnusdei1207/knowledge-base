---
title: "스케일드 애자일 프레임워크 (SAFe)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-software"
weight: 35
---

## 핵심 인사이트 (3줄 요약)
- 수백~수천 명의 개발자가 참여하는 대규모 엔터프라이즈 환경에 애자일과 린(Lean) 원칙을 적용하기 위해 설계된 프레임워크.
- 50~125명 규모의 다수 애자일 팀을 하나의 '기차(ART, Agile Release Train)'로 묶어 리듬을 동기화하고 의존성을 관리함.
- 전사적 비전(Portfolio)과 개별 팀의 실행(Team) 계층을 수직적으로 정렬(Alignment)하여 대기업이 애자일하게 움직이도록 돕는 것이 본질.
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | SAFe(Scaled Agile Framework)는 린, 애자일, 시스템 사고를 결합하여 엔터프라이즈 규모로 소프트웨어를 개발 및 전달하... | "건물 증축" |
| **필요성** | 단일 스크럼 팀(5~9명) 수준의 애자일을 대형 프로젝트나 전사 차원으로 확장하려 할 때 발생하는 팀 간 의존성, 방향성 상실, 통합 지연... | "이 개념의 핵심" |
| **3대 핵심 계층 (Essential SAFe 기준)** | 1. **Team Level**: 기존 스크럼/칸반을 수행하는 애자일 팀 (PO, SM, Team) | "이 개념의 핵심" |
| **Program Level (ART)** | 5~12개 팀(50~125명)이 묶인 Agile Release Train | "학습하는 기계" |
| **Portfolio Level** | 기업의 전략적 테마와 예산을 포트폴리오 에픽(Epic)으로 관리 | "이 개념의 핵심" |
| **PI (Program Increment)** | ART가 비즈니스 가치를 전달하는 타임박스(통상 8~12주) | "이 개념의 핵심" |
| **실무 적용의 딜레마** | SAFe는 '폭포수의 탈을 쓴 애자일(Water-Agile-Fall)'이라는 비판을 받기도 함 | "단거리 반복 달리기" |

---


## Ⅰ. 개요 및 필요성
- **개요**: SAFe(Scaled Agile Framework)는 린, 애자일, 시스템 사고를 결합하여 엔터프라이즈 규모로 소프트웨어를 개발 및 전달하는 지식 기반 프레임워크.
- **필요성**: 단일 스크럼 팀(5~9명) 수준의 애자일을 대형 프로젝트나 전사 차원으로 확장하려 할 때 발생하는 팀 간 의존성, 방향성 상실, 통합 지연 문제를 해결하기 위함.
---
## Ⅱ. 아키텍처 및 핵심 원리
- **3대 핵심 계층 (Essential SAFe 기준)**:
  1. **Team Level**: 기존 스크럼/칸반을 수행하는 애자일 팀 (PO, SM, Team).
  2. **Program Level (ART)**: 5~12개 팀(50~125명)이 묶인 Agile Release Train. 이 기차를 이끄는 RTE(Release Train Engineer)와 PM이 존재.
  3. **Portfolio Level**: 기업의 전략적 테마와 예산을 포트폴리오 에픽(Epic)으로 관리.
- **PI (Program Increment)**: ART가 비즈니스 가치를 전달하는 타임박스(통상 8~12주). 

```text
[ SAFe ART (Agile Release Train) ]
 
 Portfolio  (Strategic Themes / Value Streams / Epics)
   ⬇️ 
 Program    ====( ART: Agile Release Train, 50~125 people )==== ➡️ Release
 Level           [ PI Planning ] ➡️ [ PI 1 ] ➡️ [ PI 2 ]
   ⬇️
 Team Level   (Team 1 Sprint) / (Team 2 Sprint) / (Team 3 Sprint)  (Synchronized)
```
---
## Ⅲ. 비교 및 연결
| 구분 | SAFe | LeSS (Large-Scale Scrum) | Scrum of Scrums (SoS) |
|---|---|---|---|
| **확장 방식** | 새로운 역할(RTE 등)과 계층(Portfolio/Program) 추가 | 스크럼의 기본 틀을 최대한 유지하며 다수 팀으로 확장 | 기존 스크럼 팀의 대표자 회의(가장 단순한 확장) |
| **규칙의 복잡도** | 매우 무겁고 체계적 (대기업 선호) | 가볍고 개발자 중심적 | 매우 단순 |
| **도입 환경** | 기존 계층 구조를 가진 대형 금융/제조/공공기관 | 수평적인 문화를 가진 테크 기업 | 초기 확장 단계 조직 |
---
## Ⅳ. 실무 적용 및 기술사 판단
- **실무 적용의 딜레마**: SAFe는 '폭포수의 탈을 쓴 애자일(Water-Agile-Fall)'이라는 비판을 받기도 함. 무거운 프로세스와 새로운 직책(RTE, STE)이 오히려 애자일의 민첩성을 저해할 수 있음.
- **성공 요인**: PI Planning(PI 계획 수립 회의)에 모든 팀원이 한자리에 모여 2일간 의존성을 직접 확인하고 줄을 긋는 대면(또는 온라인 동시) 행사가 SAFe 성공의 가장 중요한 촉매제임.
---
## Ⅴ. 기대효과 및 결론
- 수백 명의 개발자가 각자 놀지 않고 기업의 전략적 목표(Alignment)에 맞춰 동일한 박자(Cadence)로 제품을 출시할 수 있음.
- 조직 전체를 단숨에 뜯어고치기 힘든 엔터프라이즈 환경에서, 기존 관료주의적 거버넌스와 애자일 개발을 타협시키는 가장 현실적인 확장(Scaling) 솔リューション.
---
### 📌 관련 개념 맵
- 애자일 ➡️ 팀 단위 스크럼 ➡️ 애자일 확장(Scaling) ➡️ SAFe / LeSS / DaD

### 📈 관련 키워드 및 발전 흐름도
- Lean Manufacturing ➡️ Agile (2001) ➡️ SAFe 1.0 (2011) ➡️ SAFe 6.0 (현재, 클라우드/AI 및 비즈니스 민첩성 강화)

### 👶 어린이를 위한 3줄 비유 설명
1. 10명이 합창을 할 때(스크럼)는 서로 눈빛만 봐도 맞출 수 있어요.
2. 하지만 1,000명이 합창을 하려면 여러 구역으로 나누고, 전체를 지휘하는 총지휘자(ART)와 악보(PI)가 따로 필요해요.
3. 이렇게 수많은 사람들이 한 치의 오차 없이 동시에 예쁜 화음을 낼 수 있도록 도와주는 거대한 규칙서가 SAFe랍니다.
