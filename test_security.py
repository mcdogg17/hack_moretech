import subprocess

def security_scan_sast(project_directory):
    """
    Выполняет SAST-сканирование проекта с использованием инструмента Bandit.

    :param project_directory: Путь к директории проекта
    """
    try:
        subprocess.run(['bandit', '-r', project_directory], check=True)
        print("SAST сканирование (Bandit) завершено успешно.")
    except subprocess.CalledProcessError:
        print("SAST сканирование (Bandit) обнаружило уязвимости.")

def security_scan_dast(base_url):
    """
    Выполняет DAST-сканирование веб-приложения с использованием инструмента OWASP ZAP.

    :param base_url: Базовый URL веб-приложения
    """
    try:
        subprocess.run(['zap-full-scan', '-t', base_url], check=True)
        print("DAST сканирование (OWASP ZAP) завершено успешно.")
    except subprocess.CalledProcessError:
        print("DAST сканирование (OWASP ZAP) обнаружило уязвимости.")

def security_scan_database(database_url, queries_to_check):
    """
    Проверяет SQL-запросы на наличие уязвимостей безопасности с использованием инструмента SQLMap.

    :param database_url: URL базы данных
    :param queries_to_check: Список SQL-запросов для проверки
    """
    try:
        subprocess.run(['sqlmap', '-u', database_url, '--data', queries_to_check], check=True)
        print("Проверка SQL-запросов (SQLMap) завершена успешно.")
    except subprocess.CalledProcessError:
        print("Проверка SQL-запросов (SQLMap) обнаружила уязвимости.")

# Пример использования:
# Путь к директории проекта, базовый URL веб-приложения и SQL-запросы для проверки.
project_directory = "/"
web_app_base_url = "http://88.218.169.17:42121"
sql_queries = "SELECT * FROM salepoint"

security_scan_sast(project_directory)
security_scan_dast(web_app_base_url)
security_scan_database(web_app_base_url, sql_queries)
