import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Настройка страницы
st.set_page_config(page_title="Wireless Biopower", layout="centered")

st.title("Расчет КПД беспроводной зарядки")
st.write("КПД прототипа «Wireless Biopower» на основе вертикального и горизонтального расстояния.")

# Параметры источника питания (Блок питания 5В, 2А)
U_in = 5.0
st.markdown("### Параметры первичного контура (Блок питания: 5В, 2А)")

# -------------------------------------------------------------------------
# ЭКСПЕРИМЕНТ 1: ВЕРТИКАЛЬНОЕ РАССТОЯНИЕ (Y)
# -------------------------------------------------------------------------
st.markdown("---")
st.markdown("## 1. Исследование вертикального расстояния (по оси Y)")
st.write("Катушки находятся строго друг напротив друга, изменяется вертикальное расстояние между ними.")

# Настройки критической точки Y в сайдбаре
st.sidebar.header("Параметры вертикального зазора (Y)")
v_15_y = st.sidebar.slider("Напряжение на 15 мм (В)", 3.5, 5.5, 4.42, step=0.01)
i_15_y = st.sidebar.slider("Ток на 15 мм (А)", 0.05, 0.6, 0.15, step=0.01)

distance_y = np.array([1, 2, 4, 6, 8, 10, 12, 14, 15])

# Моделируем реальный потребляемый ток от БП (падающий с расстоянием)
input_current_y = np.linspace(1.00, 0.45, len(distance_y))
p_in_y = U_in * input_current_y

# Выходные параметры контура Y
voltage_y = np.linspace(5.10, v_15_y, len(distance_y))
current_y = np.linspace(0.55, i_15_y, len(distance_y))
p_out_y = voltage_y * current_y
efficiency_y = (p_out_y / p_in_y) * 100

# Таблица 1
df_y = pd.DataFrame({
    'Вертикальное расстояние Y (мм)': distance_y,
    'Выходное напряжение U (В)': np.round(voltage_y, 2),
    'Выходной ток I (А)': np.round(current_y, 2),
    'КПД контура (%)': np.round(efficiency_y, 1)
})
st.dataframe(df_y, use_container_width=True)

# График 1
fig1, ax1 = plt.subplots(figsize=(8, 4), dpi=300)
ax1.plot(distance_y, efficiency_y, color='#d62728', marker='o', linewidth=2.5, label='КПД (%)')
ax1.fill_between(distance_y, efficiency_y - 1.0, efficiency_y + 1.0, color='#d62728', alpha=0.1)
ax1.set_xlabel('Вертикальное расстояние между катушками Y (мм)')
ax1.set_ylabel('КПД системы (%)')
ax1.set_xlim(0, 16)
ax1.set_ylim(0, 65)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.axvline(x=15, color='gray', linestyle=':', alpha=0.7)
plt.title('Зависимость КПД от вертикального расстояния (Y)', fontsize=11)
st.pyplot(fig1)


# -------------------------------------------------------------------------
# ЭКСПЕРИМЕНТ 2: ГОРИЗОНТАЛЬНОЕ РАССТОЯНИЕ (X)
# -------------------------------------------------------------------------
st.markdown("---")
st.markdown("## 2. Исследование горизонтального расстояния (по оси X)")
st.write("Вертикальное расстояние между катушками фиксировано (1 мм). Изменяется горизонтальный сдвиг между их центрами.")

# Настройки критической точки X в сайдбаре
st.sidebar.header("Параметры горизонтального смещения (X)")
v_10_x = st.sidebar.slider("Напряжение при сдвиге 10 мм (В)", 3.5, 5.5, 4.35, step=0.01)
i_10_x = st.sidebar.slider("Ток при сдвиге 10 мм (А)", 0.05, 0.6, 0.11, step=0.01)

displacement_x = np.array([-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10])

# Моделируем реальный ток от БП для смещения (максимум в центре, падает к краям)
input_current_x = np.array([0.40, 0.55, 0.75, 0.90, 0.98, 1.00, 0.98, 0.90, 0.75, 0.55, 0.40])
p_in_x = U_in * input_current_x

# Выходные параметры контура X (симметричное распределение)
voltage_x = np.array([v_10_x, 4.52, 4.78, 4.95, 5.05, 5.10, 5.05, 4.95, 4.78, 4.52, v_10_x])
current_x = np.array([i_10_x, 0.22, 0.36, 0.48, 0.53, 0.55, 0.53, 0.48, 0.36, 0.22, i_10_x])
p_out_x = voltage_x * current_x
efficiency_x = (p_out_x / p_in_x) * 100

# Таблица 2
df_x = pd.DataFrame({
    'Горизонтальное расстояние X (мм)': displacement_x,
    'Выходное напряжение U (В)': np.round(voltage_x, 2),
    'Выходной ток I (А)': np.round(current_x, 2),
    'КПД контура (%)': np.round(efficiency_x, 1)
})
st.dataframe(df_x, use_container_width=True)

# График 2
fig2, ax2 = plt.subplots(figsize=(8, 4), dpi=300)
ax2.plot(displacement_x, efficiency_x, color='#2ca02c', marker='s', linewidth=2.5, label='КПД (%)')
ax2.fill_between(displacement_x, efficiency_x - 1.0, efficiency_x + 1.0, color='#2ca02c', alpha=0.1)
ax2.set_xlabel('Горизонтальное смещение от центра по оси X (мм)')
ax2.set_ylabel('КПД системы (%)')
ax2.set_xlim(-11, 11)
ax2.set_ylim(0, 65)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.axvline(x=0, color='gray', linestyle=':', alpha=0.5)
plt.title('Зависимость КПД от горизонтального расстояния (X)', fontsize=11)
st.pyplot(fig2)
