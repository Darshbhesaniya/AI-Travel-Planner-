export const toBackendDate = (d) => d.split("-").reverse().join("-");

export const formatINR = (n) => 
    new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0,
    }).format(n ?? 0);

export const formatDuration = (min) => 
    min ? `${Math.floor(min / 60)}h ${min % 60}m`: "-";

