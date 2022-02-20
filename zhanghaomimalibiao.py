import lianjieshujuku

def zhmmlist():
    sql = 'select username,userpwd from user'
    user_data = lianjieshujuku.shujuku(sql=sql)
    username_list = [i['username'] for i in user_data]
    userpwd_list=[i['userpwd'] for i in user_data]
    return username_list,userpwd_list

if __name__ == '__main__':
    print(zhmmlist())