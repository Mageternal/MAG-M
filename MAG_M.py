
from email import header
import requests
import random
import string
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Medhot = ""
url = "http://magyyds.shop"
phpmyadmin_port = 9301
timeout_retry = 0
accuracy = {'HFish':0,'DecoyMini':0}

HFish_headers = {
        "Host":url,
        'Connection':'close'
}
'''
def Variable_input(phpmyadmin_port):
    phpmyadmin_port = input("发现phpmyadmin端口？")
    if phpmyadmin_port == 0:
        phpmyadmin_port = 9301
'''
def if_Medhot(timeout_retry):
    global Medhot
    if "://" not in url:
        try:
            if 200 == requests.get("http://"+url).status_code:
                Medhot = "http://"
            elif 200 == requests.get("https://"+url,verify=False).status_code:
                Medhot = "https://"
        except Exception as error :
            print("Error1：",error)
            if timeout_retry <= 3:
                timeout_retry += 1
                if_Medhot(timeout_retry)
            else:
                exit()

def HFish(accuracy,phpmyadmin_port):
    #第一验证
    try:
        if 'window.alert("操作失败")' in (requests.post(Medhot+url+"/login", params=HFish_headers,verify=False).text):
            accuracy['HFish'] += 20
        if 'window.alert("操作失败")' in (requests.post(Medhot+url+"/"+''.join(random.sample(string.ascii_letters + string.digits, 8)), params=HFish_headers,verify=False).text):
            accuracy['HFish'] += 50
    except Exception as error :
        print("Error2：",error)

    #第二验证
    try:
        #sss=requests.get(Medhot+url+":"+str(phpmyadmin_port)+"/index.php?db=&table=&token=0900719cf14fbbcc2c84071211fcae01&lang=hy").status_code
        if 200 != requests.get(Medhot+url+":"+str(phpmyadmin_port)+"/index.php?db=&table=&token=0900719cf14fbbcc2c84071211fcae01&lang=hy",verify=False).status_code:
            accuracy['HFish'] +=30
    except Exception as error :
        print("Error3：",error)

def DecoyMini(accuracy):
    #第一验证:文件验证
    try:
        html_text = requests.get(Medhot+url,verify=False).text
        if "jquery.min.js" in html_text:
            accuracy['DecoyMini'] += 10
        if "jquerys.js" in html_text and "login.js" in html_text:
            accuracy['DecoyMini'] += 30
    except Exception as error :
        print("Error5：",error)

    #第二验证:版本验证
    start = html_text.find('<script src="') + len('<script src="')
    end = html_text.find('"></script>')
    field = html_text[start:end]
    jszd = "/"+field.split("/")[0]+"/"

    try:
        if accuracy['DecoyMini'] == 5 or accuracy['DecoyMini'] == 15:
            if "jQuery v2.1.4" in requests.get(Medhot+url+jszd+"jquery.min.js",verify=False).text:
                accuracy['DecoyMini'] += 60
    except Exception as error :
        print("Error4：",error)


def statistics(accuracy):#统计
    if accuracy['HFish'] > 0:
        print("HFish蜜罐："+str(accuracy['HFish'])+"%")
    if accuracy['DecoyMini'] > 0:
        print("DecoyMini蜜罐："+str(accuracy['DecoyMini'])+"%")
    print("结束")

def main():
    if_Medhot(timeout_retry)
    HFish(accuracy,phpmyadmin_port)
    DecoyMini(accuracy)
    statistics(accuracy)
main()