import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Заголовок сайта
st.title("⚡ ИТ-Мониторинг системы «Wireless Biopower»")
st.write("Введите данные эксперимента слева, чтобы сайт автоматически перестроил графики.")

# 2. Боковая панель для ввода данных (Слайдеры и окошки)
st.sidebar.header("⚙️ Ввод параметров эксперимента")

# Создаем интерактивные ползунки для критической точки (15 мм)
st.sidebar.subheader("Данные на расстоянии 15 мм:")
v_15 = st.sidebar.slider("Напряжение в крит. точке (В)", 3.5, 5.5, 4.42, step=0.01)
i_15 = st.sidebar.slider("Сила тока в крит. точке (А)", 0.05, 0.6, 0.15, step=0.01)

# 3. Формируем таблицу на основе введенных данных
distance = np.array([1, 2, 4, 6, 8, 10, 12, 14, 15])
# Рассчитываем плавное падение до той точки, которую ввел пользователь
voltage = np.linspace(5.10, v_15, len(distance))
current = np.linspace(0.55, i_15, len(distance))

df = pd.DataFrame({
    'Расстояние (мм)': distance,
    'Напряжение (В)': np.round(voltage, 2),
    'Сила тока (А)': np.round(current, 2),
    'Мощность (Вт)': np.round(voltage * current, 2)
})

# Отображаем интерактивную таблицу на сайте
st.subheader("📊 Текущие измерения")
st.dataframe(df, use_container_width=True)

# 4. Строим интерактивный график (тот самый, с двумя осями)
st.subheader("📈 Выходные характеристики")

fig, ax1 = plt.subplots(figsize=(8, 4.5))

color = '#1f77b4'
ax1.set_xlabel('Расстояние между катушками (мм)')
ax1.set_ylabel('Выходное напряжение (В)', color=color)
ax1.plot(distance, voltage, color=color, marker='o', linewidth=2.5)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(3.5, 5.5)
ax1.grid(True, linestyle='--', alpha=0.5)

ax2 = ax1.twinx()  
color = '#ff7f0e'
ax2.set_ylabel('Сила тока (А)', color=color)
ax2.plot(distance, current, color=color, marker='s', linestyle='--', linewidth=2.5)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(0, 0.7)

plt.tight_layout()

# Выводим график прямо на страницу сайта!
st.pyplot(fig)
