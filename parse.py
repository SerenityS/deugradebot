import base64
import pyDes.pyDes as pyDes
import requests

from bs4 import BeautifulSoup
from login_data import id, pw

def enc_string(data):
    data = data.encode()
    k = pyDes.des(b"ab_booktv_abcd09", pyDes.ECB, pad=None, padmode=pyDes.PAD_PKCS5)
    d = k.encrypt(data)
    d = base64.encodebytes(d)
    return d

def get_score_data():
    enc_id = enc_string(id)
    enc_pw = enc_string(pw)
    try:
        with requests.Session() as s:
            jboss = s.post("http://smartcampus.deu.ac.kr/auth/user/loginAuth", data={'entryA': enc_id, 'entryB': enc_pw, 'strongbox': 'deusmartcampus'})
            if id not in jboss.text:
                raise Exception('JBoss')

            josso = s.post('http://smartcampus.deu.ac.kr/josso/signon/usernamePasswordLogin.do', data={'josso_cmd': 'login', 'josso_username': id, 'josso_password': enc_pw})
            if id not in josso.text:
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