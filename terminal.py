import re
from texttable import Texttable
from time import sleep
from datetime import datetime
from datetime import timedelta
from os import system
from os import name
from os import get_terminal_size
from core.startup import create_app
from math import floor

from models.host import Host
from utils.converter import to_number
from utils.progress_bar import draw_progress_bar

def clear():
    system('cls' if name=='nt' else 'clear')


def natural_keys(text):
    return [int(d) if d.isdigit() else d for d in re.split(r'(\d+)', text[0])]


if __name__ == '__main__':
    app = create_app(name=__name__, config_name='dev')
    table_text_prev = ''
    while True:
        try:
            table = Texttable(max_width=get_terminal_size()[0])

            data_rows = []
            title_row = ['Name', 'IP', 'Message', 'Last received']
            # table.add_row()
            
            with app.app_context():
                hosts = Host.get_online_hosts()
                for host in hosts:
                    message = host.message
                    
                    try:
                        if message.startswith('$'):
                            statements = message.split('$SPLIT')
                            message = ''
                            for statement in statements:
                                if statement.startswith('$PB:'):
                                    progress = statement.split('$PB:')[1]
                                    progress = progress.split(',')

                                    current = to_number(progress[0])
                                    total = to_number(progress[1])

                                    if current < 0 or total < 0:
                                        raise ValueError('contains invalid value (less than 0).')

                                    # Example: $PB:12,100
                                    message = message + f"{current}/{total}\t"
                                    message = message + draw_progress_bar(current, total, 15)

                                elif statement.startswith('$TITLE:'):
                                    title = statement.split('$TITLE:')[1]
                                    message = f"[{title}] " + message
                    except:
                        message = host.message
                    
                    data_rows.append([host.name, host.ip, message, host.last_received.strftime('%Y-%m-%d %H:%M:%S')])
                    data_rows.sort(key=natural_keys)

            table.add_rows([title_row, *data_rows])
            table_text = table.draw()
            if table_text != table_text_prev:
                clear()
                print(table_text)
                table_text_prev = table_text
            sleep(5)
        except KeyboardInterrupt:
            break