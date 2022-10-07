import os
import shutil
import sys

import api

def print_usage():
    print("---------------------")
    print("|       IoTPene     |")
    print("---------------------")
    print("")
    print("Usage:")
    print("Parameters:")
    print("db")


def write_node_dockerfile(dir_path):    
    docker_file_path = ''.join([s + '/' for s in dir_path.split('/')[:-1]])
    with open(docker_file_path+'/Dockerfile', mode='w') as f:
        f.write('FROM node:16-alpine3.15\n')
        f.write('COPY {} /\n'.format('poc_file/*', ))

def write_python_dockerfile(dir_path):
    docker_file_path = ''.join([s + '/' for s in dir_path.split('/')[:-1]])
    with open(docker_file_path+'/Dockerfile', mode='w') as f:
        f.write('FROM python:16-alpine3.15\n')

def write_ruby_dockerfile(dir_path):
    docker_file_path = ''.join([s + '/' for s in dir_path.split('/')[:-1]])
    with open(docker_file_path+'/Dockerfile', mode='w') as f:
        f.write('FROM ruby:16-alpine3.15\n')
        

def write_dockerfile(lang, dir_path):
    if lang == "node":
        write_node_dockerfile(dir_path)
        return 0
    elif lang == "python":
        write_python_dockerfile(dir_path)
        return 0
    elif lang == "ruby":
        write_ruby_dockerfile(dir_path)
        return 0
    else:
        print("Invalid value:", lang)
        return 1


def find_langage(file_path):
    file_extension = file_path.split('.')[-1]
    if file_extension == "py":
        return "python"
    elif file_extension == "js":
        return "node"
    elif file_extension == "rb":
        return "ruby"
    elif file_extension == "sh":
        return "shell"
    else :
        return "unknown"    


def create_dockerfile(exploit_file, dir_path):
    lang = find_langage(exploit_file)
    write_dockerfile(lang, dir_path)
    # create dockerfile
    

def create_env(exploit_file_path, cve_id):
    dir_path = f'./poc/{cve_id}/poc_file'
    try:
        os.makedirs(dir_path)
    except:
        print('update files')

    exploit_file = exploit_file_path.split('/')[-1]
    
    shutil.copy(exploit_file_path, dir_path)
    
    create_dockerfile(exploit_file, dir_path)
    
        
if __name__ == '__main__':
    print("IoTPene")

    # exploit_file_path = api.get(sys.argv)
    # print(exploit_file_path)
    exploit_file_path = 'api/exploit-database/exploits/multiple/local/51014.js'
    if exploit_file_path != '':
        cve_id = sys.argv[3]
        create_env(exploit_file_path, cve_id)
    else:
        print('Not Find Exploits')
        sys.exit(0)
    
    if len(sys.argv) < 2:
        print_usage()
    if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "help":
        print_usage()
    if sys.argv[1] == "db":
        api.api_run(sys.argv)

