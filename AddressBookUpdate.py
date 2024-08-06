import pickle
from collections import UserDict
from faker import Faker

fake = Faker('uk_UA')

class Field():
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return str(self.value)
    
class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Номер телефону має містити 10 цифр")
        super().__init__(value)
    
    @staticmethod
    def validate_phone(phone):
        return phone.isdigit() and len(phone) == 10
        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones =[]
        
    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)
        
    def remove_phone(self, phone_number):
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Номер телефону не знайдено")
        
    def edit_phone(self, old_number, new_number):
        phone_to_edit = self.find_phone(old_number)
        if phone_to_edit:
            if not Phone.validate_phone(new_number):
                raise ValueError ("Новий номер телефону має містити 10 чисел")
            phone_to_edit.value = new_number
        else:
            raise ValueError("Старий номер телефону не знайдено")
    
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def __str__(self) -> str:
        return f"Ім'я контакту {self.name.value}, номер: {','.join(p.value for p in self.phones)}"
        
class AddressBook(UserDict):
    def add_record(self, record): 
        self.data[record.name.value] = record
        
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Запис не знайдено")
    
    def __str__(self) -> str:
        return "\n".join(str(record) for record in self.data.values())
                
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)
        
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()
    
def generate_fake_user():
    name = fake.name()
    phone = fake.phone_number()
    phone = ''.join(filter(str.isdigit, phone))[:10]
    if len(phone) == 10:
        return name, phone
    else:
        return generate_fake_user()
    
def main():
    address_book = load_data()
    
    while True:
    
        command = input("Введіть команду (додати, корегувати, видалити, показати, знайти, зберегти, генерувати, вихід): ").strip().lower()
    
        if command == "додати":
            name = input("Введіть Ім'я: ")
            phone = input("Введіть номер телефону: ")
            try:
                record = Record(name)
                record.add_phone(phone)
                address_book.add_record(record)
                print(f"Запис додано: {record}")
            except ValueError as e:
                print(e)
        
        elif command == "корегувати":
                name = input("Введіть ім'я: ")
                old_phone = input("Введіть старий номер телефону: ")
                new_phone = input("Введіть новий номер телефону: ")
                record =address_book.find(name)
                if record:
                    try:
                        record.edit_phone(old_phone, new_phone)
                        print(f"Запис оновлено {record}")
                    except ValueError as e:
                        print(e)
                else:
                    print("Запис не знайдено")
        
        elif command == "видалити":     
            name = input("Введіть ім'я: ")
            try:
                address_book.delete(name)
                print(f"Запис видалено для {name}")
            except KeyError as e:
                print(e)
                
        elif command == "показати":
            print(address_book)
            
        elif command == "знайти":
            name = input("Введіть ім'я: ")
            record = address_book.find(name)
            if record:
                print(record)
            else:
                print("Запис не знайдено")
        
        elif command == "зберегти":
            save_data(address_book)
            print("Записник збережено")
            
            
        elif command == "генерувати":
            try:
                name, phone = generate_fake_user()
                record = Record(name)
                record.add_phone(phone)
                address_book.add_record(record)
                print(f"Згенеровано та додано запис: {record}")
            except ValueError as e:
                print(e)
                
        elif command == "вихід":
            save_data(address_book)
            print("Вихід та збереження адресної книги")
            break
            
        
        else:
            print("Команди не знайдено")

if __name__ == "__main__":
    main()
    
    
    
    