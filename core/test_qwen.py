import os
from dashscope import Generation
import dashscope

# === SET UP API KEY ===
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

if not DASHSCOPE_API_KEY:
    raise ValueError("Set DASHSCOPE_API_KEY in environment variables")

# === TEST PROMPT ===
prompt = "Say 'Hello World' and confirm this is a test."

try:
    # === MAKE API CALL ===
    response = Generation.call(
        api_key=DASHSCOPE_API_KEY,  # ✅ Explicit key passing
        model="qwen-plus",          # Try qwen-turbo if this fails
        prompt=prompt
    )
    
    # === SHOW RESPONSE ===
    print("✅ Success!")
    print("Response:", response.output.text)

except Exception as e:
    print("❌ API Call Failed:")
    print(str(e))