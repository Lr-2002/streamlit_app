import streamlit as st
import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import numpy as np
import chardet
import pandas as pd
login = False
session_state = st.session_state

def get_encoding(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read(1))['encoding']


# session_state['upload'] = False
# session_state['hand_input'] = False
def read_login():
    with open('./ppp.txt', 'r') as f:
        login = f.read()

        login = bool(int(login))
        print(login)
        return login

def update_total(full, total):
    ## todo 修改比例计算
    cate = full['科目名称'].unique()

    for i in range(total.shape[0]):
        # print(i)
        for j in cate:
            name = total.at[i, '班组']
            print(j)
            # print(full['班组'] == name )
            # print(full['科目名称'] == j)
            money = full[(full['班组'] == name) & (full['科目名称'] == j)]['金额'].sum()
            # total[(total['班组'] == name)][j + '成本消耗'] = money
            total.at[i, j + '成本消耗'] = money
    for i in total.keys():
        if '成本' in i:
            total.at[total.shape[0] - 1, i] = total[i].sum()

    for i in cate:
        source = i + '总成本'
        cost = i + '成本消耗'
        rate = i + '成本消耗比例'
        total[rate] = total[cost] / total[source]

    return total

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

def change_type(df1:pd.DataFrame, df2 :dict):
    # todo 为什么会增加unamed？
    df2 = pd.DataFrame.from_dict(df2)
    for i in df2.keys():
        df2[i] =df2[i].astype(df1[i].dtypes)

    add_list = [df1, df2]
    df = pd.concat(add_list)
    return df


@st.cache
def upload_file():
    file = st.file_uploader('上传你的文件')
    cirtify = st.button('点击确认')
    print(file)
    if file is not None and cirtify:
        data = pd.read_csv(file)
        st.write(data)

@st.cache
def convert_df(df):
    return df.to_csv().encode('gbk')

def name_and_download(text, data, filename):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(text)
    # with col2:
    #     csv = convert_df(data)
    #     st.download_button('下载该文件', data=csv, file_name=filename, mime='text/csv')

# @st.cache

def search_name_resource(key, resource):
    # key = '电动三轮车'
    # st.title(key)
    # key = '不锈钢'
    x = resource[resource['物资名称'] == key]
    z = x.set_index('物资名称').to_dict()
    ans = {}

    for i in z.keys():
        # print(z[i])
        if z[i] != {}:
            ans[i] = [str(z[i][key])]
        else:
            # st.text('没有搜索到当前商品，请手动输入')
            return False, ans
    # st.write(ans)
    return True, ans


def search_name_in_resource(key, resource):

    # print(resource['物资名称'].str.contains(key))
    x = resource.loc[resource['物资名称'].str.contains(key)]
    res = x.empty
    return res, x



    # st.title('输入：'+key)
    # x = resource[resource['物资名称'] == key]
    # z = x.set_index('物资名称').to_dict()
    # ans = {}
    # for i in z.keys():
    #     ans[i] = [str(z[i][key])]
    # return ans




def add_one_row(df, filename,upload_key, hand_input_key,resource = None):
    # input the df
    # output changed df
    # show the add button

    col1, col2 = st.columns(2)
    with col1:
        upload = st.button('上传文件', key=upload_key)
        if upload:
            session_state['upload'] = True
    with col2:
        hand_input = st.button('手动输入', key=hand_input_key)
        if hand_input:
            session_state['hand_input'] = True
    if  'upload' in session_state.keys():
        if session_state['upload']:
            file = st.file_uploader('上传你的文件')
            cirtify = st.button('点击确认')
            if file is not None and cirtify:
                st.text('您上传的文件内容如下')
                data = pd.read_csv(file)
                st.write(data)
                print('session_state:', session_state)
    if 'hand_input' in session_state.keys():
        if  session_state['hand_input']:
            st.text('hand input')
            if 'hand_input_dict' in session_state.keys():
                hand_input_dict = session_state['hand_input_dict']
            else:
                hand_input_dict = {}
                for i in df.keys():
                    hand_input_dict[i] = ['']
            end_func = ''
            # print(hand_input_dict)
            for i in df.keys():
                # if i in
                # hand_input_dict[i] = ['']
                hand_input_dict[i] = [st.text_input(i, value=hand_input_dict[i][0])]
                if '物资名称' in  hand_input_dict.keys() and hand_input_dict['物资名称'] != [''] and resource is not None :
                    gotit, return_dict = search_name_resource(hand_input_dict['物资名称'][0], resource)
                    if gotit:
                        for j in return_dict.keys():
                            hand_input_dict[j] = return_dict[j]
                end_func =i
            if hand_input_dict[end_func] != '':
                certi = st.button('确认提交')

                if certi:
                    st.success('已经成功提交')
                    # st.write(hand_input_dict)
                    df = change_type(df, hand_input_dict)
                    df.to_csv(filename, encoding='gbk')
                    session_state['hand_input'] = False
            session_state['hand_input_dict'] = hand_input_dict
            print(hand_input_dict)



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

# def search_resource(resource):
#     search = input('输入你要搜搜的东西')
#     lie = resource.shape[1]
#     # search = st.text_input('输入你要搜索的东西')
#     answer = pd.DataFrame()
#     if search == None:
#         print('no resource')
#         answer = resource
#         return answer
#     else:
#         counter = 0
#         for i in range(len(resource['物资名称'])):
#             print(resource['物资名称'][i])
#             if search in str(resource['物资名称'][i]):
#                 # print(i)
#                 answer[str(counter)] = resource[i:i+1]
#
#         answer.head()




def act():
    show()


def login_page(name, sn):
    user = st.text_input('请输入您的账号')
    number = st.text_input('请输入您的密码')
    # print(user, name, number, sn)
    if str(user) == str(name) and str(number) == str(sn) and st.button('确认登录'):
        login=True
        st.balloons()
        print('you have logined')
        session_state['logined'] = True
        # act()
    else:
        login = False
        print('your number is wrong')

# def name_and_update(text, data, filename):
#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader(text)
#     with col2:
#         csv = convert_df(data)
#         st.download_button('下载该文件', data=csv, file_name=filename, mime='text/csv')


def show():
    # st.title()
    full = pd.read_csv('./full.csv', encoding='gbk').fillna(0)
    total = pd.read_csv('./total.csv', encoding='gbk').fillna(' ')
    resource = pd.read_csv('resource.csv', encoding='gbk').fillna(0)
    st.title('')

    # st.subheader('台面账')
    # two_column()
    total = update_total(full, total)
    name_and_download('台账',total, 'total.csv')
    # add_row = st.button('增加一行')
    #
    # if add_row:
    #     add_dict = {}
    #     for i in total.keys():
    #         # todo 新加一行空
    #         add_dict[i] = 0
    #     total = change_type(total, add_dict)
        # pd.concat([total, pd.DataFrame([np.NaN] *  total.shape[0], columns = total.columns)])
    gb = GridOptionsBuilder.from_dataframe(total)
    cells_jscode = JsCode(
        """
        
function(params) {
    if (params.value > 0.9) {
        return {
            'color': 'white',
            'backgroundColor': 'red'
        }
    }else if(params.value > 0.7)
    {
        return{
            'color' : 'black',
            'backgroundColor': 'yellow'
            }    
    } else if (params.value > 0.5)
    {   
        return{
            'color' : 'white',
            'backgroundColor': 'green'
            }       
    }
    else {
        return {
            'color': 'black',
            'backgroundColor': 'white'
        }
    }
};
        """
    )
    total = total.round(2)
    for i in total.keys():
        if '成本消耗比例' in i:
            gb.configure_column(i, cellStyle= cells_jscode)
        elif '总成本' in i:
            gb.configure_column(i, editable=True)
    gridOptions = gb.build()
    data = AgGrid(
        total,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        # editable=True
    )

    # st.subheader('写实账')
    ge = GridOptionsBuilder.from_dataframe(full)
    # gg.configure_side_bar()

    ge.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    ge = ge.build()
    name_and_download('写实账', full, 'full.csv')
    # st.dataframe(full)
    AgGrid(
        pd.DataFrame(full, columns=full.columns),
        # fit_columns_on_grid_load=True,
        gridOptions=ge,
        height=500,
        enable_enterprise_modules=True
    )
    # add_one_row(full, './full.csv','full_upload', 'full_hand_input', resource)
    # todo 暂时粘贴过来
    df = full
    filename = './full.csv'
    col11, col21 = st.columns(2)
    with col11:
        upload = st.button('上传文件')
        if upload:
            session_state['full_upload'] = True
    with col21:
        hand_input = st.button('手动输入')
        if hand_input:
            session_state['full_hand_input'] = True
    if 'full_upload' in session_state.keys():
        if session_state['full_upload']:
            file = st.file_uploader('上传你的文件')
            cirtify = st.button('点击确认')
            if file is not None and cirtify:
                st.text('您上传的文件内容如下')
                data = pd.read_csv(file)
                st.write(data)
                print('session_state:', session_state)
    if 'full_hand_input' in session_state.keys():
        if session_state['full_hand_input']:
            st.text('hand input')
            if 'full_hand_input_dict' in session_state.keys():
                hand_input_dict = session_state['full_hand_input_dict']
            else:
                hand_input_dict = {}
                for i in df.keys():
                    hand_input_dict[i] = ['']
            end_func = ''
            # print(hand_input_dict)
            gotit = False
            for i in df.keys():
                # if i in
                # hand_input_dict[i] = ['']
                hand_input_dict[i] = [st.text_input(i, value=hand_input_dict[i][0])]
                if '物资名称' in hand_input_dict.keys() and hand_input_dict['物资名称'] != [''] and resource is not None:
                    gotit, return_dict = search_name_resource(hand_input_dict['物资名称'][0], resource)
                    if gotit:
                        for j in return_dict.keys():
                            hand_input_dict[j] = return_dict[j]
                    # else:
                    #     st.text('没有搜索到当前产品，请手动输入')
                end_func = i
            if not gotit:
                st.text('没有搜索到当前产品，请手动输入')
            if hand_input_dict[end_func] != '':
                certi = st.button('确认提交')

                if certi:
                    st.success('已经成功提交')
                    # st.write(hand_input_dict)
                    df = change_type(df, hand_input_dict)
                    df.to_csv(filename, encoding='gbk', index=False)
                    session_state['full_hand_input'] = False
            session_state['full_hand_input_dict'] = hand_input_dict
            print(hand_input_dict)

    # todo 暂时结束








    # st.subheader('资源表')
    name_and_download('资源表', resource, 'resource.csv')

    search = st.text_input('搜索一下')
    if search:
        res, x = search_name_in_resource(search, resource)
        if not res:
            st.dataframe(x)
        else:
            st.warning('没有相关产品')




    # st.dataframe(resource)
    gg = GridOptionsBuilder.from_dataframe(resource)
    # gg.configure_side_bar()

    gg.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    grid = gg.build()
    grid_edited = AgGrid(
        pd.DataFrame(resource, columns=resource.columns),
        width= '100%',
        gridOptions=grid,
        # editable=True,
    )
    # todo 暂时粘贴过来
    df = resource
    filename = './resource.csv'
    col1, col2 = st.columns(2)
    with col1:
        upload = st.button('上传材料表格')
        if upload:
            session_state['upload'] = True
    with col2:
        hand_input = st.button('手动输入材料')
        if hand_input:
            session_state['rs_hand_input'] = True
    if 'rs_upload' in session_state.keys():
        if session_state['rs_upload']:
            file = st.file_uploader('上传你的文件')
            cirtify = st.button('点击确认')
            if file is not None and cirtify:
                st.text('您上传的文件内容如下')
                data = pd.read_csv(file)
                st.write(data)
                print('session_state:', session_state)
    if 'rs_hand_input' in session_state.keys():
        if session_state['hand_input']:
            st.text('rs_hand input')
            if 'rs_hand_input_dict' in session_state.keys():
                hand_input_dict = session_state['rs_hand_input_dict']
            else:
                hand_input_dict = {}
                for i in df.keys():
                    hand_input_dict[i] = ['']
            end_func = ''
            # print(hand_input_dict)
            for i in df.keys():
                # if i in
                # hand_input_dict[i] = ['']
                hand_input_dict[i] = [st.text_input(i, value=hand_input_dict[i][0])]
                if '物资名称' in hand_input_dict.keys() and hand_input_dict['物资名称'] != [''] and resource is not None:
                    gotit, return_dict = search_name_resource(hand_input_dict['物资名称'][0], resource)
                    if gotit:
                        for j in return_dict.keys():
                            hand_input_dict[j] = return_dict[j]
                end_func = i
            if hand_input_dict[end_func] != '':
                certi = st.button('确认提交')

                if certi:
                    st.success('已经成功提交')
                    # st.write(hand_input_dict)
                    df = change_type(df, hand_input_dict)
                    df.to_csv(filename, encoding='gbk', index=False)
                    session_state['rs_hand_input'] = False
            session_state['rs_hand_input_dict'] = hand_input_dict
            print(hand_input_dict)

    # todo 暂时结束



    # add_one_row(resource, './resource.csv', 'rs_upload', 'rs_hand_input')
if __name__ == '__main__':
    # choice = ['登录', '首页']
    # # st.sidebar()
    if 'logined' not in session_state.keys():
        session_state['logined'] =False
    user = pd.read_csv('./admin.csv').to_numpy()
    # print(user)
    name = user[0][0]
    sc = user[0][1]
    # print(name, sc)
    # login = read_login()
    print(session_state['logined'])
    if not session_state['logined']:
        login_page(name, sc)

    if session_state['logined']:
        show()


