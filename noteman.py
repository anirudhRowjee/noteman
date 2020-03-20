#!/usr/bin/python3

'''
Script to generate and manage notes

FEATURES
1. Read presets for directory of notes
2. create subfolders for notes and create files inside them
    * Read command for subfolder
    * change into subfolder
    * create notes file
    * open editor for file
3. Search for notes file by title
4. Search for notes file by content (deep search)
5. Delete notes files

USAGE
notesman create [subdirectory] [filename] [extension]
notesman search [search_term] [deep]
notesman list [subdirectory]
notesman remove [subdirectory] [filename] [extension]
'''

import os
import shutil
import sys
import datetime
import glob
import mmap
from subprocess import call


## Global Constants
_root_dir = "notes"
_default_file_ext = "tex"
_editor = os.environ.get('EDITOR', 'vim')


_latex_template = r"""
\title{&&&}
\author{ ME }

\documentclass{article}

\begin{document}
\maketitle

\section{Introduction}
Some Introduction goes here

\end{document}
"""

_markdown_template = r"""#{title}

"""

_txt_template = r"""{title}

"""

extension_template_map = {
    'tex': _latex_template,
    'md': _markdown_template,
    'txt':_txt_template,
}


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

## CORE FUNCTIONS

def print_success(text):
    print(f"{bcolors.OKGREEN}{text}{bcolors.ENDC}")

def print_failure(text):
    print(f"{bcolors.FAIL}{text}{bcolors.ENDC}")

def print_warning(text):
    print(f"{bcolors.WARNING}{text}{bcolors.ENDC}")

def dir_create_if_not_exist(path):
    '''
    check if a directory exists. if not, create it
    '''
    if not os.path.exists(path):
        os.makedirs(path)

def format_template(title, ext):
    if ext == 'tex':
        template = extension_template_map[ext].split('&&&')
        new_template = r"{}".format(str(template[0]) + str(title) +
                                    str(template[1]))
        return new_template
    else:
        return extension_template_map[ext].format(title=title)



def open_editor(path_relative_to_root, filename, extension):
    '''
    function to open the editor on a given filename
    '''

    # get folder path for creation (if necessary)
    folder_path = "{root}/{path}/".format(root = _root_dir, path = path_relative_to_root)
    dir_create_if_not_exist(folder_path)

    #print("Folder Path Assembles as ", folder_path)

    # assemble full path from given arguments
    full_path = "{root}/{path}/{filename}.{extension}".format(root = _root_dir,
                                                              path = path_relative_to_root,
                                                              filename = filename,
                                                              extension = extension)
    #print("Full Path Assembles as ", full_path)

    # if file already exists, throw options
    if os.path.isfile(full_path):

        choice = int(input(f"{bcolors.WARNING}File Already Exists! 1 - Overwrite, 2 - open for editing >>> {bcolors.ENDC}"))

        if choice == 2:

            call([_editor, full_path])

        elif choice == 1:

            # check if template for extension exists, if so, write to file
            template = extension_template_map[extension]

            if template:
                title = "{title} ({time})".format(title=filename, time=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                with open(full_path, 'w+') as target:
                    target.write(format_template(title, extension))

            call([_editor, full_path])

    else:

        # check if template for extension exists, if so, write to file
        template = extension_template_map[extension]

        if template:
            title = "{title} ({time})".format(title=filename, time=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            with open(full_path, 'w+') as target:
                target.write(format_template(title, extension))

        call([_editor, full_path])



def delete(path_relative_to_root, filename, extension=_default_file_ext):

    # get folder path for deletion
    folder_path = "{root}/{path}/".format(root = _root_dir, path = path_relative_to_root)

    # assemble full path from given arguments
    full_path = "{root}/{path}/{filename}.{extension}".format(root = _root_dir,
                                                              path = path_relative_to_root,
                                                              filename = filename,
                                                              extension = extension)
    if os.path.exists(full_path):
        os.remove(full_path)
        print_success("Note at {} removed successfully".format(full_path))
    else:
        print_failure("NOTE DOES NOT EXIST!")


def matches_search(filepath, term):
    # check in title for match to search
    if term in filepath.split('/')[-1]:
        return True
    else:
        return False

def shallow_search(term):
    # search in all filenames and created times for term
    files = [y for y in [x for x in [f for f in glob.iglob(_root_dir + '**/**', recursive=True)] if not os.path.isdir(x)] if matches_search(y, term)]
    print("SEARCH RESULTS")
    if files:
        for file in files:
            print_success(file)
    else:
        print_failure("NO RESULTS FOUND")

def deep_search(term):
    files = [x for x in [f for f in glob.iglob(_root_dir + '**/**', recursive=True)] if not os.path.isdir(x)]
    matched = []
    for file in files:
        # stackoverflow magic incoming
        with open(file, 'rb', 0) as target, mmap.mmap(target.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(str("{}".format(term)).encode()) != -1:
                matched.append(file)
        if matches_search(file, term):
            if file not in matched: matched.append(file)
    print("SEARCH RESULTS")
    if matched:
        for file in matched:
            print_success(file)
    else:
        print_failure("NO RESULTS FOUND")


def list_notes(path=_root_dir):
    # just show a list of all the files present
    files = [x for x in [f for f in glob.iglob(_root_dir + '**/**', recursive=True)] if not os.path.isdir(x)]
    files_filtered = [x for x in files if path in x]
    print("LIST")
    if files_filtered:
        for file in files_filtered:
            print(file)
    else:
        print_warning("No Files Present")

if __name__ == '__main__':

    # check if _root_dir exists, if not create it
    dir_create_if_not_exist(_root_dir)
    args = sys.argv[1:]

    command = args[0].lower()

    if command == 'create':
        # create and open file
        if len(args) == 3:
            # assume default file extension
            open_editor(args[1], args[2], _default_file_ext )
        elif len(args) == 4:
            # file extension provided
            open_editor(args[1], args[2], args[3])
        else:
            print_failure("Invalid Arguments")

    if command == 'search':
        # search in file titles and for deep search, search by text in file,
        # return positive matched filenames
        if len(args) == 2:
            # shallow search - search only in titles and created date and times
            shallow_search(args[1])
        elif len(args) == 3 and args[2] == 'deep':
            # deep search - not just shallow search, but match text in file as
            # well
            deep_search(args[1])
        else:
            print_failure("Invalid Arguments")

    if command == 'list':
        # show tree listing of notes
        if len(args) == 1:
            # list all subdirectories and notes
            list_notes()
        elif len(args) == 2:
            # subdirectory name provied
            list_notes(args[1])
        else:
            print_failure("Invalid Arguments")

    if command == 'remove':
        # remove notes
        if len(args) == 3:
            # remove default exetension file
            delete(args[1], args[2])
        elif len(args) == 4:
            # specific extension provied
            delete(args[1], args[2], args[3])
        else:
            print_failure("Invalid Arguments")

