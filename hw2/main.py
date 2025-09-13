from lib.latex_generator import LatexTableGenerator
import sys

def main():
    generator = LatexTableGenerator(
        title="Таблицы",
        author="Мария Окорочкова",
        filename=sys.argv[1] if len(sys.argv) > 1 else "artifacts/generated_table.tex")

    generator.add_package("\\usepackage{graphicx}")
    generator.add_package("\\usepackage{amsmath}")
    generator.add_package("\\usepackage[russian]{{babel}}")

    table1 = generator.create_table(
        data=[["Продукт", "Цена"], ["Яблоки", "100"], ["Помидоры", "150"]],
        caption="Таблица продуктов",
        label="tab:products",
        alignment="l r"
    )

    table2 = generator.create_table(
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

    generator.add_table(table1)
    generator.add_table(table2)

    image = generator.create_image(
        path="image.jpg",
        caption="Осень",
        label="fig:example"
    )

    generator.add_image(image)

    saved_file = generator.generate_and_save_multi_table()
    print(f"LaTeX file generated in {saved_file}")

if __name__ == "__main__":
    main()