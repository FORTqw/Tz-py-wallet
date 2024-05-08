import datetime


class Record:
    """
        Класс для представления финансовой записи
        date - Дата записи
        category - Категория записи (доход или расход)
        amount - Сумма записи
        description - Описание записи
    """
    def __init__(self, date: datetime.date, category: str, amount: float, description: str):
        self.date: datetime.date = date
        self.category: str = category
        self.amount: float = amount
        self.description: str = description

class DataLoader:
    """
       Класс для загрузки и сохранения данных из/в файл
       data_file - Имя файла для загрузки/сохранения данных
    """
    def __init__(self, data_file: str = 'data.txt'):
        self.data_file: str = data_file

    def load_data(self) -> list[Record]:
        """
            Загружает данные из файла и возвращает список записей
        """
        records: list[Record] = []
        with open(self.data_file, 'r') as file:
            lines = file.read().strip().split('\n')
            for i in range(0, len(lines), 5):
                record_attrs: dict[str, str] = {}
                for q in range(i, min(i + 4, len(lines))):
                    if ':' in lines[q]:
                        key, value = lines[q].split(': ')
                        key = key.strip()
                        if key == 'Дата':
                            key = 'date'
                            value = datetime.datetime.strptime(value.strip(), '%d.%m.%Y').date()
                        elif key == 'Сумма':
                            key = 'amount'
                            value = float(value.strip())
                        elif key == 'Категория':
                            key = 'category'
                        elif key == 'Описание':
                            key = 'description'
                        record_attrs[key] = value
                if all(k in record_attrs for k in ['date', 'category', 'amount', 'description']):
                    records.append(Record(**record_attrs))
        return records

    def save_data(self, records: list[Record]):
        """
            Сохраняет список записей в файл
            records - Список записей для сохранения
        """
        with open(self.data_file, 'w') as file:
            for record in records:
                file.write(f"Дата: {record.date.strftime('%d.%m.%Y')}\n")
                file.write(f"Категория: {record.category}\n")
                file.write(f"Сумма: {record.amount}\n")
                file.write(f"Описание: {record.description}\n\n")

class AccountingApp:
    def __init__(self, data_loader: DataLoader = DataLoader()):
        self.data_loader: DataLoader = data_loader
        self.records: list[Record] = data_loader.load_data()
        print(f"Загружено {len(self.records)} записей из файла")

    def add_record(self, category: str, amount: float, description: str):
        record = Record(datetime.date.today(), category, amount, description)
        self.records.append(record)
        print(f"Добавлено {len(self.records)} записей. Сохранение...")
        self.data_loader.save_data(self.records)

    def edit_record(self, index: int, **kwargs):
        if 0 <= index < len(self.records):
            for key, value in kwargs.items():
                if key == 'date' and isinstance(value, str):
                    value = datetime.datetime.strptime(value, '%d.%m.%Y').date()
                elif key == 'amount':
                    value = float(value)
                setattr(self.records[index], key, value)
            print(f"Отредактировано {len(self.records)} записей. Сохранение...")
            self.data_loader.save_data(self.records)

    def search_records(self, **kwargs) -> list[Record]:
        """
            Ищет записи в списке записей, соответствующие указанным критериям, и возвращает список найденных записей
            kwargs - Словарь с критериями поиска
        """
        results: list[Record] = []
        for record in self.records:
            match = True
            for key, value in kwargs.items():
                if getattr(record, key) != value:
                    match = False
                    break
            if match:
                results.append(record)
        return results

    def get_balance(self) -> tuple[float, float, float]:
        """
            Возвращает текущий баланс, доходы и расходы
        """
        income: float = sum([record.amount for record in self.records if record.category == 'Доход'])
        expenses: float = sum([record.amount for record in self.records if record.category == 'Расход'])
        balance: float = income - expenses
        return balance, income, expenses

def main():
    app = AccountingApp()

    while True:
        print("1. Вывод баланса")
        print("2. Добавление записи")
        print("3. Редактирование записи")
        print("4. Поиск по записям")
        print("5. Выход")
        choice = int(input("Введите номер операции: "))

        if choice == 1:
            balance, income, expenses = app.get_balance()
            print(f"Баланс: {balance}")
            print(f"Доходы: {income}")
            print(f"Расходы: {expenses}")
        elif choice == 2:
            category = input("Введите категорию (Доход/Расход): ")
            amount = float(input("Введите сумму: "))
            description = input("Введите описание: ")
            app.add_record(category, amount, description)
        elif choice == 3:
            index = int(input("Введите индекс записи для редактирования: "))
            category = input("Введите новую категорию (Доход/Расход) или нажмите enter, чтобы оставить без изменений: ")
            amount = input("Введите новую сумму или нажмите Enter, чтобы оставить без изменений: ")
            description = input("Введите новое описание или нажмите enter, чтобы оставить без изменений: ")
            kwargs = {}
            if category:
                kwargs = {'category': category}
            if amount:
                kwargs['amount'] = float(amount)
            if description:
                kwargs['description'] = description
            app.edit_record(index, **kwargs)
        elif choice == 4:
            category = input("Введите категорию для поиска (Доход/Расход) или нажмите enter, чтобы искать по всем категориям: ")
            date = input("Введите дату для поиска(d.m.y) или нажмите enter, чтобы искать по всем датам: ")
            amount = input("Введите сумму для поиска или нажмите enter, чтобы искать по всем суммам: ")
            if category:
                kwargs = {'category': category}
            if date:
                kwargs['date'] = datetime.datetime.strptime(date, '%d.%m.%Y').date()
            if amount:
                kwargs['amount'] = float(amount)
            results = app.search_records(**kwargs)
            for result in results:
                print(f"Дата: {result.date.strftime('%d.%m.%Y')}")
                print(f"Категория: {result.category}")
                print(f"Сумма: {result.amount}")
                print(f"Описание: {result.description}")
                print()
        elif choice == 5:
            app.data_loader.save_data(app.records)
            break

if __name__ == "__main__":
    main()
