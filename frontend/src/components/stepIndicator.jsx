import { STEP_LABELS } from "../constants/steps";

export default function StepIndicator({ current }) {
  return (
    <ol className="mb-8 flex items-center justify-between">
      {STEP_LABELS.map((label, i) => {
        const done = i < current;
        const active = i === current;
        return (
          <li key={label} className="flex flex-1 flex-col items-center gap-1">
            <span
              className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-semibold ${
                done
                  ? "bg-green-500 text-white"
                  : active
                  ? "bg-blue-600 text-white"
                  : "bg-slate-200 text-slate-500"
              }`}
            >
              {done ? "✓" : i + 1}
            </span>
            <span className={`text-xs ${active ? "font-semibold text-blue-700" : "text-slate-500"}`}>
              {label}
            </span>
          </li>
        );
      })}
    </ol>
  );
}