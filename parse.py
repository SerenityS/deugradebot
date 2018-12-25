import requests
from bs4 import BeautifulSoup
from login_data import login_data

def get_score_data():
    try:
        with requests.Session() as s:
            jboss = s.post("http://smartcampus.deu.ac.kr/auth/user/loginAuth", data={'entryA': login_data[2], 'entryB': login_data[3], 'strongbox': 'deusmartcampus'})
            if login_data[0] not in jboss.text:
                raise Exception('JBoss')

            josso = s.post('http://smartcampus.deu.ac.kr/josso/signon/usernamePasswordLogin.do', data={'josso_cmd': 'login', 'josso_username': login_data[0], 'josso_password': login_data[3]})
            if login_data[0] not in josso.text:
                raise Exception('Josso')

            res = s.get('http://smartcampus.deu.ac.kr/webservice/302/D/01/01', cookies=josso.cookies)
            score = BeautifulSoup(res.text, "lxml")
            score_data = score.find_all(class_="info_box1")

            grade_data = []; temp = []
            for subj_data in score_data:
                subj_data = subj_data.find_all("td")
                for data in subj_data:
                    temp.append(data.text)
                grade_data.append(temp)
                temp = []
            return grade_data

    except Exception as e:
        print(e, "로그인 과정에서 오류가 발생하였습니다.")
        exit()