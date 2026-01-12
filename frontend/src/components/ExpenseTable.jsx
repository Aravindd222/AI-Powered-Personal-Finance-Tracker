export default function ExpenseTable({ expenses }) {
  return (
    <div className="bg-zinc-900 rounded-xl overflow-hidden">
      <table className="w-full text-sm text-white">
        <thead className="bg-zinc-800">
          <tr>
            <th className="p-3 text-left">Date</th>
            <th className="p-3 text-left">Category</th>
            <th className="p-3 text-left">Amount</th>
            <th className="p-3 text-left">Source</th>
          </tr>
        </thead>
        <tbody>
          {expenses.map((e, i) => (
            <tr key={i} className="border-b border-zinc-800">
              <td className="p-3">{e.date}</td>
              <td className="p-3">{e.category}</td>
              <td className="p-3">₹ {e.amount}</td>
              <td className="p-3">{e.source}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
