import { formatDuration, formatINR } from "../../utils/format";

export default function FlightCard({ option: o }) {
  return (
    <>
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold">✈️ {o.airline}</h3>
          <p className="text-sm text-slate-500">
            {o.departure_airport} → {o.arrival_airport}
          </p>
        </div>
        <div className="text-right">
          <p className="text-xl font-bold text-blue-700">{formatINR(o.price)}</p>
          <p className="text-xs text-slate-500">per person (round trip)</p>
        </div>
      </div>

      <div className="mt-3 flex flex-wrap gap-2 text-sm">
        <span className="rounded-full bg-slate-100 px-3 py-1">
          {o.departure_time} → {o.arrival_time}
        </span>
        <span className="rounded-full bg-slate-100 px-3 py-1">{formatDuration(o.total_duration_minutes)}</span>
        <span
          className={`rounded-full px-3 py-1 ${
            o.stops === 0 ? "bg-green-100 text-green-700" : "bg-amber-100 text-amber-700"
          }`}
        >
          {o.stops === 0 ? "Non-stop" : `${o.stops} stop`}
        </span>
      </div>

      <p className="mt-3 text-slate-700">{o.reason}</p>
    </>
  );
}