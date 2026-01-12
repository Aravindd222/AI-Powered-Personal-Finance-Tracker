export default function StatCard({ title, value }) {
  return (
    <div className="bg-zinc-900 p-4 rounded-xl">
      <p className="text-sm text-zinc-400">{title}</p>
      <p className="text-xl font-semibold text-white">{value}</p>
    </div>
  );
}
