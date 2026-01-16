from pathlib import Path
from openai import AzureOpenAI
import sys
sys.stdout.reconfigure(encoding="utf-8")


# ---------- HELPER FUNCTION ----------
def call_openai(client, deployment, prompt):

    response = client.responses.create(
    model=deployment,
    input=[
        {"role": "system", "content": "You are an EPS feature architect."},
        {"role": "user", "content": prompt}
    ]
)
    return response.output_text

# ---------- CONFIG ----------
BASE_DIR = Path(__file__).parent

# Load files
tal_code = (BASE_DIR / "tal" / "SOURCE LUHNCHK 1.tal").read_text(encoding="utf-8")
analysis_prompt = (BASE_DIR / "prompts" / "tal_analysis.txt").read_text(encoding="utf-8")
rule_prompt = (BASE_DIR / "prompts" / "rule_extraction.txt").read_text(encoding="utf-8")
feature_prompt = (BASE_DIR / "prompts" / "eps_feature_prompt.txt").read_text(encoding="utf-8")


AZURE_ENDPOINT = "https://gpt5-finance-dev.openai.azure.com/"
DEPLOYMENT_NAME = "gpt-5.1-codex-mini"
API_VERSION = "2025-03-01-preview"

# ---------- CREATE OPENAI CLIENT ----------
client = AzureOpenAI(
    api_key=AZURE_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=API_VERSION
)

# STEP 1: TAL Analysis
analysis_input = analysis_prompt.replace("{{TAL_CODE}}", tal_code)
analysis_output = call_openai(client, "gpt-5.1-codex-mini", analysis_input)

# STEP 2: Rule Extraction
rule_input = rule_prompt.replace("{{ANALYSIS}}", analysis_output)
rule_output = call_openai(client, "gpt-5.1-codex-mini", rule_input)

# STEP 3: EPS Feature Definition
feature_input = feature_prompt.replace("{{TAL_CODE}}", rule_output)
feature_output = call_openai(client, "gpt-5.1-codex-mini", feature_input)

# Save outputs
(BASE_DIR / "output" / "analysis.md").write_text(analysis_output, encoding="utf-8")
(BASE_DIR / "output" / "rules.md").write_text(rule_output, encoding="utf-8")
(BASE_DIR / "output" / "feature.md").write_text(feature_output, encoding="utf-8")

# Load feature output
feature_text = (BASE_DIR / "output" / "feature.md").read_text(encoding="utf-8")


# Plugin contract
plugin_contract_prompt = (BASE_DIR / "prompts" / "eps_plugin_contract.txt").read_text(encoding="utf-8")
plugin_contract_input = plugin_contract_prompt.replace("{{FEATURE}}", feature_text)
plugin_yaml = call_openai(client, "gpt-5.1-codex-mini", plugin_contract_input)
(BASE_DIR / "output" / "plugin.yaml").write_text(plugin_yaml, encoding="utf-8")

# Plugin logic
plugin_logic_prompt = (BASE_DIR / "prompts" / "eps_plugin_logic.txt").read_text(encoding="utf-8")
plugin_logic_input = plugin_logic_prompt.replace("{{FEATURE}}", feature_text)
plugin_java = call_openai(client, "gpt-5.1-codex-mini", plugin_logic_input)
(BASE_DIR / "output" / "ConvertedFromTAL.java").write_text(plugin_java, encoding="utf-8")

# Response mapping
response_prompt = (BASE_DIR / "prompts" / "eps_response_mapping.txt").read_text(encoding="utf-8")
response_input = response_prompt.replace("{{FEATURE}}", feature_text)
response_map = call_openai(client, "gpt-5.1-codex-mini", response_input)
(BASE_DIR / "output" / "response-mapping.md").write_text(response_map, encoding="utf-8")
