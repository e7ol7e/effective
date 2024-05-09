import datetime
import json
from operator import indexOf

class Record:
    def __init__(self, date: str, category: str, amount: float, description: str) -> None:
        if not isinstance(date, str) or not isinstance(category, str) or \
        not isinstance(amount, (int, float)) or not isinstance(description, str):
            raise TypeError("Invalid data type provided to Record constructor")
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    def __str__(self) -> str:
        return f"{self.date} - {self.category} - {self.amount} - {self.description}"

    def to_dict(self) -> dict[str, str]:
        """
        Returns a dictionary representation of the record.
        """
        return {
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "description": self.description
        }

    @staticmethod
    def from_dict(data: dict[str, str]) -> 'Record':
        """
        Converts a dictionary representation of a Record object back into a Record object.
        """
        return Record(data['date'], data['category'], data['amount'], data['description'])

class Wallet:
    def __init__(self, filename: str = 'wallet.txt') -> None:
        """
        Initializes a new Wallet object with the given filename for storing records.
        """
        self.filename = filename
        self.records: list[Record] = []
        self.load_records()

    def add_record(self, record: Record) -> None:
        """
        Adds a new record to the wallet.
        """
        self.records.append(record)
        self.save_records()

    def edit_record(self, index: int, new_record: Record) -> bool:
        """
        Edits a record at the specified index in the wallet.
        """
        if 0 <= index < len(self.records):
            self.records[index] = new_record
            self.save_records()
            return True
        return False

    def find_records(self, search_term: str) -> list[Record]:
        """
        Finds records in the wallet that match the given search term.
        """
        found_records = [record for record in self.records if
                        search_term.lower() in record.description.lower() or
                        search_term.lower() in record.category.lower() or
                        search_term.lower() in str(record.amount).lower() or
                        search_term.lower() == record.date.lower()]  # Perform an exact match on the date field
        return found_records
    
    def remove_record(self, index: int) -> bool:
        if 0 <= index < len(self.records):
            del self.records[index]
            self.save_records()
            return True
        return False

    def display_balance(self) -> None:
        """
        Displays the current balance, total income, and total expenses in the wallet.
        """
        income = sum(record.amount for record in self.records if record.category.lower() == 'доход')
        expense = sum(record.amount for record in self.records if record.category.lower() == 'расход')
        balance = income - expense
        print(f"\nБаланс: {balance}\nДоходы: {income}\nРасходы: {expense}")

    def save_records(self) -> None:
        """
        Saves the records to the specified file in JSON format.
        """
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([record.to_dict() for record in self.records], f, ensure_ascii=False, indent=4)

    def load_records(self) -> None:
        """
        Loads the records from the specified file in JSON format.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.records = [Record.from_dict(record) for record in json.load(f)]
        except FileNotFoundError:
            self.records = []
        except json.JSONDecodeError:  # Catch the JSONDecodeError for empty files
            self.records = []

def validate_date(date_text: str) -> bool:
    """
    Checks if the given date_text is a valid date in the format 'YYYY-MM-DD'.
    """
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def main():
    """
    Main function that runs the wallet application.
    """
    wallet = Wallet()
    while True:
        print("\n1. Показать баланс\n2. Добавить запись\n3. Редактировать запись\n4. Поиск по записям\n5. Выход")
        choice = input("Выберите действие: ")
        if choice == '1':
            wallet.display_balance()
        elif choice == '2':
            date = input("\nДобавление записи:\nДата (YYYY-MM-DD): ")
            while not validate_date(date):
                print("Неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD.")
                date = input("Дата (YYYY-MM-DD): ")
            category = input("Категория (Доход/Расход): ")
            amount_input = input("Сумма: ")
            try:
                amount = float(amount_input)
            except ValueError:
                print("Неверный формат суммы. Пожалуйста, введите число.")
                continue
            description = input("Описание: ")
            wallet.add_record(Record(date, category, amount, description))
            print("Запись добавлена.")
        elif choice == '3':
            index_input = input("\nВведите номер записи для редактирования: ")
            try:
                index = int(index_input) - 1  # Assuming user input is 1-based index
            except ValueError:
                print("Неверный формат номера записи. Пожалуйста, введите число.")
                continue
            if 0 <= index < len(wallet.records):
                date = input("Новая дата (YYYY-MM-DD): ")
                while not validate_date(date):
                    print("Неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD.")
                    date = input("Новая дата (YYYY-MM-DD): ")
                category = input("Новая категория (Доход/Расход): ")
                amount_input = input("Новая сумма: ")
                try:
                    amount = float(amount_input)
                except ValueError:
                    print("Неверный формат суммы. Пожалуйста, введите число.")
                    continue
                description = input("Новое описание: ")
                if wallet.edit_record(index, Record(date, category, amount, description)):
                    print("Запись обновлена.")
                else:
                    print("Ошибка: запись не найдена.")
            else:
                print("Запись с таким номером не найдена.")

        elif choice == '4':
            search_term = input("Введите критерий поиска (дата, категория, сумма, описание): ")
            found_records = wallet.find_records(search_term)
            if found_records:
                for record in found_records:
                    print(f"{indexOf(found_records, record)} - {record.date} - {record.category} - {record.amount} - {record.description}")
            else:
                print("Записи не найдены.")

        elif choice == '5':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()