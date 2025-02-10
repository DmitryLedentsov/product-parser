import pdfplumber
from collections import defaultdict

def parse_pdf(file_path):
    categories = defaultdict(list)
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    print(line)
                    if 'шт.' in line:  # Проверяем, что строка содержит данные о товаре
                        parts = line.split('|')
                        if len(parts) > 2:
                            product_name = parts[2].strip()
                            category = product_name.split(' - ')[0].strip()
                            categories[category].append(product_name)
    
    return categories

def print_categories(categories):
    for category, products in categories.items():
        print(f"Категория: {category}")
        for product in products:
            print(f"  - {product}")
        print()


file_path = "./naklad.pdf"
print("parsing..\n")
categories = parse_pdf(file_path)
print(len(categories))
print_categories(categories)