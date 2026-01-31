import streamlit as st
import random
from datetime import datetime

# ==========================================
# 1. 系統設定 (粉色櫻花主題)
# ==========================================
st.set_page_config(
    page_title="2026 復興區櫻花賞花指南",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學設計 (浪漫粉色系 + 玻璃擬態)
# ==========================================
st.markdown("""
    <style>
    /* 全站字體 */
    .stApp {
        background-color: #FFF0F5; /* 淺粉紅背景 */
        font-family: "Microsoft JhengHei", "Heiti TC", sans-serif;
    }

    /* 隱藏官方選單 */
    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 頂部 Header (漸層粉) */
    .header-box {
        background: linear-gradient(135deg, #FF69B4 0%, #FFB7C5 100%);
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
        margin-top: -60px; /* 滿版 */
    }
    .header-title { font-size: 28px; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.2); }
    .header-subtitle { font-size: 16px; margin-top: 5px; opacity: 0.95; }
    
    /* 卡片設計 (白色玻璃感) */
    .input-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #FFE4E1;
        margin-bottom: 20px;
    }
    
    /* 按鈕美化 */
    .stButton>button {
        width: 100%;
        background-color: #FF1493;
        color: white;
        border-radius: 50px;
        border: none;
        padding: 10px 0;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #C71585;
        transform: scale(1.02);
    }
    
    /* 行程時間軸樣式 */
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
    }
    .spot-title { font-weight: bold; color: #C71585; font-size: 18px; }
    .spot-desc { font-size: 14px; color: #555; }
    .spot-tag { 
        font-size: 12px; background: #FFE4E1; color: #D87093; 
        padding: 2px 8px; border-radius: 10px; margin-right: 5px;
    }
    
    /* 必吃美食區塊 */
    .food-card {
        background: white;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        border-bottom: 3px solid #FF69B4;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 頁面標題 (蘇佐璽區長形象)
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌸 2026 復興區櫻花秘境指南</div>
        <div class="header-subtitle">桃園市復興區長 <b>蘇佐璽</b> 邀您漫步粉紅山林</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. 輸入變數 (互動規劃)
# ==========================================
with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### 🗺️ 請告訴我您的賞花計畫")
    
    col1, col2 = st.columns(2)
    with col1:
        days = st.selectbox("📅 預計天數", ["一日遊 (當天來回)", "二日遊 (過夜慢活)", "三日遊 (深度部落)"])
        group = st.selectbox("👥 出遊夥伴", ["情侶約會", "親子家庭", "長輩樂齡", "熱血獨旅"])
    with col2:
        budget = st.select_slider("💰 預算等級 (每人)", options=["$500內 (小資)", "$1500 (舒適)", "$3000+ (豪華)"])
        transport = st.selectbox("🚗 交通方式", ["自行開車", "大眾運輸 (台灣好行/客運)", "機車漫遊"])

    # 進階需求
    interests = st.multiselect(
        "✨ 您希望行程包含 (幫您補強漏掉的體驗)",
        ["秘境探險", "原民美食", "溫泉泡湯", "天空步道", "DIY體驗", "網美拍照"],
        default=["秘境探險", "原民美食"]
    )
    
    generate_btn = st.button("🚀 AI 幫我生成專屬行程")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. 邏輯核心 (模擬 AI 規劃)
# ==========================================
def get_spots(group, days_type, user_interests):
    # 資料庫：復興區景點與秘境
    spots_db = {
        "must_visit": [
            {"name": "角板山行館", "tag": "梅花/櫻花", "desc": "北台灣賞梅首選，戰備隧道歷史巡禮。", "suitable": ["長輩樂齡", "親子家庭"]},
            {"name": "小烏來天空步道", "tag": "景觀", "desc": "透明玻璃步道，俯瞰瀑布震撼美景。", "suitable": ["所有"]},
            {"name": "拉拉山巨木區", "tag": "森林浴", "desc": "千年紅檜森林，芬多精吸好吸滿。", "suitable": ["所有"]}
        ],
        "sakura_spots": [
            {"name": "中巴陵櫻木花道", "tag": "🌸 昭和櫻秘境", "desc": "粉紅隧道，拍照最美的免費景點。", "type": "photo"},
            {"name": "恩愛農場", "tag": "🌸 千島櫻/富士櫻", "desc": "最熱門的賞櫻勝地，花況最密集(需門票)。", "type": "famous"},
            {"name": "爺亨梯田", "tag": "🌸 山櫻花/梯田", "desc": "昔日糧倉，層層疊疊的櫻花梯田美景。", "type": "secret"},
            {"name": "光華部落櫻花林", "tag": "🌸 隱藏版", "desc": "人煙稀少，真正的部落秘境。", "type": "secret"},
            {"name": "詩朗櫻花步道", "tag": "🌸 健行", "desc": "適合健行賞花，遠眺群山。", "type": "hike"}
        ],
        "food": [
            {"name": "馬告磚窯雞", "desc": "外皮酥脆，帶有檸檬香茅氣息的馬告香氣。"},
            {"name": "刺蔥蛋/炸溪蝦", "desc": "經典原民風味，下飯首選。"},
            {"name": "水蜜桃冰沙/拿鐵", "desc": "在地特產製作，甜蜜好滋味。"}
        ]
    }
    
    itinerary = []
    
    # 邏輯推演
    # Day 1 上午
    itinerary.append({"time": "09:00", "spot": spots_db["must_visit"][0]}) # 角板山起手式
    
    # Day 1 中午
    itinerary.append({"time": "12:00", "spot": {"name": "角板山商圈 / 原民風味餐", "tag": "美食", "desc": "品嚐香菇、山豬肉香腸。"}})
    
    # Day 1 下午 (根據群體選擇)
    if group == "情侶約會" or "網美拍照" in user_interests:
        itinerary.append({"time": "14:00", "spot": spots_db["sakura_spots"][0]}) # 中巴陵
        itinerary.append({"time": "16:00", "spot": spots_db["sakura_spots"][1]}) # 恩愛農場
    elif group == "親子家庭":
        itinerary.append({"time": "14:00", "spot": spots_db["must_visit"][1]}) # 小烏來
        itinerary.append({"time": "16:00", "spot": {"name": "羅浮溫泉公園", "tag": "泡腳", "desc": "免費泡腳池，舒緩走路疲勞。"}})
    elif "秘境探險" in user_interests:
        itinerary.append({"time": "14:00", "spot": spots_db["sakura_spots"][2]}) # 爺亨
        itinerary.append({"time": "16:00", "spot": {"name": "三龜戲水觀景台", "tag": "秘境", "desc": "遠眺大漢溪河谷的絕佳點位。"}})
    else:
        itinerary.append({"time": "14:30", "spot": spots_db["sakura_spots"][4]}) # 詩朗
        
    # 如果是二日遊，增加 Day 2
    day2_plan = []
    if "二日" in days_type or "三日" in days_type:
        day2_plan.append({"time": "08:00", "spot": {"name": "拉拉山巨木群步道", "tag": "芬多精", "desc": "早起空氣最好，漫步神木群。"}})
        day2_plan.append({"time": "12:00", "spot": {"name": "上巴陵景觀餐廳", "tag": "景觀午餐", "desc": "邊吃飯邊看雲海。"}})
        day2_plan.append({"time": "14:00", "spot": {"name": "比亞外/高義部落", "tag": "深度", "desc": "探訪藍腹鷴的故鄉，聆聽部落故事。"}})
        
    return itinerary, day2_plan

# ==========================================
# 6. 輸出結果 (Tab設計)
# ==========================================
if generate_btn:
    # 顯示載入動畫
    with st.spinner('🌸 蘇區長的小幫手正在幫您搜尋秘境...'):
        import time
        time.sleep(1.2)
    
    # 取得行程數據
    day1, day2 = get_spots(group, days, interests)
    
    st.markdown("### 🌸 您的專屬賞花提案")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🗓️ 行程規劃", "💰 經費預估", "🏨 住宿與交通", "💡 區長小叮嚀"])
    
    # --- Tab 1: 行程 ---
    with tab1:
        st.markdown(f"#### Day 1: {group}賞花之旅")
        for item in day1:
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">{item['time']} {item['spot']['name']}</div>
                <div>
                    <span class="spot-tag">{item['spot']['tag']}</span>
                </div>
                <div class="spot-desc">{item['spot']['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        if day2:
            st.markdown("---")
            st.markdown(f"#### Day 2: 森呼吸深度遊")
            for item in day2:
                st.markdown(f"""
                <div class="timeline-item">
                    <div class="spot-title">{item['time']} {item['spot']['name']}</div>
                    <div>
                        <span class="spot-tag">{item['spot']['tag']}</span>
                    </div>
                    <div class="spot-desc">{item['spot']['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

    # --- Tab 2: 經費 ---
    with tab2:
        st.markdown("#### 💰 預算估算表 (每人)")
        
        # 根據輸入計算
        base_food = 500 if "$500" in budget else (1000 if "$1500" in budget else 2000)
        transport_cost = 200 if transport == "自行開車" else (400 if "大眾" in transport else 150)
        ticket_cost = 300 # 預估門票 (恩愛農場/天空步道)
        accom_cost = 0
        if "二日" in days or "三日" in days:
            accom_cost = 1200 if "$1500" in budget else (2500 if "$3000" in budget else 800)
            
        total = base_food + transport_cost + ticket_cost + accom_cost
        
        c1, c2, c3 = st.columns(3)
        c1.metric("餐飲費", f"${base_food}")
        c2.metric("交通/門票", f"${transport_cost + ticket_cost}")
        c3.metric("住宿預留", f"${accom_cost}")
        
        st.success(f"📊 **預估總花費：約 ${total} / 人**")
        st.caption("※ 此為粗估，實際費用視當下消費而定。")

    # --- Tab 3: 住宿交通 ---
    with tab3:
        st.subheader("🚗 交通資訊")
        if transport == "大眾運輸 (台灣好行/客運)":
            st.info("""
            **🚌 台灣好行 502 (小烏來線)**：
            - 假日行駛，從桃園客運總站發車。
            
            **🚌 桃園客運 5090/5091 (往拉拉山)**：
            - 班次較少，建議先從大溪總站搭乘。
            - **賞櫻專車**：櫻花季期間通常會有接駁車，請關注「復興區公所」粉專公告。
            """)
        else:
            st.warning("""
            **🚗 自行開車提醒**：
            - 櫻花季期間，北橫公路 (台7線) 及 拉拉山林道 易塞車。
            - 建議 **早上 7:00 前** 抵達角板山或通過管制點。
            - 山路蜿蜒，請小心駕駛。
            """)
            
        st.markdown("---")
        st.subheader("🛏️ 住宿建議")
        st.markdown("""
        * **拉拉山民宿區**：適合想看日出、雲海的遊客 (上巴陵)。
        * **霞雲/羅浮露營區**：適合親子體驗大自然。
        * **角板山周邊**：生活機能較好，交通便利。
        """)

    # --- Tab 4: 隱藏彩蛋 (區長叮嚀) ---
    with tab4:
        st.markdown("### 💡 您可能漏掉的細節")
        
        st.markdown("""
        **1. 🍖 在地美食清單 (必吃)**
        - **馬告香腸**：路邊攤就有，香氣特殊。
        - **炸香菇**：復興區是香菇產地，新鮮多汁。
        - **水蜜桃冰沙**：雖然還沒到產季，但店家通常有釀製的果醬或冰沙。
        
        **2. 🧥 穿搭攻略**
        - 山上比平地溫低 5-8 度。
        - **洋蔥式穿法**：裡面短袖/薄長袖，外面一定要帶防風外套。
        - **好走的鞋**：賞櫻步道多為斜坡，請勿穿高跟鞋。
        
        **3. 🎁 必買伴手禮**
        - 段木香菇 (乾貨)
        - 馬告辣椒醬
        - 季節限定：綠竹筍 (依季節)
        
        **4. 📸 拍照技巧**
        - 櫻花要在「順光」時拍才粉嫩，建議上午拍東邊景點，下午拍西邊。
        """)
        
        st.image("https://images.unsplash.com/photo-1522383225653-ed111181a951?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80", caption="期待與您在復興區相遇！", use_container_width=True)

else:
    # 尚未按下按鈕時的預設畫面
    st.info("👆 請在上方選擇您的需求，區長將為您規劃專屬賞花行程！")
    
    # 隨機展示一個秘境激發興趣
    st.markdown("---")
    st.markdown("#### 🌸 秘境搶先看：爺亨梯田")
    st.markdown("除了拉拉山，**爺亨梯田**是日治時期留下的壯觀水利工程，春天時梯田邊開滿山櫻花，搭配層層疊疊的地景，是攝影師的最愛！")
