import streamlit as st
from PIL import Image
import os

# Set page config
st.set_page_config(
    page_title="Black Box Decoder",
    page_icon="🔓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #3164b7;
        font-size: 2.5em;
        margin-bottom: 30px;
    }
    
    .level-header {
        color: #ffffff;
        font-size: 1.5em;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .score-display {
        position: fixed;
        top: 20px;
        left: 20px;
        background-color: #2b2b2b;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        font-weight: bold;
        z-index: 999;
    }
    
    .success-message {
        background-color: #1dde20;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    
    .error-message {
        background-color: #cf2121;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    
    .crypto-table {
        margin: 20px 0;
    }
    
    .crypto-table table {
        width: 100%;
        border-collapse: collapse;
        background-color: #333333;
        color: white;
    }
    
    .crypto-table th, .crypto-table td {
        padding: 10px;
        text-align: center;
        border: 1px solid #555;
    }
    
    .crypto-table th {
        background-color: #2b2b2b;
        text-decoration: underline;
    }
    
    .navigation-buttons {
        display: flex;
        justify-content: space-between;
        margin: 20px 0;
    }
    
    .end-page-score {
        text-align: center;
        font-size: 2em;
        color: #3164b7;
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'start'
if 'scores' not in st.session_state:
    st.session_state.scores = 0
if 'level_1_passed' not in st.session_state:
    st.session_state.level_1_passed = False
if 'level_2_passed' not in st.session_state:
    st.session_state.level_2_passed = False
if 'level_3_passed' not in st.session_state:
    st.session_state.level_3_passed = False

def add_score():
    st.session_state.scores += 1

def show_score():
    st.markdown(f'<div class="score-display">分數： {st.session_state.scores}</div>', unsafe_allow_html=True)

def create_crypto_table(samples):
    """Create a table showing encryption samples"""
    table_html = """
    <div class="crypto-table">
        <table>
            <tr>
                <th>輸入字串</th>
                <th>加密結果</th>
            </tr>
    """
    
    for original, encrypted in samples:
        table_html += f"""
            <tr>
                <td>{original}</td>
                <td>{encrypted}</td>
            </tr>
        """
    
    table_html += """
        </table>
    </div>
    """
    return table_html

def start_page():
    st.markdown('<h1 class="main-header">🔓 Black Box Decoder</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 50px 0;">
        <h2>歡迎來到黑盒解碼挑戰！</h2>
        <p>透過觀察加密模式，破解三個關卡的密碼謎題</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 開始挑戰", use_container_width=True, type="primary"):
            st.session_state.current_page = 'level_1'
            st.rerun()

def level_page(level_num, description, samples, question, correct_answer):
    show_score()
    
    st.markdown(f'<h2 class="level-header">Level {level_num}</h2>', unsafe_allow_html=True)
    
    # Description
    st.markdown(f"**目標：** {description}")
    
    # Encryption samples table
    st.markdown(create_crypto_table(samples), unsafe_allow_html=True)
    
    # Question
    st.markdown(f"**題目：** `{question}`")
    
    # Check if level is already passed
    level_passed_key = f'level_{level_num}_passed'
    
    if st.session_state.get(level_passed_key, False):
        st.markdown(f'<div class="success-message">Level {level_num} 已通過！</div>', unsafe_allow_html=True)
        st.text_input("答案", value=correct_answer, disabled=True, key=f"input_{level_num}_disabled")
    else:
        # Input field
        user_input = st.text_input("請在此輸入解碼後的答案...", key=f"input_{level_num}")
        
        # Submit button
        if st.button("送出", key=f"submit_{level_num}"):
            if user_input == correct_answer:
                st.session_state[level_passed_key] = True
                add_score()
                st.success(f"Level {level_num} 已通過！")
                st.rerun()
            else:
                st.error("答案不正確，請再試一次！")
    
    # Navigation buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if level_num > 1:
            if st.button("⟨ 上一關"):
                st.session_state.current_page = f'level_{level_num - 1}'
                st.rerun()
    
    with col2:
        if level_num < 3:
            if st.button("下一關 ⟩"):
                st.session_state.current_page = f'level_{level_num + 1}'
                st.rerun()
    
    with col3:
        if st.button("🏠 回到開始"):
            st.session_state.current_page = 'start'
            st.rerun()
    
    with col4:
        if st.button("📊 結算", type="secondary"):
            st.session_state.current_page = 'end'
            st.rerun()

def end_page():
    st.markdown('<h1 class="main-header">🎯 挑戰結果</h1>', unsafe_allow_html=True)
    
    if st.session_state.scores == 3:
        st.markdown("## 🎉 恭喜通過所有關卡！")
        st.balloons()
        st.success("你成功破解了所有的加密謎題！")
    else:
        st.markdown("## 💪 繼續加油！")
        st.info("還有關卡等待你的挑戰！")
    
    st.markdown(f'<div class="end-page-score">最終分數：{st.session_state.scores} / 3</div>', unsafe_allow_html=True)
    
    # Show level status
    st.markdown("### 關卡狀態")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status = "✅ 已通過" if st.session_state.level_1_passed else "❌ 未通過"
        st.markdown(f"**Level 1:** {status}")
    
    with col2:
        status = "✅ 已通過" if st.session_state.level_2_passed else "❌ 未通過"
        st.markdown(f"**Level 2:** {status}")
    
    with col3:
        status = "✅ 已通過" if st.session_state.level_3_passed else "❌ 未通過"
        st.markdown(f"**Level 3:** {status}")
    
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 重新開始", use_container_width=True):
            # Reset all progress
            st.session_state.scores = 0
            st.session_state.level_1_passed = False
            st.session_state.level_2_passed = False
            st.session_state.level_3_passed = False
            st.session_state.current_page = 'start'
            st.rerun()
    
    with col2:
        if st.button("🏠 返回開始頁面", use_container_width=True):
            st.session_state.current_page = 'start'
            st.rerun()

# Main app logic
def main():
    if st.session_state.current_page == 'start':
        start_page()
    
    elif st.session_state.current_page == 'level_1':
        level_page(
            1,
            "觀察模式，推理加密邏輯，還原一組密碼，並將密碼輸入到輸入框內。(字母皆為小寫且空格和標點符號在加密前與加密後相同)",
            [("apple", "dssoh"), ("hello1", "khoor2"), ("openai8", "rshqdl9"), ("cat123", "fdw234"), ("hi", "kl")],
            "zhofrph wr 229fvlh lq qxn!",
            "welcome to 118csie in nuk!"
        )
    
    elif st.session_state.current_page == 'level_2':
        level_page(
            2,
            "觀察模式，推理加密邏輯，還原一組密碼，並將密碼輸入到輸入框內。(字母皆為小寫)",
            [("cfa22k5j2ve", "ev2j5k22afc"), ("hdfknfj94h", "h49jfnkfdh"), ("bfui4fddx", "xddf4iufb"), 
             ("oejhfo4hfj", "jfh4ofhjeo"), ("lslslslslsl", "lslslslslsl")],
            "dlrowollehhtiwtrats",
            "startwithhelloworld"
        )
    
    elif st.session_state.current_page == 'level_3':
        level_page(
            3,
            "結合前２關的模式，推理加密邏輯，還原一組密碼，並將密碼輸入到輸入框內。(字母皆為小寫)",
            [("a1dven14ture", "gtwv63pgxf3c"), ("pr1ogr1amm8er", "tg0ooc3tiq3tr"), ("algorithm", "ojvktqinc"), 
             ("alp2h0a1b5et", "vg7d3c2j4rnc"), ("6june20", "24gpwl8")],
            "pcykcvpkgfco",
            "madeintaiwan"
        )
    
    elif st.session_state.current_page == 'end':
        end_page()

# Add sidebar for debugging/navigation (optional)
with st.sidebar:
    st.markdown("### 🎮 快速導航")
    if st.button("開始頁面"):
        st.session_state.current_page = 'start'
        st.rerun()
    if st.button("Level 1"):
        st.session_state.current_page = 'level_1'
        st.rerun()
    if st.button("Level 2"):
        st.session_state.current_page = 'level_2'
        st.rerun()
    if st.button("Level 3"):
        st.session_state.current_page = 'level_3'
        st.rerun()
    if st.button("結果頁面"):
        st.session_state.current_page = 'end'
        st.rerun()
    
    st.markdown("---")
    st.markdown(f"**當前分數：** {st.session_state.scores}/3")
    
    # Debug info
    with st.expander("除錯資訊"):
        st.write("Current page:", st.session_state.current_page)
        st.write("Scores:", st.session_state.scores)
        st.write("Level 1 passed:", st.session_state.level_1_passed)
        st.write("Level 2 passed:", st.session_state.level_2_passed)
        st.write("Level 3 passed:", st.session_state.level_3_passed)

if __name__ == "__main__":
    main()
