import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Настройка страницы
st.set_page_config(page_title="Wireless Biopower - Расчет КПД", layout="centered")

st.title("Аналитическая система расчета КПД беспроводной зарядки")
st.write("Программа автоматического моделирования КПД прототипа «Wireless Biopower» на основе осевого расстояния и радиального смещения.")

# Параметры источника питания (Блок питания 5В, 2А)
U_in = 5.0
st.markdown("### Параметры первичного контура (Блок питания: 5В, 2А)")

# -------------------------------------------------------------------------
# ЭКСПЕРИМЕНТ 1: Вертикальное расстояние (У)
# -------------------------------------------------------------------------
st.markdown("---")
st.markdown("## 1. Исследование осевого расстояния (по оси "У")
st.write("Катушки находятся строго друг напротив друга, изменяется расстояние между ними.")

# Настройки критической точки Z в сайдбаре
st.sidebar.header("Параметры осевого зазора (Z)")
v_15_z = st.sidebar.slider("Напряжение на 15 мм (В)", 3.5, 5.5, 4.42, step=0.01)
i_15_z = st.sidebar.slider("Ток на 15 мм (А)", 0.05, 0.6, 0.15, step=0.01)

distance_z = np.array([1, 2, 4, 6, 8, 10, 12, 14, 15])

# Моделируем реальный потребляемый ток от БП (падающий с расстоянием)
input_current_z = np.linspace(1.00, 0.45, len(distance_z))
p_in_z = U_in * input_current_z

# Выходные параметры контура Z
voltage_z = np.linspace(5.10, v_15_z, len(distance_z))
current_z = np.linspace(0.55, i_15_z, len(distance_z))
p_out_z = voltage_z * current_z
efficiency_z = (p_out_z / p_in_z) * 100

# Таблица 1
df_z = pd.DataFrame({
    'Расстояние Z (мм)': distance_z,
    'Выходное напряжение U (В)': np.round(voltage_z, 2),
    'Выходной ток I (А)': np.round(current_z, 2),
    'КПД контура (%)': np.round(efficiency_z, 1)
})
st.dataframe(df_z, use_container_width=True)

# График 1
fig1, ax1 = plt.subplots(figsize=(8, 4), dpi=300)
ax1.plot(distance_z, efficiency_z, color='#d62728', marker='o', linewidth=2.5, label='КПД (%)')
ax1.fill_between(distance_z, efficiency_z - 1.0, efficiency_z + 1.0, color='#d62728', alpha=0.1)
ax1.set_xlabel('Осевое расстояние между катушками Z (мм)')
ax1.set_ylabel('КПД системы (%)')
ax1.set_xlim(0, 16)
ax1.set_ylim(0, 65)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.axvline(x=15, color='gray', linestyle=':', alpha=0.7)
plt.title('Зависимость КПД от осевого расстояния (Z)', fontsize=11)
st.pyplot(fig1)


# -------------------------------------------------------------------------
# ЭКСПЕРИМЕНТ 2: Горизонтальное смещение (Х)
# -------------------------------------------------------------------------
st.markdown("---")
st.markdown("## 2. Исследование горизонтального смещения (по оси Х)")
st.write("Расстояние между катушками фиксировано (1 мм). Изменяется сдвиг между их центрами.")

# Настройки критической точки Y в сайдбаре
st.sidebar.header("Параметры смещения (Y)")
v_10_y = st.sidebar.slider("Напряжение при сдвиге 10 мм (В)", 3.5, 5.5, 4.35, step=0.01)
i_10_y = st.sidebar.slider("Ток при сдвиге 10 мм (А)", 0.05, 0.6, 0.11, step=0.01)

displacement_y = np.array([-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10])

# Моделируем реальный ток от БП для смещения (максимум в центре, падает к краям)
input_current_y = np.array([0.40, 0.55, 0.75, 0.90, 0.98, 1.00, 0.98, 0.90, 0.75, 0.55, 0.40])
p_in_y = U_in * input_current_y

# Выходные параметры контура Y (симметричное распределение Гаусса)
voltage_y = np.array([v_10_y, 4.52, 4.78, 4.95, 5.05, 5.10, 5.05, 4.95, 4.78, 4.52, v_10_y])
current_y = np.array([i_10_y, 0.22, 0.36, 0.48, 0.53, 0.55, 0.53, 0.48, 0.36, 0.22, i_10_y])
p_out_y = voltage_y * current_y
efficiency_y = (p_out_y / p_in_y) * 100

# Таблица 2
df_y = pd.DataFrame({
    'Смещение по оси Y (мм)': displacement_y,
    'Выходное напряжение U (В)': np.round(voltage_y, 2),
    'Выходной ток I (А)': np.round(current_y, 2),
    'КПД контура (%)': np.round(efficiency_y, 1)
})
st.dataframe(df_y, use_container_width=True)

# График 2
fig2, ax2 = plt.subplots(figsize=(8, 4), dpi=300)
ax2.plot(displacement_y, efficiency_y, color='#2ca02c', marker='s', linewidth=2.5, label='КПД (%)')
ax2.fill_between(displacement_y, efficiency_y - 1.0, efficiency_y + 1.0, color='#2ca02c', alpha=0.1)
ax2.set_xlabel('Радиальное смещение от центра по оси Y (мм)')
ax2.set_ylabel('КПД системы (%)')
ax2.set_xlim(-11, 11)
ax2.set_ylim(0, 65)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.axvline(x=0, color='gray', linestyle=':', alpha=0.5)
plt.title('Зависимость КПД от радиального смещения по оси Y', fontsize=11)
st.pyplot(fig2)
