![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
# Algoritmo Flood Fill - Colorindo Regiões de um Terreno com Obstáculos

## Descrição do Projeto

Este projeto implementa o algoritmo **Flood Fill** para identificar e preencher automaticamente regiões conectadas em um grid 2D, simulando um sistema de mapeamento inteligente para robôs autônomos. O algoritmo é capaz de identificar áreas navegáveis em um terreno, respeitando obstáculos e colorindo cada região desconectada com uma cor diferente.

## Introdução ao Problema

O Flood Fill é um algoritmo clássico usado para determinar e modificar áreas conectadas em uma matriz bidimensional. Neste contexto, o algoritmo é aplicado para:

- **Identificar regiões navegáveis**: Detectar todas as células conectadas que representam terreno livre (valor 0)
- **Respeitar obstáculos**: Evitar células marcadas como obstáculos (valor 1)
- **Colorir regiões distintas**: Atribuir cores diferentes para cada região desconectada
- **Mapear todo o terreno**: Continuar o processo até que todas as áreas navegáveis sejam identificadas

O algoritmo funciona de forma similar à ferramenta "balde de tinta" em programas de edição de imagem, preenchendo uma área conectada com uma cor específica.

## Estrutura do Projeto

```
flood-fill/
│
├── floodfill.py           # PRINCIPAL - Implementação do algoritmo (OBRIGATÓRIO)
├── floodfill_gui.py       # OPCIONAL - Interface gráfica que usa floodfill.py
├── README.md              # OBRIGATÓRIO - Documentação
├── requirements.txt       # OBRIGATÓRIO - Dependências
```

## Requisitos

### Dependências

- Python 3.7+
- NumPy
- Matplotlib

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seuusuario/flood-fill-project.git
cd flood-fill-project
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar

### Execução Básica

Para executar o programa com os exemplos padrão:

```bash
python floodfill.py
```

### Uso Personalizado

```python
from floodfill import FloodFillAlgorithm

# Criar um grid personalizado
grid = [
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0],
    [1, 1, 0, 0]
]

# Inicializar o algoritmo
ff = FloodFillAlgorithm(grid)

# Mostrar grid inicial
ff.print_grid("Grid Inicial")

# Preencher todas as regiões começando da posição (0, 0)
ff.fill_all_regions(0, 0)

# Mostrar grid preenchido
ff.print_grid("Grid Preenchido")

# Visualizar graficamente
ff.visualize_grid("Resultado Final")
```

## Funcionamento do Algoritmo Flood Fill

### Processo de Execução

1. **Inicialização**: O algoritmo recebe um grid 2D e coordenadas iniciais (x, y)

2. **Verificação**: Verifica se a célula inicial é navegável (valor 0)

3. **Preenchimento**: A partir da célula inicial, o algoritmo:
   - Marca a célula atual com a cor designada
   - Verifica as 4 células adjacentes (cima, baixo, esquerda, direita)
   - Para cada célula adjacente navegável, repete o processo

4. **Busca por novas regiões**: Após preencher uma região:
   - Procura a próxima célula com valor 0
   - Incrementa o valor da cor
   - Repete o processo de preenchimento

5. **Finalização**: O algoritmo termina quando todas as células navegáveis foram preenchidas

### Implementações Disponíveis

O projeto oferece duas implementações do Flood Fill:

1. **Recursiva**: Mais intuitiva, mas pode causar estouro de pilha em grids grandes
2. **Iterativa (BFS)**: Usa uma fila para evitar problemas de recursão, mais eficiente para grids grandes

### Complexidade

- **Tempo**: O(n × m), onde n e m são as dimensões do grid
- **Espaço**: O(n × m) no pior caso

## Exemplos de Entrada e Saída

### Exemplo 1

**Entrada:**
```
Grid inicial:
0 0 1 0 0
0 1 1 0 0
0 0 1 1 1
1 1 0 0 0

Coordenadas iniciais: (0, 0)
```

**Saída:**
```
Grid preenchido:
2 2 1 3 3
2 1 1 3 3
2 2 1 1 1
1 1 4 4 4
```

**Visualização:**

- **Antes**: Grid com áreas brancas (navegáveis) e pretas (obstáculos)
- **Depois**: Cada região navegável preenchida com uma cor diferente:
  - Região 1 (cor 2): Vermelho - conectada a (0,0)
  - Região 2 (cor 3): Laranja - área superior direita
  - Região 3 (cor 4): Amarelo - área inferior direita

### Exemplo 2

**Entrada:**
```
Grid inicial:
0 1 0 0 1
0 1 0 0 1
0 1 1 1 1
0 0 0 1 0

Coordenadas iniciais: (0, 2)
```

**Saída:**
```
Grid preenchido:
3 1 2 2 1
3 1 2 2 1
3 1 1 1 1
3 3 3 1 4
```

### Legenda de Cores

- **0 (Branco)**: Terreno navegável não preenchido
- **1 (Preto)**: Obstáculo
- **2 (Vermelho)**: Primeira região preenchida
- **3 (Laranja)**: Segunda região preenchida
- **4 (Amarelo)**: Terceira região preenchida
- **5+ (Outras cores)**: Regiões adicionais

## Funcionalidades Extras

### Geração de Grids Aleatórios

O projeto inclui uma função para gerar grids aleatórios com proporções configuráveis de obstáculos:

```python
from floodfill import generate_random_grid

# Gerar um grid 20x20 com 30% de obstáculos
grid = generate_random_grid(20, 20, obstacle_percentage=0.3)
```

### Visualização Gráfica

Além da saída em terminal, o projeto oferece visualização gráfica colorida dos grids:

```python
# Salvar visualização em arquivo
ff.visualize_grid("Título", save_path="resultado.png")
```

## Estrutura do Código

### Classe Principal: `FloodFillAlgorithm`

- `__init__(grid)`: Inicializa com um grid
- `flood_fill_recursive(x, y, color)`: Implementação recursiva
- `flood_fill_iterative(x, y, color)`: Implementação iterativa usando BFS
- `fill_all_regions(start_x, start_y)`: Preenche todas as regiões do grid
- `find_next_empty_cell()`: Encontra a próxima célula navegável
- `print_grid(title)`: Exibe o grid no terminal
- `visualize_grid(title, save_path)`: Cria visualização gráfica

### Funções Auxiliares

- `is_valid(x, y)`: Verifica se uma posição está dentro dos limites do grid
- `generate_random_grid(rows, cols, obstacle_percentage)`: Gera grids aleatórios

## Possíveis Melhorias Futuras

1. **Interface Gráfica Interativa**: Implementar uma GUI para visualização em tempo real
2. **Animação do Processo**: Mostrar o preenchimento acontecendo passo a passo
3. **Suporte a Diagonais**: Permitir conexões diagonais entre células
4. **Otimizações**: Implementar versões paralelas para grids muito grandes
5. **Mais Padrões de Obstáculos**: Adicionar geradores de labirintos e padrões complexos

## Licença

Este projeto é desenvolvido para fins educacionais como parte do curso de Engenharia de Software.