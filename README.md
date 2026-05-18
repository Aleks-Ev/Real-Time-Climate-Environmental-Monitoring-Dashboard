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
