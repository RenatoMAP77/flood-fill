import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import deque
import random

class FloodFillAlgorithm:
    def __init__(self, grid):
        """
        Inicializa o algoritmo Flood Fill com um grid.
        
        Args:
            grid: Matriz 2D representando o terreno
        """
        self.grid = np.array(grid)
        self.rows, self.cols = self.grid.shape
        self.current_color = 2  # Começa com a cor 2 (vermelho)
        
    def is_valid(self, x, y):
        """
        Verifica se uma posição (x, y) é válida no grid.
        
        Args:
            x: Coordenada da linha
            y: Coordenada da coluna
            
        Returns:
            bool: True se a posição é válida, False caso contrário
        """
        return 0 <= x < self.rows and 0 <= y < self.cols
    
    def flood_fill_recursive(self, x, y, color):
        """
        Implementação recursiva do algoritmo Flood Fill.
        
        Args:
            x: Coordenada inicial da linha
            y: Coordenada inicial da coluna
            color: Cor para preencher a região
        """
        # Verifica se a posição é válida e se é um terreno navegável (0)
        if not self.is_valid(x, y) or self.grid[x][y] != 0:
            return
        
        # Preenche a célula atual com a cor
        self.grid[x][y] = color
        
        # Chama recursivamente para as células adjacentes (cima, baixo, esquerda, direita)
        self.flood_fill_recursive(x - 1, y, color)  # Cima
        self.flood_fill_recursive(x + 1, y, color)  # Baixo
        self.flood_fill_recursive(x, y - 1, color)  # Esquerda
        self.flood_fill_recursive(x, y + 1, color)  # Direita
    
    def flood_fill_iterative(self, x, y, color):
        """
        Implementação iterativa do algoritmo Flood Fill usando BFS.
        Mais eficiente para grids grandes.
        
        Args:
            x: Coordenada inicial da linha
            y: Coordenada inicial da coluna
            color: Cor para preencher a região
        """
        if not self.is_valid(x, y) or self.grid[x][y] != 0:
            return
        
        # Usa uma fila para BFS
        queue = deque([(x, y)])
        self.grid[x][y] = color
        
        # Direções: cima, baixo, esquerda, direita
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            curr_x, curr_y = queue.popleft()
            
            # Verifica todas as direções adjacentes
            for dx, dy in directions:
                new_x, new_y = curr_x + dx, curr_y + dy
                
                if self.is_valid(new_x, new_y) and self.grid[new_x][new_y] == 0:
                    self.grid[new_x][new_y] = color
                    queue.append((new_x, new_y))
    
    def find_next_empty_cell(self):
        """
        Encontra a próxima célula navegável (0) no grid.
        
        Returns:
            tuple: Coordenadas (x, y) da próxima célula vazia ou None se não houver
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None
    
    def fill_all_regions(self, start_x=None, start_y=None, use_recursive=False):
        """
        Preenche todas as regiões navegáveis do grid com cores diferentes.
        
        Args:
            start_x: Coordenada inicial da linha (opcional)
            start_y: Coordenada inicial da coluna (opcional)
            use_recursive: Se True, usa implementação recursiva; caso contrário, iterativa
        """
        # Se não foram fornecidas coordenadas iniciais, encontra a primeira célula vazia
        if start_x is None or start_y is None:
            first_empty = self.find_next_empty_cell()
            if first_empty:
                start_x, start_y = first_empty
            else:
                return  # Não há células vazias
        
        # Preenche a primeira região
        if use_recursive:
            self.flood_fill_recursive(start_x, start_y, self.current_color)
        else:
            self.flood_fill_iterative(start_x, start_y, self.current_color)
        
        # Continua procurando e preenchendo novas regiões
        while True:
            next_empty = self.find_next_empty_cell()
            if next_empty is None:
                break  # Todas as regiões foram preenchidas
            
            self.current_color += 1
            x, y = next_empty
            
            if use_recursive:
                self.flood_fill_recursive(x, y, self.current_color)
            else:
                self.flood_fill_iterative(x, y, self.current_color)
    
    def print_grid(self, title="Grid"):
        """
        Imprime o grid no terminal.
        
        Args:
            title: Título para exibir antes do grid
        """
        print(f"\n{title}:")
        for row in self.grid:
            print(" ".join(map(str, row)))
    
    def visualize_grid(self, title="Grid", save_path=None):
        """
        Cria uma visualização colorida do grid.
        
        Args:
            title: Título da visualização
            save_path: Caminho para salvar a imagem (opcional)
        """
        # Define as cores para cada valor
        colors_map = {
            0: 'white',      # Terreno navegável
            1: 'black',      # Obstáculo
            2: 'red',        # Vermelho
            3: 'orange',     # Laranja
            4: 'yellow',     # Amarelo
            5: 'green',      # Verde
            6: 'blue',       # Azul
            7: 'purple',     # Roxo
            8: 'pink',       # Rosa
            9: 'brown',      # Marrom
        }
        
        # Cria uma matriz de cores
        color_grid = np.zeros((*self.grid.shape, 3))
        for i in range(self.rows):
            for j in range(self.cols):
                value = self.grid[i][j]
                if value in colors_map:
                    color = mcolors.to_rgb(colors_map[value])
                else:
                    # Para valores não mapeados, gera uma cor aleatória consistente
                    random.seed(value)
                    color = (random.random(), random.random(), random.random())
                color_grid[i, j] = color
        
        # Cria a visualização
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(color_grid)
        
        # Adiciona grid
        ax.set_xticks(np.arange(-0.5, self.cols, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.rows, 1), minor=True)
        ax.grid(which="minor", color="gray", linestyle='-', linewidth=1)
        ax.tick_params(which="minor", size=0)
        
        # Configura os labels dos eixos
        ax.set_xlabel('Colunas')
        ax.set_ylabel('Linhas')
        ax.set_title(title)
        
        # Ajusta os ticks principais
        ax.set_xticks(range(self.cols))
        ax.set_yticks(range(self.rows))
        
        # Inverte o eixo y para que (0,0) fique no canto superior esquerdo
        ax.invert_yaxis()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        
        plt.show()
    
    def get_grid_copy(self):
        """
        Retorna uma cópia do grid atual.
        
        Returns:
            numpy.ndarray: Cópia do grid
        """
        return self.grid.copy()


def generate_random_grid(rows, cols, obstacle_percentage=0.3):
    """
    Gera um grid aleatório com obstáculos.
    
    Args:
        rows: Número de linhas
        cols: Número de colunas
        obstacle_percentage: Porcentagem de obstáculos (0.0 a 1.0)
        
    Returns:
        list: Grid aleatório
    """
    grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if random.random() < obstacle_percentage:
                row.append(1)  # Obstáculo
            else:
                row.append(0)  # Terreno navegável
        grid.append(row)
    return grid


def main():
    """
    Função principal para demonstrar o uso do algoritmo Flood Fill.
    """
    print("=== Algoritmo Flood Fill - Colorindo Regiões de um Terreno ===\n")
    
    # Exemplo 1
    print("EXEMPLO 1:")
    grid1 = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0]
    ]
    
    ff1 = FloodFillAlgorithm(grid1)
    ff1.print_grid("Grid inicial")
    
    # Cria uma cópia para visualização do antes
    grid1_before = ff1.get_grid_copy()
    
    # Aplica o algoritmo
    ff1.fill_all_regions(0, 0)
    ff1.print_grid("Grid preenchido")
    
    # Visualização gráfica
    # Grid antes
    ff1_before = FloodFillAlgorithm(grid1_before)
    ff1_before.visualize_grid("Exemplo 1 - Grid Inicial", "exemplo1_antes.png")
    
    # Grid depois
    ff1.visualize_grid("Exemplo 1 - Grid Preenchido", "exemplo1_depois.png")
    
    print("\n" + "="*50 + "\n")
    
    # Exemplo 2
    print("EXEMPLO 2:")
    grid2 = [
        [0, 1, 0, 0, 1],
        [0, 1, 0, 0, 1],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 1, 0]
    ]
    
    ff2 = FloodFillAlgorithm(grid2)
    ff2.print_grid("Grid inicial")
    
    # Cria uma cópia para visualização do antes
    grid2_before = ff2.get_grid_copy()
    
    # Aplica o algoritmo
    ff2.fill_all_regions(0, 2)
    ff2.print_grid("Grid preenchido")
    
    # Visualização gráfica
    # Grid antes
    ff2_before = FloodFillAlgorithm(grid2_before)
    ff2_before.visualize_grid("Exemplo 2 - Grid Inicial", "exemplo2_antes.png")
    
    # Grid depois
    ff2.visualize_grid("Exemplo 2 - Grid Preenchido", "exemplo2_depois.png")
    
    print("\n" + "="*50 + "\n")
    
    # Exemplo com grid aleatório
    print("EXEMPLO COM GRID ALEATÓRIO (10x10):")
    random_grid = generate_random_grid(10, 10, 0.25)
    
    ff_random = FloodFillAlgorithm(random_grid)
    ff_random.print_grid("Grid aleatório inicial")
    
    # Cria uma cópia para visualização do antes
    random_grid_before = ff_random.get_grid_copy()
    
    # Aplica o algoritmo
    ff_random.fill_all_regions()
    ff_random.print_grid("Grid aleatório preenchido")
    
    # Visualização gráfica
    # Grid antes
    ff_random_before = FloodFillAlgorithm(random_grid_before)
    ff_random_before.visualize_grid("Grid Aleatório - Inicial", "random_antes.png")
    
    # Grid depois
    ff_random.visualize_grid("Grid Aleatório - Preenchido", "random_depois.png")


if __name__ == "__main__":
    main()