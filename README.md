# IoTPene
CVE-IDおよびExploitDB-ID (EID)を指定することで，対応したPoCの実行環境(Dockerコンテナ)を自動で構築するツール


PoCの実行に必要なプログラミング言語の実行環境とPoCで使用されるモジュールを自動でインストールすることにより，PoCのテストやペネトレーションテストを補助します．


対応済の環境: python, Node.js
対応予定の環境: ruby

## インストール方法
python3.8.10，およびgitのインストール済を想定
```
git clone https://github.com/security-anthem/MAID.git
pip install -r requirements.txt
```
## 使い方
以下のusageを参照．
| Commnad |                                                                  |
|---------|------------------------------------------------------------------|
| update  | ローカルのExploit DBのPoCを更新                                  |
| search  | ローカルのExploit DBのPoCを検索                                  |
| get     | 指定したCVE-IDおよびEIDのPoCを表示                               |
| create  | 指定したCVE-IDおよびEIDのPoCの実行環境を作成するDockerfileを生成 |
|---------|------------------------------------------------------------------|


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
		  create [CVE] || [db ID]
		  
example:

          search CVE-2017-2351
          search 1234
          search windows oracle
          
          get   CVE-2017-2351
          get   1234
          
		  create CVE-2017-2351
		  create 1234
		  
function:

          cve_database.py is controller cve and DB json datas:
          
                  search_by_cve, search_by_id : you can get information in json data by 'id' or 'cve' code
          
          exploit_database.py is controller of exploit-database:
                  search_by_keywords : you can use searchexploit.sh file with this function


## 実行例
IoTPeneのインストール後，Exploit DBのPoCを一度ローカルにダウンロードする必要があるため，時間がかかることに注意．


DBの更新 (ダウンロード)
`$ python main.py db update all`


PoCの検索
`$ python main.py db search 'CVE-2022-35513'`
```---IoTPene---
+----------------+
| CVE-2022-35513 |
+----------------+

-------------------exploit-----------------
 Exploit DB Id: 51014
 File: /home/user/IoTPene/api/exploit-database/exploits/multiple/local/51014.js
 Date: 1970-01-01
 Author: p1ckzi
 Platform: local
 Type: multiple
 Port:`
```


PoCの実行環境を作成するDockerfileの生成
`$ python main.py db create 'CVE-2022-35513'`
```
$ python main.py db create 'CVE-2022-35513'
---IoTPene---
...
PoCの表示
...
----------------------------------------------------------------------------------
update files
Required node js packages: argparse simplecrypt
create ./poc/cve-2022-35513/Dockerfile
exec:
$ docker build -t cve-2022-35513 ./poc/cve-2022-35513/
$ docker run -it cve-2022-35513 sh
```
