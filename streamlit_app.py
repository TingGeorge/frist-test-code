import streamlit as st
import time

# Decryption logic (+3 letters, +1 number reverse)
def decrypt(cipher_text: str) -> str:
    result = []
    for ch in cipher_text:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            result.append(chr((ord(ch) - ord(base) - 3) % 26 + ord(base)))
        elif ch.isdigit():
            result.append(str((int(ch) - 1) % 10))
        else:
            result.append(ch)
    return ''.join(result)

# Correct answer
CORRECT_ANSWER = decrypt("zhofrph wr 229fvlh lq qxn!")

# Page config
st.set_page_config(page_title="黑箱解碼者", page_icon="🔓", layout="centered")

st.title("黑箱解碼者")

st.markdown(
    "目標：觀察模式，推理加密邏輯，還原一組密碼，並將密碼輸入到輸入框內。  \
    (字母皆為小寫且空格和標點符號在加密前與加密後相同)"
)

# Sample table
samples = [
    ("apple", "dssoh"),
    ("hello1", "khoor2"),
    ("openai8", "rshqdl9"),
    ("cat123", "fdw234"),
    ("hi", "kl"),
]
st.subheader("範例：輸入字串 vs 加密結果")
st.table({"輸入字串": [s[0] for s in samples], "加密結果": [s[1] for s in samples]})

# Puzzle prompt
st.subheader("題目：zhofrph wr 229fvlh lq qxn!")

# Initialize timer in session_state
def init_timer():
    st.session_state.start_time = time.perf_counter()
    st.session_state.started = True

if 'started' not in st.session_state:
    st.session_state.started = False

# Input field
user_input = st.text_input("輸入解碼結果：")

# Left-aligned buttons
col1, col2, _ = st.columns([1, 1, 4])
with col1:
    if st.button("計時"):
        init_timer()
        st.success("計時已開始，請開始解碼！")
with col2:
    if st.button("送出"):
        if not st.session_state.started:
            st.warning("請先按下「計時」按鈕開始計時。")
        elif not user_input:
            st.warning("請先輸入解碼結果。")
        else:
            if user_input.strip() == CORRECT_ANSWER:
                end_time = time.perf_counter()
                elapsed = int(end_time - st.session_state.start_time)
                minutes, seconds = divmod(elapsed, 60)
                if minutes > 0:
                    st.success(f"恭喜闖關成功！\n{CORRECT_ANSWER}\n解題花費的時間：{minutes}分{seconds}秒")
                else:
                    st.success(f"恭喜闖關成功！\n{CORRECT_ANSWER}\n解題花費的時間：{seconds}秒")
                st.session_state.started = False
            else:
                st.error("答案不正確，請再試一次。")
