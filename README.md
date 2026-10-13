# 🍔 LangChain for GenAI Applications — Assessment Submission

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.3%2B-green?logo=chainlink)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-black?logo=flask)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4%2B-F7931E?logo=scikit-learn)
![Groq](https://img.shields.io/badge/Groq-Cloud%20LLM-orange)

---

## 📌 Executive Overview

This repository contains the complete assessment solution for **Modules 13–16: Machine Learning Deployment, Generative AI Applications, Transformers & LLMs, and LangChain Multi-Turn Systems**.

The solution implements the intelligent delivery and dining assistant ecosystem for **QuickBite**, integrating predictive regression modeling, REST API deployment, interactive Streamlit GenAI applications, stateful multi-turn LangChain assistants, and defensive software refactoring.

---

## 🗂️ Repository Directory Structure

```text
LANGCHAIN FOR GENAI APPLICATIONS Assesment/
│
├── .env                                       # Local environment variables (GROQ_API_KEY)
├── .gitignore                                 # Git ignore file for secrets, venv, and caches
├── delivery_model.joblib                      # Serialized ML model for delivery time prediction
├── README.md                                  # Complete repository documentation
│
├── Section A - Concept Application/
│   └── Section_A_Answers.md                   # Scenario analysis for S1 through S6
│
├── Section B - Practical Coding Tasks/
│   ├── delivery_model.joblib                  # Model artifact for Section B
│   ├── task1_model_training.py                # Synthetic data generation, regression, joblib save
│   ├── task2_flask_api.py                     # Flask REST API (/predict endpoint with 400 validation)
│   ├── task3_dish_generator_app.py           # Streamlit AI dish description generator
│   ├── task4_langchain_memory_assistant.py    # 5-turn stateful LangChain assistant with memory buffer
│   └── task4_conversation_log.txt             # Console execution log of 5-turn test simulation
│
├── Section C - Mini Capstone Project/
│   ├── app.py                                 # QuickBite AI Streamlit multi-turn ordering application
│   ├── menu.json                              # Restaurant catalog with 12 items across 5 cuisines
│   ├── delivery_model.joblib                  # ML delivery regression artifact
│   └── capstone_documentation.md              # Architecture diagram, component logs, and guide
│
└── Section D - AI-Augmented Learning/
    ├── step1_ai_original.py                   # Unedited AI-generated order tracker (with flaws)
    ├── step2_corrected.py                     # Hardened, production-ready order tracker with unit tests
    └── ai_prompts_and_debug_notes.md          # Flaw analysis, line audit, and AI quality reflection
```

---

## 🚀 Section-by-Section Breakdown

### 📚 Section A: Concept Application
Comprehensive scenario evaluations addressing core architectural decisions:
- **Scenario S1 (Model Serialization):** Why `joblib` dramatically outperforms `pickle` for Scikit-Learn models with dense NumPy arrays, avoiding serialization overhead.
- **Scenario S2 (Generative Image Models):** Comparing Variational Autoencoders (VAEs) vs. Latent Diffusion Models (Stable Diffusion) for culinary marketing assets.
- **Scenario S3 (Transformer Architectures):** Decoder-only (GPT) vs. Encoder-only (BERT) architectures for conversational ordering assistants.
- **Scenario S4 (Few-Shot Prompt Engineering):** Eliminating hallucinations and enforcing dietary classifications via exemplar demonstrations.
- **Scenario S5 (Chains vs. Autonomous Agents):** Deterministic sequential LangChain chains vs. dynamic tool-calling ReAct agents.
- **Scenario S6 (Fine-Tuning vs. RAG):** Evaluating cost, freshness, and hallucination bounds for frequent menu updates.

---

### 💻 Section B: Practical Coding Tasks

#### 1. Task 1: Scikit-Learn Model Training & Serialization
- Synthetic dataset generation (150 orders) modeling delivery time as a function of **Distance (km)**, **Item Count**, and **Rain Flag**.
- `LinearRegression` training achieving test RMSE of **~1.78 minutes**.
- Serialization and verification using `joblib.dump` and `joblib.load`.
- **Run Task 1:**
  ```powershell
  python "Section B - Practical Coding Tasks/task1_model_training.py"
  ```

#### 2. Task 2: Flask REST API (`/predict`)
- Lightweight HTTP REST microservice loading `delivery_model.joblib` at startup.
- Robust JSON payload validation returning HTTP `400 Bad Request` with missing fields on invalid queries.
- Returns predicted delivery time rounded to 1 decimal place with HTTP `200 OK`.
- **Run Task 2:**
  ```powershell
  python "Section B - Practical Coding Tasks/task2_flask_api.py"
  ```

#### 3. Task 3: Streamlit AI Dish Description Generator
- Intuitive web application for restaurant partners to craft culinary copy.
- Inputs for **Dish Name**, **Cuisine Type**, and **Description Length** (Short, Medium, Detailed).
- Generates sensory language, dietary tags, and beverage pairings via Groq LLM.
- Includes dynamic loading spinner, styled display card, character counter, and instant "Regenerate" button.
- **Run Task 3:**
  ```powershell
  streamlit run "Section B - Practical Coding Tasks/task3_dish_generator_app.py"
  ```

#### 4. Task 4: Multi-Turn Conversation Assistant with Memory
- Multi-turn food ordering assistant tracking state across conversations.
- Retains customer delivery address and dietary preferences across 5 sequential turns.
- Interactive mode and automated 5-turn test simulation with final memory buffer dump.
- **Run Task 4:**
  ```powershell
  python "Section B - Practical Coding Tasks/task4_langchain_memory_assistant.py"
  ```

---

### 🌟 Section C: Mini-Capstone Project — QuickBite AI

QuickBite AI is an intelligent food ordering assistant combining conversational AI with an ML delivery estimator.

```mermaid
flowchart LR
    A[Customer Chat UI] --> B[LangChain Agent Core]
    B --> C[Menu KB: menu.json]
    B --> D[@tool get_delivery_estimate]
    D --> E[ML Model: delivery_model.joblib]
    B --> F[Groq Cloud LLM]
    F --> A
```

#### Core Capabilities:
1. **Interactive Chat:** Streamlit chat bubbles (`st.chat_message`) with conversational memory.
2. **Dynamic Menu Search:** Context injection of relevant items from `menu.json` (12 items across Indian, Italian, Mexican, Japanese, Continental cuisines).
3. **ML Tool Integration:** Custom `@tool get_delivery_estimate` wrapping the trained regression model.
4. **Persistent Sidebar:** Customer profile (Address, Diet selector: All/Veg/Non-Veg), interactive shopping cart with live total, direct ML slider estimator, and chat reset.
- **Launch QuickBite AI:**
  ```powershell
  streamlit run "Section C - Mini Capstone Project/app.py"
  ```

---

### 🛡️ Section D: AI-Augmented Learning

Comprehensive code review and hardening of an AI-generated order tracking module:
- **`step1_ai_original.py`:** Raw AI code containing critical flaws (unhandled `KeyError` on missing IDs, in-place global mutation, lack of type validation).
- **`step2_corrected.py`:** Production-hardened refactor introducing `OrderTracker` class, safe `.get()` retrieval, standardized JSON dictionaries, and a complete `unittest.TestCase` suite.
- **Run Unit Tests:**
  ```powershell
  python "Section D - AI-Augmented Learning/step2_corrected.py"
  ```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```powershell
git clone <your-repository-url>
cd "LANGCHAIN FOR GENAI APPLICATIONS Assesment"
```

### 2. Activate Virtual Environment
```powershell
.\env\Scripts\activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```
*(Dependencies: `scikit-learn`, `joblib`, `flask`, `streamlit`, `langchain`, `langchain-groq`, `python-dotenv`, `requests`)*

### 4. Configure API Credentials
Create or verify the `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🧪 Verification Commands

| Component | Execution Command | Expected Output |
| :--- | :--- | :--- |
| **Model Training** | `python "Section B - Practical Coding Tasks/task1_model_training.py"` | RMSE ~1.78 min, Verification: PASS |
| **Flask API** | `python "Section B - Practical Coding Tasks/task2_flask_api.py"` | Flask listening on port 5000 |
| **Dish Generator** | `streamlit run "Section B - Practical Coding Tasks/task3_dish_generator_app.py"` | Streamlit web UI at localhost:8501 |
| **Memory Assistant** | `python "Section B - Practical Coding Tasks/task4_langchain_memory_assistant.py"` | 5-turn simulation & memory buffer dump |
| **Mini-Capstone** | `streamlit run "Section C - Mini Capstone Project/app.py"` | QuickBite AI ordering dashboard |
| **Section D Tests** | `python "Section D - AI-Augmented Learning/step2_corrected.py"` | Ran 3 tests in 0.000s - OK |

---

## 👨‍💻 Author & Assessment Details
- **Module:** M16 - LangChain for GenAI Applications
- **Curriculum:** TOPS Technologies Advanced GenAI & Agentic AI Program
- **Status:** Complete & Fully Tested
