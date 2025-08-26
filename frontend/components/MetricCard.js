export default function MetricCard({ title, value, children }) {
  return (
    <div style={{ border: '1px solid #ccc', padding: '1rem', borderRadius: '4px', marginBottom: '1rem' }}>
      <h3>{title}</h3>
      {value !== undefined && <p>{value}</p>}
      {children}
    </div>
  );
}
