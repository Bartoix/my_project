import psycopg2
from flask import Flask, render_template, request


def ratio(c, d):
    """Pentru a afla raportul dintre goluri per meciuri jucate in UCL"""

    if c == 0 or d == 0:
        return 0
    else:
        return round(c / d, 2)


conn = psycopg2.connect(
        host="localhost",
        database="testare",
        user="postgres",
        password="Cu4sGr3cesc")

app = Flask('Proiect')


@app.route('/')
@app.route('/home')
def prima_pagina():
    """Tempate-ul pentru informatia din prima pagina"""

    return render_template('first.html')


@app.route('/istoric')
def history():
    """Template-ul pentru informatia din pagina istoric"""

    return render_template('historic.html')


@app.route('/castigatoare')
def winners():
    """Selectia din SQL pentru a afisa castigatoarele competitiei"""

    with conn:
        c = conn.cursor()
        query = ("""
        select e.id, concat(e.first_name, ' ', e.second_name) as "Echipa", t.id, t.tara, ac.anul
        from echipe e, tari t, anul_castigarii ac  
        where e.tari_id = t.id and ac.echipe_id = e.id
        order by ac.anul desc;

        """)
        c.execute(query)
        records = c.fetchall()
        # print(records, type(records))

    return render_template('winners.html', tabel=records)


@app.route('/echipa/<int:echipa_id>')
def echipa(echipa_id):
    """Selectia din SQL pentru link-ul catre echipa castigatoare"""

    with conn:
        c = conn.cursor()
        query = ("""
        select e.id, concat(e.first_name, ' ', e.second_name), t.id, t.tara, ac.anul
        from echipe e, tari t, anul_castigarii ac
        where e.tari_id = t.id and ac.echipe_id = e.id and e.id = %s::integer;
        """)
        c.execute(query, (echipa_id,))
        target = c.fetchall()
        # print(target, type(target))
        total = len(target)

    return render_template('winner.html', target=target, total=total)


@app.route('/tara/<tara_id>')
def country(tara_id):
    """Selectia din SQL pentru link-ul catre tara din care provine echipa si numarul de trofee per tara"""

    with conn:
        c = conn.cursor()
        query = """
        select e.id, concat(e.first_name, ' ', e.second_name), t.id, t.tara
        from echipe e, tari t
        where e.tari_id = t.id and t.id = %s::integer;
        """
        c.execute(query, (tara_id,))
        tari = c.fetchall()
        # print(tari, type(tari))

        if tari:
            denumire_tara = tari[0][3]
        else:
            denumire_tara = None

        query1 = """
        select e.id, concat(e.first_name, ' ', e.second_name), t.id, t.tara, ac.anul
        from echipe e, tari t, anul_castigarii ac 
        where e.tari_id = t.id and ac.echipe_id = e.id and t.id = %s::integer;
        """
        c.execute(query1, (tara_id,))
        anii = c.fetchall()
        # print(anii, type(anii))
        val = len(anii)
    return render_template('tara.html', pays=tari, tara=denumire_tara, val=val)


@app.route('/golgheteri')
def scorer():
    """Selectia din SQL pentru a afisa golgheterii UCL"""

    with conn:
        c = conn.cursor()
        query = """
        select g.id, concat(g.nume, ' ', g.prenume) as "Nume", g.goluri, t.tara 
        from golgheteri g, tari t 
        where g.tari_id = t.id; 
        """
        c.execute(query)
        scorers = c.fetchall()
        # print(scorers, type(scorers))
    return render_template('goool.html', marcator=scorers)


@app.route('/golgheter/<golgheter_id>')
def a_marca(golgheter_id):
    """Selectia din SQL pentru link-ul catre golgheter"""

    with conn:
        c = conn.cursor()
        query = """
        select g.id, concat(g.nume, ' ', g.prenume) as "Nume", g.goluri, g.meciuri_jucate, t.tara 
        from golgheteri g, tari t 
        where g.tari_id = t.id and g.id = %s::integer; 
        """
        c.execute(query, (golgheter_id,))
        atacant = c.fetchall()
        # print(atacant, type(atacant))
        # print(atacant[0][2], atacant[0][3])
        if atacant:
            gol_per_meci = ratio(atacant[0][2], atacant[0][3])
        else:
            gol_per_meci = None
    return render_template('golgheter.html', atacant=atacant, gol_per_meci=gol_per_meci)


@app.route('/cauta', methods=['GET', 'POST'])
def search():
    """Pentru a defini cautarea din pagina Cstigatoarele"""

    if request.method == 'POST':
        srch = request.form
    else:
        srch = request.args

    c = conn.cursor()
    query = """
    select e.id, concat(e.first_name, ' ', e.second_name)
    from echipe e;
    """
    c.execute(query)
    selectie = c.fetchall()
    # print(selectie, type(selectie))
    name = srch.get('name').lower()
    nimic = ''
    di = {}

    for i in selectie:
        ech = i[1].lower()
        if name in ech:
            di[i[0]] = i[1]
        else:
            nimic = 'Nu s-a gasit nici o echipa castigatoare a UEFA Champions League'

    return render_template('cauta.html', team=di, nothing=nimic)


@app.route('/search', methods=['GET', 'POST'])
def cauta():
    """Pentru a defini cautarea din pagina Golgheter"""

    if request.method == 'POST':
        srch = request.form
    else:
        srch = request.args

    c = conn.cursor()
    query = """
    select g.id, concat(g.nume, ' ', g.prenume)
    from golgheteri g;
    """
    c.execute(query)
    selectie = c.fetchall()
    # print(selectie, type(selectie))
    name = srch.get('nume').lower()
    nimic = ''
    di = {}

    for i in selectie:
        ech = i[1].lower()
        if name in ech:
            di[i[0]] = i[1]
        else:
            nimic = 'Nu s-a gasit nici un golgheter '

    return render_template('search.html', team=di, nothing=nimic)


@app.route('/cautari', methods=['GET', 'POST'])
def find():
    """Pentru a defini cautarea de tari"""

    if request.method == 'POST':
        srch = request.form
    else:
        srch = request.args

    c = conn.cursor()
    query = """
    select t.id, t.tara
    from tari t;
    """
    c.execute(query)
    selector = c.fetchall()
    # print(selector, type(selector))
    name = srch.get('nom').lower()

    nott = ''
    dis = {}

    for i in selector:
        este = i[1].lower()
        if name in este:
            dis[i[0]] = i[1]
        else:
            nott = 'Nu s-a gasit nici o tara, a caror echipe sa fi castigat UCL '

    return render_template('find.html', tara=dis, nothing=nott)


@app.route('/contact')
def con():
    return render_template('form_incercari.html')


@app.errorhandler(404)
def page_not_found():
    """Pentru a prinde rute inexistente"""
    return render_template('catch_errors'), 404


if __name__ == '__main__':
    app.run(debug=True)
