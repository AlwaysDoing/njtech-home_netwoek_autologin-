import requests
import re
import os
import ddddocr

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
}
self_path = os.path.dirname(os.path.abspath(__file__))  # 获取路径
session = requests.Session()


def get_args():
    res = session.get(r'https://u.njtech.edu.cn/cas/login?service=https%3A%2F%2Fu.njtech.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3DOe7wtp9CAMW0FVygUasZ%26response_type%3Dcode%26state%3Dnjtech%26s%3Df682b396da8eb53db80bb072f5745232')
    text = res.text
    # print(text)
    lt = re.findall('(?<=name="lt" value=").*', text)[0].split('"')[0]
    execution = re.findall('(?<=name="execution" value=").*', text)[0].split('"')[0]
    url_param = re.findall('(?<=action=").*', text)[0].split('"')[0]
    post_url = 'https://u.njtech.edu.cn'+url_param
    # jsessionid=re.findall('(?<=jsessionid=).*',url_param)[0].split('?')[0]
    return lt, execution, post_url


# 验证码获取与OCR识别，返回识别出来的验证码字符串
def get_captcha():
    from http import client
    client.HTTPConnection._http_vsn = 10
    client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'u.njtech.edu.cn'
    }
    res = session.get('https://u.njtech.edu.cn/cas/captcha.jpg', headers=headers)
    with open(self_path+'\\captcha.jpg', 'wb') as img:
        img.write(res.content)
    captcha = ddddocr.DdddOcr()
    with open(self_path+'\\captcha.jpg', 'rb') as img:
        imgbyte = img.read()
        result = captcha.classification(imgbyte)
    print(result)
    return result
    

def read_file(filename):
    """
    定义读取文件内容的函数
    filename: 文件名
    """
    f = open(filename, encoding='utf-8')
    data = f.readlines()
    f.close()
    return data


def str_transfer_dict(data):
    """
    定义文件转换函数，将data转换为字典并返回字典
    data: 表示需要转换的数据
    """
    # 将列表中的内容根据冒号:进行切割，切割后的内容放到字典里面
    # 定义一个空字典
    new_dict = {}
    # 循环列表
    for lines in data:
        # 将取出来的字符串的最后面的换行符\n去掉
        lines = lines.strip('\n')
        # 将字符串以:分割，放到列表中
        line = lines.split(":")
        # 索引为0的就是key，索引为1的就是value
        new_dict[line[0]] = line[1]
    return new_dict


# 进行函数调用
lt, execution, post_url = get_args()
data = read_file('.\\config.txt')
params = str_transfer_dict(data)
print(params)
params['captcha'] = get_captcha()
params['lt'] = lt
params['execution'] = execution
# 请求连接
login_response = session.post(url=r'https://u.njtech.edu.cn/cas/login?service=https%3A%2F%2Fu.njtech.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3DOe7wtp9CAMW0FVygUasZ%26response_type%3Dcode%26state%3Dnjtech%26s%3Df682b396da8eb53db80bb072f5745232', params=params, headers=headers)
print(login_response)
print('连接成功')

