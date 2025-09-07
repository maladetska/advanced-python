import sys

def number_lines(input_source, output=sys.stdout):
    line_number = 1
    for line in input_source:
        output.write(f"{line_number:6d}\t{line}")
        line_number += 1

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                number_lines(file)
        except FileNotFoundError:
            print(f"Error: file '{filename}' not found", file=sys.stderr)
            sys.exit(1)
        except IOError as e:
            print(f"Error reading the file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        number_lines(sys.stdin)

if __name__ == "__main__":
    main()
