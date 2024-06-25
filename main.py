import pygame
import pickle
import sys

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
        return f"{self.__class__.__name__} имя {self.name}, возраст {self.age}"


class Bird(Animal):
    def __init__(self, name, age, wing_span):
        super().__init__(name, age)
        self.wing_span = wing_span

    def make_sound(self):
        print(f"{self.name} говорит: Чирп!")

    def fly(self):
        print(f"{self.name} летит с размахом крыльев {self.wing_span} метров.")

    def __str__(self):
        return super().__str__() + f", с размахом крыльев {self.wing_span} метров"


class Mammal(Animal):
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self):
        print(f"{self.name} говорит: Звук для млекопитающих!")

    def __str__(self):
        return super().__str__() + f", с цветом меха {self.fur_color}"


class Reptile(Animal):
    def __init__(self, name, age, scale_type):
        super().__init__(name, age)
        self.scale_type = scale_type

    def make_sound(self):
        print(f"{self.name} говорит: Шипение!")

    def __str__(self):
        return super().__str__() + f", с {self.scale_type} чешуей"


class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def __str__(self):
        return f"{self.position} имя {self.name}"


class ZooKeeper(Employee):
    def __init__(self, name):
        super().__init__(name, "Персонал зоопарка")

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
        print(f"Добавлен {animal} в зоопарк.")

    def add_employee(self, employee):
        self.employees.append(employee)
        print(f"Добавлен {employee} в зоопарк.")

    def show_animals(self):
        print(f"Животные в {self.name} в зоопарке:")
        for animal in self.animals:
            print(animal)

    def show_employees(self):
        print(f"Сотрудники в {self.name} в зоопарке:")
        for employee in self.employees:
            print(employee)

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
        print(f"Данные зоопарка сохранены в {filename}.")

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'rb') as file:
            zoo = pickle.load(file)
        print(f"Данные зоопарка загружены из {filename}.")
        return zoo


# Определение игры
class ZooGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        pygame.display.set_caption("Мой мини зоопарк")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        self.zoo = Zoo(name="Городской Зоопарк")

        # Инициализация элементов интерфейса
        self.buttons = {
            "Добавить Животное": pygame.Rect(50, 100, 320, 50),
            "Добавить Сотрудника": pygame.Rect(50, 160, 320, 50),
            "Показать Животных": pygame.Rect(50, 220, 320, 50),
            "Показать Сотрудников": pygame.Rect(50, 280, 320, 50),
            "Сохранить": pygame.Rect(50, 340, 320, 50),
            "Загрузить": pygame.Rect(50, 400, 320, 50)
        }
        self.messages = []

    def draw_text(self, text, pos, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, pos)

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if self.buttons[button].collidepoint(event.pos):
                            self.handle_button(button)

            self.screen.fill((50, 50, 50))
            self.draw_text("Добро пожаловать в игру Мой мини зоопарк!", (150, 20), (0, 255, 0))

            for button in self.buttons:
                pygame.draw.rect(self.screen, (0, 128, 255), self.buttons[button])
                self.draw_text(button, (self.buttons[button].x + 10, self.buttons[button].y + 10))

            for i, message in enumerate(self.messages[-5:]):
                self.draw_text(message, (320, 100 + i * 30), (255, 255, 0))

            pygame.display.flip()
            self.clock.tick(30)

    def handle_button(self, button):
        if button == "Добавить Животное":
            self.add_animal_dialog()
        elif button == "Добавить Сотрудника":
            self.add_employee_dialog()
        elif button == "Показать Животных":
            self.show_animals()
        elif button == "Показать Сотрудников":
            self.show_employees()
        elif button == "Сохранить":
            self.save_zoo()
        elif button == "Загрузить":
            self.load_zoo()

    def get_user_input(self, prompt):
        pygame.font.init()
        input_box = pygame.Rect(300, 450, 200, 50)  # Увеличиваем координату y на 50 пикселей
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.fill((50, 50, 50))
            self.draw_text(prompt, (50, 400), (255, 255, 255))  # Перемещаем текст на новую строку
            txt_surface = self.font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)

            pygame.display.flip()
            self.clock.tick(30)

        return text

    def add_animal_dialog(self):
        animal_type = self.get_user_input("Введите тип животного (Птица, Млекопитающее, Рептилия): ")
        name = self.get_user_input("Введите имя животного: ")
        age = int(self.get_user_input("Введите возраст животного: "))
        if animal_type == "Птица":
            wing_span = float(self.get_user_input("Введите размах крыльев: "))
            animal = Bird(name, age, wing_span)
        elif animal_type == "Млекопитающее":
            fur_color = self.get_user_input("Введите цвет меха: ")
            animal = Mammal(name, age, fur_color)
        elif animal_type == "Рептилия":
            scale_type = self.get_user_input("Введите тип чешуи: ")
            animal = Reptile(name, age, scale_type)
        else:
            self.messages.append("Неверный тип животного!")
            return
        self.zoo.add_animal(animal)
        self.messages.append(f"Добавлено {animal}")

    def add_employee_dialog(self):
        employee_type = self.get_user_input("Введите тип сотрудника (Уход, Ветеринар): ")
        name = self.get_user_input("Введите имя сотрудника: ")
        if employee_type == "Уход":
            employee = ZooKeeper(name)
        elif employee_type == "Ветеринар":
            employee = Veterinarian(name)
        else:
            self.messages.append("Неверный тип сотрудника!")
            return
        self.zoo.add_employee(employee)
        self.messages.append(f"Добавлен {employee}")

    def show_animals(self):
        self.messages.append("Животные в зоопарке:")
        for animal in self.zoo.animals:
            self.messages.append(str(animal))

    def show_employees(self):
        self.messages.append("Сотрудники в зоопарке:")
        for employee in self.zoo.employees:
            self.messages.append(str(employee))

    def save_zoo(self):
        filename = self.get_user_input("Введите имя файла для сохранения: ")
        self.zoo.save_to_file(filename)
        self.messages.append(f"Зоопарк сохранен в {filename}")

    def load_zoo(self):
        filename = self.get_user_input("Введите имя файла для загрузки: ")
        self.zoo = Zoo.load_from_file(filename)
        self.messages.append(f"Зоопарк загружен из {filename}")

if __name__ == "__main__":
    game = ZooGame()
    game.main_loop()
