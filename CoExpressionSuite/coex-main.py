
from CoX import *

glob_dir = input("Enter Directory ")
glob_File_type = input("Enter File Extension ")



size_filter_1 = input("size_filter 1: ")
size_filter_2 = input("size_filer 2: ")
choice = input("enter 1 to measure coexpression, 2 to make coex image, 3 to measure percent coexpression by channel ")

glob_files = glob.glob(glob_dir + '/*' + glob_File_type)
for file in glob_files:
    if choice == str(1):
        co_ex = measure_coex(file, size_filter_1, size_filter_2)
        print(file, co_ex)
        continue
    if choice == str(2):
        make_coex_image(file, size_filter_1, size_filter_2)
        continue
    if choice == str(3):
        per_fil = percent_filter(file, size_filter_1, size_filter_2)
        print(file, per_fil)
        continue
