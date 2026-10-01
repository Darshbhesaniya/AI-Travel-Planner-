import { useState,useEffect } from "react";
import Field, { inputClass } from "./Field";
import InterestChips from "./InterestChips";
import { toBackendDate } from "../../utils/format";

const today = new Date().toISOString().split("T")[0];

export default function TripForm({ meta, onSubmit }) {
  const [form, setForm] = useState({
    origin_airport: "",
    allowed_state: "",
    budget: 100000,
    start_date: "",
    end_date: "",
    travelers: 2,
    interests: [],
  });
  const [error, setError] = useState("");

  useEffect(() => {
    console.log("TripForm MOUNTED");
    return () => console.log("TripForm UNMOUNTED");
    }, []);

  const set = (key, value) => setForm((f) => ({ ...f, [key]: value }));

  function handleSubmit(e) {
    e.preventDefault();

    if (form.end_date <= form.start_date) {
      return setError("End date must be after start date.");
    }
    setError("");

    onSubmit({
      origin_airport: form.origin_airport,
      allowed_state: form.allowed_state,
      budget: Number(form.budget),
      currency: "INR",
      travelers: Number(form.travelers),
      interests: form.interests,
      start_date: toBackendDate(form.start_date),
      end_date: toBackendDate(form.end_date),
    });
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5 rounded-xl bg-white p-6 shadow-sm">
      <div className="grid gap-5 md:grid-cols-2">
        <Field label="Origin city">
          <select
            required
            className={inputClass}
            value={form.origin_airport}
            onChange={(e) => set("origin_airport", e.target.value)}
          >
            <option value="">Select your city</option>
            {meta.origins.map((o) => (
              <option key={o.airport_code} value={o.airport_code}>
                {o.city} ({o.airport_code})
              </option>
            ))}
          </select>
        </Field>

        <Field label="Destination state" hint="Leave empty to search all over India">
          <select
            className={inputClass}
            value={form.allowed_state}
            onChange={(e) => set("allowed_state", e.target.value)}
          >
            <option value="">Anywhere in India</option>
            {meta.states.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </Field>

        <Field label="Start date">
          <input
            type="date"
            required
            min={today}
            className={inputClass}
            value={form.start_date}
            onChange={(e) => set("start_date", e.target.value)}
          />
        </Field>

        <Field label="End date">
          <input
            type="date"
            required
            min={form.start_date || today}
            className={inputClass}
            value={form.end_date}
            onChange={(e) => set("end_date", e.target.value)}
          />
        </Field>

        <Field label="Total budget (INR)" hint="Flights + hotel combined">
          <input
            type="number"
            required
            min="1000"
            className={inputClass}
            value={form.budget}
            onChange={(e) => set("budget", e.target.value)}
          />
        </Field>

        <Field label="Travelers">
          <input
            type="number"
            required
            min="1"
            max="9"
            className={inputClass}
            value={form.travelers}
            onChange={(e) => set("travelers", e.target.value)}
          />
        </Field>
      </div>

      <InterestChips
        options={meta.interests}
        max={meta.maxInterests}
        selected={form.interests}
        onChange={(v) => set("interests", v)}
      />

      {error && <p className="text-sm text-red-600">{error}</p>}

      <button
        type="submit"
        disabled={!form.interests.length || !form.origin_airport}
        className="w-full rounded-lg bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        Plan my trip
      </button>
    </form>
  );
}