# Knowledge Base

Quartz 기반 개인 지식 베이스입니다. 사이트 구조와 디자인은 `../codex-skills`의 Quartz 구성을 채용했고, 콘텐츠는 이 저장소의 `content/` 문서를 사용합니다.

## Commands

```bash
npm ci
npm run build
npm run dev
```

Local preview:

```text
http://localhost:8080/knowledge-base
```

## Structure

- `content/`: canonical knowledge documents and study notes
- `quartz/`: Quartz engine and design layer
- `quartz.config.default.yaml`: site configuration and theme
- `.github/workflows/`: Quartz CI and GitHub Pages deployment

Zola/Pagefind files were intentionally removed during the Quartz migration.
