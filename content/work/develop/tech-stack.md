+++
title = "🛠️ 사내 표준 기술 스택 (Tech Stack)"

[taxonomies]
tags = ["work"]

[extra]
tags = ["work"]
+++

우리 조직에서 사용하고 연구하는 핵심 기술 및 라이브러리 목록과 가이드라인입니다. 각 기술의 이론적 배경과 기초 개념은 관련 <strong>Study Note</strong>에서 깊이 있게 학습할 수 있습니다.

---

## 💻 백엔드 & 인프라 (Backend)

*   **FastAPI:** 가볍고 빠른 비동기 Python 웹 프레임워크. 사내 AI 에이전트 서비스 개발의 메인 뼈대로 채택.
    *   *이론 및 설계:* **소프트웨어 공학의 디자인 패턴** 및 **OS 비동기 I/O 원리** 참고.
*   **Docker & Docker Compose:** 모든 로컬 개발 환경 및 사내 호스팅 서비스(Gitea, Jenkins 등)의 표준 컨테이너화 도구.
    *   *이론 및 설계:* **클라우드 아키텍처 및 컨테이너 가상화** 참고.
*   **Git (GitHub):** 형상 관리 및 <strong><a href="../README.md">README</a></strong> 지식 공동 저장소의 핵심 백엔드.
    *   *프로세스 관리:* **DevOps CI/CD 파이프라인** 참고.

---

## 🗄️ 데이터베이스 & 벡터 검색 (Databases)

*   **PostgreSQL:** 강력한 표준 관계형 DB.
    *   **pgvector:** PostgreSQL 상에서 AI 텍스트 임베딩을 저장하고 유사도 검색(Vector Search)을 수행하는 확장 프로그램.
    *   *이론 및 설계:* **데이터베이스 트랜잭션 및 인덱싱** 참고.
*   **Elasticsearch / OpenSearch:** 형태소 분석 기반의 키워드 검색을 고속으로 수행하기 위한 기본 검색엔진.
    *   *이론 및 설계:* **데이터 엔지니어링** 및 **빅데이터 검색 및 처리** 참고.

---

## 🤖 인공지능 & LLM (AI & Agents)

*   **Claude API (Anthropic):** 고도의 비즈니스 로직 분석 및 코드 생성을 위한 사내 공식 LLM 파트너.
*   **LangChain / LlamaIndex:** AI 에이전트 워크플로우를 빌드하기 위한 오케스트레이션 프레임워크.
*   **Model Context Protocol (MCP):** 에이전트가 CLI나 특정 IDE에 종속되지 않고 외부 시스템과 연결되도록 만드는 표준 인터페이스.
*   **Claude Code:** 코드와 문서를 직접 읽고 수정하며, MCP를 통해 공용 지식 툴을 호출할 수 있는 작업형 AI 클라이언트.
*   <strong>Codex Python SDK (<code>openai-codex</code>):</strong> 내부 문서 자동화 워커, PR 생성기, 검토 배치 작업을 Python 서비스로 구현할 때 쓰는 Codex 실행 SDK.
    *   *이론 및 설계:* **머신러닝/딥러닝 및 LLM/RAG 구조** 참고.

---

## 📚 지식 포털 & 편집 계층 (Knowledge UX)

*   **Quartz:** Markdown 원본을 정적 웹 포털과 그래프 뷰로 렌더링하는 조회 계층.
*   **Decap CMS:** Git 저장소를 백엔드로 사용하는 웹 편집 UI. 비개발자도 브라우저에서 Markdown을 수정하고 PR 흐름으로 올릴 수 있게 해주는 계층.
*   **GitHub / Forgejo / Gitea:** 문서 원본, 권한, 이력, PR 승인을 담당하는 Git 포지 계층.
    *   *이론 및 설계:* **엔터프라이즈 시스템 및 아키텍처** 참고.

