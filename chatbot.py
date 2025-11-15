import streamlit as st
import time
import random
from openai import AzureOpenAI  # Import Azure OpenAI client
import streamlit.components.v1 as components  # For embedding Google Maps

# 模擬回應的輔助函數（備用）
def simulate_response(prompt):
    prompt_lower = prompt.lower()
    print(prompt_lower)
    if "rebook hotels" in prompt_lower or "hotel" in prompt_lower:
        return "我可以幫您在機場附近重新預訂酒店。請查看下面的地圖以了解位置。"
    elif "請幫我重新預訂到東京的航班" in prompt_lower:
        return "正在檢查可用航班... 找到明天的選項。是否確認重新預訂？"
    elif "status" in prompt_lower:
        if st.session_state.tickets:
            latest_ticket = st.session_state.tickets[-1]
            return f"您的機票 {latest_ticket['id']} 狀態：{latest_ticket['status']}。"
        else:
            return "沒有未結案的機票。需要什麼幫助？"
    elif "advice" in prompt_lower or "typhoon" in prompt_lower:
        return "如果符合資格，建議留在機場貴賓室。提供餐飲和住宿代金券。需要更多詳情或進一步協助？"
    else:
        return "我可以幫您處理重新預訂或提供建議。請提供更多詳情。"

# 顯示帶標籤酒店的 Google 地圖
def display_hotel_rebooking_text():
    hotels = [
        {"name": "東京三井花園飯店 - 銀座", "lat": 35.6717, "lng": 139.7653},
        {"name": "赤坂蒙特雷酒店", "lat": 35.6759, "lng": 139.7315},
        {"name": "大森邁斯特酒店", "lat": 35.5884, "lng": 139.7312},
        {"name": "新宿王子酒店", "lat": 35.6940, "lng": 139.7006}
    ]

    # 構建 Markdown 訊息
    msg = (
        "\n\n### 🗺️ 東京四星級酒店位置\n\n"
        "以下是東京推薦的四星級酒店地圖：\n\n"
        "**可用酒店選項：**\n\n"
    )

    for hotel in hotels:
        msg += f"- **{hotel['name']}** — 位於 {hotel['lat']}, {hotel['lng']}\n"

    msg += "\n您想預訂其中一家酒店，還是尋找更多選項？"

    return msg

# 初始化 Azure OpenAI 客戶端（請替換為您的憑證）
client = AzureOpenAI(
    azure_endpoint="https://hkust.azure-api.net",  # 您的 Azure 端點
    api_key="57579d7aaa8348ff9b94760a66a92a6c",  # 您的 Azure OpenAI API 金鑰
    api_version="2023-05-15"  # 根據您的 Azure API 版本調整
)

# 初始化 session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "您好！我是國泰航空 IROPS 助理，由 Azure OpenAI 提供支援。在這次颱風干擾期間，我可以如何幫助您重新預訂或提供建議？"}
    ]

if "tickets" not in st.session_state:
    st.session_state.tickets = []  # 機票列表：[{"id": str, "status": str, "description": str}]

if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

if "show_assistance" not in st.session_state:
    st.session_state.show_assistance = False  # 控制「需要進一步協助？」提示的可見性

# Streamlit 頁面配置
st.set_page_config(page_title="國泰航空 IROPS 聊天機器人", page_icon="✈️", layout="wide")

# 應用程式標題
st.title("國泰航空 IROPS 應變聊天機器人")

# 側邊欄用於常見問題和機票追蹤
with st.sidebar:
    st.header("常見問題")
    with st.expander("什麼是 IROPS？"):
        st.write("IROPS 代表不正常運營，例如因颱風等天氣原因導致的航班中斷。")
    with st.expander("如何重新預訂我的航班？"):
        st.write("請要求我檢查可用選項，或請求進一步協助。")
    with st.expander("如果我需要特殊協助怎麼辦？"):
        st.write("使用視訊通話選項處理複雜需求。")
    with st.expander("如何追蹤我的機票？"):
        st.write("請查看下面的機票追蹤器以了解未結案的問題。")

    st.header("機票追蹤器")
    if st.session_state.tickets:
        for ticket in st.session_state.tickets:
            st.write(f"機票 {ticket['id']}：{ticket['description']} - 狀態：{ticket['status']}")
    else:
        st.write("沒有未結案的機票。")

# 主聊天區域
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 聊天輸入
prompt = st.chat_input("在此輸入您的訊息（例如「重新預訂我的航班」或「機場住宿建議」）...")

if prompt:
    # 添加使用者訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Azure OpenAI 回應
    with chat_container:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Azure OpenAI 整合
            try:
                response = client.chat.completions.create(
                    model="gpt-35-turbo",  # 您的 Azure OpenAI 部署名稱（例如 gpt-35-turbo 或 gpt-4）
                    messages=[
                        {"role": "system", "content": "您是國泰航空的專業助理，專門處理颱風干擾期間的 IROPS（不正常運營）。請提供簡潔、準確的重新預訂、機場住宿或其他旅行相關查詢建議。如有需要，提議轉接至真人客服。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                full_response = response.choices[0].message.content.strip()
            except Exception as e:
                # 增強錯誤處理，顯示錯誤類型和詳情
                error_type = type(e).__name__
                error_message = str(e)
                full_response = f"連接到 Azure OpenAI 時發生錯誤：類型：{error_type}，訊息：{error_message}。請重試或請求進一步協助。"
                # st.error(full_response)  # 在 Streamlit UI 中顯示錯誤

            # 如果 API 調用失敗，則使用備用模擬回應
            if not full_response or "Error connecting" in full_response:
                full_response = simulate_response(prompt)

            # 特殊情況處理：酒店重新預訂與 Google 地圖
            if "rebook hotels" in prompt.lower() or "hotel" in prompt.lower():
                full_response += display_hotel_rebooking_text()
                with chat_container:
                    # 嵌入 Google 地圖 iframe
                    map_html = """<iframe src="https://www.google.com/maps/d/u/0/embed?mid=16DXmbKpDXndFpmfSNsKCGr3L2kTbS1c&ehbc=2E312F" width="640" height="480"></iframe>"""
                    components.html(map_html, height=400)
            if "請幫我重新預訂到洛杉磯的航班" in prompt:
                full_response = "正在檢查可用航班... 找到明天的選項。是否確認重新預訂？"

            # 模擬打字效果的串流回應
            for chunk in full_response.split():
                full_response_chunk = full_response[:full_response.index(chunk) + len(chunk)] + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response_chunk + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 在 AI 回應後顯示「需要進一步協助？」提示
    st.session_state.show_assistance = True

    # 為重新預訂或機票相關查詢創建機票
    if "rebook" in prompt.lower() or "ticket" in prompt.lower():
        ticket_id = str(random.randint(1000, 9999))
        st.session_state.tickets.append({
            "id": ticket_id,
            "status": "未結案",
            "description": prompt
        })
        # st.rerun()  # 刷新側邊欄

# 協助提示和按鈕
if st.session_state.show_assistance:
    with chat_container:
        st.markdown("**需要進一步協助？**")
        col1, col2, col3 = st.columns([2, 2, 3])
        with col1:
            if st.button("聯繫真人客服"):
                st.write("正在轉接至真人客服...（模擬：已連接到客服。）")
                st.session_state.show_assistance = False  # 轉接後隱藏
                # 在實際應用中，排隊至客服人員
        with col2:
            if st.button("視訊通話協助"):
                st.write("正在啟動視訊通話...（模擬：適用於老年或複雜需求。）")
                st.session_state.show_assistance = False  # 視訊通話後隱藏
                # 在實際應用中，整合視訊 API
        with col3:
            if st.button("清除聊天"):
                st.session_state.messages = [
                    {"role": "assistant", "content": "您好！我是國泰航空 IROPS 助理，由 Azure OpenAI 提供支援。在這次颱風干擾期間，我可以如何幫助您重新預訂或提供建議？"}
                ]
                st.session_state.tickets = []
                st.session_state.feedback_given = False
                st.session_state.show_assistance = False
                st.rerun()

# 互動後的反饋部分
if len(st.session_state.messages) > 2 and not st.session_state.feedback_given:
    st.header("評價您的體驗")
    rating = st.slider("星級 (1-5)", 1, 5, 3)
    if st.button("提交反饋"):
        st.write(f"感謝您的 {rating} 星評價！")
        st.session_state.feedback_given = True

# Function to display Google Maps with labeled hotels
# Function to display map.png image
# Function to display Google Maps with labeled hotels
def display_hotel_rebooking_text():
    hotels = [
        {"name": "Millennium Mitsui Garden Hotel Tokyo - Ginza", "lat": 35.6717, "lng": 139.7653},
        {"name": "Hotel Monterey Akasaka", "lat": 35.6759, "lng": 139.7315},
        {"name": "Hotel Mystays Premier Omori", "lat": 35.5884, "lng": 139.7312},
        {"name": "Shinjuku Prince Hotel", "lat": 35.6940, "lng": 139.7006}
    ]

    
    

    # Build Markdown message
    msg = (
        "\n\n### 🗺️ 4-Star Hotel Locations in Tokyo\n\n"
        "Here's a map showing recommended 4-star hotels in Tokyo:\n\n"
        "**Available Hotel Options:**\n\n"
    )

    for hotel in hotels:
        msg += f"- **{hotel['name']}** — Located at {hotel['lat']}, {hotel['lng']}\n"

    msg += "\nWould you like me to book one of these or find more options?"

    return msg


