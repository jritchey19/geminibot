from functions.write_to_file import write_to_file

if __name__ == '__main__':
    print("testing write_to_file func with -> calculator, lorem.txt, 'wait, this isn\'t lorem ipsum'")
    results = write_to_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(f"Results:\n{results}")
    print("testing write_to_file func with -> calculator, pkg/morelorem.txt, 'lorem ipsum dolor sit amet'")
    results = write_to_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(f"Results:\n{results}")
    print("testing write_to_file func with -> calculator, /tmp/temp.txt, 'this should not be allowed")
    results = write_to_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(f"Results:\n{results}")
