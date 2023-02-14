class Observer:
    def update(self, subject):
        pass


class SmsNotifier(Observer):
    def update(self, subject):
        print("SMS->", "к нам присоединился", subject.students[-1].name)


class EmailNotifier(Observer):
    def update(self, subject):
        print(("EMAIL->", "к нам присоединился", subject.students[-1].name))


class Subject:
    def __init__(self):
        self.observers: list[Observer] = []

    def notify(self):
        for item in self.observers:
            item.update(self)
