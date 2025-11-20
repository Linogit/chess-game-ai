import pygame
import chess
import chess.engine
import os
import time


class ChessGame:
    def __init__(self) -> None:
        # Inizializzazione di Pygame
        pygame.init()
        # Dimensioni della finestra di gioco
        self.__size = 600
        # Correzione delle coordinate per il posizionamento preciso dei pezzi
        self.__error_coords = 5
        # Dizionario per memorizzare i rettangoli delle caselle
        self.__squares = {}
        # Dizionario per memorizzare le immagini dei pezzi
        self.__pieces = {}
        # Creazione della scacchiera logica
        self.__board = chess.Board()
        # Calcolo della dimensione di ogni casella
        self.__square_size = self.__size // 8
        # Creazione della finestra di gioco
        self.__screen = pygame.display.set_mode((self.__size, self.__size))

        # Inizializzazione delle caselle e dei pezzi
        self.__init_squares()
        self.__init_pieces()

        # Flag per il loop principale del gioco
        self.__running = True
        # Casella selezionata (None se nessuna casella è selezionata)
        self.__selected_square = None

        # Avvio del motore scacchistico Stockfish
        # self.__engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
        self.__engine = chess.engine.SimpleEngine.popen_uci(
            "C:/Users/linoq/stockfish/stockfish-windows-x86-64-avx2.exe"
        #    self.__engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        # per far trovare il comando stockfish nel PATH del sistema
         self.__engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        )

        # Velocità di gioco e profondità di ricerca dell'AI
        self.__speed = 0.1
        self.__depth = 3

        # Valori dei pezzi per la valutazione (positivo per nero, negativo per bianco)
        self.__pieces_values = {
            "p": 1,  # Pedone nero
            "P": -1,  # Pedone bianco
            "n": 3,  # Cavallo nero
            "N": -3,  # Cavallo bianco
            "b": 3,  # Alfiere nero
            "B": -3,  # Alfiere bianco
            "r": 5,  # Torre nera
            "R": -5,  # Torre bianca
            "q": 9,  # Regina nera
            "Q": -9,  # Regina bianca
            "k": 999,  # Re nero
            "K": -999,  # Re bianco
        }

    @staticmethod
    def __invert_position(position: str) -> str:
        # Inverte la posizione (specchia la scacchiera)
        return chess.square_name(chess.square_mirror(chess.parse_square(position)))

    def __square_to_pixel(self, square: int) -> (int, int):
        # Converte una coordinata di scacchiera in coordinate pixel
        col = square // 8
        row = square % 8
        return (
            row * self.__square_size + self.__error_coords,
            col * self.__square_size + self.__error_coords,
        )

    def __init_squares(self) -> None:
        # Inizializza i rettangoli delle caselle della scacchiera
        for i in range(64):
            square_name = chess.SQUARE_NAMES[i]
            x, y = chess.square_file(i), chess.square_rank(i)
            rect = pygame.Rect(
                x * self.__square_size,
                y * self.__square_size,
                self.__square_size,
                self.__square_size,
            )
            self.__squares[square_name] = rect

    def __init_pieces(self) -> None:
        # Carica le immagini dei pezzi dai file
        self.__pieces = {
            "P": pygame.image.load(os.path.join("pieces_png", "white_P.png")),
            "p": pygame.image.load(os.path.join("pieces_png", "black_p.png")),
            "R": pygame.image.load(os.path.join("pieces_png", "white_R.png")),
            "r": pygame.image.load(os.path.join("pieces_png", "black_r.png")),
            "B": pygame.image.load(os.path.join("pieces_png", "white_B.png")),
            "b": pygame.image.load(os.path.join("pieces_png", "black_b.png")),
            "K": pygame.image.load(os.path.join("pieces_png", "white_K.png")),
            "k": pygame.image.load(os.path.join("pieces_png", "black_k.png")),
            "Q": pygame.image.load(os.path.join("pieces_png", "white_Q.png")),
            "q": pygame.image.load(os.path.join("pieces_png", "black_q.png")),
            "N": pygame.image.load(os.path.join("pieces_png", "white_N.png")),
            "n": pygame.image.load(os.path.join("pieces_png", "black_n.png")),
        }

    def __draw_chessboard(self):
        # Disegna la scacchiera con colori alternati
        for i in range(8):
            for j in range(8):
                rect = (
                    i * self.__square_size,
                    j * self.__square_size,
                    self.__square_size,
                    self.__square_size,
                )
                # Alterna i colori delle caselle
                color = (200, 150, 100) if not (i + j) % 2 == 0 else (255, 255, 255)
                pygame.draw.rect(self.__screen, color, rect)

    def __draw_pieces(self):
        # Disegna i pezzi sulla scacchiera
        for square in chess.SQUARES:
            piece = self.__board.piece_at(chess.square_mirror(square))
            if piece:
                x, y = self.__square_to_pixel(square)
                self.__screen.blit(self.__pieces[piece.symbol()], (x, y))

    def __update(self):
        # Aggiorna il display
        self.__screen.fill((255, 255, 255))
        self.__draw_chessboard()
        self.__draw_pieces()
        pygame.display.flip()

    def __create_popup(self):
        # Crea un popup per la promozione del pedone

        # Crea la superficie del popup
        popup_size = (self.__size / 3.5, self.__size / 2.5)
        popup = pygame.Surface(popup_size)
        popup_rect = popup.get_rect(center=(self.__size / 2, self.__size / 2))

        # Disegna lo sfondo e il bordo del popup
        pygame.draw.rect(popup, (255, 255, 255), (0, 0, popup_size[0], popup_size[1]))
        pygame.draw.rect(popup, (0, 0, 0), (0, 0, popup_size[0], popup_size[1]), 2)

        # Crea i pulsanti per il popup
        font = pygame.font.Font(None, 30)
        button_texts = ["DONNA", "TORRE", "ALFIERE", "CAVALLO"]
        pieces = ["q", "r", "b", "n"]
        buttons = []
        for i, text in enumerate(button_texts):
            button = pygame.Surface((130, 30))
            pygame.draw.rect(button, (0, 0, 0), (0, 0, 130, 30))
            button_text = font.render(text, True, (255, 255, 255))
            button.blit(button_text, (30, 6))
            buttons.append(button)

        # Posiziona i pulsanti sul popup
        button_rects = []
        for i, button in enumerate(buttons):
            button_rect = button.get_rect(center=(popup_size[0] / 2, 60 + i * 42))
            popup.blit(button, button_rect)
            button_rects.append(button_rect)

        # Attende la selezione dell'utente
        self.__screen.blit(popup, popup_rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Controlla se l'utente ha cliccato su uno dei pulsanti
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos = (
                        mouse_pos[0] - ((self.__size / 2) - ((self.__size / 3.5) / 2)),
                        mouse_pos[1] - ((self.__size / 2) - ((self.__size / 2.5) / 2)),
                    )
                    for i, button_rect in enumerate(button_rects):
                        if button_rect.collidepoint(mouse_pos):
                            return pieces[i]

    def __highlight_selected(self):
        # Evidenzia la casella selezionata
        coords = self.__square_to_pixel(chess.parse_square(self.__selected_square))
        highlight_surface = pygame.Surface(
            (self.__square_size, self.__square_size), pygame.SRCALPHA
        )
        highlight_surface.fill((250, 237, 39))
        highlight_surface.set_alpha(80)
        self.__screen.blit(
            highlight_surface,
            (
                coords[0] - self.__error_coords,
                self.__size - coords[1] + self.__error_coords - self.__square_size,
            ),
        )

    def __highlight_check(self):
        # Evidenzia il re sotto scacco
        king_square = self.__square_to_pixel(
            chess.square_mirror(self.__board.king(self.__board.turn))
        )
        check_surface = pygame.Surface(
            (self.__square_size, self.__square_size), pygame.SRCALPHA
        )
        check_surface.fill((255, 0, 0))
        check_surface.set_alpha(80)
        self.__screen.blit(
            check_surface,
            (
                king_square[0] - self.__error_coords,
                king_square[1] - self.__error_coords,
            ),
        )

    def __ai_turn(self):
        # Gestisce il turno dell'AI usando l'algoritmo minimax
        value, mov_ai = self.__minimax(
            self.__board, self.__depth, -float("inf"), float("inf"), True
        )
        self.__board.push(mov_ai)
        # result = self.__engine.play(self.__board, chess.engine.Limit(depth=5))
        # self.__board.push(result.move)
        self.__update()

        if self.__board.is_check():
            print("scacco")
            self.__highlight_check()
            pygame.display.update()

    def __select_or_move(self, square):
        # Gestisce la selezione di un pezzo o il movimento
        piece = self.__board.piece_at(chess.parse_square(square))
        promotion = ""
        if piece and piece.color:
            self.__update()

            if self.__board.is_check():
                self.__highlight_check()

            self.__selected_square = square
            legal_moves = list(self.__board.legal_moves)
            legal_moves = [
                move
                for move in legal_moves
                if move.from_square == chess.parse_square(square)
            ]

            destination_squares = []

            self.__highlight_selected()

            for move in legal_moves:
                is_capturable = False
                tmp_moves = list(self.__board.legal_moves)
                lgl_moves = str(self.__board.legal_moves)
                lgl_moves = lgl_moves.split("(")[1]
                lgl_moves = lgl_moves.split(")")[0]
                lgl_moves = lgl_moves.split(",")
                c = 0

                for mov in tmp_moves:
                    if move == mov:
                        break
                    c += 1

                if "x" in lgl_moves[c]:
                    is_capturable = True

                destination_square = self.__square_to_pixel(move.to_square)
                destination_squares.append([destination_square, is_capturable])

            for i, ((x, y), z) in enumerate(destination_squares):
                destination_squares[i][0] = (x + 25, y + 25)

            for (x, y), z in destination_squares:
                lgl_moves_surface = pygame.Surface(
                    (self.__square_size, self.__square_size), pygame.SRCALPHA
                )
                lgl_moves_surface.set_alpha(100)
                if z:
                    # Evidenzia le mosse di cattura
                    pygame.draw.circle(
                        lgl_moves_surface,
                        (128, 128, 128),
                        (self.__square_size / 2 + 1, self.__square_size / 2 - 1),
                        self.__square_size / 2.2,
                        5,
                    )
                    self.__screen.blit(
                        lgl_moves_surface,
                        (
                            (x + self.__error_coords - self.__square_size / 2) + 3,
                            self.__size
                            - y
                            - self.__error_coords
                            - self.__square_size / 2,
                        ),
                    )
                else:
                    # Evidenzia le mosse normali
                    pygame.draw.circle(
                        lgl_moves_surface,
                        (128, 128, 128),
                        (self.__square_size / 2, self.__square_size / 2),
                        self.__square_size / 5,
                    )
                    self.__screen.blit(
                        lgl_moves_surface,
                        (
                            (x + self.__error_coords - self.__square_size / 2) + 3,
                            self.__size
                            - y
                            - self.__error_coords
                            - self.__square_size / 2,
                        ),
                    )

            pygame.display.update()
        elif self.__selected_square:
            # Gestisce il movimento del pezzo

            sq = self.__selected_square[0]
            s = square[0]

            diff = abs(ord(sq) - ord(s))

            if (
                self.__board.piece_at(
                    chess.parse_square(self.__selected_square)
                ).symbol()
                == "P"
                and "8" in square
                and "7" in self.__selected_square
                and self.__board.turn
                and (
                    diff == 0
                    and not self.__board.piece_at(chess.parse_square(square))
                    or (diff == 1 and self.__board.piece_at(chess.parse_square(square)))
                )
            ):
                # Promozione del pedone
                promotion = self.__create_popup()

            mv = chess.Move.from_uci(self.__selected_square + square + promotion)

            done_move = False

            if mv in self.__board.legal_moves:
                self.__board.push(mv)
                done_move = True

            self.__selected_square = None
            self.__update()

            if self.__board.is_check():
                self.__highlight_check()
                pygame.display.update()

            if (
                self.__board.is_checkmate()
                or self.__board.is_stalemate()
                or self.__board.is_repetition()
            ):
                time.sleep(2)
                self.__popup_game_over()

            if done_move:
                self.__ai_turn()

            if (
                self.__board.is_checkmate()
                or self.__board.is_stalemate()
                or self.__board.is_repetition()
            ):
                time.sleep(2)
                self.__popup_game_over()

    def __popup_game_over(self):
        # Mostra il popup di fine partita
        popup_size = (self.__size / 1.8, self.__size / 3)
        popup = pygame.Surface(popup_size)
        popup_rect = popup.get_rect(center=(self.__size / 2, self.__size / 2))

        # Disegna lo sfondo e il bordo del popup
        pygame.draw.rect(popup, (255, 255, 255), (0, 0, popup_size[0], popup_size[1]))
        pygame.draw.rect(popup, (0, 0, 0), (0, 0, popup_size[0], popup_size[1]), 2)

        ##

        result = self.__board.result()

        font = pygame.font.Font(None, 50)

        lbl = pygame.Surface((popup_size[0] / 1.2, popup_size[1] / 2))
        pygame.draw.rect(lbl, (255, 255, 255), (0, 0, popup_size[0], popup_size[1]))
        lbl_text = font.render("GAME OVER!", True, (0, 0, 0))
        if result == "*":
            result = "1/2-1/2"
        lbl_text_2 = font.render(result, True, (0, 0, 0))
        lbl.blit(lbl_text, (30, 6))
        lbl.blit(lbl_text_2, (popup_size[0] / 2 - 50, 55))

        lbl_rect = lbl.get_rect(center=(popup_size[0] / 2 - 2, 100))
        popup.blit(lbl, lbl_rect)

        self.__screen.blit(popup, popup_rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    break

    def __minimax(self, board, depth, alpha, beta, maximizingPlayer):
        # Algoritmo minimax con alpha-beta pruning
        if depth == 0 or board.is_game_over():
            # Valuta la posizione usando Stockfish
            info = self.__engine.analyse(self.__board, chess.engine.Limit(depth=0))
            score = info["score"].black()

            if not score.score():
                # Gestisce le situazioni di scacco matto
                if score.mate() == 31:
                    return 8899, None
                elif score.mate() == 30:
                    return 8999, None
                elif score.mate() == 29:
                    return 9199, None
                elif score.mate() == 28:
                    return 9299, None
                elif score.mate() == 27:
                    return 9399, None
                elif score.mate() == 26:
                    return 9499, None
                elif score.mate() == 25:
                    return 9599, None
                elif score.mate() == 24:
                    return 9699, None
                elif score.mate() == 23:
                    return 9799, None
                elif score.mate() == 22:
                    return 9899, None
                elif score.mate() == 21:
                    return 9999, None
                elif score.mate() == 20:
                    return 10999, None
                elif score.mate() == 19:
                    return 11999, None
                elif score.mate() == 18:
                    return 12999, None
                elif score.mate() == 17:
                    return 13999, None
                elif score.mate() == 16:
                    return 14999, None
                elif score.mate() == 15:
                    return 15999, None
                elif score.mate() == 14:
                    return 16999, None
                elif score.mate() == 13:
                    return 17999, None
                elif score.mate() == 12:
                    return 18999, None
                elif score.mate() == 11:
                    return 19999, None
                elif score.mate() == 10:
                    return 20999, None
                elif score.mate() == 9:
                    return 21999, None
                elif score.mate() == 8:
                    return 22999, None
                elif score.mate() == 7:
                    return 23999, None
                elif score.mate() == 6:
                    return 24999, None
                elif score.mate() == 5:
                    return 25999, None
                elif score.mate() == 4:
                    return 26999, None
                elif score.mate() == 3:
                    return 27999, None
                elif score.mate() == 2:
                    return 28999, None
                elif score.mate() == 1:
                    return 29999, None
                elif score.mate() == 0:
                    return 31999, None
                else:
                    return -9999, None
            return score.score(), None

        # Inizializza la variabile che conterrà la mossa migliore trovata
        bestMove = None

        # Verifica se siamo nel nodo massimizzatore (giocatore AI)
        if maximizingPlayer:
            # MASSIMIZZATORE (GIOCATORE AI)
            # Inizializza il miglior valore a -infinito (peggior valore possibile per il massimizzatore)
            bestValue = -float("inf")

            # Itera attraverso tutte le mosse legali disponibili nella posizione corrente
            for move in board.legal_moves:
                # Esegue la mossa sulla scacchiera (modifica lo stato della board)
                board.push(move)

                # Chiamata ricorsiva a minimax per valutare la mossa appena fatta:
                # - depth - 1: diminuisce la profondità di ricerca
                # - False: il prossimo giocatore sarà il minimizzatore (avversario)
                # - alpha, beta: passa i valori per l'alpha-beta pruning
                value, _ = self.__minimax(board, depth - 1, alpha, beta, False)

                # Annulla la mossa (ripristina lo stato precedente della scacchiera)
                board.pop()

                # Se il valore della mossa corrente è migliore del miglior valore trovato finora
                if value > bestValue:
                    bestValue = value  # Aggiorna il miglior valore
                    bestMove = move  # Aggiorna la mossa migliore

                # ALPHA-BETA PRUNING: Aggiorna il valore alpha
                # Alpha rappresenta il miglior valore garantito per il massimizzatore
                alpha = max(alpha, bestValue)

                # PRUNING CONDITION: Se beta <= alpha, interrompi la ricerca in questo ramo
                # Beta rappresenta il miglior valore garantito per il minimizzatore
                # Se beta <= alpha significa che l'avversario (minimizzatore) ha già una mossa
                # che garantisce un risultato peggiore di quanto abbiamo già trovato,
                # quindi non ha senso continuare a esplorare questo ramo
                if beta <= alpha:
                    break  # Interrompe il ciclo for (pruning)

            # Restituisce il miglior valore trovato e la mossa corrispondente
            return bestValue, bestMove

        else:
            # MINIMIZZATORE (GIOCATORE UMANO o AVVERSARIO)
            # Inizializza il miglior valore a +infinito (peggior valore possibile per il minimizzatore)
            bestValue = float("inf")

            # Itera attraverso tutte le mosse legali disponibili
            for move in board.legal_moves:
                # Esegue la mossa sulla scacchiera
                board.push(move)

                # Chiamata ricorsiva a minimax:
                # - depth - 1: diminuisce la profondità
                # - True: il prossimo giocatore sarà il massimizzatore (AI)
                value, _ = self.__minimax(board, depth - 1, alpha, beta, True)

                # Annulla la mossa
                board.pop()

                # Se il valore della mossa corrente è migliore (più basso) per il minimizzatore
                if value < bestValue:
                    bestValue = (
                        value  # Aggiorna il miglior valore (più basso possibile)
                    )
                    bestMove = move  # Aggiorna la mossa migliore

                # ALPHA-BETA PRUNING: Aggiorna il valore beta
                # Beta rappresenta il miglior valore garantito per il minimizzatore
                beta = min(beta, bestValue)

                # PRUNING CONDITION: Se beta <= alpha, interrompi la ricerca
                # Significa che il massimizzatore ha già una mossa che garantisce
                # un risultato migliore di quanto stiamo trovando per il minimizzatore
                if beta <= alpha:
                    break  # Interrompe il ciclo for (pruning)

            # Restituisce il miglior valore trovato e la mossa corrispondente
            return bestValue, bestMove

    def run(self):
        # Loop principale del gioco
        self.__update()
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Gestisce il clic del mouse sulle caselle
                    for square in self.__squares:
                        if self.__squares[square].collidepoint(event.pos):
                            self.__select_or_move(self.__invert_position(square))
                            break


if __name__ == "__main__":
    # Crea e avvia il gioco
    ca = ChessGame()
    ca.run()
