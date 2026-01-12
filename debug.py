import pandasai
print(f"PandasAI Version: {pandasai.__version__}")

print("\n--- Attempting Imports ---")
try:
    from pandasai.llm import OpenAI
    print("✅ SUCCESS: 'from pandasai.llm import OpenAI'")
except ImportError:
    print("❌ FAILED: 'from pandasai.llm import OpenAI'")

try:
    from pandasai.llm.openai import OpenAI
    print("✅ SUCCESS: 'from pandasai.llm.openai import OpenAI'")
except ImportError:
    print("❌ FAILED: 'from pandasai.llm.openai import OpenAI'")

print("\n--- Inspecting Module ---")
try:
    import pandasai.llm
    print("Available classes in pandasai.llm:", dir(pandasai.llm))
except ImportError:
    print("Could not inspect pandasai.llm")