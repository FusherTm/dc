import MetricCard from '@/components/MetricCard';
import { getFinancialSummary, getOperationalSummary } from '@/lib/api';

export default async function Page() {
  const [finance, operations] = await Promise.all([
    getFinancialSummary(),
    getOperationalSummary(),
  ]);

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Dashboard</h1>
      <section>
        <h2>Finansal Özet</h2>
        <MetricCard title="Kasa Bakiyesi" value={finance.cashBalance} />
        <MetricCard title="Son 5 İşlem">
          <ul>
            {finance.lastTransactions?.map(tx => (
              <li key={tx.id}>{tx.description}: {tx.amount}</li>
            ))}
          </ul>
        </MetricCard>
      </section>
      <section>
        <h2>Operasyonel Özet</h2>
        <MetricCard title="Devam Eden İş Sayısı" value={operations.inProgressJobs} />
        <MetricCard title="Son Tamamlanan Sipariş" value={operations.lastCompletedOrder} />
      </section>
    </main>
  );
}
