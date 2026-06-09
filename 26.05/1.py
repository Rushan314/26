import json
import os
from datetime import datetime

FILENAME = "tasks.json"
STATUSES = ["новая", "в работе", "выполнена"]

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        
        """Загрузка данных из файла при запуске."""
        if os.path.exists(FILENAME):
            try:
                with open(FILENAME, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                print(
                    "Ошибка: Файл данных поврежден. Инициализирован пустой список."
                )
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        """Автоматическое сохранение данных в файл."""
        try:
            with open(FILENAME, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    def get_next_id(self):
        """Генерация уникального ID (автоинкремент)."""
        if not self.tasks:
            return 1
        return max(task["id"] for task in self.tasks) + 1

    def validate_date(self, date_str):
        """Проверка формата даты ГГГГ-ММ-ДД."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def print_table(self, tasks_to_show):
        """Вывод списка задач в виде таблицы."""
        if not tasks_to_show:
            print("Список задач пуст.")
            return

        # Заголовки таблицы
        headers = [
            "ID",
            "Название",
            "Ответственный",
            "Статус",
            "Создано",
            "Дедлайн",
        ]
        row_format = "{:<5} {:<20} {:<20} Honor{:<12} {:<12} {:<12}"
        row_format = "{:<4} | {:<20} | {:<18} | {:<10} | {:<11} | {:<11}"

        print("-" * 88)
        print(row_format.format(*headers))
        print("-" * 88)

        for t in tasks_to_show:
            title = (
                t["title"][:17] + "..." if len(t["title"]) > 20 else t["title"]
            )
            resp = (
                t["responsible"][:15] + "..."
                if len(t["responsible"]) > 18
                else t["responsible"]
            )

            print(
                row_format.format(
                    t["id"],
                    title,
                    resp,
                    t["status"],
                    t["created_at"],
                    t["deadline"],
                )
            )
        print("-" * 88)

    def add_task(self):
        """Команда add: добавление новой задачи."""
        title = input("Введите название задачи (обязательно): ").strip()
        if not title:
            print("Ошибка: Название не может быть пустым.")
            return

        description = input("Введите описание задачи: ").strip()
        responsible = input("Введите ФИО ответственного: ").strip()

        deadline = input("Введите дедлайн (ГГГГ-ММ-ДД): ").strip()
        if not self.validate_date(deadline):
            print("Ошибка: Некорректный формат даты.")
            return

        new_task = {
            "id": self.get_next_id(),
            "title": title,
            "description": description,
            "responsible": responsible,
            "status": "новая",
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "deadline": deadline,
        }

        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Задача #{new_task['id']} успешно добавлена.")

    def update_task(self, task_id):
        """Команда update <id>: изменение полей задачи."""
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            print(f"Ошибка: Задача с ID {task_id} не найдена.")
            return

        print("Оставьте поле пустым, если не хотите его изменять.")

        title = input(f"Название ({task['title']}): ").strip()
        if title:
            task["title"] = title

        description = input(f"Описание ({task['description']}): ").strip()
        if description:
            task["description"] = description

        responsible = input(f"Ответственный ({task['responsible']}): ").strip()
        if responsible:
            task["responsible"] = responsible

        status = input(f"Статус ({task['status']}): ").strip()
        if status:
            if status in STATUSES:
                task["status"] = status
            else:
                print(
                    f"Ошибка: Неверный статус. Допустимые: {', '.join(STATUSES)}"
                )
                return

        deadline = input(f"Дедлайн ({task['deadline']}): ").strip()
        if deadline:
            if self.validate_date(deadline):
                task["deadline"] = deadline
            else:
                print("Ошибка: Некорректный формат даты.")
                return

        self.save_tasks()
        print(f"Задача #{task_id} успешно обновлена.")

    def done_task(self, task_id):
        """Команда done <id>: изменение статуса на 'выполнена'."""
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            print(f"Ошибка: Задача с ID {task_id} не найдена.")
            return

        task["status"] = "выполнена"
        self.save_tasks()
        print(f"Задача #{task_id} отмечена как 'выполнена'.")

    def delete_task(self, task_id):
        """Команда delete <id>: удаление задачи."""
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            print(f"Ошибка: Задача с ID {task_id} не найдена.")
            return

        self.tasks.remove(task)
        self.save_tasks()
        print(f"Задача #{task_id} успешно удалена.")


def main():
    manager = TaskManager()
    print("--- Консольный менеджер задач загружен ---")
    print(
        "Доступные команды: " 
        "\nadd 1" \
        "\nlist 2" \
        "\nshow 3" \
        "\nupdate <id> 4" \
        "\ndone <id> 5" \
        "\ndelete <id> 6" \
        "\nresponsible <имя> 7" \
        "\nexit"
    )

    while True:
        user_input = input("\nВведите команду: ").strip().split(maxsplit=1)
        if not user_input:
            continue

        command = user_input[0].lower()
        arg = user_input[1] if len(user_input) > 1 else None

        if command == "exit":
            manager.save_tasks()
            print("Данные сохранены. Выход из программы.")
            break

        elif command == "add":
            manager.add_task()

        elif command == "list":
            manager.print_table(manager.tasks)

        elif command == "show":
            if not arg or arg not in STATUSES:
                print(
                    f"Ошибка: Укажите корректный статус ({', '.join(STATUSES)})"
                )
                continue
            filtered = [t for t in manager.tasks if t["status"] == arg]
            manager.print_table(filtered)

        elif command == "responsible":
            if not arg:
                print("Ошибка: Укажите имя сотрудника.")
                continue
            filtered = [
                t
                for t in manager.tasks
                if arg.lower() in t["responsible"].lower()
            ]
            manager.print_table(filtered)

        elif command in ["update", "done", "delete"]:
            if not arg or not arg.isdigit():
                print("Ошибка: Укажите числовой ID задачи.")
                continue

            task_id = int(arg)
            if command == "update":
                manager.update_task(task_id)
            elif command == "done":
                manager.done_task(task_id)
            elif command == "delete":
                manager.delete_task(task_id)

        else:
            print("Ошибка: Неверная команда.")

if __name__ == "__main__":
    main()


















import json
import os
from datetime import datetime

from docutils.nodes import description
from kivy.tools.report import title
from setuptools.wheel import Wheel

FILENAME = tasks.json
STAT = ["Процессе", "Новое", "Закончено"]

class TaskManager:
    def __init__(self, filename):
        self.tasks = []
        self.load_tasks

    def load_tasks(self):
        if os.path.exists(FILENAME):
            try:
                with open(FILENAME, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                print("Ошибка")
            self.tasks = []

        else: self.tasks = []

    def save_tasks(self):
        try:
            with open(FILENAME, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=4)
        except Exception as e
            print("Ошибка")

    def get_next_id(self):
        if not self.tasks:
            return 1
        return max(task["id"] for task in self.tasks) + 1

    def validate_date(self, date):
        try:
            datetime.strptime(date, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    def print_table(self, tasks_to_show):
        if not tasks_to_show:
            print("Список пуст")
            return

        headers = [
            "ID",
            "Название",
            "Ответственный",
            "Статус",
            "Создано",
            "Дедлайн",
        ]
        row_format = "{:<5} {:<20} {:<20} Honor{:<12} {:<12} {:<12}"
        row_format = "{:<4} | {:<20} | {:<18} | {:<10} | {:<11} | {:<11}"

        print("-" * 88)
        print(row_format.format(*headers))
        print("-" * 88)

        for t in tasks_to_show:
            title = (
                    t["title"][:17] + "..." if len(t["title"]) > 20 else t["title"]
            )
            resp = (
                t["responsible"][:15] + "..."
                if len(t["responsible"]) > 18
                else t["responsible"]
            )

            print(
               row_format.format(
                     t["id"],
                     title,
                     resp,
                     t["status"],
                     t["created_at"],
                     t["deadline"],
                 )
             )
        print("-" * 88)

    def add_task(self):
        task = input("---Введите задачу---").strip()
        if not task:
            print("Ошибка")
            return
        description = input().strip()
        responsible = input().strip()

        deadline = input().strip()
        if not self.validate_date(deadline):
            print("Ошибка формата даты")
            return

        new_task = {
        "id": self.get_next_id(),
        "title": title(),
        "description": description,
        "responsible": responsible,
        "status": "новое",
        "created_at": datetime.now().strftime("%d.%m.%Y"),
        "deadline": deadline
        }

        self.tasks.append(new_task)
        self.save_tasks()
        print('Задача успешно добавлена')

    def update_task(self, task_id):
        task = ((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            print("Error")
            return

        print("оставьте поле пустым если не хотите изменять")

        title = input(f"Название ({task['title']}): ").strip()
        if title:
            task["title"] = title

        description = input(f"Описание ({task['description']}): ").strip()
        if description:
            task["description"] = description

        responsible = input(f"Ответственный ({task['responsible']}): ").strip()
        if responsible:
            task["responsible"] = responsible

        status = input(f"Статус ({task['status']}): ").strip()
        if status:
            if status in STATUSES:
                task["status"] = status
            else:
                print(
                    f"Ошибка: Неверный статус. Допустимые: {', '.join(STATUSES)}"
                )
                return

        deadline = input(f"Дедлайн ({task['deadline']}): ").strip()
        if deadline:
            if self.validate_date(deadline):
                task["deadline"] = deadline
            else:
                print("Ошибка: Некорректный формат даты.")
                return

        self.save_tasks()
        print(f"Задача #{task_id} успешно обновлена.")

    def done_task(self, task_id):
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            print("Error")
            return
        self.tasks.remove(task)
        self.save_tasks()
        print(f"Задача {id} удалена")

def main():
    manager = TaskManager()
    print("Cписок Меню")
    print(
        "Доступные команды: " 
        "\nadd " \
        "\nlist " \
        "\nshow" \
        "\nupdate <id> " \
        "\ndone <id>" \
        "\ndelete <id> " \
        "\nresponsible <имя> " \
        "\nexit"
    )

    while True:
        user_input = input().strip().split(maxsplit=1)
        if not user_input:
            continue

        command = user_input[0].lower()
        args = user_input[1] if len(user_input) > 1 else None

        if command == "1":
            manager.add_task()

        elif command == "2":
            manager.list_tasks()

        elif command == "3":
            if
