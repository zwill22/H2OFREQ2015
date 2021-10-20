import os
import pandas as pd


def get_orca_mol_data(folder: str, file: str):
    mol = file.split(".")[0]
    i = 0
    read = False
    results = {}
    idx = 1
    for line in open(os.path.join(folder, file)):
        if read:
            i += 1
            if i > 4:
                if line == '\n':
                    break
                if "The first frequency considered" in line:
                    break
                l = line.split(' ')
                l = [x for x in l if x != '']
                if 'i' in l:
                    print("Not minimised: {}".format(mol))
                    return
                k = 7 if l[3] == '(' else 6
                assert len(l) == k, "Incorrect number of values in table: {}".format(l)

                results[mol + "_" + str(idx)] = float(l[1])
                idx += 1
        if "IR SPECTRUM" in line:
            read = True

    return results


def get_mol_data(folder: str, file: str):
    mol = file.split(".")[0]
    i = 0
    print_lines = False
    results = {}
    idx = 1
    for line in open(os.path.join(folder, file)):

        if print_lines:
            i += 1
            if i > 1:
                if line == '\n':
                    break
                if "Saving results in set" in line:
                    print_lines = False
                    output = ''
                    i = 0
                    idx = 1
                    continue
                l = line.split(' ')
                l = [x for x in l if x != '']
                if 'i' in l:
                    print("Not minimised: {}".format(mol))
                    return
                assert len(l) == 2, l
                fn = int(l[0])
                if mol in ["02_C2H2", "08_ClCN", "10_CO2", "12_CS2", "20_HCN", "26_N2O", "27_OCS"]:
                    if i == 2:
                        results[mol + "_" + str(idx)] = float(l[1])
                        idx += 1
                results[mol + "_" + str(idx)] = float(l[1])
                idx += 1

        if "Vibrational frequencies" in line:
            print_lines = True

    return results


def check_program(path):
    for file in os.listdir(path):
        if file.endswith('.out'):
            for line in open(os.path.join(path, file)):
                if '* O   R   C   A *' in line:
                    return 'orca'
                if '[ Qcore ]' in line:
                    return 'qcore'
            return 'none'
    return 'none'


def get_results(folder, get_data):
    all_results = {}
    for file in os.listdir(folder):
        if file.endswith(".out"):
            mol_results = get_data(folder, file)
            all_results = {**all_results, **mol_results}

    return all_results


def get_qcore_results(folder):
    return get_results(folder, get_mol_data)


def get_orca_results(folder):
    return get_results(folder, get_orca_mol_data)


def main():
    results = {}
    path = os.path.abspath('.')
    for folder in os.listdir(path):
        full_path = os.path.join(path, folder)
        if not os.path.isdir(full_path):
            continue
        if folder[0] == '_' or folder[0] == '.':
            continue
        program = check_program(full_path)
        if program == 'orca':
            results[folder] = get_orca_results(full_path)
        elif program == 'qcore':
            results[folder] = get_qcore_results(full_path)
        elif program == 'none':
            continue
        else:
            raise ValueError('Unknown program')

    pd.DataFrame(results).to_csv("freq.csv")
    

if __name__ == '__main__':
    main()
