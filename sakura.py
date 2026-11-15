import os
import requests
import json

API_KEY = os.environ.get("GEMINI_API_KEY")

print("🌸 SakuraAI शुरू हो गया!")
print("बात बंद करने के लिए exit लिखो।")

while True:
    question = input("\nतुम: ").strip()

    if question.lower() == "exit":
        print("SakuraAI: फिर मिलेंगे ❤️")
        break

    if not question:
        continue

    if not API_KEY:
        print("Gemini API Key सेट नहीं है।")
        continue

    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent"

        data = {
            "contents": [{
                "parts": [{"text": question}]
            }]
        }

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": API_KEY
            },
            data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
            timeout=60
        )

        response.encoding = "utf-8"
        result = response.json()
        response.raise_for_status()

        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        print("\nSakuraAI:", answer)

    except Exception:
        import traceback
        traceback.print_exc()
