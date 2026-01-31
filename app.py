import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定
# ==========================================
st.set_page_config(
    page_title="2026 復興區全境賞櫻制霸地圖 (含住宿連動)",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (細節優化版)
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF0F5;
        font-family: "Microsoft JhengHei", sans-serif;
    }
    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 頂部標題 */
    .header-box {
        background: linear-gradient(135deg, #FF69B4 0%, #DB7093 100%);
        padding: 30px 20px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(219, 112, 147, 0.4);
        border-radius: 0 0 20px 20px;
        margin-top: -60px;
    }
    
    /* 通用卡片 */
    .card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #FFE4E1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    
    /* 住宿專用卡片 */
    .hotel-card {
        border-left: 5px solid #9370DB; /* 紫色代表住宿 */
        background: #F8F8FF;
    }
    .hotel-tag {
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 10px;
        color: white;
        background-color: #9370DB;
        margin-right: 5px;
    }
    
    /* 連結線 (Connectivity Visual) */
    .connect-line {
        border-left: 2px dashed #aaa;
        margin-left: 20px;
        padding-left: 20px;
        padding-bottom: 20px;
        color: #666;
        font-size: 13px;
    }
    
    /* 標籤樣式 */
    .tag { font-size: 11px; padding: 2px 6px; border-radius: 4px; color: white; margin-right: 4px; }
    .tag-front { background: #2E8B57; }
    .tag-back { background: #C71585; }
    .tag-tribe { background: #D2691E; }
    
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 雙重資料庫 (景點 + 住宿)
# ==========================================

# A. 景點資料庫 (精簡版，保留核心)
spots_db = [
    # 前山
    {"name": "角板山行館", "region": "前山", "month": [1, 2], "type": "梅花/山櫻", "desc": "適合全家散步的起點。"},
    {"name": "小烏來天空步道", "region": "前山", "month": [1, 2], "type": "景觀", "desc": "透明步道俯瞰瀑布。"},
    {"name": "羅浮溫泉", "region": "前山", "month": [1, 2], "type": "泡湯", "desc": "暖身足湯與大眾池。"},
    {"name": "翠墨莊園", "region": "前山", "month": [1, 2], "type": "緋寒櫻", "desc": "精緻日式庭園(需預約)。"},
    # 部落
    {"name": "爺亨梯田", "region": "部落", "month": [1, 2, 3], "type": "山櫻", "desc": "絕美梯田粉紅花海。"},
    {"name": "比亞外部落", "region": "部落", "month": [1, 2], "type": "昭和櫻", "desc": "藍腹鷴生態秘境。"},
    # 後山
    {"name": "恩愛農場", "region": "後山", "month": [2, 3], "type": "千島櫻", "desc": "粉紅爆炸花海(必去)。"},
    {"name": "拉拉山巨木區", "region": "後山", "month": [1, 2, 3], "type": "神木", "desc": "千年紅檜森林浴。"},
    {"name": "中巴陵櫻木花道", "region": "後山", "month": [2], "type": "昭和櫻", "desc": "免費拍照隧道。"},
    {"name": "光明農場", "region": "後山", "month": [3], "type": "霧社櫻", "desc": "稀有白櫻與馬告雞。"}
]

# B. 住宿資料庫 (詳細分類與標籤)
# 邏輯：region 對應景點區域，level 對應預算 (1=平價, 2=舒適, 3=豪華)
hotels_db = [
    # 前山住宿 (適合不想開太遠山路的人)
    {"name": "復興青年活動中心", "region": "前山", "level": 1, "tags": ["高CP值", "湖景", "好停車"], "desc": "位於角板山公園內，最方便的選擇。"},
    {"name": "普拉多山丘假期", "region": "前山", "level": 3, "tags": ["歐式鄉村", "下午茶", "網美"], "desc": "三民地區的黃色歐風建築，房間精緻。"},
    {"name": "小烏來山莊", "region": "前山", "level": 2, "tags": ["近天空步道", "景觀"], "desc": "走路就能到小烏來瀑布。"},
    {"name": "羅浮天空溫泉飯店", "region": "前山", "level": 3, "tags": ["溫泉", "新開幕"], "desc": "房內即可泡湯，設施新穎。"},
    
    # 部落/中途 (適合深度遊)
    {"name": "爺亨溫泉夢幻露營", "region": "部落", "level": 2, "tags": ["露營", "溫泉", "星空"], "desc": "可以直接住在櫻花樹下的豪華露營。"},
    {"name": "河那灣民宿", "region": "部落", "level": 1, "tags": ["原民風", "溪流"], "desc": "位於羅浮橋畔，親近大自然的木屋。"},

    # 後山住宿 (適合看日出、第二天去恩愛農場)
    {"name": "恩愛農場小木屋", "region": "後山", "level": 2, "tags": ["花海第一排", "極難訂"], "desc": "出門就是櫻花，但需半年前預訂。"},
    {"name": "拉拉山 5.5K 農莊", "region": "後山", "level": 2, "tags": ["景觀", "烤肉"], "desc": "視野開闊，適合家庭聚會。"},
    {"name": "雲山仙境民宿", "region": "後山", "level": 3, "tags": ["雲海", "豪華早餐", "電梯"], "desc": "上巴陵評價極高的景觀民宿。"},
    {"name": "觀雲休憩農莊", "region": "後山", "level": 1, "tags": ["平價", "賞花"], "desc": "就在恩愛農場旁邊，CP值超高。"},
    {"name": "富仙境渡假旅館", "region": "後山", "level": 2, "tags": ["便利", "景觀"], "desc": "位於上巴陵鬧區，吃飯補給最方便。"},
    {"name": "谷點咖啡民宿", "region": "後山", "level": 3, "tags": ["無敵山景", "美食"], "desc": "擁有絕佳的下巴陵峽谷視野。"}
]

# ==========================================
# 4. 智慧連動引擎 (Connectivity Engine)
# ==========================================
def plan_itinerary(travel_date, days, budget_level, group):
    m = travel_date.month
    
    # 1. 決定 [主要景點] (根據花期)
    main_spot = next((s for s in spots_db if "恩愛" in s['name']), spots_db[-1]) # 預設恩愛
    if m == 1: main_spot = next((s for s in spots_db if "角板山" in s['name']), spots_db[0])
    
    # 2. 決定 [住宿策略] (Connectivity Logic)
    # 邏輯：如果去恩愛農場(後山)，強烈建議住後山，除非是一日遊
    stay_region = "前山" # 預設
    reason = "行程輕鬆，住前山選擇多。"
    
    if main_spot['region'] == "後山" and "一日" not in days:
        stay_region = "後山"
        reason = "💡 策略建議：因為第二天要衝恩愛農場/巨木區，強烈建議**前一晚住上巴陵(後山)**，免去早起塞車之苦！"
    elif "溫泉" in group: # 假設有溫泉需求
        stay_region = "前山" # 羅浮/爺亨
        reason = "💡 策略建議：為了享受溫泉，安排住在羅浮或爺亨周邊。"

    # 3. 篩選 [推薦住宿] (根據預算與區域)
    # 預算 mapping: 小資=1, 舒適=2, 豪華=3
    b_lvl = 1
    if "舒適" in budget_level: b_lvl = 2
    if "豪華" in budget_level: b_lvl = 3
    
    recommended_hotels = [
        h for h in hotels_db 
        if h['region'] == stay_region and abs(h['level'] - b_lvl) <= 1 # 允許彈性一級
    ]
    # 如果篩選後沒房間，就放寬區域
    if not recommended_hotels:
        recommended_hotels = [h for h in hotels_db if h['region'] == stay_region]

    return main_spot, stay_region, reason, recommended_hotels

# ==========================================
# 5. UI 呈現
# ==========================================
st.markdown("""
    <div class="header-box">
        <div style="font-size: 26px; font-weight: bold;">🌸 2026 復興區賞櫻・全連動智慧導遊</div>
        <div style="font-size: 15px; margin-top: 5px;">桃園市復興區長 <b>蘇佐璽</b> 幫您搞定「住」與「玩」的完美銜接 ❤️</div>
    </div>
""", unsafe_allow_html=True)

# 輸入區
with st.container():
    st.markdown("### 📝 行程設定")
    c1, c2 = st.columns(2)
    with c1:
        travel_date = st.date_input("出發日期", value=date(2026, 2, 20), min_value=date(2026, 1, 1), max_value=date(2026, 4, 30))
        days = st.selectbox("天數", ["二日遊 (標準)", "三日遊 (慢活)", "一日遊 (熱血)"])
    with c2:
        budget = st.select_slider("預算/住宿等級", options=["小資省錢", "舒適標準", "豪華享受"])
        group = st.selectbox("類型", ["情侶", "親子", "長輩", "攝影團"])
    
    btn = st.button("🚀 啟動連動規劃")

# 輸出區
if btn:
    main_spot, stay_region, stay_reason, hotels = plan_itinerary(travel_date, days, budget, group)
    
    st.markdown("---")
    
    # Tab 分類
    t1, t2, t3 = st.tabs(["🗺️ 完整行程表", "🛏️ 推薦住宿 (已連動)", "💰 預算詳情"])
    
    # --- Tab 1: 連動行程表 ---
    with t1:
        st.subheader(f"✨ {days} 完美銜接計畫")
        
        # Day 1
        st.markdown(f"#### Day 1：{main_spot['month'][0]}月花季序曲")
        
        # 景點 1
        spot1_name = "角板山行館"
        st.markdown(f"""
        <div class="card">
            <span class="tag tag-front">前山</span> <b>09:30 {spot1_name}</b><br>
            <span style="color:#666; font-size:13px;">北橫旅遊第一站，先在梅園/戰備隧道暖身。</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 連接線 (Connect Line)
        st.markdown(f"""<div class="connect-line">🚗 開車約 40 分鐘前往部落區午餐</div>""", unsafe_allow_html=True)
        
        # 景點 2 (午餐)
        st.markdown(f"""
        <div class="card">
            <span class="tag tag-tribe">部落</span> <b>12:30 在地風味餐</b><br>
            <span style="color:#666; font-size:13px;">推薦：炸香菇、馬告山豬肉。</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 連接線
        drive_time = "1 小時直奔後山" if stay_region == "後山" else "10 分鐘至羅浮"
        st.markdown(f"""<div class="connect-line">🚗 吃飽後移動 ({drive_time})</div>""", unsafe_allow_html=True)

        # 住宿點 (Day 1 End)
        st.markdown(f"#### 🌙 住宿落腳點：{stay_region}")
        st.info(stay_reason)
        
        # 顯示 2-3 個推薦住宿在行程表中
        cols = st.columns(2)
        for i, h in enumerate(hotels[:2]):
            with cols[i]:
                st.markdown(f"""
                <div class="card hotel-card">
                    <b>{h['name']}</b> <br>
                    <span style="font-size:12px; color:#555;">{h['desc']}</span>
                </div>
                """, unsafe_allow_html=True)

        # Day 2 (如果有的話)
        if "一日" not in days:
            st.markdown(f"#### Day 2：{main_spot['type']}大爆發")
            
            # 連接線 (起床)
            st.markdown(f"""<div class="connect-line">☀️ 早安！從{stay_region}出發</div>""", unsafe_allow_html=True)
            
            target_spot = main_spot['name']
            st.markdown(f"""
            <div class="card">
                <span class="tag tag-back">重點</span> <b>08:30 {target_spot}</b><br>
                <span style="color:#C71585; font-weight:bold;">🌸 本次行程最高潮！</span><br>
                <span style="color:#666; font-size:13px;">住在附近就是為了這一刻，避開人潮獨享花海。</span>
            </div>
            """, unsafe_allow_html=True)

    # --- Tab 2: 詳細住宿清單 ---
    with t2:
        st.markdown(f"### 🛏️ 精選 {stay_region} 住宿")
        st.caption(f"根據您的預算【{budget}】與行程動線篩選：")
        
        for h in hotels:
            tags_html = "".join([f'<span class="hotel-tag">{t}</span>' for t in h['tags']])
            price_icon = "💲" * h['level']
            
            st.markdown(f"""
            <div class="card hotel-card">
                <div style="display:flex; justify-content:space-between;">
                    <div style="font-size:18px; font-weight:bold;">{h['name']}</div>
                    <div style="color:#666;">{price_icon}</div>
                </div>
                <div style="margin: 5px 0;">{tags_html}</div>
                <div style="font-size:14px; color:#444;">{h['desc']}</div>
                <div style="margin-top:8px; font-size:12px; color:#888;">
                    💡 為什麼推薦：位於{h['region']}核心，符合您的行程動線。
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    # --- Tab 3: 預算 ---
    with t3:
        price_base = 1500 if "小資" in budget else (3000 if "舒適" in budget else 6000)
        st.metric("預估總花費 (含住宿)", f"${price_base} /人")
        st.warning("櫻花季 (2月) 住宿強烈建議提前 3-6 個月預訂！")
