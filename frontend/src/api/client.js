const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

async function request(path, options) {
    const res = await fetch(`${BASE}${path}`, options)

    if (!res.ok){
        throw new Error(`Server error (${res.status}). Please try again.`);
    }
    return res.json();
}

export const getOrigins = () => request("/origins");
export const getStates = () => request("/states");
export const getInterest = () => request("/interests")

export const startTrip = (payload) => 
    request("/start-trip", {
        method: "POST",
        headers: { "content-Type": "application/json"},
        body: JSON.stringify(payload)
    })

export const submitSelection = (url,params) => 
    request(`${url}?${new URLSearchParams(params)}`, {method: "POST"});

