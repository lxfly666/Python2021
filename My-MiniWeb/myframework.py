import time
import pymysql
import json
import logging

route_list = []

def route(path):
    def decorator(func):
        route_list.append((path, func))
        def inner():
            result = func()
            return result
        return inner
    return decorator


@route("/index.html")
def index():
    status = "200 OK"
    # 响应头信息
    response_header = [("Server", "PWS/1.1")]
    # web框架处理后的数据
    # 获取当前时间
    with open("template/index.html", "r", encoding='utf-8') as file:
        file_date = file.read()

    conn = pymysql.connect(host="localhost",
                            port=3306,
                            user="root",
                            password="root",
                            database="stock_db",
                            charset="utf8")

    cursor = conn.cursor()
    sql = "select * from info;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    conn.close()

    data = ""
    for row in result:
        data += """<tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000007"></td>
        </tr>""" % row
    response_body = file_date.replace("{%content%}", data)
    return status, response_header, response_body

@route("/center.html")
def center():
    status = "200 OK"
    response_header = [("Server", "PWS/1.1")]
    with open("template/center.html", "r", encoding='utf-8') as file:
       file_data = file.read()

    data = time.ctime()
    response_body = file_data.replace("{%content%}", data)
    print(response_body)
    return status, response_header, response_body

@route("/center_data.html")
def center_data():
    conn = pymysql.connect(host="localhost",
                           port=3306,
                           user="root",
                           password="root",
                           database="stock_db",
                           charset="utf8")
    cursor = conn.cursor()
    sql = '''select i.code, i.short, i.chg, i.turnover, i.price, i.highs, f.note_info 
             from info i inner join focus f 
             on i.id = f.info_id;'''

    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)

    center_data_list = [{
        "code": row[0],
        "short": row[1],
        "chg": row[2],
        "turnover": row[3],
        "price": str((row[4])),
        "highs": str(row[5]),
        "note_info": row[6]
    } for row in result]

    json_str = json.dumps(center_data_list, ensure_ascii=False)

    cursor.close()
    conn.close()
    status = "200 OK"
    response_header = [("Server", "PWS/1.1"),
                       ("Content-Type", "text/html;charset=utf-8")]
    return status, response_header, json_str

def not_found():
    # 状态信息
    status = "404 Not Found"
    # 响应头信息
    response_header = [("Server", "PWS/1.1")]
    # web框架处理后的数据
    data = "not found"

    # 这里返回的是元组
    return status, response_header, data


def handle_request(env):
    # return ("200 OK",[("name","lxfly")],"xxxxyyyyzzzz")
    request_path = env["request_path"]
    for path, func in route_list:
        if request_path == path:
            result = func()
            return result
    else:
        result = not_found()
        logging.error("没有设置相关的路由信息:" + request_path)
        return result


if __name__ == '__main__':
    print(route_list)


