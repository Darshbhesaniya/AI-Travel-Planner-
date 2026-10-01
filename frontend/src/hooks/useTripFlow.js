import { useState } from "react";
import { startTrip, submitSelection } from "../api/client";
import { STEP_ORDER, STEPS } from "../constants/steps";


export function useTripFlow(){
    const [phase, setPhase] = useState("form");
    const [stepIndex, setStepIndex] = useState(0);
    const [threadId, setThreadId] = useState(null);
    const [pending, setPending] = useState(null); 
    const [plan, setPlan] = useState(null);
    const [error, setError] = useState("");
    const [loadingText, setLoadingText] = useState("");


    function fail(message){
        setError(message);
        setPhase("error");
    }

    function handleResult(data){
        const interrupt = data.__interrupt__?.[0]?.value;

        if(interrupt && STEPS[interrupt.type]){
            if(!interrupt.options?.length){
                return fail(data.errors?.join(", ") || "No Questions Found. Try different details.")
            }
            setPending(interrupt);
            setStepIndex(STEP_ORDER.indexOf(interrupt.type) + 1);
            return setPhase("select")
        }

    if (data.final_plan && Object.keys(data.final_plan).length) {
      setPlan(data.final_plan);
      setStepIndex(4);
      return setPhase("final");
    }

    fail(data.errors?.join(", ") || "Something went wrong.");
    }

    async function start(payload) {
    setLoadingText("Finding destinations for you...");
    setPhase("loading");
    try {
      const data = await startTrip(payload);
      setThreadId(data.thread_id);
      handleResult(data);
    } catch (e) {
      fail(e.message);
    }
  }


  async function choose(option) {
    const step = STEPS[pending.type];
    setLoadingText(step.loadingText);
    setPhase("loading");
    try {
      const data = await submitSelection(step.url, {
        thread_id: threadId,
        [step.param]: option[step.idKey],
      });
      handleResult(data);
    } catch (e) {
      fail(e.message);
    }
  }

  function reset() {
    setPhase("form");
    setStepIndex(0);
    setThreadId(null);
    setPending(null);
    setPlan(null);
    setError("");
  }

  return {phase, stepIndex, pending, plan, error, loadingText, start, choose, reset};

}