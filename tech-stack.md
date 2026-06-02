# 🛠️ 사내 표준 기술 스택 (Tech Stack)

우리 조직에서 사용하고 연구하는 핵심 기술 및 라이브러리 목록과 가이드라인입니다.

---

## 💻 백엔드 & 인프라 (Backend)

*   **FastAPI:** 가볍고 빠른 비동기 Python 웹 프레임워크. 사내 AI 에이전트 서비스 개발의 메인 뼈대로 채택.
*   **Docker & Docker Compose:** 모든 로컬 개발 환경 및 사내 호스팅 서비스(Gitea, Jenkins 등)의 표준 컨테이너화 도구.
*   **Git (GitHub):** 형상 관리 및 **[[README]]** 지식 공동 저장소의 핵심 백엔드.

---

## 🗄️ 데이터베이스 & 벡터 검색 (Databases)

*   **PostgreSQL:** 강력한 표준 관계형 DB.
    *   **pgvector:** PostgreSQL 상에서 AI 텍스트 임베딩을 저장하고 유사도 검색(Vector Search)을 수행하는 확장 프로그램.
*   **Elasticsearch / OpenSearch:** 파편화된 다량의 비정형 문서 및 로그에서 형태소 분석 기반의 키워드 검색을 고속으로 수행하기 위한 기본 검색엔진.

---

## 🤖 인공지능 & LLM (AI & Agents)

*   **Claude API (Anthropic):** 고도의 비즈니스 로직 분석 및 코드 생성을 위한 사내 공식 LLM 파트너.
*   **LangChain / LlamaIndex:** AI 에이전트 워크플로우를 빌드하기 위한 오케스트레이션 프레임워크.
