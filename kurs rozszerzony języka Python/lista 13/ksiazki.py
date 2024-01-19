from sqlalchemy.orm import DeclarativeBase, validates, sessionmaker
from sqlalchemy import select, Table, Column, Integer, ForeignKey
from sqlalchemy import String, create_engine
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
import sys

import xmlrpc.client


class Base(DeclarativeBase):
    pass


class Znajomy(Base):
    __tablename__ = "Znajomi"
    z_id: Mapped[int] = Column("z_id", Integer, primary_key=True)
    imie: Mapped[str] = Column("imie", String)
    email: Mapped[str] = Column("email", String)
    ksiazki: Mapped[List["Ksiazka"]] = relationship(
        back_populates="uzytkownik")

    def __init__(self, z_id: int, imie: str, email: str) -> None:
        self.z_id = z_id
        self.imie = imie
        self.email = email

    def __repr__(self) -> str:
        return f"({self.z_id}): {self.imie}, {self.email}"

    @validates("email")
    def validate_email(self, key: int, email: str) -> str:
        if '@' not in email:
            raise ValueError("Brakuje '@' w adresie email")
        return email


class Ksiazka(Base):
    __tablename__ = "Ksiazki"
    k_id: Mapped[int] = Column("k_id", Integer, primary_key=True)
    tytul: Mapped[str] = Column(String)
    rok_wydania: Mapped[int] = Column(Integer)
    uzytkownik_id: Mapped[int] = Column(ForeignKey("Znajomi.z_id"))
    uzytkownik: Mapped["Znajomy"] = relationship(back_populates="ksiazki")
    autor_id: Mapped[int] = Column(ForeignKey("Autorzy.a_id"))
    autor: Mapped["Autor"] = relationship(back_populates="ksiazki")

    def __init__(self, k_id: int, tytul: str, rok_wydania: int, autor_id: int) -> None:
        self.k_id = k_id
        self.tytul = tytul
        self.rok_wydania = rok_wydania
        self.autor_id = autor_id

    def __repr__(self) -> str:
        id1 = self.k_id
        tytul = self.tytul
        a_nazwa = self.autor.nazwa
        rok = self.rok_wydania
        return f"({id1}) {tytul}, {a_nazwa} {rok}"

    @validates("rok_wydania")
    def validate_rok_wydania(self, key: int, rok_wydania: int) -> int:
        if rok_wydania < 1801:
            raise ValueError("Za wczesny rok wydania")
        return rok_wydania


class Autor(Base):
    __tablename__ = "Autorzy"
    a_id: Mapped[int] = Column(Integer, primary_key=True)
    nazwa: Mapped[str] = Column(String)
    ksiazki: Mapped[List["Ksiazka"]] = relationship(back_populates="autor")

    def __init__(self, a_id: int, nazwa: str) -> None:
        self.a_id = a_id
        self.nazwa = nazwa

    def __repr__(self) -> str:
        return f"({self.a_id}) {self.nazwa}"

    @validates("nazwa")
    def validate_nazwa(self, key: int, nazwa: str) -> str:
        if nazwa[0].islower():
            raise ValueError("Nazwa nie zaczyna się z wielkiej litery")
        return nazwa


def main() -> None:
    args = sys.argv
    if len(args) == 1:
        print("zobacz 'python ksiazki.py --help'")
        return
    args = args[1:]
    if args[0] == '--help':
        print("""
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
        wypisuje id, imie oraz email
        i wypozyczone ksiazki zapisanych znajomych
--ksiazki
        wypisuje id, tytul, autora oraz rok wydania zapisanych ksiazek
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
        if args[0] == '--dodaj-k':
            session.add(Ksiazka(int(args[1]), args[2],
                                int(args[3]), int(args[4])))
        if args[0] == '--dodaj-a':
            session.add(Autor(int(args[1]), args[2]))
        if args[0] == '--dodaj-z':
            session.add(Znajomy(int(args[1]), args[2], args[3]))
        if args[0] == '--wypozycz':
            id_znaj = int(args[1])
            id_ksia = int(args[2])
            stmt = select(Ksiazka).where(Ksiazka.k_id == id_ksia)
            ksiazka = session.scalars(stmt).one()
            ksiazka.uzytkownik_id = id_znaj
        if args[0] == '--zwroc':
            id_ksia = int(args[1])
            stmt = select(Ksiazka).where(Ksiazka.k_id == id_ksia)
            ksiazka = session.scalars(stmt).one()
            ksiazka.uzytkownik_id = None
        if args[0] == '--znajomi':
            res = []
            znajomi = session.query(Znajomy).all()
            for el in znajomi:
                res.append(str(el) + " " + str(el.ksiazki))
            print(res)
        if args[0] == '--ksiazki':
            res = []
            ksiazki = session.query(Ksiazka).all()
            for el in ksiazki:
                res.append(str(el))
            print(res)
        if args[0] == '--autorzy':
            res = []
            autorzy = session.query(Autor).all()
            for el in autorzy:
                tab = []
                for k in el.ksiazki:
                    tab.append(k.tytul)
                res.append(str((el, tab)))
            print(res)
        if args[0] == '--autorzy-API':
            print(server.autorzy_read())
        if args[0] == '--znajomi-API':
            print(server.znajomi_read())
        if args[0] == '--ksiazki-API':
            print(server.ksiazki_read())
        if args[0] == '--autorzy-delete':
            server.autorzy_delete(int(args[1]))
        if args[0] == '--autorzy-update':
            server.autorzy_update(int(args[1]), args[2])
        if args[0] == '--dodaj-a-API':
            server.autorzy_create(int(args[1]), args[2])

        session.commit()
        session.close()


engine = create_engine("sqlite:///ksiazki.db", echo=False)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    main()
