# README
please write something

api package usage:

command:

          --help, -h, help: show help message
          search: search information about db
          get: get exploit script 
          update: update db, cve code
          
usage:

          search [CVE] || [db ID] || [KEY WORDS]
          get    [CVE] || [db ID]
          update all || db || cve
example:

          search CVE-2017-2351
          search 1234
          search windows oracle
          
          get   CVE-2017-2351
          get   1234
          
function:

          cve_database.py is controller cve and DB json datas:
          
                  search_by_cve, search_by_id : you can get information in json data by 'id' or 'cve' code
          
          exploit_database.py is controller of exploit-database:
                  search_by_keywords : you can use searchexploit.sh file with this function
