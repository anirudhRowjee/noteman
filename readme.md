# Noteman  - Command Line Utility to create and manage Notes

Create, Manage and Search your LaTex, Markdown and text notes, all from the
command line.


## FEATURES
1. Create LaTeX, Markdown and Text files in subdirectories of your choice and
   have them open immediately for your editing pleasure
2. Search through these notes - according to filename, path and content inside
   the file
3. Delete Notes that you don't want anymore

## REQUIREMENTS
1. Python 3.x


## USAGE

0. Place the Script in your Home directory and make it executable
```bash
cp noteman.py ~/
cd ..
sudo chmod +x noteman.py
```
Please feel free to set a bash alias/symlink to your PATH. 

1. **Create A Note**
```
./noteman.py create [subdirectory] [filename] [extension (optional)]
```

If an extension is not provided, the extension used to create the file will be
the `_default_file_ext` specified in the python file.
All notes are created in subfolders to the `_root_dir` directory.

For example, if the following command is run - 

`./noteman.py create math/calculus differentiation`

Assuming the default settings, The note file will be created at the path

`~/notes/math/calculus/differentiation.tex`

And your system default `$EDITOR` or Vim will be used to open the file. A
substitution is performed to set the title of the file as the `filename`
argument along with the date and time of the creation. **Please make sure to
include the `\title{&&&}` in the LaTeX template if you wish to retain this
feature whilst modifying the template.**


2. **Deleting a Note**
```
./noteman.py remove [subdirectory] [filename] [extension (optional)]
```

If the extension is provied only that specific file will be deleted. Otherwise
the file with the default extension will be deleted.

3. **Searching Through Your Notes**
```
./noteman.py search [search_term] [deep (optional)]
```

Searching without the `deep` argument will just match your term with the titles
of the files. However, **using the `deep` argument will search for the term IN THE
TEXT/CONTENT OF EACH FILE THAT IS PRESENT, and also matches among titles.**


4. **Seeing all the notes you have**
```
./noteman.py list [subdirectory (optional)]
```

Using the `list` command indexes and matched folder names to `subdirectory` as well if the subdirectory
argument is present. Otherwise, it just provides you with a list of all the
notes present in the `_root_dir` folder with their full paths.
