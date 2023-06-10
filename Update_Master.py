#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import re
from sys import exit
import shutil
import glob
import filecmp
from datetime import datetime

copy_to_fina=True



def copy_if_modified (file, dest, verbose=False):
    _, tail = os.path.split(file)
    dest_file=os.path.join(dest,tail)
    problem1=''
    problem2=''
    if os.path.isfile(file) and os.path.isdir(dest) and os.path.isfile(dest_file):
        if os.path.getmtime(file)>os.path.getmtime(dest_file) and not filecmp.cmp(file, dest_file) :
            shutil.copy(file, dest)
            if verbose:
                print(tail+" updated")
        else:
            if os.path.getmtime(file)>os.path.getmtime(dest_file):
                problem1=" destination copy is more recent"
            if os.path.isfile(dest_file):
                problem2=" files are identical"
            if problem1 and problem2:
                problem=problem1+" and "+problem2
            else:
                problem=problem1+problem2
            if verbose:
                print(tail+" NOT updated because"+problem)
    elif os.path.isfile(file) and os.path.isdir(dest) and not os.path.isfile(dest_file):
        shutil.copy(file, dest)
        if verbose:
            print(tail+" copied to destination (did not exist there before)")
        
    else:
        print("Unable to copy "+file+" File or destination invalid")

def most_recent(program):
    u = [int(re.search(r'\d+',x).group()) for x in program]
    to_select=u.index(max(u))
    return program[to_select]


def is_accessible(path, mode='w+'):
    """
    Check if the file or directory at `path` can
    be accessed by the program using `mode` open flags.
    """
    try:
        f = open(path, mode)
        f.close()
    except IOError:
        return False
    return True
        
def write_log(destination):
    filename = 'update_log.txt'
    logfilepath = os.path.join(destination, filename)
    if is_accessible(logfilepath, 'w+'):
        with open(os.path.join(destination, filename), 'w+') as temp_file:
            temp_file.write("Files last updated at "+str(datetime.now()))
        print("Log file updated")
    else:
        print("Update file not accessible")

cwd = os.getcwd()

home=os.path.expanduser('~')
dst_choices=[os.path.join(home,'Dropbox','Machinegrading'),os.path.join(home,'Documents','Dropbox','Machinegrading')]
if dst_choices:
    the_dst=[x for x in dst_choices if os.path.isdir(x)][0]
    dst=os.path.join(the_dst,'Master')
else:
    sys.exit('destination folder for Master location not found. Specify correct path in dst_choices')



#collect the latest versions of Grader and MiskTasks and other ipynb files    
pyfiles=glob.glob("*.ipynb")+glob.glob('*.css')+glob.glob('*.py')
graders=[x for x in pyfiles if "Grader" in x]
miscs=[x for x in pyfiles if "MiscTasks" in x]
files_to_update=[most_recent(graders),most_recent(miscs)]+[x for x in pyfiles if not "Grader" in x and not "MiscTasks" in x and not "Untitled" in x]

if dst!=cwd:
    print("Update_Master is updating changes to Master at "+str(datetime.now()))
    for src in files_to_update:
        #print(src+" updated to Machinegrading")
        copy_if_modified(src, dst,verbose=True)
    write_log(dst)
    
    
#copy to fina
if copy_to_fina:
    print("____________________________________________")
    dst1=os.path.join(the_dst,'fina')
    if os.path.isdir(dst1) and dst1!=cwd:
        print("Update_Master is updating changes to fina:")
        for src in files_to_update:
            copy_if_modified(src, dst1,verbose=True)
    write_log(dst1)
else:
    print('Not updating fina as instructed. Change copy_to_fina to True for fina backup')


    
    


# In[ ]:




