import csv
import xml.etree.ElementTree as ET
import time
from collections import defaultdict


class CityDataProcessor:
    """
        Класс для обработки данных о городах.
    """

    def __init__(self):
        """
        Инициализирует экземпляр класса CityDataProcessor.
        """
        self.city_data = defaultdict(list)

    def load_csv(self, file_path):
        """
        Загружает данные о городах из CSV-файла.
        """
        self.city_data.clear()
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                city = row['city']
                floors = int(row['floor'])
                self.city_data[city].append(floors)

    def load_xml(self, file_path):
        """
        Загружает данные о городах из XML-файла.
        """
        self.city_data.clear()
        tree = ET.parse(file_path)
        root = tree.getroot()
        for item in root.findall('item'):
            city = item.get('city')
            floor = int(item.get('floor'))
            self.city_data[city].append(floor)

    def get_duplicates(self):
        """
        Определяет количество дублирующихся записей для каждого города.
        """
        duplicates = defaultdict(int)
        for city in self.city_data:
            duplicates[city] = len(self.city_data[city])
        return {city: count for city, count in duplicates.items() if count > 1}

    def get_floor_distribution(self):
        """
        Вычисляет распределение этажности зданий.
        """
        distribution = defaultdict(int)
        for floors in self.city_data.values():
            for floor_count in floors:
                distribution[floor_count] += 1
        return distribution


class StatisticsPrinter:
    """
    Класс для вывода и сохранения статистики.
    """

    @staticmethod
    def print_duplicates(duplicates):
        """
        Выводит информацию о дублирующихся записях в консоль.
        """
        print("Дублирующиеся записи:")
        for city, count in duplicates.items():
            print(f"{city}: {count} раз(а)")

    @staticmethod
    def print_floor_distribution(distribution):
        """
        Выводит распределение этажности зданий в консоль.
        """
        print("Распределение этажности зданий:")
        for floors, count in sorted(distribution.items()):
            print(f"{floors} этажных зданий: {count}")

    @staticmethod
    def write_statistics_to_file(duplicates, distribution, output_file):
        """
        Сохраняет статистику в текстовый файл.
        """
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("Дублирующиеся записи:\n")
            for city, count in duplicates.items():
                file.write(f"{city}: {count} раз(а)\n")

            file.write("\nРаспределение этажности зданий:\n")
            for floors, count in sorted(distribution.items()):
                file.write(f"{floors} этажных зданий: {count}\n")


class Application:
    """
    Класс для управления процессом взаимодействия с пользователем.
    """

    def __init__(self):
        """
        Инициализирует экземпляр класса Application.
        """
        self.processor = CityDataProcessor()

    def run(self):
        """
        Запускает основной цикл работы приложения.
        """
        while True:
            file_path = input("Введите путь до файла-справочника (или 'exit' для выхода): ")
            if file_path.lower() == 'exit':
                break

            start_time = time.time()
            try:
                if file_path.endswith('.csv'):
                    self.processor.load_csv(file_path)
                elif file_path.endswith('.xml'):
                    self.processor.load_xml(file_path)
                else:
                    print("Неверный формат файла. Поддерживаются только .csv и .xml.")
                    continue

                processing_time = time.time() - start_time
                duplicates = self.processor.get_duplicates()
                floor_distribution = self.processor.get_floor_distribution()

                StatisticsPrinter.print_duplicates(duplicates)
                StatisticsPrinter.print_floor_distribution(floor_distribution)

                output_file = input("Введите имя файла для сохранения статистики: ")
                StatisticsPrinter.write_statistics_to_file(duplicates, floor_distribution, output_file)

                print(f"Время обработки файла: {processing_time:.2f} секунд")
            except Exception as e:
                print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    app = Application()
    app.run()
