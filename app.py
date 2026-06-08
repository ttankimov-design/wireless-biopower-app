import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Настройка заголовка страницы
st.set_page_config(page_title="Wireless Biopower", layout="centered")

st.title("Расчет КПД беспроводной зарядки")
st.write("КПД прототипа «Wireless Biopower» на основе экспериментальных данных.")

# Фиксированные параметры источника питания (Блок питания 5В, 2А)
U_in = 5.0
I_in = 2.0
P_in = U_in * I_in  # 10 Вт

# Вывод параметров источника в интерфейс
st.markdown("### Параметры первичного контура (Источник питания)")
col1, col2, col3 = st.columns(3)
col1.metric("Входное напряжение (U_in)", f"{U_in} В")
col2.metric("Входной ток (I_in)", f"{I_in} А")
col3.metric("Входная мощность (P_in)", f"{P_in} Вт", help="P = U * I")

# Боковая панель для настройки критической точки (15 мм)
st.sidebar.header("Настройка критической точки")
st.sidebar.write("Задайте значения, полученные на максимальном расстоянии 15 мм:")

v_15 = st.sidebar.slider("Выходное напряжение на 15 мм (В)", 3.5, 5.5, 4.42, step=0.01)
i_15 = st.sidebar.slider("Выходной ток на 15 мм (А)", 0.05, 0.6, 0.15, step=0.01)

# Экспериментальные точки расстояния (от 1 до 15 мм)
distance = np.array([1, 2, 4, 6, 8, 10, 12, 14, 15])

# Моделирование промежуточных значений напряжения и тока до критической точки
voltage = np.linspace(5.10, v_15, len(distance))
current = np.linspace(0.55, i_15, len(distance))

# Расчет выходных параметров и КПД по формулам
p_out = voltage * current
efficiency = (p_out / P_in) * 100

# Создание таблицы данных
df = pd.DataFrame({
    'Расстояние (мм)': distance,
    'Выходное напряжение U_out (В)': np.round(voltage, 2),
    'Выходной ток I_out (А)': np.round(current, 2),
    'Выходная мощность P_out (Вт)': np.round(p_out, 2),
    'КПД системы (%)': np.round(efficiency, 1)
})

# Отображение таблицы расчетов
st.markdown("### Результаты расчетов эффективности")
st.dataframe(df, use_container_width=True)

# Построение графика зависимости КПД от расстояния
st.markdown("### График зависимости КПД от осевого расстояния")

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

# Линия КПД
ax.plot(distance, efficiency, color='#d62728', marker='o', linewidth=2.5, label='КПД (%)')
ax.fill_between(distance, efficiency - 1.0, efficiency + 1.0, color='#d62728', alpha=0.1)

# Настройки координатной сетки
ax.set_xlabel('Расстояние между центрами катушек (мм)', fontsize=10)
ax.set_ylabel('Коэффициент полезного действия (%)', fontsize=10)
ax.set_xlim(0, 16)
ax.set_ylim(0, 35)  # Ограничение оси Y для наглядности (макс КПД около 28%)
ax.grid(True, linestyle='--', alpha=0.5)

# Индикация критической точки
ax.axvline(x=15, color='gray', linestyle=':', alpha=0.7, linewidth=1.5)
ax.text(14.8, 2, 'Предельное расстояние (15 мм)', color='gray', rotation=90, va='bottom', ha='right', fontsize=9)

plt.title('Кривая изменения эффективности энергопередачи (КПД)', fontsize=11, pad=15)
plt.tight_layout()

# Вывод графика на страницу
st.pyplot(fig)
