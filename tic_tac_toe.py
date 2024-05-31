import tkinter as tk
from tkinter import messagebox
import random

# Initialisierung der Emojis
PLAYER_EMOJI = '🤩'  
COMPUTER_EMOJI = '😎' 


def draw_board(board, buttons):
    # Aktualisiert die Buttons entsprechend dem Spielbrett
    for i in range(1, 10):
        buttons[i - 1].config(text=board[i])


def input_player_emoji():
    # Fragt den Spieler, welches Emoji er sein möchte
    return [PLAYER_EMOJI, COMPUTER_EMOJI]


def who_goes_first():
    # Zufällige Auswahl, wer zuerst geht
    return 'computer' if random.randint(0, 1) == 0 else 'player'


def make_move(board, emoji, move):
    # Setzt das Emoji auf das Spielbrett
    board[move] = emoji


def is_winner(bo, le):
    # Prüft, ob ein Spieler gewonnen hat
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or
            (bo[4] == le and bo[5] == le and bo[6] == le) or
            (bo[1] == le and bo[2] == le and bo[3] == le) or
            (bo[7] == le and bo[4] == le and bo[1] == le) or
            (bo[8] == le and bo[5] == le and bo[2] == le) or
            (bo[9] == le and bo[6] == le and bo[3] == le) or
            (bo[7] == le and bo[5] == le and bo[3] == le) or
            (bo[9] == le and bo[5] == le and bo[1] == le))


def is_space_free(board, move):
    # Prüft, ob das Feld auf dem Spielbrett frei ist
    return board[move] == ' '


def get_player_move(board, buttons):
    # Ermöglicht dem Spieler einen Zug zu machen
    for i, button in enumerate(buttons, start=1):
        if is_space_free(board, i):
            button.config(state='normal')
        else:
            button.config(state='disabled')


def choose_random_move_from_list(board, moves_list):
    # Wählt einen zufälligen Zug aus einer Liste aus
    possible_moves = [i for i in moves_list if is_space_free(board, i)]
    return random.choice(possible_moves) if possible_moves else None


def get_computer_move(board, computer_emoji):
    # Funktion, die den Computerzug bestimmt
    player_emoji = PLAYER_EMOJI if computer_emoji == COMPUTER_EMOJI else COMPUTER_EMOJI  # Festlegen des Spieler-Emojis

    for i in range(1, 10):  # Schleife über die möglichen Züge
        board_copy = board[:]  # Kopie des aktuellen Spielbretts
        if is_space_free(board_copy, i):  # Überprüfung, ob das Feld frei ist
            make_move(board_copy, computer_emoji, i)  # Setzen des Computer-Emojis auf das Spielbrett
            if is_winner(board_copy, computer_emoji):  # Überprüfung, ob der Computer gewinnen kann
                return i  # Rückgabe des Zugindexes

    for i in range(1, 10):  # Weitere Schleife über die möglichen Züge
        board_copy = board[:]  # Erneute Kopie des aktuellen Spielbretts
        if is_space_free(board_copy, i):  # Überprüfung, ob das Feld frei ist
            make_move(board_copy, player_emoji, i)  # Setzen des Spieler-Emojis auf das Spielbrett
            if is_winner(board_copy, player_emoji):  # Überprüfung, ob der Spieler gewinnen kann
                return i  # Rückgabe des Zugindexes

    move = choose_random_move_from_list(board, [1, 3, 7, 9])  # Auswahl eines Zuges aus den Eckfeldern
    if move:  # Überprüfung, ob ein Zug verfügbar ist
        return move  # Rückgabe des Zugindexes

    if is_space_free(board, 5):  # Überprüfung, ob das Zentrum frei ist
        return 5  # Rückgabe des Zugindexes für das Zentrum

    return choose_random_move_from_list(board, [2, 4, 6, 8])  # Auswahl eines Zuges aus den Seitenelementen



def is_board_full(board):
    # Prüft, ob das Spielbrett voll ist
    return all(not is_space_free(board, i) for i in range(1, 10))


def main():
    root = tk.Tk()
    root.title("Tic Tac Toe with Emojis")

    the_board = [' '] * 10  # Initialisierung des Spielbretts
    player_emoji, computer_emoji = input_player_emoji()  # Eingabe der Spieler- und Computer-Emojis
    turn = who_goes_first()  # Bestimmung des Startspielers

    buttons = [tk.Button(root, text=' ', font='Arial 20', width=5, height=2,
                         command=lambda i=i: player_move(i)) for i in range(1, 10)]  # Erstellung der Buttons

    for i, button in enumerate(buttons):
        button.grid(row=i // 3, column=i % 3)  # Anordnung der Buttons im Raster

    def player_move(i):
        nonlocal turn
        if is_space_free(the_board, i):  # Überprüfung, ob das Feld frei ist
            make_move(the_board, player_emoji, i)  # Setzen des Spieler-Emojis auf das Spielbrett
            draw_board(the_board, buttons)  # Aktualisierung der Anzeige
            if is_winner(the_board, player_emoji):
                messagebox.showinfo("Tic Tac Toe", "Hooray! You have won the game!")
                root.quit()
            elif is_board_full(the_board):
                messagebox.showinfo("Tic Tac Toe", "The game is a tie!")
                root.quit()
            else:
                turn = 'computer'  # Wechsel zum Computerzug
                computer_move()

    def computer_move():
        nonlocal turn
        move = get_computer_move(the_board, computer_emoji)  # Bestimmung des Computerzugs
        make_move(the_board, computer_emoji, move)  # Setzen des Computer-Emojis auf das Spielbrett
        draw_board(the_board, buttons)  # Aktualisierung der Anzeige
        if is_winner(the_board, computer_emoji):
            messagebox.showinfo("Tic Tac Toe", "The computer has beaten you! You lose.")
            root.quit()
        elif is_board_full(the_board):
            messagebox.showinfo("Tic Tac Toe", "The game is a tie!")
            root.quit()
        else:
            turn = 'player'  # Wechsel zum Spielerzug
            get_player_move(the_board, buttons)

    if turn == 'player':
        get_player_move(the_board, buttons)
    else:
        computer_move()

    root.mainloop()


if __name__ == "__main__":
    main()
