import flet as ft
from datetime import datetime, timedelta

from ai_code import Sequential

# ---------- Цветовые константы (HEX) ----------
COLOR_RED = "#ef4444"
COLOR_ORANGE = "#f97316"
COLOR_AMBER = "#eab308"
COLOR_GREEN = "#22c55e"
COLOR_GREY = "#9ca3af"
COLOR_BLUE = "#3b82f6"
COLOR_WHITE = "#ffffff"
COLOR_WHITE70 = "#B3ffffff"
COLOR_WHITE54 = "#8Affffff"
COLOR_WHITE38 = "#61ffffff"
COLOR_CARD_BG = "#161B22"
COLOR_BG = "#0D1117"

# ---------- Модели данных ----------
class Sensor:
    def __init__(self, id, name, value, unit, status, normal_th, warn_th, crit_th, last_update):
        self.id = id
        self.name = name
        self.value = value
        self.unit = unit
        self.status = status
        self.normal = normal_th
        self.warning = warn_th
        self.critical = crit_th
        self.last_update = last_update

class Forecast:
    def __init__(self, id, node_name, defect, probability, hours_left, shifts_left, recommendation, created, acknowledged):
        self.id = id
        self.node_name = node_name
        self.defect = defect
        self.probability = probability
        self.hours_left = hours_left
        self.shifts_left = shifts_left
        self.recommendation = recommendation
        self.created = created
        self.acknowledged = acknowledged

class Equipment:
    def __init__(self, id, name, inv_num, etype, status, sector, gateway, last_conn, sensors, forecasts):
        self.id = id
        self.name = name
        self.inv_num = inv_num
        self.type = etype
        self.status = status
        self.sector = sector
        self.gateway = gateway
        self.last_conn = last_conn
        self.sensors = sensors
        self.forecasts = forecasts

class Event:
    def __init__(self, id, equip_id, equip_name, etype, severity, message, timestamp, acknowledged, ack_by=None, ack_at=None):
        self.id = id
        self.equip_id = equip_id
        self.equip_name = equip_name
        self.type = etype
        self.severity = severity
        self.message = message
        self.timestamp = timestamp
        self.acknowledged = acknowledged
        self.ack_by = ack_by
        self.ack_at = ack_at

class Part:
    def __init__(self, id, name, part_number, category, manufacturer, description, specs, compat_equip, price, stock, status, lead_time, warranty):
        self.id = id
        self.name = name
        self.part_number = part_number
        self.category = category
        self.manufacturer = manufacturer
        self.description = description
        self.specs = specs
        self.compat_equip = compat_equip
        self.price = price
        self.stock = stock
        self.status = status
        self.lead_time = lead_time
        self.warranty = warranty

# ---------- Тестовые данные ----------
now = datetime.now()
s1 = Sensor("s1", "Вибрация привода", 8.5, "мм/с", "critical", 4.5, 7.0, 8.0, now - timedelta(seconds=30))
s2 = Sensor("s2", "Температура двигателя", 78, "°C", "warning", 65, 75, 85, now - timedelta(seconds=30))
s3 = Sensor("s3", "Ток двигателя", 42, "А", "normal", 45, 50, 55, now - timedelta(seconds=30))
s4 = Sensor("s4", "Скорость ленты", 1.25, "м/с", "normal", 1.5, 1.8, 2.0, now - timedelta(seconds=30))
equip1 = Equipment("conv-001", "Конвейер №1 (очистной)", "INV-2023-001", "conveyor", "critical", "Участок A",
                   "iROBO-2000 Участок A", now - timedelta(seconds=30), [s1,s2,s3,s4],
                   [Forecast("f1", "Подшипник приводного барабана", "Износ наружного кольца", 87, 48, 6,
                             "Плановая замена в окно ТО", now - timedelta(hours=1), False)])

s5 = Sensor("s5", "Вибрация редуктора", 6.2, "мм/с", "warning", 5.0, 6.0, 8.0, now - timedelta(seconds=15))
s6 = Sensor("s6", "Температура масла", 58, "°C", "normal", 70, 80, 90, now - timedelta(seconds=15))
s7 = Sensor("s7", "Давление гидросистемы", 180, "бар", "normal", 200, 220, 240, now - timedelta(seconds=15))
equip2 = Equipment("comb-001", "Комбайн КШ-3МУ №5", "INV-2023-015", "combine", "forecast", "Участок Б",
                   "iROBO-2000 Участок Б", now - timedelta(seconds=15), [s5,s6,s7],
                   [Forecast("f2", "Редуктор исполнительного органа", "Дисбаланс вала", 65, 120, 15,
                             "Балансировка при следующем ТО", now - timedelta(hours=2), True)])

s8 = Sensor("s8", "Вибрация корпуса", 7.1, "мм/с", "warning", 5.0, 7.0, 9.0, now - timedelta(seconds=20))
s9 = Sensor("s9", "Температура подшипника", 72, "°C", "warning", 60, 70, 85, now - timedelta(seconds=20))
s10 = Sensor("s10", "Давление на выходе", 28, "бар", "normal", 35, 40, 45, now - timedelta(seconds=20))
s11 = Sensor("s11", "Расход", 285, "м³/ч", "normal", 320, 350, 380, now - timedelta(seconds=20))
equip3 = Equipment("pump-001", "Насос ЦНС-300 №12", "INV-2023-042", "pump", "warning", "Водоотлив",
                   "iROBO-2000 Водоотлив", now - timedelta(seconds=20), [s8,s9,s10,s11], [])

s15 = Sensor("s15", "Вибрация корпуса", 0, "мм/с", "offline", 5.0, 7.0, 9.0, now - timedelta(minutes=10))
s16 = Sensor("s16", "Температура подшипника", 0, "°C", "offline", 60, 70, 85, now - timedelta(minutes=10))
equip5 = Equipment("pump-002", "Насос ЦНС-300 №13", "INV-2023-043", "pump", "offline", "Водоотлив",
                   "iROBO-2000 Резерв", now - timedelta(minutes=10), [s15,s16], [])

mock_equipment = [equip1, equip2, equip3, equip5]

mock_events = [
    Event("e1", "conv-001", "Конвейер №1 (очистной)", "alarm", "critical",
          "Критический уровень вибрации привода (8.5 мм/с)", now - timedelta(seconds=30), False),
    Event("e2", "conv-001", "Конвейер №1 (очистной)", "forecast", "warning",
          "Прогноз отказа: Подшипник приводного барабана (87%, 48 часов)", now - timedelta(hours=1), False),
    Event("e3", "pump-001", "Насос ЦНС-300 №12", "warning", "warning",
          "Превышен порог вибрации корпуса (7.1 мм/с)", now - timedelta(minutes=2), False),
    Event("e4", "comb-001", "Комбайн КШ-3МУ №5", "user_action", "info",
          "Прогноз подтверждён диспетчером", now - timedelta(hours=2), True, "Иванов И.И.", now - timedelta(hours=2)),
    Event("e5", "pump-002", "Насос ЦНС-300 №13", "alarm", "critical",
          "Потеря связи с оборудованием", now - timedelta(minutes=10), False),
    # Event("")
]


import mysql.connector
from mysql.connector import Error
from my_database import DB_CONFIG
import numpy as np


def predict_one(X_input, X_mean, X_std, y_mean, y_std, model):
    """Безопасный инференс для одной записи."""
    try:
        X_norm = (X_input - X_mean) / X_std
        pred_norm = model.predict(X_norm)[0][0]
        if pred_norm is None or np.isnan(pred_norm):
            return 5
        return max(5, int(round(pred_norm * y_std + y_mean)))
    except Exception:
        return 5

def refresh_events():
    global mock_events
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, type, today_date, fix_out, current, temperature, vibration, pressure 
            FROM machines
        """)
        rows = cursor.fetchall()

        if not rows:
            mock_events = []
            print("⚠️ Нет записей в machines")
            return

        with np.load('machine_model.npz', allow_pickle=True) as data:
            X_mean = np.asarray(data['X_mean'], dtype=np.float64)
            X_std  = np.asarray(data['X_std'], dtype=np.float64)
            y_mean = float(np.squeeze(data['y_mean']))
            y_std  = float(np.squeeze(data['y_std']))
        model, _ = Sequential.load('machine_model.npz')

        mock_events = []
        now = datetime.now()

        for row in rows:
            machine_id, machine_name, machine_type, today_str, fix_out_str, current, temp, vibration, pressure = row
            if fix_out_str is None: continue

            try:
                d1 = datetime.strptime(str(today_str), "%Y-%m-%d")
                d2 = datetime.strptime(str(fix_out_str), "%Y-%m-%d")
                days_since = abs((d1 - d2).days)
            except ValueError: continue

            X_input = np.array([[days_since, current, temp, vibration, pressure]], dtype=np.float64)
            pred_days = predict_one(X_input, X_mean, X_std, y_mean, y_std, model)
            base_id = f"e{machine_id}"

            # 1. КРИТИЧЕСКИЕ (Alarm / Critical)
            if vibration > 7.0:
                mock_events.append(Event(
                    f"{base_id}_vib", machine_id, machine_name,
                    "alarm", "critical",
                    f"Критический уровень вибрации привода ({vibration:.1f} мм/с)",
                    now - timedelta(seconds=30), False))
            elif temp > 120 or temp < -30:
                mock_events.append(Event(
                    f"{base_id}_temp", machine_id, machine_name,
                    "alarm", "critical",
                    f"Критическая температура подшипника ({temp:.1f}°C)",
                    now - timedelta(seconds=45), False))
            elif current > 550:
                mock_events.append(Event(
                    f"{base_id}_cur", machine_id, machine_name,
                    "alarm", "critical",
                    f"Перегрузка электродвигателя (ток {current:.1f} А)",
                    now - timedelta(seconds=60), False))
            elif pressure > 20:
                mock_events.append(Event(
                    f"{base_id}_press", machine_id, machine_name,
                    "alarm", "critical",
                    f"Аварийное давление в системе ({pressure:.1f} атм)",
                    now - timedelta(seconds=90), False))

            # 2. ПРЕДУПРЕЖДЕНИЯ (Warning)
            elif vibration > 5.0:
                mock_events.append(Event(
                    f"{base_id}_vib_w", machine_id, machine_name,
                    "warning", "warning",
                    f"Превышен порог вибрации корпуса ({vibration:.1f} мм/с)",
                    now - timedelta(minutes=2), False))
            elif temp > 90:
                mock_events.append(Event(
                    f"{base_id}_temp_w", machine_id, machine_name,
                    "warning", "warning",
                    f"Повышенная температура двигателя ({temp:.1f}°C)",
                    now - timedelta(minutes=5), False))
            elif current > 450:
                mock_events.append(Event(
                    f"{base_id}_cur_w", machine_id, machine_name,
                    "warning", "warning",
                    f"Высокий рабочий ток ({current:.1f} А)",
                    now - timedelta(minutes=3), False))

            # 3. ПРОГНОЗ ИИ (Forecast)
            if pred_days <= 14:
                severity = "critical" if pred_days <= 7 else "warning"
                confidence = int(100 - (pred_days / 14) * 40)
                mock_events.append(Event(
                    f"{base_id}_fc", machine_id, machine_name,
                    "forecast", severity,
                    f"Прогноз отказа: {machine_name} (вероятность {confidence}%, ~{int(pred_days)} дней)",
                    now - timedelta(hours=1), False))

                if pred_days <= 5:
                    mock_events.append(Event(
                        f"{base_id}_ack", machine_id, machine_name,
                        "user_action", "info",
                        f"Прогноз подтверждён диспетчером для {machine_name}",
                        now - timedelta(hours=2), True, "Иванов И.И.", now - timedelta(hours=2)))
            elif not any(ev.id.startswith(f"{base_id}_") for ev in mock_events):
                mock_events.append(Event(
                    f"{base_id}_ok", machine_id, machine_name,
                    "info", "info",
                    f"Оборудование в штатном режиме. Данные обновлены.",
                    now - timedelta(minutes=10), False))

        print(f"✅ Сгенерировано {len(mock_events)} событий")

    except Exception as e:
        print(f"❌ Ошибка в refresh_events: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if conn and conn.is_connected():
            conn.close()

mock_parts = [
    Part("part-001", "Подшипник радиальный 6320", "SKF-6320-C3", "bearing", "SKF",
         "Радиальный шариковый подшипник", {"Внутр. диам.": "100 мм", "Нар. диам.": "215 мм"}, ["conv-001","conv-002"],
         18500, 4, "in_stock", 14, 12),
    Part("part-003", "Электродвигатель АИР 160S4", "AIR160S4-15KW", "motor", "Siemens",
         "Асинхронный двигатель 15 кВт", {"Мощность": "15 кВт", "Обороты": "1460 об/мин"}, ["conv-001","conv-002"],
         75000, 2, "in_stock", 30, 24),
    Part("part-004", "Датчик вибрации IFM VSE150", "IFM-VSE150", "sensor", "IFM Electronic",
         "Интеллектуальный датчик вибрации", {"Диапазон": "0-25 мм/с", "Выход": "4-20 мА"}, ["conv-001","pump-001","comb-001"],
         32000, 8, "in_stock", 10, 36),
    Part("part-007", "Насос центробежный ЦНС-300", "CNS-300-180", "pump", "ГидроМаш",
         "Центробежный насос", {"Произв.": "300 м³/ч", "Напор": "180 м"}, ["pump-001","pump-002"],
         450000, 0, "out_of_stock", 60, 18),
]

STATUS_COLORS = {
    "critical": COLOR_RED,
    "warning": COLOR_AMBER,
    "forecast": COLOR_ORANGE,
    "offline": COLOR_GREY,
    "normal": COLOR_GREEN,
}

# ---------- Главное приложение ----------
def main(page: ft.Page):
    page.title = "Система предиктивного мониторинга"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.bgcolor = COLOR_BG
    page.padding = 0

    current_page = ft.Ref[ft.Column]()

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=180,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Обзор"),
            ft.NavigationRailDestination(icon=ft.Icons.BUILD, label="Оборудование"),
            ft.NavigationRailDestination(icon=ft.Icons.BOOK, label="Журнал"),
            ft.NavigationRailDestination(icon=ft.Icons.FILE_PRESENT, label="Отчёты"),
            ft.NavigationRailDestination(icon=ft.Icons.SHOPPING_CART, label="Запчасти"),
            ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Настройки"),
        ],
        on_change=lambda e: switch_page(e.control.selected_index),
    )

    content_area = ft.Column(ref=current_page, expand=True, scroll=ft.ScrollMode.AUTO)

    def switch_page(index):
        views = [
            build_dashboard(),
            build_equipment_list_page(),   # Двухуровневая вкладка "Оборудование"
            build_event_log(),
            build_reports(),
            build_parts_catalog(),
            build_settings(),
        ]
        content_area.controls.clear()
        content_area.controls.append(views[index])
        page.update()

    def _stat_card(title, value, subtitle, color):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(title, size=14, color=COLOR_WHITE70),
                    ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=color),
                    ft.Text(subtitle, size=12, color=COLOR_WHITE54),
                ], spacing=4),
                padding=15,
                width=160,
            ),
            bgcolor=COLOR_CARD_BG,
            elevation=2,
        )

    # Состояния фильтров
    filter_type = "all"
    filter_status = "all"
    filter_sector = "all"

    def build_dashboard():
        nonlocal filter_type, filter_status, filter_sector

        total = len(mock_equipment)
        stats = {
            "normal": sum(1 for e in mock_equipment if e.status == "normal"),
            "warning": sum(1 for e in mock_equipment if e.status == "warning"),
            "critical": sum(1 for e in mock_equipment if e.status == "critical"),
            "forecast": sum(1 for e in mock_equipment if e.status == "forecast"),
            "offline": sum(1 for e in mock_equipment if e.status == "offline"),
        }

        stats_row = ft.Row(
            controls=[
                _stat_card("Всего", f"{total}", "единиц техники", COLOR_BLUE),
                _stat_card("Норма", f"{stats['normal']}", "в норме", COLOR_GREEN),
                _stat_card("Прогноз", f"{stats['forecast']}", "требует внимания", COLOR_ORANGE),
                _stat_card("Предупр.", f"{stats['warning']}", "контроль", COLOR_AMBER),
                _stat_card("Авария", f"{stats['critical']}", "срочно!", COLOR_RED),
                _stat_card("Нет связи", f"{stats['offline']}", "офлайн", COLOR_GREY),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        search_input = ft.TextField(
            hint_text="Поиск по названию или инвентарному номеру...",
            prefix_icon=ft.Icons.SEARCH,
            bgcolor=ft.Colors.GREY_800,
            border_radius=8,
            expand=True,
        )

        # Плашки фильтров (Container'ы, чтобы избежать проблем с кнопками)
        def make_type_pill(value, label):
            is_active = (filter_type == value)
            return ft.Container(
                content=ft.Text(label, color=COLOR_WHITE, size=14),
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                border_radius=8,
                bgcolor=COLOR_BLUE if is_active else ft.Colors.GREY_800,
                on_click=lambda e: set_filter("type", value),
                ink=True,
            )

        type_pills = ft.Row(
            controls=[
                make_type_pill("all", "Все"),
                make_type_pill("conveyor", "Конвейер"),
                make_type_pill("combine", "Комбайн"),
                make_type_pill("pump", "Насос"),
            ],
            spacing=5,
        )

        def make_status_pill(value, label):
            is_active = (filter_status == value)
            return ft.Container(
                content=ft.Text(label, color=COLOR_WHITE, size=14),
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                border_radius=8,
                bgcolor=COLOR_BLUE if is_active else ft.Colors.GREY_800,
                on_click=lambda e: set_filter("status", value),
                ink=True,
            )

        status_pills = ft.Row(
            controls=[
                make_status_pill("all", "Все"),
                make_status_pill("critical", "Авария"),
                make_status_pill("warning", "Предупреждение"),
                make_status_pill("forecast", "Прогноз"),
                make_status_pill("normal", "Норма"),
                make_status_pill("offline", "Нет связи"),
            ],
            spacing=5,
        )

        def make_sector_pill(value, label):
            is_active = (filter_sector == value)
            return ft.Container(
                content=ft.Text(label, color=COLOR_WHITE, size=14),
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                border_radius=8,
                bgcolor=COLOR_BLUE if is_active else ft.Colors.GREY_800,
                on_click=lambda e: set_filter("sector", value),
                ink=True,
            )

        sector_pills = ft.Row(
            controls=[
                make_sector_pill("all", "Все"),
                make_sector_pill("Участок A", "Участок A"),
                make_sector_pill("Участок Б", "Участок Б"),
                make_sector_pill("Водоотлив", "Водоотлив"),
            ],
            spacing=5,
        )

        equip_list = ft.ListView(expand=True, spacing=10)

        def apply_filters():
            query = search_input.value.strip().lower() if search_input.value else ""
            filtered = []
            for eq in mock_equipment:
                if query and query not in eq.name.lower() and query not in eq.inv_num.lower():
                    continue
                if filter_type != "all" and eq.type != filter_type:
                    continue
                if filter_status != "all" and eq.status != filter_status:
                    continue
                if filter_sector != "all" and eq.sector != filter_sector:
                    continue
                filtered.append(eq)

            equip_list.controls.clear()
            for eq in filtered:
                equip_list.controls.append(_equipment_card(eq))
            page.update()

        def set_filter(what, value):
            nonlocal filter_type, filter_status, filter_sector
            if what == "type":
                filter_type = value
            elif what == "status":
                filter_status = value
            elif what == "sector":
                filter_sector = value
            # Перестроить дашборд с новыми фильтрами
            content_area.controls.clear()
            content_area.controls.append(build_dashboard())
            page.update()

        search_input.on_change = lambda e: apply_filters()
        apply_filters()

        return ft.Column([
            stats_row,
            ft.Row([search_input], spacing=10),
            ft.Text("Тип:", color=COLOR_WHITE70, size=13),
            type_pills,
            ft.Text("Статус:", color=COLOR_WHITE70, size=13),
            status_pills,
            ft.Text("Участок:", color=COLOR_WHITE70, size=13),
            sector_pills,
            equip_list,
        ], spacing=10)

    def _equipment_card(eq: Equipment):
        status_color = STATUS_COLORS.get(eq.status, COLOR_GREY)

        def sensor_dots():
            if eq.status == "offline":
                return ft.Text("Все в норме", color=COLOR_GREEN, size=12)
            dots = []
            for s in eq.sensors:
                if s.status == "critical":
                    clr = COLOR_RED
                elif s.status == "warning":
                    clr = COLOR_ORANGE
                else:
                    clr = COLOR_GREEN
                dots.append(ft.Container(width=12, height=12, border_radius=6, bgcolor=clr, margin=2))
            return ft.Row(dots, wrap=True)

        forecast_text = ft.Text(f"{len(eq.forecasts)}", color=COLOR_ORANGE, size=12)

        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Container(width=6, bgcolor=status_color, border_radius=ft.BorderRadius.only(top_left=8, bottom_left=8)),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(eq.name, weight=ft.FontWeight.BOLD, color=COLOR_WHITE, expand=True),
                                ft.Container(
                                    content=ft.Text(eq.status.upper(), color=status_color, size=12),
                                    bgcolor=status_color + "33",
                                    padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                                    border_radius=12,
                                ),
                            ]),
                            ft.Row([
                                ft.Text(eq.type, color=COLOR_WHITE54, size=12),
                                ft.Text(" · ", color=COLOR_WHITE38),
                                ft.Text(eq.inv_num, color=COLOR_WHITE54, size=12),
                                ft.Text(" · ", color=COLOR_WHITE38),
                                ft.Text(eq.sector, color=COLOR_WHITE54, size=12),
                            ]),
                            ft.Row([
                                ft.Column([ft.Text("Датчики", size=11, color=COLOR_WHITE70), sensor_dots()]),
                                ft.Column([ft.Text("Прогнозы", size=11, color=COLOR_WHITE70), forecast_text]),
                                ft.Column([
                                    ft.Text("Связь", size=11, color=COLOR_WHITE70),
                                    ft.Row([
                                        ft.Icon(ft.Icons.WIFI if eq.status != "offline" else ft.Icons.WIFI_OFF, size=14,
                                                color=COLOR_GREEN if eq.status != "offline" else COLOR_GREY),
                                        ft.Text(eq.gateway, size=12, color=COLOR_WHITE70),
                                    ]),
                                    ft.Text(eq.last_conn.strftime("%H:%M:%S"), size=11, color=COLOR_WHITE38),
                                ]),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ]),
                        padding=10,
                        expand=True,
                    ),
                ]),
                padding=0,
            ),
            bgcolor=COLOR_CARD_BG,
            elevation=2,
        )

    def build_equipment_list_page():
        """Двухуровневая вкладка: список оборудования -> детали."""
        container = ft.Column(expand=True, spacing=10)

        def show_list():
            equip_list = ft.ListView(expand=True, spacing=10)
            for eq in mock_equipment:
                equip_list.controls.append(
                    ft.GestureDetector(
                        content=_equipment_card(eq),
                        on_tap=lambda e, eq=eq: show_detail(eq)
                    )
                )
            container.controls.clear()
            container.controls.append(
                ft.Column([
                    ft.Text("Оборудование", size=20, weight=ft.FontWeight.BOLD),
                    equip_list
                ], spacing=10, expand=True)
            )
            page.update()

        def show_detail(eq):
            detail_view = build_equipment_detail(eq.id)
            back_button = ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: show_list()),
                ft.Text(eq.name, size=20, weight=ft.FontWeight.BOLD),
            ])
            container.controls.clear()
            container.controls.append(
                ft.Column([
                    back_button,
                    detail_view
                ], spacing=10, expand=True)
            )
            page.update()

        show_list()
        return container

    def build_equipment_detail(equip_id):
        eq = next((e for e in mock_equipment if e.id == equip_id), mock_equipment[0])
        status_color = STATUS_COLORS.get(eq.status, COLOR_GREY)

        sensor_cards = ft.GridView(expand=True, max_extent=200, spacing=10, run_spacing=10)
        for s in eq.sensors:
            s_color = STATUS_COLORS.get(s.status, COLOR_GREY)
            sensor_cards.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(s.name, weight=ft.FontWeight.BOLD, size=14),
                            ft.Text(f"{s.value} {s.unit}", size=24, weight=ft.FontWeight.BOLD, color=s_color),
                            ft.Text(f"Норма < {s.normal}", size=12, color=COLOR_GREEN),
                            ft.Text(f"Предупр. < {s.warning}", size=12, color=COLOR_ORANGE),
                            ft.Text(f"Авария < {s.critical}", size=12, color=COLOR_RED),
                        ], spacing=4),
                        padding=10,
                    ),
                    bgcolor=COLOR_CARD_BG,
                )
            )

        forecast_cards = ft.Column(spacing=10)
        for f in eq.forecasts:
            ack_color = COLOR_GREEN if f.acknowledged else COLOR_ORANGE
            forecast_cards.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f.node_name, weight=ft.FontWeight.BOLD),
                                ft.Text("✓" if f.acknowledged else "Требует внимания", color=ack_color),
                            ]),
                            ft.Text(f"Дефект: {f.defect}", size=14),
                            ft.Text(f"Вероятность отказа: {f.probability}%", size=14, color=COLOR_RED if f.probability>=80 else COLOR_ORANGE),
                            ft.Text(f"Остаточный ресурс: {f.hours_left} ч ({f.shifts_left} смен)"),
                            ft.Text(f"Рекомендация: {f.recommendation}", size=14),
                        ], spacing=5),
                        padding=10,
                    ),
                    bgcolor=COLOR_CARD_BG,
                )
            )

        # Вкладки: Датчики / Прогнозы (график убран)
        tab_index = [0]
        tab_content = ft.Column()

        def set_tab(index):
            tab_index[0] = index
            tab_content.controls.clear()
            if index == 0:
                tab_content.controls.append(sensor_cards)
            elif index == 1:
                tab_content.controls.append(forecast_cards)
            # График удалён
            page.update()

        set_tab(0)

        tabs_row = ft.Row([
            ft.ElevatedButton("Датчики", on_click=lambda e: set_tab(0)),
            ft.ElevatedButton("Прогнозы", on_click=lambda e: set_tab(1)),
            # Кнопка "График" удалена
        ])

        return ft.Column([
            ft.Row([
                ft.Text(eq.name, size=24, weight=ft.FontWeight.BOLD),
                ft.Container(content=ft.Text(eq.status.upper(), color=status_color), bgcolor=status_color + "33", padding=5, border_radius=12),
            ]),
            ft.Text(f"{eq.inv_num} · {eq.sector}"),
            tabs_row,
            tab_content,
        ], spacing=10, expand=True)

    def build_event_log():
        refresh_events()
        events_list = ft.ListView(expand=True, spacing=10)
        for ev in mock_events:
            sev_color = {"critical": COLOR_RED, "warning": COLOR_ORANGE, "info": COLOR_BLUE}.get(ev.severity, COLOR_GREY)
            events_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(ev.equip_name, weight=ft.FontWeight.BOLD),
                                ft.Text(ev.severity.upper(), color=sev_color, size=12),
                                ft.Text("✓" if ev.acknowledged else "Новое", color=COLOR_GREEN if ev.acknowledged else COLOR_RED),
                            ]),
                            ft.Text(ev.message, size=14),
                            ft.Text(ev.timestamp.strftime("%d.%m.%Y %H:%M:%S"), size=12, color=COLOR_WHITE38),
                            ft.Row([
                                ft.ElevatedButton("Подтвердить", on_click=lambda e, ev=ev: acknowledge_event(ev))
                            ]) if not ev.acknowledged else ft.Text("Подтверждено", color=COLOR_GREEN),
                        ], spacing=5),
                        padding=10,
                    ),
                    bgcolor=COLOR_CARD_BG,
                )
            )
        return ft.Column([ft.Text("Журнал событий", size=20), events_list], spacing=10)

    def acknowledge_event(ev):
        ev.acknowledged = True
        ev.ack_by = "Иванов И.И."
        ev.ack_at = datetime.now()
        switch_page(2)

    def build_reports():
        # --- Данные для сводки ---
        total_work_hours = 156
        work_change = 5
        total_downtime_hours = 12
        downtime_percent = 7.1

        num_alarms = sum(1 for ev in mock_events if ev.severity == "critical")
        num_warnings = sum(1 for ev in mock_events if ev.severity == "warning")
        num_forecasts = sum(1 for eq in mock_equipment for f in eq.forecasts)

        alarmed_eq = list({ev.equip_name for ev in mock_events if ev.severity == "critical"})

        top_reasons = [
            ("Износ подшипников", 45),
            ("Перегрев двигателя", 25),
            ("Дисбаланс вала", 20),
            ("Прочие", 10),
        ]

        table_data = [
            {"name": "Конвейер №1 (очистной)", "type": "Конвейер", "work": 4, "downtime": 4, "alarms": 1, "warns": 1},
            {"name": "Комбайн KLI-3MU №5", "type": "Комбайн", "work": 8, "downtime": 0, "alarms": 0, "warns": 0},
            {"name": "Насос ЦНС-300 №12", "type": "Насос", "work": 1, "downtime": 7, "alarms": 0, "warns": 1},
            {"name": "Конвейер №2 (магистральный)", "type": "Конвейер", "work": 3, "downtime": 5, "alarms": 0, "warns": 0},
            {"name": "Насос ЦНС-300 №13", "type": "Насос", "work": 2, "downtime": 6, "alarms": 1, "warns": 0},
        ]

        for row in table_data:
            total_time = row["work"] + row["downtime"]
            row["ktg"] = round((row["work"] / total_time * 100), 1) if total_time else 0

        # --- Виджеты ---
        def stat_card(title, value, subtitle, value_color=COLOR_WHITE):
            return ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(title, size=14, color=COLOR_WHITE70),
                        ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=value_color),
                        ft.Text(subtitle, size=12, color=COLOR_WHITE54),
                    ], spacing=4),
                    padding=20,
                    width=250,
                ),
                bgcolor=COLOR_CARD_BG,
                elevation=2,
            )

        header_row = ft.Row([
            stat_card("Время работы", f"{total_work_hours} ч", f"≈ {work_change}% к предыдущей смене", COLOR_BLUE),
            stat_card("Простои", f"{total_downtime_hours} ч", f"≈ {downtime_percent}% от времени", COLOR_ORANGE),
        ], spacing=15, scroll=ft.ScrollMode.AUTO)

        # Блок событий (исправлено: без распаковки)
        alarmed_list = []
        if alarmed_eq:
            alarmed_list = [ft.Text(f"• {name}", size=14, color=COLOR_RED) for name in alarmed_eq]
        else:
            alarmed_list = [ft.Text("Нет аварий", size=14, color=COLOR_GREEN)]

        events_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("События", weight=ft.FontWeight.BOLD, size=16, color=COLOR_WHITE),
                        ft.Text(f"Аварии: {num_alarms}", size=14, color=COLOR_RED),
                        ft.Text(f"Предупреждения: {num_warnings}", size=14, color=COLOR_AMBER),
                        ft.Text(f"Прогнозы: {num_forecasts}", size=14, color=COLOR_ORANGE),
                    ],
                    spacing=5,
                ),
                padding=15,
            ),
            bgcolor=COLOR_CARD_BG,
            elevation=2,
            width=250,
        )

        alarmed_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Аварии по оборудованию", weight=ft.FontWeight.BOLD, size=16, color=COLOR_WHITE),
                        *alarmed_list,
                    ],
                    spacing=5,
                ),
                padding=15,
            ),
            bgcolor=COLOR_CARD_BG,
            elevation=2,
            width=350,
        )

        events_row = ft.Row([events_card, alarmed_card], spacing=15, scroll=ft.ScrollMode.AUTO)

        # Топ-3 причин
        def reason_bar(label, percent, color=COLOR_BLUE):
            return ft.Row([
                ft.Text(label, size=13, color=COLOR_WHITE, width=150),
                ft.Container(
                    content=ft.Container(width=percent * 2, height=16, bgcolor=color, border_radius=4),
                    width=200,
                ),
                ft.Text(f"{percent}%", size=13, color=COLOR_WHITE),
            ], spacing=10)

        reasons_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Топ-3 причины простоев", weight=ft.FontWeight.BOLD, size=16, color=COLOR_WHITE),
                    *[reason_bar(name, val, COLOR_ORANGE if i==0 else COLOR_AMBER if i==1 else COLOR_GREEN) 
                      for i, (name, val) in enumerate(top_reasons)],
                ], spacing=10),
                padding=15,
            ),
            bgcolor=COLOR_CARD_BG,
            elevation=2,
        )

        # Таблица
        table_header = ft.Row([
            ft.Text("Оборудование", weight=ft.FontWeight.BOLD, color=COLOR_WHITE, width=220),
            ft.Text("Тип", weight=ft.FontWeight.BOLD, color=COLOR_WHITE, width=100),
            ft.Text("Время работы", weight=ft.FontWeight.BOLD, color=COLOR_WHITE, width=100),
            ft.Text("Простои", weight=ft.FontWeight.BOLD, color=COLOR_WHITE, width=80),
            ft.Text("Аварии", weight=ft.FontWeight.BOLD, color=COLOR_WHITE, width=70),
            ft.Text("Предупр.", weight=ft.FontWeight.BOLD, color=COLOR_WHITE, width=80),
            ft.Text("КТГ %", weight=ft.FontWeight.BOLD, color=COLOR_WHITE, width=70),
        ], spacing=5)

        table_rows = []
        for row in table_data:
            table_rows.append(
                ft.Row([
                    ft.Text(row["name"], color=COLOR_WHITE, width=220),
                    ft.Text(row["type"], color=COLOR_WHITE, width=100),
                    ft.Text(f"{row['work']} ч", color=COLOR_WHITE, width=100),
                    ft.Text(f"{row['downtime']} ч", color=COLOR_WHITE, width=80),
                    ft.Text(str(row["alarms"]), color=COLOR_RED if row["alarms"] else COLOR_WHITE, width=70),
                    ft.Text(str(row["warns"]), color=COLOR_AMBER if row["warns"] else COLOR_WHITE, width=80),
                    ft.Text(f"{row['ktg']}%", color=COLOR_GREEN if row["ktg"] > 50 else COLOR_ORANGE, width=70),
                ], spacing=5)
            )

        table_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Детальная информация по оборудованию", weight=ft.FontWeight.BOLD, size=16, color=COLOR_WHITE),
                    table_header,
                    *table_rows,
                ], spacing=8),
                padding=15,
            ),
            bgcolor=COLOR_CARD_BG,
            elevation=2,
        )

        # Диаграмма по сменам
        shift_names = ["Смена А", "Смена Б", "Смена В"]
        work_data = [6, 5, 7]
        downt_data = [2, 3, 1]

        def make_bar_pair(work_h, downt_h):
            max_h = max(work_h, downt_h)
            scale = 80 / max(max_h, 1)
            work_height = work_h * scale
            downt_height = downt_h * scale
            return ft.Column([
                ft.Row([
                    ft.Container(width=20, height=work_height, bgcolor=COLOR_BLUE, border_radius=2),
                    ft.Container(width=20, height=downt_height, bgcolor=COLOR_ORANGE, border_radius=2),
                ], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                ft.Text(f"{work_h}ч/{downt_h}ч", size=11, color=COLOR_WHITE38, text_align=ft.TextAlign.CENTER),
            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        bar_row = ft.Row([
            ft.Column([
                ft.Text(name, size=13, color=COLOR_WHITE, text_align=ft.TextAlign.CENTER),
                make_bar_pair(work_data[i], downt_data[i]),
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            for i, name in enumerate(shift_names)
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        legend = ft.Row([
            ft.Row([ft.Container(width=12, height=12, bgcolor=COLOR_BLUE, border_radius=2), ft.Text("Работа", size=12, color=COLOR_WHITE)]),
            ft.Row([ft.Container(width=12, height=12, bgcolor=COLOR_ORANGE, border_radius=2), ft.Text("Простой", size=12, color=COLOR_WHITE)]),
        ], spacing=15)

        chart_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Работа и простои по сменам", weight=ft.FontWeight.BOLD, size=16, color=COLOR_WHITE),
                    bar_row,
                    legend,
                ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
            ),
            bgcolor=COLOR_CARD_BG,
            elevation=2,
        )

        return ft.Column([
            ft.Text("Отчёты", size=24, weight=ft.FontWeight.BOLD),
            header_row,
            events_row,
            reasons_card,
            table_card,
            chart_card,
        ], spacing=20, scroll=ft.ScrollMode.AUTO)

    def build_parts_catalog():
        parts_grid = ft.GridView(expand=True, max_extent=250, spacing=10, run_spacing=10)
        for part in mock_parts:
            color = {"in_stock": COLOR_GREEN, "low_stock": COLOR_ORANGE, "out_of_stock": COLOR_RED}.get(part.status, COLOR_GREY)
            parts_grid.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(part.name, weight=ft.FontWeight.BOLD, size=14),
                            ft.Text(f"{part.manufacturer} · {part.part_number}"),
                            ft.Text(f"Цена: {part.price:,} ₽".replace(",", " ")),
                            ft.Text(f"Наличие: {part.stock} шт.", color=color),
                        ], spacing=4),
                        padding=10,
                    ),
                    bgcolor=COLOR_CARD_BG,
                )
            )
        return ft.Column([ft.Text("Каталог запчастей", size=20), parts_grid], spacing=10)

    def build_settings():
        return ft.Column([ft.Text("Настройки", size=20),
                          ft.Slider(min=50, max=100, divisions=50, label="Чувствительность ИИ"),
                          ft.Text("Пороговые значения датчиков (в разработке)")], spacing=10)

    switch_page(0)

    page.add(
        ft.Row(
            [
                nav_rail,
                ft.VerticalDivider(width=1),
                content_area,
            ],
            expand=True,
        )
    )

ft.run(main)
