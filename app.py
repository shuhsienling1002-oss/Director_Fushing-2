import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定
# ==========================================
st.set_page_config(
    page_title="2026 復興區全境賞櫻制霸地圖",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (櫻花粉 + 資訊密度優化)
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
    
    /* 景點卡片 */
    .spot-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #FFE4E1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        height: 100%;
        transition: transform 0.2s;
        margin-bottom: 10px;
    }
    .spot-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(255, 105, 180, 0.3);
        border-color: #FF69B4;
    }
    
    /* 地區標籤 */
    .tag {
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 10px;
        color: white;
        display: inline-block;
        margin-right: 5px;
    }
    .tag-front { background-color: #2E8B57; }
    .tag-tribe { background-color: #D2691E; }
    .tag-back { background-color: #C71585; }
    .tag-secret { background-color: #663399; }
    
    /* 花種標籤 */
    .flower-tag {
        color: #C71585;
        font-size: 13px;
        font-weight: bold;
        background: #FFF0F5;
        padding: 2px 6px;
        border-radius: 4px;
    }
    
    /* 搜尋框優化 */
    .stTextInput>div>div>input {
        border-radius: 20px;
        border: 2px solid #FFB6C1;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 終極資料庫 (30+ 景點)
# ==========================================
all_spots = [
    # --- 前山 (入門輕鬆) ---
    {"name": "角板山行館", "region": "前山", "type": "梅花/山櫻", "month": [1, 2], "desc": "北橫賞花起點，戰備隧道與環湖步道。", "fee": "免門票"},
    {"name": "東眼山櫻花大道", "region": "前山", "type": "山櫻花", "month": [1, 2], "desc": "通往遊樂區的林道，早開山櫻形成紅色隧道。", "fee": "免門票"},
    {"name": "詩朗櫻花步道", "region": "前山", "type": "枝垂櫻/八重櫻", "month": [1, 2], "desc": "位於角板山對面，在地人的健行秘境。", "fee": "免門票"},
    {"name": "羅馬公路 (118縣道)", "region": "前山", "type": "山櫻花", "month": [1, 2], "desc": "沿途50公里種植上千棵山櫻，最美兜風路線。", "fee": "免門票"},
    {"name": "成福道路 (桃119線)", "region": "前山", "type": "山櫻花", "month": [1, 2], "desc": "東眼山支線，沿途山櫻花密集。", "fee": "免門票"},
    {"name": "翠墨莊園", "region": "前山", "type": "緋寒櫻/各類", "month": [1, 2], "desc": "需預約的精緻莊園，有日式鳥居造景。", "fee": "門票$150"},
    {"name": "悠然秘境小屋", "region": "前山", "type": "吉野櫻/八重櫻", "month": [2, 3], "desc": "三民地區隱藏版，花況極佳的私人園區。", "fee": "門票$50"},
    {"name": "丸山咖啡", "region": "前山", "type": "景觀櫻花", "month": [2], "desc": "海拔600公尺景觀餐廳，吃飯賞花。", "fee": "低消"},
    {"name": "小烏來風景區", "region": "前山", "type": "山櫻花", "month": [1, 2], "desc": "天空步道周邊有零星櫻花點綴。", "fee": "門票$50"},

    # --- 部落深處 (中橫/北橫中段) ---
    {"name": "比亞外 (Piyaway)", "region": "部落", "type": "山櫻/昭和櫻", "month": [1, 2], "desc": "藍腹鷴的故鄉，部落入口與教堂旁有櫻花。", "fee": "免門票"},
    {"name": "高義蘭部落 (夏蝶冬櫻)", "region": "部落", "type": "香水櫻/八重櫻", "month": [2], "desc": "★新秘境！『夏蝶冬櫻山谷園地』雙色花海。", "fee": "免門票/露營"},
    {"name": "內奎輝部落", "region": "部落", "type": "山櫻花", "month": [1, 2], "desc": "極少遊客的深山部落，野櫻綻放。", "fee": "免門票"},
    {"name": "上高義古路步道", "region": "部落", "type": "山櫻花", "month": [1, 2], "desc": "北橫公路旁的古道，幽靜自然。", "fee": "免門票"},
    {"name": "爺亨梯田", "region": "部落", "type": "山櫻/媽媽桃花", "month": [1, 2, 3], "desc": "梯田地景配粉色花海，攝影師最愛。", "fee": "免門票"},
    {"name": "光華櫻花故事林道", "region": "部落", "type": "昭和櫻", "month": [2, 3], "desc": "光華國小附近，浪漫的櫻花林道。", "fee": "免門票"},
    {"name": "雪霧鬧部落", "region": "部落", "type": "山櫻/桃花", "month": [2, 3], "desc": "雲端上的部落，產地桃花與櫻花交錯。", "fee": "免門票"},

    # --- 後山 (拉拉山/巴陵 - 一級戰區) ---
    {"name": "中巴陵櫻木花道", "region": "後山", "type": "昭和櫻", "month": [2], "desc": "最親民的免費昭和櫻隧道，必拍。", "fee": "免門票"},
    {"name": "拉拉山遊客中心", "region": "後山", "type": "千島櫻/吉野櫻", "month": [2, 3], "desc": "遊客中心對面停車場就是絕美賞櫻點。", "fee": "免門票"},
    {"name": "恩愛農場", "region": "後山", "type": "千島/富士櫻", "month": [2, 3], "desc": "王者等級！全台最知名的粉紅爆炸花海。", "fee": "門票$100"},
    {"name": "觀雲休憩農莊", "region": "後山", "type": "昭和/千島櫻", "month": [2, 3], "desc": "恩愛農場旁，佛心免門票，花況也不輸人。", "fee": "免門票"},
    {"name": "俠雲山莊", "region": "後山", "type": "昭和櫻/宏佳騰", "month": [2], "desc": "梯田式櫻花林，與恩愛農場相鄰。", "fee": "免門票"},
    {"name": "楓墅農莊", "region": "後山", "type": "昭和櫻", "month": [2], "desc": "隱藏在中心路的小型農莊秘境。", "fee": "清潔費"},
    {"name": "嶺鎮農場", "region": "後山", "type": "各類櫻花", "month": [2, 3], "desc": "視野極佳，可俯瞰山谷櫻花。", "fee": "需消費"},
    {"name": "光明農場", "region": "後山", "type": "霧社櫻 (白櫻)", "month": [3], "desc": "★稀有！台灣特有種白色霧社櫻，配馬告雞。", "fee": "需用餐"},
    {"name": "拉拉山輕鬆園", "region": "後山", "type": "墨染櫻/富士櫻", "month": [2, 3], "desc": "★隱藏版！位於比該道路，有少見的墨染櫻。", "fee": "門票$100"},
    {"name": "八福原櫻園", "region": "後山", "type": "富士/千島櫻", "month": [2, 3], "desc": "★卡拉部落秘境！花況密集度不輸恩愛。", "fee": "門票制"},
    {"name": "櫻花莊園", "region": "後山", "type": "雙色櫻", "month": [2, 3], "desc": "精緻的民宿櫻花造景。", "fee": "住宿客限定"},
    {"name": "中心路沿線", "region": "後山", "type": "富士櫻", "month": [2, 3], "desc": "通往恩愛農場的路邊私人農園。", "fee": "部分收費"},
    {"name": "巴陵古道生態園區", "region": "後山", "type": "山櫻/昭和櫻", "month": [2], "desc": "結合博物館與森林步道，知性賞櫻。", "fee": "免門票"},
    {"name": "拉拉山5.5K觀景台", "region": "後山", "type": "昭和櫻", "month": [2], "desc": "攝影愛好者拍攝彎道櫻花的著名點位。", "fee": "免門票"}
]

# ==========================================
# 4. 頁面內容
# ==========================================
st.markdown("""
    <div class="header-box">
        <div style="font-size: 28px; font-weight: bold;">🌸 2026 復興區賞櫻・終極全制霸</div>
        <div style="font-size: 16px; margin-top: 5px;">桃園市復興區長 <b>蘇佐璽</b> 獻給您最完整的 30+ 處賞花地圖 ❤️</div>
    </div>
""", unsafe_allow_html=True)

# 搜尋過濾器
col_search, col_filter = st.columns([2, 1])
with col_search:
    search_query = st.text_input("🔍 搜尋關鍵字 (如：免門票、昭和櫻、秘境)", placeholder="輸入關鍵字...")
with col_filter:
    region_filter = st.selectbox("地區篩選", ["全部地區", "前山 (近)", "部落 (中)", "後山 (遠)"])

# 篩選邏輯
filtered_spots = []
for s in all_spots:
    match_search = search_query == "" or search_query in s['name'] or search_query in s['type'] or search_query in s['desc'] or search_query in s['fee']
    match_region = region_filter == "全部地區" or region_filter[:2] in s['region']
    if match_search and match_region:
        filtered_spots.append(s)

# 顯示統計
st.caption(f"共搜尋到 **{len(filtered_spots)}** 個賞櫻景點 (全區共 {len(all_spots)} 個)")

# 建立 Grid 顯示
cols = st.columns(2) # 手機版雙欄顯示

for i, spot in enumerate(filtered_spots):
    # 決定標籤顏色
    tag_class = "tag-front"
    if spot['region'] == "部落": tag_class = "tag-tribe"
    if spot['region'] == "後山": tag_class = "tag-back"
    
    # 判斷是否為特殊秘境
    is_secret = "★" in spot['desc']
    secret_badge = '<span class="tag tag-secret">秘境</span>' if is_secret else ''
    
    with cols[i % 2]:
        # ⚠️ 關鍵修正：HTML 字串完全靠左，避免被誤判為 Markdown 程式碼區塊
        card_html = f"""
<div class="spot-card">
    <div style="font-weight: bold; font-size: 18px; color: #333; margin-bottom: 5px;">
        <span class="tag {tag_class}">{spot['region']}</span>
        {spot['name']}
    </div>
    <div style="margin-bottom: 8px;">
        {secret_badge}
        <span class="flower-tag">🌸 {spot['type']}</span>
        <span style="font-size: 12px; color: #666; margin-left: 5px;">📅 {spot['month'][0]}-{spot['month'][-1]}月</span>
    </div>
    <div style="font-size: 14px; color: #555; line-height: 1.4; margin-bottom: 8px;">
        {spot['desc']}
    </div>
    <div style="font-size: 13px; color: #E91E63; font-weight: bold;">
        💰 {spot['fee']}
    </div>
</div>
"""
        st.markdown(card_html, unsafe_allow_html=True)

# ==========================================
# 5. 底部互動區
# ==========================================
st.markdown("---")
with st.expander("📝 區長的小叮嚀 (點我展開)"):
    st.markdown("""
    1. **秘境禮儀**：部分景點為私人農園 (如夏蝶冬櫻、悠然秘境)，請務必愛護環境，勿喧嘩、勿留垃圾。
    2. **交通管制**：櫻花季期間 (2月中-3月中)，後山地區 (恩愛農場周邊) 會有嚴格交通管制，建議搭乘接駁車。
    3. **即時花況**：花期受氣候影響很大，出發前建議先上「復興區公所」或各農場粉專確認最新花況。
    """)
