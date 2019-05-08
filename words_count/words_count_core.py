import ast
import os
import collections

from service_funcs import flat, is_verb


def get_trees(dirpath, with_filenames=False, with_file_content=False):
    filenames = []
    trees = []
    for dirname, dirs, files in os.walk(dirpath, topdown=True):
        for file in files:
            if file.endswith('.py') and len(filenames) < 100:
                filenames.append(os.path.join(dirname, file))
    print('total %s files' % len(filenames))
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None
        if with_filenames:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
    print('trees generated')
    return trees


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_all_words_in_path(dirpath):
    trees = [t for t in get_trees(dirpath) if t]
    names = [get_all_names(t) for t in trees]
    function_names = [f for f in flat(names) if not (f.startswith('__') and f.endswith('__'))]
    words = []
    for function_name in function_names:
        words += [n for n in function_name.split('_') if n]
    return words


def get_top_verbs_in_path(dirpath, top_size=10):
    trees = [t for t in get_trees(dirpath) if t]
    nodes = []
    for t in trees:
        nodes += [node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)]
    function_names = [f for f in nodes if not (f.startswith('__') and f.endswith('__'))]
    print('functions extracted')
    verbs = flat([get_verbs_from_function_name(function_name) for function_name in function_names])
    return collections.Counter(verbs).most_common(top_size)


def get_top_functions_names_in_path(dirpath, top_size=10):
    nodes = []
    for t in get_trees(dirpath):
        nodes += [node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)]
    nms = [f for f in nodes if not (f.startswith('__') and f.endswith('__'))]
    return collections.Counter(nms).most_common(top_size)


if __name__ == "__main__":
    wds = []
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]
    for project in projects:
        dirpath = os.path.join('.', project)
        wds += get_top_verbs_in_path(dirpath)

    top_size = 200
    print('total %s words, %s unique' % (len(wds), len(set(wds))))
    for word, occurence in collections.Counter(wds).most_common(top_size):
        print(word, occurence)
