import sys

def count_stats(text):
    lines = text.count('\n')
    words = len(text.split())
    bytes_count = len(text.encode('utf-8'))
    return lines, words, bytes_count

def process_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            return count_stats(content)
    except FileNotFoundError:
        print(f"{filename}: No such file or directory", file=sys.stderr)
    except IsADirectoryError:
        print(f"'{filename}' is not a file, but a directory.", file=sys.stderr)
    except Exception as e:
        print(f"wc: {filename}: {e}", file=sys.stderr)
    return None

def process_stdin():
    content = sys.stdin.read()
    return count_stats(content)

def format_output(lines, words, bytes_count, filename=None):
    if filename:
        return f"{lines:8d}{words:8d}{bytes_count:8d} {filename}"
    return f"{lines:8d}{words:8d}{bytes_count:8d}"

def main():
    files = sys.argv[1:]
    total_lines, total_words, total_bytes = 0, 0, 0
    results = []
    
    if not files:
        lines, words, bytes_count = process_stdin()
        print(format_output(lines, words, bytes_count))
    else:
        for filename in files:
            result = process_file(filename)
            if result is not None:
                lines, words, bytes_count = result
                results.append((lines, words, bytes_count, filename))
                total_lines += lines
                total_words += words
                total_bytes += bytes_count
        for lines, words, bytes_count, filename in results:
            print(format_output(lines, words, bytes_count, filename))
        if len(results) > 1:
            print(format_output(total_lines, total_words, total_bytes, "total"))

if __name__ == "__main__":
    main()
