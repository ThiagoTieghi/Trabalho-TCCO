# Trabalho Final
# Software de conversão de sentenças de autômato finito não-determinístico (AFND)
#em determinístico (AFD) minimizado;
# Matéria: Teoria da Computação
# Dupla: Rebecca Paulino e Thiago Tieghi

import pandas as pd

# Inicialização da AFN
afn = {}

# Inserção dos dados
numero_estados = int(input("Insira o número de estados: "))
qtd_arestas = int(input("Insira o número de arestas: "))

for i in range(numero_estados):
  estado = input("Insira o estado: ")
  afn[estado] = {}
  for j in range(qtd_arestas):
    aresta = input("Insira o aresta: ")
    print("Insira o próximo estado de {} para {}: ".format(estado, aresta))
    # Lista com a informação inserida pelo usuário
    encontrando_estado = [x for x in input().split()]
    afn[estado][aresta] = encontrando_estado

# Imprime a AFN em forma de tabela
print("\n\nTabela AFN")
tabela_afn = pd.DataFrame(afn)
print(tabela_afn.transpose())

# Estado Final
print("\nInsira o estado final da AFN: ")
estadoFinal_afn = [x for x in input().split()]

###### AFD ######

# Inicialização da AFD
novos_estados = []
afd = {}
transiçoes = list(list(afn.keys())[0])
lista_aresta = list(afn[transiçoes[0]].keys())
afd[transiçoes[0]] = {}

# Contrução da tabela de transição
for y in range(qtd_arestas):

  # Criação de estados que serão analisados
  possiveis_estados = "".join(afn[transiçoes[0]][lista_aresta[y]])
  afd[transiçoes[0]][lista_aresta[y]] = possiveis_estados

  # Inclusão dos novos estados encontrados
  if possiveis_estados not in transiçoes:
    novos_estados.append(possiveis_estados)
    transiçoes.append(possiveis_estados)

while len(novos_estados) != 0:
  # Inicialização da tabela de transição
  afd[novos_estados[0]] = {}

  # Iteração dos arestas
  for _ in range(len(novos_estados[0])):
    for i in range (len(lista_aresta)):
      lista = []
      for j in range (len(novos_estados[0])):
        # Lista de estados alcançáveis
        lista += afn[novos_estados[0][j]][lista_aresta[i]]
        novo_estado =""
        novo_estado = novo_estado.join(lista)
        
        if novo_estado not in transiçoes:
          novos_estados.append(novo_estado)
          transiçoes.append(novo_estado)
        afd[novos_estados[0]][lista_aresta[i]] = novo_estado

  novos_estados.remove(novos_estados[0])

print("\n\nTabela AFD")
tabela_afd = pd.DataFrame(afd)
tabela_afd_transposta = tabela_afd.transpose()
print(tabela_afd_transposta)

# Encontrando o estado final
estado_afd = list(afd.keys())
estadoFinal_afd = []
for x in estado_afd:
  for i in x:
    if i in estadoFinal_afn:
      estadoFinal_afd.append(x)
      break

print("\nEstados finais de AFD: ", estadoFinal_afd)

######  AFD Minimizado  ######

# Verificar e agrupar linhas com colunas iguais
colunas_iguais = []

for i in range(len(tabela_afd_transposta.columns)):
    for j in range(i + 1, len(tabela_afd_transposta.columns)):
        if (tabela_afd_transposta.iloc[:, i] == tabela_afd_transposta.iloc[:, j]).all():
            colunas_iguais.append((i, j))

# Criar uma nova tabela agrupando linhas com colunas iguais
tabela_afd_min = tabela_afd_transposta.drop_duplicates()

for colunas in colunas_iguais:
    tabela_afd_min = tabela_afd_min.append(
        tabela_afd_transposta.iloc[:, colunas[0]].copy(), ignore_index=True)

print("\n\nTabela AFD Minimizada")  
print(tabela_afd_min)
print("\n")