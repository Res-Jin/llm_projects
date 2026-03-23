import streamlit as st

from llm.qwen_client import QwenClient
from llm.ollama_client import OllamaClient
from config import SYSTEM_PROMPT
from utils.chat_storage import save_chat, load_chat, list_chat_sessions

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

    if "selected_session" not in st.session_state:
        st.session_state.selected_session = None

def reset_chat():
    st.session_state.messages = [
        {"role": "system", "content": st.session_state.system_prompt}
    ]
    st.session_state.current_session_filename = None

def get_chat_messages():
    return st.session_state.messages[1:]

def save_current_chat(save_filename: str | None = None):
    saved_path = save_chat(
        messages=st.session_state.messages,
        backend=st.session_state.backend,
        system_prompt=st.session_state.system_prompt,
        filename=save_filename if save_filename else st.session_state.current_session_filename,
    )
    st.session_state.current_session_filename = saved_path.split("\\")[-1].split("/")[-1]
    return saved_path

def load_selected_chat(filename: str):
    data = load_chat(filename)
    st.session_state.backend = data["backend"]
    st.session_state.system_prompt = data["system_prompt"]
    st.session_state.messages = data["messages"]
    st.session_state.current_session_filename = filename
    st.session_state.selected_session = filename

init_session_state()

st.title("🤖 Dual Chat Assistant")
st.caption("第六轮：Web UI 升级版")

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

    st.subheader("会话管理")

    sessions = list_chat_sessions()
    selected_session = st.selectbox(
        "历史会话",
        options=[""] + sessions,
        index=0 if not st.session_state.selected_session or st.session_state.selected_session not in sessions
        else ([""] + sessions).index(st.session_state.selected_session)
    )

    col3, col4 = st.columns(2)

    with col3:
        if st.button("加载会话"):
            if selected_session:
                try:
                    load_selected_chat(selected_session)
                    st.success(f"已加载：{selected_session}")
                    st.rerun()
                except Exception as e:
                    st.error(f"加载失败：{e}")

    with col4:
        if st.button("另存为"):
            try:
                saved_path = save_current_chat()
                st.success(f"已保存：{saved_path}")
            except Exception as e:
                st.error(f"保存失败：{e}")

    save_filename = st.text_input("保存文件名（可选）", value="")

    if st.button("保存当前会话"):
        try:
            saved_path = save_current_chat(save_filename.strip() if save_filename.strip() else None)
            st.success(f"已保存：{saved_path}")
        except Exception as e:
            st.error(f"保存失败：{e}")

    st.divider()
    st.write(f"当前后端：`{st.session_state.backend}`")
    st.write(f"当前消息数：`{len(st.session_state.messages)}`")
    st.write(f"当前会话：`{st.session_state.current_session_filename or '未保存'}`")


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

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_reply = ""

            reply = client.chat(st.session_state.messages)

            for char in reply:
                full_reply += char
                placeholder.markdown(full_reply)

        st.session_state.messages.append({"role": "assistant", "content": full_reply})

    except Exception as e:
        st.error(f"请求失败：{e}")