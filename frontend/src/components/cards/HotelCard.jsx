import { formatINR } from "../../utils/format";

export default function HotelCard({ option: o }) {
  return (
    <>
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold">🏨 {o.name}</h3>
          <p className="text-sm text-slate-500">
            {"★".repeat(o.hotel_class || 0)} · Rating {o.overall_rating} ({o.reviews} reviews)
          </p>
        </div>
        <div className="text-right">
          <p className="text-xl font-bold text-blue-700">{formatINR(o.total_price)}</p>
          <p className="text-xs text-slate-500">{formatINR(o.price_per_night)} / night</p>
        </div>
      </div>

      <div className="mt-3 flex flex-wrap gap-2">
        {o.amenities?.map((a) => (
          <span key={a} className="rounded-full bg-slate-100 px-3 py-1 text-xs">
            {a}
          </span>
        ))}
      </div>

      <p className="mt-3 text-slate-700">{o.reason}</p>
      {o.link && (
        <a href={o.link} target="_blank" rel="noreferrer" className="mt-1 inline-block text-sm text-blue-600 hover:underline">
          Hotel website ↗
        </a>
      )}
    </>
  );
}