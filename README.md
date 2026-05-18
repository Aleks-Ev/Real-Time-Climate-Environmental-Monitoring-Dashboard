```markdown
# 🌤️ Real-Time Climate & Environmental Monitoring Dashboard

An interactive, production-ready real-time data visualization dashboard designed to monitor metropolitan microclimates and detect dangerous environmental anomalies (Urban Heat Island effects, flash heatwaves, and climate fluctuations). Built with **Python**, **Streamlit**, and **Altair**, utilizing live data streaming from the **OpenWeatherMap REST API**.

This project represents **Track B (Real-Time Data Visualization)** of the Final Data Visualization Project.

## 🚀 Key Features

- **Live REST Ingestion Pipeline:** Consumes current climate metrics every 10 seconds with optimized connection handlers to stay safely within API rate limits (`HTTP 429` protection).
- **Dynamic Node Switching:** Interactive sidebar to select different metropolitan nodes (Ankara, Istanbul, Moscow, London, New York) on the fly, with automated state management that flushes buffers upon node mutation.
- **Sliding Window Temporal Context:** Displays an ongoing trend history bounded strictly at a fixed $N=20$ data points window to ensure optimal memory consumption and historical context.
- **Pre-attentive Alerting System:** Real-time threshold monitoring with dynamic HTML/CSS injection. Breaching safe parameters triggers high-contrast blinking crimson styling (`#EF4444`) to instantly capture human pre-attentive focus without cognitive overhead.
- **Enforced Chart Axis Stability:** Spatially locked coordinates inside Altair charts prevent axis-jumping, allowing operators to easily track exact trend slopes.
- **Data Audit Export:** Dynamic on-the-fly serialization of the current sliding window matrix into a downloadable `.csv` spreadsheet file for compliance logging.

---

## 🛠️ Installation & Local Setup Instructions

Follow these steps to deploy and run the dynamic monitoring dashboard on your local machine:

### Prerequisites
Ensure you have **Python 3.8 to 3.11** installed on your system. You can verify your version by running:
```bash
python --version

```

### 1. Clone or Navigate to the Project Directory

Open your terminal (Command Prompt or PowerShell on Windows) and navigate to the project directory:

```bash
cd "path/to/your/DV2/folder"

```

### 2. Install Required Dependencies

Install all necessary Python data processing and visualization libraries via `pip`:

```bash
pip install streamlit requests pandas altair

```

### 3. Run the Streamlit Application

Because of environment path specifications on certain Windows machines, it is highly recommended to run Streamlit explicitly via the Python module flag:

```bash
python -m streamlit run app.py

```

Once executed, the terminal will spin up a local hosting worker instance, and the interactive interface will automatically open in your default browser at:
`http://localhost:8501`

---

## ⚙️ Project Architecture & Pipeline Flow

The system operates via a continuous REST Polling architecture:

```
[ OpenWeatherMap API ] ──(HTTP GET every 10s)──> [ Streamlit Backend Buffer ]
                                                              │
                                                  (Pruning > 20 points)
                                                              │
                                                              ▼
                                               [ Live Reactive Interface ]
                                               ├── KPI Metrics Cards
                                               ├── Stable Line Charts
                                               └── Dynamic CSV Exporter

```

## 🚨 Demonstration Guideline (For Project Presentation)

To demonstrate the **Conditional Formatting Threshold Alert** during grading:

1. Let the system run for 30 seconds in standard execution mode (Metrics cards will display a stable, calm slate-blue style).
2. Go to the **🚨 Threshold Configurations** module located in the left sidebar.
3. Lower the **Set Temperature Alert Limit (°C)** numerical wheel value to a digit slightly below the current actual node temperature.
4. During the next 10-second polling refresh cycle, the UI will capture the change, swap current cards into a high-visibility crimson red blinking alarm state, and change the trend chart vectors to crimson red.

## 👥 Team Composition & Members

* **Member 1:** [Your Name / GitHub Profile]
* **Member 2:** [Partner Name]
* **Member 3:** [Partner Name]

**Submission Deadline Reference:** May 25, 2026.

```

---

### Совет по загрузке на GitHub:
Когда вы создадите репозиторий на GitHub и загрузите туда ваш `app.py` и этот `README.md`, GitHub автоматически прочитает этот файл и превратит его в красивую веб-страницу с таблицами, кодом и разметкой. Это будет выглядеть очень стильно для проверяющих!

```
