# coding:utf-8
hour, minute, count, flag = 14, 50, 0, True

while flag:
    if hour == 14 and 51 <= minute <= 59 or (hour == 15 and minute == 0):
        count += 1
    minute += 1
    if minute == 1:
        flag = False
    if minute == 60:
        minute = 0
        hour = 15
    print(hour, minute)
