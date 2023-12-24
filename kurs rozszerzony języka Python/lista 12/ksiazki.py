from sqlalchemy.orm import DeclarativeBase, validates, sessionmaker
from sqlalchemy import select, Table, Column, Integer, ForeignKey, String, create_engine
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List
import sys

import xmlrpc.client

class Base(DeclarativeBase):
    pass

class Znajomy(Base):
    __tablename__ = "Znajomi"
    z_id  = Column("z_id", Integer, primary_key= True)
    imie  = Column("imie",  String)
    email = Column("email", String)
    ksiazki: Mapped[List["Ksiazka"]] = relationship(back_populates="uzytkownik")

    def __init__(self, z_id, imie, email):
        self.z_id = z_id
        self.imie  = imie
        self.email = email

    def __repr__(self):
        return f"({self.z_id}): {self.imie}, {self.email}"

    @validates("email")
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Brakuje '@' w adresie email")
        return email

class Ksiazka(Base):
    __tablename__ = "Ksiazki"
    k_id = Column("k_id", Integer, primary_key=True)
    tytul = Column(String)
    rok_wydania = Column(Integer)
    uzytkownik_id: Mapped[Integer] = Column(ForeignKey("Znajomi.z_id"))
    uzytkownik: Mapped["Znajomy"] = relationship(back_populates="ksiazki")
    autor_id: Mapped[Integer] = Column(ForeignKey("Autorzy.a_id"))
    autor: Mapped["Autor"] = relationship(back_populates="ksiazki")

    def __init__(self, k_id, tytul, rok_wydania, autor_id):
        self.k_id = k_id
        self.tytul = tytul
        self.rok_wydania = rok_wydania
        self.autor_id = autor_id

    def __repr__(self):
        return f"({self.k_id}) {self.tytul}, {self.autor.nazwa} {self.rok_wydania}"
    
    @validates("rok_wydania")
    def validate_rok_wydania(self, key, rok_wydania):
        if int(rok_wydania) < 1801:
            raise ValueError("Za wczesny rok wydania") 
            # Za najstarszą drukowaną książkę,
            # która przetrwała do czasów współczesnych uważa się „Diamentową Sutrę”, 
            # pochodzącą z dziewiątego wieku naszej ery
        return rok_wydania
     
class Autor(Base):
    __tablename__ = "Autorzy"
    a_id = Column(Integer, primary_key=True)
    nazwa = Column(String)
    ksiazki: Mapped[List["Ksiazka"]] = relationship(back_populates="autor")

    def __init__(self, a_id, nazwa):
        self.a_id = a_id
        self.nazwa = nazwa

    def __repr__(self):
        return f"({self.a_id}) {self.nazwa}"

    @validates("nazwa")
    def validate_nazwa(self, key, nazwa):
        if nazwa[0].islower():
            raise ValueError("Nazwa nie zaczyna sie z wielkiej litery")
        return nazwa

def main(args):
    if(args[0] == '--help'):
        print(
    """
    --dodaj-k <id> <tytul> <rok_wydania> <id_autora>
            dodaje ksiazke o danym id, tytule, roku wydania i id_autora
    --dodaj-a <id> <nazwa>
            dodaje autora o danym id i nazwie
            (nazwa - Platon lub Jan Kochanowski)
    --dodaj-a-API <id> <nazwa>
            jak --dodaj-a ale przez API
    --dodaj-z <id> <imie> <email>
            dodaje znajomego o danym id imieniu i emailu
    --wypozycz <id_znajomego> <id_ksiazki>
            przypisuje ksiazke o danym id znajomemu o danym id
    --zwroc <id_ksiazki>
            zwraca ksiazke o danym id
    --znajomi 
            wypisuje id, imie oraz email i wypozyczone ksiazki zapisanych znajomych
    --ksiazki
            wypisuje id, tytul,autora  oraz rok wydania zapisanych ksiazek
    --autorzy
            wypisuje autorow i ich ksiazki
    --znajomi-API
            jak --znajomi ale przez API
    --ksiazki-API
            jak --ksiazki ale przez API
    --autorzy-API
            jak --autrzy ale przez API
    --autorzy-update <id> <nowa_nazwa>
            zmienia nazwe autora o danym id przez API
    --autorzy-delete <id>
            usuwa autora o danym id i jego ksiazki
    """)
    else:
        server = xmlrpc.client.ServerProxy("http://localhost:8002")
        session = Session()
        if(args[0] == '--dodaj-k'):
            session.add(Ksiazka(args[1],args[2],args[3],args[4]))
        if(args[0] == '--dodaj-a'):
            session.add(Autor(args[1],args[2]))
        if(args[0] == '--dodaj-z'):
            session.add(Znajomy(args[1],args[2],args[3]))
        if(args[0] == '--wypozycz'):
            id_znaj = args[1]
            id_ksia = args[2]
            stmt = select(Ksiazka).where(Ksiazka.k_id == id_ksia)
            ksiazka = session.scalars(stmt).one()
            ksiazka.uzytkownik_id = id_znaj
        if(args[0] == '--zwroc'):
            id_ksia = args[1]
            stmt = select(Ksiazka).where(Ksiazka.k_id == id_ksia)
            ksiazka = session.scalars(stmt).one()
            ksiazka.uzytkownik_id = None
        if(args[0] == '--znajomi'):
            res = []
            znajomi = session.query(Znajomy).all()
            for el in znajomi:
                res.append(str(el) + " " + str(el.ksiazki))
            # return res
            print(res)
        if(args[0] == '--ksiazki'):
            res = []
            ksiazki = session.query(Ksiazka).all()
            for el in ksiazki:
                res.append(str(el))
            # return res
            print(res)
        if(args[0] == '--autorzy'):
            res = []
            autorzy = session.query(Autor).all()
            for el in autorzy:
                tab = []
                for k in el.ksiazki:
                    tab.append(k.tytul)
                res.append(str((el, tab)))
            # return res
            print(res)
        if(args[0] == '--autorzy-API'):
            print(server.autorzy_read())
        if(args[0] == '--znajomi-API'):
            print(server.znajomi_read())
        if(args[0] == '--ksiazki-API'):
            print(server.ksiazki_read())
        if(args[0] == '--autorzy-delete'):
            server.autorzy_delete(args[1])
        if(args[0] == '--autorzy-update'):
            server.autorzy_update(args[1], args[2])
        if(args[0] == '--dodaj-a-API'):
            server.autorzy_create(args[1], args[2])

        session.commit()
        session.close()

engine = create_engine("sqlite:///ksiazki.db", echo=False)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

if __name__=="__main__":
    if len(sys.argv) == 1:
         print("zobacz 'python ksiazki.py --help'")
    else:
        main(sys.argv[1:])