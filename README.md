AI Security Scanner

A Python-based security scanner that uses Google's Gemini API to analyze source code for common security vulnerabilities. The scanner identifies potential issues, assigns severity levels, and displays results with color-coded output to help prioritize fixes.

Features
AI-powered vulnerability detection using Gemini 2.5 Flash
Severity ratings:
Critical
High
Medium
Low
Color-coded terminal output
Automatic sorting by severity
Simple command-line interface
Works on any source code file that can be read as text
Project Structure
.
├── scanner.py
├── vulnerable.py
├── .env
└── README.md
scanner.py

The main application. Reads a source code file, sends it to Gemini for analysis, sorts findings by severity, and displays color-coded results.

vulnerable.py

A sample file containing intentionally vulnerable code for testing the scanner.

.env

Stores your Gemini API key.

Requirements
Python 3.10+
Google Gemini API key
Setup
1. Clone the repository
git clone <your-repository-url>
cd <repository-name>
2. Create a virtual environment

Mac/Linux:

python3 -m venv venv

Windows:

python -m venv venv
3. Activate the virtual environment

Mac/Linux:

source venv/bin/activate

Windows:

venv\Scripts\activate
4. Install dependencies
pip install google-genai python-dotenv colorama

Or create a requirements.txt file and run:

pip install -r requirements.txt
5. Configure your API key

Create a .env file in the project root:

GOOGLE_API_KEY=your_api_key_here
Usage

Run the scanner and provide the path to the file you want analyzed:

python scanner.py vulnerable.py

Example:

python scanner.py app.py
Example Output
Severity: Critical
Vulnerability: SQL Injection
Why: User input is directly concatenated into SQL queries.
Impact: Attackers can execute arbitrary SQL commands.
Fix: Use parameterized queries.

--------------------------------------------------

Severity: High
Vulnerability: Command Injection
Why: User input is passed directly to system commands.
Impact: Attackers may execute arbitrary commands.
Fix: Validate input and avoid shell execution.
Sample Vulnerabilities Included

The included vulnerable.py file contains examples of:

SQL Injection
Weak password hashing (MD5)
Command Injection
Hardcoded credentials
Exposed API secrets
How It Works
Reads the target source code file.
Sends the code to Gemini 2.5 Flash.
Requests a structured security review.
Sorts findings by severity.
Displays color-coded results in the terminal.