import sys
import latexgenlib.latex_generator as lg

def main():
    title = "Таблицы и изображения"
    author = "Мария Окорочкова"
    filename = sys.argv[1] if len(sys.argv) > 1 else "artifacts/generated_document.tex"

    packages = [
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage[T2A]{fontenc}",
        "\\usepackage[russian]{babel}",
        "\\usepackage{array}",
        "\\usepackage{multirow}",
        "\\usepackage{graphicx}",
        "\\usepackage{amsmath}"
    ]

    table1 = lg.generate_table_content(
        data=[["Продукт", "Цена"], ["Яблоки", "100"], ["Помидоры", "150"]],
        caption="Таблица продуктов",
        label="tab:products",
        alignment="l r"
    )

    table2 = lg.generate_table_content(
        data=[
            ["Тип данных", "Пример", "Описание"],
            ["Строка", "Hello & World", "Текст с амперсандом"],
            ["Число", 42, "Целое число"],
            ["Дробное", 3.14, "Число с плавающей точкой"],
            ["Процент", "50% скидка", "Текст с процентом"],
            ["Математика", "E = mc^2", "Формула"],
            ["Спецсимволы", "#comment_{text}", "Разные символы"]
        ],
        caption="Большой пример таблицы",
        label="tab:complex_data",
        alignment="l l p{6cm}"
    )
    image = lg.generate_image_content(
        image_path="image.png",
        caption="Осень",
        label="fig:example"
    )

    all_content = table1 + "\n\n" + table2 + "\n\n" + image
    latex_document = lg.generate_document(title, author, all_content, packages)
    saved_file = lg.save_to_file(latex_document, filename)
    print(f"LaTeX file generated in {saved_file}")

if __name__ == "__main__":
    main()