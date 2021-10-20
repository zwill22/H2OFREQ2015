import os


def switch_folder(path, func, *args):
    for folder in os.listdir(path):
        full_path = os.path.join(path, folder)
        if not os.path.isdir(full_path):
            continue
        if folder[0] == ".":
            continue 
        func(full_path, *args)


def ls(path):
    for doc in os.listdir(path):
        print(doc)


def remove_aux(path, valid_exts):
    for doc in os.listdir(path):
        ext = doc.split(".")[-1]
        if ext not in valid_exts:
            os.remove(os.path.join(path, doc))    


def list_exts(path):
    exts = []
    for doc in os.listdir(path):
        ext = doc.split(".")[-1]
        if ext not in exts:
            exts.append(ext)

    print(exts)


def main():
    pwd = os.getcwd()
    valid_exts = ["out", "in", "sub", "xyz"]
    switch_folder(pwd, lambda x: remove_aux(x, valid_exts))


if __name__ == "__main__":
    main()


