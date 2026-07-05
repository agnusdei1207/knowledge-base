---
title: "애자일 스크럼 (Agile Scrum)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-software"
weight: 34
---

## 핵심 인사이트 (3줄 요약)
- 럭비의 스크럼 대형처럼 팀이 똘똘 뭉쳐 짧은 반복 주기(Sprint) 내에 잠재적 배포 가능한 소프트웨어를 만들어내는 애자일 프레임워크.
- 3가지 역할(PO, SM, Team), 3가지 산출물(Product Backlog, Sprint Backlog, Increment), 5가지 이벤트(스프린트, 계획, 일일, 리뷰, 회고)가 핵심 구성 요소.
- 투명성(Transparency), 검사(Inspection), 적응(Adaptation)의 경험주의 원칙을 바탕으로 지속적인 가치 인도를 목표로 함.
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **애자일 스크럼** | 애자일 스크럼 (Agile Scrum)의 핵심 개념 | 이 주제의 본질 |

---

## Ⅰ. 개요 및 필요성
- **개요**: 복잡한 환경 속에서 팀이 가치를 창출할 수 있도록 돕는 경량화된 애자일 프레임워크의 사실상 표준(De facto).
- **필요성**: 장기적인 계획과 방대한 문서 위주의 프로젝트 실패율이 높아지면서, 짧은 주기의 피드백 루프를 통해 고객의 진짜 요구사항을 발굴하고 변화에 기민하게 대응할 수단이 필요함.
---
## Ⅱ. 아키텍처 및 핵심 원리
- **3 역할 (Roles)**:
  1. **Product Owner (PO)**: 제품 백로그 우선순위 결정, 비즈니스 가치 극대화 책임 (고객 대표).
  2. **Scrum Master (SM)**: 팀의 장애물(Impediment) 제거, 스크럼 원칙 준수를 돕는 서번트 리더(Servant Leader).
  3. **Development Team**: 자가 조직화(Self-organizing)되고 교차 기능(Cross-functional)을 가진 전문가 집단.

```text
[ Scrum Process Flow ]
                                (Daily Scrum)
 Product       Sprint                ⬇️              Potentially
 Backlog ➡️   Planning  ➡️ [ Sprint (1~4 Weeks) ] ➡️ Shippable 
 (by PO)      Backlog                ⬇️              Increment
                               (Review / Retro) 
```
- **5 이벤트 (Events)**:
  1. **Sprint**: 모든 이벤트의 컨테이너 (보통 2주).
  2. **Sprint Planning**: 이번 스프린트에 할 일 선정.
  3. **Daily Scrum**: 매일 15분, 진척과 장애물 공유.
  4. **Sprint Review**: 스프린트 종료 시 결과물 시연 및 피드백.
  5. **Sprint Retrospective (회고)**: 다음 스프린트 프로세스 개선점 도출 (KPT 방식 등).
---
## Ⅲ. 비교 및 연결
| 구분 | 스크럼 (Scrum) | 칸반 (Kanban) | 익스트림 프로그래밍 (XP) |
|---|---|---|---|
| **초점** | 팀 매니지먼트, 역할, 타임박스 | 워크플로우 최적화, WIP 제한 | 엔지니어링 프랙티스 (TDD, 짝 프로그래밍) |
| **주기(Iteration)** | 정해진 타임박스 (1~4주) | 타임박스 없음 (연속적 흐름) | 1~2주 (스크럼과 결합하여 자주 쓰임) |
| **역할 정의** | PO, SM 등 역할 명확 | 기존 역할 유지 | 개발자 중심 |
---
## Ⅳ. 실무 적용 및 기술사 판단
- **안티 패턴(Anti-pattern)**: 데일리 스크럼이 스크럼 마스터를 향한 진척 보고(Reporting) 회의로 변질되거나, PO가 스토리 포인트나 작업 방식(How)에 개입하는 마이크로 매니지먼트.
- **실무 융합 (ScrumBan, XP 연계)**: 스크럼의 관리 체계 위에 XP의 엔지니어링 프랙티스(CI/CD, TDD)를 도입하고, 유지보수 조직은 칸반 보드로 WIP를 제한하는 하이브리드 모델(ScrumBan) 적용이 현대 실무의 정석.
---
## Ⅴ. 기대효과 및 결론
- 고객 피드백 루프 단축으로 시장 적합성(Product-Market Fit) 달성 확률 증가 및 지속적인 프로세스 개선(회고) 효과.
- 스크럼은 단순한 개발 방법론이 아니라 '조직 문화'의 변혁을 요구하므로, 최고 경영진의 스폰서십과 팀의 자율성(Autonomy) 보장이 성공의 핵심 열쇠임.
---
### 📌 관련 개념 맵
- 애자일 ➡️ 프레임워크 (Scrum) ➡️ 관리 지표 (Burn-down Chart, Story Point) ➡️ 규모 확장 (SAFe, LeSS)

### 📈 관련 키워드 및 발전 흐름도
- 경험주의 프로세스 ➡️ Scrum (Jeff Sutherland, 1995) ➡️ Agile Manifesto (2001) ➡️ SAFe (Enterprise Scrum)

### 👶 어린이를 위한 3줄 비유 설명
1. 스크럼은 친구들끼리 역할극을 하면서 블록 장난감을 만드는 놀이예요. 
2. '대장(PO)'은 무엇을 만들지 리스트를 적어주고, '도우미(SM)'는 친구들이 싸우지 않게 도와줘요.
3. 매일 아침 "어제 뭐 했어? 오늘 뭐 할 거야?" 짧게 얘기하고(일일 스크럼), 2주 뒤에 만든 걸 엄마한테 자랑하는(리뷰) 방식이랍니다.
