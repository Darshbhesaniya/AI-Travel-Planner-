export default function Loader({ text = "Loading..." }) {
  return (
    <div className="flex flex-col items-center gap-4 rounded-xl bg-white py-16 shadow-sm">
      <div className="h-10 w-10 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600" />
      <p className="text-slate-600">{text}</p>
      <p className="text-xs text-slate-400">This can take 5-15 seconds</p>
    </div>
  );
}