

class Vehicle:

    def __init__(self,year,model,name) -> None:
        self.year = year
        self.model = model
        self.name = name


class Car(Vehicle):

    def __init__(self, year, model, name,boot_space) -> None:
        super().__init__(year, model, name)
        self.boot_space = boot_space


    def speed(self):
        return self.boot_space*self.year*2
    

class Truck(Vehicle):

    def __init__(self, year, model, name,boot_space) -> None:
        super().__init__(year, model, name)
        self.boot_space = boot_space

    def speed(self):
        return self.boot_space/self.year


