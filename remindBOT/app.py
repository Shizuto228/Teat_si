from typing import Text
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    TemplateSendMessage,ButtonsTemplate,messages,URIAction, QuickReplyButton, QuickReply, MessageAction
)
import os
import datetime as dt
import datetime
import calendar
import pytz
import gspread
import schedula
import time
from oauth2client.service_account import ServiceAccountCredentials
import csv

app = Flask(__name__)

line_bot_api = LineBotApi('7x4Jpi7kVqJLAul106Md6bBZfggcvjRyoShBl5rXNzdQ1ExHIsaHfrw1WEQBSo3yO6Q1i3uC/oz3iMhftmt4ev5JapPA/5fbXCuhOEbYKXSuwlyIy7yddyL8U3tqkoPQ0KS6GyD/Tn/9jdrSvbdPQAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9687a7f73db2eab97781657b3c8692aa')
text_message=''
json_file = 'ydanavo-78022b450d88.json'
file_name = 'chatbot_db'
sheet_name1 = 'シート1'
sheet_name2 = 'csv_sheet'
#sheet_name2 = 'csv_sheet'
csv_file_name = 'Davis.csv'

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

@app.route("/")
def test():
    return "ok"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'



def make_button_template():
    message_template = TemplateSendMessage(
        alt_text="ドライブへのリンク",
        template=ButtonsTemplate(
            text="アカウント認証が必要な場合があります",
            title="授業に関するドライブへのリンクです",
            image_size="cover",
            thumbnail_image_url="https://example.com/gazou.jpg",
            actions=[
                URIAction(
                    uri="https://drive.google.com/drive/u/0/folders/1zc_nkwN15v2I0rJstkW0byXjShx0z0cL",
                    label="課題のドライブ"
                ),
                URIAction(
                    uri="https://drive.google.com/drive/u/0/folders/19eCHgk6EynTT-8NP1Js4KsSHmHgYACDX",
                    label="教材のドライブ"
                )
            ]
        )
    )
def keiba_template():
    message_template = TemplateSendMessage(
        alt_text="競馬へのリンク",
        template=ButtonsTemplate(
            title="ジャパンカップのURLです",
            text="破産する可能性があります",
            image_size="cover",
            thumbnail_image_url="https://www-f.keiba.jp/img/graderace/2021/1128_japancup/japanCup_001.jpg?",
            actions=[
                URIAction(
                    uri="https://race.netkeiba.com/race/shutuba.html?race_id=202105050812",
                    label="出走馬の一覧です"
                ),
                URIAction(
                    uri="https://race.netkeiba.com/race/data_top.html?race_id=202105050812&rf=race_submenu",
                    label="データ分析の一覧です"
                )
            ]
        )
    )
    return message_template


@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    
    cuttext = event.message.text
    cuttext=cuttext.split(",")
    if event.message.text == "リマインド":
        reply_message="リマインドする内容を教えて"
       
    elif cuttext[0]=="リマインド" and cuttext[1]!=None and cuttext[2]!=None:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
        gc = gspread.authorize(credentials)
        sh = gc.open(file_name)
        wks = sh.get_worksheet(0)
        list_data = [cuttext[1],cuttext[2],cuttext[3]]
        wks.append_row(list_data)
        reply_message="このリマインドメッセージをおくるね"
    
    elif cuttext[0]=="ご意見":
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
        gc = gspread.authorize(credentials)
        sh = gc.open(file_name)
        wks = sh.get_worksheet(1)
        list_data = [cuttext[1]]
        wks.append_row(list_data)
        reply_message="ご意見ありがとうございます！"
  
    elif "ゼミ" in event.message.text or "進級制作" in event.message.text:
        reply_message = "こちらがゼミのurlです\nhttps://zoom.us/j/91713846508?pwd=UmJQSldkWmdxbzIyMEVKZGxKZmVuZz09"

    elif "kadai" in event.message.text or "課題" in event.message.text:
        reply_message = "こちらが課題のurlです\nhttps://drive.google.com/drive/u/1/folders/1zc_nkwN15v2I0rJstkW0byXjShx0z0cL"

    elif "ドライブ" in event.message.text:
        messages = make_button_template()
        line_bot_api.reply_message(
        event.reply_token,
        messages
        )
    elif "月曜日" in event.message.text:
        reply_message ="今日は一日進級制作の授業です"
    elif "火曜日" in event.message.text:
        reply_message ="今日は午前中は就職対策の授業です"
    elif "水曜日" in event.message.text:
        reply_message ="今日は午前中は資格対策、午後はゲームプログラミングの授業です"
    elif "木曜日" in event.message.text:
        reply_message ="今日は午前中はゲームビジネス、午後はゲームアルゴリズムの授業です"
    elif "金曜日" in event.message.text:
        reply_message ="今日は午前中は進級制作、午後はサーバープログラミングの授業です"
    

    elif  "授業" in event.message.text:
         line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text='一覧から選んでね',
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="月曜日", text="月曜日")),
                        QuickReplyButton(action=MessageAction(label="火曜日", text="火曜日")),
                        QuickReplyButton(action=MessageAction(label="水曜日", text="水曜日")),
                        QuickReplyButton(action=MessageAction(label="木曜日", text="木曜日")),
                        QuickReplyButton(action=MessageAction(label="金曜日", text="金曜日")),
                    ])
            )
        )
    elif "競馬" in event.message.text:
        messages = keiba_template()
        line_bot_api.reply_message(
        event.reply_token,
        messages
        )


    elif "月曜前" in event.message.text:
        reply_message ="奥谷先生だよ"
    elif "月曜後" in event.message.text:
        reply_message ="藤田先生だよ"
    elif "火曜前" in event.message.text:
        reply_message ="藤田先生だよ"
    elif "火曜後" in event.message.text:
        reply_message ="お休みだよ"
    elif "水曜前" in event.message.text:
        reply_message ="藤田先生だよ"
    elif "水曜後" in event.message.text:
        reply_message ="奥谷先生だよ"
    elif "木曜前" in event.message.text:
        reply_message ="髙橋先生だよ"
    elif "木曜後" in event.message.text:
        reply_message ="藤田先生だよ"
    elif "金曜前" in event.message.text:
        reply_message ="高原先生だよ"
    elif "金曜後" in event.message.text:
        reply_message ="髙橋先生だよ"

    elif "げつ" in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='時間帯を選んでね',
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="午前", text="月曜前")),
                        QuickReplyButton(action=MessageAction(label="午後", text="月曜後")),
                    ])
            )
       )
    elif "か" in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='時間帯を選んでね',
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="午前", text="火曜前")),
                        QuickReplyButton(action=MessageAction(label="午後", text="火曜後")),
                    ])
            )
       )
    elif "すい" in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='時間帯を選んでね',
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="午前", text="水曜前")),
                        QuickReplyButton(action=MessageAction(label="午後", text="水曜後")),
                    ])
            )
       )
    elif "もく" in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='時間帯を選んでね',
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="午前", text="木曜前")),
                        QuickReplyButton(action=MessageAction(label="午後", text="木曜後")),
                    ])
            )
       )
    elif "きん" in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='時間帯を選んでね',
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="午前", text="金曜前")),
                        QuickReplyButton(action=MessageAction(label="午後", text="金曜後")),
                    ])
            )
       )

    elif "先生" in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='曜日を選んでね',
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="月曜日", text="げつ")),
                        QuickReplyButton(action=MessageAction(label="火曜日", text="か")),
                        QuickReplyButton(action=MessageAction(label="水曜日", text="すい")),
                        QuickReplyButton(action=MessageAction(label="木曜日", text="もく")),
                        QuickReplyButton(action=MessageAction(label="金曜日", text="きん")),
                    ])
            )
        )
    
    else:
        reply_message = "登録されているキーワードとは一致しませんでした"
    

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))

def sendMessage():
        """
        送信するテキストを作成する関数
        """
        dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        date = dt.date(dt_now.year, dt_now.month, dt_now.day)
        weekday = datetime.date.today().weekday()
        weekday_name = calendar.day_name[weekday]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
        gc = gspread.authorize(credentials)
        sh = gc.open(file_name)
        wks = sh.get_worksheet(0)
        global text_message 
        gyou=1

        if weekday_name == 'Monday':
            text_message='今日は月曜日！授業は卒業制作だよ。課題は大丈夫かな'
        if weekday_name == 'Tuesday':
            text_message='今日は火曜日！授業は就職対策と選択授業だよ。課題は大丈夫かな'
        if weekday_name == 'Wednesday':
            text_message='今日は水曜日！授業は資格対策とゲームプログラミングだよ。課題は大丈夫かな'
        if weekday_name == 'Thursday':
            text_message='今日は木曜日！授業はゲームプランニングとゲームアルゴリズムだよ。課題は大丈夫かな'
        if weekday_name == 'Friday':
            text_message='今日は金曜日！授業は卒業制作とサーバープログラミングだよ。課題は大丈夫かな'
        if weekday_name == 'Saturday':
            text_message='今日は土曜日！授業はお休みだよ。ゆっくり過ごしてね'
        if weekday_name == 'Sunday':
            text_message='今日は日曜日！授業はお休みだよ。明日の用意は大丈夫かな'
        
        messages = TextSendMessage(text=text_message)
        line_bot_api.broadcast(messages=messages)

        while True:
            
            if wks.row_values(gyou) == None:
                break
            else: 
                row_list = wks.row_values(gyou)
                if row_list[0]== str(dt_now.month) and row_list[1]==str(dt_now.day):
                    text_message=row_list[2]
                    messages = TextSendMessage(text=text_message)
                    line_bot_api.broadcast(messages=messages)
            gyou+=1
            

if __name__ == "__main__":
    
    sendMessage()
    app.run()