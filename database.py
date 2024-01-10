import datetime
import sqlite3

conn = sqlite3.connect('db.db')


def query_exec(query):
    with conn as db:
        cursor = db.cursor()
        print(query)
        q = cursor.execute(query)
        db.commit()
        return q


def endshift(day, overall, stopped, working, start, end, project):
    t = [datetime.time(*[i // 60 // 60, i // 60, i % 60]) for i in [overall, stopped, working]]

    try:
        query_exec(f'INSERT INTO Worktime VALUES(\'{day}\', \'{t[0]}\', \'{t[1]}\', \'{t[2]}\', \'{start}\', \'{end}\', \'{project}\')')
    except Exception as e:
        print(e)
        #t_old = query_exec(f'SELECT Overall, Stopped, Working FROM Worktime WHERE Day = {day}')
        ##lst_t = [datetime.timedelta(*[int(j) for j in a[0][i].split(':')]) + datetime.timedelta(*[int(j) for j in str(list(t)[i]).split(':')]) for i in range(3)]
        #b = list(t_old)
        #print(b)
        #a = [[int(i) for i in [j.split(':') for j in [b[0][k] for k in range(3)]][0]]]
        #lst_t = [t[i] + datetime.timedelta(hours=a[i][0], minutes=a[i][1], seconds=a[i][2]) for i in range(3)]
        #query_exec(
        #    f'UPDATE Worktime SET Overall = \'{t[0]}\', Stopped = \'{t[1]}\', Working = \'{t[2]}\' WHERE Day = \'{t}\'')


def get_db():
    data = query_exec('SELECT * FROM Worktime')
    values = data.fetchall()
    headers = [h[0] for h in data.description]
    return values, headers
