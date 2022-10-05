import os
import sys

from .exploit_database import *
from .cve_database import *

db_path = ""
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

def print_usage(argv):
    print("---------------------")
    print("|      db   API     |")
    print("---------------------")
    print("")
    print("Command:")
    print("search: Search information about db")
    print("usage: search [CVE] || [db ID] || 'penetrate ")
    print("get: Get script of db")
    print("usage: get    [CVE] || [db ID]")
    print("update: Update db data")
    print("usage: update all || db || cve")
    print("")
    print("Example:")
    print("search CVE")
    print("get CVE")
    print("update")

def search(argv):
    query_string = argv[3]

    if query_string[0 : 3].upper() == "CVE":
        return search_by_cve(query_string)
    elif query_string.isnumeric():
        if not search_by_id(query_string):
            return search_by_keywords(argv[3:])
    else:
        argv.append('-t')
        return search_by_keywords(argv[3:])

def get(argv):
    query_string = argv[3]
    files = open(db_path + "/exploit-database/files_exploits.csv", errors="ignore")
    reader = csv.reader(files)
    next(reader)

    if query_string[0 : 3].upper() == "CVE":
        if not query_string.upper() in exploit_cve_map:
            files.close()
            return 0
        query_string = [query_string.upper()]
    elif query_string.isnumeric():
        if not query_string in exploit_db_id_map:
            files.close()
            return 0
        query_string = exploit_db_id_map.get(query_string)

    for query in query_string:
        for row in reader:
            edb, file, description, date, author, platform, type, port = tuple(row)
            if edb in exploit_cve_map[query]:
                file_route = db_path + "/exploit-database/" + file
                exploit_script = open(file_route)
                print("===================================================================")
                print("=                     {}                               =".format(query))
                print("===================================================================")
                print(exploit_script.read())
                exploit_script.close()


    files.close()
def update(argv):
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

options = {"--help":    print_usage,
           "-h":        print_usage,
           "search":    search,
           "get":       get,
           "update":    update}

def api_run(argv):

    if argv[1] != "db":
        sys.exit(0)

    if check_db_exist() == False:
        print("exploit db not exist download start")
        download_db()

    if len(argv) < 3:
        print_usage(argv)

    options.get(argv[2])(argv)

