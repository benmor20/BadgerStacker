import os


def path_to(rel_path: str):
    return '\\..\\'.join([os.path.realpath(__file__), rel_path])
