import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定
# ==========================================
st.set_page_config(
    page_title="2026 復興區花季行程規劃 (邏輯修復版)",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (保留 iPhone 黑字修正)
# ==========================================
st.markdown("""
    <style>
    /* 強制全站字體顏色為深色 (修正 iPhone 深色模式問題) */
    .stApp {
        background-color: #FFF0F5;
        font-family: "Microsoft JhengHei", sans-serif;
        color: #333333 !important;
    }
    
    p, div, span, h1, h2, h3, h4, h5, h6, label, .stMarkdown, .stSelectbox div, .stDateInput input {
        color: #333333 !important;
    }

    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 標題區 (維持白字) */
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
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 資料庫 (已整合您指定的6大名所)
# ==========================================
all_spots_db = [
    # --- 您指定的 6 個重點賞櫻區 (權重調高) ---
    {"name": "翠墨莊園", "region": "前山", "month": [1, 2], "type": "賞花", "flower": "緋寒櫻", "desc": "三民里大窩部落，精緻日式造景 (需預約)。"},
    {"name": "詩朗櫻花坡", "region": "前山", "month": [1, 2], "type": "賞花", "flower": "八重櫻/昭和櫻", "desc": "澤仁里詩朗部落，整片粉紅山坡秘境。"},
    {"name": "詩朗部落祕境", "region": "前山", "month": [1, 2], "type": "健行", "flower": "枝垂櫻", "desc": "澤仁里詩朗部落深處，幽靜步道。"},
    {"name": "中巴陵櫻木花道", "region": "後山", "month": [2], "type": "賞花", "flower": "昭和櫻", "desc": "華陵里中巴陵，免費粉紅隧道必拍。"},
    {"name": "青鬆園", "region": "後山", "month": [2, 3], "type": "賞花", "flower": "墨染櫻", "desc": "華陵里上巴陵比該路段，賞花新秘境。"},
    {"name": "恩愛農場", "region": "後山", "month": [2, 3], "type": "賞花", "flower": "千島/富士櫻", "desc": "華陵里上巴陵中心路頂端，全台最知名。"},

    # --- 其他經典景點 ---
    {"name": "角板山行館", "region": "前山", "month": [1, 2], "type": "賞花", "flower": "梅花/山櫻", "desc": "北橫賞花起點，戰備隧道。"},
    {"name": "羅馬公路", "region": "前山", "month": [1, 2], "type": "兜風", "flower": "山櫻花", "desc": "最美兜風路線。"},
    {"name": "東眼山櫻花大道", "region": "前山", "month": [1, 2], "type": "健行", "flower": "山櫻花", "desc": "林道兩旁紅色隧道。"},
    {"name": "小烏來風景區", "region": "前山", "month": [1, 2], "type": "景觀", "flower": "山櫻花", "desc": "天空步道與瀑布。"},
    {"name": "悠然秘境小屋", "region": "前山", "month": [2, 3], "type": "賞花", "flower": "吉野櫻", "desc": "三民隱藏版私人園區。"},
    
    {"name": "爺亨梯田", "region": "部落", "month": [1, 2, 3], "type": "景觀", "flower": "山櫻/桃花", "desc": "梯田地景配粉色花海。"},
    {"name": "比亞外部落", "region": "部落", "month": [1, 2], "type": "生態", "flower": "昭和櫻", "desc": "藍腹鷴的故鄉。"},
    {"name": "光華櫻花故事林道", "region": "部落", "month": [2, 3], "type": "秘境", "flower": "昭和櫻", "desc": "光華國小旁浪漫林道。"},
    
    {"name": "拉拉山遊客中心", "region": "後山", "month": [2, 3], "type": "賞花", "flower": "千島櫻", "desc": "停車場就是絕美景點。"},
    {"name": "觀雲休憩農莊", "region": "後山", "month": [2, 3], "type": "賞花", "flower": "昭和櫻", "desc": "恩愛農場旁免門票秘境。"},
    {"name": "光明農場", "region": "後山", "month": [3], "type": "美食", "flower": "霧社櫻", "desc": "稀有白櫻配馬告雞。"},
    {"name": "拉拉山巨木區", "region": "後山", "month": [1, 2, 3, 4], "type": "健行", "flower": "神木", "desc": "千年紅檜群深呼吸。"}
]

hotels_db = [
    {"name": "復興青年活動中心", "region": "前山", "tag": "高CP值", "price": 2000, "desc": "角板山公園內，最方便。"},
    {"name": "普拉多山丘假期", "region": "前山", "tag": "歐式鄉村", "price": 3800, "desc": "三民地區黃色歐風建築。"},
    {"name": "羅浮天空溫泉飯店", "region": "前山", "tag": "溫泉", "price": 4500, "desc": "房內泡湯，設施新穎。"},
    {"name": "爺亨溫泉夢幻露營", "region": "部落", "tag": "露營", "price": 3500, "desc": "櫻花樹下的豪華露營。"},
    {"name": "恩愛農場小木屋", "region": "後山", "tag": "花海", "price": 5000, "desc": "出門就是櫻花(極難訂)。"},
    {"name": "雲山仙境民宿", "region": "後山", "tag": "雲海", "price": 4200, "desc": "上巴陵高評價景觀民宿。"},
    {"name": "谷點咖啡民宿", "region": "後山", "tag": "景觀", "price": 3800, "desc": "無敵山景視野。"},
    {"name": "富仙境渡假旅館", "region": "後山", "tag": "便利", "price": 2500, "desc": "上巴陵鬧區，吃飯方便。"}
]

# ==========================================
# 4. 邏輯核心：動態行程生成演算法 (修復版)
# ==========================================
def generate_itinerary(travel_date, days_str, group):
    m = travel_date.month
    
    # 1. 篩選「當月」有花的景點
    available = [s for s in all_spots_db if m in s['month']]
    
    # 防呆：若該月沒花，塞入常態景點
    if not available:
        available = [s for s in all_spots_db if s['flower'] in ["神木", "景觀"]]

    # 2. 分區清單
    front_spots = [s for s in available if s['region'] == "前山"]
    tribe_spots = [s for s in available if s['region'] == "部落"]
    back_spots = [s for s in available if s['region'] == "後山"]
    
    itinerary = {}
    
    # --- Day 1 邏輯：前山出發，慢慢往內走 ---
    # 優先推薦您指定的「前山」新景點
    d1_candidates = [s for s in front_spots if s['name'] in ["翠墨莊園 (翠墨山莊)", "詩朗櫻花坡"]]
    if not d1_candidates: d1_candidates = front_spots # 若沒對應到，用所有前山
    
    # 上午：前山重點
    d1_s1 = d1_candidates[0] if d1_candidates else available[0]
    
    # 下午：往部落或後山移動 (或繼續前山)
    d1_s2 = next((s for s in tribe_spots), None)
    if not d1_s2: d1_s2 = next((s for s in front_spots if s != d1_s1), available[-1])
    
    itinerary[1] = [d1_s1, d1_s2]
    
    # --- Day 2 邏輯 (若有)：直攻後山精華 ---
    if "二日" in days_str or "三日" in days_str:
        # 優先推薦您指定的「後山」新景點
        d2_candidates = [s for s in back_spots if s['name'] in ["恩愛農場", "中巴陵櫻木花道", "青鬆園"]]
        if not d2_candidates: d2_candidates = back_spots
        
        # 上午：後山大景
        d2_s1 = d2_candidates[0] if d2_candidates else available[0]
        
        # 下午：神木或其他後山點
        d2_s2 = next((s for s in back_spots if s['flower'] == "神木"), None)
        if not d2_s2: d2_s2 = next((s for s in back_spots if s != d2_s1), available[0])
        
        itinerary[2] = [d2_s1, d2_s2]

    # --- Day 3 邏輯 (若有)：回程補漏 ---
    if "三日" in days_str:
        d3_s1 = next((s for s in front_spots if s['name'] not in [d1_s1['name'], d1_s2['name']]), None)
        if not d3_s1: d3_s1 = {"name": "新溪口吊橋", "region": "前山", "flower": "景觀", "desc": "全台最長懸索橋。"}
        
        d3_s2 = {"name": "大溪老街", "region": "前山", "flower": "採買", "desc": "回程購買伴手禮。"}
        itinerary[3] = [d3_s1, d3_s2]

    # 花況標題
    titles = {1: "❄️ 1月：寒梅與早春山櫻", 2: "🌸 2月：粉紅櫻花大爆發", 3: "🍑 3月：桃花與吉野櫻尾聲", 4: "🌲 4月：螢火蟲與神木季"}
    status = titles.get(m, "🌲 四季山林森呼吸")
    
    return status, itinerary

# ==========================================
# 5. UI 呈現
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌸 2026 復興區花季攻略</div>
        <div class="header-subtitle">桃園市復興區長 <b>蘇佐璽</b> 邀請您 ❤️</div>
    </div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        travel_date = st.date_input("預計出發日期", value=date(2026, 2, 20), min_value=date(2026, 1, 1), max_value=date(2026, 4, 30))
        days = st.selectbox("行程天數", ["一日遊", "二日遊", "三日遊"])
    with col2:
        group = st.selectbox("出遊夥伴", ["情侶/夫妻", "親子家庭", "長輩樂齡", "攝影團"])
        transport = st.selectbox("交通方式", ["自行開車", "大眾運輸", "機車"])
    
    btn = st.button("🚀 開始規劃行程")
    st.markdown('</div>', unsafe_allow_html=True)

if btn:
    status_title, itinerary = generate_itinerary(travel_date, days, group)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="weather-tag">{status_title}</div>
        <div style="color:#555 !important;">根據您的日期 <b>{travel_date.month}/{travel_date.day}</b>，我們為您挑選了花況最佳的景點。</div>
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["🗓️ 詳細行程", "💰 經費概算", "🚗 交通住宿", "🌸 景點名錄"])

    # --- Tab 1: 行程 ---
    with t1:
        for day, spots in itinerary.items():
            st.markdown(f"#### Day {day}")
            # 上午
            s1 = spots[0]
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">09:30 {s1['name']} <span class="spot-tag">{s1['region']}</span></div>
                <div class="spot-desc">{s1['desc']} ({s1['flower']})</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 午餐
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">12:30 在地風味午餐</div>
                <div class="spot-desc">品嚐馬告磚窯雞或山產料理。</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 下午
            s2 = spots[1]
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">14:30 {s2['name']} <span class="spot-tag">{s2['region']}</span></div>
                <div class="spot-desc">{s2['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if day < len(itinerary):
                st.markdown(f"""
                <div class="timeline-item" style="border-color:#9370DB;">
                    <div class="spot-title" style="color:#9370DB !important;">18:00 入住民宿 (詳見住宿頁籤)</div>
                </div>
                """, unsafe_allow_html=True)

    # --- Tab 2: 經費 ---
    with t2:
        day_num = len(itinerary)
        base_cost = 1000 * day_num
        if day_num > 1: base_cost += 2500 * (day_num - 1) # 住宿費
        st.metric("預估總花費 (每人)", f"${base_cost} 起", "含食宿交通")
        st.caption("※ 櫻花季期間 (2月) 民宿房價可能會有浮動。")

    # --- Tab 3: 交通住宿 ---
    with t3:
        st.subheader("🚗 交通方式")
        st.info("🚗 **自行開車**：櫻花季北橫易塞車，建議 07:00 前抵達大溪。")
        st.info("🚌 **大眾運輸**：可於大溪總站搭乘 5090 / 5091 客運前往拉拉山。")
        
        st.markdown("---")
        st.subheader("🛏️ 推薦住宿")
        
        # 根據行程區域推薦
        target_region = itinerary[1][1]['region'] if len(itinerary) > 0 else "前山"
        rec_hotels = [h for h in hotels_db if h['region'] == target_region]
        if not rec_hotels: rec_hotels = hotels_db[:4]
        
        cols = st.columns(2)
        for i, h in enumerate(rec_hotels):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="hotel-card">
                    <div style="font-weight:bold;">{h['name']} <span style="font-size:12px;">(${h['price']})</span></div>
                    <div style="font-size:12px; margin-top:5px;">🏷️ {h['tag']}</div>
                    <div style="font-size:12px; color:#555 !important;">{h['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

    # --- Tab 4: 景點名錄 ---
    with t4:
        st.markdown("### 🌸 完整景點資料庫")
        search = st.text_input("🔍 搜尋景點", placeholder="輸入關鍵字...")
        
        filtered = all_spots_db
        if search:
            filtered = [s for s in all_spots_db if search in s['name'] or search in s['desc']]
            
        for s in filtered:
            st.markdown(f"""
            <div class="mini-card" style="margin-bottom:10px;">
                <b>{s['name']}</b> <span style="font-size:12px; color:#C71585 !important;">{s['flower']}</span><br>
                <span style="font-size:12px; color:#666 !important;">📍 {s['region']} | {s['desc']}</span>
            </div>
            """, unsafe_allow_html=True)

else:
    st.info("👆 請調整上方日期與人數，按下按鈕生成行程！")
