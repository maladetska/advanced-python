def escape_latex_special_chars(text):
    """Escape LaTeX special characters"""
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

def validate_data(data):
    """
    Checks the validity of the input data.
    """
    if not data or not any(data):
        raise ValueError("The data cannot be empty")
    
    if not all(isinstance(row, (list, tuple)) for row in data):
        raise ValueError("All data elements must be lists or tuples.")
    
    return True

def generate_table_header(num_columns, alignment):
    """
    Generates an aligned table header.
    """
    align = alignment if alignment else 'c' * num_columns
    return f"\\begin{{tabular}}{{{align}}}"

def generate_table_content(data, caption=None, label=None, alignment=None):
    """
    Generates LaTeX code for a specific table.
    """
    validate_data(data)
    num_columns = max(len(row) for row in data)
    table_alignment = alignment or 'c' * num_columns
    
    latex_lines = [
        "\\begin{table}[htbp]",
        "\\centering",
        generate_table_header(num_columns, table_alignment),
        "\\hline"
    ]
    
    for i, row in enumerate(data):
        escaped_row = [escape_latex_special_chars(cell) for cell in row]
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
        latex_lines.append(f"\\caption{{{escape_latex_special_chars(caption)}}}")
    if label:
        latex_lines.append(f"\\label{{{label}}}")
    
    latex_lines.append("\\end{table}")
    
    return "\n".join(latex_lines)

def generate_image_content(image_path, caption=None, label=None, width="1.0\\textwidth", height=None):
    """
    Generates LaTeX code for an image.
    """
    latex_lines = [
        "\\begin{figure}[htbp]",
        "\\centering"
    ]
    
    image_command = "\\includegraphics"
    
    options = []
    if width:
        options.append(f"width={width}")
    if height:
        options.append(f"height={height}")
    
    if options:
        image_command += f"[{', '.join(options)}]"
    
    image_command += f"{{{image_path}}}"
    latex_lines.append(image_command)
    
    if caption:
        latex_lines.append(f"\\caption{{{escape_latex_special_chars(caption)}}}")
    if label:
        latex_lines.append(f"\\label{{{label}}}")
    
    latex_lines.append("\\end{figure}")
    
    return "\n".join(latex_lines)

def generate_document(title, author, content, packages):
    """
    Generates a complete LaTeX document with a table.
    """
    packages_str = "\n".join(packages)
    
    return f"""\\documentclass{{article}}
{packages_str}

\\title{{{escape_latex_special_chars(title)}}}
\\author{{{escape_latex_special_chars(author)}}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

{content}

\\end{{document}}"""

def save_to_file(content, filename, encoding='utf-8'):
    """
    Saves the content to a file.
    """
    with open(filename, 'w', encoding=encoding) as f:
        f.write(content)
    
    return filename
