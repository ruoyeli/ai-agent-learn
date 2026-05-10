import streamlit as st
from openai import OpenAI
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
st.title("AI智能伴侣")

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
    api_key="sk-330a51f858774bac998fa0c7fa84eb55",
    base_url="https://api.deepseek.com"
)
with st.sidebar:
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