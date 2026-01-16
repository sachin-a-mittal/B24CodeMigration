print("Program started")
from openai import AzureOpenAI
from pathlib import Path

# ---------- CONFIG ----------
client = AzureOpenAI(
    api_key="9wKNlRndrixJfMJUZe5TdTecdxVIwrVDruTmddgw6iQD2G9F88vyJQQJ99BLACfhMk5XJ3w3AAABACOGVGPD",
    azure_endpoint="https://gpt5-finance-dev.openai.azure.com/",
    api_version="2025-03-01-preview"   # use your actual version
)

# ---------- UTILS ----------
def load_file(file_path):
    return Path(file_path).read_text(encoding="utf-8")

# ---------- LOAD INPUTS ----------
tal_code = load_file("tal/SOURCE LUHNCHK 1.tal")
#prompt_template = load_file("prompts/eps_feature_prompt.txt")
prompt_path = load_file("prompts/eps_feature_prompt.txt")
final_prompt = prompt_path.replace("{{TAL_CODE}}", tal_code)

response = client.responses.create(
    model="gpt-5.1-codex-mini",
    input=[
        {"role": "system", "content": "You are an EPS feature architect."},
        {"role": "user", "content": final_prompt}
    ]
)

# ---------- OUTPUT ----------
print("===== EPS FEATURE DEFINITION =====")
print(response.output_text)
