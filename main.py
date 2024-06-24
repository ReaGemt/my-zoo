import pickle

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        raise NotImplementedError("This method should be overridden in subclasses")

    def eat(self):
        print(f"{self.name} ест.")

    def __str__(self):
        return f"{self.__class__.__name__} имя {self.name}, возраст {self.age}"


class Bird(Animal):
    def __init__(self, name, age, wing_span):
        super().__init__(name, age)
        self.wing_span = wing_span  # Размах крыльев

    def make_sound(self):
        print(f"{self.name} says: Chirp!")

    def fly(self):
        print(f"{self.name} is flying with a wingspan of {self.wing_span} meters.")

    def __str__(self):
        return super().__str__() + f", with a wingspan of {self.wing_span} meters"


class Mammal(Animal):
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.fur_color = fur_color  # Цвет меха

    def make_sound(self):
        print(f"{self.name} says: Generic mammal sound!")

    def __str__(self):
        return super().__str__() + f", with fur color {self.fur_color}"


class Reptile(Animal):
    def __init__(self, name, age, scale_type):
        super().__init__(name, age)
        self.scale_type = scale_type  # Тип чешуи

    def make_sound(self):
        print(f"{self.name} says: Hiss!")

    def __str__(self):
        return super().__str__() + f", with {self.scale_type} scales"


class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def __str__(self):
        return f"{self.position} named {self.name}"


class ZooKeeper(Employee):
    def __init__(self, name):
        super().__init__(name, "ZooKeeper")

    def feed_animal(self, animal):
        print(f"{self.name} is feeding {animal.name}.")

    def __str__(self):
        return super().__str__()


class Veterinarian(Employee):
    def __init__(self, name):
        super().__init__(name, "Veterinarian")

    def heal_animal(self, animal):
        print(f"{self.name} is healing {animal.name}.")

    def __str__(self):
        return super().__str__()


class Zoo:
    def __init__(self, name):
        self.name = name
        self.animals = []
        self.employees = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"Added {animal} to the zoo.")

    def add_employee(self, employee):
        self.employees.append(employee)
        print(f"Added {employee} to the zoo.")

    def show_animals(self):
        print(f"Animals in {self.name} Zoo:")
        for animal in self.animals:
            print(animal)

    def show_employees(self):
        print(f"Employees in {self.name} Zoo:")
        for employee in self.employees:
            print(employee)

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
        print(f"Zoo data saved to {filename}.")

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'rb') as file:
            zoo = pickle.load(file)
        print(f"Zoo data loaded from {filename}.")
        return zoo


# Примеры использования
parrot = Bird(name="Polly", age=1, wing_span=0.5)
dog = Mammal(name="Buddy", age=3, fur_color="brown")
snake = Reptile(name="Slytherin", age=2, scale_type="smooth")

keeper = ZooKeeper(name="Alice")
vet = Veterinarian(name="Dr. Smith")

zoo = Zoo(name="City Zoo")

zoo.add_animal(parrot)
zoo.add_animal(dog)
zoo.add_animal(snake)

zoo.add_employee(keeper)
zoo.add_employee(vet)

zoo.show_animals()
zoo.show_employees()

# Сохранение данных в файл
zoo.save_to_file('zoo_data.pkl')

# Загрузка данных из файла
loaded_zoo = Zoo.load_from_file('zoo_data.pkl')
loaded_zoo.show_animals()
loaded_zoo.show_employees()

# Использование специфических методов
keeper.feed_animal(parrot)
vet.heal_animal(dog)
