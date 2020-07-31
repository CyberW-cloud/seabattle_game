import os


class Game:

    def __init__(self):
        self.active_player = None
        self.waiting_player = None
        self.message = ""

    @staticmethod
    def clear_display():
        os.system('cls' if os.name == 'nt' else 'clear')

    def _change_active_player(self):
        self.active_player, self.waiting_player = \
            self.waiting_player, self.active_player
        self.message = ""

    def _draw_fields(self):
        self.clear_display()
        print("    Your field              Guess field")
        for your_line, guess_line in zip(self.active_player.field,
                                         self.active_player.guess_field):
            print(f'{" ".join(your_line)}     {" ".join(guess_line)}')

    def _hit_check(self, x, y):
        if self.waiting_player.field[y - 1][x - 1] == "o":
            self.waiting_player.field[y - 1][x - 1] = "x"
            self.active_player.guess_field[y - 1][x - 1] = "x"
            self.waiting_player.left_alive -= 1
            self.message = f"Nice shot! The ship at x = {x}, y = {y}" \
                           f" has been destroyed!"
            return True
        else:
            self.waiting_player.field[y - 1][x - 1] = "*"
            self.active_player.guess_field[y - 1][x - 1] = "*"
            self.message = f"{self.active_player.name} missed the shot!"
            return False

    def _validate(self, user_input):
        try:
            coord_list = user_input.split(",")
            x, y = int(coord_list[0]), int(coord_list[1])
            return True, x, y
        except TypeError:
            self.message = "Invalid input, use only numbers"
            return False, None, None
        except ValueError:
            self.message = \
                "Invalid input, x and y should be integer in range 1 to 10."
            return False, None, None
        except IndexError:
            self.message = "Invalid input, enter both 'x,y' coordinates"
            return False, None, None

    def greet(self):
        self.clear_display()
        print("Welcome to the game 'Sea Battle'!")
        print("This game is designed for 2 players. The target of the game"
              " - destroy all 8 opponent's ships to win.")
        print("You will have 2 10x10 fields for each: your field on "
              "the left side and guess field on the right side.")
        print("Cell symbols: ~ - empty cell, "
              "о - alive ship, х - destroyed ship, * - miss shot\n")

    def run(self):
        self.greet()

        player1_name = input("Input 1st player name >>>")
        player1 = Player(player1_name)
        player2_name = input("Input 2nd player name >>>")
        player2 = Player(player2_name)

        self.active_player = player1
        self.waiting_player = player2

        while True:
            self._draw_fields()
            print(f"\n{self.active_player.name}'s turn. {self.message}")
            player_input = input("Input 'x,y' coordinates of your shot >>>")

            valid = self._validate(player_input)
            if valid[0]:
                x, y = valid[1], valid[2]
                hit = self._hit_check(x, y)
                if not hit:
                    self.clear_display()
                    input(f"{self.message} Press 'Enter' to change the player")
                    self._change_active_player()
            if self.waiting_player.left_alive == 0:
                print(f"Congratulations! {self.active_player.name} won the "
                      f"game with {self.active_player.left_alive} ships alive")
                break


class Player:
    def __init__(self, name):
        self.name = name
        self.field = self._random_field()
        self.guess_field = [["~" for _ in range(10)] for _ in range(10)]
        self.left_alive = 8

    @staticmethod
    def _random_field():
        import random
        field = [["~" for _ in range(10)] for _ in range(10)]
        i = 0
        while i < 8:
            ship_xpos, ship_ypos = random.randrange(10), random.randrange(10)
            if field[ship_ypos][ship_xpos] == "~":
                field[ship_ypos][ship_xpos] = "o"
                i += 1
        return field


new_game = Game()
new_game.run()
