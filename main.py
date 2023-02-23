import random
import sqlite3

# Константи
TREASURE = "TREASURE"
WATER = "WATER"
SHOVEL = "SHOVEL"
KEY = "KEY"
BEAST = "BEAST"
EASY_SIZE = 5
MEDIUM_SIZE = 10
HARD_SIZE = 20
EASY_MOVES = 10
MEDIUM_MOVES = 20
HARD_MOVES = 40

# Функції
def generate_map(size, num_waters, num_shovels, num_keys, num_beasts, has_treasure):
    """
    Generates a map of the specified size with random items.
    """
    items = [None] * size**2
    if has_treasure:
        treasure_location = random.randint(0, size**2 - 1)
        items[treasure_location] = TREASURE
    for i in range(num_waters):
        location = random.randint(0, size**2 - 1)
        while items[location] is not None:
            location = random.randint(0, size**2 - 1)
        items[location] = WATER
    for i in range(num_shovels):
        location = random.randint(0, size**2 - 1)
        while items[location] is not None:
            location = random.randint(0, size**2 - 1)
        items[location] = SHOVEL
    for i in range(num_keys):
        location = random.randint(0, size**2 - 1)
        while items[location] is not None:
            location = random.randint(0, size**2 - 1)
        items[location] = KEY
    for i in range(num_beasts):
        location = random.randint(0, size**2 - 1)
        while items[location] is not None:
            location = random.randint(0, size**2 - 1)
        items[location] = BEAST
    return items


def print_map(size, player_location, items, moves_left):
    """
    Prints the map with the player's location and items.
    """
    for i in range(size):
        for j in range(size):
            location = i * size + j
            if (i, j) == player_location:
                print("[*]", end="")
            else:
                print("   ", end="")
            if items[location] is None:
                print("  ", end="")
            else:
                print(f" {items[location][0]} ", end="")
        print()
    print(f"Moves left: {moves_left}")

def get_direction(size, player_location, item_location):
    """
    Returns the direction (up, down, left, or right) to reach the item_location
    from the player_location.
    """
    player_row, player_col = player_location
    item_row, item_col = item_location
    if player_row < item_row:
        return "down"
    elif player_row > item_row:
        return "up"
    elif player_col < item_col:
        return "right"
    elif player_col > item_col:
        return "left"
    else:
        return None

def play_game(difficulty, username):
    """
    Plays the Treasure Hunt game with the specified difficulty and username.
    """
   
    # Підключення дб
    conn = sqlite3.connect("treasure_hunt.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS scores (username TEXT, difficulty TEXT, score INT)")
    
    # Ініціалізація змінних гри на основі складності
    if difficulty == "easy":
        size = EASY_SIZE
        num_waters = 2
        num_shovels = 2
        num_keys = 2
        num_beasts = 1
        moves_left = EASY_MOVES
        has_treasure = True
    elif difficulty == "medium":
        size = MEDIUM_SIZE
        num_waters = 4
        num_shovels = 3
        num_keys = 3
        num_beasts = 2
        moves_left = MEDIUM_MOVES
        has_treasure = True
    elif difficulty == "hard":
        size = HARD_SIZE
        num_waters = 8
        num_shovels = 5
        num_keys = 4
        num_beasts = 4
        moves_left = HARD_MOVES
        has_treasure = True
        hints_on = False
        
    # Генерація карти
    items = generate_map(size, num_waters, num_shovels, num_keys, num_beasts, has_treasure)
    
    # Ініціалізувати місце розташування гравця та рахунок
    player_location = (0, 0)
    score = 0
    
    # Гра
    while moves_left > 0:
        print_map(size, player_location, items, moves_left)
        
        # Отримати хід користувача
        move = input("Enter a move (up, down, left, right): ")
        
        # розташування гравця на основі ходу
        if move == "up":
            if player_location[0] > 0:
                player_location = (player_location[0] - 1, player_location[1])
        elif move == "down":
            if player_location[0] < size - 1:
                player_location = (player_location[0] + 1, player_location[1])
        elif move == "left":
            if player_location[1] > 0:
                player_location = (player_location[0], player_location[1] - 1)
        elif move == "right":
            if player_location[1] < size - 1:
                player_location = (player_location[0], player_location[1] + 1)
        else:
            print("Invalid move!")
            continue
        
        # Зменшення рухів 
        moves_left -= 1
        
        # Перевірка чи гравець найшов предмет
        location = player_location[0] * size + player_location[1]
        if items[location] == TREASURE:
            print("Congratulations! You found the treasure!")
            score += 100
            break
        elif items[location] == WATER:
            print("Oh no! You fell into the water!")
            score -= 25
        elif items[location] == SHOVEL:
            print("You found a shovel!")
            score += 10
        elif items[location] == KEY:
            print("You found a key!")
            score += 20
        elif items[location] == BEAST:
            print("Oh no! You were eaten by a beast!")
            score -= 50       
def display_results(username, difficulty, moves_left, found_treasure):
    print(f"Game over, {username}!")
    if found_treasure:
        print("Congratulations! You found the treasure!")
    else:
        print("Sorry, you didn't find the treasure.")
    print(f"You completed the {difficulty} level with {moves_left} moves left.")
    display_results(username, difficulty, moves_left, found_treasure)

play_game("medium", "None")