import { getClients } from '@/lib/clients';
import { ClientsTable } from '@/components/clients-table';
import { auth } from '@/lib/auth';
import Link from 'next/link';

export default async function Home() {
  const session = await auth();
  const clients = getClients();

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <header className="mb-10 flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">📚 Knowledgebase</h1>
          <p className="mt-2 text-sm text-gray-500">
            1인 회사를 위한 통합 지식 자산 — 문서·데이터·그래프
          </p>
        </div>
        <nav className="flex items-center gap-3 text-sm">
          <Link href="/docs" className="text-gray-600 hover:text-gray-900">
            📝 문서
          </Link>
          <Link href="/graph" className="text-gray-600 hover:text-gray-900">
            🕸️ 그래프
          </Link>
          <span className="h-4 w-px bg-gray-300" />
          {session?.user ? (
            <span className="text-gray-500">@{session.user.name}</span>
          ) : (
            <Link
              href="/api/auth/signin"
              className="rounded-md bg-gray-900 px-3 py-1.5 text-white hover:bg-gray-800"
            >
              GitHub 로그인
            </Link>
          )}
        </nav>
      </header>

      <section>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">
            📊 클라이언트
          </h2>
          <a
            href="https://github.com/agnusdei1207/knowledge-base/blob/main/data/clients.yaml"
            target="_blank"
            rel="noopener"
            className="text-xs text-gray-500 hover:underline"
          >
            data/clients.yaml 편집 →
          </a>
        </div>
        <ClientsTable clients={clients} />
      </section>

      <section className="mt-10">
        <h2 className="mb-4 text-lg font-semibold text-gray-900">
          🔧 다음에 만들 것
        </h2>
        <div className="grid gap-3 sm:grid-cols-3">
          {[
            { icon: '🔍', title: '의미 검색', desc: 'AI가 KB를 보고 인용하며 답' },
            { icon: '✏️', title: '웹 에디터', desc: '브라우저에서 markdown 직접 수정' },
            { icon: '🕸️', title: '그래프 뷰', desc: '문서/클라이언트 관계 시각화' },
            { icon: '🤖', title: 'MCP 서버', desc: 'AI 에이전트가 KB 호출' },
            { icon: '⏰', title: 'Cron Jobs', desc: '주간 보고 자동 생성' },
            { icon: '📈', title: '메트릭 대시보드', desc: 'CSV → 차트' },
          ].map((item) => (
            <div
              key={item.title}
              className="rounded-lg border border-gray-200 bg-white p-4 text-sm"
            >
              <div className="mb-1 text-2xl">{item.icon}</div>
              <div className="font-medium text-gray-900">{item.title}</div>
              <div className="text-xs text-gray-500">{item.desc}</div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
