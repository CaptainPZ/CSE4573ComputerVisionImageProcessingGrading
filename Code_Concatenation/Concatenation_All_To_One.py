from Utils import *




def combine_all(dir,  file_ls, out_file_name):

    all_contents = []
    all_contents.append("2019 Spring Submissions\n\n")
    for file in file_ls:
        file = os.path.join(dir, file)
        with open(os.path.join( file)) as f:
            lines = f.read().splitlines()
        all_contents.extend(lines)

    all_contents.append("\n\n\n")

    with open(out_file_name, 'w') as f:
        for line in all_contents:
            f.write(line + '\n')

    return



# concatenate all files in one folder to just one py file

dir = "./out"  # dir to all python scripts to be concatenated

combine_all(dir, os.listdir(dir), "2019SpringAll.py")