import tkinter as tk
from tkinter import messagebox
import ast
import random

# Определение классов животных и сотрудников
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        raise NotImplementedError("Этот метод должен быть переопределен в подклассах")

    def eat(self):
        print(f"{self.name} ест.")

    def __str__(self):
        return f"{self.get_type()} по имени {self.name}, возраст {self.age}"

    def to_dict(self):
        return {
            "type": self.get_type(),
            "name": self.name,
            "age": self.age
        }

    @staticmethod
    def from_dict(data):
        if data["type"] == "Птица":
            return Bird(data["name"], data["age"], data["wing_span"])
        elif data["type"] == "Млекопитающее":
            return Mammal(data["name"], data["age"], data["fur_color"])
        elif data["type"] == "Рептилия":
            return Reptile(data["name"], data["age"], data["scale_type"])
        else:
            return None

    def get_type(self):
        raise NotImplementedError("Этот метод должен быть переопределен в подклассах")


class Bird(Animal):
    def __init__(self, name, age, wing_span):
        super().__init__(name, age)
        self.wing_span = wing_span

    def make_sound(self):
        print(f"{self.name} говорит: Чирик!")

    def fly(self):
        print(f"{self.name} летит с размахом крыльев {self.wing_span} метров.")

    def __str__(self):
        return super().__str__() + f", с размахом крыльев {self.wing_span} метров"

    def to_dict(self):
        data = super().to_dict()
        data["wing_span"] = self.wing_span
        return data

    def get_type(self):
        return "Птица"


class Mammal(Animal):
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self):
        print(f"{self.name} говорит: Общий звук млекопитающего!")

    def __str__(self):
        return super().__str__() + f", с цветом меха {self.fur_color}"

    def to_dict(self):
        data = super().to_dict()
        data["fur_color"] = self.fur_color
        return data

    def get_type(self):
        return "Млекопитающее"


class Reptile(Animal):
    def __init__(self, name, age, scale_type):
        super().__init__(name, age)
        self.scale_type = scale_type

    def make_sound(self):
        print(f"{self.name} говорит: Шшш!")

    def __str__(self):
        return super().__str__() + f", с типом чешуи {self.scale_type}"

    def to_dict(self):
        data = super().to_dict()
        data["scale_type"] = self.scale_type
        return data

    def get_type(self):
        return "Рептилия"


class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def __str__(self):
        return f"{self.position} по имени {self.name}"

    def to_dict(self):
        return {
            "name": self.name,
            "position": self.position
        }

    @staticmethod
    def from_dict(data):
        if data["position"] == "Смотритель зоопарка":
            return ZooKeeper(data["name"])
        elif data["position"] == "Ветеринар":
            return Veterinarian(data["name"])
        else:
            return None


class ZooKeeper(Employee):
    def __init__(self, name):
        super().__init__(name, "Смотритель зоопарка")

    def feed_animal(self, animal):
        print(f"{self.name} кормит {animal.name}.")

    def __str__(self):
        return super().__str__()


class Veterinarian(Employee):
    def __init__(self, name):
        super().__init__(name, "Ветеринар")

    def heal_animal(self, animal):
        print(f"{self.name} лечит {animal.name}.")

    def __str__(self):
        return super().__str__()


class Zoo:
    def __init__(self, name):
        self.name = name
        self.animals = []
        self.employees = []

    def add_animal(self, animal):
        self.animals.append(animal)
        self.log_message(f"Добавлено {animal} в зоопарк.")

    def add_employee(self, employee):
        self.employees.append(employee)
        self.log_message(f"Добавлено {employee} в зоопарк.")

    def show_animals(self):
        return [str(animal) for animal in self.animals]

    def show_employees(self):
        return [str(employee) for employee in self.employees]

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for animal in self.animals:
                file.write("Animal:" + str(animal.to_dict()) + "\n")
            for employee in self.employees:
                file.write("Employee:" + str(employee.to_dict()) + "\n")
        self.log_message(f"Данные зоопарка сохранены в {filename}.")

    @staticmethod
    def load_from_file(filename):
        zoo = Zoo(name="Городской Зоопарк")
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith("Animal:"):
                    animal_data = ast.literal_eval(line[len("Animal:"):])
                    zoo.animals.append(Animal.from_dict(animal_data))
                elif line.startswith("Employee:"):
                    employee_data = ast.literal_eval(line[len("Employee:"):])
                    zoo.employees.append(Employee.from_dict(employee_data))
        zoo.log_message(f"Данные зоопарка загружены из {filename}.")
        return zoo

    def log_message(self, message):
        print(message)


# Определение игры
class ZooGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Игра Управление Зоопарком")
        self.zoo = Zoo(name="Городской Зоопарк")

        # Инициализация элементов интерфейса
        self.messages = []

        tk.Label(root, text="Добро пожаловать в игру Управление Зоопарком!", font=("Helvetica", 16)).pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Button(frame, text="Добавить Животное", command=self.add_animal).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Добавить Сотрудника", command=self.add_employee).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Показать Животных", command=self.show_animals).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame, text="Показать Сотрудников", command=self.show_employees).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame, text="Сохранить", command=self.save_zoo).grid(row=2, column=0, padx=5)
        tk.Button(frame, text="Загрузить", command=self.load_zoo).grid(row=2, column=1, padx=5)
        tk.Button(frame, text="Случайное Животное", command=self.add_random_animal).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(frame, text="Случайный Сотрудник", command=self.add_random_employee).grid(row=3, column=1, padx=5, pady=5)

        self.messages_listbox = tk.Listbox(root, width=80, height=10)
        self.messages_listbox.pack(pady=10)

    def add_animal(self):
        self.handle_input("add_animal Bird Polly 2 0.5")

    def add_employee(self):
        self.handle_input("add_employee ZooKeeper Alice")

    def show_animals(self):
        self.handle_input("show_animals")

    def show_employees(self):
        self.handle_input("show_employees")

    def save_zoo(self):
        self.handle_input("save zoo_data.txt")

    def load_zoo(self):
        self.handle_input("load zoo_data.txt")

    def add_random_animal(self):
        animal_types = ['Птица', 'Млекопитающее', 'Рептилия']
        names = ['Чарли', 'Макс', 'Белла', 'Луна', 'Рокки']
        animal_type = random.choice(animal_types)
        name = random.choice(names)
        age = random.randint(1, 10)
        if animal_type == 'Птица':
            wing_span = round(random.uniform(0.5, 2.0), 1)
            self.handle_input(f"add_animal Bird {name} {age} {wing_span}")
        elif animal_type == 'Млекопитающее':
            fur_color = random.choice(['коричневый', 'черный', 'белый', 'серый'])
            self.handle_input(f"add_animal Mammal {name} {age} {fur_color}")
        elif animal_type == 'Рептилия':
            scale_type = random.choice(['гладкая', 'грубая'])
            self.handle_input(f"add_animal Reptile {name} {age} {scale_type}")

    def add_random_employee(self):
        employee_types = ['ZooKeeper', 'Veterinarian']
        names = ['Алиса', 'Боб', 'Ева', 'Джон', 'Грейс']
        employee_type = random.choice(employee_types)
        name = random.choice(names)
        self.handle_input(f"add_employee {employee_type} {name}")

    def handle_input(self, input_text):
        commands = input_text.split()
        if not commands:
            return

        command = commands[0].lower()
        if command == "add_animal":
            if len(commands) >= 5:
                animal_type = commands[1].capitalize()
                name = commands[2]
                age = int(commands[3])
                if animal_type == "Bird" and len(commands) == 5:
                    wing_span = float(commands[4])
                    animal = Bird(name, age, wing_span)
                elif animal_type == "Mammal" and len(commands) == 5:
                    fur_color = commands[4]
                    animal = Mammal(name, age, fur_color)
                elif animal_type == "Reptile" and len(commands) == 5:
                    scale_type = commands[4]
                    animal = Reptile(name, age, scale_type)
                else:
                    return
                self.zoo.add_animal(animal)
                self.messages_listbox.insert(tk.END, f"Добавлено {animal}")

        elif command == "add_employee":
            if len(commands) >= 3:
                employee_type = commands[1].capitalize()
                name = commands[2]
                if employee_type == "Zookeeper":
                    employee = ZooKeeper(name)
                elif employee_type == "Veterinarian":
                    employee = Veterinarian(name)
                else:
                    return
                self.zoo.add_employee(employee)
                self.messages_listbox.insert(tk.END, f"Добавлено {employee}")

        elif command == "show_animals":
            animals = self.zoo.show_animals()
            self.messages_listbox.insert(tk.END, "Показаны животные:")
            for animal in animals:
                self.messages_listbox.insert(tk.END, animal)

        elif command == "show_employees":
            employees = self.zoo.show_employees()
            self.messages_listbox.insert(tk.END, "Показаны сотрудники:")
            for employee in employees:
                self.messages_listbox.insert(tk.END, employee)

        elif command == "save":
            if len(commands) == 2:
                filename = commands[1]
                self.zoo.save_to_file(filename)
                self.messages_listbox.insert(tk.END, f"Данные зоопарка сохранены в {filename}")

        elif command == "load":
            if len(commands) == 2:
                filename = commands[1]
                try:
                    self.zoo = Zoo.load_from_file(filename)
                    self.messages_listbox.insert(tk.END, f"Данные зоопарка загружены из {filename}")
                except FileNotFoundError:
                    self.messages_listbox.insert(tk.END, f"Файл {filename} не найден.")

        else:
            self.messages_listbox.insert(tk.END, f"Неизвестная команда: {command}")


# Запуск игры
if __name__ == "__main__":
    root = tk.Tk()
    game = ZooGame(root)
    root.mainloop()
