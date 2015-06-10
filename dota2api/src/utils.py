import os

def load_json_file(file_name):
    inp_file = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..",
        "ref",
        file_name))
    return inp_file
