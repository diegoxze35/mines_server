from socket import socket, AF_INET, SOCK_STREAM, gethostname, gethostbyname
import sys
import pickle

from Board import Board
from Difficulty import Difficulty

game_over = False

def get_fake_board(size_board: int) -> str:
    fake_board = '\t'
    for i in range(size_board):
        fake_board += f'{i}\t'
    else:
        fake_board += '\n'
    fake_board += '\t'
    fake_board += '_' * (len(fake_board) * 2)
    fake_board += '\n'
    for i in range(size_board):
        fake_board += f' {i}|\t'
        for _ in range(size_board):
            fake_board += '-\t'
        fake_board += '\n'
    return fake_board


def set_game_over():
    global game_over
    game_over = True


if __name__ == '__main__':
    port = int(sys.argv[1])
    ip = gethostbyname(gethostname())
    print(f'My IP is {ip}')
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen(1)
        s.setblocking(True)
        conn, addr = s.accept()
        print(f'Connected to {addr[0]}:{addr[1]}!')
        with conn:
            difficulty: Difficulty = pickle.loads(conn.recv(1024))
            print(f'{addr[0]} has selected {difficulty}')
            fake = get_fake_board(difficulty.squares)
            conn.send(pickle.dumps(fake))
            first_point = pickle.loads(conn.recv(48))
            print(f'{addr[0]} has selected {first_point} as the first point!')
            board = Board(first_shoot=first_point, difficulty=difficulty, on_click_mine=set_game_over)
            while not game_over:
                conn.send(pickle.dumps(str(board)))
                coordinates = pickle.loads(conn.recv(48))
                print(coordinates)
                board.on_click_square(coordinates)
                if board.player_has_won():
                    break
            if game_over:
                message = 'Game Over!'
                board.reveal_mines()
                conn.send(pickle.dumps((message, str(board))))
            else:
                message = 'You won!'
                conn.send(pickle.dumps((message, str(board))))