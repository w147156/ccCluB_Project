import json
import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi, WebhookHandler
# 載入對應的函式庫
from linebot.models import TextSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage, PostbackEvent, FlexSendMessage
from linebot.models import FlexSendMessage
import random
import emoji
from fuzzywuzzy import process

# 引用 flex_msg.py 文件
from flex_msg import create_flex_message
from flex_msg_sim import create_flex_message_sim

msg_dict_simlist = {}
json_file_path_simlist = 'simlist.json'
with open(json_file_path_simlist, 'r', encoding='utf-8') as file:
    data_simlist = json.load(file)
    # 將資料加入 msg_dict_simlist
for entry in data_simlist:
    base = entry['基底']
    ingredients = entry['材料']
    msg_dict_simlist[ingredients] = base

msg_dict_mix = {}
msg_dict_mix_all = {}
img_dict = {}
json_file_path_mix = 'mixology_t1.json'
with open(json_file_path_mix, 'r', encoding='utf-8') as file:
    data_mix = json.load(file)
    # 將資料加入 msg_dict_mix
for entry in data_mix:
    name = entry['酒名']
    base = entry['基底']
    ingredients = entry['材料']
    picture = entry['酒品實拍']
    msg_dict_mix[name] = ingredients
    msg_dict_mix_all[name] = {'基底': base, '材料': ingredients,'酒品實拍':picture}
    img_dict[name] = picture


def linebot(request):
    try:
        body = request.get_data(as_text=True)
        json_data = json.loads(body)                           # json 格式化收到的訊息
        line_bot_api = LineBotApi('9STVARbASfkAlRERVnFWsrljqdUSKpgFEVaXonug52xCGy2CJzdU73CI4vrnWFn8eAH47+jSBTj7O1bd/qQ7DsunYamEWNjk4nwbY9SYWDCHGQBD5hdU1uFB+7d30vHNjdyJlwv+AQBNThArqXLOCAdB04t89/1O/w1cDnyilFU=')  # 輸入 你的 Channel access token
        handler = WebhookHandler('1d505ddf02faf2b841f2cc54fb2841eb')         # 輸入 你的 Channel secret
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        events = json_data['events']
        for event in events:
            if 'replyToken' in event:
                reply_token = event['replyToken']
                message_type = event['message']['type']
                if message_type == 'text':
                    text_message = event['message']['text']
                    if '排行' in text_message:
                        reply_content = reply_msg_case5()
                    # 回覆訊息
                        line_bot_api.reply_message(reply_token, TextSendMessage(text=reply_content)) 
                    elif '您選擇的是Professional' in text_message:
                    # Trigger Flex Message creation and sending for Professional
                        flex_msg = create_flex_message(reply_token)
                        line_bot_api.reply_message(reply_token, flex_msg)
                    elif '您選擇的是Simple' in text_message:
                    # Trigger Flex Message creation and sending for Simple
                        flex_msg_sim = create_flex_message_sim(reply_token)
                        line_bot_api.reply_message(reply_token, flex_msg_sim)              
                    elif text_message in msg_dict_mix:
                    # 呼叫 reply_msg_case1 來處理回覆訊息
                        reply_content = reply_msg_case1(text_message)
                    # 回覆訊息
                        line_bot_api.reply_message(reply_token, reply_content)
                    elif 'pro' in text_message:
                        reply_content = reply_msg_case2(text_message)
                    # 回覆訊息
                        line_bot_api.reply_message(reply_token, reply_content)
                    elif 'sim' in text_message:
                        reply_content = reply_msg_case3(text_message)
                    # 回覆訊息
                        line_bot_api.reply_message(reply_token, reply_content)
                    elif any(process.extractOne(text_message, msg_dict_mix.keys())[1] >= 50 for key in msg_dict_mix.keys()) and 'pro' not in text_message and 'sim' not in text_message:
                        reply_content = reply_msg_case4(text_message)
                    # 回覆訊息
                        line_bot_api.reply_message(reply_token, reply_content)
                    else:
                        line_bot_api.reply_message(reply_token, TextSendMessage(text=f"HIHI \n\n請輸入欲查詢酒譜的『酒名』 \n\n或輸入『排行』看看大家都喝些什麼 \n\n或於下方圖片點選『專業or簡易調酒』並選擇基底由小酒酒為您推薦唷 {emoji.emojize(':face_savoring_food: :face_savoring_food:')}"))
                elif message_type == 'sticker':
                    stickerId = json_data['events'][0]['message']['stickerId']  # 取得 stickerId
                    packageId = json_data['events'][0]['message']['packageId']  # 取得 packageId
                    # 使用 TextSendMessage 顯示貼圖ID
                    reply_content = StickerSendMessage(sticker_id=stickerId, package_id=packageId)
                    line_bot_api.reply_message(reply_token, reply_content)
                elif message_type == 'location':
                    # 如果是收到的訊息是地點資訊
                    line_bot_api.reply_message(reply_token, TextSendMessage(text='好地點！'))
                elif message_type == 'image':
                    # 如果是收到的訊息是圖片
                    line_bot_api.reply_message(reply_token, TextSendMessage(text='好圖給讚！'))
                elif message_type == 'audio':
                    # 如果是收到的訊息是聲音
                    line_bot_api.reply_message(reply_token, TextSendMessage(text='聲音讚喔～'))
                elif message_type == 'video':
                    # 如果是收到的訊息是影片
                    line_bot_api.reply_message(reply_token, TextSendMessage(text='影片內容真是不錯！'))
    except:
        print('error', body)
    return 'OK'
# 定義回覆訊息的函式

def reply_msg_case1(text_message):
    # 初始化回覆訊息列表
    reply_messages = []

    # 直接使用 text 作為酒名查詢
    if text_message in msg_dict_mix:
        ingredients = msg_dict_mix[text_message]
        picture = img_dict[text_message]

        # 建立文字訊息
        text_message = TextSendMessage(text=f"{text_message}\n\n{emoji.emojize(':wine_glass: :cocktail_glass: :tropical_drink: :wine_glass: :cocktail_glass: :tropical_drink:')}\n\n{ingredients}")

        # 建立圖片訊息
        image_message = ImageSendMessage(original_content_url=picture, preview_image_url=picture)

        # 將文字和圖片訊息加入回覆列表
        reply_messages.append(text_message)
        reply_messages.append(image_message)
    else:
        # 找不到符合的基底
        reply_messages.append(TextSendMessage(text="抱歉，找不到符合的酒名資料"))

    return reply_messages

def reply_msg_case2(text_message):
    reply_messages = []
    pickbase = text_message.replace('pro', "").strip()
    matching_bases = [base for base, data in msg_dict_mix_all.items() if pickbase in data['基底']]

    if matching_bases:
        random_drink_name = random.choice(matching_bases)
        picture = img_dict[random_drink_name]
        # 建立文字訊息
        text = TextSendMessage(text=f"基底為{pickbase}的隨機精選：\n\n{random_drink_name}\n\n{emoji.emojize(':wine_glass: :cocktail_glass: :tropical_drink: :wine_glass: :cocktail_glass: :tropical_drink:')}\n\n{msg_dict_mix[random_drink_name]}")
        # 建立圖片訊息
        image = ImageSendMessage(original_content_url=picture, preview_image_url=picture)
        # 將文字和圖片訊息加入回覆列表
        reply_messages.append(text)
        reply_messages.append(image)
    else:
        # 找不到符合的基底
        reply_messages.append(TextSendMessage(text="抱歉，找不到符合的基底資料"))

    return reply_messages

def reply_msg_case3(text_message):
    reply_messages = []
    pickbase = text_message.replace('sim', "").strip()
    matching_bases = [base for base, data in msg_dict_simlist.items() if pickbase in data]

    if matching_bases:
        base = matching_bases[0]
        # 直接使用 base 作為酒名
        random_drink_ingredients = msg_dict_simlist[base]
        # 建立文字訊息
        reply_messages.append(TextSendMessage(text=f"基底為{pickbase}的隨機精選：\n\n{emoji.emojize(':wine_glass: :cocktail_glass: :tropical_drink: :wine_glass: :cocktail_glass: :tropical_drink:')}\n\n{base}"))
    else:
        # 找不到符合的基底
        reply_messages.append(TextSendMessage(text="抱歉，找不到符合的基底資料"))

    return reply_messages

def reply_msg_case4(text_message):
    # 初始化回覆訊息列表
    reply_messages = []

    # 使用模糊匹配找到最相似的酒名
    matches = process.extract(text_message, msg_dict_mix.keys())

    # 選擇相似度分數最高的前三個酒名
    top_matches = [match for match, score in matches if score >= 50][:3]

    if top_matches:
        for match in top_matches:
            ingredients = msg_dict_mix[match]
            picture = img_dict[match]

            # 建立文字訊息
            text_message = TextSendMessage(text=f"{match}\n\n{emoji.emojize(':wine_glass: :cocktail_glass: :tropical_drink: :wine_glass: :cocktail_glass: :tropical_drink:')}\n\n{ingredients}")
            # 建立圖片訊息
            image_message = ImageSendMessage(original_content_url=picture, preview_image_url=picture)

            # 將文字和圖片訊息加入回覆列表
            reply_messages.append(text_message)
            reply_messages.append(image_message)
    else:
        # 找不到相似的酒名
        reply_messages.append(TextSendMessage(text="抱歉，找不到符合的酒名資料"))

    return reply_messages

def reply_msg_case5():
    reply_messages = []
    qua = 0

    url = 'https://mixology.com.tw/Recipe.aspx?ord=1&page=1'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    final_reply_message =''
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        wines = soup.find_all('div', class_='recipe_list_content')

        for wine in wines:
            name = wine.find('div', class_='recipe_list_content_name')
            name = name.span.text
            reply_messages.append(f"No.{qua+1} {name}\n\n")
            qua += 1
            if qua >= 10:
                break

        final_reply_message = f"以下是人氣排行前10名：\n\n{emoji.emojize(':wine_glass: :cocktail_glass: :tropical_drink: :wine_glass: :cocktail_glass: :tropical_drink:')}\n\n" + ''.join(reply_messages)

    return final_reply_message