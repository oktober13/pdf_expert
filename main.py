import PyPDF2
from fuzzywuzzy import fuzz

file_path = input("Введите путь к файлу: ")

with open(file_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)

    search_query = input("Введите строку для поиска: ")

    results = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        text = text.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')

        # Вычисление сходства строки поиска с текстом страницы
        match_score = fuzz.partial_ratio(search_query.lower(), text.lower())

        # Если сходство выше 50%, добавить результат в список
        if match_score >= 81:
            results.append((page_number, match_score, 'Совпадение'))
        elif 81 > match_score >= 65:
            results.append((page_number, match_score, 'Внимание, необходимо проверить!'))

    # Сохраняем в файл
    with open('search_results.txt', 'w') as output_file:
        output_file.write(f"Объект капитального строительства: {search_query}'\n")
        for i, result in enumerate(results, start=1):
            page_number, match_score, comment = result
            output_file.write(f"{i}. Найдено совпадение на странице {page_number} - процент сходства {match_score}% - {comment}\n")



# Введите путь к файлу: pdf/Раздел ПД №1_Том 1_51-ПЗ.00027-21_СКЭ-25982.pdf
# Введите строку для поиска: Капитальный ремонт автомобильной дороги Р-215 Астрахань - Кочубей - Кизляр - Махачкала, подъезд к г. Грозный на участке км 70+127 – км 85+267, Чеченская Республика