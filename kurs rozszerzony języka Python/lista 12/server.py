from xmlrpc.server import SimpleXMLRPCServer

from ksiazki import *

server = SimpleXMLRPCServer(('localhost', 8002), allow_none=True)

#READ dla ksiazek i znajomych
def znajomi_read():
    session = Session()
    res = []
    znajomi = session.query(Znajomy).all()
    for el in znajomi:
        res.append(str(el) + str(el.ksiazki))
    session.close()
    return res

def ksiazki_read():
    session = Session()
    res = []
    ksiazki = session.query(Ksiazka).all()
    for el in ksiazki:
        res.append(str(el))
    session.close()
    return res

server.register_function(znajomi_read)
server.register_function(ksiazki_read)


# CRUD dla tablicy autorow
def autorzy_create(a_id, nazwa): #dodaje autora o danym id i danej nazwie
    session = Session()
    session.add(Autor(a_id, nazwa))
    session.commit()
    session.close()

def autorzy_read(): #zwraca tablice krotek autorow i ich ksiazke
    session = Session()
    autorzy = session.query(Autor).all()
    res = []
    for autor in autorzy:
        tab = []
        for ksiazka in autor.ksiazki:
            tab.append(ksiazka)
        res.append(str((autor, tab)))
    session.close()
    # print(res)
    return res

def autorzy_update(a_id, nowa_nazwa): #zmiania nazwe autora o danym id na nowa nazwe
    session = Session()
    session.query(Autor).filter_by(a_id=a_id).nazwa = nowa_nazwa
    session.commit()
    session.close()

def autorzy_delete(a_id): #usuwa autora o danym id i jego ksiazki
    session = Session()
    autorzy = session.query(Autor).filter_by(a_id=a_id).delete()
    ksiazki = session.query(Ksiazka).filter_by(autor_id=a_id).delete()
    session.commit()
    session.close()


server.register_function(autorzy_create)
server.register_function(autorzy_read)
server.register_function(autorzy_update)
server.register_function(autorzy_delete)

server.serve_forever()