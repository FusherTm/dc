const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export async function getFinancialSummary() {
  const res = await fetch(`${API_BASE}/finance/summary`);
  if (!res.ok) {
    throw new Error('Failed to fetch financial summary');
  }
  return res.json();
}

export async function getOperationalSummary() {
  const res = await fetch(`${API_BASE}/operations/summary`);
  if (!res.ok) {
    throw new Error('Failed to fetch operational summary');
  }
  return res.json();
}
