'''
---- Simulador MMU ----
Autor: Roger Rothmund
Matricula: 48032

Curso de Ciência da Computação
Disciplina: Sistemas Operacionais
'''

import os
from copy import deepcopy

tam = 256 #tamanho inicial da memoria em bytes
memoria = [None]*tam
particaoLivreLst = []

def main():
	#Inicia a lista de espaços livres
	updatePartLivre()
	
	while True:
		os.system('cls' if os.name == 'nt' else 'clear') 
		print("**** Simulador de gerenciamento de memória ****")
		print("1 - Iniciar simulação manual")
		print("2 - Iniciar simulação atravez de arquivo de entrada")
		print("3 - Configuração da Memoria")
		print("4 - Sair")
		opcaoMenuPrinc = int(input())
	
		if opcaoMenuPrinc == 1:
			while True:
				os.system('cls' if os.name == 'nt' else 'clear') 
				print("==== Simulação manual ====")
				print("1 - Print da memoria")
				print("2 - Adicionar novo Processo")
				print("3 - Remover Processo")
				print("4 - Compactar Memoria")
				print("5 - Exportar \'.txt\' com print da memoria e todos os processos")
				print("6 - Voltar")
				opcaoSimMan = int(input())

				if opcaoSimMan == 1:
					printMemoria()
					printPartLivre()
					input("\nPressione ENTER para continuar...")

				elif opcaoSimMan == 2:
					print("\n-- Selecione o critério de alocação --")
					print("1 - First-fit")
					print("2 - Best-fit")
					print("3 - Worst-fit")
					critAlocacao = int(input())

					if critAlocacao > 0 and critAlocacao < 4:
						print("\nInformações do Processo:")
						nome = input("Nome: ")
						tamanhoProc = int(input("Tamanho: "))
						novoProcesso(nome, tamanhoProc, critAlocacao) #1 firstFit, 2 bestFit, 3 worstFit

						printMemoria()
						printPartLivre()
						input("\nPressione ENTER para continuar...")
					else:
						print("\nCritério de alocação invalido!")
						input("\nPressione ENTER para continuar...")

				elif opcaoSimMan == 3:
					print("\n-- Remover Processo --")
					procNome = input("Nome do processo: ")
					killProcesso(procNome)
					input("\nPressione ENTER para continuar...")

				elif opcaoSimMan == 4:
					compactarMemoria()
					print('\nCompactação realizada com sucesso!')
					printMemoria()
					printPartLivre()
					input("\nPressione ENTER para continuar...")

				elif opcaoSimMan == 5:
					input("\nArquivo \'viewMemoria.txt\' exportado no local: "+os.path.dirname(os.path.realpath(__file__))+"\nPressione ENTER para continuar...")
					exportaMemoriaArquivo()

				elif opcaoSimMan == 6:
					break;
			
		elif opcaoMenuPrinc == 2:
			print("\n==== Iniciar simulação atravez de arquivo de entrada ====")

			input("\nAdicione, caso não exista, o arquivo \'entrada.txt\' no local: "+os.path.dirname(os.path.realpath(__file__))+"\nApós pressione ENTER para continuar...")
			#Pega o arquivo entrada.txt da mesma pasta onde o arquivo Python se encontra
			pathFile = os.path.dirname(os.path.realpath(__file__))+'\\entrada.txt'
			entrada = trataEntrada(pathFile)

			if 'Erro' in entrada:
				input("\nArquivo não encontrado! Pressione ENTER para continuar...")
			else:
				simulaPorArq(entrada)
				input("\nLog gerado com sucesso! Pressione ENTER para continuar...")

		elif opcaoMenuPrinc == 3:
			print("\n==== Configuração da Memoria ====")
			print("Tamanho: ", len(memoria))

			alteraSize = input("\nPressione ENTER para continuar ou digite SIZE para alterar o tamanho da memória...")
			if alteraSize == 'SIZE':
				newSize = int(input("\nNovo tamaho: "))
				tamanhoMemoria(newSize)

		elif opcaoMenuPrinc == 4:
			quit()
		else:
			print('Alternativa inexistente!')

## Funcoes
def tamanhoMemoria(tam):
	#Função responsavel por alterar o tamanho da Memória
	memoria.clear()
	for i in range(tam):
		memoria.append(None)

	updatePartLivre()
	
def addProcesso(posInicio, posFim, processo):
	processo.posInicio = posInicio
	processo.posFim = posFim

	for x in range(len(memoria)):
		if posInicio <= x and x <= posFim:
			memoria[x] = processo

	updatePartLivre()

def killProcesso(procNome, msg=1):
	encontrado = False
	for x in range(len(memoria)):
		if type(memoria[x]) is Processo:
			if memoria[x].nome == procNome:
				encontrado = True
				for y in range(memoria[x].posInicio, (memoria[x].posFim+1)):
					memoria[y] = None
				break;
	if encontrado == True:
		if msg == 1:
			print('\nPrecesso', procNome, 'removido com sucesso!')
		updatePartLivre()
	else:
		if msg == 1:
			print('\nPrecesso', procNome, 'não encontrado!')

def novoProcesso(nome, tamanhoProc, tipoAlocacao):
	novoProcesso = Processo(nome, tamanhoProc, 0, 0, 0, 0) #nome, tamanho, instanteInicio, duracao, posInicio, posFim

	if tipoAlocacao == 1:
		firstFit(novoProcesso)

	elif tipoAlocacao == 2:
		bestFit(novoProcesso)

	elif tipoAlocacao == 3:
		worstFit(novoProcesso)
	else:
		print('Criterio de alocação inválido!')

def updatePartLivre():
	#Atualiza lista com as partições (espaços) livres
	particaoLivreLst.clear()
	inicio = 0
	fim = 0
	tam = 0
	for x in range(len(memoria)):
		if memoria[x] == None and x == 0:
			inicio = x
			fim = x
			tam = 1 + (fim - inicio)

		elif memoria[x] == None and type(memoria[x-1]) is Processo  and x > 0:
			inicio = x
			fim = x
			tam = 1 + (fim - inicio)

		elif memoria[x] == None and x > 0 and tam > 0:
			fim = x
			tam = 1 + (fim - inicio)

		elif memoria[x] != None:
			if tam > 0:
				particao = particaoLivre(inicio, fim, tam)
				particaoLivreLst.append(particao)
				inicio = 0
				fim = 0
				tam = 0
				
		if len(memoria) == x+1 and tam > 0:
			particao = particaoLivre(inicio, fim, tam)
			particaoLivreLst.append(particao)
			inicio = 0
			fim = 0
			tam = 0

def printPartLivre():
	#Print na tela com as partições (espaços) livres
	print('\n\nEspaços livres disponíveis: ')
	for x in range(len(particaoLivreLst)):
		print(str(x+1), '-> Inicio: ',particaoLivreLst[x].inicio,'| Fim: ',particaoLivreLst[x].fim,'| Size: ',particaoLivreLst[x].tamanho)

def retornaPartLivre():
	#Retorna string para o Log com as partições (espaços) livres
	log = []
	for x in range(len(particaoLivreLst)):
		log.append(str(particaoLivreLst[x].inicio)+' - '+str(particaoLivreLst[x].fim))
		if x != len(particaoLivreLst)-1:
			log.append(', ')
	return(''.join(log))

def printMemoria():
	#Print na tela da Memória, com espaços preenchidos por processo ou livres
	print('\nTamanho da Memória:', len(memoria), '\n')
	for x in range(len(memoria)):
		if x == 0:
			if memoria[x] != None:
				print('(',memoria[x].nome, ')', end = "")
			else:
				print('( -- )', end = "")
		else:
			if memoria[x] != None:
				print('\t(',memoria[x].nome, ')', end = "")
			else:
				print('\t( -- )', end = "")
			
def compactarMemoria():
	#Compactação da Memória, os processos são realocados, removendo os espaços livres
	posLivre = None

	for x in range(len(memoria)):
		if memoria[x] == None:
			posLivre = x
			for y in range(posLivre, len(memoria)-1):
				if type(memoria[y]) is Processo:
					processo = memoria[y]
					killProcesso(processo.nome, 0)
					posFim = (processo.tamanho + posLivre) - 1
					addProcesso(posLivre, posFim, processo)
					auxSaida = True
					break;
	#Finalizando é atualizado a lista de partições (espaços) livres
	updatePartLivre()

def trataEntrada(pathFile):
	#Trata o arquivo de entrada, utilizado na simulação
	#Os dados são transferidos para uma lista
	try:
		f = open(pathFile, 'r')
		entradaAux = f.readlines()
		entrada = []
		
		for x in range(len(entradaAux)):
			entrada.append( entradaAux[x].replace("\n", "").strip().split(",") )

		f.close
		return entrada
	except FileNotFoundError as e:
		return 'Erro'

def firstFit(processo, msg=0):
	procSize = processo.tamanho
	posInicio = 0
	posFim = 0
	tamAux = 0
	espacoNaoEncontrado = 0
	#Verifica todos os nodos da memória, até encontrar um espaço livre, representado por None
	#Apos verifica se apartir deste ponto há o espaço necessario para o processo
	for x in range(len(memoria)):
		if memoria[x] == None:
			tamAux += 1
			if tamAux == procSize:
				posFim = x
				posInicio = (posFim+1) - procSize
				addProcesso(posInicio, posFim, processo) #adiciona processo na memoria
				break;
		else:
			tamAux = 0
			if x == 0:
				espacoNaoEncontrado += 1
			elif type(memoria[x-1]) is Processo and memoria[x] is None: 
				espacoNaoEncontrado += 1
			elif type(memoria[x-1]) is Processo and memoria[x-1].nome != memoria[x].nome:
				espacoNaoEncontrado += 1
	
	if tamAux < procSize:
		espacoNaoEncontrado += 1
		if msg == 1:
			return "Erro! Não foi possivel adicionar o processo.", processo.nome, ' - Tentativas: ',espacoNaoEncontrado
		else:
			print("Erro! Não foi possivel adicionar o processo.", processo.nome, ' - Tentativas: ',espacoNaoEncontrado)
	else:
		if msg == 1:
			return 'Adicionar o processo.', processo.nome, ' - Tentativas: ',espacoNaoEncontrado, ' -  posInicio: ', posInicio, ' -  posFim: ',posFim

def bestFit(processo, msg=0):
	procSize = processo.tamanho 
	melhorTamanho = 1000000
	melhorPart = None
	espacoNaoEncontrado = 0
	#Com o auxilio da lista de partições (espaços) livres é verificado se há o espaço nescessario para o processo
	#No bestFit o processo é alocado na partição que mais se aproximar ao tamaho do processo
	for x in range(len(particaoLivreLst)):
		particao = particaoLivreLst[x]

		if particao.tamanho >= procSize and particao.tamanho < melhorTamanho:
			melhorTamanho = particao.tamanho
			melhorPart = x
		else:
			espacoNaoEncontrado += 1

	if melhorPart != None:
		posFim = (particaoLivreLst[melhorPart].inicio + procSize) - 1
		posInicio = particaoLivreLst[melhorPart].inicio
		addProcesso(particaoLivreLst[melhorPart].inicio, posFim, processo) #adiciona processo na memoria
		if msg == 1:
			return 'Adicionar o processo.', processo.nome, ' - Tentativas: ',espacoNaoEncontrado, ' -  posInicio: ', posInicio, ' -  posFim: ',posFim
	else:
		if msg == 1:
			return "Erro! Não foi possivel adicionar o processo.", processo.nome, ' - Tentativas: ',espacoNaoEncontrado
		else:
			print("Erro! Não foi possivel adicionar o processo.", processo.nome, ' - Tentativas: ',espacoNaoEncontrado)

def worstFit(processo, msg=0):
	procSize = processo.tamanho 
	piorTamanho = 0
	piorPart = None
	espacoNaoEncontrado = 0
	#Com o auxilio da lista de partições (espaços) livres é verificado se há o espaço nescessario para o processo
	#No worstFit o processo é alocado na maior partição disponivel
	for x in range(len(particaoLivreLst)):
		particao = particaoLivreLst[x]

		if particao.tamanho >= procSize and particao.tamanho > piorTamanho:
			piorTamanho = particao.tamanho
			piorPart = x
		else:
			espacoNaoEncontrado += 1

	if piorPart != None:
		posFim = (particaoLivreLst[piorPart].inicio + procSize) - 1
		posInicio = particaoLivreLst[piorPart].inicio
		addProcesso(particaoLivreLst[piorPart].inicio, posFim, processo) #adiciona processo na memoria
		if msg == 1:
			return 'Adicionar o processo.', processo.nome, ' - Tentativas: ',espacoNaoEncontrado, ' -  posInicio: ', posInicio, ' -  posFim: ',posFim
	else:
		if msg == 1:
			return "Erro! Não foi possivel adicionar o processo.", processo.nome, ' - Tentativas: ',espacoNaoEncontrado
		else:
			print("Erro! Não foi possivel adicionar o processo.", processo.nome, ' - Tentativas: ',espacoNaoEncontrado)

def simulaPorArq(entrada):
	log = [] #Lista de log responsavel pelo arquivo .txt
	memSize = len(memoria)
	memoria.clear() #É esvaziado a memoria, garantindo que seja lido somente a partir do arquivo de entrada
	filaExec = [] #Iniciado fila de execução, foi o escalonado adotado para a simulação de execução
	for i in range(memSize):
		memoria.append(None)#Inicia a memoria com os espaços livres

	log.append('Tamanho da Memória: '+str(len(memoria))+' bytes\n')#Exemplo de adição de mensagem ao Log
	#A simulação roda para os 3 criterios de alocação sequencialmente
	for x in range(0, 3):
		filaExec.clear()
		tempo = 0
		entradaAux = deepcopy(entrada) #É feito uma copia profunda da lista de entrada
		tempoExe = 0
		falhaAlocação = 0
		exitSim = False
		if x == 0: #first-fit
			log.append('\n******************************************\nFirst-fit\n******************************************\n')
		if x == 1: #best-fit
			log.append('\n******************************************\nBest-fit\n******************************************\n')
		if x == 2: #worst-fit
			log.append('\n******************************************\nWorst-fit\n******************************************\n')

		while exitSim == False:
			for y in range(len(entradaAux)):
				if y < len(entradaAux):
					if int(entradaAux[y][2]) == tempo:
						#nome, tamanho, instanteInicio, duracao, posInicio, posFim
						novoProcesso = Processo(entradaAux[y][0], int(entradaAux[y][1]), int(entradaAux[y][2]), int(entradaAux[y][3]), 0, 0)
						
						log.append('T'+str(tempo)+': procurando espaço livre para '+novoProcesso.nome+' ('+str(novoProcesso.tamanho)+' bytes)\n')
						#selecionar critério de alocação
						if x == 0:
							confirm = firstFit(novoProcesso, 1)
						if x == 1:
							confirm = bestFit(novoProcesso, 1)
						if x == 2:
							confirm = worstFit(novoProcesso, 1)

						if 'Erro' in confirm[0]:
							log.append('T'+str(tempo)+': não há espaço livre disponível. Compactando memoria!\n')
							#Compacta memoria e faz nova tentativa
							falhaAlocação += 1
							compactarMemoria()
							#Selecionar critério de alocação
							if x == 0:
								confirm = firstFit(novoProcesso, 1)
							if x == 1:
								confirm = bestFit(novoProcesso, 1)
							if x == 2:
								confirm = worstFit(novoProcesso, 1)

							if 'Erro' in confirm[0]:
								falhaAlocação += 1
								#Como ainda nao ha espaco remove da lista de entrada
								log.append('T'+str(tempo)+': não há espaço livre disponível!\n')
								entradaAux.pop(0)

							else:
								log.append('T'+str(tempo)+': espaço livre encontrado e alocado na posição '+str(confirm[5])+' até ' + str(confirm[7]) +'.\n')
								
								if(len(retornaPartLivre()) > 0):
									log.append('T'+str(tempo)+': espaços livres disponíveis: '+retornaPartLivre()+'\n')
								else:
									log.append('T'+str(tempo)+': espaços livres disponíveis: 0.\n')
								
								#Apos a compactação é encontrado espaço para o processo,
								#então ele é adicionado à lista de execução
								filaExec.append(novoProcesso)
								entradaAux.pop(0)
						else:
							log.append('T'+str(tempo)+': espaço livre encontrado e alocado na posição '+str(confirm[5])+' até ' + str(confirm[7]) +'.\n')
							if(len(retornaPartLivre()) > 0):
								log.append('T'+str(tempo)+': espaços livres disponíveis: '+retornaPartLivre()+'\n')
							else:
								log.append('T'+str(tempo)+': espaços livres disponíveis: 0.\n')
							
							#Há espaço em memória para o processo, então é adicionado à lista de execução
							filaExec.append(novoProcesso)
							entradaAux.pop(0)

			if len(filaExec) > 0: #Controla a execução dos processos
				if tempoExe ==  filaExec[0].duracao:
					#Quando a execução do processo chega ao fim, ele é removido da fila de execução e da Memória
					log.append('T'+str(tempo)+': desalocando: '+filaExec[0].nome+' ('+str(filaExec[0].tamanho)+' bytes)\n')
					killProcesso(filaExec[0].nome, 0)
					filaExec.pop(0)
					tempoExe = 0
				tempoExe += 1 #É contabilizado o tempo de execução do processo que esta em execução, o primeiro da fila


			if len(entradaAux) == 0 and len(filaExec) == 0: #Quando a fila de execução e a lista do arquivo de entrada estiverem vazias, a simulação é concluida
				log.append('\n**Tempo necessário para executar todos os processos: '+str(tempo)+' u.t.\n')
				log.append('**Número de vezes em que não foi encontrado espaço livre: '+str(falhaAlocação)+'\n')
				exitSim = True

			tempo += 1 #tempo total da simulação
			
	log = ''.join(log) #Lista é transformada em uma unica string
	exportaLogArquivo(log)

def exportaLogArquivo(txt):
	#Exporta o log .txt para a mesma pasta onde o arquivo Python se encontra
	saida = open(os.path.dirname(os.path.realpath(__file__))+'\\logMMU.txt', 'w')
	saida.writelines(txt)
	saida.close

def exportaMemoriaArquivo():
	#Exporta uma visualização da Memória em .txt para a mesma pasta onde o arquivo Python se encontra
	saida = open(os.path.dirname(os.path.realpath(__file__))+'\\viewMemoria.txt', 'w')

	log = []
	log.append('Tamanho da Memória:'+ str(len(memoria))+ '\n')
	for x in range(len(memoria)):
		if x == 0 or x % 16 == 0:
			if memoria[x] != None:
				log.append('( '+memoria[x].nome+' )')
			else:
				log.append('( -- )')
		else:
			if memoria[x] != None:
				log.append('\t( '+memoria[x].nome+' )')
			else:
				log.append('\t( -- )')
			#print(' - ', end = "")

		if (x+1) % 16 == 0:
			log.append('\n')

	if particaoLivreLst[0].tamanho != len(memoria):
		log.append('\nProcessos na Memória:\n')

	for x in range(len(memoria)):
		if x == 0:
			if memoria[x] != None:
				log.append('Nome: '+memoria[x].nome+' | Tamanho: '+str(memoria[x].tamanho)+' | Posição Inicial: '+str(memoria[x].posInicio)+' | Posição Final: '+str(memoria[x].posFim)+'\n')
		else:
			if memoria[x] != None:
				if type(memoria[x]) is Processo and memoria[x-1] == None:
					log.append('Nome: '+memoria[x].nome+' | Tamanho: '+str(memoria[x].tamanho)+' | Posição Inicial: '+str(memoria[x].posInicio)+' | Posição Final: '+str(memoria[x].posFim)+'\n')

				if type(memoria[x]) is Processo and memoria[x-1] != None:
					if memoria[x].nome != memoria[x-1].nome:
						log.append('Nome: '+memoria[x].nome+' | Tamanho: '+str(memoria[x].tamanho)+' | Posição Inicial: '+str(memoria[x].posInicio)+' | Posição Final: '+str(memoria[x].posFim)+'\n')

	log = ''.join(log)
	saida.writelines(log)
	saida.close

## Classes
class Processo:
	def __init__(self, nome, tamanho, instanteInicio, duracao, posInicio, posFim):
		self.nome = nome
		self.tamanho = tamanho
		self.instanteInicio = instanteInicio
		self.duracao = duracao
		self.posInicio = posInicio
		self.posFim = posFim

class particaoLivre:
	def __init__(self, inicio, fim, tamanho):
		self.inicio = inicio
		self.fim = fim
		self.tamanho = tamanho

if __name__ == "__main__":
	main()