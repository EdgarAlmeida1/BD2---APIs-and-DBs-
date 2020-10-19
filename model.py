import json
import requests
from decimal import Decimal
from DAO import *

class Ligas:
    @staticmethod
    def consultaLiga(id):
        sessao = DAOGenerico.getSession()
        sessao.expire_on_commit = False
        result = DAOLiga.consultaLiga(sessao, id)
        sessao.commit()
        sessao.close()
        return result

    @staticmethod
    def allLeagues():
        sessao = DAOGenerico.getSession()
        sessao.expire_on_commit = False
        leagues = DAOLiga.allLeagues(sessao)
        sessao.commit()
        sessao.close()
        return leagues

    @staticmethod
    def getLeagues():
        print("Requisitando ligas...")
        response = requests.get("https://www.thesportsdb.com/api/v1/json/1/all_leagues.php")
        leagues = response.json()['leagues']

        print("Adicionando ligas no banco de dados...")
        for league in leagues:
            if league['strSport'] == 'Basketball':
                response = requests.get(
                    "https://www.thesportsdb.com/api/v1/json/1/lookupleague.php?id=" + league['idLeague'])
                leagueDetails = response.json()['leagues'][0]

                liga = League(id_liga=int(leagueDetails['idLeague']),
                              nome_liga=leagueDetails['strLeague'],
                              nome_alternativo_liga=leagueDetails['strLeagueAlternate'],
                              ano_formacao_liga=int(leagueDetails['intFormedYear']),
                              pais_liga=leagueDetails['strCountry'],
                              descricao=leagueDetails['strDescriptionEN'])

                if not Ligas.consultaLiga(liga.id_liga):
                    sessao = DAOGenerico.getSession()
                    DAOGenerico.insere(sessao, liga)
                    sessao.commit()
                    sessao.close()

                    print("Inserido a liga " + leagueDetails['strLeague'])

        print("Terminou!\n")

    @staticmethod
    def leaguesObjToJSONObj(ligas):
        leaguesToSave = []
        for liga in ligas:
            attrs = vars(liga)
            ligaToAdd = {}
            for [item, value] in attrs.items():
                if item != "_sa_instance_state":
                    ligaToAdd[item] = value

            if (ligaToAdd["id_liga"] != None):
                leaguesToSave.append(ligaToAdd)

        with open('League.json', 'w') as arquivo:
            json.dump(leaguesToSave, arquivo)

class Times:
    @staticmethod
    def consultaTime(id):
        sessao = DAOGenerico.getSession()
        sessao.expire_on_commit = False
        result = DAOTime.consultaTime(sessao, id)
        sessao.commit()
        sessao.close()
        return result

    @staticmethod
    def consultaTimeLiga(idTime, idLiga):
        sessao = DAOGenerico.getSession()
        sessao.expire_on_commit = False
        result = DAOTime.consultaTimeLiga(sessao, idTime, idLiga)
        sessao.commit()
        sessao.close()
        return result

    @staticmethod
    def allTeams():
        sessao = DAOGenerico.getSession()
        sessao.expire_on_commit = False

        teams = DAOTime.allTeams(sessao)
        sessao.commit()
        sessao.close()
        return teams

    @staticmethod
    def allTeamLeagues():
        sessao = DAOGenerico.getSession()
        sessao.expire_on_commit = False

        teamleagues = DAOTime.allTeamLeagues(sessao)
        sessao.commit()
        sessao.close()
        return teamleagues

    @staticmethod
    def getTeams(liga, idliga):
        print("Requisitando times da liga " + liga)
        response = requests.get("https://www.thesportsdb.com/api/v1/json/1/search_all_teams.php?l=" + liga)
        teams = response.json()['teams']


        if (teams is not None):
            print("Inserindo times no banco de dados...")
            for team in teams:
                response = requests.get("https://www.thesportsdb.com/api/v1/json/1/lookupteam.php?id=" + team['idTeam'])
                teamDetails = response.json()['teams'][0]

                time = Team(id_time=int(teamDetails['idTeam']),
                            nome_time=teamDetails['strTeam'],
                            ano_formacao_time=int(teamDetails['intFormedYear']) if teamDetails['intFormedYear'] is not None else 0,
                            estadio_time=teamDetails['strStadium'],
                            pais_time=teamDetails['strCountry'],
                            liga_time=int(idliga))


                if not Times.consultaTime(time.id_time):
                    sessao = DAOGenerico.getSession()
                    DAOGenerico.insere(sessao, time)

                    sessao.commit()
                    sessao.close()
                    print("Inserido o time " + teamDetails['strTeam'])

                time_liga = TeamLeague(id_time=int(teamDetails['idTeam']),
                                       id_liga=int(idliga),
                                       nome_time=teamDetails['strTeam'],
                                       nome_liga=liga)


                if not Times.consultaTimeLiga(time_liga.id_time, time_liga.id_liga):
                    sessao = DAOGenerico.getSession()
                    DAOGenerico.insere(sessao, time_liga)
                    sessao.commit()
                    sessao.close()

                    print("Inserido ligacao entre time " + teamDetails['strTeam'] + " e liga " + liga)

        print("Terminou!")

    @staticmethod
    def teamsObjToJSONObj(times):
        teamsToSave = []
        for time in times:
            attrs = vars(time)
            timeToAdd = {}
            for [item, value] in attrs.items():
                if item != "_sa_instance_state":
                    timeToAdd[item] = value

            if (timeToAdd["id_time"] != None):
                teamsToSave.append(timeToAdd)

        with open('Team.json', 'w') as arquivo:
            json.dump(teamsToSave, arquivo)

    @staticmethod
    def teamleaguesObjToJSONObj(times_ligas):
        team_leaguesToSave = []
        for time_liga in times_ligas:
            attrs = vars(time_liga)
            time_ligaToAdd = {}
            for [item, value] in attrs.items():
                if item != "_sa_instance_state":
                    time_ligaToAdd[item] = value

            if (time_ligaToAdd["id_time"] != None and time_ligaToAdd["id_liga"] != None):
                team_leaguesToSave.append(time_ligaToAdd)

        with open('TeamLeague.json', 'w') as arquivo:
            json.dump(team_leaguesToSave, arquivo)

class Jogadores:
    @staticmethod
    def consultaJogador(id):
        sessao = DAOGenerico.getSession()
        sessao.expire_on_commit = False

        result = DAOJogador.consultaJogador(sessao, id)
        sessao.commit()
        sessao.close()
        return result

    @staticmethod
    def allPlayers():
        sessao = DAOGenerico.getSession()
        sessao.expire_on_commit = False

        players = DAOJogador.allPlayers(sessao)
        sessao.commit()
        sessao.close()
        return players

    @staticmethod
    def getPlayers(time):
        print("Requisitando jogadores do time " + time)
        response = requests.get('https://www.thesportsdb.com/api/v1/json/1/searchplayers.php?t=' + time + '&p=%%')
        players = response.json()['player']

        if (players is not None):
            print("Inserindo jogadores no banco de dados...")
            for player in players:
                ##print(player['strHeight'], player['strWeight'])
                if player['strSport'] != "Basketball" or not Times.consultaTime(int(player['idTeam'])):
                    continue
                else:
                    height = None
                    weight = None
                    if player['strHeight'] is not None and len(str(player['strHeight'])) > 0:
                        height = Player.convertHeight(player['strHeight'])
                        if height is not None:
                            Decimal(height)

                    if player['strWeight'] is not None and len(str(player['strWeight'])) > 0:
                        weight = Player.convertWeight(player['strHeight'])
                        if weight is not None:
                            Decimal(weight)

                    jogador = Player(id_jogador=int(player['idPlayer']),
                                     id_time=int(player['idTeam']),
                                     nome_jogador=player['strPlayer'],
                                     nacionalidade_jogador=player['strNationality'],
                                     data_nasc_jogador=player['dateBorn'],
                                     genero_jogador=player['strGender'],
                                     altura_jogador=height,
                                     peso_jogador=weight,
                                     )
                    if not Jogadores.consultaJogador(jogador.id_jogador):
                        sessao = DAOGenerico.getSession()
                        DAOGenerico.insere(sessao, jogador)
                        sessao.commit()
                        sessao.close()

                        print("Inserido jogador " + player['strPlayer'])

        print("Terminou!")

    @staticmethod
    def playersObjToJSONObj(jogadores):
        playersToSave = []
        for jogador in jogadores:
            attrs = vars(jogador)
            jogadorToAdd = {}
            for [item, value] in attrs.items():
                if (str(type(value)) == "<class 'datetime.date'>"):
                    jogadorToAdd[item] = str(value)
                elif item != "_sa_instance_state":
                    jogadorToAdd[item] = value

            if (jogadorToAdd["id_jogador"] != None):
                playersToSave.append(jogadorToAdd)

        with open('Player.json', 'w') as arquivo:
            json.dump(playersToSave, arquivo)

class Jogos:
    @staticmethod
    def consultaJogo(id):
        sessao = DAOGenerico.getSession()
        sessao.expire_on_commit = False

        result = DAOJogo.consultaJogo(sessao, id)
        sessao.commit()
        sessao.close()
        return result

    @staticmethod
    def allGames():
        sessao = DAOGenerico.getSession()
        sessao.expire_on_commit = False

        games = DAOJogo.allGames(sessao)
        sessao.commit()
        sessao.close()
        return games

    @staticmethod
    def getGames(time):
        print("Requisitando jogos do time " + str(time))

        response = requests.get('https://www.thesportsdb.com/api/v1/json/1/eventslast.php?id=' + str(time))
        games = response.json()['results']

        if (games is not None):
            print("Inserindo jogos no banco de dados...")
            for game in games:
                if (game['strSport'] == "Basketball" and Times.consultaTime(int(game['idHomeTeam'])) and Times.consultaTime(int(game['idAwayTeam']))):
                    jogo = Game(
                        id_partida=int(game['idEvent']),
                        nome_partida=game['strEvent'],
                        data_partida=game['dateEvent'],
                        local_partida=game['strVenue'],
                        time_casa=game['idHomeTeam'],
                        time_visitante=game['idAwayTeam'],
                        pontos_time_casa=int(game['intHomeScore']) if game['intHomeScore'] is not None else 0,
                        visitante_time_casa=int(game['intAwayScore']) if game['intAwayScore'] is not None else 0,
                        hora_partida=game['strTime'].split(' ', 1)[0] if game['strTime'] is not None and len(
                            game['strTime']) > 0 else None
                    )

                    if not Jogos.consultaJogo(jogo.id_partida):
                        sessao = DAOGenerico.getSession()
                        DAOGenerico.insere(sessao, jogo)
                        sessao.commit()
                        sessao.close()

                        print("Inserido jogo " + game['strEvent'] + 'de id ' + game['idEvent'])

        print("Terminou!")

    @staticmethod
    def gamesObjToJSONObj(jogos):
        gamesToSave = []
        for jogo in jogos:
            attrs = vars(jogo)
            jogoToAdd = {}
            for [item, value] in attrs.items():
                if (str(type(value)) == "<class 'datetime.date'>" or str(type(value)) == "<class 'datetime.time'>"):
                    jogoToAdd[item] = str(value)
                elif item != "_sa_instance_state":
                    jogoToAdd[item] = value

            if (jogoToAdd["id_partida"] != None):
                gamesToSave.append(jogoToAdd)

        with open('Game.json', 'w') as arquivo:
            json.dump(gamesToSave, arquivo)