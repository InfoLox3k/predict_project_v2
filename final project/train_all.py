from ai_code import Sequential, DenseLayer
import numpy as np
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from my_database import DB_CONFIG

np.random.seed(42)
n_samples = 2000

x_raw = np.zeros((n_samples, 5))
x_raw[:, 0] = np.random.uniform(0, 365, n_samples)
x_raw[:, 1] = np.random.randint(1, 601, n_samples)
x_raw[:, 2] = np.random.randint(-50, 151, n_samples)
x_raw[:, 3] = np.random.uniform(0.1, 50, n_samples)
x_raw[:, 4] = np.random.uniform(0, 25, n_samples)

# Целевая переменная (осталось дней до ремонта)
np.random.seed(42)
y_raw = (350
         - (x_raw[:, 0] * 0.35)  # Дни эксплуатации: чем больше, тем меньше осталось
         - (x_raw[:, 1] * 0.25)  # Пробег/нагрузка: аналогично
         - (x_raw[:, 3] * 0.4)  # Давление/расход: выше стресс → быстрее износ
         - (x_raw[:, 4] * 0.5)  # Вибрация: прямой деградирующий фактор
         + (x_raw[:, 2] * 0.03)  # Температура: малый эффект (оптимальный диапазон ~0)
         + np.random.normal(0, 15, n_samples))
y_raw = np.maximum(y_raw, 5).reshape(-1, 1)

# Нормализация. mean(axis=0)-ср.арифм. по столбцам, std()- стандартное отклонение.
X_mean, X_std = x_raw.mean(axis=0), x_raw.std(axis=0)
y_mean, y_std = y_raw.mean(), y_raw.std()

x_train = (x_raw - X_mean) / X_std
y_train = (y_raw - y_mean) / y_std

model = Sequential()
# model.add(DenseLayer(units=1024, activation='relu', input_dim=5))
# model.add(DenseLayer(units=512, activation='relu'))
model.add(DenseLayer(units=64, activation='relu', input_dim=5))
model.add(DenseLayer(units=32, activation='relu'))
model.add(DenseLayer(units=16, activation='relu'))
model.add(DenseLayer(units=1, activation='linear'))  # ⚠️ Регрессия: 1 выход, linear

def fit_2(epoch):

    print("🚀 Начинаю обучение модели...")
    model, scaler = Sequential.load('machine_model.npz')
    X_mean, X_std = scaler['X_mean'], scaler['X_std']
    y_mean, y_std = scaler['y_mean'], scaler['y_std']

    # ✅ Дообучаем ещё 500 эпох с уменьшенным LR
    model.fit(x_train, y_train, epochs=epoch, learning_rate=0.001, verbose=1)

    # 💾 Пересохраняем обновлённые веса
    model.save('machine_model.npz', X_mean, X_std, y_mean, y_std)

import os

def calculate():
    try:
        if not os.path.exists('machine_model.npz'):
            print("⚠️ machine_model.npz не найден. Сначала обучите модель.")
            return None

        with np.load('machine_model.npz', allow_pickle=True) as data:
            # 📊 X_mean и X_std остаются МАССИВАМИ (shape: (5,))
            X_mean = np.asarray(data['X_mean'], dtype=np.float64)
            X_std = np.asarray(data['X_std'], dtype=np.float64)

            # 🎯 y_mean и y_std приводятся к СКАЛЯРАМ (float)
            y_mean = float(np.squeeze(data['y_mean']))
            y_std = float(np.squeeze(data['y_std']))

        print(f"📊 Статистика загружена: y_mean={y_mean:.2f}, y_std={y_std:.2f}")

        # 🤖 Загрузка весов модели
        model, _ = Sequential.load('machine_model.npz')

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT id, today_date, fix_out, current, temperature, vibration, pressure FROM machines")
        rows = cursor.fetchall()

        if not rows:
            print("В таблице machines нет записей.")
            return 'nnnn'

        results = []
        for row in rows:
            machine_id, today_str, fix_out_str, current, temp, vibration, pressure = row
            if fix_out_str is None:
                continue

            try:
                d1 = datetime.strptime(str(today_str), "%Y-%m-%d")
                d2 = datetime.strptime(str(fix_out_str), "%Y-%m-%d")
                days_since = abs((d1 - d2).days)
            except ValueError:
                continue

            # 📥 Формируем входной вектор (1, 5)
            X_input = np.array([[days_since, current, temp, vibration, pressure]], dtype=np.float64)

            # 🔄 Нормализация (broadcasting: (1,5) - (5,) -> (1,5))
            X_norm = (X_input - X_mean) / X_std

            # 🤖 Предсказание
            pred_norm = model.predict(X_norm)[0][0]

            if pred_norm is None or np.isnan(pred_norm):
                pred_real = 5
            else:
                # 📤 Денормализация (скаляры!)
                pred_real = int(round(pred_norm * y_std + y_mean))
                pred_real = max(5, pred_real)

            cursor.execute(
                "UPDATE machines SET predicted_days_until_fix = %s WHERE id = %s",
                (pred_real, machine_id)
            )
            results.append({"id": machine_id, "predicted_days": pred_real})
            print(f"✅ Устройство {machine_id}: прогноз {pred_real} дн.")

        conn.commit()
        return results

    except Exception as e:
        print(f"❌ Ошибка в calculate: {e}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals() and conn.is_connected():
            conn.rollback()
        return None
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()
        print("🔌 Соединение с БД закрыто.")

def calculate_wrong():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # ✅ Забираем все 5 признаков
        cursor.execute("""
            SELECT id, today_date, fix_out, current, temperature, vibration, pressure 
            FROM machines
        """)
        rows = cursor.fetchall()

        if not rows:
            print("В таблице machines нет записей.")
            return 'nnnn'

        results = []
        for row in rows:
            machine_id, today_str, fix_out_str, current, temp, vibration, pressure = row

            if fix_out_str is None:
                continue

            try:
                d1 = datetime.strptime(str(today_str), "%Y-%m-%d")
                d2 = datetime.strptime(str(fix_out_str), "%Y-%m-%d")
                days_since = abs((d1 - d2).days)
            except ValueError:
                continue

            # [дни, ток, температура, вибрация, давление]
            X_input = np.array([[days_since, current, temp, vibration, pressure]])

            X_norm = (X_input - X_mean) / X_std
            pred_norm = model.predict(X_norm)[0][0]
            pred_real = max(1, int(pred_norm * y_std + y_mean))

            cursor.execute(
                "UPDATE machines SET predicted_days_until_fix = %s WHERE id = %s",
                (pred_real, machine_id)
            )
            results.append({"id": machine_id, "predicted_days": pred_real})
            print(f"Устройство {machine_id}: прогноз {pred_real} дн.")

        conn.commit()
        return results

    except Exception as e:
        print(f"Ошибка в calculate: {e}")
        if 'conn' in locals(): conn.rollback()
        return None
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()
        print("🔌 Соединение с БД закрыто.")
