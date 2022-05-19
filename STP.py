import sqlite3, sys
from alive_progress import alive_bar


def tables_list(database):
    result = []
    db = sqlite3.connect(database)
    sql = db.cursor()

    sql.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for i in sql.fetchall():
        result.append(str(i[0]))
    return result


def column_list(database):
    import sqlite3
    conn = sqlite3.connect(database)
    cu = conn.cursor()

    # Получите имя таблицы, сохраните его в списке tab_name
    cu.execute("select name from sqlite_master where type='table'")
    tab_name = cu.fetchall()
    tab_name = [tab_name[x][0] for x in range(len(tab_name))]

    # Получить имена столбцов (имена полей) таблицы и сохранить их в списке col_names
    col_names = []
    for n in range(len(tab_name)):
        cu.execute('pragma table_info({})'.format(tab_name[n]))
        col_name = cu.fetchall()
        col_name = [col_name[x][1] for x in range(len(col_name))]
        col_names.append(col_name)

    return col_names


def data_list(database, table):
    result = []
    import sqlite3
    db = sqlite3.connect(database)
    sql = db.cursor()
    for i in sql.execute(f"SELECT * FROM {table}"):
        result += [i]
    return result

cmm = sys.argv[1]

if cmm in ['-i', '--input']:
    d = sys.argv[2]
    if d[:2] == '.\\':
        d = d[2:]
        print(d)
    lst = tables_list(d)
    c_list = column_list(database=d)
elif cmm in ['-h', '--help']:
    print('-i  --input   =>    Input DBname')
    print()
    print('-h  --help    =>    This help blank')
    sys.exit()
    #print('command --input dbname')
else:
    print('-h, --help   =   help')
    sys.exit()



def create_tables():
    for i in range(len(lst)):
        table_name = lst[i]
        cul_list = c_list[i]
        print('SELECTED  =>  '+table_name.replace("'", "\'"))
        cc = ''
        for col in cul_list:
            cc += col + ' TEXT,'
        cc = cc[:len(cc)-1]
        import psycopg2
        with psycopg2.connect(database=d[:len(d) - 3], user="postgres", password="armageddon") as db:
            sql = db.cursor()
            tn = table_name.replace("'", "\'")
            sql.execute(f"""CREATE TABLE IF NOT EXISTS {tn} ({cc})""")
            db.commit()
            print('Table created')

        # PLACE FOR DATA CONVERT
        print('Start convert...')
        with alive_bar(len(data_list(d, table_name))) as bar:

            for dat in data_list(d, table_name):
                bar()
                new_data = ''
                for da in dat:
                    ddd = da.replace("'", "\'")
                    new_data += f"'{ddd}', "
                new_data = new_data[:len(new_data)-2]
                with psycopg2.connect(database=d[:len(d) - 3], user="postgres", password="armageddon") as db:
                    sql = db.cursor()
                    sql.execute(f"INSERT INTO {table_name} VALUES({new_data})")
                    db.commit()
        print("Table converted")
        print()

    print()
    print()
    print('######     ######    ####   ##   #######')
    print('##   ##   ##    ##   ## ##  ##   ##')
    print('##    ##  ##    ##   ##  ## ##   #######')
    print('##   ##   ##    ##   ##   ####   ##')
    print('######     ######    ##     ##   #######')
    print()
    print()


create_tables()

