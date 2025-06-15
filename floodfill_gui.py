import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from collections import deque
import random
import time
# Importa a classe principal do arquivo floodfill.py
from floodfill import FloodFillAlgorithm

class FloodFillGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flood Fill - Visualização Interativa")
        self.root.geometry("800x700")
        
        # Configurações do grid
        self.rows = 15
        self.cols = 15
        self.cell_size = 30
        self.grid = None
        self.original_grid = None
        self.current_color = 2
        self.animation_speed = 50  # ms entre cada passo
        self.is_animating = False
        
        # Cores
        self.colors = {
            0: '#FFFFFF',  # Branco - navegável
            1: '#000000',  # Preto - obstáculo
            2: '#FF0000',  # Vermelho
            3: '#FFA500',  # Laranja
            4: '#FFFF00',  # Amarelo
            5: '#00FF00',  # Verde
            6: '#0000FF',  # Azul
            7: '#800080',  # Roxo
            8: '#FFC0CB',  # Rosa
            9: '#8B4513',  # Marrom
        }
        
        self.setup_ui()
        self.generate_random_grid()
        
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame de controles
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Controles de tamanho do grid
        ttk.Label(control_frame, text="Linhas:").pack(side=tk.LEFT, padx=5)
        self.rows_var = tk.IntVar(value=self.rows)
        rows_spin = ttk.Spinbox(control_frame, from_=5, to=30, textvariable=self.rows_var, width=5)
        rows_spin.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Colunas:").pack(side=tk.LEFT, padx=5)
        self.cols_var = tk.IntVar(value=self.cols)
        cols_spin = ttk.Spinbox(control_frame, from_=5, to=30, textvariable=self.cols_var, width=5)
        cols_spin.pack(side=tk.LEFT, padx=5)
        
        # Controle de obstáculos
        ttk.Label(control_frame, text="Obstáculos %:").pack(side=tk.LEFT, padx=5)
        self.obstacle_var = tk.IntVar(value=25)
        obstacle_scale = ttk.Scale(control_frame, from_=0, to=50, variable=self.obstacle_var, 
                                  orient=tk.HORIZONTAL, length=100)
        obstacle_scale.pack(side=tk.LEFT, padx=5)
        
        # Botões
        ttk.Button(control_frame, text="Novo Grid", command=self.generate_new_grid).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Resetar", command=self.reset_grid).pack(side=tk.LEFT, padx=5)
        
        # Frame de algoritmo
        algo_frame = ttk.Frame(self.root, padding="10")
        algo_frame.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Button(algo_frame, text="Preencher Tudo", command=self.fill_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(algo_frame, text="Preencher com Animação", command=self.fill_animated).pack(side=tk.LEFT, padx=5)
        ttk.Button(algo_frame, text="Parar Animação", command=self.stop_animation).pack(side=tk.LEFT, padx=5)
        
        # Controle de velocidade
        ttk.Label(algo_frame, text="Velocidade:").pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.IntVar(value=50)
        speed_scale = ttk.Scale(algo_frame, from_=1, to=200, variable=self.speed_var, 
                               orient=tk.HORIZONTAL, length=100, command=self.update_speed)
        speed_scale.pack(side=tk.LEFT, padx=5)
        
        # Canvas para o grid
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white')
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        # Bind do clique do mouse
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Status bar
        self.status_var = tk.StringVar(value="Clique em uma célula navegável para iniciar o preenchimento")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def generate_random_grid(self):
        """Gera um grid aleatório"""
        obstacle_prob = self.obstacle_var.get() / 100
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < obstacle_prob:
                    self.grid[i, j] = 1
                    
        self.original_grid = self.grid.copy()
        self.current_color = 2
        self.draw_grid()
        
    def generate_new_grid(self):
        """Gera um novo grid com as dimensões especificadas"""
        self.rows = self.rows_var.get()
        self.cols = self.cols_var.get()
        self.generate_random_grid()
        
    def reset_grid(self):
        """Reseta o grid para o estado original"""
        if self.original_grid is not None:
            self.grid = self.original_grid.copy()
            self.current_color = 2
            self.draw_grid()
            self.status_var.set("Grid resetado")
    
    def draw_grid(self):
        """Desenha o grid no canvas"""
        self.canvas.delete("all")
        
        # Calcula o tamanho das células baseado no canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            self.cell_size = min(
                (canvas_width - 20) // self.cols,
                (canvas_height - 20) // self.rows
            )
        
        # Desenha as células
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size + 10
                y1 = i * self.cell_size + 10
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                color = self.colors.get(self.grid[i, j], '#CCCCCC')
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline='gray',
                    width=1,
                    tags=f"cell_{i}_{j}"
                )
    
    def on_canvas_click(self, event):
        """Manipula cliques no canvas"""
        if self.is_animating:
            return
            
        # Calcula qual célula foi clicada
        col = (event.x - 10) // self.cell_size
        row = (event.y - 10) // self.cell_size
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.grid[row, col] == 0:
                self.flood_fill(row, col, self.current_color)
                self.current_color += 1
                self.draw_grid()
                self.status_var.set(f"Região preenchida com cor {self.current_color - 1}")
            else:
                self.status_var.set("Clique em uma célula navegável (branca)")
    
    def flood_fill(self, start_row, start_col, color):
        """Implementação do flood fill usando BFS"""
        if self.grid[start_row, start_col] != 0:
            return
            
        queue = deque([(start_row, start_col)])
        self.grid[start_row, start_col] = color
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            row, col = queue.popleft()
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.rows and 
                    0 <= new_col < self.cols and 
                    self.grid[new_row, new_col] == 0):
                    
                    self.grid[new_row, new_col] = color
                    queue.append((new_row, new_col))
    
    def fill_all(self):
        """Preenche todas as regiões sem animação"""
        if self.is_animating:
            return
            
        self.current_color = 2
        filled_count = 0
        
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == 0:
                    self.flood_fill(i, j, self.current_color)
                    self.current_color += 1
                    filled_count += 1
        
        self.draw_grid()
        self.status_var.set(f"Preenchimento completo: {filled_count} regiões identificadas")
    
    def fill_animated(self):
        """Preenche todas as regiões com animação"""
        if self.is_animating:
            return
            
        self.is_animating = True
        self.current_color = 2
        
        # Encontra a primeira célula vazia
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == 0:
                    self.animate_flood_fill(i, j, self.current_color)
                    return
    
    def animate_flood_fill(self, start_row, start_col, color):
        """Anima o processo de flood fill"""
        if not self.is_animating or self.grid[start_row, start_col] != 0:
            self.find_next_region()
            return
            
        queue = deque([(start_row, start_col)])
        self.grid[start_row, start_col] = color
        visited = {(start_row, start_col)}
        
        def process_next():
            if not self.is_animating or not queue:
                # Região atual preenchida, procura próxima
                self.find_next_region()
                return
                
            row, col = queue.popleft()
            
            # Atualiza a célula visualmente
            x1 = col * self.cell_size + 10
            y1 = row * self.cell_size + 10
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=self.colors.get(color, '#CCCCCC'),
                outline='gray',
                width=1,
                tags=f"cell_{row}_{col}"
            )
            
            # Adiciona vizinhos à fila
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.rows and 
                    0 <= new_col < self.cols and 
                    self.grid[new_row, new_col] == 0 and
                    (new_row, new_col) not in visited):
                    
                    self.grid[new_row, new_col] = color
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col))
            
            # Continua a animação
            self.root.after(self.animation_speed, process_next)
        
        # Inicia o processo
        process_next()
    
    def find_next_region(self):
        """Encontra a próxima região vazia para preencher"""
        if not self.is_animating:
            return
            
        self.current_color += 1
        
        # Procura próxima célula vazia
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == 0:
                    self.animate_flood_fill(i, j, self.current_color)
                    return
        
        # Não há mais regiões vazias
        self.is_animating = False
        self.status_var.set(f"Animação completa: {self.current_color - 2} regiões preenchidas")
    
    def stop_animation(self):
        """Para a animação"""
        self.is_animating = False
        self.status_var.set("Animação parada")
    
    def update_speed(self, value):
        """Atualiza a velocidade da animação"""
        self.animation_speed = int(float(value))


def main():
    root = tk.Tk()
    app = FloodFillGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()