import numpy as np
import argparse
from models import ConnectFourGameSettings, UserInput
from pydantic import ValidationError


class ConnectFour:
    def __init__(self, height: int = 6, width: int = 7, player_num: int = 2):
        """
        constructor for class ConnectFour

        :param height: int: the height of the game board
        :param width: int: the width of the game board
        :param player_num: int: the number of players in the game
        """
        self.height = height
        self.width = width
        self.board = np.zeros((height, width))
        self.game_over = False
        self.player = 1
        self.player_num = player_num

    def drop_piece(self, row, col):
        """
        updates the board matrix

        :param row: int: row index of new move
        :param col: int: column index of new move
        """
        self.board[row][col] = self.player

    def is_valid_move(self, col):
        """
        checks if move is valid at column col for current board setting

        :param col: int: column index of new move
        :returns: True if a move is valid else False
        """
        return self.board[self.height-1][col] == 0  

    def get_next_open_row(self, col):
        """
        get empty row index where piece will land

        :param col: int: column index of new move
        :returns: int: row index of empty cell where the piece will land
        """
        for r in range(self.height):
            if self.board[r][col] == 0:
                return r

    def check_win(self):
        """
        checks if player has won the game.

        :returns: True if player has won the game else False
        """
        # Check horizontal win
        for c in range(self.width - 3):
            for r in range(self.height):
                if (
                    self.board[r][c] == self.player
                    and self.board[r][c + 1] == self.player
                    and self.board[r][c + 2] == self.player
                    and self.board[r][c + 3] == self.player
                ):
                    return True

        # Check vertical win
        for c in range(self.width):
            for r in range(self.height - 3):
                if (
                    self.board[r][c] == self.player
                    and self.board[r + 1][c] == self.player
                    and self.board[r + 2][c] == self.player
                    and self.board[r + 3][c] == self.player
                ):
                    return True

        # Check diagonal up-right win
        for c in range(self.width - 3):
            for r in range(3, self.height):
                if (
                    self.board[r][c] == self.player
                    and self.board[r - 1][c + 1] == self.player
                    and self.board[r - 2][c + 2] == self.player
                    and self.board[r - 3][c + 3] == self.player
                ):
                    return True

        # Check diagonal up-left win
        for c in range(self.width - 3):
            for r in range(self.height - 3):
                if (
                    self.board[r][c] == self.player
                    and self.board[r + 1][c + 1] == self.player
                    and self.board[r + 2][c + 2] == self.player
                    and self.board[r + 3][c + 3] == self.player
                ):
                    return True

        return False

    def run(self):

        print(f"Game for {self.player_num} players starts: \n")
        print(np.flipud(self.board))

        board = self.board

        while not self.game_over:
            input_value = input(
                f"Player {self.player}, make your selection (0-{self.width-1}): "
            )

            col = UserInput(value=input_value, max_value=self.width - 1)

            if self.is_valid_move(col.value):
                row = self.get_next_open_row(col.value)
                self.drop_piece(row, col.value)

                if self.check_win():
                    print(f"Player {self.player} wins!")
                    self.game_over = True

                if 0 not in board:
                    print("The game is a draw!")
                    self.game_over = True
            else:
                print("Invalid move, try again.")
                continue

            print(np.flipud(self.board))

            self.player = self.player + 1 if self.player < self.player_num else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect Four game configuration")
    parser.add_argument(
        "--height", type=int, default=6, help="the height of the game board"
    )
    parser.add_argument(
        "--width", type=int, default=7, help="the width of the game board"
    )
    parser.add_argument(
        "--players", type=int, default=2, help="the number of players in the game"
    )
    args = parser.parse_args()

    game_settings_input = {
        "height": args.height,
        "width": args.width,
        "player_num": args.players,
    }

    # TODO: Create custom error instead of Validation error

    try:
        game_settings = ConnectFourGameSettings(**game_settings_input)
        ConnectFour(**game_settings_input).run()
    except ValidationError as e:
        print(e.json())
