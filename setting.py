import os

working_dir = "DocFormatter"
modified_file_dir = "Modified file"
csv_file_dir = "csv files"
excel_file_dir = "excel files"
docx_file_dir = "docx files"
def initialize():
    try:
        cwd = os.chdir("C:/")
        if working_dir not in os.listdir(cwd):
            os.mkdir(working_dir)
            os.chdir(working_dir)
            if modified_file_dir not in os.listdir(cwd):
                os.mkdir(modified_file_dir)
                os.chdir(modified_file_dir)

            else:
                os.chdir(modified_file_dir)
        else:
            os.chdir(working_dir)
            if modified_file_dir not in os.listdir(cwd):
                os.mkdir(modified_file_dir)
                os.chdir(modified_file_dir)
            else:
                os.chdir(modified_file_dir)
            pass
    except:
        pass

def file_exist(fname):
    listdir = os.listdir(os.getcwd())
    if fname in listdir:
        return True
    else:
        return False

def separate_dir():
    dir = [csv_file_dir, excel_file_dir, docx_file_dir]
    initialize()
    cwd = os.getcwd()
    for i in dir:
        if i not in os.listdir(cwd):
            os.mkdir(i)
            print(f"directory named [{i}] created.")
        else:
            pass

#separate_dir()


def run_mul(func:list, args:list):
    for i in range(len(args)):
        if args[i]:
            func[i]()
        else:
            pass

"""
def print1():
    print(1)

def print2():
    print(2)

def print3():
    print(3)

funcList = [print1, print2, print3]
bol = (True, True,False)

run_mul(funcList, bol)"""