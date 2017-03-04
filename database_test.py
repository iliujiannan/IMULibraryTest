import pymysql.cursors
from library_service import GetStudentPosition, Student

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '',
    'db': 'library',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}
conn  = pymysql.connect(**config)
g = GetStudentPosition()
data_list = g.get_seat_info_dict('2017-03-04', '18:00', '19:00')
for student in data_list:
    seat_id = student.dev_id
    seat_name = student.dev_name
    sql = 'insert into seat (seat_id ,seat_name) VALUES ("' + seat_id + '","' + seat_name + '")'
    conn.cursor().execute(sql)
    conn.commit()
conn.close()
# try:
#     with conn.cursor() as curs :
#         sql = 'insert into seat (seat_id ,seat_name) VALUES ("15100654854","1B001")'
#         curs.execute(sql)
#         conn.commit()
# except Exception as e:
#     print('数据库异常')
# finally:
#     conn.close()

