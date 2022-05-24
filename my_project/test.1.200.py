import psycopg2


def initializare_conexiune():
    """Initializam conexiunea """

    return psycopg2.connect(
        host="localhost",
        database="testare",
        user="postgres",
        password="Cu4sGr3cesc")


def reset_sql():
    """Pentru ca vrem sa creem tabelele de la zero in SQL"""
    with conn:
        c = conn.cursor()
        query = 'drop table golgheteri, anul_castigarii, echipe, tari;'
        c.execute(query)
        c.close()


def create_tables():
    """Creem tabelele in SQL"""

    with conn:
        c = conn.cursor()
        query1 = '''create table if not exists tari (
        id serial primary key,
        tara varchar(20),
        cod_tara varchar(20)
        );'''

        query2 = '''create table if not exists echipe (
        id serial primary key,
        first_name varchar(20),
        second_name varchar(20),
        tari_id int,
        constraint fk_echipe foreign key (tari_id) references tari(id)
         );'''

        query3 = '''create table if not exists anul_castigarii (
        id serial primary key,
        anul int,
        locul_finalei varchar(20),
        echipe_id int,
        constraint fk_anul_castigarii foreign key (echipe_id) references echipe(id)
        );'''

        query4 = """create table if not exists golgheteri (
        id serial primary key,
        nume varchar(20),
        prenume varchar(20),
        goluri int,
        meciuri_jucate int,
        tari_id int,
        constraint fk_echipe foreign key (tari_id) references tari(id)
        );"""

        c.execute(query1)
        c.execute(query2)
        c.execute(query3)
        c.execute(query4)
        c.close()


def inserare_tabel():
    """Inseram valorile in tabele"""

    tipar_tiparire1 = '''insert into tari (tara, cod_tara) values '''
    tipar_tiparire = '''insert into echipe (first_name, second_name, tari_id) values '''
    tipar_tiparire2 = '''insert into anul_castigarii (anul, locul_finalei, echipe_id) values '''
    tipar_tiparire3 = '''insert into golgheteri (nume, prenume, goluri, meciuri_jucate, tari_id) values '''

    randuri = 0
    r1 = 0
    r2 = 0
    r3 = 0

    with conn:
        c = conn.cursor()
        with open('csv/tari.csv', 'r', encoding="utf-8") as ln:
            for txt in ln:
                # print(txt)
                txt = txt.strip()
                if txt == '':
                    continue
                r1 += 1
                rezultat = txt.strip().split(',')
                print(rezultat, r1)

                if r1 == 1:
                    continue
                else:
                    rezultat_final1 = tipar_tiparire1 + str(tuple(rezultat)) + ';'
                    query5 = rezultat_final1
                    print(query5)
                    c.execute(query5)

        with open('csv/echipe.csv', 'r', encoding="utf-8") as line:
            for text in line:
                # print(text)
                text = text.strip()
                if text == '':
                    continue
                randuri += 1
                rezultat_lista = text.strip().split(',')
                # print(rezultat_lista, randuri)
                if randuri == 1:
                    continue
                else:
                    rezultat_final = tipar_tiparire + str(tuple(rezultat_lista)) + ';'
                    query6 = rezultat_final
                    print(query6)
                    c.execute(query6)

        with open('csv/anul.csv', 'r', encoding="utf-8") as lni:
            for tx in lni:
                # print(tx)
                tx = tx.strip()
                if tx == '':
                    continue
                r2 += 1
                rez = tx.strip().split(',')
                # print(rez, r2)
                if r2 == 1:
                    continue
                else:
                    rezultat_final2 = tipar_tiparire2 + str(tuple(rez)) + ';'
                    query7 = rezultat_final2
                    print(query7)
                    c.execute(query7)

        with open('csv/golgheteri.csv', 'r', encoding="utf-8") as ls:
            for tl in ls:
                # print(tl)
                tl = tl.strip()
                if tl == '':
                    continue
                r3 += 1
                rezult = tl.strip().split(',')
                # print(rezult, r3)
                if r3 == 1:
                    continue
                else:
                    rezultat_final3 = tipar_tiparire3 + str(tuple(rezult)) + ';'
                    query8 = rezultat_final3
                    print(query8)
                    c.execute(query8)
        c.close()


if __name__ == '__main__':
    conn = initializare_conexiune()

    reset_sql()

    create_tables()

    inserare_tabel()



