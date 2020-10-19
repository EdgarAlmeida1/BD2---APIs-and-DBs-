from models import League
from models import Team
from models import TeamLeague
from models import Player
from models import Game
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

class DAOGenerico():
    @staticmethod
    def getSession():
        engine = create_engine("postgresql+psycopg2://postgres:root@localhost:5432/trabalho", echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    @staticmethod
    def insere(sessao, obj):
        sessao.add(obj)


class DAOLiga():
    @staticmethod
    def consultaLiga(session, id):
        test = session.query(League).filter(League.id_liga == id).first()
        if (test):
            return 1
        return 0

    @staticmethod
    def allLeagues(session):
        leagues = session.query(League).all()
        session.expunge_all()
        return leagues

class DAOTime():
    @staticmethod
    def consultaTime(session, id):
        test = session.query(Team).filter(Team.id_time == id).first()
        if (test):
            return 1
        return 0

    @staticmethod
    def consultaTimeLiga(session, idTime, idLiga):
        test = session.query(TeamLeague).filter(TeamLeague.id_time == idTime).filter(TeamLeague.id_liga == idLiga).first()
        if (test):
            return 1
        return 0

    @staticmethod
    def allTeams(session):
        teams = session.query(Team).all()
        session.expunge_all()
        return teams

    @staticmethod
    def allTeamLeagues(session):
        teamleagues = session.query(TeamLeague).all()
        session.expunge_all()
        return teamleagues

class DAOJogador():
    @staticmethod
    def consultaJogador(session, id):
        test = session.query(Player).filter(Player.id_jogador == id).first()
        if (test):
            return 1
        return 0

    @staticmethod
    def allPlayers(session):
        players = session.query(Player).all()
        session.expunge_all()
        return players

class DAOJogo():
    @staticmethod
    def consultaJogo(session, id):
        test = session.query(Game).filter(Game.id_partida == id).first()
        if (test):
            return 1
        return 0

    @staticmethod
    def allGames(session):
        games = session.query(Game).all()
        session.expunge_all()
        return games