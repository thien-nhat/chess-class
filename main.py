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
                        # print("Ănnnnnn")
                        newBoardRow += insertPiece
                        newBoardRow += boardRow[pRow+1:]
                        return newBoardRow
                tempIndex += 1
                newBoardRow += piece
    # print("Không ăn")
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

def update_old_fen(boardRow, rowIndex):
    # print("Old fen", boardRow, rowIndex)
    res = ""
    tempIndex = 0
    for pRow, piece in enumerate(boardRow):
        if piece.isdigit():
            tempIndex += int(piece)
            res += piece
        else:
            if tempIndex == rowIndex:
                if pRow + 1 < len(boardRow) and boardRow[pRow + 1].isdigit(): #check again
                    num = 0
                    if pRow > 0 and boardRow[pRow - 1].isdigit():
                        # print("Res before cut " + res)
                        res = res[:-1]
                        # print("Res after cut " + res)
                        num += int(boardRow[pRow - 1])
                    num += int(boardRow[pRow + 1]) + 1
                    res += str(num)
                    res += boardRow[pRow+2:]
                else:
                    num = 0
                    if pRow > 0 and boardRow[pRow - 1].isdigit():
                        # print("Res before cut " + res)
                        res = res[:-1]
                        # print("Res after cut " + res)
                        num += int(boardRow[pRow - 1])
                    num += 1
                    res += str(num)
                    res+= boardRow[pRow+1:]
                return res
            tempIndex += 1
            res += piece
    return res

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
        for new_pCol in range(pCol + 1, pCol + 3):
            print(f"Trying to access board[{new_pCol}][{pRow}]")
            newboard = board.copy()
            if 0 <= new_pCol < 8:
                if meet_pieces(board[new_pCol], pRow):
                    break
                else:
                    # print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
                    newboard[pCol] =  update_old_fen(board[pCol], pRow)
                    newboard[new_pCol] = update_board_with_fen(board[new_pCol], pRow, piece)         
                    result = '/'.join(newboard)
                    print(result)
                    moves.append(result)
        
    else:
        new_pCol = pCol + 1
        print(f"Trying to eating access board[{new_pCol}][{pRow}]")
        newboard = board.copy()
        if 0 <= new_pCol < 8:
            # print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
            if not meet_pieces(board[new_pCol], pRow):
                # print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                newboard[new_pCol] = update_board_with_fen(board[new_pCol], pRow, piece)         
                result = '/'.join(newboard)
                print(result)
                moves.append(result)
    
    # Ăn
    print("ear")
    offsets = [(1, 1), (1, -1)]
    for offset in offsets:
        new_pCol = pCol + offset[0]
        new_pRow = pRow + offset[1]
        print(f"Trying to access board[{new_pCol}][{new_pRow}]")
        newboard = board.copy()
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            if meet_pieces(board[new_pCol], new_pRow):
                # print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
                result = eat_pieces(board[new_pCol], new_pRow, piece)         
                if newboard[new_pCol] == result:
                    continue
                newboard[new_pCol] = result
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                result = '/'.join(newboard)
                print(result) 
                moves.append(result)

    return moves

def move_P(board, pCol, pRow, piece):
    moves = []
    # Di chuyển
    if pCol == 6:
        print(f"Tốt trying to access board[{pCol}][{pRow}]")
        for new_pCol in range(5,3,-1):
            print(f"Trying to access board[{new_pCol}][{pRow}]")
            newboard = board.copy()
            if 0 <= new_pCol < 8:
                if meet_pieces(board[new_pCol], pRow):
                    break
                else:
                    # print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
                    newboard[pCol] =  update_old_fen(board[pCol], pRow)
                    newboard[new_pCol] = update_board_with_fen(board[new_pCol], pRow, piece)         
                    result = '/'.join(newboard)
                    print(result)
                    moves.append(result)    
    else:
        new_pCol = pCol - 1
        print(f"Trying to access board[{new_pCol}][{pRow}]")
        newboard = board.copy()
        if 0 <= new_pCol < 8:
            # print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
            if not meet_pieces(board[new_pCol], pRow):
                # print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                newboard[new_pCol] = update_board_with_fen(board[new_pCol], pRow, piece)         
                result = '/'.join(newboard)
                print(result)
                moves.append(result)   
    
    # Ăn
    offsets = [(-1, 1), (-1, -1)]
    for offset in offsets:
        new_pCol = pCol + offset[0]
        new_pRow = pRow + offset[1]
        print(f"Trying to access board[{new_pCol}][{new_pRow}]")
        newboard = board.copy()
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            if meet_pieces(board[new_pCol], new_pRow):
                # print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
                result = eat_pieces(board[new_pCol], new_pRow, piece)
                # print(result)
                # print(newboard[new_pCol])        
                if newboard[new_pCol] == result:
                    continue
                newboard[new_pCol] = result
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                result = '/'.join(newboard)
                print(result)
                moves.append(result)

    return moves

def move_r(board, pCol, pRow, piece):
    moves = []
    # Check all squares in the same pCol to the right of the rook
    for new_pRow in range(pRow + 1, 8):
        if 0 <= pCol < 8 and 0 <= new_pRow < 8:
            print(f"Trying to access board[{pCol}][{new_pRow}]")
            newboard = board.copy()
            # result = update_board_with_fen(board[pCol], new_pRow, piece)
            # if result == board[pCol]:
            #     break
            # print("The new update: " + result)
            if meet_pieces(board[pCol], new_pRow):
                # print("The new update: " + eat_pieces(board[pCol], new_pRow, piece))
                # board[pCol] =  update_old_fen(board[pCol], pRow)
                result = eat_pieces(board[pCol], new_pRow, piece)
                if newboard[pCol]  == result:
                    break
                newboard[pCol] = result
                newboard[pCol] =  update_old_fen(newboard[pCol], pRow) 
                result = '/'.join(newboard)
                print(result)
                moves.append(result) 
                break
            else:
                # print("The new update: " + update_board_with_fen(board[pCol], new_pRow, piece))
                result = update_old_fen(board[pCol], pRow)
                newboard[pCol] = update_board_with_fen(result, new_pRow, piece)         
                result = '/'.join(newboard)
                print(result)
                moves.append(result)    
        
        else:
            break
    # Check all squares in the same pCol to the left of the rook
    for new_pRow in range(pRow - 1, -1, -1):
        if 0 <= pCol < 8 and 0 <= new_pRow < 8:
            print(f"Trying to access board[{pCol}][{new_pRow}]")
            newboard = board.copy()
            if meet_pieces(board[pCol], new_pRow):
                # print("The new update: " + eat_pieces(board[pCol], new_pRow, piece))
                result = eat_pieces(board[pCol], new_pRow, piece) 
                if newboard[pCol]   == result:
                    break
                newboard[pCol] = result
                newboard[pCol] =  update_old_fen(newboard[pCol], pRow)
                result = '/'.join(newboard)
                print(result)
                moves.append(result) 
                break
            else:
                # print("The new update: " + update_board_with_fen(board[pCol], new_pRow, piece))
                result =  update_old_fen(board[pCol], pRow)
                # print(result)
                newboard[pCol] = update_board_with_fen(result, new_pRow, piece)         
                result = '/'.join(newboard)
                print(result)
                moves.append(result) 
        
    # Check all squares in the same pRow above the rook
    for new_pCol in range(pCol + 1, 8):
        if 0 <= new_pCol < 8 and 0 <= pRow < 8:
            print(f"Trying to access board[{new_pCol}][{pRow}]")
            newboard = board.copy()
            if meet_pieces(board[new_pCol], pRow):
                # print("The new update: " + eat_pieces(board[new_pCol], pRow, piece))
                result = eat_pieces(board[new_pCol], pRow, piece)         
                if newboard[new_pCol] == result:
                    break
                newboard[new_pCol] = result
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                result = '/'.join(newboard)
                print(result)
                moves.append(result)
                break
            else:
                # print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                newboard[new_pCol] = update_board_with_fen(board[new_pCol], pRow, piece)         
                result = '/'.join(newboard)
                print(result)
                moves.append(result) 
        
    # Check all squares in the same pRow below the rook
    for new_pCol in range(pCol - 1, -1, -1):
        if 0 <= new_pCol < 8 and 0 <= pRow < 8:
            print(f"Trying to access board[{new_pCol}][{pRow}]")
            newboard = board.copy()
            if meet_pieces(board[new_pCol], pRow):
                # print("The new update: " + eat_pieces(board[new_pCol], pRow, piece))
                result = eat_pieces(board[new_pCol], pRow, piece)
                if newboard[new_pCol] == result:
                    break
                newboard[new_pCol] = result
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                result = '/'.join(newboard)
                print(result)
                moves.append(result)
                break
            else:
                # print("The new update: " + update_board_with_fen(board[new_pCol], pRow, piece))
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                newboard[new_pCol] = update_board_with_fen(board[new_pCol], pRow, piece)
                result = '/'.join(newboard)
                print(result)
                moves.append(result) 
    return moves

def move_b(board, pCol, pRow, piece):
    moves = []
    # Check diagonal squares up-right
    for delta in range(1, min(8 - pCol, 8 - pRow)):
        new_pCol = pCol + delta
        new_pRow = pRow + delta
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            print(f"Trying to access board[{new_pCol}][{new_pRow}]")
            # result = update_board_with_fen(board[new_pCol], new_pRow,piece)
            if meet_pieces(board[new_pCol], new_pRow):
                # print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
                newboard = board.copy()
                result = eat_pieces(board[new_pCol], new_pRow, piece) 
                if newboard[new_pCol] == result:
                    break
                newboard[new_pCol] = result        
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                result = '/'.join(newboard)
                print(result)
                moves.append(result)
                break
            else:
                # print("The new update: " + update_board_with_fen(board[new_pCol], new_pRow, piece))
                newboard = board.copy()
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                newboard[new_pCol] = update_board_with_fen(board[new_pCol], new_pRow, piece)         
                result = '/'.join(newboard)
                print(result)
                moves.append(result)

    # Check diagonal squares up-left
    for delta in range(1, min(8 - pCol, pRow + 1)):
        new_pCol = pCol + delta
        new_pRow = pRow - delta
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            print(f"Trying to access board[{new_pCol}][{new_pRow}]")
            if meet_pieces(board[new_pCol], new_pRow):
                # print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
                newboard = board.copy()
                result = eat_pieces(board[new_pCol], new_pRow, piece)         
                if newboard[new_pCol] == result:
                    break
                newboard[new_pCol] = result
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                result = '/'.join(newboard)
                print(result)
                moves.append(result)
                break
            else:
                # print("The new update: " + update_board_with_fen(board[new_pCol], new_pRow, piece))
                newboard = board.copy()
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                newboard[new_pCol] = update_board_with_fen(board[new_pCol], new_pRow, piece)         
                result = '/'.join(newboard)
                print(result)
                moves.append(result)

    # Check diagonal squares down-right
    for delta in range(1, min(pCol + 1, 8 - pRow)):
        new_pCol = pCol - delta
        new_pRow = pRow + delta
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            print(f"Trying to access board[{new_pCol}][{new_pRow}]")
            if meet_pieces(board[new_pCol], new_pRow):
                # print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
                newboard = board.copy()
                result = eat_pieces(board[new_pCol], new_pRow, piece)     
                if newboard[new_pCol] == result:
                    break
                newboard[new_pCol] = result    
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                result = '/'.join(newboard)
                print(result)
                moves.append(result)
                break
            else:
                # print("The new update: " + update_board_with_fen(board[new_pCol], new_pRow, piece))
                newboard = board.copy()
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                newboard[new_pCol] = update_board_with_fen(board[new_pCol], new_pRow, piece)         
                result = '/'.join(newboard)
                print(result)
                moves.append(result) 

    # Check diagonal squares down-left
    for delta in range(1, min(pCol + 1, pRow + 1)):
        new_pCol = pCol - delta
        new_pRow = pRow - delta
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            print(f"Trying to access board[{new_pCol}][{new_pRow}]")
            if meet_pieces(board[new_pCol], new_pRow):
                # print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
                newboard = board.copy()
                result = eat_pieces(board[new_pCol], new_pRow, piece) 
                if newboard[new_pCol] == result:
                    break
                newboard[new_pCol] = result       
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                result = '/'.join(newboard)
                print(result)
                moves.append(result)
                break
            else:
                # print("The new update: " + update_board_with_fen(board[new_pCol], new_pRow, piece))
                newboard = board.copy()
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                newboard[new_pCol] = update_board_with_fen(board[new_pCol], new_pRow, piece)         
                result = '/'.join(newboard)
                print(result)
                moves.append(result)

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
            if meet_pieces(board[new_pCol], new_pRow):
                
                # print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
                newboard = board.copy()
                result = eat_pieces(board[new_pCol], new_pRow, piece)
                if newboard[new_pCol] == result:
                    continue
                newboard[new_pCol] = result  
                newboard[pCol] =  update_old_fen(board[pCol], pRow)    
                result = '/'.join(newboard)
                print(result)
                moves.append(result)  

            else:
                # print("The new update: " + update_board_with_fen(board[new_pCol], new_pRow, piece))
                newboard = board.copy()
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                if new_pCol == pCol:
                    newboard[new_pCol] = update_board_with_fen(newboard[pCol], new_pRow, piece)
                else:
                    newboard[new_pCol] = update_board_with_fen(board[new_pCol], new_pRow, piece)         
                result = '/'.join(newboard)
                print(result)   
                moves.append(result)
    return moves

def move_n(board, pCol, pRow, piece):
    moves = []
    offsets = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    for offset in offsets:
        new_pCol = pCol + offset[0]
        new_pRow = pRow + offset[1]
        print(f"Trying to access board[{new_pCol}][{new_pRow}]")
        if 0 <= new_pCol < 8 and 0 <= new_pRow < 8:
            if meet_pieces(board[new_pCol], new_pRow):
                # print("The old update: " + update_old_fen(board[pCol], pRow))
                # print("The new update: " + eat_pieces(board[new_pCol], new_pRow, piece))
                newboard = board.copy()
                result = eat_pieces(board[new_pCol], new_pRow, piece)    
                if newboard[new_pCol] == result:
                    continue
                newboard[new_pCol] = result
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                result = '/'.join(newboard)
                print(result)
                moves.append(result)                       
            else:
                # print("The old update: " + update_old_fen(board[pCol], pRow))
                # print("The new update: " + update_board_with_fen(board[new_pCol], new_pRow, piece))
                newboard = board.copy()
                newboard[new_pCol] = update_board_with_fen(board[new_pCol], new_pRow, piece)      
                newboard[pCol] =  update_old_fen(board[pCol], pRow)
                result = '/'.join(newboard)
                print(result)
                moves.append(result)                                                 
    return moves




def generate_legal_moves(fen):
    board, turn, _, _, _, _ = parse_fen(fen)
    all_moves = []  # Initialize an empty list to collect all moves
    for pCol, row in enumerate(board):
        rowTemp = 0
        for pRow, piece in enumerate(row):
            if piece.isdigit():
                rowTemp += int(piece)
            elif (turn == 'w' and piece.isupper()) or (turn == 'b' and piece.islower()):
                if piece.lower() == 'k':
                    print(f"Vua found at {pCol}, {rowTemp}")  
                    all_moves.extend(move_k(board, pCol, rowTemp, piece))
                elif piece.lower() == 'n':
                    print(f"Mã found at {pCol}, {rowTemp}")  
                    all_moves.extend(move_n(board, pCol, rowTemp, piece))
                elif piece.lower() == 'p':  
                    if piece == 'p':
                        print(f"Tốt đen found at {pCol}, {rowTemp}")
                        all_moves.extend(move_p(board, pCol, rowTemp, piece))
                    else:
                        print(f"Tốt Trắng found at {pCol}, {rowTemp}")
                        all_moves.extend(move_P(board, pCol, rowTemp, piece))
                elif piece.lower() == 'r':
                    print(f"Xe found at {pCol}, {rowTemp}")  
                    all_moves.extend(move_r(board, pCol, rowTemp, piece))
                elif piece.lower() == 'b':
                    print(f"Tượng found at {pCol}, {rowTemp}")  
                    all_moves.extend(move_b(board, pCol, rowTemp, piece))
                elif piece.lower() == 'q':
                    print(f"Hậu found at {pCol}, {rowTemp}")  
                    all_moves.extend(move_q(board, pCol, rowTemp, piece))
                rowTemp += 1
            else:
                rowTemp += 1
    return all_moves
fen = "1n6/1p1k1ppr/rP6/p1p1PN2/R3pNRb/1QP5/5P2/4K3 w - - 0 24"
all_moves = generate_legal_moves(fen)

# print(all_moves)
def compare_fen_lists(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    in_list1_not_list2 = set1 - set2
    in_list2_not_list1 = set2 - set1

    return in_list1_not_list2, in_list2_not_list1



def read_file_and_get_first_part(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    expected = [line.split(' ')[0] for line in lines]
    return expected

# Usage
expected = read_file_and_get_first_part('text.txt')

print(compare_fen_lists(expected, all_moves))