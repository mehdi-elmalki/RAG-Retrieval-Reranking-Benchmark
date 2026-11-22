
<div align="center">

# 🔎 RAGNova
### Information Retrieval & Reranking Benchmark

**A reproducible document retrieval and binary question-answering system**

BM25 · TF-IDF · LSA · Hybrid Fusion · RRF · Logistic Reranking

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?logo=streamlit&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-Machine_Learning-F7931E?logo=scikitlearn&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white)
![Dataset](https://img.shields.io/badge/Dataset-BoolQ-725AC1)

**École Centrale Casablanca | Data Science Project**

[Overview](#-overview) •
[Architecture](#-architecture) •
[Methods](#-retrieval-methods) •
[Installation](#-installation--quick-start) •
[Evaluation](#-evaluation--reproducibility)

</div>

---

## 📌 Overview

**RAGNova** is a document retrieval and reranking benchmark developed to compare multiple information retrieval approaches on the **BoolQ dataset**.

The system evaluates how different ranking strategies retrieve relevant passages and integrates a lightweight machine-learning reader for binary question answering.

The application provides an interactive Streamlit interface for exploring retrieval results.

> **Scope:** RAGNova is a retrieval and binary question-answering prototype, not a generative RAG system. Its reader predicts **Yes / No** answers and does not generate free-form text.

### Key Features

- 🔍 Six retrieval and reranking strategies
- 📊 Comparative evaluation of retrieval performance
- 🧠 Binary question answering using TF-IDF and logistic regression
- 🔀 Hybrid retrieval and Reciprocal Rank Fusion
- 🖥️ Interactive Streamlit application
- 🧪 Unit tests and reproducibility scripts
- 🚀 Automated Windows launcher

---

## 🏗️ Architecture

```text
                     ┌──────────────────┐
                     │   BoolQ Dataset  │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Data Preparation │
                     └────────┬─────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │   Retrieval Pipeline    │
                 ├─────────────────────────┤
                 │ BM25                    │
                 │ TF-IDF                  │
                 │ LSA (SVD)               │
                 │ Weighted Fusion         │
                 │ RRF                     │
                 │ Logistic Reranking      │
                 └────────────┬────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Ranked Passages  │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │  Binary Reader   │
                     │ TF-IDF + LogReg  │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │  YES / NO        │
                     └──────────────────┘
```

---

## 🧠 Retrieval Methods

RAGNova compares six retrieval and ranking approaches.

| Method | Approach | Description |
|---|---|---|
| **BM25** | Lexical retrieval | Probabilistic term-based ranking |
| **TF-IDF** | Vector-space retrieval | Term weighting and similarity |
| **LSA** | Dimensionality reduction | Latent semantic analysis using 48 SVD dimensions |
| **Weighted Fusion** | Hybrid retrieval | Combination of BM25 and TF-IDF scores |
| **RRF** | Rank fusion | Reciprocal Rank Fusion |
| **Logistic Reranking** | Machine learning | Reranking using four combined signals |

### Binary Question Answering

The reader uses **TF-IDF features and logistic regression** to predict a binary answer.

**Output:** `Yes` or `No`

Neural encoders, cross-encoders and generative language models discussed in the accompanying report are theoretical extensions and are not executed by the current application.

---

## 📂 Project Structure

```text
RAGNova_Centrale_Casablanca_Final/
│
├── 01_Rapport/
│   └── Research report (Word / PDF)
│
├── 02_Presentation/
│   └── Project presentation (PPTX / PDF)
│
├── 03_Dataset/
│   └── Source data and preparation scripts
│
├── 04_Experiments/
│   ├── Experimental scripts
│   ├── Prepared data
│   ├── Results
│   └── Trained models
│
├── 05_Application/
│   ├── app.py
│   ├── rag_core.py
│   └── Verification and test scripts
│
├── 06_Documentation/
│   └── Methodology and reproducibility
│
├── 07_Captures/
│   └── Application screenshots
│
├── .streamlit/
├── Dockerfile
├── requirements.txt
├── requirements-documents.txt
├── lancer_windows.bat
└── README.md
```

---

## 🚀 Installation & Quick Start

### Option 1 — Automatic Windows Launcher (Recommended)

The easiest way to run RAGNova is through the provided Windows launcher.

**Requirements:** Windows and Python 3.12 (64-bit).

**Step 1.** Download or clone the repository.

**Step 2.** Open the project folder.

**Step 3.** Double-click:

```text
lancer_windows.bat
```

The launcher automatically:

1. Checks Python 3.12 availability.
2. Creates or validates the virtual environment.
3. Installs the required dependencies.
4. Starts the Streamlit application.

Once the server is running, open:

**http://localhost:8501**

> The first launch may take several minutes while Python packages are installed. An internet connection is required for missing dependencies.

### Option 2 — Manual Installation

Open PowerShell in the project root.

**Create the virtual environment:**

```powershell
py -3.12 -m venv .venv
```

**Upgrade pip:**

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

**Install dependencies:**

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Start the application:**

```powershell
.\.venv\Scripts\python.exe -m streamlit run 05_Application\app.py
```

**Application URL:** http://localhost:8501

To stop the application, press `Ctrl + C` in the terminal.

---

## 🖥️ Interactive Application

RAGNova provides a Streamlit interface for exploring document retrieval and binary question answering.

The application allows users to interact with the implemented retrieval pipeline and inspect ranked passages.

Application screenshots are available in:

```text
07_Captures/
```

---

## 📊 Evaluation & Reproducibility

The repository includes experimental scripts, archived results and verification tools.

### Run Unit Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s 05_Application -v
```

The application includes four unit tests.

### Verify the Retrieval Pipeline

```powershell
.\.venv\Scripts\python.exe 05_Application\verify_pipeline.py 2083
```

This command compares pipeline outputs with archived traces.

### Reproduce Experiments

```powershell
.\.venv\Scripts\python.exe 03_Dataset\prepare_data.py
.\.venv\Scripts\python.exe 04_Experiments\run_experiments.py
.\.venv\Scripts\python.exe 04_Experiments\statistical_analysis.py
```

> **Important:** These commands regenerate experimental data and results under `04_Experiments/`, replacing existing archived outputs.

### Reproducibility Notes

- Dependencies are pinned in `requirements.txt`.
- Four unit tests and Streamlit execution have been verified on Windows.
- Strict comparisons with archived retrieval traces may differ across platforms when passages have identical scores.
- NumPy top-k selection does not explicitly resolve score ties.
- RRF and logistic reranking may inherit candidate-list differences.
- Archived metrics in `04_Experiments/results/metrics.json` are not recalculated by the Streamlit application.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python 3.12 |
| Interface | Streamlit |
| Data processing | NumPy, pandas |
| Machine learning | Scikit-learn |
| Retrieval | BM25, TF-IDF, LSA |
| Fusion | Weighted Fusion, RRF |
| Reranking | Logistic Regression |
| Visualization | Matplotlib |
| Dataset | BoolQ |
| Environment | Python venv |
| Deployment assets | Windows BAT launcher, Dockerfile |

---

## 🔧 Troubleshooting

| Issue | Recommended Action |
|---|---|
| Python 3.12 not found | Install Python 3.12 (64-bit) |
| Streamlit module missing | Install `requirements.txt` |
| Incompatible virtual environment | Recreate `.venv` with Python 3.12 |
| First launch is slow | Wait for dependency installation |
| Port 8501 already in use | Stop the other Streamlit instance or select another port |
| Archived trace mismatch | Check score ties and platform-dependent ranking |

---

## 📚 Documentation

The repository contains supporting academic and technical materials:

- **Research Report:** project background, methodology and analysis.
- **Presentation:** project overview and experimental discussion.
- **Experiments:** scripts, results and trained models.
- **Technical Documentation:** reproducibility notes and methodology.
- **Application Screenshots:** visual documentation of the Streamlit interface.

---

## 🎓 Academic Context

Developed as a **Data Science academic project at École Centrale Casablanca**.

The project focuses on information retrieval, ranking algorithms, machine learning and experimental reproducibility.

---

<div align="center">

### RAGNova — Retrieval, Ranking & Reproducibility

*From lexical retrieval to hybrid ranking and binary question answering.*

**École Centrale Casablanca**

</div>
