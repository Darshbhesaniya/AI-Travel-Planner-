export default function DestinationCard({ option: o }) {
  return (
    <>
      <div className="flex flex-wrap items-center gap-2">
        <h3 className="text-lg font-semibold">📍 {o.name}</h3>
        <span className="rounded-full bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-700">
          {o.airport_code}
        </span>
      </div>
      <p className="text-xs text-slate-500">{o.airport_name}</p>
      <p className="mt-2 text-slate-700">{o.reason}</p>
    </>
  );
}