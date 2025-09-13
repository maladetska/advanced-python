class LatexTableGenerator:

    class Table:
        def __init__(self, data, caption=None, label=None, alignment=None):
            self.data = data
            self.caption = caption
            self.label = label
            self.alignment = alignment

    class Image:
        def __init__(self, image_path, caption=None, label=None, width=None, height=None):
            self.image_path = image_path
            self.caption = caption
            self.label = label
            self.width = width
            self.height = height

    def __init__(self,
                title="LaTeX table example",
                author="Table generator",
                filename="result_file.tex",
                alignment=None):
        self._title = title
        self._author = author
        self._filename = filename if filename.endswith('.tex') else filename + '.tex'
        self._alignment = alignment
        self._packages = [
            "\\usepackage[utf8]{inputenc}",
            "\\usepackage[T2A]{fontenc}",
            "\\usepackage[russian]{babel}",
            "\\usepackage{array}",
            "\\usepackage{multirow}"
        ]
        self._tables = []
        self._images = []

    def create_table(self, data, caption=None, label=None, alignment=None):
        """
        Creates a new Table object.
        """
        return self.Table(data, caption, label, alignment)

    def create_image(self, path, caption=None, label=None, width="1.0\\textwidth", height=None):
        """
        Creates a new Image object.
        """
        return self.Image(path, caption, label, width, height)

    def add_table(self, table):
        """
        Adds the Table object to the list.
        """
        if not isinstance(table, self.Table):
            raise ValueError("The table must be a Table object.")
        self._tables.append(table)
        return len(self._tables) - 1

    def add_image(self, image):
        """
        Adds the Image object to the list.
        """
        if not isinstance(image, self.Image):
            raise ValueError("The image must be an Image object.")
        self._images.append(image)
        return len(self._images) - 1

    def add_table_from_data(self, data, caption=None, label=None, alignment=None):
        """
        Creates and adds a table from the data.
        """
        table = self.Table(data, caption, label, alignment)
        return self.add_table(table)
    
    def add_image_from_path(self, image_path, caption=None, label=None, width=None, height=None):
        """
        Creates and adds an image from the path.
        """
        image = self.Image(image_path, caption, label, width, height)
        return self.add_image(image)

    def clear_tables(self):
        """
        Clean the table list.
        """
        self._tables.clear()

    def clear_images(self):
        """
        Clean the image list.
        """
        self._images.clear()

    def add_package(self, package):
        """
        Add the package to the list.
        """
        if not isinstance(package, str):
            raise ValueError("The package must be a string.")
        if package not in self._packages:
            self._packages.append(package)

    def save_to_file(self, content, filename=None, encoding='utf-8'):
        """
        Saves the content to a file.
        """
        save_filename = filename or self._filename
        
        with open(save_filename, 'w', encoding=encoding) as f:
            f.write(content)
        
        return save_filename

    def generate_table_content(self, table):
        """
        Generates LaTeX code for a specific table.
        """
        if not isinstance(table, self.Table):
            raise ValueError("The Table object is expected.")
        
        data = table.data
        caption = table.caption
        label = table.label
        alignment = table.alignment or self._alignment
        
        self._validate_data(data)
        num_columns = max(len(row) for row in data)

        table_alignment = alignment or 'c' * num_columns
        
        latex_lines = [
            "\\begin{table}[htbp]",
            "\\centering",
            self._generate_table_header(num_columns, table_alignment),
            "\\hline"
        ]
        
        for i, row in enumerate(data):
            escaped_row = [self._escape_latex_special_chars(cell) for cell in row]
            while len(escaped_row) < num_columns:
                escaped_row.append("")
            
            row_content = " & ".join(escaped_row)
            latex_lines.append(f"{row_content} \\\\")
            
            if i == 0:
                latex_lines.append("\\hline")
        
        latex_lines.extend([
            "\\hline",
            "\\end{tabular}"
        ])
        
        if caption:
            latex_lines.append(f"\\caption{{{self._escape_latex_special_chars(caption)}}}")
        if label:
            latex_lines.append(f"\\label{{{label}}}")
        
        latex_lines.append("\\end{table}")
        
        return "\n".join(latex_lines)

    def generate_image_content(self, image):
        """
        Generates LaTeX code for an image.
        """
        if not isinstance(image, self.Image):
            raise ValueError("The Image object is expected.")
        
        latex_lines = [
            "\\begin{figure}[htbp]",
            "\\centering"
        ]
        image_command = f"\\includegraphics"
        options = []
        if image.width:
            options.append(f"width={image.width}")
        if image.height:
            options.append(f"height={image.height}")
        
        if options:
            image_command += f"[{', '.join(options)}]"
        
        image_command += f"{{{image.image_path}}}"
        latex_lines.append(image_command)
        
        if image.caption:
            latex_lines.append(f"\\caption{{{self._escape_latex_special_chars(image.caption)}}}")
        if image.label:
            latex_lines.append(f"\\label{{{image.label}}}")
        
        latex_lines.append("\\end{figure}")
        
        return "\n".join(latex_lines)

    def generate_and_save_table(self, data, caption=None, label=None, alignment=None, filename=None):
        """
        Generates and saves the table to a file.
        """
        table_content = self.generate_table_content(self.Table(data, caption, label, alignment))
        return self.save_to_file(table_content, filename)

    def generate_and_save_image(self, image_path, caption=None, label=None, width=None, height=None, filename=None):
        """
        Generates and saves the image to a file.
        """
        image_content = self.generate_image_content(self.Image(image_path, caption, label, width, height))
        return self.save_to_file(image_content, filename)

    def generate_and_save_document(self, table_content, filename=None, custom_packages=None):
        """
        Generates and saves the complete document to a file.
        """
        document_content = self.generate_document(table_content, custom_packages)
        return self.save_to_file(document_content, filename)

    def generate_and_save_complete(self, data, caption=None, label=None, alignment=None, 
                                 filename=None, custom_packages=None):
        """
        table generation + document generation + saving to a file.
        """
        table = self.Table(data, caption, label, alignment)
        table_content = self.generate_table_content(table)
        document_content = self.generate_document(table_content, custom_packages)
        return self.save_to_file(document_content, filename)

    def generate_multi_table_document(self, custom_packages=None):
        """
        Generates and saves a document with all tables and images.
        """
        if not self._tables and not self._images:
            raise ValueError("There are no tables or images for document generation.")
        
        packages_to_use = custom_packages if custom_packages is not None else self._packages
        packages_str = "\n".join(packages_to_use)

        tables_content = "\n\n".join(self.generate_table_content(table) for table in self._tables)
        images_content = "\n\n".join(self.generate_image_content(image) for image in self._images)
        
        content = ""
        if tables_content:
            content += tables_content + "\n\n"
        if images_content:
            content += images_content
        
        return f"""\\documentclass{{article}}
{packages_str}

\\title{{{self._escape_latex_special_chars(self._title)}}}
\\author{{{self._escape_latex_special_chars(self._author)}}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

{content}

\\end{{document}}"""

    def generate_and_save_multi_table(self, filename=None, custom_packages=None):
        """
        Generates and saves a document with all tables and images .
        """
        document_content = self.generate_multi_table_document(custom_packages)
        return self.save_to_file(document_content, filename)

    @staticmethod
    def _escape_latex_special_chars(text):
        """
        Escapes LaTeX special characters.
        """
        if not isinstance(text, str):
            text = str(text)
        
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text

    @staticmethod
    def _generate_table_header(num_columns, alignment):
        """
        Generates an aligned table header.
        """
        align = alignment if alignment else 'c' * num_columns
        return f"\\begin{{tabular}}{{{align}}}"

    @staticmethod
    def _validate_data(data):
        """
        Checks the validity of the input data.
        """
        if not data or not any(data):
            raise ValueError("The data cannot be empty")
        
        if not all(isinstance(row, (list, tuple)) for row in data):
            raise ValueError("All data elements must be lists or tuples.")
        
        return True

    def generate_document(self, table_content, custom_packages=None):
        """
        Generates a complete LaTeX document with a table.
        """
        packages_to_use = custom_packages if custom_packages is not None else self._packages
        packages_str = "\n".join(packages_to_use)
        
        return f"""\\documentclass{{article}}
{packages_str}

\\title{{{self._escape_latex_special_chars(self._title)}}}
\\author{{{self._escape_latex_special_chars(self._author)}}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

{table_content}

\\end{{document}}"""
