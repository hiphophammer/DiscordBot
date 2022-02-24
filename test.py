import datetime

result = []
d_tday = datetime.datetime.now()
d1 = datetime.datetime(2022, 2, 25, hour=8)
delta = d1 - d_tday
if delta.seconds > 0:
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60
    result.append('출시까지 ' + str(delta.days) + '일' + str(hours) + '시간' + str(minutes) + '분' + str(seconds) + '초')
z = ''.join(result)
print(z)