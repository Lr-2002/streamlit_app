import streamlit as st
import datetime
import numpy as np
import pandas as pd
login = False

def read_login():
    with open('./ppp.txt', 'r') as f:
        login = f.read()

        login = bool(int(login))
        print(login)
        return login

def write_login(login):
    with open('./ppp.txt','w') as f:
        f.write(str(int(login)))
        print('wirted')


def logined(F):
    if login:
        print('您已经登录')
        return F()
    else:
        print('您还没有登录，请先进行登录')

def add_one_row(df):
    # input the df
    # output changed df
    # show the add button

    col1, col2 = st.columns(2)
    with col1:
        upload = st.button('上传文件')
    with col2:
        hand_input = st.button('手动输入')
    if upload:
        file = st.file_uploader('上传你的文件')
        cirtify = st.button('点击确认')
        print(file)
        if file is not None and cirtify:
            data = pd.read_csv(file)
            st.write(data)
    elif hand_input:
        for i in df.keys():
            st.text_input(i)

    else:
        pass
    # pass


# def logined(login):
#     def Outer(F):
#         def inner():
#             if login:
#                 print('您还没有登录，请先登录')
#             else:
#                 print('登录成功')
#             return inner
#     return Outer

# def read_csv(filename):
#     map_header = ['序号', '日期', '班组', '物资编码', '物资名称', '规格型号/图号/材质', '计量单位', '单价', '数量',
#        '金额', '科目编号', '科目名称']
#     map_type = [np.int64, datetime, str, np.int64, str, str, str, np.float64, np.int64, np.int64, str, str]
#     dic = {map_header[i]: map_type[i] for i in range(len(map_type))}
#     df = pd.read_csv(filename, encoding='gbk')
#     df_k = df.keys()
#
#     print(df.dtypes)
#     for i in range(len(df_k)):
#         df[[map_header[i]]] = df[[map_header[i]]].astype(dic[map_header[i]])
#     print(df.dtypes)

def search_resource(resource):
    search = input('输入你要搜搜的东西')
    lie = resource.shape[1]
    # search = st.text_input('输入你要搜索的东西')
    answer = pd.DataFrame()
    if search == None:
        print('no resource')
        answer = resource
        return answer
    else:
        counter = 0
        for i in range(len(resource['物资名称'])):
            print(resource['物资名称'][i])
            if search in str(resource['物资名称'][i]):
                # print(i)
                answer[str(counter)] = resource[i:i+1]

        answer.head()




def act():
    show()


def login_page(name, sn):
    user = st.text_input('请输入您的账号')
    number = st.text_input('请输入您的密码')
    # print(user, name, number, sn)
    if str(user) == str(name) and str(number) == str(sn):
        login=True
        st.balloons()
        print('you have logined')
        write_login(1)
        # act()
    else:
        login = False
        print('your number is wrong')



def show():
    # st.title()
    full = pd.read_csv('./full.csv', encoding='gbk').fillna(0)
    total = pd.read_csv('./total.csv', encoding='gbk').fillna(' ')
    resource = pd.read_csv('resource.csv', encoding='gbk').fillna(0)
    st.title('')

    st.subheader('台面账')
    st.dataframe(total)

    st.subheader('写实账')
    st.dataframe(full)

    st.subheader('资源表')
    st.dataframe(resource)
    add_one_row(resource)
if __name__ == '__main__':
    # choice = ['登录', '首页']
    # # st.sidebar()

    user = pd.read_csv('./admin.csv').to_numpy()
    print(user)
    name = user[0][0]
    sc = user[0][1]
    print(name, sc)
    login = read_login()
    if not login:
        login_page(name, sc)

    if login:
        show()


