import requests

r1 = requests.get("http://localhost:8000/run-graph")
data = r1.json()
thread_id = data["thread_id"]
first_option_name = data["destination_options"][0]["name"]

print("thread_id:", thread_id)
print("selecting:", first_option_name)

r2 = requests.post(
    "http://localhost:8000/select-destination",
    params={"thread_id": thread_id, "destination": first_option_name}
)

print("status:", r2.status_code)
print(r2.json())