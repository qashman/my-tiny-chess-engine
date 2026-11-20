# main.py - Compact Chess Agent for make.fun tiny-chess-01
# Uses Kaggle chess format: observation.board (64 ints), observation.legal_moves (UCI strings)

def agent(observation, configuration):
    moves = observation.legal_moves
    if not moves:
        return None

    # Piece values: P=10, N=30, B=30, R=50, Q=90, K=0. Black is negative.
    # 1-6 = White P,N,B,R,Q,K. 8-13 = Black p,n,b,r,q,k.
    values = {1: 10, 2: 30, 3: 30, 4: 50, 5: 90, 6: 0, 8: -10, 9: -30, 10: -30, 11: -50, 12: -90, 13: 0}
    
    # Simplified piece-square table for knights and pawns (white perspective, mirrored for black)
    pst = [
         0,  0,  0,  0,  0,  0,  0,  0,
         5, 10, 10, -20, -20, 10, 10,  5,
         5, -5, -10,   0,   0, -10, -5,  5,
         0,  0,  0,  20,  20,   0,  0,  0,
         5,  5, 10,  25,  25,  10,  5,  5,
        10, 10, 20,  30,  30,  20, 10, 10,
        50, 50, 50,  50,  50,  50, 50, 50,
         0,  0,  0,  0,  0,  0,  0,  0
    ]

    def evaluate(board):
        score = 0
        for i, p in enumerate(board):
            if p in values:
                score += values[p]
                # Add positional bonus for knights (2) and pawns (1, 8)
                if p in (2, 9):
                    idx = i if p == 2 else 63 - i
                    score += (5 if pst[idx] > 0 else 0)
        return score if observation.mark == 1 else -score

    def apply_move(board, move):
        new_board = list(board)
        src = (int(move[1]) - 1) * 8 + (ord(move[0]) - 97)
        dst = (int(move[3]) - 1) * 8 + (ord(move[2]) - 97)
        piece = new_board[src]
        new_board[dst] = piece
        new_board[src] = 0
        # Simplified promotion: always promote to Queen
        if piece == 1 and dst >= 56: new_board[dst] = 5
        if piece == 8 and dst <= 7:  new_board[dst] = 12
        return new_board

    best_move = moves[0]
    best_score = -999999

    # Sort moves to check captures first (improves alpha-beta if we add it later)
    def capture_value(m):
        dst = (int(m[3]) - 1) * 8 + (ord(m[2]) - 97)
        return values.get(observation.board[dst], 0)
    
    sorted_moves = sorted(moves, key=capture_value, reverse=True)

    for move in sorted_moves:
        sim_board = apply_move(observation.board, move)
        score = evaluate(sim_board)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move "This is a starter chess engine for the make.fun tiny-chess-01 bounty. It uses a 1-ply greedy search. Please upgrade it to a 2-ply alpha-beta search with quiescence search for captures. Keep it under 4096 bytes. Use only the Python standard library."