import pygame
import networkx as nx
from queue import PriorityQueue
from math import inf
import time

# Colors
MARRON = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 255, 0)

# Table: 9x9
DIM = 9
RES = 720

# Variable declaration
running = True
editorMode = False
barriers = []
pygame.init()
Graph = nx.Graph()
screen = pygame.display.set_mode((RES, RES))
pygame.display.set_caption("Quoridor")
myfont = pygame.font.SysFont('Comic Sans MS', 30)
textsurface = myfont.render('Modo edicion activado', False, (255, 0, 0))


def cost(u, v):
    if Graph.get_edge_data(u, v).get('weight') != 1:
        pygame.quit()
        print("EL COSTO NO FUE UNO")
    return Graph.get_edge_data(u, v).get('weight')


def reconstruct_path(prev, source, target):
    node = target
    path = []
    while node != source:
        path.append(node)
        node = prev[node]
    path.append(node)
    path.reverse()
    return path


def manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def dijkstra(start, end):
    # Variable Declaration
    pq = PriorityQueue()
    visited = set()
    previous = {}

    distances = {v: inf for v in list(nx.nodes(Graph))}
    distances[start] = 0
    pq.put((distances[start], start))
    # While the priority queue has data
    while not pq.empty():
        distance, current = pq.get()
        visited.add(current)
        for neighbor in dict(Graph.adjacency()).get(current):
            route = distances[current] + cost(current, neighbor)
            if route < distances[neighbor]:
                distances[neighbor] = route
                previous[neighbor] = current
                if neighbor not in visited:
                    visited.add(neighbor)
                    pq.put((distances[neighbor], neighbor))
                else:
                    _ = pq.get((distances[neighbor], neighbor))
                    pq.put((distances[neighbor], neighbor))
    return reconstruct_path(previous, start, end)


def a_star(start, final):
    # Variable Declaration
    g = {g: float("inf") for g in list(nx.nodes(Graph))}
    f = {f: float("inf") for f in list(nx.nodes(Graph))}
    count = 0
    pq = PriorityQueue()
    pq.put((0, count, start))
    previous = {}

    g[start] = 0
    f[start] = cost(start, final)
    open_set_hash = {start}
    while not pq.empty():
        current = pq.get()[2]
        open_set_hash.remove(current)
        if current == final:
            return reconstruct_path(previous, start, final)
        for neighbor in dict(Graph.adjacency()).get(current):
            temp_g_score = g[current] + 1
            if temp_g_score < g[neighbor]:
                previous[neighbor] = current
                g[neighbor] = temp_g_score
                f[neighbor] = temp_g_score + cost(neighbor, final)
                if neighbor not in open_set_hash:
                    count += 1
                    pq.put((f[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
    return reconstruct_path(previous, start, final)


# Bot Class
class Bot:
    def __init__(self, node, x, y, barriers, name):
        self.node = node
        self.barriers = barriers
        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.step = 80
        self.width = 60

    def make_move(self):
        # route = dijkstra(self.node, 81)
        route = nx.astar_path(Graph, self.node, 81)
        print(route)
        """""
        print(nx.shortest_path(Graph, self.node, 81))
        print(nx.astar_path(Graph, self.node, 81))
        print(nx.dijkstra_path(Graph, self.node, 81))
        print(nx.bellman_ford_path(Graph, self.node, 81))
        """""
        if not len(route) == 0:
            if route[1] == self.node + 1:
                self.move_right()
            elif route[1] == self.node - 1:
                self.move_left()
            elif route[1] == self.node + DIM:
                self.move_down()
            elif route[1] == self.node - DIM:
                self.move_up()

    def move_up(self):
        if Graph.has_edge(self.node, self.node - DIM):
            self.y = self.y - self.step
            self.node = self.node - DIM
            return True
        else:
            return False

    def move_left(self):
        if Graph.has_edge(self.node, self.node - 1):
            self.x = self.x - self.step
            self.node = self.node - 1
            return True
        else:
            return False

    def move_right(self):
        if Graph.has_edge(self.node, self.node + 1):
            self.x = self.x + self.step
            self.node = self.node + 1
            return True
        else:
            return False

    def move_down(self):
        if Graph.has_edge(self.node, self.node + DIM):
            self.y = self.y + self.step
            self.node = self.node + DIM
            return True
        else:
            return False

    def check_win(self):
        if self.node >= DIM * 8:
            print("---------------------------")
            print(" Bot won")
            print("---------------------------")
            return True
        else:
            return False

    def draw(self):
        pygame.draw.ellipse(screen, AZUL, (self.x, self.y, self.width, self.width))


# Player Class
class Player:
    def __init__(self, node, x, y, barriers, name):
        self.node = node
        self.barriers = barriers
        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.step = 80
        self.width = 60
        self.has_played = False

    def move_up(self):
        if Graph.has_edge(self.node, self.node - DIM):
            self.y = self.y - self.step
            self.node = self.node - DIM
            self.has_played = True
            return True
        else:
            return False

    def move_left(self):
        if Graph.has_edge(self.node, self.node - 1):
            self.x = self.x - self.step
            self.node = self.node - 1
            self.has_played = True
            return True
        else:
            return False

    def move_right(self):
        if self.node + 1 == 81:
            return False
        if Graph.has_edge(self.node, self.node + 1):
            self.x = self.x + self.step
            self.node = self.node + 1
            self.has_played = True
            return True
        else:
            return False

    def move_down(self):
        if Graph.has_edge(self.node, self.node + DIM):
            self.y = self.y + self.step
            self.node = self.node + DIM
            self.has_played = True
            return True
        else:
            return False

    def check_win(self):
        if self.node < DIM:
            print("---------------------------")
            print(" Player won")
            print("---------------------------")
            return True
        else:
            return False

    def draw(self):
        pygame.draw.ellipse(screen, NEGRO, (self.x, self.y, self.width, self.width))


# Barrier Class
class Barrier:
    def __init__(self, player_node, x, y):
        self.player_node = player_node
        self.x = x
        self.y = y
        self.angle = 90
        self.step = 80
        self.width = 9
        self.height = 160

    def draw(self):
        if self.angle == 90:  # |
            pygame.draw.rect(screen, NEGRO, (self.x, self.y, self.width, self.height))
        elif self.angle == 180:  # -
            pygame.draw.rect(screen, NEGRO, (self.x + 4, self.y - 4, self.height, self.width))

    def rotate(self):
        if self.angle == 90:
            self.angle = 180
        elif self.angle == 180:
            self.angle = 90

    def move_up(self):
        if self.y == 12:
            return False
        self.y = self.y - self.step
        self.player_node = self.player_node - DIM
        return True

    def move_left(self):
        if self.x == 9:
            return False
        self.x = self.x - self.step
        self.player_node = self.player_node - 1
        return True

    def move_right(self):
        if self.x == 649:
            return False
        self.x = self.x + self.step
        self.player_node = self.player_node + 1
        return True

    def move_down(self):
        if self.y == 652:
            return False
        self.y = self.y + self.step
        self.player_node = self.player_node + DIM
        return True

    def save(self):
        if self.angle == 90:
            Graph.remove_edge(self.player_node, self.player_node - 1)
            Graph.remove_edge(self.player_node + DIM, self.player_node + 8)
        elif self.angle == 180:
            Graph.remove_edge(self.player_node, self.player_node - DIM)
            Graph.remove_edge(self.player_node + 1, self.player_node - 8)


# Add all the nodes
for i in range(DIM * DIM):
    Graph.add_node(i)
Graph.add_node(81)

# Add all the connections (edges)
node = 0
for i in range(DIM):
    for j in range(DIM):
        # (↑ ↓) connections
        if i == DIM - 1:
            Graph.add_edge(node, 81, weight=1)
        if i != (DIM - 1):
            Graph.add_edge(node, node + DIM, weight=1)
        # (← →) connections
        if j != (DIM - 1):
            Graph.add_edge(node, node + 1, weight=1)
        node = node + 1


# Draw map
def draw_map():
    block_size = RES / DIM
    for x in range(DIM):
        for y in range(DIM):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            pygame.draw.rect(screen, MARRON, rect, 1)


# Game Mechanics
bot = Bot(4, 329, 12, 10, "Terminator")
player = Player(76, 329, 652, 10, "Marco")
barrier = Barrier(0, -10, -10)

while running:
    # Check player or bot victory
    if player.check_win():
        running = False
    elif bot.check_win():
        running = False

    # Screen Background
    if not editorMode:
        screen.fill((139, 69, 19))
    else:
        screen.fill((191, 125, 59))

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not player.has_played:
                if not editorMode:
                    # Player's turn
                    if event.key == pygame.K_SPACE:
                        editorMode = True
                        barrier = Barrier(player.node, player.x - 13, player.y - 12)
                        print("Editor mode: enabled")
                    elif event.key == pygame.K_UP:
                        player.move_up()
                    elif event.key == pygame.K_DOWN:
                        player.move_down()
                    elif event.key == pygame.K_LEFT:
                        player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        player.move_right()
                    print("Player node: ", player.node, "(X: ", player.x, " Y: ", player.y, ")")
                else:
                    # Editor Mode
                    if event.key == pygame.K_ESCAPE:
                        editorMode = False
                        print("Editor mode: disabled")
                    elif event.key == pygame.K_r:
                        barrier.rotate()
                    elif event.key == pygame.K_UP:
                        barrier.move_up()
                    elif event.key == pygame.K_DOWN:
                        barrier.move_down()
                    elif event.key == pygame.K_LEFT:
                        barrier.move_left()
                    elif event.key == pygame.K_RIGHT:
                        barrier.move_right()
                    elif event.key == pygame.K_SPACE:
                        editorMode = False
                        barrier.save()
                        barriers.append(barrier)
                        print("New barrier added, exiting editor mode")
                    print("Barrier node: ", barrier.player_node, "(X: ", barrier.x, " Y: ", barrier.y, ")")
            else:
                t0 = time.time()
                # Bot's turn
                bot.make_move()
                player.has_played = False
                print("Bot node:    ", bot.node, "(X: ", bot.x, " Y: ", bot.y, ")")
                print(time.time() - t0)
    # Drawing
    draw_map()
    bot.draw()
    player.draw()
    barrier.draw()
    player.check_win()
    for obj in barriers:
        obj.draw()
    if editorMode:
        screen.blit(textsurface, (15, 15))
    pygame.display.update()
