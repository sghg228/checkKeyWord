import os
import docx2txt
from openpyxl import load_workbook
import time
import socket
from striprtf.striprtf import rtf_to_text


def check_keywords_in_text(text, keywords):
    found_keywords = [keyword for keyword in keywords if keyword in text]
    return found_keywords


def check_keywords_in_docx(file_path, keywords):
    content = docx2txt.process(file_path)
    return check_keywords_in_text(content, keywords)


def check_keywords_in_rtf(file_path, keywords):
    with open(file_path) as infile:
        content = infile.read()
        text = rtf_to_text(content)
    return check_keywords_in_text(text, keywords)


def check_keywords_in_xlsx(file_path, keywords):
    workbook = load_workbook(file_path)
    content = []
    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        for row in sheet.iter_rows():
            for cell in row:
                content.append(str(cell.value))
    return check_keywords_in_text('\n'.join(content), keywords)


def search_files_in_folder(folder_path, keywords):
    name = os.environ['USERNAME']
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            start_time = time.time()
            file_path = os.path.join(root, file_name)
            found_keywords = None
            if file_path.endswith(('.txt', '.docx', '.doc', '.rtf', 'xls', 'xlsx')):
                if file_path.endswith('.txt'):
                    found_keywords = check_keywords_in_text(open(file_path, 'r', encoding='utf-8').read(), keywords)
                elif file_path.endswith(('.docx', '.doc')):
                    found_keywords = check_keywords_in_docx(file_path, keywords)
                elif file_path.endswith('.rtf'):
                    found_keywords = check_keywords_in_rtf(file_path, keywords)
                elif file_path.endswith('.xlsx'):
                    found_keywords = check_keywords_in_xlsx(file_path, keywords)
                if found_keywords:
                    print(f'[{str(name)}] File {file_path} contains keywords: {", ".join(found_keywords)}')
            end_time = time.time()

            # Рассчитайте разницу, чтобы узнать время выполнения
            execution_time = end_time - start_time
            print(str(execution_time) + ' ' + file_name)


if __name__ == "__main__":
    # Путь к папке, которую нужно проверить
    folder_path = 'C:\\Users\\User\\Desktop\\lalala'

    # Список ключевых слов для поиска
    keywords = ['Test a']

    search_files_in_folder(folder_path, keywords)
