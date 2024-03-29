import requests

url = "http://54.169.239.115:8808/visa/saveApptMonitor"
json_data = {
    "apptTime": "2024-09-09",
    "consDist": '测试英国',
    "apptType": '',
    "ipAddr": "39.98.88.235",
    "monCountry": '美签',
    "status": '2',
    "sys": 'AIS',
    "userName": 'Test@163.com',
    "passWord": '12345'
}
response = requests.post(url, json=json_data)