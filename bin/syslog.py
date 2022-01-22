from time import strptime as time_parser
import os


def parser(line):
    month, day, time, domain, sndr, *msg = line.split()
    sender, *number = sndr.rstrip(':').rstrip(']').split('[')  # ``sender[number]'' OR ``sender''
    message = ' '.join(msg)

    return dict(

        datatime=time_parser(
            "{day};{month};13;{time}".format(
                month=month,
                day=day,
                time=time,
            ),
            '%d;%b;%y;%H:%M:%S'  # 'day;month;year;hour:minute:second'
        ),

        domain=domain,
        sender=sender,
        message=message
    )

'''
with open("", "r") as f:
    data = f.readlines()
    for lines in data:
        print(parser(lines))
'''