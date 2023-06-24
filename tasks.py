import os
import PyPDF2
from fuzzywuzzy import fuzz
from celery import Celery

# Создание экземпляра Celery
app = Celery('tasks', broker='redis://localhost:6379/0')

# Конфигурация Celery
app.conf.task_routes = {
    'process_pdf': {'queue': 'pdf_queue'}
}

# Определение задачи Celery
@app.task
def process_pdf(file_path, search_query):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        results = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            text = text.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')

            match_score = fuzz.partial_ratio(search_query.lower(), text.lower())

            if match_score >= 81:
                results.append((page_number, match_score, 'Совпадение'))
            elif 81 > match_score >= 65:
                results.append((page_number, match_score, 'Внимание, необходимо проверить!'))

        # Сохраняем в файл
        filename = os.path.splitext(os.path.basename(file_path))[0]
        # output_filename = f"result_{filename}.txt"
        output_directory = os.path.dirname(file_path)
        output_filename = os.path.join(output_directory, f"result_{filename}.txt")

        with open(output_filename, 'w') as output_file:
            output_file.write(f"Объект капитального строительства: {search_query}\n")
            for i, result in enumerate(results, start=1):
                page_number, match_score, comment = result
                output_file.write(f"{i}. Найдено совпадение на странице {page_number} - процент сходства {match_score}% - {comment}\n")