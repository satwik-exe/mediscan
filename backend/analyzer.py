"""
analyzer.py
-----------
Handles LLM-powered analysis of extracted lab report text.
Uses Google Gemini (free tier) via the google-generativeai SDK.
"""

import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def analyze_report(extracted_text: str) -> dict:
    """
    Analyze extracted lab report text using the Google Gemini API.

    Args:
        extracted_text: Raw text extracted from the PDF lab report.

    Returns:
        A dict with keys: summary (str), values (list of dicts).

    Raises:
        EnvironmentError: If GEMINI_API_KEY is not set.
        ValueError: If the LLM returns unparseable output.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY is not set. "
            "Please add it to your .env file."
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""You are a medical lab report analyzer. You will be given text extracted from a medical lab report PDF.

Your task:
1. Identify all lab test values present in the text.
2. For each value, extract:
   - name: the test name (e.g., "Hemoglobin", "WBC", "Glucose")
   - value: the numeric result (as a number if possible, otherwise a string)
   - unit: the unit of measurement (e.g., "g/dL", "mg/dL")
   - status: classify as one of: "normal", "high", "low", or "critical"
     * "critical" means dangerously abnormal (e.g., extremely high potassium, very low hemoglobin)
     * "high" means above normal range
     * "low" means below normal range
     * "normal" means within reference range
   - explanation: For non-normal values, write 2-3 sentences in plain English that a non-medical person can understand. Explain what the test measures, what it means that the value is high/low, and what it could indicate. For normal values, set this to null.
3. Write an overall summary in 3-4 sentences covering the general state of the patient's health based on these results.

IMPORTANT: You MUST respond ONLY with a valid JSON object. No markdown, no backticks, no explanation text before or after the JSON.

The JSON must match this exact schema:
{{
  "summary": "string",
  "values": [
    {{
      "name": "string",
      "value": "number or string",
      "unit": "string",
      "status": "normal or high or low or critical",
      "explanation": "string or null"
    }}
  ]
}}

Lab report text:
---
{extracted_text}
---

Respond with ONLY the JSON object:"""

    response = model.generate_content(prompt)
    raw_response = response.text.strip()
    return _parse_llm_response(raw_response)


def _parse_llm_response(raw_response: str) -> dict:
    """
    Parse and validate the JSON response from the LLM.

    Args:
        raw_response: The raw string returned by the LLM.

    Returns:
        A validated dict matching the analysis schema.

    Raises:
        ValueError: If valid JSON cannot be extracted from the response.
    """
    # Try direct parse first
    try:
        data = json.loads(raw_response)
        return _validate_response_schema(data)
    except json.JSONDecodeError:
        pass

    # Strip markdown fences if present
    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_response, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            return _validate_response_schema(data)
        except json.JSONDecodeError:
            pass

    # Find first { ... } block
    brace_match = re.search(r"\{.*\}", raw_response, re.DOTALL)
    if brace_match:
        try:
            data = json.loads(brace_match.group(0))
            return _validate_response_schema(data)
        except json.JSONDecodeError:
            pass

    raise ValueError("The AI returned an unreadable response. Please try again.")


def _validate_response_schema(data: dict) -> dict:
    """
    Validate that the parsed dict contains required fields,
    filling in safe defaults where needed.

    Args:
        data: Parsed dictionary from the LLM response.

    Returns:
        The validated dict.

    Raises:
        ValueError: If the top-level structure is wrong.
    """
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object at the top level.")

    if "summary" not in data:
        data["summary"] = "Analysis complete. Please review the values below."

    if "values" not in data or not isinstance(data["values"], list):
        data["values"] = []

    valid_statuses = {"normal", "high", "low", "critical"}
    for item in data["values"]:
        if "status" not in item or item["status"] not in valid_statuses:
            item["status"] = "normal"
        if "explanation" not in item:
            item["explanation"] = None
        if "unit" not in item:
            item["unit"] = ""

    return data