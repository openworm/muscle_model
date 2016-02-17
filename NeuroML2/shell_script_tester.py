import os
import subprocess as sp


def collect_files(extension = ".sh"):
    '''
    Collects all the files with a particular extension from the current working directory
    :param extension: extension of files that are to be collected
    :return: list containing all the names of files with a given extension
    '''

    # Initialize empty list for collecting all required files
    file_list = []

    # This for loop collects all the required files from current working directory
    for each_file in os.listdir(os.getcwd()):
        if each_file.endswith(extension):
            file_list.append(each_file)

    return file_list

def shell_script_tester(file_list):
    '''
    Tests all the shell scripts based on its exit code
    :param file_list: contains files that are to be tested
    :return: exitcode of each file
    '''
    for each_script in file_list:
        file_name = ' "./' +each_script+'"'
        result = sp.Popen(file_name, shell=True)
        returncode = result.returncode

        if returncode == 0:
            print(file_name+'\n Executed Successfully with code:'+str(returncode))
        else:
            print(file_name+'\n Execution failed with code:'+str(returncode))

print collect_files()
shell_script_tester(collect_files)