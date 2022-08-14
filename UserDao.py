# design by Yang liu
from typing import Dict

import pymysql

# 获取Connection对象，如果账号、密码、数据库名错误，则报错
# 若在您的机器上运行，请修改user,password,db(数据库名)
conn = pymysql.connect(host='localhost', user='root',
                       password='123456', charset='utf8', db='faceProject')

"""
-User表的建立代码如下

create table user
(
    user_no         int auto_increment
        primary key,
    user_account    varchar(30)          not null,
    user_password   varchar(20)          not null,
    user_name       varchar(20)          null,
    user_idCard     varchar(20)          null,
    user_authorized tinyint(1) default 0 not null,
    constraint user_table_user_account_u_index
        unique (user_account),
    constraint user_table_user_no_u_index
        unique (user_no)
);

"""
# 下列为用户一些信息，默认为None，登录后将自动更改
# 指明了数据类型，若乱输入则错误
_isLogin = False
_account: str = str(None)
_idcard: str = str(None)
_password: str = str(None)
_username: str = str(None)
_authorized: bool = False


def is_login():
    return bool(_isLogin)


def is_authorized():
    return bool(_authorized)


def register(account: str, password: str, username: str = None, idcard: str = None) -> bool:
    """
    用户注册
    :param account:账号
    :param password:密码
    :param username:姓名，可空
    :param idcard:身份账号，可空
    :return:返回是否添加成功
    """
    cursor = conn.cursor()
    sql = '''
        insert into user(user_account,user_password,user_name,user_idCard) 
        values (%s,%s,%s,%s)
    '''
    # 参数元组
    pas = (account, password, username, idcard)
    try:
        cursor.execute(sql, pas)
        cursor.close()
        conn.commit()
        return True
    except pymysql.err.Error:
        conn.rollback()
        return False


# result = register('root10', '123456', '杨柳', '123456')
# print(result)

def update_user_info(password: str = _password, username: str = _username,
                     idcard: str = _idcard) -> bool:
    """
    更新用户信息，账号为当前用户的信息，需要登录后才使用，不指定参数则不修改
    :param password:修改后的密码
    :param username:修改后的用户名
    :param idcard:修改后的身份证号
    :return:返回是否修改成功
    """
    # 判断是否登录，未登录则False
    if not is_login():
        return False

    cursor = conn.cursor()
    sql = '''
        UPDATE user 
            SET
            user_password =%s,user_name=%s,user_idCard=%s 
        WHERE  user_account=%s AND user_password = %s
    '''
    # 参数元组
    pas = (password, username, idcard, _account, _password)
    try:
        cursor.execute(sql, pas)
        cursor.close()
        conn.commit()
        login(_account, password)
        return True
    except pymysql.err.Error:
        conn.rollback()
        return False


def get_user_info() -> Dict[str, str]:
    """
    :return:返回一个字典，为当前登录用户的数据
        输出实例：{'account': 'root', 'password': '123456', 'username': None, 'idcard': None}
    """
    return {'account': _account, 'password': _password,
            'username': _username, 'idcard': _idcard}


def login(account: str, password: str) -> bool:
    """
    返回是否登录成功，若要获取用户信息，可使用get_user_info()方法
    """

    global _isLogin, _account, _password, _username, _idcard, _authorized

    cursor = conn.cursor()
    sql = '''
    SELECT user_account,user_password,
            user_name,user_idCard,user_authorized 
    FROM user 
    WHERE user_account= %s and user_password =%s
    '''
    # 参数元组
    par = (account, password)
    cursor.execute(sql, par)
    cursor.close()
    row = cursor.fetchone()
    if row:
        _isLogin = True
        _account, _password, _username, _idcard, _authorized = row
        return True
    return False


# print(login('root', 'root'))
# print(get_user_info())


def close_connection() -> None:
    """
    关闭数据库连接，程序结束前可调用此程序，一般没什么用，不调用也行
    """
    global conn
    conn.close()
