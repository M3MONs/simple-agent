from functions.get_file_content import get_file_content

if __name__ == "__main__":
    print("Testing get_file_content(\"calculator\", \"lorem.txt\"):")
    result = get_file_content("calculator", "lorem.txt")
    print(f"Length: {len(result)}")
    if result.endswith(f'[...File "lorem.txt" truncated at {10000} characters]'):
        print("Truncation message present.")
    else:
        print("No truncation message.")
    print()

    print("get_file_content(\"calculator\", \"main.py\"):")
    result = get_file_content("calculator", "main.py")
    print(result)
    print()

    print("get_file_content(\"calculator\", \"pkg/calculator.py\"):")
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)
    print()

    print("get_file_content(\"calculator\", \"/bin/cat\"):")
    result = get_file_content("calculator", "/bin/cat")
    print(result)
    print()

    print("get_file_content(\"calculator\", \"pkg/does_not_exist.py\"):")
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)
    print()