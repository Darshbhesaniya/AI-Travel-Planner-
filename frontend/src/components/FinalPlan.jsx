import { formatDuration, formatINR } from "../utils/format";

function Section({ title, children }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <h3 className="mb-3 text-lg font-semibold">{title}</h3>
      {children}
    </div>
  );
}

function Row({ label, value, bold }) {
  return (
    <div className="flex justify-between py-1 text-sm">
      <span className="text-slate-500">{label}</span>
      <span className={bold ? "font-bold text-slate-900" : "font-medium"}>{value}</span>
    </div>
  );
}

export default function FinalPlan({ plan, onReset }) {
  const { trip_info: t, flight: f, hotel: h, cost_breakdown: c } = plan;
  const usedPercent = Math.min(100, Math.round((c.grand_total / c.budget) * 100));

  return (
    <div className="space-y-4">
      <div className="rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 p-6 text-white">
        <h2 className="text-3xl font-bold">{plan.trip_title}</h2>
        <p className="mt-2 text-blue-50">{plan.overview}</p>
      </div>

      <Section title="🧭 Trip details">
        <Row label="From" value={t.origin} />
        <Row label="To" value={t.destination} />
        <Row label="Dates" value={`${t.start_date} → ${t.end_date} (${t.duration_days} days)`} />
        <Row label="Travelers" value={t.travelers} />
      </Section>

      <Section title="✈️ Flight">
        <Row label="Airline" value={f.airline} />
        <Row label="Departure" value={f.departure_time} />
        <Row label="Arrival" value={f.arrival_time} />
        <Row label="Duration" value={formatDuration(f.duration_minutes)} />
        <Row label="Stops" value={f.stops === 0 ? "Non-stop" : f.stops} />
        <Row label="Price" value={`${formatINR(f.price_per_person)} × ${t.travelers} = ${formatINR(f.total_price)}`} />
        <p className="mt-2 text-sm italic text-slate-600">{f.highlight}</p>
      </Section>

      <Section title="🏨 Hotel">
        <Row label="Name" value={h.name} />
        <Row label="Class / Rating" value={`${h.hotel_class}★ · ${h.rating}`} />
        <Row label="Per night" value={formatINR(h.price_per_night)} />
        <Row label="Total stay" value={formatINR(h.total_price)} />
        <div className="mt-2 flex flex-wrap gap-2">
          {h.amenities?.map((a) => (
            <span key={a} className="rounded-full bg-slate-100 px-3 py-1 text-xs">{a}</span>
          ))}
        </div>
        <p className="mt-2 text-sm italic text-slate-600">{h.highlight}</p>
      </Section>

      <Section title="💰 Cost breakdown">
        <Row label="Flights" value={formatINR(c.flight_total)} />
        <Row label="Hotel" value={formatINR(c.hotel_total)} />
        <Row label="Total" value={formatINR(c.grand_total)} bold />
        <Row label="Budget" value={formatINR(c.budget)} />
        <div className="mt-3 h-3 overflow-hidden rounded-full bg-slate-200">
          <div
            className={`h-full ${c.within_budget ? "bg-green-500" : "bg-red-500"}`}
            style={{ width: `${usedPercent}%` }}
          />
        </div>
        <p className={`mt-2 text-sm ${c.within_budget ? "text-green-700" : "text-red-600"}`}>
          {c.within_budget
            ? `✅ Within budget. ${formatINR(c.remaining_budget)} left for food and activities.`
            : "⚠️ Over budget"}
        </p>
      </Section>

      <Section title="💡 Travel tips">
        <ul className="list-disc space-y-1 pl-5 text-slate-700">
          {plan.tips.map((tip) => (
            <li key={tip}>{tip}</li>
          ))}
        </ul>
      </Section>

      <button
        onClick={onReset}
        className="w-full rounded-lg border border-blue-600 py-3 font-semibold text-blue-600 hover:bg-blue-50"
      >
        Plan another trip
      </button>
    </div>
  );
}