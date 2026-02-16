import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定
# ==========================================
st.set_page_config(
    page_title="2026 復興區花季行程規劃 (風管處地圖融合版)",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (iPhone 深色模式/黑底黑字 修復專區)
# ==========================================
st.markdown("""
    <style>
    /* 1. 強制全站背景為粉色，字體為深色 */
    .stApp {
        background-color: #FFF0F5;
        font-family: "Microsoft JhengHei", sans-serif;
        color: #333333 !important;
    }
    
    /* 2. 強制所有一般文字元素為深色 */
    p, div, span, h1, h2, h3, h4, h5, h6, label, .stMarkdown {
        color: #333333 !important;
    }

    /* === 3. 核心修復：強制輸入框與選單在深色模式下維持「白底黑字」 === */
    /* 針對輸入框容器、下拉選單容器 */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important; /* 強制白底 */
        border: 1px solid #cccccc !important;
        color: #333333 !important; /* 強制黑字 */
    }
    
    /* 針對輸入框內的文字 (日期、打字) */
    input {
        color: #333333 !important;
    }
    
    /* 針對下拉選單內的文字 */
    div[data-baseweb="select"] span {
        color: #333333 !important;
    }
    
    /* 針對下拉選單彈出的列表 */
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
    }
    li[data-baseweb="option"] {
        color: #333333 !important;
    }

    /* 針對 SVG 圖示 (如日曆icon、下拉箭頭) 強制轉深色 */
    svg {
        fill: #333333 !important;
        color: #333333 !important;
    }

    /* === 4. 特別加強：日期選單高亮 (使用者指定) === */
    div[data-testid="stDateInput"] > label {
        color: #C71585 !important; /* 深粉紅 */
        font-size: 24px !important; /* 加大字體 */
        font-weight: 900 !important;
        text-shadow: 0px 0px 5px rgba(255, 105, 180, 0.6);
        margin-bottom: 10px !important;
        display: block;
    }
    div[data-testid="stDateInput"] div[data-baseweb="input"] {
        border: 3px solid #FF1493 !important; /* 粗邊框 */
        background-color: #FFF5F7 !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(255, 20, 147, 0.3); /* 發光特效 */
    }

    /* 隱藏官方元件 */
    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 標題區 (維持白字，這裡需要反向設定) */
    .header-box {
        background: linear-gradient(135deg, #FF69B4 0%, #FFB7C5 100%);
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        color: white !important;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
        margin-top: -60px;
    }
    /* 標題區內的文字需強制反白，覆蓋上面的全域黑字 */
    .header-box h1, .header-box div, .header-box span {
        color: white !important;
    }
    .header-title { font-size: 28px; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.2); }
    
    /* 輸入卡片 */
    .input-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #FFE4E1;
        margin-bottom: 20px;
    }
    
    /* 按鈕 */
    .stButton>button {
        width: 100%;
        background-color: #FF1493;
        color: white !important;
        border-radius: 50px;
        border: none;
        padding: 12px 0;
        font-weight: bold;
        transition: 0.3s;
        font-size: 18px;
    }
    
    /* 資訊看板 */
    .info-box {
        background-color: #fffbea;
        border-left: 5px solid #FFD700;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    
    /* 時間軸 */
    .timeline-item {
        border-left: 3px solid #FF69B4;
        padding-left: 20px;
        margin-bottom: 20px;
        position: relative;
    }
    .timeline-item::before {
        content: '🌸';
        position: absolute;
        left: -13px;
        top: 0;
        background: #FFF0F5;
        border-radius: 50%;
    }
    .day-header {
        background: #FFE4E1;
        color: #C71585 !important;
        padding: 5px 15px;
        border-radius: 15px;
        display: inline-block;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .spot-title { font-weight: bold; color: #C71585 !important; font-size: 18px; }
    .spot-tag { 
        font-size: 12px; background: #FFE4E1; color: #D87093 !important; 
        padding: 2px 8px; border-radius: 10px; margin-right: 5px;
    }
    
    /* 住宿卡片 */
    .hotel-card {
        background: #F8F8FF;
        border-left: 5px solid #9370DB;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .hotel-tag {
        font-size: 11px;
        background: #9370DB;
        color: white !important;
        padding: 2px 6px;
        border-radius: 8px;
        margin-right: 5px;
    }
    
    /* 景點名錄小卡 */
    .mini-card {
        background: white;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #eee;
        font-size: 14px;
        margin-bottom: 8px;
        border-left: 3px solid #FF69B4;
    }
    .flower-badge {
        background: #FF69B4; color: white !important; padding: 1px 5px; border-radius: 4px; font-size: 11px; margin-left: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (融合風管處地圖 + 原有資料)
# ==========================================
# 資料來源：本系統整合 2026 北橫櫻花地圖與在地旅遊資訊
all_spots_db = [
    # --- 【重點 1】您指定的 6 大名所 (置頂) ---
    {"name": "翠墨莊園 (翠墨山莊)", "region": "前山", "month": [1, 2], "type": "網美", "flower": "緋寒櫻", "fee": "門票$150", "desc": "三民里大窩部落，精緻日式造景。"},
    {"name": "詩朗櫻花坡 (詩朗道路)", "region": "前山", "month": [1, 2, 3], "type": "賞花", "flower": "多品種櫻花", "fee": "免門票", "desc": "澤仁里詩朗部落。花期：枝垂櫻1/20-2/15、八重櫻2/10-3/2、吉野櫻2/15-3/2。"},
    {"name": "詩朗部落祕境", "region": "前山", "month": [1, 2], "type": "健行", "flower": "枝垂櫻", "fee": "免門票", "desc": "澤仁里詩朗部落深處，在地人才知道的幽靜步道。"},
    {"name": "中巴陵櫻木花道", "region": "後山", "month": [2, 3], "type": "賞花", "flower": "昭和櫻/千島櫻", "fee": "免門票", "desc": "華陵里中巴陵，免費粉紅隧道。花期：昭和櫻2/18-3/10、千島櫻2/28-3/15。"},
    {"name": "青鬆園 (輕鬆園)", "region": "後山", "month": [2, 3], "type": "賞花", "flower": "墨染櫻", "fee": "門票$100", "desc": "華陵里上巴陵比該路段，賞花新秘境。電話：0937-840-134。"},
    {"name": "恩愛農場", "region": "後山", "month": [2, 3], "type": "賞花", "flower": "千島/富士櫻", "fee": "門票$100", "desc": "華陵里上巴陵中心路頂端，全台最知名。電話：03-3912335。"},

    # --- 【重點 2】角板山・東眼山・羅浮一帶 (前山) ---
    {"name": "悠然秘境小屋", "region": "前山", "month": [2, 3], "flower": "吉野櫻", "type": "賞花", "fee": "門票$50", "desc": "三民隱藏版。導航「復興觀音洞」再依指標。電話：0958-761-027。"},
    {"name": "新櫻花莊園", "region": "前山", "month": [1, 2], "flower": "山櫻花", "type": "賞花", "fee": "洽詢", "desc": "復興區詩朗19號。電話：0922-295-888。"},
    {"name": "角板山行館", "region": "前山", "month": [1, 2], "flower": "梅花/山櫻", "type": "賞花", "fee": "免門票", "desc": "北橫賞花起點，戰備隧道。山櫻花期：1/20-2/15。"},
    {"name": "東眼山櫻花大道", "region": "前山", "month": [1, 2], "flower": "山櫻花", "type": "健行", "fee": "免門票", "desc": "往東眼山森林遊樂區桃119線。花期：1/25-2/15。"},
    {"name": "羅馬公路", "region": "前山", "month": [1, 2], "flower": "山櫻花", "type": "兜風", "fee": "免門票", "desc": "桃118線，最美兜風路線。花期：1/25-2/15。"},
    {"name": "小烏來風景區", "region": "前山", "month": [1, 2], "flower": "山櫻花", "type": "景觀", "fee": "門票$50", "desc": "義盛義興里下方內1鄰4-6號。花期：1/25-2/15。"},
    {"name": "成福道路", "region": "前山", "month": [1, 2], "flower": "山櫻花", "type": "兜風", "fee": "免門票", "desc": "東眼山支線 (桃119線) 秘境。"},
    {"name": "丸山咖啡", "region": "前山", "month": [2], "flower": "景觀櫻花", "type": "美食", "fee": "低消", "desc": "海拔600m景觀餐廳。"},
    {"name": "新溪口吊橋", "region": "前山", "month": [1, 2, 3], "flower": "景觀", "type": "景觀", "fee": "門票$50", "desc": "全台最長懸索橋。"},

    # --- 【重點 3】高義・爺亨・下巴陵一帶 (部落) ---
    {"name": "培雅境露營區", "region": "部落", "month": [1, 2, 3], "flower": "昭和櫻/千島櫻", "type": "露營", "fee": "洽詢", "desc": "澤仁里新興露營秘境，被粉紅花海包圍。"},
    {"name": "卡維蘭部落", "region": "部落", "month": [2, 3], "flower": "八重櫻/吉野櫻", "type": "秘境", "fee": "免門票", "desc": "高義村。吉野櫻 2/12-3/5、八重櫻 2/10-3/2。"},
    {"name": "光華櫻花故事林道", "region": "部落", "month": [1, 2, 3], "flower": "昭和櫻", "type": "秘境", "fee": "免門票", "desc": "光華國小旁。昭和櫻 2/20-3/5。"},
    {"name": "比亞外櫻花迎賓道", "region": "部落", "month": [1, 2, 3], "flower": "昭和櫻/山櫻", "type": "生態", "fee": "免門票", "desc": "昭和櫻 2/12-3/5、山櫻花 1/25-2/25。"},
    {"name": "爺亨梯田", "region": "部落", "month": [1, 2], "flower": "山櫻/富士櫻", "type": "景觀", "fee": "免門票", "desc": "爺亨道路。山櫻 1/25-2/20、富士櫻 1/30-2/20。"},
    {"name": "巴陵道路", "region": "部落", "month": [2, 3], "flower": "八重/香水/吉野", "type": "兜風", "fee": "免門票", "desc": "花期：八重櫻2/10-2/28、香水櫻2/18-3/10。"},
    {"name": "內奎輝部落", "region": "部落", "month": [1, 2], "flower": "野櫻", "type": "秘境", "fee": "免門票", "desc": "深山寧靜部落。"},
    {"name": "高義蘭(夏蝶冬櫻)", "region": "部落", "month": [2], "flower": "香水櫻", "type": "賞花", "fee": "免門票", "desc": "新開發的山谷雙色花海。"},
    {"name": "雪霧鬧部落", "region": "部落", "month": [2, 3], "flower": "桃花/櫻花", "type": "秘境", "fee": "免門票", "desc": "雲端上的部落。"},

    # --- 【重點 4】中巴陵・上巴陵一帶 (後山) ---
    {"name": "谷點咖啡民宿", "region": "後山", "month": [2], "flower": "櫻花景觀", "type": "美食", "fee": "低消", "desc": "中巴陵絕佳視野。電話：03-3912415。"},
    {"name": "拉拉山遊客中心", "region": "後山", "month": [2, 3], "flower": "千島櫻", "type": "賞花", "fee": "免門票", "desc": "華陵里7鄰29號。停車場就是絕美景點。"},
    {"name": "上巴陵九鄰櫻花部落", "region": "後山", "month": [2, 3], "flower": "櫻花", "type": "秘境", "fee": "免門票", "desc": "復興區詩朗19號 (地圖標示位)。"},
    {"name": "拉拉山秘密花園", "region": "後山", "month": [2, 3], "flower": "櫻花", "type": "賞花", "fee": "洽詢", "desc": "復興區神木路。電話：0985-430-486。"},
    {"name": "觀雲休憩農莊", "region": "後山", "month": [2, 3], "flower": "昭和櫻", "type": "賞花", "fee": "免門票", "desc": "中心路145-6號。電話：0965-357-601。"},
    {"name": "楓墅農莊", "region": "後山", "month": [2], "flower": "昭和櫻", "type": "秘境", "fee": "清潔費", "desc": "中心路210巷17號。電話：0965-357-601。"},
    {"name": "光明休閒農場", "region": "後山", "month": [3], "flower": "霧社櫻", "type": "美食", "fee": "需用餐", "desc": "華陵村11鄰192-8號。稀有白櫻。電話：0913-566-218。"},
    {"name": "中心路沿線", "region": "後山", "month": [2, 3], "flower": "富士/昭和/千島", "type": "兜風", "fee": "部分收費", "desc": "富士櫻2/18-3/10、昭和櫻2/20-3/5。"},
    {"name": "嶺鎮渡假木屋", "region": "後山", "month": [2, 3], "flower": "櫻花", "type": "景觀", "fee": "需消費", "desc": "中心路210巷2號。電話：0928-036-122。"},
    {"name": "拉拉山巨木區", "region": "後山", "month": [1, 2, 3, 4], "flower": "神木", "type": "健行", "fee": "門票$100", "desc": "千年紅檜群深呼吸。電話：03-3912142。"},
    {"name": "俠雲山莊", "region": "後山", "month": [2], "flower": "昭和櫻", "type": "賞花", "fee": "免門票", "desc": "梯田式櫻花林。"},
    {"name": "八福原櫻園", "region": "後山", "month": [2, 3], "flower": "富士櫻", "type": "賞花", "fee": "門票制", "desc": "卡拉部落新秘境。"},
    {"name": "櫻花莊園", "region": "後山", "month": [2, 3], "flower": "雙色櫻", "type": "住宿", "fee": "住宿客", "desc": "精緻民宿造景。"},
    {"name": "巴陵古道生態園區", "region": "後山", "month": [2], "flower": "山櫻/昭和", "type": "文化", "fee": "免門票", "desc": "森林步道與博物館。"},
    {"name": "拉拉山5.5K觀景台", "region": "後山", "month": [2], "flower": "昭和櫻", "type": "攝影", "fee": "免門票", "desc": "攝影師拍攝彎道名點。"}
]

# 住宿資料庫
hotels_db = [
    # 前山
    {"name": "復興青年活動中心", "region": "前山", "tag": "高CP值", "price": 2000, "desc": "角板山公園內，最方便。"},
    {"name": "普拉多山丘假期", "region": "前山", "tag": "歐式鄉村", "price": 3800, "desc": "三民地區黃色歐風建築。"},
    {"name": "羅浮天空溫泉飯店", "region": "前山", "tag": "溫泉", "price": 4500, "desc": "房內泡湯，設施新穎。"},
    {"name": "小烏來山莊", "region": "前山", "tag": "景觀", "price": 2800, "desc": "近天空步道。"},
    {"name": "山水奇異民宿", "region": "前山", "tag": "英式", "price": 3500, "desc": "適合拍照。"},
    {"name": "象山民宿", "region": "前山", "tag": "平價", "price": 1800, "desc": "老字號民宿。"},
    
    # 部落
    {"name": "爺亨溫泉夢幻露營", "region": "部落", "tag": "露營", "price": 3500, "desc": "櫻花樹下的豪華露營。"},
    {"name": "河那灣民宿", "region": "部落", "tag": "原民風", "price": 2200, "desc": "羅浮橋畔，親近自然。"},
    {"name": "飛鼠不渴露營區", "region": "部落", "tag": "親子", "price": 3000, "desc": "雪霧鬧雲端露營。"},
    {"name": "伊萬農場", "region": "部落", "tag": "賞櫻", "price": 1000, "desc": "知名賞櫻露營點。"},
    
    # 後山
    {"name": "恩愛農場小木屋", "region": "後山", "tag": "花海", "price": 5000, "desc": "出門就是櫻花(極難訂)。"},
    {"name": "雲山仙境民宿", "region": "後山", "tag": "雲海", "price": 4200, "desc": "上巴陵高評價景觀民宿。"},
    {"name": "谷點咖啡民宿", "region": "後山", "tag": "景觀", "price": 3800, "desc": "無敵山景視野 (含賞櫻)。"},
    {"name": "富仙境渡假旅館", "region": "後山", "tag": "便利", "price": 2500, "desc": "上巴陵鬧區，吃飯方便。"},
    {"name": "俠雲山莊", "region": "後山", "tag": "包棟", "price": 3000, "desc": "就在櫻花林旁邊。"},
    {"name": "嶺鎮渡假木屋", "region": "後山", "tag": "視野", "price": 3200, "desc": "中心路最高點，俯瞰全景。"},
    {"name": "瑞士鄉村農莊", "region": "後山", "tag": "歐風", "price": 3600, "desc": "中心路老字號民宿。"},
    {"name": "達觀山莊", "region": "後山", "tag": "神木", "price": 2800, "desc": "近拉拉山神木區入口。"},
    {"name": "侑德園民宿", "region": "後山", "tag": "木屋", "price": 3000, "desc": "上巴陵中心，環境舒適。"},
    {"name": "觀雲休憩農莊", "region": "後山", "tag": "平價", "price": 2000, "desc": "恩愛農場旁高CP值。"}
]

# ==========================================
# 4. 邏輯核心：動態行程生成演算法
# ==========================================
def generate_dynamic_itinerary(travel_date, days_str, group):
    m = travel_date.month
    
    # 1. 篩選當月可去的景點
    available_spots = [s for s in all_spots_db if m in s['month']]
    
    # 防呆：若該月無花，塞入常態景點
    if not available_spots:
        available_spots = [s for s in all_spots_db if s['flower'] in ["神木", "景觀"]]

    # 2. 分區篩選
    front_spots = [s for s in available_spots if s['region'] == "前山"]
    back_spots = [s for s in available_spots if s['region'] == "後山"]
    
    if "一日" in days_str: day_count = 1
    elif "二日" in days_str: day_count = 2
    else: day_count = 3
    
    itinerary = {}
    
    # --- Day 1: 必去賞花熱點 ---
    # 優先從您指定的熱點中挑選 Day 1 上午
    top_picks = ["角板山行館", "翠墨莊園 (翠墨山莊)", "詩朗櫻花坡", "恩愛農場"]
    d1_spot1 = next((s for s in available_spots if s['name'] in top_picks), available_spots[0])
    
    remaining = [s for s in available_spots if s['name'] != d1_spot1['name']]
    d1_spot2 = remaining[0] if remaining else d1_spot1
    
    itinerary[1] = [d1_spot1, d1_spot2]
    
    # --- Day 2: 深入後山 ---
    if day_count >= 2:
        # Day 2 上午：優先挑選後山指定新景點
        d2_priority = ["青鬆園 (輕鬆園)", "中巴陵櫻木花道", "拉拉山巨木區", "拉拉山秘密花園"]
        d2_spot1 = next((s for s in back_spots if s['name'] in d2_priority), None)
        if not d2_spot1: d2_spot1 = back_spots[0] if back_spots else front_spots[0]
        
        # Day 2 下午
        used_names = [s['name'] for s in itinerary[1]] + [d2_spot1['name']]
        d2_pool = [s for s in available_spots if s['name'] not in used_names]
        d2_spot2 = d2_pool[0] if d2_pool else d2_spot1
            
        itinerary[2] = [d2_spot1, d2_spot2]

    # --- Day 3: 回程補漏 ---
    if day_count == 3:
        used_names = [s['name'] for day in itinerary.values() for s in day]
        d3_pool = [s for s in front_spots if s['name'] not in used_names]
        if not d3_pool: d3_pool = [s for s in available_spots if s['name'] not in used_names]
        
        d3_spot1 = d3_pool[0] if d3_pool else itinerary[1][0]
        d3_spot2 = {"name": "大溪老街/復興橋", "region": "前山", "flower": "人文", "type": "採買", "fee": "免門票", "desc": "回程購買名產與豆干。"}
        
        itinerary[3] = [d3_spot1, d3_spot2]

    titles = {1: "❄️ 早春寒梅與山櫻", 2: "🌸 粉紅櫻花大爆發", 3: "🍑 桃花與吉野櫻尾聲", 4: "🌲 螢火蟲與神木季"}
    status_title = titles.get(m, "🌲 四季山林森呼吸")
    
    return status_title, itinerary

# ==========================================
# 5. 頁面內容
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌸 2026 復興區櫻花季攻略</div>
        <div class="header-subtitle">桃園市復興區長 <b>蘇佐璽</b> 邀請您 ❤️</div>
    </div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        # 日期選單 (CSS 已特別加強高亮)
        travel_date = st.date_input("📅 出發日期 (必填)", value=date(2026, 2, 14))
    with col2:
        days_str = st.selectbox("🕒 行程天數", ["一日遊 (快閃)", "二日遊 (過夜)", "三日遊 (深度)"])
        group = st.selectbox("👥 出遊夥伴", ["情侶/夫妻", "親子家庭", "長輩同行", "熱血獨旅"])
    
    if st.button("🚀 生成蘇區長推薦行程"):
        st.session_state['generated'] = True
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get('generated'):
    status_title, itinerary = generate_dynamic_itinerary(travel_date, days_str, group)
    
    st.markdown(f"""
    <div class="info-box">
        <h4>{status_title}</h4>
        <p>為您規劃 <b>{travel_date.strftime('%Y/%m/%d')}</b> 出發的 <b>{group}</b> 行程！</p>
    </div>
    """, unsafe_allow_html=True)

    # --- 顯示行程 ---
    for day, spots in itinerary.items():
        st.markdown(f'<div class="day-header">Day {day}</div>', unsafe_allow_html=True)
        
        for i, spot in enumerate(spots):
            time_label = "☀️ 上午" if i == 0 else "🌤️ 下午"
            
            # 標籤生成
            tags_html = f'<span class="spot-tag">{spot["type"]}</span>'
            tags_html += f'<span class="spot-tag">{spot["flower"]}</span>'
            if spot['region'] == "部落": tags_html += '<span class="spot-tag" style="background:#E6E6FA;color:#4B0082!important;">部落秘境</span>'
            
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">{time_label}：{spot['name']}</div>
                <div style="margin: 5px 0;">{tags_html}</div>
                <div style="font-size: 14px; color: #555;">
                    💰 {spot['fee']} <br>
                    📝 {spot['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- 住宿推薦 (僅多日遊顯示) ---
    if "一日" not in days_str:
        st.markdown("### 🏨 蘇區長精選住宿")
        
        # 簡單篩選邏輯
        if "後山" in [s['region'] for day in itinerary.values() for s in day]:
            rec_hotels = [h for h in hotels_db if h['region'] in ["後山", "部落"]]
        else:
            rec_hotels = [h for h in hotels_db if h['region'] == "前山"]
            
        # 隨機秀 3 間
        for h in random.sample(rec_hotels, min(3, len(rec_hotels))):
            st.markdown(f"""
            <div class="hotel-card">
                <div style="font-weight:bold; color:#483D8B;">{h['name']} <span class="hotel-tag">{h['tag']}</span></div>
                <div style="font-size:13px; color:#666; margin-top:3px;">
                    💲 {h['price']}起 | {h['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- 頁尾景點總覽 ---
with st.expander("📖 查看 2026 所有賞櫻熱點名錄"):
    st.markdown("#### 北橫櫻花地圖總覽")
    # 依區域分類顯示
    for region in ["前山", "部落", "後山"]:
        st.markdown(f"**【{region}區】**")
        region_spots = [s for s in all_spots_db if s['region'] == region]
        cols = st.columns(2)
        for i, s in enumerate(region_spots):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="mini-card">
                    <b>{s['name']}</b> <span class="flower-badge">{s['flower']}</span><br>
                    <span style="color:#888; font-size:12px;">{s['desc']}</span>
                </div>
                """, unsafe_allow_html=True)
