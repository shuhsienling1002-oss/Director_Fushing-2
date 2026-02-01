import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定
# ==========================================
st.set_page_config(
    page_title="2026 復興區花季行程規劃 (修正版)",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (保持原樣，微調細節)
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF0F5;
        font-family: "Microsoft JhengHei", sans-serif;
    }
    header {visibility: hidden;}
    footer {display: none !important;}
    
    .header-box {
        background: linear-gradient(135deg, #FF69B4 0%, #FFB7C5 100%);
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
        margin-top: -60px;
    }
    .header-title { font-size: 28px; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.2); }
    
    .input-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #FFE4E1;
        margin-bottom: 20px;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #FF1493;
        color: white;
        border-radius: 50px;
        border: none;
        padding: 12px 0;
        font-weight: bold;
        transition: 0.3s;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #C71585;
        transform: scale(1.02);
    }
    
    /* 資訊看板 */
    .info-box {
        background-color: #fffbea;
        border-left: 5px solid #FFD700;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .weather-tag { font-weight: bold; color: #e67e22; font-size: 18px; }
    
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
        color: #C71585;
        padding: 5px 15px;
        border-radius: 15px;
        display: inline-block;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .spot-title { font-weight: bold; color: #333; font-size: 16px; }
    .spot-desc { font-size: 14px; color: #666; }
    .spot-tag { 
        font-size: 12px; background: #FF69B4; color: white; 
        padding: 2px 8px; border-radius: 10px; margin-right: 5px;
    }
    
    /* 住宿與其他 */
    .hotel-card {
        background: #F8F8FF;
        border-left: 5px solid #9370DB;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .mini-card {
        background: white;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #eee;
        font-size: 14px;
        height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (結構優化)
# ==========================================
# 增加 "type" 標籤以區分景點性質 (賞花, 健行, 文化, 食物)
all_spots_db = [
    # 前山
    {"name": "角板山行館", "region": "前山", "month": [1, 2], "flower": "梅花/山櫻", "type": "賞花", "desc": "北橫賞花起點，戰備隧道。"},
    {"name": "東眼山櫻花大道", "region": "前山", "month": [1, 2], "flower": "山櫻花", "type": "健行", "desc": "林道兩旁紅色隧道。"},
    {"name": "羅馬公路", "region": "前山", "month": [1, 2], "flower": "山櫻花", "type": "兜風", "desc": "最美兜風路線。"},
    {"name": "翠墨莊園", "region": "前山", "month": [1, 2], "flower": "緋寒櫻", "type": "網美", "desc": "需預約，日式造景。"},
    {"name": "小烏來風景區", "region": "前山", "month": [1, 2], "flower": "山櫻花", "type": "景觀", "desc": "天空步道與瀑布。"},
    {"name": "新溪口吊橋", "region": "前山", "month": [1, 2, 3], "flower": "景觀", "type": "景觀", "desc": "全台最長懸索橋。"},
    
    # 部落
    {"name": "爺亨梯田", "region": "部落", "month": [1, 2, 3], "flower": "山櫻/桃花", "type": "景觀", "desc": "梯田地景配粉色花海。"},
    {"name": "光華櫻花故事林道", "region": "部落", "month": [2, 3], "flower": "昭和櫻", "type": "秘境", "desc": "光華國小旁浪漫林道。"},
    {"name": "比亞外部落", "region": "部落", "month": [1, 2], "flower": "昭和櫻", "type": "生態", "desc": "藍腹鷴的故鄉。"},
    
    # 後山
    {"name": "中巴陵櫻木花道", "region": "後山", "month": [2], "flower": "昭和櫻", "type": "賞花", "desc": "免費粉紅隧道必拍。"},
    {"name": "拉拉山遊客中心", "region": "後山", "month": [2, 3], "flower": "千島櫻", "type": "賞花", "desc": "停車場就是絕美景點。"},
    {"name": "恩愛農場", "region": "後山", "month": [2, 3], "flower": "千島/富士櫻", "type": "賞花", "desc": "全台最知名爆炸花海。"},
    {"name": "觀雲休憩農莊", "region": "後山", "month": [2, 3], "flower": "昭和櫻", "type": "秘境", "desc": "恩愛農場旁免門票秘境。"},
    {"name": "光明農場", "region": "後山", "month": [3], "flower": "霧社櫻", "type": "美食", "desc": "稀有白櫻配馬告雞。"},
    {"name": "拉拉山巨木區", "region": "後山", "month": [1, 2, 3, 4], "flower": "神木", "type": "健行", "desc": "千年紅檜群深呼吸。"},
    {"name": "巴陵古道生態園區", "region": "後山", "month": [2], "flower": "山櫻/昭和", "type": "文化", "desc": "森林步道與博物館。"}
]

hotels_db = [
    {"name": "復興青年活動中心", "region": "前山", "tag": "高CP值", "price": 2000, "desc": "角板山公園內，最方便。"},
    {"name": "羅浮天空溫泉飯店", "region": "前山", "tag": "溫泉", "price": 4500, "desc": "房內泡湯，設施新穎。"},
    {"name": "小烏來山莊", "region": "前山", "tag": "景觀", "price": 2800, "desc": "近天空步道。"},
    {"name": "爺亨溫泉夢幻露營", "region": "部落", "tag": "露營", "price": 3500, "desc": "櫻花樹下的豪華露營。"},
    {"name": "恩愛農場小木屋", "region": "後山", "tag": "花海", "price": 5000, "desc": "出門就是櫻花(極難訂)。"},
    {"name": "谷點咖啡民宿", "region": "後山", "tag": "景觀", "price": 3800, "desc": "無敵山景視野。"},
    {"name": "嶺鎮農場", "region": "後山", "tag": "視野", "price": 3200, "desc": "中心路最高點，俯瞰全景。"},
    {"name": "富仙境渡假旅館", "region": "後山", "tag": "便利", "price": 2500, "desc": "上巴陵鬧區，吃飯方便。"}
]

# ==========================================
# 4. 邏輯修復：動態行程生成演算法
# ==========================================
def generate_dynamic_itinerary(travel_date, days_str, group):
    m = travel_date.month
    
    # 1. 篩選當月可去的景點
    available_spots = [s for s in all_spots_db if m in s['month']]
    
    # 若該月無花，加入常態景點 (神木、吊橋) 避免空清單
    if not available_spots:
        available_spots = [s for s in all_spots_db if s['flower'] in ["神木", "景觀"]]

    # 2. 分區篩選 (為了路線順暢)
    front_spots = [s for s in available_spots if s['region'] == "前山"]
    tribe_spots = [s for s in available_spots if s['region'] == "部落"]
    back_spots = [s for s in available_spots if s['region'] == "後山"]
    
    # 3. 判斷行程天數 (將字串轉為數字)
    if "一日" in days_str: day_count = 1
    elif "二日" in days_str: day_count = 2
    else: day_count = 3
    
    itinerary = {}
    
    # --- Day 1: 必去賞花熱點 (通常以前山或剛入後山為主) ---
    # 優先選熱門點
    d1_spot1 = next((s for s in available_spots if s['name'] in ["角板山行館", "恩愛農場", "中巴陵櫻木花道"]), available_spots[0])
    # 排除已選，選第二個
    remaining = [s for s in available_spots if s['name'] != d1_spot1['name']]
    d1_spot2 = remaining[0] if remaining else d1_spot1
    
    itinerary[1] = [d1_spot1, d1_spot2]
    
    # --- Day 2: 深入後山或部落 (避免與Day1重複) ---
    if day_count >= 2:
        # Day 2 早上通常建議去健行 (拉拉山巨木區優先)
        d2_spot1 = next((s for s in back_spots if s['type'] == "健行"), None)
        if not d2_spot1: d2_spot1 = back_spots[0] if back_spots else front_spots[0]
        
        # Day 2 下午去部落或特色點 (排除已選)
        used_names = [s['name'] for s in itinerary[1]] + [d2_spot1['name']]
        d2_pool = [s for s in available_spots if s['name'] not in used_names]
        
        # 根據群體推薦
        if "親子" in group:
            d2_spot2 = next((s for s in d2_pool if s['type'] == "生態" or s['type'] == "景觀"), d2_pool[0] if d2_pool else d2_spot1)
        else:
            d2_spot2 = d2_pool[0] if d2_pool else d2_spot1
            
        itinerary[2] = [d2_spot1, d2_spot2]

    # --- Day 3: 回程與伴手禮 (補上前山未去景點) ---
    if day_count == 3:
        # 找出前山還沒去的點 (回程順路)
        used_names = [s['name'] for day in itinerary.values() for s in day]
        d3_pool = [s for s in front_spots if s['name'] not in used_names]
        
        if not d3_pool: d3_pool = [s for s in available_spots if s['name'] not in used_names]
        
        d3_spot1 = d3_pool[0] if d3_pool else itinerary[1][0]
        # Day 3 下午通常是老街或買東西，這裡用通用邏輯
        d3_spot2 = {"name": "大溪老街/復興橋", "region": "前山", "flower": "人文", "type": "採買", "desc": "回程購買名產與豆干。"}
        
        itinerary[3] = [d3_spot1, d3_spot2]

    # 花況標題
    titles = {1: "❄️ 早春寒梅與山櫻", 2: "🌸 粉紅櫻花大爆發", 3: "🍑 桃花與吉野櫻尾聲", 4: "🌲 螢火蟲與神木季"}
    status_title = titles.get(m, "🌲 四季山林森呼吸")
    
    return status_title, itinerary

# ==========================================
# 5. 頁面內容
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌸 2026 復興區花季攻略</div>
        <div class="header-subtitle">邏輯修正版：精準規劃您的每一天</div>
    </div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        travel_date = st.date_input("預計出發日期", value=date(2026, 2, 20), min_value=date(2026, 1, 1), max_value=date(2026, 4, 30))
        days = st.selectbox("行程天數", ["一日遊", "二日遊", "三日遊"])
    with col2:
        group = st.selectbox("出遊夥伴", ["情侶/夫妻", "親子家庭", "長輩樂齡", "熱血獨旅"])
        transport = st.selectbox("交通方式", ["自行開車", "大眾運輸 (客運)", "機車/單車"])
    
    generate_btn = st.button("🚀 生成邏輯正確的行程")
    st.markdown('</div>', unsafe_allow_html=True)

if generate_btn:
    # 執行演算法
    status_title, itinerary = generate_dynamic_itinerary(travel_date, days, group)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="weather-tag">{status_title}</div>
        <div>根據您選擇的 <b>{days}</b> 與 <b>{transport}</b>，我們重新計算了最佳路徑。</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🗓️ 詳細行程", "💰 精準預算", "🚗 交通建議", "🌸 景點名錄"])

    # --- Tab 1: 動態行程 ---
    with tab1:
        for day_num, spots in itinerary.items():
            st.markdown(f'<div class="day-header">Day {day_num}</div>', unsafe_allow_html=True)
            
            # 上午景點
            s1 = spots[0]
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">09:30 {s1['name']} <span class="spot-tag">{s1['region']}</span></div>
                <div class="spot-desc">{s1['desc']} ({s1['flower']})</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 午餐插曲
            lunch_text = "景觀餐廳享用原民風味餐" if s1['region'] == "後山" else "角板山商圈或路邊小吃"
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">12:30 午餐時間</div>
                <div class="spot-desc">{lunch_text}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 下午景點
            s2 = spots[1]
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">14:30 {s2['name']} <span class="spot-tag">{s2['region']}</span></div>
                <div class="spot-desc">{s2['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 只有在非最後一天顯示住宿
            if day_num < len(itinerary):
                 st.markdown(f"""
                <div class="timeline-item" style="border-color:#9370DB;">
                    <div class="spot-title" style="color:#9370DB;">18:00 入住 {s2['region']} 或鄰近地區</div>
                    <div class="spot-desc">建議選擇下方「交通住宿」頁籤中的推薦民宿。</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                 st.markdown(f"""
                <div class="timeline-item" style="border-color:#4CAF50;">
                    <div class="spot-title" style="color:#4CAF50;">17:00 快樂賦歸</div>
                    <div class="spot-desc">帶著滿滿的照片與回憶回家。</div>
                </div>
                """, unsafe_allow_html=True)

    # --- Tab 2: 經費 (邏輯修復) ---
    with tab2:
        # 計算變數
        day_count = len(itinerary)
        person_count = 2 if "情侶" in group else (4 if "親子" in group or "長輩" in group else 1)
        
        # 基準費用
        food_cost = 800 * day_count
        stay_cost = 0
        if day_count > 1:
            avg_room_price = 3000
            # 住宿夜數 = 天數 - 1
            nights = day_count - 1
            # 假設每2人一間房
            rooms = (person_count + 1) // 2
            total_stay = avg_room_price * nights * rooms
            stay_cost = total_stay / person_count # 人均住宿
            
        trans_cost = 500 if "大眾" in transport else (300 if "機車" in transport else 800) # 油錢或車票
        
        total_est = food_cost + stay_cost + trans_cost
        
        c1, c2, c3 = st.columns(3)
        c1.metric("餐飲預算(人)", f"${food_cost}")
        c2.metric("住宿預算(人)", f"${int(stay_cost)}")
        c3.metric("交通/雜支(人)", f"${trans_cost}")
        
        st.divider()
        st.subheader(f"💵 總預算預估：${int(total_est)} /人")
        st.info(f"計算基礎：{day_count}天行程，{person_count}人同行，{transport}。")

    # --- Tab 3: 交通與住宿 (邏輯修復) ---
    with tab3:
        st.subheader("🚗 交通策略")
        if "自行開車" in transport:
            st.warning("⚠️ **山路駕駛注意**：台7線北橫公路彎道多，櫻花季(2-3月)假日必塞車。建議早上 07:00 前通過大溪，或下午 16:00 後再下山。")
            st.info("🅿️ **停車資訊**：上巴陵停車位極少，恩愛農場等熱點需搭乘接駁車，請勿違停。")
        elif "大眾運輸" in transport:
            st.error("🚌 **公車族必看**：山區公車班次極少！錯過要等2小時。")
            st.markdown("""
            * **5090 (桃園-林班口)**：每日僅一班 06:50 發車。
            * **5091 (中壢-林班口)**：每日兩班 10:35 / 14:00 (通常僅能玩前山)。
            * **5104 (大溪-復興)**：班次較多，適合前山一日遊。
            * *建議：大眾運輸較適合定點二日遊，住宿處請民宿老闆協助接駁。*
            """)
        else:
            st.info("🏍️ **機車/單車**：請注意保暖與煞車檢查，山區午後易起霧。")

        st.divider()
        st.subheader("🛏️ 住宿推薦")
        
        # 根據行程的主要區域推薦住宿 (通常住 Day 1 下午所在的區域)
        stay_region = itinerary[1][1]['region'] if len(itinerary) > 0 else "後山"
        filtered_hotels = [h for h in hotels_db if h['region'] == stay_region]
        
        if not filtered_hotels: filtered_hotels = hotels_db[:4]
        
        st.caption(f"根據您的行程，第一晚建議住在 **{stay_region}** 地區：")
        
        cols = st.columns(2)
        for i, h in enumerate(filtered_hotels):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="hotel-card">
                    <div style="font-weight:bold;">{h['name']} <span style="font-size:12px; color:#666;">({h['price']}元起)</span></div>
                    <div style="font-size:12px; margin-top:5px;">🏷️ {h['tag']} | {h['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

    # --- Tab 4: 景點名錄 ---
    with tab4:
        st.write("目前收錄之完整景點資料庫：")
        st.dataframe(all_spots_db)

else:
    st.info("👆 請調整上方選項，我們將為您生成邏輯嚴謹的行程。")
