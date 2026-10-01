import { useEffect, useState } from "react";
import { getInterest, getOrigins, getStates } from "../api/client";

export function useMetadata(){
    const [data, setData] = useState({origins: [], states:[], interests: [], maxInterests: 5});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const loadData = async() =>{
            try {
                const [origins, states, interests] = await Promise.all([
                    getOrigins(),
                    getStates(),
                    getInterest()
                ]);

                setData({
                    origins,
                    states,
                    interests: interests.items,
                    maxInterests: interests.max
                });
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false)
            }
        };
        loadData();
    }, []);

    return {...data,loading,error};
}