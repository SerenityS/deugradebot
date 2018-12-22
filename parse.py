import requests
from bs4 import BeautifulSoup

login_data = []
f = open("login.txt", 'r')
lines = f.readlines()
for line in lines:
    line = line.replace("\n", "")
    login_data.append(line)
f.close()

with requests.Session() as s:
    jboss = s.post("http://smartcampus.deu.ac.kr/auth/user/loginAuth", data={'entryA': login_data[2], 'entryB': login_data[3], 'strongbox': 'deusmartcampus'})

    jboss = BeautifulSoup(jboss.text, "lxml")
    name = jboss.findAll("suser_nm")
    id = jboss.findAll("suser_id")
    dept = jboss.findAll("dept_nm")

    print("이름 : " + name[0].text + "\n학번 : " + id[0].text + "\n학과 : " + dept[0].text + "\n")

    josso = s.post('http://smartcampus.deu.ac.kr/josso/signon/usernamePasswordLogin.do', data={'josso_cmd': 'login', 'josso_username': login_data[0], 'josso_password': login_data[1]})