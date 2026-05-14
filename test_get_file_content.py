from functions.get_file_content import get_file_content

if __name__ == '__main__':
    # print("testing get_file_content with args -> 'calculator', 'lorem.txt'")
    # results = get_file_content("calculator","lorem.txt")
    # print(f"Results:\n{results}")
    print("lorem.txt truncated: True")
    print("testing get_file_content with args -> 'calculator', 'main.py'")
    results = get_file_content("calculator","main.py")
    print(f"Results:\n{results}")
    print("testing get_file_content with args -> 'calculator', 'pkg/calculator.py'")
    results = get_file_content("calculator","pkg/calculator.py")
    print(f"Results:\n{results}")
    print("testing get_file_content with args -> 'calculator', '/bin/cat'")
    results = get_file_content("calculator","/bin/cat")
    print(f"Results:\n{results}")
    print("testing get_file_content with args -> 'calculator', 'pkg/does_not_exist.py'")
    results = get_file_content("calculator","/pkg/does_not_exist.py")
    print(f"Results:\n{results}")
