def parse_fen(fen):
    board, turn, castling, en_passant, halfmove_clock, fullmove_number = fen.split()
    return board.split('/'), turn, castling, en_passant, int(halfmove_clock), int(fullmove_number)

# tạo hàm này để tránh trường hợp của quân tốt
def eat_pieces(boardRow, rowIndex, insertPiece):
    tempIndex = 0
    newBoardRow = ''
    for pRow, piece in enumerate(boardRow):
            if piece.isdigit():
                tempIndex += int(piece)
                newBoardRow += piece
            else: 
                if tempIndex == rowIndex:
                    print(f"piece: {piece}, insertPiece: {insertPiece}")
                    if (piece.isupper() and insertPiece.islower()) or (piece.islower() and insertPiece.isupper()):
                        print("Ănnnnnn")
                        newBoardRow += insertPiece
                        newBoardRow += boardRow[pRow+1:]
                        return newBoardRow
                tempIndex += 1
                newBoardRow += piece
    print("Không ăn")
    return newBoardRow
# Hàm này check gặp piece hay không, nếu gặp thì trả về 1, nếu không thì trả về 0
def meet_pieces(boardRow, rowIndex):
    tempIndex = 0
    for pRow, piece in enumerate(boardRow):
            if piece.isdigit():
                tempIndex += int(piece)
            else: 
                if tempIndex == rowIndex:
                    return 1
                tempIndex += 1
    return 0

def update_board_with_fen(boardRow, rowIndex, insertPiece):
    res = ""
    tempIndex = -1
    for pRow, piece in enumerate(boardRow):
        if piece.isdigit():
            if tempIndex + int(piece) >= rowIndex:
                num1 = rowIndex - tempIndex- 1
                num2 = int(tempIndex + int(piece)) - rowIndex
                res +=  (str(num1) if num1 != 0 else '') + insertPiece + (str(num2) if num2 != 0 else '') #return at this 
                res += boardRow[pRow+1:]
                return res
            else:
                tempIndex += int(piece)
                res += piece
        else: 
            tempIndex += 1
            res += piece
        
    return res
#pCol = col, pRow = row 
def move_p(board, pCol, pRow, piece):
    moves = []
    # Di chuyển
    if pCol == 1:
        for new_pCol in range(pCol + 1, pCol + 2):
            print(f"Trying to access board[{new_pCol}][{pRow}]")
            if 0 <= new_pCol < 8:
                moves.append((new_pCol, pRow))
                if meet_pieces(board[new_pCol], pRow):
                    break
                else:
                    print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
        
            else:
                break
    else:
        new_pCol = pCol + 1
        print(f"Trying to access board[{new_pCol}][{pRow}]")
        if 0 <= new_pCol < 8:
            moves.append((new_pCol, pRow))
            # print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
            if not meet_pieces(board[new_pCol], pRow):
                print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
    
    # Ăn
    offsets = [(1, 1), (1, -1)]
    for offset in offsets:
        new_pCol = pCol + offset[0]
        new_pRow = pRow + offset[1]
        print(f"Trying to access board[{new_pCol}][{new_pRow}]")
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            moves.append((new_pCol, new_pRow))
            if meet_pieces(board[new_pCol], new_pRow):
                print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
        else:
            break

    return moves

def move_P(board, pCol, pRow, piece):
    moves = []
    # Di chuyển
    if pCol == 6:
        for new_pCol in range(pCol - 1, pCol - 2):
            print(f"Trying to access board[{new_pCol}][{pRow}]")
            if 0 <= new_pCol < 8:
                moves.append((new_pCol, pRow))
                if meet_pieces(board[new_pCol], pRow):
                    break
                else:
                    print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
        
            else:
                break
    else:
        new_pCol = pCol - 1
        print(f"Trying to access board[{new_pCol}][{pRow}]")
        if 0 <= new_pCol < 8:
            moves.append((new_pCol, pRow))
            # print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
            if not meet_pieces(board[new_pCol], pRow):
                print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
    
    # Ăn
    offsets = [(-1, 1), (-1, -1)]
    for offset in offsets:
        new_pCol = pCol + offset[0]
        new_pRow = pRow + offset[1]
        print(f"Trying to access board[{new_pCol}][{new_pRow}]")
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            moves.append((new_pCol, new_pRow))
            if meet_pieces(board[new_pCol], new_pRow):
                print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
        else:
            break

    return moves

def move_r(board, pCol, pRow, piece):
    moves = []

    # Check all squares in the same pCol to the right of the rook
    for new_pRow in range(pRow + 1, 8):
        if 0 <= pCol < 8 and 0 <= new_pRow < 8:
            print(f"Trying to access board[{pCol}][{new_pRow}]")
            moves.append((pCol, new_pRow))
            # result = update_board_with_fen(board[pCol], new_pRow, piece)
            # if result == board[pCol]:
            #     break
            # print("The new update: " + result)
            if meet_pieces(board[pCol], new_pRow):
                print("The new update: " + eat_pieces(board[pCol], new_pRow, piece))
                break
            else:
                print("The new update: " + update_board_with_fen(board[pCol], new_pRow, piece))
        
        else:
            break
    # Check all squares in the same pCol to the left of the rook
    for new_pRow in range(pRow - 1, -1, -1):
        if 0 <= pCol < 8 and 0 <= new_pRow < 8:
            print(f"Trying to access board[{pCol}][{new_pRow}]")
            moves.append((pCol, new_pRow))
            if meet_pieces(board[pCol], new_pRow):
                print("The new update: " + eat_pieces(board[pCol], new_pRow, piece))
                break
            else:
                print("The new update: " + update_board_with_fen(board[pCol], new_pRow, piece))
        
        else:
            break
    # Check all squares in the same pRow above the rook
    for new_pCol in range(pCol + 1, 8):
        if 0 <= new_pCol < 8 and 0 <= pRow < 8:
            print(f"Trying to access board[{new_pCol}][{pRow}]")
            moves.append((new_pCol, pRow))
            if meet_pieces(board[new_pCol], pRow):
                print("The new update: " + eat_pieces(board[new_pCol], pRow, piece))
                break
            else:
                print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
        
        else:
            break
    # Check all squares in the same pRow below the rook
    for new_pCol in range(pCol - 1, -1, -1):
        if 0 <= new_pCol < 8 and 0 <= pRow < 8:
            print(f"Trying to access board[{new_pCol}][{pRow}]")
            moves.append((new_pCol, pRow))
            if meet_pieces(board[new_pCol], pRow):
                print("The new update: " + eat_pieces(board[new_pCol], pRow, piece))
                break
            else:
                print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
        
        else:
            break
    return moves

def move_b(board, pCol, pRow, piece):
    moves = []

    # Check diagonal squares up-right
    for delta in range(1, min(8 - pCol, 8 - pRow)):
        new_pCol = pCol + delta
        new_pRow = pRow + delta
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            print(f"Trying to access board[{new_pCol}][{new_pRow}]")
            moves.append((new_pCol, new_pRow))
            # result = update_board_with_fen(board[new_pCol], new_pRow,piece)
            if meet_pieces(board[new_pCol], new_pRow):
                print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
                break
            else:
                print("The new update: " + update_board_with_fen(board[new_pCol], new_pRow, piece))
        else:
            break

    # Check diagonal squares up-left
    for delta in range(1, min(8 - pCol, pRow + 1)):
        new_pCol = pCol + delta
        new_pRow = pRow - delta
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            print(f"Trying to access board[{new_pCol}][{new_pRow}]")
            moves.append((new_pCol, new_pRow))
            if meet_pieces(board[new_pCol], new_pRow):
                print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
                break
            else:
                print("The new update: " + update_board_with_fen(board[new_pCol], new_pRow, piece))
        else:
            break

    # Check diagonal squares down-right
    for delta in range(1, min(pCol + 1, 8 - pRow)):
        new_pCol = pCol - delta
        new_pRow = pRow + delta
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            print(f"Trying to access board[{new_pCol}][{new_pRow}]")
            moves.append((new_pCol, new_pRow))
            if meet_pieces(board[new_pCol], new_pRow):
                print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
                break
            else:
                print("The new update: " + update_board_with_fen(board[new_pCol], new_pRow, piece))
        else:
            break

    # Check diagonal squares down-left
    for delta in range(1, min(pCol + 1, pRow + 1)):
        new_pCol = pCol - delta
        new_pRow = pRow - delta
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            print(f"Trying to access board[{new_pCol}][{new_pRow}]")
            moves.append((new_pCol, new_pRow))
            if meet_pieces(board[new_pCol], new_pRow):
                print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
                break
            else:
                print("The new update: " + update_board_with_fen(board[new_pCol], new_pRow, piece))
        else:
            break

    return moves

def move_q(board, pCol, pRow, piece):
    # Combine the movements of a rook and a bishop
    moves = move_r(board, pCol, pRow, piece) + move_b(board, pCol, pRow, piece)
    return moves

def move_k(board, pCol, pRow, piece):
    moves = []
    offsets = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]
    for offset in offsets:
        new_pCol = pCol + offset[0]
        new_pRow = pRow + offset[1]
        print(f"Trying to access board[{new_pCol}][{new_pRow}]")
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            moves.append((new_pCol, new_pRow))
            if meet_pieces(board[new_pCol], new_pRow):
                print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
            else:
                print("The new update: " + update_board_with_fen(board[new_pCol], new_pRow, piece))

        else:
            break
    return moves

def move_n(board, pCol, pRow, piece):
    moves = []
    offsets = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    for offset in offsets:
        new_pCol = pCol + offset[0]
        new_pRow = pRow + offset[1]
        print(f"Trying to access board[{new_pCol}][{new_pRow}]")
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            moves.append((new_pCol, new_pRow))
            if meet_pieces(board[new_pCol], new_pRow):
                print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
            else:
                print("The new update: " + update_board_with_fen(board[new_pCol], new_pRow, piece))
        else:
            break
    return moves


def generate_legal_moves(fen):
    board, _, _, _, _, _ = parse_fen(fen)
    print(board)
    for pCol, row in enumerate(board):
        rowTemp = 0
        for pRow, piece in enumerate(row):
            if piece.isdigit():
                rowTemp += int(piece)
            elif piece == 'k' or piece == 'K':  
                print(f"Vua found at {pCol}, {rowTemp}")
                move_k(board, pCol, rowTemp, piece)
                rowTemp += 1
            elif piece == 'n' or piece == 'N':  
                print(f"Mã found at {pCol}, {rowTemp}")
                move_n(board, pCol, rowTemp, piece)
                rowTemp += 1
                # legal_moves.extend([(pCol, pRow, new_pCol, new_pRow) for new_pCol, new_pRow in knight_moves])
            elif piece == 'p':  
                print(f"Tốt đen found at {pCol}, {rowTemp}")
                move_p(board, pCol, rowTemp, piece)
                rowTemp += 1
            elif piece == 'P':  
                print(f"Tốt trắng found at {pCol}, {rowTemp}")
                move_P(board, pCol, rowTemp, piece)
                rowTemp += 1
            elif piece == 'r' or piece == 'R':  
                print(f"Xe found at {pCol}, {rowTemp}")
                move_r(board, pCol, rowTemp, piece)
                rowTemp += 1
            elif piece == 'b' or piece == 'B':  
                print(f"Tượng found at {pCol}, {rowTemp}")
                move_b(board, pCol, rowTemp, piece)
                rowTemp += 1
            elif piece == 'q' or piece == 'Q':  
                print(f"Hậu found at {pCol}, {rowTemp}")
                move_q(board, pCol, rowTemp, piece)
                rowTemp += 1
            else :
                rowTemp += 1
    # return legal_moves

fen = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1 w KQkq - 0 1"
generate_legal_moves(fen)

# for move in legal_moves:
#     print(move)