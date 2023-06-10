#!/usr/bin/env python
# coding: utf-8

# This files brings the latest versions of all the ipynb and css files. Does not overwrite newer or identical versions of files. 

# In[28]:


import os
import re
from sys import exit
import shutil
import glob
import filecmp

def copy_if_modified (file, dest, verbose=False):
    _, tail = os.path.split(file)
    dest_file=os.path.join(dest,tail)
    if os.path.isfile(file) and os.path.isdir(dest) and os.path.isfile(dest_file):
        if os.path.getmtime(file)>os.path.getmtime(dest_file) and not filecmp.cmp(file, dest_file) :
            shutil.copy(file, dest)
            if verbose:
                print(tail+" updated")
        else:
            if os.path.getmtime(file)>os.path.getmtime(dest_file):
                problem=" destination copy is more recent"
            if os.path.isfile(dest_file):
                problem=" files are identical"
            if verbose:
                print(tail+" NOT updated because"+problem)
    elif os.path.isfile(file) and os.path.isdir(dest) and not os.path.isfile(dest_file):
        shutil.copy(file, dest)
        if verbose:
            print(tail+" copied to destination (did not exist there before)")
        
    else:
        print("Unable to copy "+file+" File or destination invalid")

cwd = os.getcwd()
src_folder='fina'
#src_folder='fina'

def most_recent(program):
    u = [int(re.search(r'\d+',x).group()) for x in program]
    to_select=u.index(max(u))
    return program[to_select]


home=os.path.expanduser('~')
src_choices=[os.path.join(home,'Dropbox','Machinegrading',src_folder),os.path.join(home,'Documents','Dropbox','Machinegrading',src_folder)]
if src_choices:
    frm=[x for x in src_choices if os.path.isdir(x)][0]
else:
    sys.exit('origin folder not found. Specify correct path in src_choices')
    
#get latest versions of Grader and MiskTasks
pyfiles=glob.glob(os.path.join(frm, '*.ipynb'))+glob.glob(os.path.join(frm, '*.css'))+glob.glob(os.path.join(frm, '*.py'))
graders=[x for x in pyfiles if "Grader" in x]
miscs=[x for x in pyfiles if "MiscTasks" in x]
toget=[most_recent(graders),most_recent(miscs)]+[x for x in pyfiles if not "Grader" in x and not "MiscTasks" in x and not "Untitled" in x]

print("Bring_files is bringing necessary files from: "+frm)
if cwd!=frm:
    for file in toget:
        _, tail = os.path.split(file)
        copy_if_modified(file, cwd, verbose=True)
else:
    print("Copy this file over to the destination folder and then run it")


# In[27]:


miscs


# In[23]:


u


# In[ ]:




