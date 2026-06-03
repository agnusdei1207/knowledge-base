import type { Client } from '@/lib/clients';

const statusStyle: Record<Client['status'], string> = {
  active: 'bg-green-100 text-green-800',
  pending: 'bg-yellow-100 text-yellow-800',
  lost: 'bg-gray-100 text-gray-600',
  churned: 'bg-red-100 text-red-700',
};

const statusLabel: Record<Client['status'], string> = {
  active: '활성',
  pending: '대기',
  lost: '실패',
  churned: '이탈',
};

function formatMRR(n: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  }).format(n);
}

function formatDate(s: string): string {
  return new Date(s).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

export function ClientsTable({ clients }: { clients: Client[] }) {
  if (clients.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-8 text-center text-sm text-gray-500">
        아직 클라이언트가 없습니다.{' '}
        <code className="rounded bg-gray-100 px-1 py-0.5 text-xs">data/clients.yaml</code>에
        추가하면 여기에 표시됩니다.
      </div>
    );
  }

  const totalMRR = clients
    .filter((c) => c.status === 'active')
    .reduce((sum, c) => sum + c.mrr, 0);

  return (
    <div className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
      <div className="flex items-center justify-between border-b border-gray-200 bg-gray-50 px-4 py-3">
        <div className="text-sm text-gray-600">
          총 <span className="font-semibold text-gray-900">{clients.length}</span>개
        </div>
        <div className="text-sm text-gray-600">
          활성 MRR 합계:{' '}
          <span className="font-semibold text-green-700">{formatMRR(totalMRR)}</span>
        </div>
      </div>
      <table className="w-full text-left text-sm">
        <thead className="bg-gray-50 text-xs uppercase text-gray-500">
          <tr>
            <th className="px-4 py-3">이름</th>
            <th className="px-4 py-3">도메인</th>
            <th className="px-4 py-3">상태</th>
            <th className="px-4 py-3 text-right">MRR</th>
            <th className="px-4 py-3">담당자</th>
            <th className="px-4 py-3">시작일</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {clients.map((c) => (
            <tr key={c.id} className="hover:bg-gray-50">
              <td className="px-4 py-3 font-medium text-gray-900">
                <div>{c.name}</div>
                {c.notes && (
                  <div className="mt-0.5 text-xs text-gray-500">{c.notes}</div>
                )}
              </td>
              <td className="px-4 py-3 text-gray-600">{c.domain}</td>
              <td className="px-4 py-3">
                <span
                  className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${statusStyle[c.status]}`}
                >
                  {statusLabel[c.status]}
                </span>
              </td>
              <td className="px-4 py-3 text-right font-mono text-gray-900">
                {formatMRR(c.mrr)}
              </td>
              <td className="px-4 py-3 text-gray-600">
                <a href={`mailto:${c.contact}`} className="hover:underline">
                  {c.contact}
                </a>
              </td>
              <td className="px-4 py-3 text-gray-500">{formatDate(c.addedAt)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
