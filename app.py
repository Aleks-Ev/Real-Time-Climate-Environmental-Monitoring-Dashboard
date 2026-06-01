import streamlit as st
import requests
import pandas as pd
import time
import random
from datetime import datetime
import altair as alt

# =========================================================================
# 🛠️ CONFIGURATION PALETTE (НАСТРОЙКА ЦВЕТОВ ДЛЯ ТЕБЯ / РАЗРАБОТЧИКА)
# =========================================================================
# Изменяй эти значения ниже, чтобы мгновенно перекрасить весь дашборд:

THEME_BG_START = "#F7F8E2"    # Начало фонового градиента (светло-пастельный)
THEME_BG_END = "#E2E8F0"      # Конец фонового градиента (мягкий серый)
THEME_TEXT_COLOR = "#0F172A"  # Основной цвет текста и крупных цифр в карточках
THEME_SUBTEXT_COLOR = "#475569" # Цвет подписей и мелкого текста (secondary text)

# Настройка круглых коконов-подложек для иконок:
# Рекомендуется использовать темный цвет с прозрачностью (0.08), чтобы иконки не сливались с белым стеклом
THEME_COCOON_BG = "rgba(15, 23, 42, 0.08)" 

# =========================================================================
# 1. UI CONFIGURATION & UX STRATEGY (LIGHT GLASSMORPHISM)
# =========================================================================
st.set_page_config(
    page_title="Live Weather & Environment Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# Внедрение стилей. f-строка автоматически подставляет твои цвета из палитры выше
st.markdown(f"""
    <style>
    /* 1.1. ГЛОБАЛЬНЫЙ ФОН СТРАНИЦЫ: Задает двухцветный плавный градиент */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(135deg, {THEME_BG_START} 0%, {THEME_BG_END} 100%) !important;
    }}
    
    /* 1.2. БОКОВАЯ ПАНЕЛЬ (SIDEBAR): Размытие заднего фона для эффекта глубины */
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 0, 0, 0.05);
    }}
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {{
        color: {THEME_TEXT_COLOR} !important;
    }}

    /* 1.3. БАЗОВАЯ КАРТОЧКА МАТОВОГО СТЕКЛА (GLASSMORPHISM):
       Размывает фон под собой на 12px и имеет полупрозрачную белую основу */
    .metric-card {{
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.6); /* Глянцевый кант "стекла" */
        box-shadow: 0 4px 20px 0 rgba(15, 23, 42, 0.05);
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between; /* Текст уходит влево, иконка вправо */
        align-items: center;
    }}

    /* 1.4. КАРТОЧКА ТРЕВОГИ (ALERT STATE): Подсвечивается красным при превышении порога */
    .alert-card {{
        background: rgba(254, 226, 226, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(239, 68, 68, 0.4);
        box-shadow: 0 4px 20px 0 rgba(239, 68, 68, 0.1);
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        animation: pulse 2.5s infinite; /* Эффект "дышащей" пульсации рамы */
    }}
    
    .card-text {{
        flex: 1;
    }}
    
    /* 1.5. КОКОНЫ ДЛЯ ИКОНОК (КОНТРАСТНАЯ ЗАЩИТА):
       Круглые подложки фиксированного размера (60x60px), центрируют эмодзи и картинки,
       не давая светлым иконкам из API (например, белому дождю) исчезнуть на белом стекле */
    .icon-cocoon {{
        background: {THEME_COCOON_BG} !important; 
        border-radius: 50%; 
        width: 60px; 
        height: 60px; 
        display: flex; 
        justify-content: center; 
        align-items: center;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1); /* Внутренняя тень для объема */
        margin-left: 10px;
        flex-shrink: 0; /* Защита от сжатия при длинном тексте слева */
    }}

    /* Размер шрифта для эмодзи внутри коконов */
    .emoji-icon {{
        font-size: 28px;
        line-height: 1;
    }}
    
    @keyframes pulse {{
        0% {{ border-color: rgba(239, 68, 68, 0.4); }}
        50% {{ border-color: rgba(239, 68, 68, 0.8); }}
        100% {{ border-color: rgba(239, 68, 68, 0.4); }}
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INTERACTIVE SIDEBAR FOR MONITORING SETTINGS
# ==========================================
st.sidebar.header("⚙️ Monitoring Settings")

CITIES = {
    "Ankara 🇹🇷": "Ankara",
    "Istanbul 🇹🇷": "Istanbul",
    "Moscow 🇷🇺": "Moscow",
    "London 🇬🇧": "London",
    "New York 🇺🇸": "New York"
}
# help-подписи выводят всплывающие подсказки при наведении на знак "?" на UI
selected_city_label = st.sidebar.selectbox(
    "Select Target City:", 
    list(CITIES.keys()),
    help="Смена географического узла (ноды). Автоматически сбрасывает скользящий датафрейм истории."
)
CITY = CITIES[selected_city_label]

st.sidebar.markdown("---")
st.sidebar.subheader("🚨 Threshold Configurations")

ALERT_THRESHOLD_TEMP = st.sidebar.number_input(
    label="Set Temperature Alert Limit (°C):",
    min_value=0.0,
    max_value=40.0,
    value=19.5,
    step=0.5,
    help="Критический температурный порог. Переводит UI в Alarm State при превышении лимита."
)

st.sidebar.markdown("---")
st.sidebar.subheader("📝 Project Track Focus")
st.sidebar.info(
    f"**Why monitor {CITY}?**\n"
    "Real-time microclimate monitoring reveals critical Urban Heat Island (UHI) effects."
)

# Логика очистки истории при переключении городов
if "current_city" not in st.session_state:
    st.session_state.current_city = CITY

if st.session_state.current_city != CITY:
    st.session_state.weather_history = pd.DataFrame(columns=["Timestamp", "Temperature", "Humidity"])
    st.session_state.current_city = CITY

# ==========================================
# 3. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ И ИНИЦИАЛИЗАЦИЯ
# ==========================================
MAX_POINTS = 20 # Размер окна истории на графике (тайм-вектор)

if "weather_history" not in st.session_state:
    st.session_state.weather_history = pd.DataFrame(columns=["Timestamp", "Temperature", "Humidity"])

API_KEY = "YOUR_API_KEY"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def get_wind_direction(degrees):
    """Преобразует азимут ветра в градусах в строковый вектор с эмодзи-стрелкой"""
    val = int((degrees / 22.5) + .5)
    directions = ["N ⬆️", "NNE ↗️", "NE ↗️", "ENE ↗️", "E ➡️", "ESE ↘️", "SE ↘️", "SSE ↘️", 
                  "S ⬇️", "SSW ↙️", "SW ↙️", "WSW ↙️", "W ⬅️", "WNW ↖️", "NW ↖️", "NNW ↖️"]
    return directions[(val % 16)]

def fetch_weather_data():
    """Запрос сырых метеоданных из API, деструктуризация JSON и сборка URL иконки погоды"""
    try:
        response = requests.get(URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            simulated_noise = random.uniform(-0.5, 0.5) # Имитация живых колебаний датчика
            
            temp_actual = round(data["main"]["temp"] + simulated_noise, 2)
            feels_like = round(data["main"]["feels_like"] + simulated_noise, 2)
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["main"] if "weather" in data else "Clear"
            
            # Извлечение уникального ID погодной иконки (например, '10d' или '01n')
            icon_code = data["weather"][0]["icon"] if "weather" in data else "01d"
            
            wind_speed = data["wind"]["speed"]
            wind_deg = data["wind"].get("deg", 0)
            wind_dir_string = get_wind_direction(wind_deg)
            
            return {
                "success": True,
                "temp": temp_actual,
                "feels_like": feels_like,
                "humidity": humidity,
                "condition": condition,
                # Ссылка на x2 PNG векторную иконку с официального сервера OpenWeather:
                "icon_url": f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                "wind_speed": wind_speed,
                "wind_dir": wind_dir_string,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "status": "Connected"
            }
        else:
            return {"success": False, "status": f"API Error {response.status_code}"}
    except Exception as e:
        return {"success": False, "status": "Disconnected / Timeout"}

# ==========================================
# 4. DASHBOARD PRESENTATION LAYER (СЛОЙ ОТРИСОВКИ)
# ==========================================
st.title("🌤️ Live Weather & Environmental Monitoring Dashboard")
st.markdown(f"### Active Target Node: **{selected_city_label}**")

# Инициализация пустых слотов (containers) для динамического рефреша без мерцания страниц
status_container = st.empty()
metrics_container = st.empty()
chart_container = st.empty()
download_container = st.empty()

while True:
    live_data = fetch_weather_data()
    current_time = datetime.now().strftime("%H:%M:%S")
    
    if live_data["success"]:
        # Добавление новой итерации лога в DataFrame
        new_row = pd.DataFrame([{
            "Timestamp": live_data["timestamp"],
            "Temperature": live_data["temp"],
            "Humidity": live_data["humidity"]
        }])
        st.session_state.weather_history = pd.concat([st.session_state.weather_history, new_row], ignore_index=True)
        
        # Обрезка старых точек, чтобы график не сжимался бесконечно
        if len(st.session_state.weather_history) > MAX_POINTS:
            st.session_state.weather_history = st.session_state.weather_history.iloc[1:].reset_index(drop=True)
            
        with status_container:
            col_stat1, col_stat2 = st.columns(2)
            col_stat1.markdown(f"**Connection Status:** `{live_data['status']}`")
            col_stat2.markdown(f"**System Clock Refresh Time:** `{current_time}`")

        # Проверка триггера превышения критической температуры
        is_alert = live_data["temp"] > ALERT_THRESHOLD_TEMP
        
        # --- СБОРКА И ПУБЛИКАЦИЯ КАРТОЧЕК МЕТРИК ---
        with metrics_container:
            col1, col2, col3, col4 = st.columns(4)
            
            # 1. КАРТОЧКА ТЕМПЕРАТУРЫ (С поддержкой Alarm State)
            if is_alert:
                col1.markdown(f"""
                    <div class="alert-card">
                        <div class="card-text">
                            <h3 style='margin:0; color:#B91C1C; font-size:15px;'>⚠️ TEMP CRITICAL ALERT</h3>
                            <p style='margin:5px 0 0 0; font-size:26px; color:#7F1D1D;'><b>{live_data['temp']} °C</b></p>
                            <small style='color: #991B1B;'>Feels like: <b>{live_data['feels_like']} °C</b></small>
                        </div>
                        <div class="icon-cocoon" style="background: rgba(239, 68, 68, 0.2) !important;">
                            <span class="emoji-icon">🚨</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                col1.markdown(f"""
                    <div class="metric-card">
                        <div class="card-text">
                            <h3 style='margin:0; color:#0284C7; font-size:15px;'>Current Temperature</h3>
                            <p style='margin:5px 0 0 0; font-size:26px; color:{THEME_TEXT_COLOR};'><b>{live_data['temp']} °C</b></p>
                            <small style='color: {THEME_SUBTEXT_COLOR};'>Feels like: <b>{live_data['feels_like']} °C</b></small>
                        </div>
                        <div class="icon-cocoon">
                            <span class="emoji-icon">🌡️</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            # 2. КАРТОЧКА ВЛАЖНОСТИ
            col2.markdown(f"""
                <div class="metric-card">
                    <div class="card-text">
                        <h3 style='margin:0; color:#059669; font-size:15px;'>Air Humidity</h3>
                        <p style='margin:5px 0 0 0; font-size:26px; color:{THEME_TEXT_COLOR};'><b>{live_data['humidity']} %</b></p>
                        <small style='color: {THEME_SUBTEXT_COLOR};'>Atmospheric stability</small>
                    </div>
                    <div class="icon-cocoon">
                        <span class="emoji-icon">💧</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 3. КАРТОЧКА ОБЩЕЙ ПОГОДЫ (Иконка с drop-shadow отсекает слияние со светлым стеклом)
            col3.markdown(f"""
                <div class="metric-card">
                    <div class="card-text">
                        <h3 style='margin:0; color:#D97706; font-size:15px;'>Sky Condition</h3>
                        <p style='margin:5px 0 0 0; font-size:26px; color:{THEME_TEXT_COLOR};'><b>{live_data['condition']}</b></p>
                        <small style='color: {THEME_SUBTEXT_COLOR};'>Real-time satellite vector</small>
                    </div>
                    <div class="icon-cocoon">
                        <img src="{live_data['icon_url']}" style="
                            width: 55px; 
                            height: 55px; 
                            filter: drop-shadow(1px 2px 3px rgba(15, 23, 42, 0.4)); /* Тень для белых иконок */
                        " alt="weather-icon"/>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 4. КАРТОЧКА СКОРОСТИ ВЕТРА
            col4.markdown(f"""
                <div class="metric-card">
                    <div class="card-text">
                        <h3 style='margin:0; color:#7C3AED; font-size:15px;'>Wind Flow Velocity</h3>
                        <p style='margin:5px 0 0 0; font-size:26px; color:{THEME_TEXT_COLOR};'><b>{live_data['wind_speed']} m/s</b></p>
                        <small style='color: {THEME_SUBTEXT_COLOR};'>Vector: <b>{live_data['wind_dir']}</b></small>
                    </div>
                    <div class="icon-cocoon">
                        <span class="emoji-icon">💨</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # 5. ГРАФИК КОЛЕБАНИЙ ТЕМПЕРАТУРЫ (ALTAIR)
        with chart_container:
            base_chart = alt.Chart(st.session_state.weather_history).mark_line(
                point=True, 
                color="#EF4444" if is_alert else "#0284C7"
            ).encode(
                x=alt.X('Timestamp:N', sort=None, title='Time Vector (Sliding Window Track)'),
                y=alt.Y('Temperature:Q', scale=alt.Scale(domain=[10.0, 30.0]), title='Temperature Scale (°C)'),
                tooltip=['Timestamp', 'Temperature']
            ).properties(
                title=f"Real-Time Thermal Fluctuations Trend ({CITY})",
                height=350
            )
            
            # Кастомизация стилей графика под общую палитру
            styled_chart = base_chart.configure(
                background='rgba(255, 255, 255, 0.45)' # Интеграция в Glassmorphism
            ).configure_view(
                strokeWidth=0
            ).configure_title(
                color=THEME_TEXT_COLOR,
                fontSize=14
            ).configure_axis(
                labelColor=THEME_SUBTEXT_COLOR,
                titleColor=THEME_TEXT_COLOR,
                gridColor='rgba(15, 23, 42, 0.06)'
            ).interactive()
            
            st.altair_chart(styled_chart, use_container_width=True)

        # 6. КНОПКА СКАЧИВАНИЯ ЛОГОВ (ДАННЫХ) В CSV
        with download_container:
            csv_buffer = st.session_state.weather_history.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Export Current Sliding Window Data Log ({CITY})",
                data=csv_buffer,
                file_name=f"environmental_metrics_{CITY}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    else:
        with status_container:
            st.error(f"Data ingestion pipeline drop detected. Status: {live_data['status']}. Retrying handshake...")

    time.sleep(10) # Тайм-аут шага итерации (10 секунд)
