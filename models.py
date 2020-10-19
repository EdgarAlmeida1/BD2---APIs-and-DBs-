# coding: utf-8
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import re

Base = declarative_base()
metadata = Base.metadata


class League(Base):
    __tablename__ = 'league'

    id_liga = Column(Integer, primary_key=True)
    nome_liga = Column(String(50), nullable=False)
    nome_alternativo_liga = Column(String(100))
    ano_formacao_liga = Column(Integer, nullable=False)
    pais_liga = Column(String(50), nullable=False)
    descricao = Column(String(5000), nullable=False)


class Team(Base):
    __tablename__ = 'team'

    id_time = Column(Integer, primary_key=True)
    nome_time = Column(String(100), nullable=False)
    ano_formacao_time = Column(Integer, nullable=False)
    estadio_time = Column(String(100))
    pais_time = Column(String(50), nullable=False)
    liga_time = Column(ForeignKey('league.id_liga'), nullable=False)

    league = relationship('League')


class Game(Base):
    __tablename__ = 'game'

    id_partida = Column(Integer, primary_key=True)
    nome_partida = Column(String(100), nullable=False)
    data_partida = Column(Date)
    local_partida = Column(String(100))
    time_casa = Column(ForeignKey('team.id_time'), nullable=False)
    time_visitante = Column(ForeignKey('team.id_time'), nullable=False)
    pontos_time_casa = Column(Integer, nullable=False)
    visitante_time_casa = Column(Integer, nullable=False)
    hora_partida = Column(Time)

    team = relationship('Team', primaryjoin='Game.time_casa == Team.id_time')
    team1 = relationship('Team', primaryjoin='Game.time_visitante == Team.id_time')


class Player(Base):
    __tablename__ = 'player'

    id_jogador = Column(Integer, primary_key=True)
    id_time = Column(ForeignKey('team.id_time'), nullable=False)
    nome_jogador = Column(String(100), nullable=False)
    nacionalidade_jogador = Column(String(50), nullable=False)
    data_nasc_jogador = Column(Date, nullable=False)
    genero_jogador = Column(String(20), nullable=False)
    altura_jogador = Column(Float(53))
    peso_jogador = Column(Float(53))

    team = relationship('Team')

    def convertHeight(height):
        nums = re.findall(r'\d+', height)

        if(len(nums) > 0):
            h_ft = int(nums[0])
            h_inch = 0
            if(len(nums) > 1):
                h_inch = int(nums[1])

            h_inch += h_ft * 12
            return round(h_inch * 2.54/100, 1)
        else:
            return None

    def convertWeight(weight):
        nums = re.findall(r'\d+', weight)

        if(len(nums) > 0):
            return round(int(nums[0]) * 0.454, 1)
        else:
            return None


class TeamLeague(Base):
    __tablename__ = 'team_league'

    id_time = Column(ForeignKey('team.id_time'), primary_key=True, nullable=False)
    id_liga = Column(ForeignKey('league.id_liga'), primary_key=True, nullable=False)
    nome_time = Column(String(50))
    nome_liga = Column(String(50))

    league = relationship('League')
    team = relationship('Team')
