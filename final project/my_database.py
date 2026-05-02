import mysql.connector
from mysql.connector import Error
from datetime import date

DB_CONFIG = {
    'host': 'DESKTOP-B0A23CQ',
    'database': 'my_new_project_db',
    'user': 'admin1',
    'password': 'LOLpassWoRD45'
}
connection = None

def set_table():
    try:
        # 1️⃣ Подключение к MySQL
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Есть контакт")

        cursor = connection.cursor()

        cursor.execute("DROP TABLE machines")
        create_table = """
        CREATE TABLE IF NOT EXISTS machines (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            fix_out DATE,
            today_date DATE,
            action TEXT,
            current INT,
            temperature INT,
            vibration INT,
            pressure INT,
            predicted_days_until_fix INT
        )
        """
        cursor.execute(create_table)
        print("📦 Таблица 'machines' готова.")

        examples(cursor, connection)

    except Error as e:
        print(f"❌ Ошибка работы с MySQL: {e}")
        if connection:
            connection.rollback()  # Откат изменений при ошибке

    finally:
        # 7️⃣ Закрытие соединения
        if 'cursor' in locals():
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("\n🔌 Соединение с базой закрыто.")


def examples(cursor, connection):
    data = [
        ("Очистной комбайн KSW-460NE", "comb-001", date(2023, 3, 5), date.today(),
         "Замена контроллера, замена блока управления радио", 5, 160, 10, 5),
        ("Ленточный конвейер КЛКТ-1200", "conv-001", date(2023, 1, 6), date.today(),
         "Произвести аварийно-восстановительный ремонт...", 4, 45, 8, 4),
        ("Проходческий комбайн КП-21Д", "comb-001", date(2023, 4, 12), date.today(),
         "Произвести замену кабельной перемычки", 2, 30, 5, 3),
        ("Высоковольтные кабели", "comb-001", date(2023, 8, 13), date.today(),
         "Перемонтаж и ремонт кабельных линий...", 3, 40, 7, 4)
    ]

    sql = """INSERT INTO machines 
             (name, type, fix_out, today_date, action, current, temperature, vibration, pressure) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor.executemany(sql, data)
    connection.commit()
    print(f"Вставлено {len(data)} записей в таблицу 'machines'.")
