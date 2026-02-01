import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定
# ==========================================
st.set_page_config(
    page_title="2026 復興區花季行程規劃",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (維持浪漫粉色 + 玻璃質感)
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
    .header-subtitle { font-size: 16px; margin-top: 5px; opacity: 0.95; }
    
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
    
    /* 資訊看板樣式 */
    .info-box {
        background-color: #fffbea;
        border-left: 5px solid #FFD700;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .weather-tag {
        font-weight: bold;
        color: #e67e22;
        font-size: 18px;
    }
    
    /* 時間軸樣式 */
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
    .spot-title { font-weight: bold; color: #C71585; font-size: 18px; }
    .spot-desc { font-size: 14px; color: #555; }
    .spot-tag { 
        font-size: 12px; background: #FFE4E1; color: #D87093; 
        padding: 2px 8px; border-radius: 10px; margin-right: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 邏輯核心：花況與天氣判斷
# ==========================================
def analyze_date(travel_date):
    month = travel_date.month
    day = travel_date.day
    
    # 1. 花況判斷 (Based on Fuxing District History)
    flower_status = ""
    main_flower = ""
    recommend_spot = ""
    
    if month == 1:
        main_flower = "❄️ 梅花 (White Plum)"
        flower_status = "角板山梅花季盛開中，空氣中有淡淡清香。"
        recommend_spot = "角板山行館"
    elif month == 2 and day <= 10:
        main_flower = "🌺 山櫻花 (Taiwan Cherry)"
        flower_status = "緋紅色的山櫻花開始綻放，像掛滿紅色鈴鐺。"
        recommend_spot = "羅浮橋 / 北橫沿線"
    elif month == 2 and day > 10:
        main_flower = "🌸 昭和櫻/千島櫻 (Pink Cherry)"
        flower_status = "最夢幻的粉紅風暴！恩愛農場進入最佳觀賞期。"
        recommend_spot = "恩愛農場 / 中巴陵"
    elif month == 3:
        main_flower = "🍑 吉野櫻 & 桃花 (Yoshino & Peach)"
        flower_status = "櫻花季尾聲，接力登場的是嬌豔的桃花與吉野櫻。"
        recommend_spot = "上巴陵 / 拉拉山"
    else:
        main_flower = "🌲 翠綠山林 (Green Forest)"
        flower_status = "非主要賞花季，但山林翠綠，適合避暑與森林浴。"
        recommend_spot = "小烏來 / 東眼山"

    # 2. 氣溫預估 (山上溫度通常比平地低 5-8 度)
    temp_desc = ""
    if month in [12, 1, 2]:
        temp_desc = "🥶 寒冷 (5°C - 12°C)，絕對需要羽絨衣與毛帽。"
    elif month in [3, 4]:
        temp_desc = "🌬️ 微涼 (10°C - 18°C)，洋蔥式穿搭，早晚溫差大。"
    else:
        temp_desc = "☀️ 舒適 (18°C - 26°C)，適合輕便服裝，但需帶薄外套。"
        
    return main_flower, flower_status, recommend_spot, temp_desc

# ==========================================
# 4. 頁面內容
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌸 2026 復興區花季行程規劃</div>
        <div class="header-subtitle">桃園市復興區長 <b>蘇佐璽</b> 幫您算準花期，不撲空 ❤️</div>
    </div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### 📅 第一步：選擇出發日期")
    st.caption("氣候與花況息息相關，區長會根據日期幫您客製化行程！")
    
    # 日期選擇器
    travel_date = st.date_input("預計出發日期", value=date(2026, 2, 20), min_value=date(2026, 1, 1), max_value=date(2026, 4, 30))
    
    st.markdown("---")
    st.markdown("### 🗺️ 第二步：行程偏好")
    
    col1, col2 = st.columns(2)
    with col1:
        days = st.selectbox("行程天數", ["一日遊 (當天來回)", "二日遊 (住一晚)", "三日遊 (深度慢活)"])
        group = st.selectbox("出遊夥伴", ["情侶/夫妻", "親子家庭", "長輩樂齡", "攝影愛好者"])
    with col2:
        budget = st.select_slider("預算等級", options=["小資遊", "舒適遊", "豪華遊"])
        transport = st.selectbox("交通方式", ["自行開車", "搭乘公車/接駁車", "機車"])

    interests = st.multiselect("額外興趣", ["部落美食", "秘境探險", "溫泉泡湯", "農事體驗"], default=["部落美食"])
    
    generate_btn = st.button("🚀 開始規劃賞花行程")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. 生成結果
# ==========================================
if generate_btn:
    # 執行日期分析
    main_flower, flower_status, best_spot, weather_info = analyze_date(travel_date)
    
    # 顯示載入動畫
    with st.spinner(f'正在分析 {travel_date.strftime("%m/%d")} 的天氣與花況...'):
        import time
        time.sleep(1)

    # === 重點資訊看板 (日期連動結果) ===
    st.markdown(f"""
    <div class="info-box">
        <div style="font-size: 20px; font-weight: bold; color: #C71585; margin-bottom: 10px;">
            🌸 {travel_date.month}月{travel_date.day}日 花況情報
        </div>
        <div><b>主力花種：</b> {main_flower}</div>
        <div><b>花況預測：</b> {flower_status}</div>
        <div style="margin-top: 10px; border-top: 1px dashed #ccc; padding-top: 10px;">
            <span class="weather-tag">🌡️ 氣候預報</span><br>
            {weather_info}
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🗓️ 專屬行程", "💰 經費概算", "🚗 交通住宿"])

    # --- Tab 1: 行程 (根據花況動態調整) ---
    with tab1:
        st.subheader(f"🌸 {days} 賞花路線")
        
        # Day 1 上午：必定是當季最推薦的點
        st.markdown(f"""
        <div class="timeline-item">
            <div class="spot-title">09:30 {best_spot} (當季首選)</div>
            <div><span class="spot-tag">必訪花點</span><span class="spot-tag">拍照</span></div>
            <div class="spot-desc">根據您的日期，這裡是目前花況最棒的地方！建議早點抵達避開人潮。</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Day 1 中午
        food = "馬告磚窯雞" if "豪華" in budget else "原民竹筒飯套餐"
        st.markdown(f"""
        <div class="timeline-item">
            <div class="spot-title">12:30 在地風味午餐</div>
            <div><span class="spot-tag">美食</span><span class="spot-tag">{food}</span></div>
            <div class="spot-desc">品嚐復興區招牌料理，補充體力。</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Day 1 下午 (根據夥伴與日期調整)
        pm_spot = "小烏來天空步道" # Default
        pm_desc = "走在透明玻璃上，俯瞰瀑布美景。"
        
        if "長輩" in group:
            pm_spot = "羅浮溫泉公園"
            pm_desc = "免費泡腳池，溫暖長輩的雙腳，促進血液循環。"
        elif "親子" in group:
            pm_spot = "角板山戰備隧道"
            pm_desc = "帶孩子探險神秘隧道，順便在草地上野餐跑跳。"
        elif travel_date.month == 2 and "情侶" in group:
            pm_spot = "中巴陵櫻木花道"
            pm_desc = "粉紅色的櫻花隧道，最適合情侶牽手散步拍照。"
            
        st.markdown(f"""
        <div class="timeline-item">
            <div class="spot-title">14:30 {pm_spot}</div>
            <div><span class="spot-tag">午後時光</span></div>
            <div class="spot-desc">{pm_desc}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Day 2 (如果有選)
        if "二日" in days or "三日" in days:
            st.markdown("---")
            st.markdown("#### Day 2: 深入部落深呼吸")
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">08:00 拉拉山巨木區</div>
                <div class="spot-desc">早晨空氣最好，欣賞千年神木的壯麗。</div>
            </div>
            <div class="timeline-item">
                <div class="spot-title">11:00 爺亨梯田 / 幽靈瀑布</div>
                <div class="spot-desc">探訪更深處的秘境，感受大自然的鬼斧神工。</div>
            </div>
            """)

    # --- Tab 2: 經費 ---
    with tab2:
        # 動態計算邏輯
        base_cost = 800 if "小資" in budget else (1500 if "舒適" in budget else 3000)
        stay_cost = 0
        if "二日" in days: stay_cost = 2000
        if "三日" in days: stay_cost = 4000
        
        # 旺季加成 (2月櫻花季住宿較貴)
        season_markup = 1.2 if travel_date.month == 2 else 1.0
        final_accom = int(stay_cost * season_markup)
        
        st.markdown("#### 💰 預算預估表 (每人)")
        c1, c2, c3 = st.columns(3)
        c1.metric("餐飲娛樂", f"${base_cost}")
        c2.metric("住宿預算", f"${final_accom}", delta="旺季微調" if season_markup > 1 else None)
        c3.metric("交通油資", "$300-500")
        
        st.info(f"💡 **總計約：${base_cost + final_accom + 400} / 人**")
        if travel_date.month == 2:
            st.caption("⚠️ 提醒：2月份為超級旺季，民宿建議提前 2 個月預訂！")

    # --- Tab 3: 交通住宿 ---
    with tab3:
        st.subheader("🚗 交通攻略")
        if transport == "自行開車":
            st.warning(f"""
            **{travel_date.month}月份路況提醒：**
            {"櫻花季車潮眾多，北橫公路容易回堵，請務必早上 7 點前通過大溪。" if travel_date.month == 2 else "山區午後易起霧，請小心駕駛。"}
            """)
        elif transport == "搭乘公車/接駁車":
            st.info("""
            **賞櫻專車資訊：**
            - 請至大溪客運總站搭乘 5090/5091 路線。
            - 櫻花季期間 (2月中-3月中)，區公所通常會安排**「中巴陵-恩愛農場」**的計程車接駁，單趟約 $100/人。
            """)
            
        st.subheader("🛏️ 住宿建議")
        st.markdown("""
        - **想看雲海**：住「上巴陵」地區民宿。
        - **想方便**：住「角板山」或「羅浮」周邊。
        - **想省錢**：選擇「公有露營區」或教會民宿。
        """)

else:
    # 預設畫面
    st.info("👆 請輸入您的出發日期，讓我們幫您算出花開了沒！")
    
    # 彩蛋：根據當下真實月份給建議
    current_month = datetime.now().month
    if current_month == 1:
        st.markdown("**現在是 1 月，角板山的梅花正香喔！**")
    elif current_month == 2:
        st.markdown("**現在是 2 月，櫻花季大爆發！趕快規劃！**")
