
from bin import reciveFiles, correlation
print("[INFO]: reciving files...")
reciveFiles.reciveFile()

print("[INFO]: writing data into database...")
reciveFiles.insertData("/Users/21shish/PycharmProjects/lsfilter/logs/got_syslog.txt")

print("[INFO]: finding incidents...")
correlation.check_incident()
