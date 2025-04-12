# capitais_bsc_Lar_pro_heu
Implementação do algoritmo A* com heurística baseada na diferença no preço do etanol entre capitais e estimativa de saltos no grafo rodoviário do Brasil. Projeto da disciplina de IA do Mestrado em Ciência da Computação da UTFPR.

🔍 Projeto A* com Heurística baseada no Preço do Etanol entre Capitais Brasileiras
Este projeto foi desenvolvido como parte da disciplina de Inteligência Artificial do curso de Mestrado em Ciência da Computação - UTFPR, sob orientação do Prof. André Pinz Borges.
Autores:
🎓 Rodrigo Vieira
🎓 Kleber Barcarollo
📌 Descrição
Implementamos o algoritmo A* com uma heurística personalizada, adaptada ao cenário brasileiro, utilizando duas fontes principais de informação:
Preço do etanol por capital (dados da ANP, semana 30/03 a 05/04/2025).
Conectividade entre capitais baseada nas fronteiras estaduais e nas distâncias rodoviárias (GoodWay).
💡 Heurística proposta
A função heurística h(n) combina dois fatores:
Diferença normalizada no preço do etanol entre a cidade atual e o destino.
Estimativa de saltos (graus de conexão) multiplicada por uma média de 500 km por salto.
Fórmula heurística:
perl
Copiar
Editar
h(n) = (0.3 × Diferença no preço do etanol) + (0.7 × Saltos estimados × 500km)
Essa abordagem permite priorizar caminhos mais econômicos e curtos, sem uso de coordenadas geográficas, mantendo simplicidade e eficiência na estimativa de custo.
🧠 Funcionalidades
Definição de um grafo com todas as capitais brasileiras.
Inclusão dos preços reais do etanol em cada capital.
Conexões rodoviárias entre capitais vizinhas.
Implementações dos algoritmos de busca:
Busca em largura (BFS)
Busca em profundidade (DFS)
A* com heurística baseada em custo de combustível
📊 Fontes de dados
🛢️ Preço do etanol: ANP - Agência Nacional do Petróleo
🛣️ Distâncias rodoviárias: GoodWay
📁 Estrutura modular do projeto
main.py: ponto de entrada para execução das buscas
distancias.py: dados das conexões e distâncias
combustivel.py: preços do etanol por capital
utils.py: funções auxiliares, como cálculo de distância e heurística
🚀 Como usar
Basta definir a cidade de origem e o destino para ver:
O melhor caminho encontrado
A distância total

As cidades visitadas durante a busca
