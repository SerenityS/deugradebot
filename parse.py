import requests
from bs4 import BeautifulSoup

def get_score_data(login_data):
    with requests.Session() as s:
        jboss = s.post("http://smartcampus.deu.ac.kr/auth/user/loginAuth", data={'entryA': login_data[2], 'entryB': login_data[3], 'strongbox': 'deusmartcampus'})

        jboss = BeautifulSoup(jboss.text, "lxml")
        name = jboss.findAll("suser_nm")
        id = jboss.findAll("suser_id")
        dept = jboss.findAll("dept_nm")

        print("이름 : " + name[0].text + "\n학번 : " + id[0].text + "\n학과 : " + dept[0].text + "\n")

        josso = s.post('http://smartcampus.deu.ac.kr/josso/signon/usernamePasswordLogin.do', data={'josso_cmd': 'login', 'josso_username': login_data[0], 'josso_password': login_data[3]})

        res = s.get('http://smartcampus.deu.ac.kr/webservice/302/D/01/01', cookies=josso.cookies)

        score = BeautifulSoup(res.text, "lxml")
        score_data = score.find_all(class_="info_box1")
        subj_data = []
        for data in score_data:
            subj_data.append(data.find_all("td"))
        return subj_data