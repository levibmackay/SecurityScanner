import os
import sys
import re
from dotenv import load_dotenv
import google.genai as genai
from colorama import Fore, Style, init

init(autoreset=True)

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ GOOGLE_API_KEY not found in .env file")
    sys.exit(1)

client = genai.Client(api_key=api_key)

security_prompt = """
You are a cybersecurity expert.

DO NOT use markdown.
DO NOT use bullet points.
DO NOT use headings.
Output plain text only.

Separate each finding with:
---

Format exactly:

Severity: Low
Vulnerability: ...
Why: ...
Impact: ...
Fix: ...

Code:
{code}
"""

def sort_blocks(text):
    blocks = re.split(r"\n\s*---\s*\n", text.strip())
    blocks = [b.strip() for b in blocks if b.strip()]

    def score(block):
        b = block.lower()

        if "critical" in b:
            return 4
        if "high" in b:
            return 3
        if "medium" in b:
            return 2
        if "low" in b:
            return 1
        return 0

    return sorted(blocks, key=score, reverse=True)
def color_block(block):
    b = block.lower()

    if "severity: critical" in b or "critical" in b:
        return Fore.RED + block + Style.RESET_ALL
    elif "severity: high" in b or "high" in b:
        return Fore.LIGHTRED_EX + block + Style.RESET_ALL
    elif "severity: medium" in b or "medium" in b:
        return Fore.YELLOW + block + Style.RESET_ALL
    elif "severity: low" in b or "low" in b:
        return Fore.GREEN + block + Style.RESET_ALL

    return block

if len(sys.argv) < 2:
    print("Usage: python scanner.py <file_path>")
    sys.exit(1)

code_path = sys.argv[1]

with open(code_path, "r", encoding="utf-8") as f:
    code = f.read()

prompt = security_prompt.format(code=code)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    blocks = sort_blocks(response.text)

    for block in blocks:
        print(color_block(block))
        print("-" * 50)

except Exception as e:
    print(f"❌ Connection failed: {e}")