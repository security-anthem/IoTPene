import csv
import os
import sys

from .exploit_database import *
from .cve_database import *

db_path = "./api/"

def will_exit_after_call(func):
    def wrapper():
        func()
    sys.exit(0)

def check_db_exist():
    global db_path
    now_path = os.path.abspath('.').lstrip(os.path.abspath('../'))
    if now_path == 'IoTPene':
        db_path = os.path.abspath('.') + '/api'
        return os.path.exists(os.path.abspath('./api/exploit-database'))
    elif now_path == 'api':
        db_path = os.path.abspath('.')
        return os.path.exists(os.path.abspath('./exploit-database'))
    else:
        print("path must in IoTpene or IoTPene/api")
        sys.exit(0)

# @will_exit_after_call
def print_usage(argv :list):
    print("---------------------")
    print("|      db   API     |")
    print("---------------------")
    print("")
    print("Command:")
    print("search: Search information about db")
    print("usage: search [CVE] || [db ID] || 'penetrate ")
    print("get: Get script of db by Id")
    print("usage: get    [CVE] || [db ID]")
    print("update: Update db data")
    print("usage: update all || db || cve")
    print("")
    print("Example:")
    print("search CVE")
    print("get CVE")
    print("update")
    sys.exit(0)


# @will_exit_after_call
def search(argv :list):
    query_string = argv[3]

    if query_string[0 : 3].upper() == "CVE":
        return search_by_cve(query_string)
    elif query_string.isnumeric():
        if not search_by_id(query_string):
            return search_by_keywords(argv[3:])
    else:
        argv.append('-t')
        return search_by_keywords(argv[3:])
    sys.exit(0)

    
# @will_exit_after_call
def get(argv :list):
    query_string = argv[3]
    exploit_files = open(db_path + "/exploit-database/files_exploits.csv", errors="ignore")
    shellcode_files = open(db_path + "/exploit-database/files_shellcodes.csv", errors="ignore")
    exploit_reader = csv.reader(exploit_files)
    shellcode_reader = csv.reader(shellcode_files)

    next(exploit_reader)
    next(shellcode_reader)

    def get_script_by_id(id, reader):
        for row in reader:
            edb, file, description, date, author, platform, type, port = tuple(row)
            file_route = ''
            print('file', file_route)
            if edb == id:
                file_route = db_path + "/exploit-database/" + file
                exploit_script = open(file_route)
                print(exploit_script.read())
                exploit_script.close()
        return file_route

    res = ''
    if query_string[0 : 3].upper() == "CVE":
        if not query_string.upper() in exploit_cve_map:
            exploit_files.close()
        exploit_db_id_list = exploit_cve_map.get(query_string)
        if len(exploit_db_id_list) > 1:
            print("Total length of DB list: {}".format(len(exploit_db_id_list)))
            print("Id list: ", *exploit_db_id_list)
            for id in exploit_db_id_list:
                search_by_id(id)
            print("Input DB Id to get a script")
        elif len(exploit_db_id_list) == 1:
            res = get_script_by_id(exploit_db_id_list[0], exploit_reader)
        else:
            print("Exploit: No Results")

    elif query_string.isnumeric():
        print(exploit_db_id_map)
        if query_string in exploit_db_id_map:
            res = get_script_by_id(query_string, exploit_reader)
        elif query_string in shellcode_db_id_map:
            res = get_script_by_id(query_string, shellcode_reader)
        else:
            print("No script found")

    exploit_files.close()
    shellcode_files.close()
    return res
    # sys.exit(0)
    

# @will_exit_after_call
def update(argv :list):
    query_string = argv[3]
    if query_string == "all":
        update_db()
        update_shellcode_cve_json()
        update_shellcode_cve_json()
    if query_string == "db":
        update_db()
    if query_string == "cve":
        update_shellcode_cve_json()
        update_shellcode_cve_json()
    sys.exit(0)
    

options = {"--help":    print_usage,
           "-h":        print_usage,
           "help":      print_usage,
           "search":    search,
           "get":       get,
           "update":    update}

def api_run(argv :list):

    if argv[1] != "db":
        sys.exit(0)

    if check_db_exist() == False:
        print("exploit db not exist download start")
        download_db()

    if len(argv) < 3:
        print_usage(argv)

    options.get(argv[2])(argv)

