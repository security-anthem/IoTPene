import os
import re
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


def find_node_package(file_path):
    pattern = 'require\(\'(.*)\'\)'
    packages = []
    with open (file_path, mode='r') as f:        
        for line in f:
            packages += re.findall(pattern, line)

    print('Required node js packages: ', end='')
    for p in packages:
        print(p, end=' ')
    print(end='\n')

    return packages

    
def write_node_dockerfile(dir_path, exploit_file):    
    docker_file_path = ''.join([s + '/' for s in dir_path.split('/')[:-1]])
    packages = find_node_package(dir_path+'/'+exploit_file)
    with open(docker_file_path+'/Dockerfile', mode='w') as f:
        f.write('FROM node:16-alpine3.15\n')
        f.write('RUN mkdir -p poc_file\n')
        f.write('COPY poc_file/* poc_file/\n')
        f.write('WORKDIR poc_file/\n')
        for p in packages:
            f.write('RUN npm install {}\n'.format(p))


def find_python_package(file_path):
    pattern = 'require\(\'(.*)\'\)'
    packages = []
    with open (file_path, mode='r') as f:        
        for line in f:
            packages += re.findall(pattern, line)

    print('Required node js packages: ', end='')
    for p in packages:
        print(p, end=' ')
    print(end='\n')

    return packages


def write_python_dockerfile(dir_path, exploit_file):
    docker_file_path = ''.join([s + '/' for s in dir_path.split('/')[:-1]])
    with open(docker_file_path+'/Dockerfile', mode='w') as f:
        f.write('FROM python:3.8.2-slim-buster\n')
        f.write('RUN mkdir -p poc_file\n')
        f.write('COPY poc_file/* poc_file/\n')
        f.write('WORKDIR poc_file/\n')
        f.write('RUN pip install pipreqs\n')
        f.write('RUN pipreqs .\n')
        f.write('RUN pip install -r requirements.txt\n')
    

def write_ruby_dockerfile(dir_path, exploit_file):
    docker_file_path = ''.join([s + '/' for s in dir_path.split('/')[:-1]])
    with open(docker_file_path+'/Dockerfile', mode='w') as f:
        f.write('FROM ruby:16-alpine3.15\n')
        

def write_dockerfile(lang, dir_path, exploit_file):
    if lang == "node":
        write_node_dockerfile(dir_path, exploit_file)
        return 0
    elif lang == "python":
        write_python_dockerfile(dir_path, exploit_file)
        return 0
    elif lang == "ruby":
        write_ruby_dockerfile(dir_path, exploit_file)
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
    write_dockerfile(lang, dir_path, exploit_file)
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
    
    docker_file_path = ''.join([s + '/' for s in dir_path.split('/')[:-1]])
    print('create ' + docker_file_path + 'Dockerfile')
    print('exec:')
    print('$ docker build -t ' + cve_id + ' ' + docker_file_path)
    print('$ docker run -it ' + cve_id + ' sh')
    
        
if __name__ == '__main__':
    print("---IoTPene---")

    # exploit_file_path = 'api/exploit-database/exploits/multiple/local/51014.js'
    
    if len(sys.argv) < 2:
        print_usage()
    if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "help":
        print_usage()
    if sys.argv[1] == "db":
        if sys.argv[2] == "create":
            sys.argv[2] = "get"
            exploit_file_path = api.api_run(sys.argv)
            print('----------------------------------------------------------------------------------')
            if exploit_file_path != '':
                cve_id = sys.argv[3]
                create_env(exploit_file_path, cve_id.lower())
            else:
                print('Not Find Exploits')
        else:
            api.api_run(sys.argv)
            

