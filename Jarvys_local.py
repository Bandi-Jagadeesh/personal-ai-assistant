import ollama

print("==============================")
print("       JARVYS ONLINE")
print("==============================")

while True:

    user = input("\nYOU: ")

    if user.lower() in ["exit", "quit", "bye"]:
        print("JARVYS: Goodbye!")
        break

    try:
        response = ollama.chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are JARVYS, a personal AI assistant. "
                        "Be helpful, intelligent and concise."
                    )
                },
                {
                    "role": "user",
                    "content": user
                }
            ]
        )

        answer = response["message"]["content"]

        print("\nJARVYS:", answer)

    except Exception as e:
        print("\nJARVYS ERROR:", e)
