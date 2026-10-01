export default function InterestChips({ options, selected, onChange, max }) {
  function toggle(value) {
     console.log("clicked:", value, "already selected:", selected.includes(value));
    if (selected.includes(value)) {
      onChange(selected.filter((v) => v !== value));
    } else if (selected.length < max) {
      onChange([...selected, value]);
    }
  }

  const limitReached = selected.length >= max;

  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <span className="text-sm font-medium text-slate-700">Interests (pick 1 to {max})</span>
        <span className="text-xs text-slate-500">
          {selected.length}/{max} selected
        </span>
      </div>

      <div className="flex flex-wrap gap-2">
        {options.map((o) => {
          const active = selected.includes(o.value);
          const disabled = !active && limitReached;
          return (
            <button
              type="button"
              key={o.value}
              onClick={() => toggle(o.value)}
              disabled={disabled}
              className={`rounded-full border px-4 py-2 text-sm transition ${
                active
                  ? "border-blue-600 bg-blue-600 text-white"
                  : "border-slate-300 bg-white hover:border-blue-400"
              } ${disabled ? "cursor-not-allowed opacity-40" : ""}`}
            >
              {o.emoji} {o.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}