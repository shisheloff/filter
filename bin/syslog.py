def parser(line):
    month, day, time, domain, sndr, *msg = line.split()
    sender, *number = sndr.rstrip(':').rstrip(']').split('[')  # ``sender[number]'' OR ``sender''
    message = ' '.join(msg)

    return dict(
        month=month,
        day=day,
        time=time,
        domain=domain,
        sender=sender,
        message=message
    )
