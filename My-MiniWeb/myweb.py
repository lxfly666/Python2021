import socket
import myframework
import threading
import logging
import sys

class HttpWebServer(object):

    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s-%(filename)s[lineno:%(lineno)d]-%(levelname)s-%(message)s",
                        filename="log.txt",
                        filemode="w")

    def __init__(self, port):
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        tcp_server_socket.bind(("", port))
        tcp_server_socket.listen(128)
        self.tcp_server_socket = tcp_server_socket

    def start(self):
        while True:
            new_socket, ip_port = self.tcp_server_socket.accept()
            sub_thread = threading.Thread(target=self.handle_client_request, args=(new_socket,))
            sub_thread.setDaemon(True)
            sub_thread.start()

    @staticmethod
    def handle_client_request(new_socket):

        recv_data = new_socket.recv(4096)

        if len(recv_data) == 0:
            new_socket.close()
            return

        recv_content = recv_data.decode("utf-8")
        print(recv_content)

        request_list = recv_content.split(" ", maxsplit=2)
        request_path = request_list[1]

        if request_path == "/":
            request_path = "/index.html"

        if request_path.endswith(".html"):
            logging.info("动态资源请求地址:" + request_path)
            env = {
                "request_path": request_path
            }
            status, headers, response_body = myframework.handle_request(env)

            response_line = "HTTP/1.1 %s\r\n" % status
            response_header = ""

            for header in headers:
                response_header += "%s: %s\r\n" % header

            response_data = (response_line + response_header + "\r\n" + response_body).encode("utf-8")

            new_socket.send(response_data)
            new_socket.close()

        else:
            logging.info("静态资源请求地址:" + request_path)
            try:
              with open("static"+request_path, "rb") as file:
                  file_data = file.read()
            except Exception as e:
                response_line = "HTTP/1.1 404 Not Found\r\n"
                response_header = "Server: PWS/1.0\r\n"
                with open("static/error.html", "rb") as file:
                    file_data = file.read()
                response_body = file_data
                response = (response_line+response_header+"\r\n").encode("utf-8")+response_body
                new_socket.send(response)
            else:
                response_line = "HTTP/1.1 200 OK\r\n"
                response_header = "Server: PWS/1.0\r\n"
                response_body = file_data
                response = (response_line+response_header+"\r\n").encode("utf-8")+response_body
                new_socket.send(response)
            finally:
                new_socket.close()





def main():
    web_server = HttpWebServer(8080)
    web_server.start()
    # params = sys.argv
    #
    # if len(params) != 2:
    #     print("执行的命令格式如下: python3 xxx.py 9000")
    #     logging.warning("在终端启动程序参数的个数不等于2!")
    #     return
    # if not params[1].isdigit():
    #     print("执行的命令格式如下: python3 xxx.py 9000")
    #     logging.warning("在终端启动程序参数的类型不是数字字符串!")
    #     return
    #
    # port = int(params[1])
    # web_server = HttpWebServer(port)
    # web_server.start()


if __name__ == '__main__':
    main()