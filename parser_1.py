import tabula
from collections import defaultdict
from tabulate import tabulate


AVAIBLE_CATS_CHECKS={
    "жижи": lambda s: "Жидкость" in s
}
def get_category(s):
    for name, check in AVAIBLE_CATS_CHECKS.items():
        if(check(name)):
            return name
    return "aaa"
def parse_pdf(file_path):
    categories = defaultdict(list)
    
    # Чтение таблиц из PDF с помощью tabula
    tables = tabula.read_pdf(file_path, pages="all", multiple_tables=True)
    
    for table in tables:
        print(table.columns)
        # Предполагаем, что таблица имеет колонки "Товар", "Ед.", "Цена", "Кол-во", "Сумма"
        if "Товар" in table.columns:
            for _, row in table.iterrows():
                product_name = row["Товар"]
                if isinstance(product_name, str):  # Проверяем, что это строка
                    
                    category = "aaa"#get_category(product_name)
                    if(category):
                        categories[category].append(product_name)
    
    return categories

def print_categories(categories):
    for category, products in categories.items():
        print(f"Категория: {category}")
        # Преобразуем список товаров в таблицу
        table = [[i + 1, product] for i, product in enumerate(products)]
        print(tabulate(table, headers=["№", "Товар"], tablefmt="pretty"))
        print()  # Пустая строка для разделения категорий


file_path = "./naklad.pdf"
categories = parse_pdf(file_path)
print_categories(categories)