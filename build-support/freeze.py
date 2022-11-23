import json
import sys

import toml


def get_all_resolves():
    conf = toml.load("pants.toml")
    return [k for k in conf["python"]["resolves"]]


def show_all_resolves():
    for k in get_all_resolves():
        print(k)


def print_freeze(resolve: str):
    if resolve not in get_all_resolves():
        print("Here is a list of available resolves:")
        show_all_resolves()
        return
    conf = toml.load("pants.toml")
    resolve_file = conf["python"]["resolves"][resolve]
    with open(resolve_file) as f:
        meta_lines = [line[3:] for line in f.readlines() if line.startswith("// ")]
        meta_text = "".join(meta_lines[3:-1])
        meta_json = json.loads(meta_text)
        for req in meta_json["generated_with_requirements"]:
            print(req)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        show_all_resolves()
        exit(0)
    elif len(sys.argv) > 1:
        print_freeze(sys.argv[1])
