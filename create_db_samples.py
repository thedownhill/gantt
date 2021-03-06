from clickhouse_driver import Client
from datetime import datetime
from random import randint

num_samples = 10000


def main():
    client = Client(host='localhost')
    client.execute('DROP TABLE IF EXISTS Task')
    client.execute('DROP TABLE IF EXISTS User')

    client.execute(''
                   'CREATE TABLE Task '
                   '(name String, start_date String, duration Int32,'
                   ' assigned_users Array(String), description String, progress Int32, creation_date Date) '
                   'ENGINE = MergeTree(creation_date, name, 8192)')
    client.execute(''
                   'CREATE TABLE User '
                   '(name String, creation_date Date) '
                   'ENGINE = MergeTree(creation_date, name, 8192)')

    values = [[f'task {i}', str(datetime(2019, 4, randint(20, 27)).date()), randint(1, 10), [], f'description of task {i}',
               randint(0, 100), datetime.today().date()] for i in range(num_samples)]
    users = [[f'default_user{i}', datetime.today().date()] for i in range(2)]

    client.execute('insert into Task values ', values)
    client.execute('insert into User values', users)


if __name__ == '__main__':
    main()
