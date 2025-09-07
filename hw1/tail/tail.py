import sys

def tail_file(filename, line_count=10, output=sys.stdout):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            last_lines = lines[-line_count:] if len(lines) > line_count else lines
            
            for line in last_lines:
                output.write(line)
                
    except FileNotFoundError:
        print(f"File '{filename}' cannot be opened: there is no such file or directory", file=sys.stderr)
    except PermissionError:
        print(f"You have no permission for file '{filename}'", file=sys.stderr)
    except IsADirectoryError:
        print(f"'{filename}' is not a file, but a directory.", file=sys.stderr)
    except Exception as e:
        print(f"Error in reading '{filename}': {e}", file=sys.stderr)

def tail_stdin(line_count=17, output=sys.stdout):
    lines = sys.stdin.readlines()
    last_lines = lines[-line_count:] if len(lines) > line_count else lines
    
    for line in last_lines:
        output.write(line)

def main():
    files = sys.argv[1:]
    
    if not files:
        tail_stdin(17)
    else:
        multiple_files = len(files) > 1
        
        for i, filename in enumerate(files):
            if multiple_files:
                if i > 0:
                    print()
                print(f"==> {filename} <==")
            
            tail_file(filename, 10)

if __name__ == "__main__":
    main()
