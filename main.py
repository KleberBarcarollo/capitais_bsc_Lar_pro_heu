# Anulos: Rodrigo Vieira,  Kleber Barcarollo
# Instituição: UTFPF
# Curso: Mestrado em Ciencia da Computação
# Disciplina: Inteligência Artificial - Mestrado UTFPR
# Professor: André Pinz Borges


########################################################################################
# ENUNCIADO                                                                            #
########################################################################################                              
"""
HEURÍSTICA A* (com base no preço do etanol):

Neste projeto, utilizamos uma heurística personalizada para o algoritmo A*,
combinando dois fatores:

1. Diferença no preço do etanol entre a cidade atual e o destino:
   A ideia é que cidades com preços de etanol semelhantes tendem a estar
   geograficamente ou economicamente próximas. Quando a diferença de preço é
   grande, é provável que as cidades estejam mais distantes ou pertençam a
   regiões com logística muito diferente. Essa diferença é normalizada para
   manter os valores comparáveis.

2. Estimativa de saltos mínimos até o destino:
   Usamos a razão entre o número de vizinhos da cidade atual e do destino como
   uma aproximação da "proximidade topológica" no grafo. Isso indica, de forma
   simples, o quanto a cidade atual está conectada e pode levar à cidade final.
   Este fator é multiplicado por um valor fixo (~500 km), representando uma
   média de distância por salto.

A heurística final é uma combinação ponderada desses dois elementos:
- 30% da diferença no preço do etanol.
- 70% da estimativa de saltos em quilômetros.

Essa abordagem nos dá uma estimativa razoável do custo até o destino,
sem exigir cálculos geográficos complexos como coordenadas ou geolocalização.
Ela ajuda o A* a priorizar caminhos mais curtos e economicamente viáveis
de forma simples e eficaz.
"""
# Classe Capital com uma função
class Capital:
    def __init__(self, nome, preco_etanol):
        self.nome = nome
        self.preco_etanol = preco_etanol  # Preço do etanol como peso no grafo
        self.vizinhos = {}  # {capital_vizinha: distância_km}

# classe MapaBrasil
class MapaBrasil:
    def __init__(self):
        self.capitais = {}  # Dicionário de todas as capitais
    
    # Função adiciona Capital
    def adicionar_capital(self, nome, preco_etanol):
        # Adiciona uma nova capital no mapa
        self.capitais[nome] = Capital(nome, preco_etanol)
    
    # Função adiciona Vizinhos
    def adicionar_vizinho(self, capital1, capital2, distancia):
        # Conecta duas capitais (ida e volta)
        if capital1 in self.capitais and capital2 in self.capitais:
            self.capitais[capital1].vizinhos[capital2] = distancia
            self.capitais[capital2].vizinhos[capital1] = distancia
###########################################################################################################################################################
# Função Carrega Mapa
def carregar_mapa():
    mapa = MapaBrasil()
    
    # Preços do etanol realizado 30/03 a 05/04/2025)
    # Fonte: https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/arquivos-lpc/2025/resumo_semanal_lpc_2025-03-30_2025-04-05.xlsx
    # Aqui temos um objeto chamado mapa onde criamos para 
    # que no objeto seja adicionado a capital com o valor do etanol
    mapa.adicionar_capital("Aracajú (SE)", 4.99)
    mapa.adicionar_capital("Belém (PA)", 5.69)
    mapa.adicionar_capital("Belo Horizonte (MG)", 5.04)
    mapa.adicionar_capital("Boa Vista (RR)", 5.2)
    mapa.adicionar_capital("Brasília (DF)", 4.79)
    mapa.adicionar_capital("Campo Grande (MS)", 5.05)
    mapa.adicionar_capital("Cuiabá (MT)", 4.49)
    mapa.adicionar_capital("Curitiba (PR)", 4.99)
    mapa.adicionar_capital("Florianópolis (SC)", 6.36)
    mapa.adicionar_capital("Fortaleza (CE)", 5.69)
    mapa.adicionar_capital("Goiânia (GO)", 4.89)
    mapa.adicionar_capital("João Pessoa (PB)", 4.99)
    mapa.adicionar_capital("Macapá (AP)", 5.9)
    mapa.adicionar_capital("Maceió (AL)", 5.49)
    mapa.adicionar_capital("Manaus (AM)", 5.59)
    mapa.adicionar_capital("Natal (RN)", 5.49)
    mapa.adicionar_capital("Palmas (TO)", 5.49)
    mapa.adicionar_capital("Porto Alegre (RS)", 5.93)
    mapa.adicionar_capital("Porto Velho (RO)", 5.99)
    mapa.adicionar_capital("Recife (PE)", 6.49)
    mapa.adicionar_capital("Rio Branco (AC)", 6.08)
    mapa.adicionar_capital("R. Janeiro (RJ)", 5.49)
    mapa.adicionar_capital("Salvador (BA)", 5.29)
    mapa.adicionar_capital("São Luis (MA)", 5.79)
    mapa.adicionar_capital("São Paulo (SP)", 5.99)
    mapa.adicionar_capital("Teresina (PI)", 5.15)
    mapa.adicionar_capital("Vitória (ES)", 5.08)
    #####################################################################################################################################################

    # Aqui atrelamos no objeto mapa as capitais vizinhas junto com sua distancia
    # A estrutura e colocar todos os vizinhos das capitais sendo que uma capital pode ter um vizinho
    # Ou uma capital pode ter varios vizinhos
    # Distâncias rodoviárias entre as capitais vizinhas, ou seja, capitais na qual seus estados fazem fronteiras (em km)
    # Fonte: https://www.goodway.com.br/distancias.htm 
    #####################################################################################################################################################
   
    mapa.adicionar_vizinho("Aracajú (SE)", "Maceió (AL)", 201)
    mapa.adicionar_vizinho("Aracajú (SE)", "Salvador (BA)", 277)
    mapa.adicionar_vizinho("Belém (PA)", "Boa Vista (RR)", 6083)
    mapa.adicionar_vizinho("Belém (PA)", "Cuiabá (MT)", 1778)
    mapa.adicionar_vizinho("Belém (PA)", "Macapá (AP)", 329)
    mapa.adicionar_vizinho("Belém (PA)", "Manaus (AM)", 1292)
    mapa.adicionar_vizinho("Belém (PA)", "Palmas (TO)", 1283)
    mapa.adicionar_vizinho("Belém (PA)", "São Luis (MA)", 481)
    mapa.adicionar_vizinho("Belo Horizonte (MG)", "Brasília (DF)", 716)
    mapa.adicionar_vizinho("Belo Horizonte (MG)", "Goiânia (GO)", 906)
    mapa.adicionar_vizinho("Belo Horizonte (MG)", "R. Janeiro (RJ)", 434)
    mapa.adicionar_vizinho("Belo Horizonte (MG)", "Salvador (BA)", 1372)
    mapa.adicionar_vizinho("Belo Horizonte (MG)", "São Paulo (SP)", 586)
    mapa.adicionar_vizinho("Belo Horizonte (MG)", "Vitória (ES)", 524)
    mapa.adicionar_vizinho("Boa Vista (RR)", "Belém (PA)", 6083)
    mapa.adicionar_vizinho("Boa Vista (RR)", "Manaus (AM)", 661)
    mapa.adicionar_vizinho("Brasília (DF)", "Belo Horizonte (MG)", 716)
    mapa.adicionar_vizinho("Brasília (DF)", "Goiânia (GO)", 209)
    mapa.adicionar_vizinho("Campo Grande (MS)", "Cuiabá (MT)", 694)
    mapa.adicionar_vizinho("Campo Grande (MS)", "Curitiba (PR)", 991)
    mapa.adicionar_vizinho("Campo Grande (MS)", "Goiânia (GO)", 935)
    mapa.adicionar_vizinho("Cuiabá (MT)", "Belém (PA)", 1778)
    mapa.adicionar_vizinho("Cuiabá (MT)", "Campo Grande (MS)", 694)
    mapa.adicionar_vizinho("Cuiabá (MT)", "Goiânia (GO)", 740)
    mapa.adicionar_vizinho("Cuiabá (MT)", "Manaus (AM)", 1453)
    mapa.adicionar_vizinho("Cuiabá (MT)", "Palmas (TO)", 1784)
    mapa.adicionar_vizinho("Cuiabá (MT)", "Porto Velho (RO)", 1456)
    mapa.adicionar_vizinho("Curitiba (PR)", "Florianópolis (SC)", 300)
    mapa.adicionar_vizinho("Curitiba (PR)", "São Paulo (SP)", 408)
    mapa.adicionar_vizinho("Florianópolis (SC)", "Curitiba (PR)", 300)
    mapa.adicionar_vizinho("Florianópolis (SC)", "Porto Alegre (RS)", 376)
    mapa.adicionar_vizinho("Fortaleza (CE)", "João Pessoa (PB)", 688)
    mapa.adicionar_vizinho("Fortaleza (CE)", "Natal (RN)", 537)
    mapa.adicionar_vizinho("Fortaleza (CE)", "Recife (PE)", 800)
    mapa.adicionar_vizinho("Fortaleza (CE)", "Teresina (PI)", 634)
    mapa.adicionar_vizinho("Goiânia (GO)", "Belo Horizonte (MG)", 906)
    mapa.adicionar_vizinho("Goiânia (GO)", "Brasília (DF)", 209)
    mapa.adicionar_vizinho("Goiânia (GO)", "Campo Grande (MS)", 935)
    mapa.adicionar_vizinho("Goiânia (GO)", "Cuiabá (MT)", 740)
    mapa.adicionar_vizinho("Goiânia (GO)", "Palmas (TO)", 874)
    mapa.adicionar_vizinho("Goiânia (GO)", "Salvador (BA)", 1225)
    mapa.adicionar_vizinho("João Pessoa (PB)", "Fortaleza (CE)", 688)
    mapa.adicionar_vizinho("João Pessoa (PB)", "Natal (RN)", 185)
    mapa.adicionar_vizinho("João Pessoa (PB)", "Recife (PE)", 120)
    mapa.adicionar_vizinho("Macapá (AP)", "Belém (PA)", 329)
    mapa.adicionar_vizinho("Maceió (AL)", "Aracajú (SE)", 201)
    mapa.adicionar_vizinho("Maceió (AL)", "Recife (PE)", 285)
    mapa.adicionar_vizinho("Maceió (AL)", "Salvador (BA)", 632)  
    mapa.adicionar_vizinho("Manaus (AM)", "Belém (PA)", 1292)
    mapa.adicionar_vizinho("Manaus (AM)", "Boa Vista (RR)", 661)
    mapa.adicionar_vizinho("Manaus (AM)", "Cuiabá (MT)", 1453)
    mapa.adicionar_vizinho("Manaus (AM)", "Porto Velho (RO)", 901)
    mapa.adicionar_vizinho("Manaus (AM)", "Rio Branco (AC)", 1149)
    mapa.adicionar_vizinho("Natal (RN)", "Fortaleza (CE)", 537)
    mapa.adicionar_vizinho("Natal (RN)", "João Pessoa (PB)", 185)
    mapa.adicionar_vizinho("Palmas (TO)", "Belém (PA)", 1283)
    mapa.adicionar_vizinho("Palmas (TO)", "Cuiabá (MT)", 1784)
    mapa.adicionar_vizinho("Palmas (TO)", "Goiânia (GO)", 874)
    mapa.adicionar_vizinho("Palmas (TO)", "Salvador (BA)", 1114)
    mapa.adicionar_vizinho("Palmas (TO)", "São Luis (MA)", 964)
    mapa.adicionar_vizinho("Palmas (TO)", "Teresina (PI)", 835)
    mapa.adicionar_vizinho("Porto Alegre (RS)", "Florianópolis (SC)", 376)
    mapa.adicionar_vizinho("Porto Velho (RO)", "Cuiabá (MT)", 1456)
    mapa.adicionar_vizinho("Porto Velho (RO)", "Manaus (AM)", 901)
    mapa.adicionar_vizinho("Porto Velho (RO)", "Rio Branco (AC)", 449)
    mapa.adicionar_vizinho("Recife (PE)", "Fortaleza (CE)", 800)
    mapa.adicionar_vizinho("Recife (PE)", "João Pessoa (PB)", 120)
    mapa.adicionar_vizinho("Recife (PE)", "Maceió (AL)", 285)
    mapa.adicionar_vizinho("Recife (PE)", "Salvador (BA)", 675)
    mapa.adicionar_vizinho("Recife (PE)", "Teresina (PI)", 1137)
    mapa.adicionar_vizinho("Rio Branco (AC)", "Manaus (AM)", 1149)
    mapa.adicionar_vizinho("Rio Branco (AC)", "Porto Velho (RO)", 449)
    mapa.adicionar_vizinho("R. Janeiro (RJ)", "Belo Horizonte (MG)", 434)
    mapa.adicionar_vizinho("R. Janeiro (RJ)", "São Paulo (SP)", 429)
    mapa.adicionar_vizinho("R. Janeiro (RJ)", "Vitória (ES)", 412)
    mapa.adicionar_vizinho("Salvador (BA)", "Aracajú (SE)", 277)
    mapa.adicionar_vizinho("Salvador (BA)", "Belo Horizonte (MG)", 1372)
    mapa.adicionar_vizinho("Salvador (BA)", "Goiânia (GO)", 1225)
    mapa.adicionar_vizinho("Salvador (BA)", "Maceió (AL)", 632)
    mapa.adicionar_vizinho("Salvador (BA)", "Palmas (TO)", 1114)
    mapa.adicionar_vizinho("Salvador (BA)", "Recife (PE)", 675)
    mapa.adicionar_vizinho("Salvador (BA)", "Teresina (PI)", 1163)
    mapa.adicionar_vizinho("Salvador (BA)", "Vitória (ES)", 1202)
    mapa.adicionar_vizinho("São Luis (MA)", "Belém (PA)", 481)
    mapa.adicionar_vizinho("São Luis (MA)", "Palmas (TO)", 964)
    mapa.adicionar_vizinho("São Luis (MA)", "Teresina (PI)", 446)
    mapa.adicionar_vizinho("São Paulo (SP)", "Belo Horizonte (MG)", 586)
    mapa.adicionar_vizinho("São Paulo (SP)", "Curitiba (PR)", 408)
    mapa.adicionar_vizinho("São Paulo (SP)", "R. Janeiro (RJ)", 429)
    mapa.adicionar_vizinho("Teresina (PI)", "Fortaleza (CE)", 634)
    mapa.adicionar_vizinho("Teresina (PI)", "Palmas (TO)", 835)
    mapa.adicionar_vizinho("Teresina (PI)", "Recife (PE)", 1137)
    mapa.adicionar_vizinho("Teresina (PI)", "Salvador (BA)", 1163)
    mapa.adicionar_vizinho("Teresina (PI)", "São Luis (MA)", 446)
    mapa.adicionar_vizinho("Vitória (ES)", "Belo Horizonte (MG)", 524)
    mapa.adicionar_vizinho("Vitória (ES)", "R. Janeiro (RJ)", 412)
    mapa.adicionar_vizinho("Vitória (ES)", "Salvador (BA)", 1202)
    return mapa
##########################################################################################################

# Aqui criamos uma função que faz a busca em largura
# onde no nosso objeto mapa ele usa origem e destino
def buscar_largura(mapa, origem, destino):
    # Busca em largura padrão 
    fila = [[origem]]
    visitados = set()
    visitados.add(origem)
    cidades_visitadas = [origem]  # Analisa as capitais visitas
    
    while fila:
        caminho = fila.pop(0)
        cidade_atual = caminho[-1]
        
        if cidade_atual == destino:
            distancia_total = calcular_distancia(mapa, caminho)
            return caminho, distancia_total, cidades_visitadas
        
        for vizinho in mapa.capitais[cidade_atual].vizinhos:
            if vizinho not in visitados:
                visitados.add(vizinho)
                cidades_visitadas.append(vizinho)
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                fila.append(novo_caminho)
    
    return None, 0, cidades_visitadas
###############################################################################################################
# Aqui criamos a função de busca por profundidade

def buscar_profundidade(mapa, origem, destino):
    # Busca em profundidade 
    pilha = [[origem]]
    visitados = set()
    visitados.add(origem)
    cidades_visitadas = [origem]
    
    while pilha:
        caminho = pilha.pop()
        cidade_atual = caminho[-1]
        
        if cidade_atual == destino:
            distancia_total = calcular_distancia(mapa, caminho)
            return caminho, distancia_total, cidades_visitadas
        
        for vizinho in mapa.capitais[cidade_atual].vizinhos:
            if vizinho not in visitados:
                visitados.add(vizinho)
                cidades_visitadas.append(vizinho)
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                pilha.append(novo_caminho)
    
    return None, 0, cidades_visitadas
#########################################################################################################################

# Aqui criamos a Busca Heuristica
def buscar_a_estrela(mapa, origem, destino):
    # A* com heurística de preço do etanol
    fila_prioridade = [{
        'f': heuristica(mapa, origem, destino),  # f = g + h
        'g': 0,                                  # Custo real
        'caminho': [origem]
    }]
    visitados = set()
    cidades_visitadas = [origem]
    
    while fila_prioridade:
        fila_prioridade.sort(key=lambda x: x['f'])  # Ordena pelo menor custo
        atual = fila_prioridade.pop(0)
        cidade_atual = atual['caminho'][-1]
        
        if cidade_atual == destino:
            return atual['caminho'], atual['g'], cidades_visitadas
        
        if cidade_atual in visitados:
            continue
            
        visitados.add(cidade_atual)
        
        for vizinho, distancia in mapa.capitais[cidade_atual].vizinhos.items():
            if vizinho not in visitados:
                cidades_visitadas.append(vizinho)
                novo_g = atual['g'] + distancia
                novo_f = novo_g + heuristica(mapa, vizinho, destino)
                novo_caminho = list(atual['caminho'])
                novo_caminho.append(vizinho)
                
                fila_prioridade.append({
                    'f': novo_f,
                    'g': novo_g,
                    'caminho': novo_caminho
                })
    
    return None, 0, cidades_visitadas

def heuristica(mapa, cidade, destino):
    # Heurística melhorada que combina:
    # 1. Diferença de preço do etanol (peso menor)
    # 2. Estimativa de distância baseada em saltos (peso maior)
    
    # Fator de diferença de preço (0-1 normalizado)
    diff_preco = abs(mapa.capitais[cidade].preco_etanol - mapa.capitais[destino].preco_etanol) / 2.0
    
    # Estimativa de saltos mínimos (considerando que cada salto é ~500km)
    # Isso faz com que a busca priorize cidades que levem na direção do destino
    saltos_estimados = len(mapa.capitais[cidade].vizinhos) / len(mapa.capitais[destino].vizinhos)
    
    # Combinação ponderada
    return (0.3 * diff_preco) + (0.7 * saltos_estimados * 500)
####################################################################################################################

#Aqui criamos a função calcular_distancia 
def calcular_distancia(mapa, caminho):
    # Soma as distâncias entre cidades consecutivas no caminho
    distancia = 0
    for i in range(len(caminho)-1):
        distancia += mapa.capitais[caminho[i]].vizinhos[caminho[i+1]]
    return distancia
####################################################################################################################

#Aqui criamos a Função para mostrar o menu das capitais
def mostrar_menu_capitais(mapa):
    # Exibe menu numerado com todas as capitais
    print("\nCapitais disponíveis:")
    capitais = sorted(mapa.capitais.keys())
    for i, capital in enumerate(capitais, 1):
        print(f"{i}. {capital}")
    return capitais
####################################################################################################################
#Aqui criamos a função main
def main():
    # Fluxo principal
    mapa = carregar_mapa()
    capitais = mostrar_menu_capitais(mapa)
    
    # Seleção de origem/destino
    while True:
        try:
            print("\nSelecione a capital de origem:")
            origem_idx = int(input("Digite o número da capital: ")) - 1
            origem = capitais[origem_idx]
            
            print("\nSelecione a capital de destino:")
            destino_idx = int(input("Digite o número da capital: ")) - 1
            destino = capitais[destino_idx]
            
            break
        except (ValueError, IndexError):
            print("Entrada inválida. Use o número relativo à capital.")
    
    print(f"\nCalculando rotas de {origem} para {destino}...")
    
    # Executa todos os algoritmos
    caminho_largura, distancia_largura, visitados_largura = buscar_largura(mapa, origem, destino)
    caminho_profundidade, distancia_profundidade, visitados_profundidade = buscar_profundidade(mapa, origem, destino)
    caminho_a_estrela, distancia_a_estrela, visitados_a_estrela = buscar_a_estrela(mapa, origem, destino)
    
    # Exibe resultados
    print("\n--- Busca em Largura ---")
    if caminho_largura:
        print(f"Melhor caminho ({len(caminho_largura)} cidades): {' → '.join(caminho_largura)}")
        print(f"Distância total: {distancia_largura} km")
        print(f"Cidades visitadas: {', '.join(visitados_largura)}")
    else:
        print("Nenhum caminho encontrado.")
    
    print("\n--- Busca em Profundidade ---")
    if caminho_profundidade:
        print(f"Caminho encontrado ({len(caminho_profundidade)} cidades): {' → '.join(caminho_profundidade)}")
        print(f"Distância: {distancia_profundidade} km")
        print(f"Cidades visitadas: {', '.join(visitados_profundidade)}")
    
    print("\n--- Busca A* ---")
    if caminho_a_estrela:
        print(f"Melhor caminho ({len(caminho_a_estrela)} cidades): {' → '.join(caminho_a_estrela)}")
        print(f"Distância: {distancia_a_estrela} km")
        print(f"Heurística: diferença de preço do etanol + estimativa de saltos")
        print(f"Cidades visitadas: {', '.join(visitados_a_estrela)}")
    
    # Comparativo final
    print("\n--- Comparativo ---")
    print(f"{'Método':<20} {'Cidades':<10} {'Distância (km)':<15}")
    print("-"*45)
    for metodo, caminho, distancia in [
        ("Busca em Largura", caminho_largura, distancia_largura),
        ("Busca em Profund.", caminho_profundidade, distancia_profundidade),
        ("Busca A*", caminho_a_estrela, distancia_a_estrela)
    ]:
        cidades = len(caminho) if caminho else "N/A"
        dist = distancia if caminho else "N/A"
        print(f"{metodo:<20} {cidades:<10} {dist:<15}")

if __name__ == "__main__":
    main()