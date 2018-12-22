import requests
from bs4 import BeautifulSoup

login_data = []
f = open("enc_login.txt", 'r')
lines = f.readlines()
for line in lines:
    line = line.replace("\n", "")
    login_data.append(line)
f.close()

res = requests.post("http://smartcampus.deu.ac.kr/auth/user/loginAuth", data={'entryA': login_data[0], 'entryB': login_data[1], 'strongbox': 'deusmartcampus'})

res = BeautifulSoup(res.text, "lxml")
name = res.findAll("suser_nm")
id = res.findAll("suser_id")
dept = res.findAll("dept_nm")

print("이름 : " + name[0].text + "\n학번 : " + id[0].text + "\n학과 : " + dept[0].text + "\n")