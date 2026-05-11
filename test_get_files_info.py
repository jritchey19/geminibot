from functions.get_files_info import get_files_info

if __name__ == '__main__':
    print("testing get_files_info function, args -> 'calculator', '.':")
    results_calc_root = get_files_info("calculator",".")
    print(f"Results for current Directory:\n{results_calc_root}")
    print("testing get_files_info function, args -> 'calculator', 'pkg':")
    results_calc_pkg = get_files_info("calculator","pkg")
    print(f"Results for 'pkg' Directory:\n{results_calc_pkg}")
    print("testing get_files_info function, args -> 'calculator', '/bin':")
    results_calc_slash_bin = get_files_info("calculator","/bin")
    print(f"Results for '/bin' Directory:\n{results_calc_slash_bin}")
    print("testing get_files_info function, args -> 'calculator', '../':")
    results_calc_dot_dot_slash = get_files_info("calculator","../")
    print(f"Results for '../' Directory:\n{results_calc_dot_dot_slash}")

