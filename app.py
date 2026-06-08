import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Заголовок сайта (без эмодзи)
st.title("Wireless Biopower")
st.write("Введите данные эксперимента слева, чтобы сайт автоматически перестроил графики.")

# 2. Боковая панель для ввода данных
st.sidebar.header("Ввод параметров эксперимента")

# Блок входных значений (от блока питания / генератора)
st.sidebar.subheader("Входные параметры (Источник):")
u_in = st.sidebar.number_input("Входное напряжение U_in (В)", min_value=5.0, max_value=12.0, value=5.0, step=0.1)
i_in = st.sidebar.number_input("Входная сила тока I_in (А)", min_value=0.5, max_value=2.0, value=1.0, step=0.05)

# Расчет входной мощности
p_in = u_in * i_in

# Блок выходных критических значений на 15 мм
st.sidebar.subheader("Выходные параметры на расстоянии 15 мм:")
v_15 = st.sidebar.slider("Напряжение в крит. точке (В)", 3.5, 5.5, 4.42, step=0.01)
i_15 = st.sidebar.slider("Сила тока в крит. точке (А)", 0.05, 0.6, 0.15, step=0.01)

# 3. Расчет экспериментальной таблицы данных
distance = np.array([1, 2, 4, 6, 8, 10, 12, 14, 15])

# Моделируем распределение напряжения и тока до критической точки
voltage = np.linspace(5.10, v_15, len(distance))
current = np.linspace(0.55, i_15, len(distance))

# Автоматический расчет Мощности и КПД
p_out = voltage * current
efficiency = (p_out / p_in) * 100

# Создаем датафрейм для отображения
df = pd.DataFrame({
    'Расстояние (мм)': distance,
    'Напряжение U_out (В)': np.round(voltage, 2),
    'Сила тока I_out (А)': np.round(current, 2),
    'Выходная мощность P_out (Вт)': np.round(p_out, 2),
    'КПД (%)': np.round(efficiency, 1)
})

# Отображаем входную мощность для справки
st.info(f"Входная мощность системы (P_in): {p_in:.2f} Вт")

# Отображаем таблицу данных
st.subheader("Результаты измерений и автоматических расчетов")
st.dataframe(df, use_container_width=True)

# 4. Построение графика зависимости Выходной мощности от Расстояния
st.subheader("График зависимости выходной мощности от расстояния")

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

# Строим линию мощности
ax.plot(distance, p_out, color='#2ca02c', marker='g', linewidth=2.5, label='Выходная мощность (Вт)')
ax.fill_between(distance, p_out - 0.05, p_out + 0.05, color='#2ca02c', alpha=0.1)

# Настройка осей и сетки
ax.set_xlabel('Расстояние между катушками (мм)', fontsize=10)
ax.set_ylabel('Выходная мощность P_out (Вт)', fontsize=10)
ax.set_xlim(0, 16)
ax.set_ylim(0, max(p_out) + 0.5)
ax.grid(True, linestyle='--', alpha=0.5)

# Вертикальная черта критической точки
ax.axvline(x=15, color='red', linestyle=':', alpha=0.7, linewidth=1.5)
ax.text(14.8, 0.2, 'Критическая точка (15 мм)', color='red', rotation=90, va='bottom', ha='right', fontsize=9)

plt.title('Зависимость передаваемой мощности от осевого зазора катушек', fontsize=11, pad=15)
plt.tight_layout()

# Выводим график на сайт
st.pyplot(fig)
