
# Shipping Email Segregation & Data Extraction System

This project classifies shipping emails into:
- Tonnage
- Cargo VC
- Cargo TC

and extracts structured information using:
- Regex
- Rule-based NLP
- Scikit-learn ML classifier

## Features
- No external LLM APIs used
- Automatic email classification
- Structured JSON output
- Easy to extend

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Project Structure

```
shipping_email_project/
│
├── main.py
├── classifier.py
├── extractors.py
├── utils.py
├── sample_emails.py
├── requirements.txt
└── output/
```
