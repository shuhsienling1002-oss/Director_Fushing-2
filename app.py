import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定 (保持原樣)
# ==========================================
st.set_page_config(
    page_title="2026 復興區花季行程規劃",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (保持原本的粉色玻璃感)
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
    .spot-title { font-weight: bold; color: #C71585; font-size: 18px; }
    .spot-desc { font-size: 14px; color: #555; }
    .spot-tag { 
        font-size: 12px; background: #FFE4E1; color: #D87093; 
        padding: 2px 8px; border-radius: 10px; margin-right: 5px;
    }
    
    /* 30個景點列表樣式 */
    .all-spots-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }
    .mini-card {
        background: white;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #eee;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (已擴充至 30+ 個景點)
# ==========================================
all_spots_db = [
    # 前山
    {"name": "角板山行館", "region": "前山", "month": [1, 2], "flower": "梅花/山櫻", "desc": "北橫賞花起點，戰備隧道。"},
    {"name": "東眼山櫻花大道", "region": "前山", "month": [1, 2], "flower": "山櫻花", "desc": "林道兩旁紅色隧道。"},
    {"name": "詩朗櫻花步道", "region": "前山", "month": [1, 2], "flower": "枝垂櫻", "desc": "在地健行秘境。"},
    {"name": "羅馬公路", "region": "前山", "month": [1, 2], "flower": "山櫻花", "desc": "最美兜風路線。"},
    {"name": "成福道路", "region": "前山", "month": [1, 2], "flower": "山櫻花", "desc": "東眼山支線秘境。"},
    {"name": "翠墨莊園", "region": "前山", "month": [1, 2], "flower": "緋寒櫻", "desc": "需預約，日式造景。"},
    {"name": "悠然秘境小屋", "region": "前山", "month": [2, 3], "flower": "吉野櫻", "desc": "三民隱藏版私人園區。"},
    {"name": "丸山咖啡", "region": "前山", "month": [2], "flower": "景觀櫻花", "desc": "海拔600m景觀餐廳。"},
    {"name": "小烏來風景區", "region": "前山", "month": [1, 2], "flower": "山櫻花", "desc": "天空步道周邊。"},
    
    # 部落
    {"name": "比亞外部落", "region": "部落", "month": [1, 2], "flower": "昭和櫻", "desc": "藍腹鷴的故鄉。"},
    {"name": "高義蘭(夏蝶冬櫻)", "region": "部落", "month": [2], "flower": "香水櫻", "desc": "新開發的山谷雙色花海。"},
    {"name": "內奎輝部落", "region": "部落", "month": [1, 2], "flower": "野櫻", "desc": "深山寧靜部落。"},
    {"name": "上高義古路", "region": "部落", "month": [1, 2], "flower": "山櫻花", "desc": "北橫旁古道。"},
    {"name": "爺亨梯田", "region": "部落", "month": [1, 2, 3], "flower": "山櫻/桃花", "desc": "梯田地景配粉色花海。"},
    {"name": "光華櫻花故事林道", "region": "部落", "month": [2, 3], "flower": "昭和櫻", "desc": "光華國小旁浪漫林道。"},
    {"name": "雪霧鬧部落", "region": "部落", "month": [2, 3], "flower": "桃花/櫻花", "desc": "雲端上的部落。"},
    
    # 後山
    {"name": "中巴陵櫻木花道", "region": "後山", "month": [2], "flower": "昭和櫻", "desc": "免費粉紅隧道必拍。"},
    {"name": "拉拉山遊客中心", "region": "後山", "month": [2, 3], "flower": "千島櫻", "desc": "停車場就是絕美景點。"},
    {"name": "恩愛農場", "region": "後山", "month": [2, 3], "flower": "千島/富士櫻", "desc": "全台最知名爆炸花海。"},
    {"name": "觀雲休憩農莊", "region": "後山", "month": [2, 3], "flower": "昭和櫻", "desc": "恩愛農場旁免門票秘境。"},
    {"name": "俠雲山莊", "region": "後山", "month": [2], "flower": "昭和櫻", "desc": "梯田式櫻花林。"},
    {"name": "楓墅農莊", "region": "後山", "month": [2], "flower": "昭和櫻", "desc": "中心路小型秘境。"},
    {"name": "嶺鎮農場", "region": "後山", "month": [2, 3], "flower": "各類櫻花", "desc": "俯瞰山谷視野極佳。"},
    {"name": "光明農場", "region": "後山", "month": [3], "flower": "霧社櫻", "desc": "稀有白櫻配馬告雞。"},
    {"name": "拉拉山輕鬆園", "region": "後山", "month": [2, 3], "flower": "墨染櫻", "desc": "比該道路隱藏版。"},
    {"name": "八福原櫻園", "region": "後山", "month": [2, 3], "flower": "富士櫻", "desc": "卡拉部落新秘境。"},
    {"name": "櫻花莊園", "region": "後山", "month": [2, 3], "flower": "雙色櫻", "desc": "精緻民宿造景。"},
    {"name": "中心路沿線", "region": "後山", "month": [2, 3], "flower": "富士櫻", "desc": "前往恩愛農場路邊。"},
    {"name": "巴陵古道生態園區", "region": "後山", "month": [2], "flower": "山櫻/昭和", "desc": "森林步道與博物館。"},
    {"name": "拉拉山5.5K觀景台", "region": "後山", "month": [2], "flower": "昭和櫻", "desc": "攝影師拍攝彎道名點。"}
]

# 智慧推薦邏輯 (從大資料庫挑選)
def analyze_trip(travel_date, group):
    m = travel_date.month
    
    # 1. 篩選當月有花的景點
    valid_spots = [s for s in all_spots_db if m in s['month']]
    
    if not valid_spots:
        # 非花季，給通用建議
        return "🌲 森林浴季節", "目前非主花季，推薦深呼吸行程。", {"name": "小烏來天空步道", "region": "前山", "flower": "景觀", "desc": "透明步道與瀑布"}, {"name": "拉拉山巨木區", "region": "後山", "flower": "神木", "desc": "千年紅檜群"}

    # 2. 判斷花況文字
    flower_status = ""
    if m == 1: flower_status = "❄️ 梅花與山櫻花 (早春序曲)"
    elif m == 2: flower_status = "🌸 粉紅櫻花大爆發 (最美時刻)"
    elif m == 3: flower_status = "🍑 桃花與吉野櫻 (春日尾聲)"
    
    # 3. 挑選推薦點 (Amis AI Logic)
    # 優先推薦：當月最熱門 (通常在後山)
    primary_spot = next((s for s in valid_spots if s['name'] in ["恩愛農場", "角板山行館", "中巴陵櫻木花道", "爺亨梯田"]), valid_spots[0])
    
    # 次要推薦：根據群體
    secondary_spots = [s for s in valid_spots if s['name'] != primary_spot['name']]
    secondary_spot = secondary_spots[0] if secondary_spots else primary_spot
    
    if "長輩" in group or "親子" in group:
        # 找前山或平緩的
        easy_spots = [s for s in secondary_spots if s['region'] == "前山"]
        if easy_spots: secondary_spot = easy_spots[0]
    elif "情侶" in group:
        # 找浪漫的
        romantic = [s for s in secondary_spots if "昭和櫻" in s['flower'] or "吉野櫻" in s['flower']]
        if romantic: secondary_spot = romantic[0]
        
    return flower_status, f"根據日期，推薦您前往 {primary_spot['region']} 與 {secondary_spot['region']} 賞花。", primary_spot, secondary_spot

# ==========================================
# 4. 頁面內容 (回歸原本架構)
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌸 2026 復興區花季行程規劃</div>
        <div class="header-subtitle">桃園市復興區長 <b>蘇佐璽</b> 幫您算準花期，不撲空 ❤️</div>
    </div>
""", unsafe_allow_html=True)

# === 輸入區 (原本的樣子) ===
with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### 📅 第一步：選擇出發日期")
    
    col1, col2 = st.columns(2)
    with col1:
        travel_date = st.date_input("預計出發日期", value=date(2026, 2, 20), min_value=date(2026, 1, 1), max_value=date(2026, 4, 30))
        days = st.selectbox("行程天數", ["一日遊", "二日遊", "三日遊"])
    with col2:
        group = st.selectbox("出遊夥伴", ["情侶/夫妻", "親子家庭", "長輩樂齡", "熱血獨旅"])
        transport = st.selectbox("交通方式", ["自行開車", "大眾運輸", "機車"])
    
    generate_btn = st.button("🚀 開始規劃賞花行程")
    st.markdown('</div>', unsafe_allow_html=True)

# === 結果顯示 ===
if generate_btn:
    # 執行分析
    status_title, status_desc, spot1, spot2 = analyze_trip(travel_date, group)
    
    # 資訊看板
    st.markdown(f"""
    <div class="info-box">
        <div style="font-size: 20px; font-weight: bold; color: #C71585; margin-bottom: 5px;">
            📅 {travel_date.month}/{travel_date.day} 花況預報
        </div>
        <div class="weather-tag">{status_title}</div>
        <div style="color: #555;">{status_desc}</div>
    </div>
    """, unsafe_allow_html=True)

    # Tab 分頁 (加入全景點名鑑)
    tab1, tab2, tab3, tab4 = st.tabs(["🗓️ 推薦行程", "💰 經費概算", "🚗 交通住宿", "🌸 30處賞櫻名鑑"])

    # --- Tab 1: 行程 ---
    with tab1:
        st.subheader(f"✨ {days} 專屬規劃")
        # 上午
        st.markdown(f"""
        <div class="timeline-item">
            <div class="spot-title">09:30 {spot1['name']} ({spot1['region']})</div>
            <div><span class="spot-tag">當日首選</span><span class="spot-tag">{spot1['flower']}</span></div>
            <div class="spot-desc">{spot1['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 中午
        st.markdown(f"""
        <div class="timeline-item">
            <div class="spot-title">12:30 在地風味餐</div>
            <div class="spot-desc">推薦：馬告磚窯雞、刺蔥烘蛋。</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 下午
        st.markdown(f"""
        <div class="timeline-item">
            <div class="spot-title">14:30 {spot2['name']} ({spot2['region']})</div>
            <div><span class="spot-tag">順遊秘境</span><span class="spot-tag">{spot2['flower']}</span></div>
            <div class="spot-desc">{spot2['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if "二日" in days or "三日" in days:
            st.markdown("---")
            st.markdown("**Day 2 建議**：清晨前往 **拉拉山巨木區** 吸收芬多精，中午至 **上巴陵** 觀景台用餐。")

    # --- Tab 2: 經費 ---
    with tab2:
        base = 1000
        if "二日" in days: base += 2000
        st.metric("預估費用 (每人)", f"${base} 起", "含餐飲交通")
        st.caption("※ 櫻花季民宿房價可能浮動，請以店家報價為準。")

    # --- Tab 3: 交通 ---
    with tab3:
        st.info("🚗 **自行開車**：櫻花季北橫易塞車，建議 07:00 前抵達大溪。")
        st.info("🚌 **大眾運輸**：可於大溪總站搭乘 5090 / 5091 客運前往拉拉山。")

    # --- Tab 4: 全部景點 (滿足您的要求) ---
    with tab4:
        st.markdown("### 🌸 復興區 30+ 賞櫻地圖全收錄")
        st.caption("這就是您要的「全部全部」！包含農場、部落與公路秘境。")
        
        # 分區顯示
        for region_name in ["前山", "部落", "後山"]:
            st.markdown(f"#### 📍 {region_name}地區")
            cols = st.columns(2)
            region_spots = [s for s in all_spots_db if s['region'] == region_name]
            
            for i, s in enumerate(region_spots):
                with cols[i%2]:
                    st.markdown(f"""
                    <div class="mini-card">
                        <b>{s['name']}</b> <span style="color:#C71585; font-size:12px;">{s['flower']}</span><br>
                        <span style="color:#666; font-size:12px;">{s['desc']}</span>
                    </div>
                    """, unsafe_allow_html=True)

else:
    st.info("👆 請調整上方日期與人數，按下按鈕生成行程！")
