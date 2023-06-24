import os
from tasks import process_pdf
from celery import Celery
from celery import group

# Создание экземпляра Celery
app = Celery('tasks', broker='redis://localhost:6379/0')


def process_folder(folder_path, search_query):
    tasks = []

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.pdf'):
                file_path = os.path.join(root, file_name)
                task = process_pdf.delay(file_path, search_query)
                tasks.append(task)

    # Группировка задач и ожидание их выполнения
    group(tasks).get(None)


if __name__ == '__main__':
    folder_path = input("Введите путь к папке: ")
    search_query = input("Введите строку для поиска: ")

    process_folder(folder_path, search_query)



# Введите путь к папке: pdf_docs
# Введите строку для поиска: Капитальный ремонт автомобильной дороги Р-215 Астрахань - Кочубей - Кизляр - Махачкала, подъезд к г. Грозный на участке км 70+127 – км 85+267, Чеченская Республика

# Введите путь к папке: pdf_docs2
# Введите строку для поиска: Строительство и обустройство скважин куста № 10 Гарюшкинского месторождения