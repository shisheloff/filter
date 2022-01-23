import psycopg2
from config.config import host, user, password, db_name


def check_incident():
    try:
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cursor:
            connection.autocommit = True
            cursor.execute("select * from public.datastore where message like '%authentication failure%'")
            potentially_incidents_for_first_rule = cursor.fetchall()
            if potentially_incidents_for_first_rule:
                cursor.execute("update public.datastore set incidents='yes' where message like '%authentication failure%'")
                print("[SUCCESS]: Incident: potentially brute force attack!")
                print("incidents:\n" + '\n'.join(map(str, potentially_incidents_for_first_rule)))
            cursor.execute("select * from public.datastore where message like '%user NOT in sudoers%'")
            potentially_incidents_for_second_rule = cursor.fetchall()
            if potentially_incidents_for_second_rule:
                cursor.execute("update public.datastore set incidents = 'yes' where message like '%user NOT in sudoers%'")
                print("[SUCCESS]: Incident: privilege escalation!")
                print("incidents:\n" + '\n'.join(map(str, potentially_incidents_for_second_rule)))

    except Exception as _ex:
        print("[ERROR]: ", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO]: postgresql connection closed")
