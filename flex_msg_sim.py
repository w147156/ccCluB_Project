from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction, PostbackAction

def create_flex_message_sim(reply_token):
    line_bot_api = LineBotApi('9STVARbASfkAlRERVnFWsrljqdUSKpgFEVaXonug52xCGy2CJzdU73CI4vrnWFn8eAH47+jSBTj7O1bd/qQ7DsunYamEWNjk4nwbY9SYWDCHGQBD5hdU1uFB+7d30vHNjdyJlwv+AQBNThArqXLOCAdB04t89/1O/w1cDnyilFU=')

    flex_message = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://onepage.nownews.com/sites/default/files/styles/list_big_new_thematic/public/2020-07/%E8%AA%BF%E9%85%921.jpg?h=d66c01e2&itok=n7oZ0IVU",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "http://linecorp.com/"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "請選擇喜歡的基底",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                        {"type": "icon", "size": "xl", "url": "https://www.emojiall.com/images/240/emojipedia/1f974.png"},
                        {"type": "icon", "size": "xl", "url": "https://www.emojiall.com/images/240/emojipedia/1f974.png"},
                        {"type": "icon", "size": "xl", "url": "https://www.emojiall.com/images/240/emojipedia/1f974.png"},
                        {"type": "icon", "size": "xl", "url": "https://www.emojiall.com/images/240/emojipedia/1f974.png"},
                        {"type": "icon", "url": "https://www.emojiall.com/images/240/emojipedia/1f974.png", "size": "xl"},
                        {"type": "icon", "url": "https://www.emojiall.com/images/240/emojipedia/1f974.png", "size": "xl"},
                        {"type": "icon", "url": "https://www.emojiall.com/images/240/emojipedia/1f974.png", "size": "xl"},
                        {"type": "icon", "url": "https://www.emojiall.com/images/240/emojipedia/1f974.png", "size": "xl"}
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {"type": "box","layout": "vertical","contents": [
                    {"type": "button","action": {"type": "message", "label": "伏特加","text": "伏特加sim"}},
                    {"type": "button","action": {"type": "message", "label": "琴酒","text": "琴酒sim"}},
                    {"type": "button","action": {"type": "message", "label": "蘭姆酒","text": "蘭姆酒sim"}}
                    ]
                },
                {"type": "box","layout": "vertical","contents": [
                    {"type": "button","action": {"type": "message", "label": "龍舌蘭","text": "龍舌蘭sim"}},
                    {"type": "button","action": {"type": "message", "label": "威士忌","text": "威士忌sim"}},
                    {"type": "button","action": {"type": "message", "label": "利口酒","text": "利口酒sim"}}
                    ]
                },
                {"type": "box","layout": "vertical","contents": [
                    {"type": "button","action": {"type": "message", "label": "清酒","text": "清酒sim"}},
                    {"type": "button","action": {"type": "message", "label": "燒酒","text": "燒酒sim"}},
                    {"type": "button","action": {"type": "message", "label": "啤酒","text": "啤酒sim"}}
                    ]
                }
            ],
    "flex": 0
    }
}

    return FlexSendMessage(alt_text='Flex Message', contents=flex_message)
