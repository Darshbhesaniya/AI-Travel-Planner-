export const STEPS = {
    destination_selection: {
        url: "/select-destination",
        param: "destination",
        idKey: "name",
        title: "Choose your destination",
        subtitle: "Top Picks based on your interests and budget",
        loadingText: "searching the best flight for you...",
    },
    flight_selection: {
        url: "/select-flight",
        param: "flight_id",
        idKey: "flight_id",
        title: "Choose your flight",
        subtitle: "Real flight options, ranked for you",
        loadingText: "Finding hotels at your destination...",
    },
    hotel_selection: {
        url: "/select-hotel",
        param: "hotel_id",
        idKey: "hotel_id",
        title: "Choose your hotel",
        subtitle: "Stays that fit your budget",
        loadingText: "Putting your final plan together...", 
    },
};

export const STEP_ORDER = Object.keys(STEPS);
export const STEP_LABELS = ["Details", "Destination", "Flight", "Hotel", "Your Plan"];