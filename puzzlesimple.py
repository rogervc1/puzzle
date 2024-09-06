import tkinter as tk
from tkinter import messagebox
import heapq
import itertools

def heuristica(state, orden_final):
    distancia = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_index = orden_final.index(value)
                goal_x, goal_y = divmod(goal_index, 3)
                distancia += abs(i - goal_x) + abs(j - goal_y)
    return distancia

def get(state):
    neighbors = []
    zero_x, zero_y = [(ix, iy) for ix, row in enumerate(state) for iy, i in enumerate(row) if i == 0][0]
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        new_x, new_y = zero_x + dx, zero_y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = [row[:] for row in state]
            new_state[zero_x][zero_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[zero_x][zero_y]
            neighbors.append((new_state, (new_x, new_y)))
    return neighbors

def empezar(state):
    return '\n'.join(' '.join(map(str, row)) for row in state)

def imprimir_nodo(frontier_count, expanded_count, step):
    print(f"Step {step}:")
    print(f"Frontier nodes: {frontier_count}")
    print(f"Expanded nodes: {expanded_count}")
    print()

def algoritmo(start_state, goal_state):
    orden_final = list(itertools.chain(*goal_state))
    orde_inicial = tuple(itertools.chain(*start_state))
    frontier = [(0 + heuristica(start_state, orden_final), 0, start_state, [])]
    expanded = set()
    step = 0
    
    print("Empezando algoritmo:")
    
    while frontier:
        imprimir_nodo(len(frontier), len(expanded), step)
        step += 1
        
        _, cost, current_state, path = heapq.heappop(frontier)
        current_state_flat = tuple(itertools.chain(*current_state))
        
        if current_state == goal_state:
            print(f"Final frontier nodes: {len(frontier)}")
            print(f"Final expanded nodes: {len(expanded)}")
            return path
        
        if current_state_flat in expanded:
            continue
        
        expanded.add(current_state_flat)
        
        for neighbor, _ in get(current_state):
            if tuple(itertools.chain(*neighbor)) not in expanded:
                new_cost = cost + 1
                new_path = path + [neighbor]
                heapq.heappush(frontier, (new_cost + heuristica(neighbor, orden_final), new_cost, neighbor, new_path))
    
    print("No se encontro solucion")
    return None

class puzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Puzzle deslizante")
        
        self.start_state = [
            [2, 6, 3],
            [1, 0, 5],
            [7, 4, 8]
        ]
        
        self.goal_state = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        
        print("Resolviendo puzzle")
        self.solution = algoritmo(self.start_state, self.goal_state)
        print("Solucion encontrada")
        self.current_step = 0
        
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(master, text="", width=5, height=2, font=('Arial', 20, 'bold'))
                self.buttons[i][j].grid(row=i, column=j, padx=2, pady=2)
        
        self.next_button = tk.Button(master, text="1 Paso", command=self.avanzar)
        self.next_button.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.actualizar(self.start_state)
    
    def actualizar(self, state):
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                self.buttons[i][j]['text'] = str(value) if value != 0 else ""
                self.buttons[i][j]['bg'] = 'white' if value != 0 else 'gray'
    
    def avanzar(self):
        if self.current_step < len(self.solution):
            print(f"\nGUI Paso {self.current_step + 1}:")
            print(empezar(self.solution[self.current_step]))
            self.actualizar(self.solution[self.current_step])
            self.current_step += 1
        else:
            print("Puzzle resuelto en GUI")
            messagebox.showinfo("Resuelto", "Puzzle resuelto")
            self.next_button['state'] = 'disabled'

def main():
    root = tk.Tk()
    app = puzzleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()