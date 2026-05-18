# 🌤️ Real-Time Climate & Environmental Monitoring Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Streamlit-1.25+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Altair-Enforced%20Stability-orange?style=for-the-badge" alt="Altair">
  <img src="https://img.shields.io/badge/API-OpenWeatherMap-informational?style=for-the-badge&logo=unrealengine&logoColor=white" alt="API">
</p>

---

## 📌 Project Overview

This interactive, production-ready live dashboard is engineered to monitor metropolitan microclimates and instantly capture severe environmental anomalies. By tracking real-time fluctuations, the system addresses the risks of **Urban Heat Island (UHI)** effects and unexpected local heatwaves.

---

## 🚀 Key Technical Features

### 📡 1. Optimized REST Ingestion Pipeline
- Consumes live atmospheric metrics from the **OpenWeatherMap API** endpoint.
- Enforces a strict **10-second REST polling frequency** loop. This mathematically utilizes only 6 requests/min out of the 60 requests/min free-tier limit, providing an 80% safety buffer against rate-limiting (`HTTP 429` errors).

### ⏳ 2. Bounded Sliding Window
- Maintains a strict historical state queue constrained to **$N=20$ active data points** inside `st.session_state`. 
- Prevents memory bloating by automatically pruning the oldest data frame records as new updates arrive.

### 🚨 3. Pre-attentive Threshold Alerting
- Features a dynamic sidebar configuration where operators can adjust the **Temperature Alert Limit**.
- Breaching safe operational boundaries instantly overrides the presentation layout with custom CSS animations, pulsing a high-contrast crimson warning (`#EF4444`) to guarantee immediate human reaction without reading fine print.

### 📊 4. Spatial Axis Stability
- Locks the horizontal coordinate system and trend slopes inside Altair charts (`scale(domain=[10.0, 30.0])`). 
- This prevents disturbing "axis jumping" transitions, optimizing cognitive load management.

### 💾 5. Compliance Log Export
- Includes a live-serialization data engine that exports the current sliding window matrix into a standardized `.csv` spreadsheet file at the click of a button.

---

## ⚙️ Pipeline Architecture Flow


```

[ OpenWeatherMap API Node ]
│
▼ (HTTP GET Request / Non-blocking Polling Every 10s)
[ Streamlit Backend Engine ]
│
▼ (Evaluates State Array Matrix / Prunes Index > 20)
[ Reactive Presentation Layer ]
├── Real-Time KPI Cards (Dynamic HTML/CSS Injection)
├── Stable Coordinate Trend Line Charts
└── On-the-fly CSV Document Exporter

```

---

## 🛠️ Local Installation & Launch Guide

Follow these simple steps to deploy and execute the monitoring application on your local terminal environment:

### Prerequisites
Make sure **Python 3.8 to 3.11** is installed on your computer. You can verify it by executing:
```bash
python --version

```

### Step 1: Open the Project Directory

Launch your preferred terminal application (Command Prompt or PowerShell for Windows) and navigate to your source directory:

```bash
cd "C:\Users\Erdem\OneDrive\Рабочий стол\DV2"

```

### Step 2: Install Pipeline Dependencies

Execute the standard package manager command to download required matrix processing and streaming modules:

```bash
pip install streamlit requests pandas altair

```

### Step 3: Spin Up the Streamlit Engine

To bypass any environmental binary execution constraints on Windows machines, launch the script explicitly using the Python module flag:

```bash
python -m streamlit run app.py

```

Upon successful startup, a background web-worker instance will run locally, and your default web browser will automatically open the dashboard view at:
👉 **`http://localhost:8501`**

---

## 💡 Live Demonstration Guide (For Presentation & Grading)

To showcase the system's reactive **Change Detection & Alerting mechanisms** during your practical evaluation session, follow this scenario:

1. **Baseline Mode:** Let the system execute smoothly for 30–40 seconds. Point out that the metrics layout uses neutral slate-blue tones, and connection updates refresh flawlessly every 10 seconds.
2. **Axis Stability Evaluation:** Show that as new points arrive, the graph moves smoothly from right to left while the Y-axis numbers remain perfectly steady.
3. **Triggering the Alert:** Navigate to the **🚨 Threshold Configurations** component in the left sidebar.
4. **Altering Parameters:** Use the numerical input field to reduce the **Set Temperature Alert Limit (°C)** to a digit lower than the current temperature on screen.
5. **Result Evaluation:** On the very next refresh cycle, the main indicator card will instantly turn bright red, start an automated flashing pulse, and modify the chart trend lines to crimson red, demonstrating effective **pre-attentive visualization design**.

---

## 👥 Engineering Team & Contacts

* **Developer 1:** Erdem `[GitHub Profile Link / Contact Info]`
* **Developer 2:** `[Partner Name / Contact Info]`
3. **Раскрывающийся список:** Раздел демонстрации для преподавателя будет аккуратно спрятан под стрелочку, по клику на которую развернется пошаговый чек-лист. Это экономит место и выглядит очень аккуратно.

Этот файл готов на 100%. Просто сохрани его и отправляй в свой GitHub-репозиторий!
