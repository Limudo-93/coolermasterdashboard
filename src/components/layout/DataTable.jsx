export function DataTable({ columns, rows }) {
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col} style={{ textAlign: 'left', fontSize: 13, color: 'var(--muted)', borderBottom: '1px solid var(--border)', padding: '10px 8px' }}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={index}>
              {row.map((cell, cIdx) => (
                <td key={`${index}-${cIdx}`} style={{ borderBottom: '1px solid var(--border)', padding: '10px 8px' }}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
