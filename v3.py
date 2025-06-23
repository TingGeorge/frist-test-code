import streamlit as st
from PIL import Image
import string

# Set page config
st.set_page_config(
    page_title="Black Box Decoder",
    page_icon="\ud83d\udd13",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- Styles ---------- #
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
</style>
""", unsafe_allow_html=True)

# ---------- Encrypt / Decrypt Logic ---------- #
def encrypt_level_1(plain_text):
    res = []
    for ch in plain_text:
        if 'a' <= ch <= 'z':
            res.append(chr((ord(ch) - ord('a') + 3) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            res.append(chr((ord(ch) - ord('A') + 3) % 26 + ord('A')))
        elif ch.isdigit():
            res.append(str((int(ch) + 1) % 10))
        else:
            res.append(ch)
    return ''.join(res)

def decrypt_level_1(cipher_text):
    res = []
    for ch in cipher_text:
        if 'a' <= ch <= 'z':
            res.append(chr((ord(ch) - ord('a') - 3) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            res.append(chr((ord(ch) - ord('A') - 3) % 26 + ord('A')))
        elif ch.isdigit():
            res.append(str((int(ch) - 1) % 10))
        else:
            res.append(ch)
    return ''.join(res)

def encrypt_level_2(plain_text):
    return plain_text[::-1]

def decrypt_level_2(cipher_text):
    return cipher_text[::-1]

def encrypt_level_3(plain_text):
    return encrypt_level_2(encrypt_level_1(plain_text))

def decrypt_level_3(cipher_text):
    return decrypt_level_1(decrypt_level_2(cipher_text))

# ---------- Level Configuration ---------- #
LEVEL_CONFIGS = {
    1: {
        "description": "觀察模式，推理加密邏輯，還原一組密碼...",
        "samples_plain": ["apple", "hello1", "openai8", "cat123", "hi"],
        "encrypt_func": encrypt_level_1,
        "decrypt_func": decrypt_level_1,
        "question_cipher": "zhofrph wr 229fvlh lq qxn!"
    },
    2: {
        "description": "觀察模式，推理加密邏輯...",
        "samples_plain": ["cfa22k5j2ve", "hdfknfj94h", "bfui4fddx", "oejhfo4hfj", "lslslslslsl"],
        "encrypt_func": encrypt_level_2,
        "decrypt_func": decrypt_level_2,
        "question_cipher": "dlrowollehhtiwtrats"
    },
    3: {
        "description": "結合前２關的模式...",
        "samples_plain": ["a1dven14ture", "pr1ogr1amm8er", "algorithm", "alp2h0a1b5et", "6june20"],
        "encrypt_func": encrypt_level_3,
        "decrypt_func": decrypt_level_3,
        "question_cipher": "pcykcvpkgfco"
    }
}

# ---------- Helper Functions ---------- #
def create_crypto_table(samples, encrypt_func):
    table_html = """
    <div class="crypto-table">
        <table>
            <tr><th>輸入字串</th><th>加密結果</th></tr>
    """
    for plain in samples:
        cipher = encrypt_func(plain)
        table_html += f"<tr><td>{plain}</td><td>{cipher}</td></tr>"
    table_html += "</table></div>"
    return table_html

def add_score():
    st.session_state.scores += 1

def show_score_sidebar():
    st.sidebar.markdown(f"## 分數: {st.session_state.scores} / 3")

# ---------- Pages ---------- #
def start_page():
    st.markdown('<h1 class="main-header">\ud83d\udd13 Black Box Decoder</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin: 50px 0;">
        <h2>歡迎來到黑盒解碼挑戰！</h2>
        <p>透過觀察加密模式，破解三個關卡的密碼謎題</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("\ud83d\ude80 開始挑戰"):
        st.session_state.current_page = 'level_1'
        st.experimental_rerun()

def level_page(level_num):
    show_score_sidebar()
    cfg = LEVEL_CONFIGS[level_num]
    st.markdown(f'<h2 class="level-header">Level {level_num}</h2>', unsafe_allow_html=True)
    st.markdown(f"**目標：** {cfg['description']}")
    st.markdown(create_crypto_table(cfg['samples_plain'], cfg['encrypt_func']), unsafe_allow_html=True)
    question = cfg['question_cipher']
    st.markdown(f"**題目：** `{question}`")
    correct_answer = cfg['decrypt_func'](question)
    level_key = f'level_{level_num}_passed'
    if st.session_state.get(level_key, False):
        st.markdown(f'<div class="success-message">Level {level_num} 已通過！</div>', unsafe_allow_html=True)
        st.text_input("答案", value=correct_answer, disabled=True)
    else:
        user_input = st.text_input("請在此輸入解碼後的答案...")
        if st.button("送出"):
            if user_input.strip() == correct_answer:
                st.session_state[level_key] = True
                add_score()
                st.success("答對了！")
                st.experimental_rerun()
            else:
                st.error("答案不正確，請再試一次！")
    cols = st.columns(4)
    if level_num > 1 and cols[0].button("⟨ 上一關"):
        st.session_state.current_page = f'level_{level_num - 1}'
        st.experimental_rerun()
    if level_num < 3 and cols[1].button("下一關 ⟩"):
        st.session_state.current_page = f'level_{level_num + 1}'
        st.experimental_rerun()
    if cols[2].button("\ud83c\udfe0 回到開始"):
        st.session_state.current_page = 'start'
        st.experimental_rerun()
    if cols[3].button("\ud83d\udcca 結算"):
        st.session_state.current_page = 'end'
        st.experimental_rerun()

def end_page():
    show_score_sidebar()
    st.markdown('<h1 class="main-header">\ud83c\udfaf 挑戰結果</h1>', unsafe_allow_html=True)
    score = st.session_state.scores
    if score == 3:
        st.balloons()
        st.success("\ud83c\udf89 恭喜通過所有關卡！")
    else:
        st.info("還有關卡等待你的挑戰！")
    st.markdown(f"### 最終分數：{score} / 3")
    cols = st.columns(3)
    for i in range(3):
        passed = st.session_state.get(f'level_{i+1}_passed', False)
        cols[i].markdown(f"**Level {i+1}:** {'✅' if passed else '❌'}")
    if st.button("🔄 重新開始"):
        st.session_state.scores = 0
        for i in range(1, 4):
            st.session_state[f'level_{i}_passed'] = False
        st.session_state.current_page = 'start'
        st.experimental_rerun()

# ---------- Main ---------- #
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'start'
if 'scores' not in st.session_state:
    st.session_state.scores = 0
for i in range(1, 4):
    st.session_state.setdefault(f'level_{i}_passed', False)

with st.sidebar:
    st.markdown("### 🎮 快速導航")
    for i in range(1, 4):
        if st.button(f"Level {i}"):
            st.session_state.current_page = f'level_{i}'
            st.experimental_rerun()
    if st.button("開始頁面"):
        st.session_state.current_page = 'start'
        st.experimental_rerun()
    if st.button("結果頁面"):
        st.session_state.current_page = 'end'
        st.experimental_rerun()

page = st.session_state.current_page
if page == 'start':
    start_page()
elif page == 'end':
    end_page()
elif page.startswith('level_'):
    level_num = int(page.split('_')[1])
    level_page(level_num)
