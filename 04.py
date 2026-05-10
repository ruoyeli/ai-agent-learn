import os.path
import json
import streamlit as st
from openai import OpenAI
from datetime import datetime

# 设置页面的配置项

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="📖",
    # 布局
    layout="wide",
    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={
    }
)
# 定义一个函数保存会话信息
def save_session():
        if st.session_state.current_session:
            session_data = {
                "nick_name" :st.session_state.nick_name,
                "nature" : st.session_state.nature,
                "message" : st.session_state.messages,
                "current_session" : st.session_state.current_session
            }
            #如果文件不存在，则创建
            if not os.path.exists("session"):
                os.makedirs("session")
    #         保存会话信息
            with open(f"session/{st.session_state.current_session}.json","w",encoding = "utf-8") as f:
                json.dump(session_data,f,ensure_ascii=False,indent=2)
#生成会话的标识（时间标识）
# 加载所有会话
def load_sessions():
    session_list = []
    if os.path.exists("session"):
        file_list = os.listdir("session")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)
    return session_list
def load_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            with open(f"session/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["message"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception as e:
        st.error(f"加载会话失败!",{e})
#  删除会话功能实现
def delete_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            os.remove(f"session/{session_name}.json")
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception as e:
        st.error(f"删除会话失败!,{e}")


def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# 初始化 session_state
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "李若叶"
if "nature" not in st.session_state:
    st.session_state.nature = "活泼可爱的南方姑娘"
st.title("AI智能聊天")


st.logo(r"C:\Users\DELL\Desktop\yi.jpg")

system_prompt = """
        你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色。
        规则：
        .每次只回1条消息
        .禁止任何场景或状态描述性文字
        你必须严格遵守上述规则来回复用户
        .匹配用户的语言
        .回复简短，像微信聊天一样
        .有需要的话可以用等emoji表情
        .伴侣性格：%s
        """
if "messages" not in st.session_state:
    st.session_state.messages = []

if "nick_name" not in st.session_state:
    st.session_state.nick_name = "李若叶"

if "nature" not in st.session_state:
    st.session_state.nature = "活泼可爱的南方姑娘"
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
with st.sidebar:
    st.subheader("会话控制面板")
    if st.button("新建会话",width = "stretch",icon="🖊"):

        #创建新的会话：
        st.session_state.messages = []
        st.session_state.current_session = generate_session_name()
        save_session()
        st.rerun()
    # 会话历史
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1,col2 = st.columns([4,1])
        with col1:
            if st.button(session,width="stretch",icon="🤪",key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            if st.button("",width="stretch",icon="✖",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()


    st.divider()
    st.subheader("伴侣信息")
    nick_name = st.text_input("昵称",placeholder="请输入你的昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name

    nature = st.text_input("伴侣性格",placeholder="请输入伴侣性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature


prompt = st.chat_input("请输入你想咨询的问题")
if prompt:
    st.chat_message("user").write(prompt)
    print("------->调用AI大模型，提示词：", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content":system_prompt %(st.session_state.nick_name,st.session_state.nature)},
                *st.session_state.messages,
            ],
            stream=True,
        )
    #非流式输出
    # print("<--------大模型返回的结果：", response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    response_message = st.empty()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response +=  content
            response_message.chat_message("assistant").write(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_session()