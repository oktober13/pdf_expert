import PyPDF2
from fuzzywuzzy import fuzz

file_path = input("Введите путь к файлу: ")

with open(file_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)

    search_query = input("Введите строку для поиска: ")

    results = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        # Вычисление сходства строки поиска с текстом страницы
        match_score = fuzz.partial_ratio(search_query.lower(), text.lower())

        # Если сходство выше 50%, добавить результат в список
        if match_score >= 50:
            results.append((page_number, match_score))

    # Сохраняем в файл
    with open('search_results.txt', 'w') as output_file:
        for i, result in enumerate(results, start=1):
            page_number, match_score = result
            output_file.write(f"{i}. Найдено '{search_query}' - номер страницы {page_number} - процент сходства {match_score}%\n")

