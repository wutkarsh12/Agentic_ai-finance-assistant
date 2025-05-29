import requests
import pyttsx3

# Step 1: Get orchestrated data
orchestrated_data = requests.get("http://localhost:8003/morning_brief").json()

# Step 2: Send to Gemini-based language agent
response = requests.post("http://localhost:8004/generate_summary", json=orchestrated_data)

print("Status Code:", response.status_code)
print("Raw Response:", response.text)

try:
    result = response.json()
    summary = result.get("summary")

    if summary:
        print("\n🧠 Summary:\n", summary)

        # Step 3: Speak it
        print("\n🔊 Speaking summary...")
        engine = pyttsx3.init()
        engine.say(summary)
        engine.runAndWait()
    else:
        print("No summary received.")
except Exception as e:
    print("Failed to parse response:", str(e))
