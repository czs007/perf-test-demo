REP_KEYS_MAP = {
    "perf":('ROWS', 'REP_SET_NAMES', 'REP_DATASETS', 'REP_FUNC_NAMES'),
    "scale": ('REP_NODES', 'REP_SET_NAMES', 'REP_DATASETS', 'REP_FUNC_NAMES'),
}

def read_and_replace(data_path, mode):
    string_data = ""
    with open (data_path, "r") as f:
        lines = f.readlines()
        string_data = "".join(lines)
    string_data = string_data or "{}"
    import ast
    eval = ast.literal_eval
    rep_data = eval(string_data)
    assert rep_data

    rep_keys = REP_KEYS_MAP[mode]

    with open (template_path, "r") as f:
        lines = f.readlines()
        all_string = "".join(lines)
        for k in rep_keys:
            v = rep_data[k]
            all_string = all_string.replace(k, str(v))

    if all_string:
        with open (output_path, "w") as f:
            f.write(all_string)

def print_help():
    print('python gen_perf_html.py  -m <mode> -t <template_path> -d <data_path> -o <output_path>')

if __name__ == "__main__":

    import sys
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], "-m:-t:-d:-o:-h",['mode', 'template_path','data_path', 'output_path', 'help'])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    template_path = ""
    data_path = ""
    output_path = ""
    mode = ""

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-t", "--template_path"):
            template_path = arg
        elif opt in ("-d", "--data_path"):
            data_path = arg
        elif opt in ("-o", "--output_path"):
            output_path = arg

    if "" in (template_path, data_path, output_path, mode):
        print_help()
        sys.exit()

    if mode not in REP_KEYS_MAP:
        print_help()
        sys.exit()

    read_and_replace(data_path, mode)
