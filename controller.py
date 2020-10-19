from view import View
from model import *

class Controle():
    def __init__(self):
        self.view = View()

    def inicio(self):
        opt = self.view.inicio()

        while opt:
            if opt == 1:
                Ligas.getLeagues()
                ligas = Ligas.allLeagues()
                for liga in ligas:
                    Times.getTeams(liga.nome_liga, liga.id_liga)
                times = Times.allTeams()
                for time in times:
                    Jogadores.getPlayers(time.nome_time)
                    Jogos.getGames(time.id_time)
            elif opt == 2:
                ligas = Ligas.allLeagues()
                times = Times.allTeams()
                times_ligas = Times.allTeamLeagues()
                jogadores = Jogadores.allPlayers()
                jogos = Jogos.allGames()

                Ligas.leaguesObjToJSONObj(ligas)
                Times.teamsObjToJSONObj(times)
                Times.teamleaguesObjToJSONObj(times_ligas)
                Jogadores.playersObjToJSONObj(jogadores)
                Jogos.gamesObjToJSONObj(jogos)

                print("Exportado! \n Os arquivos se encontram na pasta do programa!")
            opt = self.view.inicio()

if __name__ == '__main__':
    ctrl = Controle()
    ctrl.inicio()
