import tabula
import pandas as pd
from tabulate import tabulate
from collections import defaultdict

def parse_pdf(file_path):
    # Чтение всех таблиц из PDF с помощью tabula
    # Используем параметр `pages="all"` для чтения всех страниц
    # и `multiple_tables=False`, чтобы объединить данные в одну таблицу
    tables = tabula.read_pdf(file_path, pages="all", multiple_tables=False)
    
    # Объединяем все таблицы в один DataFrame
    combined_table = pd.concat(tables, ignore_index=True)
    
    return combined_table

def get_products(df):
    result = []
    # Проверяем, что DataFrame содержит колонку "Товар"
    if "Товар" in df.columns:
        #удаляем последнюю лишнюю строку с доставкой
        df = df[~df["Товар"].str.contains("Доставка", case=False, na=False)]
        # Преобразуем DataFrame в список списков для вывода с помощью tabulate
        table_data = df[["Товар", "Цена", "Кол-во"]].values.tolist()
        # Добавляем нумерацию строк
        table_data = [[i + 1, row[0], row[1], int(row[2])]  for i, row in enumerate(table_data) ] 
        
        result =table_data
    else:
        raise Exception("Колонка 'Товар' не найдена в таблице.")
    return result

def print_table(table,h=["№", "Товар","Цена","Кол-во"]):
     # Выводим таблицу
    print(tabulate(table, headers=h, tablefmt="pretty"))
def add_categories(products):
    categories = defaultdict(list)
    for product in products:
        name = product[1].lower()  # Приводим название товара к нижнему регистру для удобства
        
        # Определяем категорию на основе ключевых слов
        if "жидкость" in name:
            categories["Жидкости"].append(product)
        elif "plonq" in name:
            categories["Plonq"].append(product)
       
        elif " mah " in name or " pod " in name:
            categories["Многоразки"].append(product)
        elif "табак" in name:
            categories["Табак"].append(product)
        elif "картридж" in name or "смесь" in name:
            categories["Расходники"].append(product)
        elif True:
            categories["Одноразки"].append(product)
        else:
            # Если категория не определена, добавляем в "Другое"
            categories["Другое"].append(product)
    
    return categories
file_path = "./naklad.pdf"
combined_table = parse_pdf(file_path)

# Выводим объединенную таблицу товаров
print("Общая таблица товаров:")
table = get_products(combined_table)
print_table(table)
table_with_categories = add_categories(table)

print("категории:")
for cat, table in table_with_categories.items():
    print(cat,"\n")
    print_table(table)