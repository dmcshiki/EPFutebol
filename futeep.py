from satisfacao_restricoes import Restricao, SatisfacaoRestricoes
import numpy as np

equipe = {
  "Campos FC": {"cidade": "Campos", "torcedores": 23, "classico": False},
  "Guardiões FC": {"cidade": "Guardião", "torcedores": 40, "classico": True},
  "CA Protetores": {"cidade": "Guardião", "torcedores": 20, "classico": False},
  "SE Leões": {"cidade": "Leão", "torcedores": 40, "classico": True},
  "Simba FC": {"cidade": "Leão", "torcedores": 15, "classico": False},
  "SE Granada": {"cidade": "Granada", "torcedores": 10, "classico": False},
  #"CA Lagos": {"cidade": "Lagos", "torcedores": 20, "classico": False},
  #"Solaris RC": {"cidade": "Ponte-do-Sol", "torcedores": 30, "classico": False},
  #"Porto EC": {"cidade": "Porto", "torcedores": 45, "classico": True},
  #"Ferroviária EC": {"cidade": "Campos", "torcedores": 38, "classico": True},
  #"Portuários AA": {"cidade": "Porto", "torcedores": 12, "classico": False},
  #"CA Azedos": {"cidade": "Limões", "torcedores": 18, "classico": False},
  #"SE Escondidos": {"cidade": "Escondidos", "torcedores": 50, "classico": True},
  #"Secretos FC": {"cidade": "Escondidos", "torcedores": 25, "classico": False}
}

RODADAS = (len(equipe)-1) * 2
JOGOS = int(len(equipe)/2)

combinacao_de_todos_jogos = np.empty(RODADAS*JOGOS, dtype=tuple)
cont_combinacao_classicos = 0

aux = 0
for e1 in equipe.keys():
  for e2 in equipe.keys():
    if e1 != e2:
      combinacao_de_todos_jogos[aux] = (e1, e2)
      aux += 1

for e1 in equipe.keys():
  for e2 in equipe.keys():
    if e1 != e2:
      if equipe[e1]["classico"] and equipe[e2]["classico"]:
        cont_combinacao_classicos += 1
      
# Dica 1: Fazer Restrições Genéricas
class UmTimePorRodadaRestricao(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)

  def esta_satisfeita(self, atribuicao):
    jogosPossiveis = atribuicao
    rodadas = {}
    rCidades = {}
    jogosRealizados = {}

    for i in range(RODADAS): # rodadas
      rodadas["R" + str(i)] = set()
      rCidades["R" + str(i)] = set()

    for variavel in jogosPossiveis.keys():
      rodada = variavel[0:2]
      times = jogosPossiveis[variavel]
      if times is not None:
        time1 = times[0]
        time2 = times[1]
        if equipe[time1]["cidade"] in rCidades[rodada]:
          return False
        if time1 in rodadas[rodada] or time2 in rodadas[rodada]:
          return False
        elif f'{time1}{time2}' in jogosRealizados.keys():
          return False
        else:
          rodadas[rodada].add(time1)
          rodadas[rodada].add(time2)
          jogosRealizados[f'{time1}{time2}'] = True
          rCidades[rodada].add(equipe[time1]["cidade"])
    return True

class JogoClassico(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)

  def esta_satisfeita(self, atribuicao):
    jogosPossiveis = atribuicao
    rodadas = {}
    rClassico = {}

    for i in range(RODADAS): # rodadas
      rodadas["R" + str(i)] = set()
      rClassico["R" + str(i)] = set()

    for variavel in jogosPossiveis.keys():
      rodada = variavel[0:2]
      times = jogosPossiveis[variavel]
			
      if times is not None:
        time1 = times[0]
        time2 = times[1]
				
        if equipe[time1]["classico"] in rClassico[rodada] and equipe[time2]["classico"] in rClassico[rodada]:
          return False
        elif equipe[time1]["classico"] and equipe[time2]["classico"]:
          rodadas[rodada].add(time1)
          rodadas[rodada].add(time2)
          rClassico[rodada].add(equipe[time1]["classico"])
          rClassico[rodada].add(equipe[time2]["classico"])
    return True

if __name__ == "__main__":
    variaveis = []
  
    if cont_combinacao_classicos < RODADAS:
      for i in range(RODADAS):
        for j in range(JOGOS):
          # Variável RiJj, tal que i é o número da rodada e j é o jogo da rodada
          variaveis.append("R" + str(i) + "J" + str(j))
        
      dominios = {}
      for variavel in variaveis:
          # o domínio são as combinações de todos os possívels jogos
          dominios[variavel] = combinacao_de_todos_jogos
      
      problema = SatisfacaoRestricoes(variaveis, dominios)
      problema.adicionar_restricao( UmTimePorRodadaRestricao(variaveis) )
      problema.adicionar_restricao( JogoClassico(variaveis) )  
  	
      resposta = problema.busca_backtracking()
      if resposta is None:
        print("Nenhuma resposta encontrada")
      else:
        print("------------------------------\n--------- Campeonato ---------\n------------------------------\n")
        for i in range(RODADAS): # rodadas
          print("\n---------- Rodada " + str(i+1) + " ----------\n")
          for j in range(JOGOS): # jogos
            jogo = resposta["R" + str(i) + "J" + str(j)]
            if equipe[jogo[0]]["classico"] and equipe[jogo[1]]["classico"]:
              print(f'Jogo {j+1}: {jogo[0]} x {jogo[1]} \tCidade: {equipe[jogo[0]]["cidade"]} * Clássico *')  
            else:
              print(f'Jogo {j+1}: {jogo[0]} x {jogo[1]} \tCidade: {equipe[jogo[0]]["cidade"]}')
    else:
      print("Nenhuma resposta encontrada")
