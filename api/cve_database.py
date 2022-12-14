import csv
import json
import os
import random
import sys
import time

import progressbar
import requests

exploit_db_mapping = "/exploitdb_mapping.json"
shellcode_db_mapping = "/shellcode_mapping.json"

exploit_cve_map = {}
exploit_db_id_map = {}
shellcode_cve_map = {}
shellcode_db_id_map = {}
pdir = os.path.dirname(os.path.abspath(__file__))


# @Misc{cve_searchsploit,
#   author       = {Andrea Fioraldi},
#   howpublished = {GitHub},
#   month        = jun,
#   title        = {{CVE SearchSploit}},
#   year         = {2017},
#   url          = {https://github.com/andreafioraldi/cve_searchsploit},
# }
def update_exploit_cve_json():
    data = {}

    if not os.path.exists(pdir + exploit_db_mapping):
        with open(pdir + exploit_db_mapping, "w") as db_file:
            json.dump(db_file)
    else:
        with open(pdir + exploit_db_mapping) as db_file:
            data = json.load(db_file)

        print("Refreshing exploit-database repo with latest exploits")
        os.system("cd %s/exploit-database/; git pull origin master" % pdir)

        files = open(pdir + "/exploit-database/files_exploits.csv", errors='ignore')
        reader = csv.reader(files)
        next(reader)

        reader = list(reader)
        csv_len = len(reader)

        get_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, '
                                    'like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        def locations_of_substring(string, substring):
            substring_length = len(substring)

            def recurse(locations_found, start):
                location = string.find(substring, start)
                if location != -1:
                    return recurse(locations_found + [location], location + substring_length)
                else:
                    return locations_found

            return recurse([], 0)

        print("Refreshing EDBID-CVE mapping")
        bar = progressbar.ProgressBar(
            widgets=[' [', progressbar.Timer(), '] ', progressbar.Bar(), ' (', progressbar.ETA(), ') '],
            maxval=csv_len).start()
        for i in range(csv_len):
            edb = tuple(reader[i])[0]
            if edb in data:
                # print "Skipping edb id " + edb
                pass
            else:
                print("Downloading https://www.exploit-db.com/exploits/" + edb)
                content = ""
                while True:
                    try:
                        r = requests.get("https://www.exploit-db.com/exploits/" + edb, headers=get_header)
                        content = r.text
                    except Exception:
                        time.sleep(10)
                        continue
                    finally:
                        break
                used = []
                indexes = locations_of_substring(content, 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-')
                for pos in indexes:
                    cve = r.text[pos + len('https://cve.mitre.org/cgi-bin/cvename.cgi?name='): pos + len(
                        'https://cve.mitre.org/cgi-bin/cvename.cgi?name=') + 9].upper()
                    pos += len('https://cve.mitre.org/cgi-bin/cvename.cgi?name=') + 9
                    while pos < len(r.text) and r.text[pos].isdigit():
                        cve += r.text[pos]
                        pos += 1
                    cve = cve.replace("\u2013", "-")
                    if cve in used: continue
                    used.append(cve)
                    print("Found: edbid " + edb + " <---> " + cve)
                indexes = locations_of_substring(content, 'https://nvd.nist.gov/vuln/detail/CVE-')
                for pos in indexes:
                    cve = r.text[pos + len('https://nvd.nist.gov/vuln/detail/'): pos + len(
                        'https://nvd.nist.gov/vuln/detail/') + 9].upper()
                    pos += len('https://nvd.nist.gov/vuln/detail/') + 9
                    while pos < len(r.text) and r.text[pos].isdigit():
                        cve += r.text[pos]
                        pos += 1
                    cve = cve.replace("\u2013", "-")
                    if cve in used: continue
                    used.append(cve)
                    print("Found: edbid " + edb + " <---> " + cve)
                data[edb] = used
                time.sleep(random.uniform(0.1, 0.3))
            bar.update(i)
        bar.finish()

        with open(pdir + "/exploitdb_mapping.json", "w") as db_file:
            json.dump(data, db_file, indent=2)

        cve_data = {}
        for k, v in data.items():
            for e in v:
                cve_data[e] = cve_data.get(e, [])
                cve_data[e].append(k)

        with open(pdir + "/exploitdb_mapping_cve.json", "w") as db_file:
            json.dump(cve_data, db_file, indent=2)

def update_shellcode_cve_json():
    data = {}

    if not os.path.exists(pdir + shellcode_db_mapping):
        with open(pdir + shellcode_db_mapping, "w") as db_file:
            json.dump(db_file)
    else:
        with open(pdir + shellcode_db_mapping) as db_file:
            data = json.load(db_file)

        print("Refreshing exploit-database repo with latest exploits")
        os.system("cd %s/exploit-database/; git pull origin master" % pdir)

        files = open(pdir + "/exploit-database/files_shellcodes.csv", errors='ignore')
        reader = csv.reader(files)
        next(reader)

        reader = list(reader)
        csv_len = len(reader)

        get_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, '
                                    'like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        def locations_of_substring(string, substring):
            substring_length = len(substring)

            def recurse(locations_found, start):
                location = string.find(substring, start)
                if location != -1:
                    return recurse(locations_found + [location], location + substring_length)
                else:
                    return locations_found

            return recurse([], 0)

        print("Refreshing EDBID-CVE mapping")
        bar = progressbar.ProgressBar(
            widgets=[' [', progressbar.Timer(), '] ', progressbar.Bar(), ' (', progressbar.ETA(), ') '],
            maxval=csv_len).start()
        for i in range(csv_len):
            edb = tuple(reader[i])[0]
            if edb in data:
                # print "Skipping edb id " + edb
                pass
            else:
                print("Downloading https://www.exploit-db.com/exploits/" + edb)
                content = ""
                while True:
                    try:
                        r = requests.get("https://www.exploit-db.com/exploits/" + edb, headers=get_header)
                        content = r.text
                    except Exception:
                        time.sleep(10)
                        continue
                    finally:
                        break
                used = []
                indexes = locations_of_substring(content, 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-')
                for pos in indexes:
                    cve = r.text[pos + len('https://cve.mitre.org/cgi-bin/cvename.cgi?name='): pos + len(
                        'https://cve.mitre.org/cgi-bin/cvename.cgi?name=') + 9].upper()
                    pos += len('https://cve.mitre.org/cgi-bin/cvename.cgi?name=') + 9
                    while pos < len(r.text) and r.text[pos].isdigit():
                        cve += r.text[pos]
                        pos += 1
                    cve = cve.replace("\u2013", "-")
                    if cve in used: continue
                    used.append(cve)
                    print("Found: edbid " + edb + " <---> " + cve)
                indexes = locations_of_substring(content, 'https://nvd.nist.gov/vuln/detail/CVE-')
                for pos in indexes:
                    cve = r.text[pos + len('https://nvd.nist.gov/vuln/detail/'): pos + len(
                        'https://nvd.nist.gov/vuln/detail/') + 9].upper()
                    pos += len('https://nvd.nist.gov/vuln/detail/') + 9
                    while pos < len(r.text) and r.text[pos].isdigit():
                        cve += r.text[pos]
                        pos += 1
                    cve = cve.replace("\u2013", "-")
                    if cve in used: continue
                    used.append(cve)
                    print("Found: edbid " + edb + " <---> " + cve)
                data[edb] = used
                time.sleep(random.uniform(0.1, 0.3))
            bar.update(i)
        bar.finish()

        with open(pdir + "/shellcode_mapping.json", "w") as db_file:
            json.dump(data, db_file, indent=2)

        cve_data = {}
        for k, v in data.items():
            for e in v:
                cve_data[e] = cve_data.get(e, [])
                cve_data[e].append(k)

        with open(pdir + "/shellcode_mapping_cve.json", "w") as db_file:
            json.dump(cve_data, db_file, indent=2)


def _search_cve_aux(cve):
    print("-------------------exploit-----------------")
    files = open(pdir + "/exploit-database/files_exploits.csv")
    reader = csv.reader(files)
    # reader.next() #skip header
    next(reader)

    found = False
    for row in reader:
        edb, file, description, date, author, platform, type, port = tuple(row)
        if edb in exploit_cve_map[cve]:
            found = True
            print(" Exploit DB Id: " + edb)
            print(" File: " + pdir + "/exploit-database/" + file)
            print(" Date: " + date)
            print(" Author: " + author)
            print(" Platform: " + platform)
            print(" Type: " + type)
            if port != "0":
                print(" Port: " + port)
            print("")
    if not found:
        print("ERROR - No EDB Id found")
        print("")

    files.close()
    print("")

    return found

def search_from_file(file):
    for line in file:
        line = line.strip()
        if not line:
            continue

        cve = line.upper()
        sname = "| " + cve + " |"
        print("+" + "-" * (len(sname) - 2) + "+")
        print(sname)
        print("+" + "-" * (len(sname) - 2) + "+")
        print("")

        if not cve in exploit_cve_map:
            print("ERROR - CVE not found.")
            print("")
            continue

        _search_cve_aux(cve)


def search_from_nessus(file):
    reader = csv.reader(file)
    # reader.next() #skip header
    next(reader)

    for row in reader:
        cve = tuple(row)[1].upper()
        proto = tuple(row)[5]
        port = tuple(row)[6]
        name = tuple(row)[7]

        if not cve in exploit_cve_map:
            continue

        sname = "| " + name + " |"
        print("+" + "-" * (len(sname) - 2) + "+")
        print(sname)
        print("+" + "-" * (len(sname) - 2) + "+")
        print("")
        print(" CVE: " + cve)
        print(" Protocol: " + proto)
        print(" Port: " + port)
        print("")
        print(" +----+ Exploit DB matching +----+ ")
        print("")

        _search_cve_aux(cve)
        print("")


def search_by_cve(cve):
    cve = cve.upper()

    sname = "| " + cve + " |"
    print("+" + "-" * (len(sname) - 2) + "+")
    print(sname)
    print("+" + "-" * (len(sname) - 2) + "+")
    print("")

    if not cve in exploit_cve_map:
        print("CVE not found in exploit.")
        print("")
    else:
        found = _search_cve_aux(cve)
        if not found:
            print("------------------------")

def search_by_id(id):

    sname = "| " + str(id) + " |"
    print("+" + "-" * (len(sname) - 2) + "+")
    print(sname)
    print("+" + "-" * (len(sname) - 2) + "+")
    print("")
    found = False

    if not id in exploit_db_id_map:
        print("CVE not found in exploit.")
        print("")
    else:
        for cve in exploit_db_id_map.get(id):
            found = _search_cve_aux(cve)
            if not found:
                print("-----------------")

    if not id in shellcode_db_id_map:
        print("CVE not found in shellcode")
        print("")
    else:
        for cve in shellcode_db_id_map.get(id):
            found = _search_cve_aux(cve)
            if not found:
                print("-----------------")
    return found
#######################

def cve_usage():
    print("+------------------------------------+")
    print("|          cve_searchsploit          |")
    print("| Copyright 2017-19, Andrea Fioraldi |")
    print("+------------------------------------+")
    print("")
    print("Usage:")
    print("  python3 cve_searchsploit.py [parameters...]")
    print("")
    print("Parameters:")
    print("  <cve>                      search exploits by a cve")
    print("  -u                         update the cve-edbid database")
    print("  -f <file with cve list>    search exploits by a cve list file")
    print("  -n <nessus csv scan file>  search exploits by the cve matching with a nessus scan in csv format")
    print("")
    return


def cve_main():
    global exploit_cve_map

    if len(sys.argv) < 2:
        cve_usage()
    if sys.argv[1] == "-u":
        update_exploit_cve_json()
        return

    for i in range(1, len(sys.argv)):
        a = sys.argv[i]
        if a == "-u":
            print("ERROR - '-u' is mutually exclusive with all the other arguments")
            print("")
            return
        elif a == "-f":
            if i + 1 == len(sys.argv):
                cve_usage()
            try:
                file = open(sys.argv[i + 1], "r")
                search_from_file(file)
            except Exception as exc:
                print("ERROR - " + str(exc))
                print("")
                return
        elif a == "-n":
            if i + 1 == len(sys.argv):
                cve_usage()
            try:
                file = open(sys.argv[i + 1], "r")
                search_from_nessus(file)
            except Exception as exc:
                print("ERROR - " + str(exc))
                print("")
                return
        else:
            search_by_cve(a)


if not os.path.isdir(pdir + "/exploit-database"):
    print("Cloning exploit-database repository")
    os.system("cd {}; git clone https://github.com/offensive-security/exploit-database".format(pdir))

with open(pdir + "/exploitdb_mapping_cve.json") as data_file:
    exploit_cve_map = json.load(data_file)
with open(pdir + "/exploitdb_mapping.json") as data_file:
    exploit_db_id_map = json.load(data_file)
with open(pdir + "/shellcode_mapping_cve.json") as data_file:
    shellcode_cve_map = json.load(data_file)
with open(pdir + "/shellcode_mapping.json") as data_file:
    shellcode_db_id_map = json.load(data_file)
