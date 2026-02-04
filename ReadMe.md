# Adversarial Phishing Detection: Build, Breach, Patch

![Status](https://img.shields.io/badge/Status-Complete-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-grey)

## Overview

This project explores the fragility of NLP-based security tools. We trained a DistilBERT classifier to detect phishing emails, then demonstrated how easily it could be bypassed using **Context Injection** (MITRE T1566).

The core experiment consists of three phases:
1.  **Build:** Training a baseline model on the Morpheus dataset.
2.  **Breach:** Bypassing detection by wrapping malicious payloads in polite corporate jargon .
3.  **Patch:** Hardening the model via adversarial retraining to achieve 100% resilience against the identified vectors.

## Full Project Presentation
For a complete explanation of the methodology, attack vectors, adversarial retraining, and implementation details, see the full project presentation on YouTube:
https://youtu.be/OXoXY1Huljg

## Repository Structure

| File / Folder | Description |
| :--- | :--- |
| `MVP/app.py` | **(MVP)** Streamlit web interface for real-time testing. |
| `MVP/traffic_logs.log` | Auto-generated audit logs for security review. |
| `notebook.ipynb` | Main research notebook containing the full attack/defense pipeline. |
| `morpheus_dataset_final.jsonl` | Training and validation dataset. |
| `requirements.txt` | Python dependencies. |
| `phishing_model/` | **(External)** Baseline model artifacts. Download from Releases. |
| `phishing_model_optimized/` | **(External)** Hardened model artifacts. Download from Releases. |

## Quick Start

### 1. Setup Environment
Clone the repo and install dependencies:

```bash
git clone https://github.com/ItsBarMor/AI-Driven-Cybersecurity.git
cd AI-Driven-Cybersecurity
pip install -r requirements.txt
```

### 2. Download Model Artifacts
**Note**: The models are too large for standard Git and are hosted externally.

1. Go to the [Releases]('https://github.com/ItsBarMor/AI-Driven-Cybersecurity/releases') section of this repository.
2. Download phishing_model.zip and phishing_model_optimized.zip.
3. Extract them into the root directory of the project.

**Your folder structure must look like this for the notebook to run:** 
```
/AI-Driven-Cybersecurity
  ├── notebook.ipynb
  |         *
  |         *
  |         *
  ├── morpheus_dataset_final.jsonl
  ├── phishing_model/              <-- Extracted Folder 1
  └── phishing_model_optimized/    <-- Extracted Folder 2
```
### 3. Run the Analysis
Open Jupyter Lab or Notebook:
```bash
jupyter notebook notebook.ipynb
```
Run all cells to reproduce the training, attack simulation, and verification graphs.

### 4. Run the MVP Interface (Prototype)
To launch the interactive web dashboard and test emails in real-time:
```bash
pip install streamlit
cd MVP #from root
streamlit run app.py 
```
This will open your browser to http://localhost:8501.
* Input: Paste any email text.
* Output: Instant classification (Safe/Phishing) + confidence score.
* Logging: All requests are automatically saved to traffic_logs.log for auditing.

# Team
* Adi Haim
* Afik Aharon
* Bar Mor
* Ron Noiman

# Disclaimer
This code is for educational and research purposes only. The attack vectors demonstrated here should only be used on systems you own or have explicit permission to test.


