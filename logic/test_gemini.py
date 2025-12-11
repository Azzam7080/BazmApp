import google.generativeai as genai

API_KEY = "AIzaSyDGZd33PYWKzZZ-EHGposPU766IBXGS-bM"

print("🔧 Testing Gemini API...")

try:
    # Configure
    genai.configure(api_key=API_KEY)
    print("✅ API configured")
    
    # List available models
    print("\n📋 Available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
    
    # Try to generate content
    print("\n🤖 Testing generation...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print(f"✅ Response: {response.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")