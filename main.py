"""
The main file of the project
"""
# Import section
from code_project.functions import *
import os

if __name__ == "__main__":
    # read all files from input folder
    files = get_all_files('input\\')
    css_files = []

    for file in files:
        if is_css(file):
            css_files.append(file)

    if len(css_files) == 0:
        css_files = None
    else:
        print("Fichiers CSS detectés !")

    for md in files:
        print(get_target(md))
        md_to_html(md, get_target(md), css_files)
