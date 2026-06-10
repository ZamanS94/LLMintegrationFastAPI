import ollama

client = ollama.Client()

model = "llama2"
prompt = "In short what is python"

response = client.generate(model=model,prompt=prompt)

print("Response")
print(response.response)