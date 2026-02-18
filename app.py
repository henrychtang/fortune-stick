from flask import Flask, render_template, jsonify
import random
import json
import os
from datetime import datetime

app = Flask(__name__)

# 122車公96支簽文
FORTUNE_STICKS = [
    {
        "number": 1,
        "type": "上籤",
        "poem": "靈雞啄粟在籬籠，羽翰雖成未得通；\n早晚忽然頭角露，風雲際會出籠中。",
        "meaning": "此籤主先難後易。凡事初時雖有阻滯，但只要堅持，終必成功。",
        "career": "事業初時有阻，終必亨通",
        "wealth": "財運漸佳，宜守不宜急",
        "love": "姻緣天定，佳偶天成",
        "health": "病遇良醫，漸漸痊癒"
    },
    {
        "number": 2,
        "type": "中籤",
        "poem": "枯木逢春色更鮮，花開結實富多年；\n桃源盛景人爭羨，子孫綿綿福澤全。",
        "meaning": "此籤主否極泰來。運氣將由衰轉盛，宜把握時機。",
        "career": "事業轉機，宜積極進取",
        "wealth": "財運回升，有意外之財",
        "love": "感情和好，破鏡重圓",
        "health": "身體漸康，精神爽朗"
    },
    {
        "number": 3,
        "type": "上籤",
        "poem": "鯤鯨變化北溟中，一日乘風九萬重；\n從此翱翔天地外，凌霄直上看飛龍。",
        "meaning": "此籤主鵬程萬里。有大展鴻圖之象，宜積極進取。",
        "career": "事業騰飛，宜大展拳腳",
        "wealth": "財源廣進，投資有利",
        "love": "桃花旺盛，喜結良緣",
        "health": "身強力壯，百病不侵"
    },
    # {
    #     "number": 4,
    #     "type": "下籤",
    #     "poem": "風卷楊花未有情，水面浮萍卻自輕；\n勸君莫作閒遊蕩，且向書窗勤讀經。",
    #     "meaning": "此籤主虛浮不實。宜安份守己，不可妄動。",
    #     "career": "事業不穩，宜守不宜攻",
    #     "wealth": "財來財去，難以積聚",
    #     "love": "感情浮動，難以長久",
    #     "health": "體弱多病，宜加調養"
    # },
    {
        "number": 5,
        "type": "中籤",
        "poem": "蚌蛤生珠在綠波，龍蛇混雜勢難和；\n澄清四海功名就，一躍天梯上玉珂。",
        "meaning": "此籤主先苦後甜。雖有混亂，終必澄清。",
        "career": "事業有阻，終必亨通",
        "wealth": "財運浮沉，宜保守投資",
        "love": "感情波折，終成眷屬",
        "health": "病有反覆，終得痊癒"
    },
    {
        "number": 6,
        "type": "上籤",
        "poem": "月出光輝四海明，前途照耀太平生；\n求名求利皆如意，正是人間有福人。",
        "meaning": "此籤主光明前景。凡事皆順遂，福祿雙全。",
        "career": "事業順遂，步步高陞",
        "wealth": "財運亨通，正偏財皆旺",
        "love": "婚姻美滿，家庭幸福",
        "health": "身心康泰，平安喜樂"
    },
    # {
    #     "number": 7,
    #     "type": "下籤",
    #     "poem": "田園價值久漁耕，不料新禾竟不成；\n早把青苗分付火，枉勞心力誤蒼生。",
    #     "meaning": "此籤主徒勞無功。所作之事難以成功，宜及時止損。",
    #     "career": "事業多阻，難以發展",
    #     "wealth": "投資失利，宜止損離場",
    #     "love": "感情無果，宜放手",
    #     "health": "病情反覆，宜尋名醫"
    # },
    {
        "number": 8,
        "type": "中籤",
        "poem": "一年作事少成功，破耗虛名總是空；\n寄語時人宜謹守，莫教春日等秋風。",
        "meaning": "此籤主虛名無實。宜腳踏實地，不可好高騖遠。",
        "career": "事業平平，宜腳踏實地",
        "wealth": "收支平衡，難有積蓄",
        "love": "感情平淡，宜細水長流",
        "health": "身體無礙，宜多加保養"
    },
    {
        "number": 9,
        "type": "上籤",
        "poem": "龍頭虎踞勢崢嶸，指日飛騰上玉京；\n萬里風雲皆入夢，九天雨露盡沾身。",
        "meaning": "此籤主飛黃騰達。有龍虎之勢，必成大業。",
        "career": "事業騰飛，前程似錦",
        "wealth": "大發橫財，富貴逼人",
        "love": "金玉良緣，百年好合",
        "health": "龍精虎猛，長壽康寧"
    },
    {
        "number": 10,
        "type": "中籤",
        "poem": "花花葉葉正當時，富貴榮華有根基；\n若得栽培須著力，前途遠大莫遲疑。",
        "meaning": "此籤主時機正好。宜把握機會，努力耕耘。",
        "career": "事業正當時，宜努力進取",
        "wealth": "財運正旺，宜積極投資",
        "love": "良緣當前，宜把握機會",
        "health": "身體康健，精神飽滿"
    },
    # {
    #     "number": 11,
    #     "type": "下籤",
    #     "poem": "浪靜風平沒是非，舟人撐櫓向前移；\n忽然浪起風頭急，險些翻船喪命時。",
    #     "meaning": "此籤主平地風波。雖然平靜，仍須提防突發變故。",
    #     "career": "事業有變，宜守不宜攻",
    #     "wealth": "財運有損，宜保守理財",
    #     "love": "感情生變，宜多加溝通",
    #     "health": "健康有險，宜多加注意"
    # },
    {
        "number": 12,
        "type": "上籤",
        "poem": "紅輪西墜兔東升，陰陽交會定太平；\n凡事任他無刻意，自然亨福到家庭。",
        "meaning": "此籤主陰陽和諧。凡事順其自然，福自天降。",
        "career": "事業順利，水到渠成",
        "wealth": "財運平穩，不求自來",
        "love": "姻緣和諧，白頭偕老",
        "health": "陰陽調和，百病不生"
    },
    {
        "number": 13,
        "type": "中籤",
        "poem": "風雲致雨落洋洋，天災時氣必有傷；\n命內此事難和順，更宜修善祈福康。",
        "meaning": "此籤主有災難。宜修心積德，以化解凶煞。",
        "career": "事業多艱，宜多行善積德",
        "wealth": "財運受損，宜守不宜攻",
        "love": "感情有阻，宜多包容",
        "health": "健康有損，宜修心養性"
    },
    {
        "number": 14,
        "type": "上籤",
        "poem": "宛如仙鶴出樊籠，脫卻羈絆處處通；\n南北東西無阻隔，任君飛翔九霄中。",
        "meaning": "此籤主自由自在。脫離束縛，無往不利。",
        "career": "事業自由發展，無往不利",
        "wealth": "財路暢通，四方來財",
        "love": "感情自由，無拘無束",
        "health": "身心自由，無病無痛"
    },
    # {
    #     "number": 15,
    #     "type": "下籤",
    #     "poem": "離鄉別井去尋謀，歷盡風霜志未酬；\n寄語時人宜謹守，莫教春日等寒秋。",
    #     "meaning": "此籤主奔波勞碌。宜守舊，不宜外出發展。",
    #     "career": "事業在外不順，宜返鄉發展",
    #     "wealth": "財運不佳，難以積聚",
    #     "love": "離鄉背井，感情疏遠",
    #     "health": "奔波勞碌，身體受損"
    # },
    {
        "number": 16,
        "type": "中籤",
        "poem": "龍虎相逢在道途，忽然平地起風波；\n勸君莫作虛妄事，守舊安居是福窩。",
        "meaning": "此籤主口舌是非。宜低調行事，避免爭執。",
        "career": "事業有是非，宜低調處理",
        "wealth": "財運平平，宜守舊",
        "love": "感情有爭執，宜多溝通",
        "health": "情緒不穩，宜靜心修養"
    },
    {
        "number": 17,
        "type": "上籤",
        "poem": "池中龍馬已非常，一日乘風九萬翔；\n從此翱翔天地外，凌霄直上看飛揚。",
        "meaning": "此籤主飛黃騰達。如龍馬乘風，一飛沖天。",
        "career": "事業騰飛，一飛沖天",
        "wealth": "大發其財，富貴雙全",
        "love": "良緣天賜，美滿姻緣",
        "health": "身強力壯，百病不侵"
    },
    {
        "number": 18,
        "type": "中籤",
        "poem": "綠柳青青正芳菲，逢春桃李又開花；\n勸君莫作遲疑計，自有佳音到汝家。",
        "meaning": "此籤主春回大地。萬物復甦，好事將至。",
        "career": "事業轉機，宜把握時機",
        "wealth": "財運回升，有意外之喜",
        "love": "桃花盛開，良緣將至",
        "health": "身體康復，精神飽滿"
    },
    # {
    #     "number": 19,
    #     "type": "下籤",
    #     "poem": "心中有事最難忘，慾望思量不得長；\n寄語時人宜謹守，莫教好事變成殃。",
    #     "meaning": "此籤主心事重重。宜放寬心胸，不可鑽牛角尖。",
    #     "career": "事業有憂，宜放寬心",
    #     "wealth": "財運不順，宜守舊",
    #     "love": "感情有憂，宜多溝通",
    #     "health": "憂思傷身，宜放鬆心情"
    # },
    {
        "number": 20,
        "type": "上籤",
        "poem": "桃李春風花正開，錦繡文章映日來；\n一朝折桂蟾宮去，萬里鵬程任往來。",
        "meaning": "此籤主金榜題名。學業事業皆有成，前途無量。",
        "career": "事業有成，前途無量",
        "wealth": "財運亨通，正偏財皆旺",
        "love": "姻緣美滿，琴瑟和鳴",
        "health": "身心康泰，平安喜樂"
    },
    {
        "number": 21,
        "type": "中籤",
        "poem": "枯木逢春色更鮮，花開結實富多年；\n桃源盛景人爭羨，子孫綿綿福澤全。",
        "meaning": "此籤主否極泰來。運氣將由衰轉盛，宜把握時機。",
        "career": "事業轉機，宜積極進取",
        "wealth": "財運回升，有意外之財",
        "love": "感情和好，破鏡重圓",
        "health": "身體漸康，精神爽朗"
    },
    {
        "number": 22,
        "type": "上籤",
        "poem": "日出東方萬丈高，前途照耀顯英豪；\n功名富貴天註定，一躍龍門步步高。",
        "meaning": "此籤主旭日東昇。前途光明，步步高升。",
        "career": "事業蒸蒸，日漸高升",
        "wealth": "財運亨通，日進斗金",
        "love": "姻緣美滿，幸福甜蜜",
        "health": "身體康健，精神飽滿"
    },
    # {
    #     "number": 23,
    #     "type": "下籤",
    #     "poem": "暗箭飛來最難防，是非口舌惹災殃；\n勸君莫作虛妄事，守舊安居是福鄉。",
    #     "meaning": "此籤主暗箭難防。宜小心謹慎，避免是非。",
    #     "career": "事業有小人，宜謹慎防範",
    #     "wealth": "財運受損，宜守不宜攻",
    #     "love": "感情有變，宜多留意",
    #     "health": "小心意外，注意安全"
    # },
    {
        "number": 24,
        "type": "中籤",
        "poem": "風平浪靜可行舟，恰是中秋月一輪；\n凡事不須多用力，自然榮顯耀門庭。",
        "meaning": "此籤主順其自然。不必強求，好事自來。",
        "career": "事業平穩，順其自然",
        "wealth": "財運平穩，不求自來",
        "love": "感情穩定，水到渠成",
        "health": "身體無礙，平安喜樂"
    },
    {
        "number": 25,
        "type": "上籤",
        "poem": "龍門此日又重開，躍過三級喜自來；\n從此蓬萊添景福，春風滿面笑顏開。",
        "meaning": "此籤主魚躍龍門。一舉成功，福祿雙全。",
        "career": "事業成功，一躍龍門",
        "wealth": "大發橫財，富貴逼人",
        "love": "良緣天賜，喜結連理",
        "health": "百病全消，身強力壯"
    },
    # {
    #     "number": 26,
    #     "type": "下籤",
    #     "poem": "行船又遇打頭風，前進無功後退凶；\n寄語時人宜靜守，莫教妄動反招窮。",
    #     "meaning": "此籤主逆風行舟。進退兩難，宜靜守待時。",
    #     "career": "事業受阻，宜靜守",
    #     "wealth": "投資失利，宜止損",
    #     "love": "感情不順，宜冷靜",
    #     "health": "病情反覆，宜休養",
    #     "hk_interpretation": {
    #         "economy": "香港經濟發展面臨逆風，投資環境較為困難，建議保守策略，不宜冒進擴張",
    #         "finance": "金融市場波動較大，投資需謹慎，建議保守理財，現金為王，保留實力等待時機",
    #         "society": "社會氛圍需要更多包容與溝通，各方宜保持理性，避免對立升級，和諧共處方能渡過難關",
    #         "health": "公共衛生仍需關注，社會需要時間休養生息，注重身心平衡",
    #         "advice": [
    #             "以守為攻 - 穩固現有基礎，不宜貿然改革",
    #             "審時度勢 - 耐心等待轉機，時機成熟再行動",
    #             "積聚實力 - 利用這段時間提升競爭力",
    #             "團結一致 - 社會各界同心協力，共渡時艱"
    #         ]
    #     }
    # },
    {
        "number": 27,
        "type": "中籤",
        "poem": "花開花謝滿園春，富貴榮華總是空；\n勸君莫作虛妄計，守舊安居是福庭。",
        "meaning": "此籤主虛華不實。宜腳踏實地，不可貪圖虛名。",
        "career": "事業平平，宜腳踏實地",
        "wealth": "收支平衡，難有積蓄",
        "love": "感情平淡，宜細水長流",
        "health": "身體無礙，宜多加保養"
    },
    {
        "number": 28,
        "type": "上籤",
        "poem": "玉兔東升萬里明，前途照耀顯崢嶸；\n求名求利皆如意，正是人間有福人。",
        "meaning": "此籤主前途光明。凡事皆順遂，福祿雙全。",
        "career": "事業順遂，步步高升",
        "wealth": "財運亨通，正偏財皆旺",
        "love": "婚姻美滿，家庭幸福",
        "health": "身心康泰，平安喜樂"
    },
    # {
    #     "number": 29,
    #     "type": "下籤",
    #     "poem": "烏雲遮月暗無光，遇事諸多不順常；\n寄語時人宜謹守，莫教好事變成殃。",
    #     "meaning": "此籤主運氣低迷。諸事不順，宜謹慎守舊。",
    #     "career": "事業多阻，宜守不宜攻",
    #     "wealth": "財運不佳，難以積聚",
    #     "love": "感情不順，宜多包容",
    #     "health": "身體不適，宜多加調養"
    # },
    {
        "number": 30,
        "type": "中籤",
        "poem": "雲開霧散月重明，枯木逢春葉又生；\n凡事從頭皆改變，自然家國保安寧。",
        "meaning": "此籤主否極泰來。運氣將由衰轉盛，宜把握時機。",
        "career": "事業轉機，宜積極進取",
        "wealth": "財運回升，有意外之財",
        "love": "感情和好，破鏡重圓",
        "health": "身體漸康，精神爽朗"
    }
]

# 香港來年展望專用解讀
HK_OUTLOOK_TEMPLATE = {
    "title": "香港來年展望",
    "subtitle": "根據122車公籤文預測",
    "aspects": {
        "economy": {"title": "經濟", "icon": "📈"},
        "finance": {"title": "金融", "icon": "💰"},
        "society": {"title": "社會", "icon": "🤝"},
        "health": {"title": "健康", "icon": "🏥"}
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hk-outlook")
def hk_outlook():
    """香港來年展望頁面"""
    current_year = datetime.now().year
    # 如果提供了籤號參數，使用該籤；否則隨機選擇一籤
    from flask import request
    fortune_number = request.args.get('fortune', type=int)
    if fortune_number:
        fortune = next((s for s in FORTUNE_STICKS if s["number"] == fortune_number), None)
    else:
        fortune = random.choice(FORTUNE_STICKS)
    
    # 添加香港專屬解讀
    if fortune and "hk_interpretation" not in fortune:
        hk_interpretations = {
            "上籤": {
                "economy": "香港經濟蓬勃發展，百業興旺，適合拓展商機。新興產業蓬勃發展，創造就業機會。",
                "finance": "金融市場活躍，投資機會良好，股市樓市皆有上升空間，宜把握時機。",
                "society": "社會和諧穩定，市民安居樂業，各界齊心協力，共創繁榮。",
                "health": "公共衛生良好，醫療系統完善，市民身體健康，精神飽滿。",
                "advice": ["把握機遇，積極進取", "拓展商機，乘勢而上", "投資有道，財源廣進", "和諧共處，共創佳績"]
            },
            "中籤": {
                "economy": "經濟平穩發展，宜穩中求進，腳踏實地，不宜冒進。",
                "finance": "財運平穩，宜保守理財，積少成多，不宜投機。",
                "society": "社會氛圍平和，需要更多溝通理解，化解分歧。",
                "health": "整體健康良好，宜注意保養，預防勝於治療。",
                "advice": ["穩中求進，量力而行", "韜光養晦，蓄勢待發", "保守理財，積穀防饑", "溝通理解，和諧共處"]
            },
            "下籤": {
                "economy": "經濟發展面臨逆風，投資環境較為困難，建議保守策略，不宜貿然改革。",
                "finance": "金融市場波動較大，投資需謹慎，建議保守理財，現金為王，保留實力等待時機。",
                "society": "社會氛圍需要更多包容與溝通，各方宜保持理性，避免對立升級，和諧共處方能渡過難關。",
                "health": "公共衛生仍需關注，社會需要時間休養生息，注重身心平衡。",
                "advice": ["以守為攻，穩固基礎", "審時度勢，耐心等待", "積聚實力，提升競爭力", "團結一致，共渡時艱"]
            }
        }
        fortune_type = fortune["type"]
        if fortune_type in hk_interpretations:
            fortune["hk_interpretation"] = hk_interpretations[fortune_type]
    
    return render_template("hk_outlook.html", year=current_year, fortune=fortune)

@app.route("/api/draw")
def draw_fortune():
    """抽一支籤"""
    stick = random.choice(FORTUNE_STICKS)
    return jsonify(stick)

@app.route("/api/draw-hk")
def draw_hk_fortune():
    """抽香港來年展望籤"""
    stick = random.choice(FORTUNE_STICKS)
    
    # 添加香港專屬解讀
    hk_interpretations = {
        "上籤": {
            "economy": "香港經濟蓬勃發展，百業興旺，適合拓展商機",
            "finance": "金融市場活躍，投資機會良好，宜把握時機",
            "society": "社會和諧穩定，市民安居樂業，共創繁榮",
            "health": "公共衛生良好，市民身體健康，精神飽滿",
            "advice": ["把握機遇", "積極進取", "乘勢而上", "共創佳績"]
        },
        "中籤": {
            "economy": "經濟平穩發展，宜穩中求進，腳踏實地",
            "finance": "財運平穩，宜保守理財，積少成多",
            "society": "社會氛圍平和，需要更多溝通理解",
            "health": "整體健康良好，宜注意保養",
            "advice": ["穩中求進", "量力而行", "韜光養晦", "蓄勢待發"]
        },
        "下籤": {
            "economy": "經濟發展面臨逆風，投資環境較為困難，建議保守策略",
            "finance": "金融市場波動較大，投資需謹慎，建議保守理財",
            "society": "社會氛圍需要更多包容與溝通，各方宜保持理性",
            "health": "公共衛生仍需關注，社會需要時間休養生息",
            "advice": ["以守為攻", "審時度勢", "積聚實力", "團結一致"]
        }
    }
    
    fortune_type = stick["type"]
    if fortune_type in hk_interpretations:
        stick["hk_interpretation"] = hk_interpretations[fortune_type]
    
    return jsonify(stick)

@app.route("/api/all")
def get_all_fortunes():
    """獲取所有籤文"""
    return jsonify(FORTUNE_STICKS)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
