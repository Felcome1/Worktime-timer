import sys
from datetime import time
import PySimpleGUI as sg
import timer
import asyncio
import database

starttime: time = timer.MyTime().time
endtime: time = None
TIME = 20
time_overall: int = 0
time_stopped: int = 0
time_worked: int = 0
date: str = ''
count: bool = True
turned: bool = True
UTC: str = '+0'
wind = 1


async def time_now():
    global date

    while True:
        now = timer.MyTime()
        print(now.time)
        window['now'].update(now.time)
        date = now.time

        await asyncio.sleep(TIME)


def to_iso(value):
    return (value // 60 // 60, value // 60, value % 60)


async def time_gone():
    global time_overall
    global time_stopped
    global time_worked

    while True:
        if not turned and count:
            time_stopped += 1
        if count:
            time_overall += 1
        window['overall_time'].update(time(*to_iso(time_overall)))
        window['stoptime'].update(time(*to_iso(time_stopped)))
        time_worked = time_overall - time_stopped
        window['time'].update(time(*to_iso(time_worked)))

        await asyncio.sleep(1)


async def ui():
    global turned
    global count
    global time_overall
    global time_stopped
    global time_worked

    while True:
        event, value = window.read(timeout=0.01)

        if event == None:
            sys.exit()

        elif event == 'Start':
            turned = True
            if not count:
                time_overall, time_stopped, time_worked = 0, 0, 0
                count = True
            else:
                count = True
        elif event == 'Stop':
            turned = False

        elif event == 'End shift':
            database.endshift(date[0], time_overall, time_stopped, time_worked, starttime[1], date[1], 'project')
            count = False
            db = database.get_db()
            window['-TABLE-'].update(values=db[0],)
        elif event == 'Data':
            global wind
            wind = 0 if wind else 1
        await asyncio.sleep(0.01)


async def db_list():
    window_db = sg.Window('Worktime', layout_db.pop(0))

    while True:
        event, value = window_db.read(timeout=0.01)

        if event == 'Exit':
            break


async def wait_list():
    await asyncio.gather(ui(), time_now(), time_gone())


layout = [[sg.Button('Data')],
           [sg.Text(starttime), sg.Text(f'       UTC{UTC}')],
           [sg.Text(0, key='now')],
           [sg.Text('Working'), sg.Text('Chillin\''), sg.Text('Overall worktime')],
           [sg.Text(0, key='time'), sg.Text('', key='stoptime'), sg.Text('', key='overall_time')],
           [sg.Button('Start'), sg.Button('Stop'), sg.Button('End shift')]]

db = database.get_db()
layout_db = [[sg.Table(values=db[0], headings=db[1], auto_size_columns=False,
                       justification='right', key='-TABLE-', display_row_numbers=False,
                       enable_events=True, num_rows=min(25, len(db[1])))],
              [sg.Text('')],
              [sg.Text(starttime), sg.Text(f'       UTC{UTC}')],
              [sg.Text(0, key='now')],
              [sg.Text('')],
              [sg.Text('Working'), sg.Text('Chillin\''), sg.Text('Overall worktime')],
              [sg.Text(0, key='time'), sg.Text('', key='stoptime'), sg.Text('', key='overall_time')],
              [sg.Text('')],
              [sg.Button('Start'), sg.Button('Stop'), sg.Button('End shift')]]


window = sg.Window('Timer', layout_db)


