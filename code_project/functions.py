# This file contains all functions

# Import section
import markdown as md
from shutil import copyfile
from os import listdir as ls
from os import mkdir as make
from os import rmdir as remove
from os import path
from os import walk


# function section declaration
def md_to_html(source, target, css=None):
    """
    this function convert a markdown file to an HTML file
    :param css: css file to add
    :param target:
    :param source: source file
    :return: an output file in html
    """
    # Creat a path
    src = str.format('{}', source)
    out = str.format('output/{}', target)
    name, ex = get_extension(src)
    if ex == '.md':
        md.markdownFromFile(
            input=src,
            output=out,
            encoding='utf8'
        )
        # add footer and header
        add_header_and_footer(target, css)
    else:
        print("le fichier {} n'est un fichier Markdown, il ne va pas être converti !".format(src))
        copyfile(src, "{}{}".format(name, ex).replace('input', 'output'))


def get_target(src):
    """
    this functions is used to get html target file name
    :param src: the source file Markdown
    :return: target: the target name
    """
    target = src.replace(".md", ".html").replace("input", "")
    return target


def get_all_files(path_src):
    """
    this function read all files from input folder
    :return: list of all files
    """
    root_dir = ls(path_src)
    files = list()

    for element in root_dir:
        element_path = path.join(path_src, element)
        if path.isdir(element_path):
            try:
                make(element_path.replace('input', 'output'))
            except FileExistsError:
                print("Le dossier {} existe déjà, il va étre remplacer !".format(element_path))
                try:
                    remove(element_path.replace('input', 'output'))
                    make(element_path.replace('input', 'output'))
                except OSError:
                    print("Erreur lors de remplacement de dossier {} ".format(element_path))

            files = files + get_all_files(element_path)
        else:
            files.append(element_path)

    list_of_files = list()
    for (dirpath, dirnames, filenames) in walk(path_src):
        list_of_files += [path.join(dirpath, file) for file in filenames]

    return list_of_files


def add_header_and_footer(src, css=None):
    """
    this function add the header to HTML file
    :return: the new HTML file with header
    """
    try:
        src = str.format('output\\{}', src)
        content = get_content(src)
        header, footer = get_header_and_footer()
        html = open(src, 'r+')
        if css is None:
            html.write(header + "\n" + content + "\n" + footer)
        else:
            html.write(header.replace("<span></span>", add_css_code(css)) + "\n" + content + "\n" + footer)
        html.close()
    except FileNotFoundError:
        print("Le fichier {} n'existe pas ou endomagé !".format(src))
        return
    return html


def get_header_and_footer():
    """
    this function read header and footer HTML
    :return: (header, footer)
    """
    with open('code_project/assets/header.html', 'r') as head_file:
        header = head_file.read()
    with open('code_project/assets/footer.html') as feet_file:
        footer = feet_file.read()
    return header, footer


def get_content(src):
    """
    this function get content of a given file (src path)
    :param src:
    :return: the content of the file
    """
    with open(src, 'r+') as file:
        content = file.read()
        return content


def is_css(file):
    """
    this function check is it's a css file or scss
    :param file: the given file
    :return: true of false
    """
    _, ex = path.splitext(file)
    if ex == '.css' or ex == '.scss':
        return True
    else:
        return False


def get_extension(file):
    """
    this function get the extension of the given file
    :param file: given file
    :return: name, extension
    """
    return path.splitext(file)


def add_css_code(lise):
    """
    this function add css code
    :param lise: input list of files
    :return: code to add
    """
    css_balise = "<link rel=\"stylesheet\" href=\"{}\">\n"
    code = ""
    for el in lise:
        css_file = el.replace('input', '').replace('\\', '/')
        code += css_balise.format(css_file)

    return code
