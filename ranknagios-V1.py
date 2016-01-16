#This version use files to handle data
#from  collections import Counter
import operator
import time
start_time = time.time()

print "Hello World!"

nagioslogfile = 'nagioslog13141516-1.log'
arquivodesaida = 'maiorlinha.txt'
rankingdat = 'ranking.dat'

def abrirArquivos():
    global lognagios
    global logsaida
    lognagios = open(nagioslogfile)
    logsaida =  open(arquivodesaida, 'w')

def fecharArquivos():
    lognagios.close()
    logsaida.close()

def abrirSaida():
    arqsaida =  open(arquivodesaida)

def fecharSaida():
    arqsaida.close()

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

def filtrarLinhas():
    abrirArquivos()
    for linha in lognagios:
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
                logsaida.write(linha)
    fecharArquivos()

filtrarLinhas()

def preparaRanking():
    arqsaida =  open(arquivodesaida)
    rank_saida = open(rankingdat, 'w')
    for i in arqsaida: #prepara arquivo para count
        i = i.split(';')
        del i[0] #remove datas
        del i[(len(i)-3):] # remove detalhes do alarme
        i = ';'.join(i[:]) + '\n'
        rank_saida.write(i)
    arqsaida.close()
    rank_saida.close()

preparaRanking()

def montaRank():
    infile =  open(rankingdat)
    infile2 = open('ranking_V1.txt', 'w')
    contador = {} #dictionary
    j = 0
    for alarme in infile:
        if alarme not in contador.keys(): #verifica se o alarme existe no dicionario, se nao, adiciona a key com o valor 1
            contador[alarme]=1
        else: # se sim soma 1 ao valor
            contador[alarme] += 1 
    ranking = sorted(contador.items(), key=operator.itemgetter(1), reverse=True) #Ordena de forma decrescente pelos Values
    for i, j in ranking: #Inverte Values e Keys e escreve em arquivo
        linha = str(j) + ' ' + str(i)
        infile2.write(linha)
    infile.close()
    infile2.close()
montaRank()


print("--- %s seconds ---" % (time.time() - start_time))
