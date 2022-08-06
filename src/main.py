# coding:utf-8
import sys
import time
import psutil
import requests

requests.packages.urllib3.disable_warnings()
requests.DEFAULT_RETRIES = 5

CURRENT_ROOM_DATA = ("GET", "/lol-lobby/v2/lobby") #获取当前房间信息

class LCUClient:
    def __init__(self):
        self.url = "https://riot:auth_token@127.0.0.1:app_port"

    def query_interface(self, method, interface):
        """
        发送接口
        :return:lol本地服务返回的信息
        """
        print("query interface", interface)
        res = requests.request(method, self.url + interface, verify=False)
        print(res.json())
        return res

    def get_user_info(self):
        """
        获取登录的用户信息
        :return:
        """
        self.query_interface("get", "/lol-summoner/v1/current-summoner")

def find_lcu_process():
    """
    找到LeagueClientUx.exe进程,获取启动参数
    :return:参数列表
    """
    lol_ux_cmdline = []
    while True:
        for process in psutil.process_iter():
            try:
                process_info = process.as_dict(attrs=["name", "cmdline"])
            except:
                pass
            else:
                if process_info["name"] == "LeagueClientUx.exe":
                    lol_ux_cmdline = process_info["cmdline"]
                    break
        if len(lol_ux_cmdline):
            print("find LeagueClientUx process")
            break
        time.sleep(1)
    return lol_ux_cmdline

def init_env(LCU_api_client):
    """
    初始化与客户端的连接
    :return:
    """
    lol_ux_cmdline = find_lcu_process()
    #获取参数
    arg_dic = {}
    for line in lol_ux_cmdline:
        if "=" in line:
            key, val = line.strip().split('=')
            arg_dic[key] = val
    print(arg_dic)


    try:
        real_url = LCU_api_client.url
        real_url = real_url.replace("auth_token", arg_dic["--remoting-auth-token"])
        real_url = real_url.replace("app_port", arg_dic["--app-port"])
        LCU_api_client.url = real_url
    except:
        return False
    finally:
        print(LCU_api_client.url)

    return True


if __name__ == "__main__":
    LCU_api_client = LCUClient()
    env_ok = False
    while not env_ok:
        env_ok = init_env(LCU_api_client)
        # listen

    LCU_api_client.get_user_info()

    sys.exit(0)







