import sqlite3

class CoffeeERP:
    def __init__(self, db_name="coffee.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._init_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            try:
                self.cursor.execute("DELETE FROM orders")
                self.cursor.execute("DELETE FROM menu")
                self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='menu'")
                self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='orders'")
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Ошибка при очистке данных: {e}")
            finally:
                self.conn.close()

    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                total REAL NOT NULL
            )
        ''')

        self.cursor.execute("SELECT COUNT(*) FROM menu")
        if self.cursor.fetchone()[0] == 0:
            items = [('Эспрессо', 150), ('Капучино', 190), ('Латте', 210)]
            self.cursor.executemany("INSERT INTO menu (name, price) VALUES (?, ?)", items)
            self.conn.commit()

    def show_menu(self):
        print("Меню кофейни")
        self.cursor.execute("SELECT id, name, price FROM menu")
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"[{row[0]}] {row[1]} — {row[2]} руб.")

    def make_order(self):
        self.show_menu()
        try:
            item_id = int(input("\nВведите ID товара: "))
            qty = int(input("Введите количество: "))

            self.cursor.execute("SELECT name, price FROM menu WHERE id = ?", (item_id,))
            item = self.cursor.fetchone()

            if not item:
                print("Товар с таким ID не найден!")
                return

            name, price = item
            total_price = price * qty

            self.cursor.execute(
                "INSERT INTO orders (item_name, quantity, total) VALUES (?, ?, ?)",
                (name, qty, total_price)
            )
            self.conn.commit()
            print(f"Успешно добавлен заказ: {name} x{qty}. Итого: {total_price}")

        except ValueError:
            print("Ошибка ввода! Вводите только числа.")

    def show_report(self):
        print("\n--- ОТЧЕТ О ПРОДАЖАХ ---")
        self.cursor.execute("SELECT item_name, quantity, total FROM orders")
        orders = self.cursor.fetchall()

        if not orders:
            print("Продаж пока не было")
            return

        for row in orders:
            print(f"Товар: {row[0]} | Кол-во: {row[1]} | Сумма: {row[2]} руб.")

        self.cursor.execute("SELECT SUM(total) FROM orders")
        total_revenue = self.cursor.fetchone()[0] or 0
        print(f"\nОбщая выручка: {total_revenue} руб.")


def main():
    with CoffeeERP() as erp:
        while True:
            print("1. Показать меню")
            print("2. Добавить заказ")
            print("3. Показать выручку")
            print("4. Выход")

            choice = input("Выберите действие (1-4): ")
            if choice == '1':
                erp.show_menu()
            elif choice == '2':
                erp.make_order()
            elif choice == '3':
                erp.show_report()
            elif choice == '4':
                print("Программа завершена.")
                break
            else:
                print("Неверный пункт меню!")
if __name__ == "__main__":
    main()
