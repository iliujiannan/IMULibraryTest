from httplib2 import Http
from urllib.parse import urlencode
import json
import time
import datetime

class Student:
    id = ''
    seat = ''
    name = ''
    dev_id = ''
    dev_name = ''

class GetStudentPosition():
    def __init__(self):
        pass
    def send_request(self, room_id, date, start_time, end_time):
        # name = '1B%E5%8C%BA'
        http = Http()
        url = 'http://202.207.7.180:8081/ClientWeb/pro/ajax/device.aspx?'
        param = 'byType=devcls&display=fp&md=d&room_id={{room_id}}&purpose='\
                '&img=..%2F..%2Fupload%2FDevImg%2FFloorPlan%2Frm100485891.jpg''&cld_name=default'\
                '&date={{date}}&fr_start={{fr_start}}&fr_end={{fr_end}}&act=get_rsv_sta&_=1488367036015'
        param = param.replace("{{room_id}}", str(room_id))
        param = param.replace("{{date}}", str(date))
        param = param.replace("{{fr_start}}", str(start_time))
        param = param.replace("{{fr_end}}", str(end_time))
        url = url + param
        response, conetent = http.request(uri=url, method='GET')
        # print(conetent.decode('utf-8'))
        return conetent.decode('utf-8')
    def get_seat_info_dict(self, date, start_time, end_time):

        list = []
        # 1B
        temp_list = self.analyze_result(self.send_request("100485887", date, start_time, end_time))

        list.extend(temp_list)
        #2B1
        temp_list = self.analyze_result(self.send_request("100485889", date, start_time, end_time))

        list.extend(temp_list)
        #2B2
        temp_list = self.analyze_result(self.send_request("100485891", date, start_time, end_time))

        list.extend(temp_list)
        #2A
        temp_list = self.analyze_result(self.send_request("100485893", date, start_time, end_time))

        list.extend(temp_list)
        #3B1
        temp_list = self.analyze_result(self.send_request("100485895", date, start_time, end_time))

        list.extend(temp_list)
        #3B2
        temp_list = self.analyze_result(self.send_request("100485897", date, start_time, end_time))

        list.extend(temp_list)
        #3A
        temp_list = self.analyze_result(self.send_request("100485899", date, start_time, end_time))

        list.extend(temp_list)

        return list
    def analyze_result(self, content):
        content = json.loads(content)
        data = content['data']
        students = []
        for element in data:
            if len(element.get('ts')) == 0:
                continue
            if element.get('ts')[0].get('owner') == "null":
                name = element.get('ts')[0].get('owner')
                print(name)
                continue
            student = Student()
            student.id = element.get('id')
            student.name = element.get('ts')[0].get('owner')
            student.seat = element.get('labName') + " " + element.get('title')
            student.dev_id = element.get('dev_id')
            student.dev_name = element.get('dev_name')
            students.append(student)
        return students

class Subscribe():
    def __init__(self, zjh, pwd):
        self.zjh = zjh
        self.pwd = pwd
        self.header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Length': '38',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': '202.207.7.180:8081',
            'Referer': 'http://202.207.7.180:8081/ClientWeb/xcus/ic2/Default.aspx',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': '202.207.7.180:8081',
            'Referer': 'http://202.207.7.180:8081/ClientWeb/xcus/ic2/Default.aspx',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'X-Requested-With': 'XMLHttpRequest',
        }
    def get_cookie(self):
        try:
            conn = Http()
            url = 'http://202.207.7.180:8081/ClientWeb/pro/ajax/login.aspx'
            form_data = {
                'id': self.zjh,
                'pwd': self.pwd,
                'act': 'login'
            }
            cont, resp = conn.request(url, 'POST', urlencode(form_data), headers=self.header)

            resp = resp.decode('utf-8')
            resp = json.loads(resp)
            state = resp['ret']
            if state == 1:
                cookie = str(cont['set-cookie']).replace('; path=/; HttpOnly', '')
                result = {
                    'statues': 1,
                    'msg': '成功',
                    'cookie': cookie
                }
                # print(cookie)
            else:
                result = {
                    'statues': 0,
                    'msg': '账号或密码错误'
                }
            return result
        except Exception as e:
            print(e)
            result = {
                'statues': 0,
                'msg': 'get_cookie服务异常，请稍后重试'
            }
            return result
    def subscribe(self, dev_id, start, end):
        try:
            result = self.get_cookie()
            if result['statues'] == 1:
                self.headers['Cookie'] = result['cookie']
                # print(result['cookie'])
                conn = Http()
                url = 'http://202.207.7.180:8081/ClientWeb/pro/ajax/reserve.aspx?dev_id={{dev_id}}&lab_id=&kind_id=&type=dev&prop=&test_id=&term=&test_name=&start={{start}}&end={{end}}&start_time={{start_time}}&end_time={{end_time}}&up_file=&memo=&act=set_resv&_={{_}}'
                start_time = str(start)[-5:]
                start_time = start_time.replace(':', '')
                end_time = str(end)[-5:]
                end_time = end_time.replace(':', '')
                start = start.replace(' ', '+')
                end = end.replace(' ', '+')
                times = str(int(round(time.time() * 1000)))
                url = url.replace('{{dev_id}}', str(dev_id))
                url = url.replace('{{start}}', str(start))
                url = url.replace('{{end}}', str(end))
                url = url.replace('{{start_time}}', str(start_time))
                url = url.replace('{{end_time}}', str(end_time))
                url = url.replace('{{_}}', str(times))
                # print(url)
                cont, res = conn.request(url, 'GET', headers=self.headers)
                # print(1)
                # print((res))
                res = json.loads(res.decode('utf-8'))
                array = {
                    'statues': res['ret'],
                    'msg': res['msg']
                }
            else:
                array = {
                    'statues': 0,
                    'msg': result['msg']
                }
            return array
        except Exception as e:
            print(e)
            array = {
                'statues': 0,
                'msg': 'subscribe服务异常，请稍后重试'
            }
            return array
"""
main
"""
# g = GetStudentPosition()
# for student in g.get_seat_info_dict('2017-03-02', '17:10', '21:10'):
#     if student.name == '郑希阳':
#         print("id:" + student.id)
#         print("name:" + student.name)
#         print("seat:" + student.seat)
# print('\n')
# s = Subscribe('0151122350', '0151122350')
# result = s.subscribe('100486431', '2017-03-03 20:00', '2017-03-03 21:00')
# print(result['msg'])

