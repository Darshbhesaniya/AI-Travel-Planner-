import Header from "./components/Header";
import StepIndicator from "./components/StepIndicator";
import Loader from "./components/Loader";
import ErrorMessage from "./components/ErrorMessage";
import TripForm from "./components/form/TripForm";
import SelectionStep from "./components/SelectionStep";
import FinalPlan from "./components/FinalPlan";
import { useMetadata } from "./hooks/useMetadata";
import { useTripFlow } from "./hooks/useTripFlow";

export default function App() {
  const meta = useMetadata();
  const flow = useTripFlow();

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      <Header />
      <main className="mx-auto max-w-4xl px-4 py-8">
        <StepIndicator current={flow.stepIndex} />

        {flow.phase === "form" &&
          (meta.loading ? (
            <Loader text="Loading form..." />
          ) : meta.error ? (
            <ErrorMessage message={meta.error} />
          ) : (
            <TripForm meta={meta} onSubmit={flow.start} />
          ))}

        {flow.phase === "loading" && <Loader text={flow.loadingText} />}

        {flow.phase === "select" && (
          <SelectionStep pending={flow.pending} onSelect={flow.choose} />
        )}

        {flow.phase === "final" && <FinalPlan plan={flow.plan} onReset={flow.reset} />}

        {flow.phase === "error" && (
          <ErrorMessage message={flow.error} onRetry={flow.reset} />
        )}
      </main>
    </div>
  );
}