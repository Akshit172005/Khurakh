import google.generativeai as genai

genai.configure(api_key="AQ.-")

print("Available Models:\n")

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)