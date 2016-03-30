import os
import subprocess as sp
import pytest
import matplotlib
matplotlib.use('Agg')

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

def test_shell_scripts(file_list = collect_files()):
    '''
    Tests all the shell scripts based on its exit code
    :param file_list: contains files that are to be tested
    :return: exitcode of each file
    '''
    returncode_list = []
    for each_script in file_list:
        file_name = ' "./' +each_script+'"'

        returncode = sp.call(file_name+' -nogui', shell=True)
        returncode_list.append(returncode)


    for i in range(len(file_list)):
        assert(returncode_list[i] == 0),"Test Failed for " + file_list[i]
        print("test passed for " + file_list[i])
