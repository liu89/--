#encoding:utf-8
import requests,re,json

def get_parameter(html):
    '''获取构建请求的参数，包括请求和post参数'''

    '''首先是构建请求'''
    '''channel=chunlei&web=1这两个参数不变，直接写就可以，每个参数间用&相连'''
    '''1.sign参数，返回格式字符串'''
    '''对于得到的多着双引号的将其删去，第一个和最后一个'''
    sign_pattern = re.compile(r'"sign":(.*?),',re.S)
    sign = "".join(sign_pattern.findall(html)[0])[1:-1]
    '''2.timestamp参数，返回格式字符串'''
    timestamp_pattern = re.compile(r'"timestamp":(.*?),',re.S)
    timestamp = "".join(timestamp_pattern.findall(html)[0])
    #print(timestamp)
    '''3.app_id参数，返回字符串格式'''
    appid_pattern = re.compile(r'"app_id":(.*?),',re.S)
    appid = "".join(appid_pattern.findall(html)[0])[1:-1]
    #print(appid)
    '''4.bdstoken参数，返回字符串格式'''
    bdstoken_pattern = re.compile(r'"bdstoken":(.*?),',re.S)
    bdstoken = "".join(bdstoken_pattern.findall(html)[0])[1:-1]
    #print(bdstoken)
    request_url = 'https://pan.baidu.com/api/sharedownload?sign='\
            +sign+'&timestamp='+timestamp+'&channel=chunlei&web=1&app_id='\
            +appid+'&bdstoken='+bdstoken
    #print(request_url)
    '''构造post参数'''
    '''1.product是一定的，为share'''
    product = 'share'
    '''2.uk参数,字符串格式'''
    uk_pattern = re.compile(r'uk=(.*?)&',re.S)
    uk = uk_pattern.findall(html)[0]
    '''3.primaryid参数，与网上资料对比发现，与shareid的值一致，字符串格式'''
    primaryid_pattern = re.compile(r'"shareid":(.*?),',re.S)
    primaryid = "".join(primaryid_pattern.findall(html)[0])
    #print(primaryid)
    '''4.fid_list参数，搜索fid，出现过，但是需要处理'''
    fid_pattern = re.compile(r'fid=(.*?)&',re.S)
    fid = int(fid_pattern.findall(html)[0][18:])
    #print('[{fid}]'.format(fid=fid))
    data = {
        'product':product,
        'uk':uk,
        'primaryid':primaryid,
        'fid_list':'[{fid}]'.format(fid=fid),
    }
    return request_url,data
url = ''
headers = {
    'User-Agent': '',
    'Cookie':'',
}
r = requests.get(url, headers = headers)
request_url,data = get_parameter(r.text)
print(request_url)
print(data)
rr = requests.post(request_url,headers=headers,data=data)
true_url_dict = json.loads(rr.text)
true_url = str(true_url_dict['list'][0]['dlink'])
response = requests.get(true_url,headers=headers)
gg = response.apparent_encoding
response.encoding = gg
with open('xxx.txt','w',encoding='utf-8') as f:
    f.write(response.text)
print('爬取成功')

