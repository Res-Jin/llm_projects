import streamlit as st
from llm.qwen_client import QwenClient
from llm.ollama_client import OllamaClient
from config import SYSTEM_PROMPT
from utils.chat_storage import save_chat

st.set_page_config(page_title="Dual Caht Assistent", page_icon="🤖", layout="wide")

def build_client(backend: str):
    if backend == "qwen":
        return QwenClient()
    elif backend == "ollama":
        return OllamaClient()
    else:
        raise ValueError("未知后端")
    
def init_session_state():
    if "backend" not in st.session_state:
        st.session_state.backend = "qwen"

    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = SYSTEM_PROMPT

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": st.session_state.system_prompt}
        ]

    if "current_session_filename" not in st.session_state:
        st.session_state.current_session_filename = None

def reset_chat():
    st.session_state.messages = [
        {"role": "system", "content": st.session_state.system_prompt}
    ]

def get_chat_messages():
    return st.session_state.messages[1:]

init_session_state()

st.title("🤖 Dual Chat Assistant")
st.caption("第五轮：Streamlit 网页版")

with st.sidebar:
    st.header("配置")

    backend = st.selectbox(
        "选择后端",
        options=["qwen", "ollama"],
        index=0 if st.session_state.backend == "qwen" else 1,
    )
    st.session_state.backend = backend

    new_system_prompt = st.text_area(
        "System Prompt",
        value=st.session_state.system_prompt,
        height=120
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("更新 Prompt"):
            st.session_state.system_prompt = new_system_prompt
            reset_chat()
            st.success("System Prompt 已更新，并已重置上下文。")

    with col2:
        if st.button("清空对话"):
            reset_chat()
            st.success("上下文已清空。")

    st.divider()

    save_filename = st.text_input("保存文件名（可选）", value="")

    if st.button("保存当前会话"):
        try:
            saved_path = save_chat(
                messages=st.session_state.messages,
                backend=st.session_state.backend,
                system_prompt=st.session_state.system_prompt,
                filename=save_filename if save_filename.strip() else None
            )
            st.session_state.current_session_filename = saved_path.split("\\")[-1].split("/")[-1]
            st.success(f"已保存：{saved_path}")
        except Exception as e:
            st.error(f"保存失败：{e}")

    st.divider()
    st.write(f"当前后端：`{st.session_state.backend}`")
    st.write(f"当前消息数：`{len(st.session_state.messages)}`")


for msg in get_chat_messages():
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("请输入你的消息")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        client = build_client(st.session_state.backend)
        reply = client.chat(st.session_state.messages)

        st.session_state.messages.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.markdown(reply)

    except Exception as e:
        st.error(f"请求失败：{e}")