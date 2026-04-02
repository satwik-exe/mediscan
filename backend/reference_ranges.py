"""
reference_ranges.py
-------------------
Defines standard reference ranges for common laboratory values.
Used to flag abnormal results in parsed lab reports.
"""

REFERENCE_RANGES = {
    "Hemoglobin": {
        "male": (13.5, 17.5),
        "female": (12.0, 15.5),
        "unit": "g/dL",
    },
    "WBC": {
        "normal": (4.5, 11.0),
        "unit": "x10^9/L",
    },
    "RBC": {
        "male": (4.5, 5.9),
        "female": (4.0, 5.2),
        "unit": "x10^12/L",
    },
    "Platelets": {
        "normal": (150, 400),
        "unit": "x10^9/L",
    },
    "Hematocrit": {
        "male": (41.0, 53.0),
        "female": (36.0, 46.0),
        "unit": "%",
    },
    "MCV": {
        "normal": (80.0, 100.0),
        "unit": "fL",
    },
    "MCH": {
        "normal": (27.0, 33.0),
        "unit": "pg",
    },
    "MCHC": {
        "normal": (32.0, 36.0),
        "unit": "g/dL",
    },
    "Neutrophils": {
        "normal": (1.8, 7.7),
        "unit": "x10^9/L",
    },
    "Lymphocytes": {
        "normal": (1.0, 4.8),
        "unit": "x10^9/L",
    },
    "Glucose (Fasting)": {
        "normal": (70.0, 99.0),
        "unit": "mg/dL",
    },
    "HbA1c": {
        "normal": (4.0, 5.6),
        "unit": "%",
    },
    "Creatinine": {
        "male": (0.74, 1.35),
        "female": (0.59, 1.04),
        "unit": "mg/dL",
    },
    "BUN": {
        "normal": (7.0, 20.0),
        "unit": "mg/dL",
    },
    "Sodium": {
        "normal": (136.0, 145.0),
        "unit": "mEq/L",
    },
    "Potassium": {
        "normal": (3.5, 5.1),
        "unit": "mEq/L",
    },
    "Chloride": {
        "normal": (98.0, 107.0),
        "unit": "mEq/L",
    },
    "Calcium": {
        "normal": (8.6, 10.3),
        "unit": "mg/dL",
    },
    "ALT": {
        "male": (7.0, 56.0),
        "female": (7.0, 45.0),
        "unit": "U/L",
    },
    "AST": {
        "normal": (10.0, 40.0),
        "unit": "U/L",
    },
    "Total Bilirubin": {
        "normal": (0.1, 1.2),
        "unit": "mg/dL",
    },
    "Total Cholesterol": {
        "normal": (0.0, 200.0),
        "unit": "mg/dL",
    },
    "HDL": {
        "male": (40.0, 999.0),
        "female": (50.0, 999.0),
        "unit": "mg/dL",
    },
    "LDL": {
        "normal": (0.0, 100.0),
        "unit": "mg/dL",
    },
    "Triglycerides": {
        "normal": (0.0, 150.0),
        "unit": "mg/dL",
    },
    "TSH": {
        "normal": (0.4, 4.0),
        "unit": "mIU/L",
    },
}