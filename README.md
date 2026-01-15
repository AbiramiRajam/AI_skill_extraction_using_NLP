# AI Skill Extraction Platform

## Overview

The AI Skill Extraction Platform is a Streamlit application that uses natural language processing (NLP) to extract technical and soft skills from job descriptions. The platform helps HR professionals, recruiters, and data teams to analyze job descriptions and map skills in a structured format.

Key functionalities include:

- Extracting programming languages, databases, cloud platforms, DevOps and CI/CD tools, BI/ETL tools, containerization, ML/AI frameworks, and soft skills.
- Handling pasted text or uploaded PDF/DOCX files.
- Normalizing skill names and handling aliases for consistency.
- Counting occurrences of each skill for analysis and reporting.

## NLP Approach
Rule-based NLP using spaCy PhraseMatcher.

### Why Rule-Based?
- Interpretable
- No training data required
- High precision
- Easy to maintain

## Tech Stack
Python, Streamlit, spaCy, pdfplumber, python-docx

## Features

- Multiple input options: paste text or upload PDF/DOCX files.
- AI-powered skill extraction using spaCy.
- Structured output categorized by technology, tools, and soft skills.
- Extensible tech stack: easy to update or add new categories.
- Real-time interactive interface via Streamlit.

## Technology Stack

- Python 3
- Streamlit
- spaCy (`en_core_web_sm` model)
- pdfplumber
- python-docx

## How to Run
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run streamlit_app.py
```
## Future Enhancements
- Transformer NER
- Resume matching
- Skill gap analysis
