import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定
# ==========================================
st.set_page_config(
    page_title="2026 復興區賞櫻全攻略 (資料庫終極版)",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學
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
    
    /* 卡片設計 */
    .card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #FFE4E1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 10px;
        height: 100%;
    }
    
    /* 住宿卡片 (紫色) */
    .hotel-card { border-left: 5px solid #9370DB; background: #F8F8FF; }
    .hotel-tag { font-size: 11px; padding: 2px 8px; border-radius: 10px; color: white; background-color: #9370DB; margin-right: 5px; }
    
    /* 景點卡片 (粉色) */
    .spot-card-full { border-left: 5px solid #FF69B4; }
    
    /* 連結線 */
    .connect-line {
        border-left: 2px dashed #aaa;
        margin-left: 20px;
        padding-left: 20px;
        padding-bottom: 20px;
        color: #666;
        font-size: 13px;
    }
    
    /* 標籤 */
    .tag { font-size: 11px; padding: 2px 6px; border-radius: 4px; color: white; margin-right: 4px; }
    .tag-front { background: #2E8B57; }
    .tag-tribe { background: #D2691E; }
    .tag-back { background: #C71585; }
    .flower-tag { color: #C71585; font-size: 12px; font-weight: bold; background: #FFF0F5; padding: 2px 6px; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 終極資料庫 (30景點 + 25住宿)
# ==========================================

# A. 30+ 賞櫻景點 (一個都沒少)
all_spots_db = [
    # 前山
    {"name": "角板山行館", "region": "前山", "month": [1, 2], "type": "梅花/山櫻", "desc": "北橫賞花起點，戰備隧道。", "fee": "免門票"},
    {"name": "東眼山櫻花大道", "region": "前山", "month": [1, 2], "type": "山櫻花", "desc": "林道兩旁紅色隧道。", "fee": "免門票"},
    {"name": "詩朗櫻花步道", "region": "前山", "month": [1, 2], "type": "枝垂櫻", "desc": "在地健行秘境。", "fee": "免門票"},
    {"name": "羅馬公路", "region": "前山", "month": [1, 2], "type": "山櫻花", "desc": "最美兜風路線。", "fee": "免門票"},
    {"name": "成福道路", "region": "前山", "month": [1, 2], "type": "山櫻花", "desc": "東眼山支線秘境。", "fee": "免門票"},
    {"name": "翠墨莊園", "region": "前山", "month": [1, 2], "type": "緋寒櫻", "desc": "需預約，日式造景。", "fee": "門票$150"},
    {"name": "悠然秘境小屋", "region": "前山", "month": [2, 3], "type": "吉野櫻", "desc": "三民隱藏版私人園區。", "fee": "門票$50"},
    {"name": "丸山咖啡", "region": "前山", "month": [2], "type": "景觀櫻花", "desc": "海拔600m景觀餐廳。", "fee": "低消"},
    {"name": "小烏來風景區", "region": "前山", "month": [1, 2], "type": "山櫻花", "desc": "天空步道周邊。", "fee": "門票$50"},
    
    # 部落
    {"name": "比亞外部落", "region": "部落", "month": [1, 2], "type": "昭和櫻", "desc": "藍腹鷴的故鄉。", "fee": "免門票"},
    {"name": "高義蘭(夏蝶冬櫻)", "region": "部落", "month": [2], "type": "香水櫻", "desc": "★新秘境！山谷雙色花海。", "fee": "免門票"},
    {"name": "內奎輝部落", "region": "部落", "month": [1, 2], "type": "野櫻", "desc": "深山寧靜部落。", "fee": "免門票"},
    {"name": "上高義古路", "region": "部落", "month": [1, 2], "type": "山櫻花", "desc": "北橫旁古道。", "fee": "免門票"},
    {"name": "爺亨梯田", "region": "部落", "month": [1, 2, 3], "type": "山櫻/桃花", "desc": "梯田地景配粉色花海。", "fee": "免門票"},
    {"name": "光華櫻花故事林道", "region": "部落", "month": [2, 3], "type": "昭和櫻", "desc": "光華國小旁浪漫林道。", "fee": "免門票"},
    {"name": "雪霧鬧部落", "region": "部落", "month": [2, 3], "type": "桃花/櫻花", "desc": "雲端上的部落。", "fee": "免門票"},
    
    # 後山
    {"name": "中巴陵櫻木花道", "region": "後山", "month": [2], "type": "昭和櫻", "desc": "免費粉紅隧道必拍。", "fee": "免門票"},
    {"name": "拉拉山遊客中心", "region": "後山", "month": [2, 3], "type": "千島櫻", "desc": "停車場就是絕美景點。", "fee": "免門票"},
    {"name": "恩愛農場", "region": "後山", "month": [2, 3], "type": "千島/富士櫻", "desc": "全台最知名爆炸花海。", "fee": "門票$100"},
    {"name": "觀雲休憩農莊", "region": "後山", "month": [2, 3], "type": "昭和櫻", "desc": "恩愛農場旁免門票秘境。", "fee": "免門票"},
    {"name": "俠雲山莊", "region": "後山", "month": [2], "type": "昭和櫻", "desc": "梯田式櫻花林。", "fee": "免門票"},
    {"name": "楓墅農莊", "region": "後山", "month": [2], "type": "昭和櫻", "desc": "中心路小型秘境。", "fee": "清潔費"},
    {"name": "嶺鎮農場", "region": "後山", "month": [2, 3], "type": "各類櫻花", "desc": "俯瞰山谷視野極佳。", "fee": "需消費"},
    {"name": "光明農場", "region": "後山", "month": [3], "type": "霧社櫻", "desc": "★稀有！白櫻配馬告雞。", "fee": "需用餐"},
    {"name": "拉拉山輕鬆園", "region": "後山", "month": [2, 3], "type": "墨染櫻", "desc": "★隱藏版！比該道路秘境。", "fee": "門票$100"},
    {"name": "八福原櫻園", "region": "後山", "month": [2, 3], "type": "富士櫻", "desc": "★卡拉部落新秘境。", "fee": "門票制"},
    {"name": "櫻花莊園", "region": "後山", "month": [2, 3], "type": "雙色櫻", "desc": "精緻民宿造景。", "fee": "住宿客"},
    {"name": "中心路沿線", "region": "後山", "month": [2, 3], "type": "富士櫻", "desc": "前往恩愛農場路邊。", "fee": "部分收費"},
    {"name": "巴陵古道生態園區", "region": "後山", "month": [2], "type": "山櫻/昭和", "desc": "森林步道與博物館。", "fee": "免門票"},
    {"name": "拉拉山5.5K觀景台", "region": "後山", "month": [2], "type": "昭和櫻", "desc": "攝影師拍攝彎道名點。", "fee": "免門票"}
]

# B. 25+ 住宿資料庫 (擴充版)
hotels_db = [
    # --- 前山 ---
    {"name": "復興青年活動中心", "region": "前山", "level": 1, "tags": ["高CP值", "湖景"], "desc": "角板山公園內，最方便。"},
    {"name": "普拉多山丘假期", "region": "前山", "level": 3, "tags": ["歐式鄉村", "網美"], "desc": "三民地區黃色歐風建築。"},
    {"name": "小烏來山莊", "region": "前山", "level": 2, "tags": ["近天空步道"], "desc": "走路就到小烏來瀑布。"},
    {"name": "羅浮天空溫泉飯店", "region": "前山", "level": 3, "tags": ["溫泉", "新開幕"], "desc": "房內泡湯，設施新穎。"},
    {"name": "山水奇異民宿", "region": "前山", "level": 2, "tags": ["英式風", "景觀"], "desc": "北橫路邊，適合拍照。"},
    {"name": "象山民宿", "region": "前山", "level": 1, "tags": ["平價", "老字號"], "desc": "小烏來風景區內。"},
    {"name": "基國派老教堂民宿", "region": "前山", "level": 2, "tags": ["文化", "安靜"], "desc": "鄰近老教堂，環境清幽。"},
    
    # --- 部落 ---
    {"name": "爺亨溫泉夢幻露營", "region": "部落", "level": 2, "tags": ["露營", "溫泉"], "desc": "櫻花樹下的豪華露營。"},
    {"name": "河那灣民宿", "region": "部落", "level": 1, "tags": ["原民風", "溪流"], "desc": "羅浮橋畔，親近自然。"},
    {"name": "飛鼠不渴露營區", "region": "部落", "level": 2, "tags": ["露營", "親子"], "desc": "雪霧鬧部落，雲端露營。"},
    {"name": "伊萬農場", "region": "部落", "level": 1, "tags": ["露營", "賞櫻"], "desc": "雪霧鬧知名賞櫻露營點。"},
    {"name": "摩亞農場", "region": "部落", "level": 1, "tags": ["露營", "雲海"], "desc": "光華部落高海拔露營。"},
    
    # --- 後山 (上巴陵) ---
    {"name": "恩愛農場小木屋", "region": "後山", "level": 2, "tags": ["花海第一排"], "desc": "出門就是櫻花 (極難訂)。"},
    {"name": "拉拉山 5.5K 農莊", "region": "後山", "level": 2, "tags": ["景觀", "烤肉"], "desc": "視野開闊，適合聚會。"},
    {"name": "雲山仙境民宿", "region": "後山", "level": 3, "tags": ["雲海", "電梯"], "desc": "上巴陵高評價景觀民宿。"},
    {"name": "觀雲休憩農莊", "region": "後山", "level": 1, "tags": ["平價", "賞花"], "desc": "恩愛農場旁高CP值。"},
    {"name": "富仙境渡假旅館", "region": "後山", "level": 2, "tags": ["便利", "景觀"], "desc": "上巴陵鬧區，吃飯方便。"},
    {"name": "谷點咖啡民宿", "region": "後山", "level": 3, "tags": ["無敵山景"], "desc": "下巴陵峽谷視野。"},
    {"name": "俠雲山莊", "region": "後山", "level": 2, "tags": ["賞花", "包棟"], "desc": "就在櫻花林旁邊。"},
    {"name": "嶺鎮農場", "region": "後山", "level": 2, "tags": ["最高點", "視野"], "desc": "中心路最高點，俯瞰全景。"},
    {"name": "瑞士鄉村農莊", "region": "後山", "level": 2, "tags": ["歐風", "老牌"], "desc": "中心路老字號民宿。"},
    {"name": "達觀山莊", "region": "後山", "level": 2, "tags": ["木屋", "神木"], "desc": "近拉拉山神木區入口。"},
    {"name": "侑德園民宿", "region": "後山", "level": 2, "tags": ["木屋", "庭園"], "desc": "上巴陵中心，環境舒適。"},
    {"name": "拉拉山雲河露營農場", "region": "後山", "level": 1, "tags": ["露營", "雲海"], "desc": "中心路高海拔露營。"}
]

# ==========================================
# 4. 智慧連動引擎
# ==========================================
def plan_itinerary(travel_date, days, budget_level, group):
    m = travel_date.month
    
    # 1. 景點選擇
    candidates = [s for s in all_spots_db if m in s['month']]
    if not candidates: candidates = all_spots_db[:3]
    
    main_spot = next((s for s in candidates if "恩愛" in s['name']), candidates[-1])
    if m == 1: main_spot = next((s for s in candidates if "角板山" in s['name']), candidates[0])
    
    # 2. 住宿策略
    stay_region = "前山"
    reason = "行程輕鬆，選擇多樣。"
    
    if main_spot['region'] == "後山" and "一日" not in days:
        stay_region = "後山"
        reason = "💡 策略：為避開第二天上山車潮，強烈建議**前一晚住上巴陵(後山)**！"
    elif "溫泉" in group:
        stay_region = "前山" # 羅浮/爺亨
        reason = "💡 策略：為了享受溫泉，建議安排羅浮或部落區住宿。"
    elif "露營" in group: # 假設有露營需求
        stay_region = "部落"
        reason = "💡 策略：復興區部落擁有最美的星空露營區。"

    # 3. 住宿篩選
    b_lvl = 1
    if "舒適" in budget_level: b_lvl = 2
    if "豪華" in budget_level: b_lvl = 3
    
    # 先篩區域
    recommended_hotels = [h for h in hotels_db if h['region'] == stay_region]
    
    # 再篩等級 (寬容度+1/-1)
    final_hotels = [h for h in recommended_hotels if abs(h['level'] - b_lvl) <= 1]
    
    # 如果篩完沒東西，就退回區域篩選結果
    if not final_hotels: final_hotels = recommended_hotels

    return main_spot, stay_region, reason, final_hotels

# ==========================================
# 5. UI 呈現
# ==========================================
st.markdown("""
    <div class="header-box">
        <div style="font-size: 26px; font-weight: bold;">🌸 2026 復興區賞櫻攻略</div>
        <div style="font-size: 15px; margin-top: 5px;">桃園市復興區長 <b>蘇佐璽</b> 邀請您 ❤️</div>
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
        group = st.selectbox("類型", ["情侶", "親子", "長輩", "攝影團", "露營愛好者"])
    
    btn = st.button("🚀 啟動連動規劃")

# 輸出區
if btn:
    main_spot, stay_region, stay_reason, hotels = plan_itinerary(travel_date, days, budget, group)
    
    st.markdown("---")
    
    t1, t2, t3, t4 = st.tabs(["🗺️ 連動行程表", "🛏️ 推薦住宿", "💰 預算詳情", "🌸 景點大全"])
    
    # --- Tab 1: 行程 ---
    with t1:
        st.subheader(f"✨ {days} 完美銜接計畫")
        st.markdown(f"#### Day 1：{main_spot['month'][0]}月花季序曲")
        
        st.markdown(f"""
        <div class="card">
            <span class="tag tag-front">前山</span> <b>09:30 角板山/羅浮</b><br>
            <span style="color:#666; font-size:13px;">北橫旅遊第一站，暖身行程。</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""<div class="connect-line">🚗 前往{stay_region} (途中午餐)</div>""", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="card">
            <span class="tag tag-tribe">部落</span> <b>12:30 在地風味餐</b><br>
            <span style="color:#666; font-size:13px;">推薦：馬告山豬肉、竹筒飯。</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"#### 🌙 住宿落腳點：{stay_region}")
        st.info(stay_reason)
        
        # 顯示推薦住宿 (前3個)
        cols = st.columns(3)
        for i, h in enumerate(hotels[:3]):
            with cols[i]:
                st.markdown(f"""
                <div class="card hotel-card">
                    <b>{h['name']}</b><br>
                    <span style="font-size:12px; color:#555;">{h['desc']}</span>
                </div>
                """, unsafe_allow_html=True)

        if "一日" not in days:
            st.markdown(f"#### Day 2：{main_spot['type']}大爆發")
            st.markdown(f"""<div class="connect-line">☀️ 早安！從{stay_region}出發</div>""", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="card">
                <span class="tag tag-back">重點</span> <b>08:30 {main_spot['name']}</b><br>
                <span style="color:#C71585; font-weight:bold;">🌸 本次行程最高潮！</span><br>
                <span style="color:#666; font-size:13px;">{main_spot['desc']}</span>
            </div>
            """, unsafe_allow_html=True)

    # --- Tab 2: 完整住宿 ---
    with t2:
        st.markdown(f"### 🛏️ 精選 {stay_region} 住宿 ({len(hotels)}間)")
        st.caption(f"已根據您的預算【{budget}】篩選：")
        
        # Grid 顯示
        cols = st.columns(2)
        for i, h in enumerate(hotels):
            with cols[i%2]:
                tags_html = "".join([f'<span class="hotel-tag">{t}</span>' for t in h['tags']])
                price_icon = "💲" * h['level']
                
                st.markdown(f"""
                <div class="card hotel-card">
                    <div style="display:flex; justify-content:space-between;">
                        <div style="font-size:16px; font-weight:bold;">{h['name']}</div>
                        <div style="color:#666;">{price_icon}</div>
                    </div>
                    <div style="margin: 5px 0;">{tags_html}</div>
                    <div style="font-size:13px; color:#444;">{h['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

    # --- Tab 3: 預算 ---
    with t3:
        price_base = 1500 if "小資" in budget else (3000 if "舒適" in budget else 6000)
        st.metric("預估總花費", f"${price_base} /人")
        st.warning("⚠️ 櫻花季 (2月) 住宿強烈建議提前 3-6 個月預訂！")

    # --- Tab 4: 景點全名鑑 ---
    with t4:
        st.markdown("### 🌸 30+ 賞櫻地圖全收錄")
        search = st.text_input("🔍 搜尋景點", placeholder="輸入關鍵字...")
        
        for region_name in ["前山", "部落", "後山"]:
            st.markdown(f"#### 📍 {region_name}地區")
            region_spots = [s for s in all_spots_db if s['region'] == region_name]
            if search:
                region_spots = [s for s in region_spots if search in s['name'] or search in s['desc'] or search in s['type']]
                
            cols = st.columns(2)
            for i, s in enumerate(region_spots):
                tag_cls = "tag-front"
                if region_name == "部落": tag_cls = "tag-tribe"
                if region_name == "後山": tag_cls = "tag-back"

                with cols[i%2]:
                    st.markdown(f"""
                    <div class="card spot-card-full">
                        <div style="font-weight: bold; font-size: 16px;">
                            <span class="tag {tag_cls}">{s['region']}</span>
                            {s['name']}
                        </div>
                        <div style="margin: 5px 0;">
                            <span class="flower-tag">🌸 {s['type']}</span>
                        </div>
                        <div style="font-size: 13px; color: #555;">{s['desc']}</div>
                        <div style="font-size: 12px; color: #E91E63; margin-top: 5px;">💰 {s['fee']}</div>
                    </div>
                    """, unsafe_allow_html=True)
