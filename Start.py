import requests

Now_data_str = "2024-08-13"
From_GuoJia = "玻利维亚"
city_chinese = "阿巴斯"
ip = "123123123"

url = "http://api.visa5i.com/wuai/system/wechat-notification/save"
json_data = {
    "apptTime": Now_data_str,
    "consDist": From_GuoJia,
    "apptType": city_chinese,
    "ipAddr": ip,
    "monCountry": '美国',
    "status": '2',
    "sys": 'AIS',
    "userName": 'jiankong@163.com',
    "passWord": '12345'
}
response = requests.post(url, json=json_data)
print(response)

#
# url = "http://api.visa5i.com/wuai/system/wechat-notification/save"
# json_data = {
#     "apptTime": this_date_str,
#     "consDist": '英国',
#     "apptType": 'Free',
#     "ipAddr": ip,
#     "monCountry": 'BRP卡',
#     "status": '1',
#     "sys": 'Other',
#     "userName": username,
#     "passWord": password
# }
# response = requests.post(url, json=json_data)