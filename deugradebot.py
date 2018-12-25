import os
import telegram

from login_data import bot_data
from parse import get_score_data

def send_message(data):
    bot.sendMessage(chat_id=chat_id, text="%s 과목의 성적이 갱신되었습니다.\n\n과목명 : %s\n분류 : %s\n이수 학점 : %s\n평점 : %s(%s)" % (data[2], data[2], data[3], data[4], data[5], data[6]))

bot = telegram.Bot(token=bot_data[0])
chat_id = bot_data[1]

data = get_score_data()

for subj_data in data:
    if subj_data[6] != '':
        if not os.path.exists(subj_data[0]):
            send_message(subj_data)
            with open(subj_data[0], 'w') as f:
                f.close()