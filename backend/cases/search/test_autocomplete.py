import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/cases/search/suggestion/"

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcyMzM5MzczLCJpYXQiOjE3NzIzMzU3NzMsImp0aSI6Ijk4ZjFmNWE3ZDVkMjQ0MjFiYmQ4NzMxNGVhNmIyM2YwIiwidXNlcl9pZCI6IjIifQ.Nu3FSKLkEuNc8gV26ZwRtzEYrk6rnKCw71OZKnSDOb8"


def fetch_suggestions(query: str):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    try:
        response = requests.get(
            BASE_URL,
            params={"q": query},
            headers=headers
        )
        response.raise_for_status()

        data = response.json()

        # If paginated
        if isinstance(data, dict) and "results" in data:
            return data["results"]

        # If already list
        return data

    except Exception as e:
        print(f"Error: {e}")
        return []


def simulate_typing(input_text: str, delay=0.3):
    current = ""

    print("\nSimulating typing...\n")

    for char in input_text:
        current += char
        print(f"Input: {current}")

        words = current.split()
        if not words:
            continue
        last_word = words[-1]
        suggestions = fetch_suggestions(last_word)

        if suggestions:
            for s in suggestions:
                print(f"  → {s}")
        else:
            print("  (no suggestions)")

        print("-" * 40)
        time.sleep(delay)


if __name__ == "__main__":
    while True:
        user_input = input("\nEnter text to simulate typing (or 'exit'): ")

        if user_input.lower() == "exit":
            break

        simulate_typing(user_input)