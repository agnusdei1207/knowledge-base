---
title: "Prompt Engineering In-Context Learning"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ICL(In-Context Learning)은 LLM의 transformer self-attention 내부, 특히 **induction head 회로**가 입력 프롬프트에 삽입된 (xᵢ, yᵢ) demonstration 쌍들로부터 `(이전 토큰 패턴) -> (다음 토큰 예측)` 메타-매핑을 추론하여, **∇θL = 0** (가중치 동결) 상태로 inference 시점에서 신규 task를 일반화하는 emergent meta-learning 현상이다.
> 2. **가치**: 10~100개의 라벨링된 demonstration만으로 fine-tuning 대비 **60~80% 성능을 1/6,600 TCO**(GPT-4 기준, fine-tuning ~$200/epoch vs. 1k-token ICL 호출 ~$0.03)로 달성하며, 배포 후 즉시 모델 적응과 prompt hot-swap이 가능하다.
> 3. **판단 포인트**: ①Fine-Tuning vs. ICL vs. RAG의 **데이터량·latency·업데이트 빈도** 3축 trade-off, ②Demonstration의 **semantic diversity vs. task coverage** 균형, ③Context window(8K~200K) 내 **attention dilution** 방지를 위한 정보 밀도 최적화, ④**Prompt injection·data exfiltration** 등
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 297 / 300

<- **이전**: [296. RAG 아키텍처 검색 증강 생성 파이프라인 (RAG Architecture Retrieval Augmented Generation)](/studynote/14_data_engineering/05_exam_keywords/296_rag_architecture/)
**다음**: [298. AI 에이전트 도구 사용 자율 워크플로 (AI Agent Tool Use Autonomous Workflow)](/studynote/14_data_engineering/05_exam_keywords/298_ai_agent_workflow/) ->

---
