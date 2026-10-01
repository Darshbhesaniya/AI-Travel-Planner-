import { STEPS } from "../constants/steps";
import DestinationCard from "./cards/DestinationCard";
import FlightCard from "./cards/FlightCard";
import HotelCard from "./cards/HotelCard";

const CARDS = {
  destination_selection: DestinationCard,
  flight_selection: FlightCard,
  hotel_selection: HotelCard,
};

export default function SelectionStep({ pending, onSelect }) {
  const step = STEPS[pending.type];
  const Card = CARDS[pending.type];

  return (
    <section>
      <h2 className="text-2xl font-bold">{step.title}</h2>
      <p className="mb-5 text-slate-500">{step.subtitle}</p>

      <div className="grid gap-4">
        {pending.options.map((option) => (
          <div
            key={option[step.idKey]}
            className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md"
          >
            <Card option={option} />
            <button
              onClick={() => onSelect(option)}
              className="mt-4 rounded-lg bg-blue-600 px-5 py-2 font-medium text-white hover:bg-blue-700"
            >
              Select
            </button>
          </div>
        ))}
      </div>
    </section>
  );
}