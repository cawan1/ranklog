#This version use variables to handle data
import operator
import time
start_time = time.time()

print "Hello World!"


nagioslogfile = 'nagioslog13141516-1.log'
arquivodesaida = 'ranking_V2.txt'
global contador
contador = {}

def abrirArquivos():
    global lognagios
    global logsaida
    lognagios = open(nagioslogfile)
    logsaida =  open(arquivodesaida, 'w')

def fecharArquivos():
    lognagios.close()
    logsaida.close()

#Acha a maior linha
def maiorLinha():
    abrirArquivos()
    maiorlinha = ''
    for i in lognagios:
        if len(i) > len(maiorlinha):
            maiorlinha = i
    logsaida.write(maiorlinha)
    fecharArquivos()
#maiorLinha()

def filtrarLinhas(linha):
        linha = linha.split(';')  #separa por ';'
        linha[0] = linha[0].split(' ')  #separa primeira coluna
        if linha[0][6] == 'ALERT:': #Mantem apenas alertas
            del linha[0][5:7] #Mantem apenas data e host na primeira coluna
            linha[0][0] = ' '.join(linha[0][0:5]) #Configura a data
            del linha[0][1:5]
            linha.insert(1,linha[0][0])
            linha.insert(2,linha[0][1])
            del linha[0]
            if linha[4] == 'HARD': #Filtra por alarme do tipo HARD
                # del linha[(len(linha)-3):]
                linha = ';'.join(linha[:]) #+ '\n' #Monta linha dividindo colunas por ';'
                return linha
            else:
                pass
        else:
            pass

def preparaRanking(i):
        i = i.split(';') # separa linha por ';'
        del i[0] #remove datas
        del i[(len(i)-3):] # remove detalhes do alarme
        i = ';'.join(i[:]) #+ '\n'
        return i


def contaRank(alarme):
    if alarme not in contador.keys(): #verifica se o alarme existe no dicionario, se nao, adiciona a key com o valor 1
        contador[alarme]=1
    else: # se sim soma 1 ao valor
        contador[alarme] += 1 
    ranking = sorted(contador.items(), key=operator.itemgetter(1), reverse=True) #Ordena de forma decrescente pelos Values
    return ranking

def inverteRank(ranking):
    final_rank = []
    for i, j in ranking: #Inverte Values e Keys e escreve em arquivo
        linha = str(j) + ' ' + str(i) + '\n'
        final_rank.append(linha)
    return final_rank

lista_rank = []

abrirArquivos()
for linha in lognagios:
    escreva = filtrarLinhas(linha)
    if escreva is not None:
       escreva = preparaRanking(escreva)
       lista_rank.append(escreva)
for i in lista_rank:
    ranking = contaRank(i)

final_rank = inverteRank(ranking)

for i in range(len(final_rank)):
    logsaida.write(final_rank[i])

fecharArquivos()

print("--- %s seconds ---" % (time.time() - start_time))
