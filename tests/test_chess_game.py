import pytest
import chess
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from ChessGame import ChessGame

class TestChessGame:
    def test_board_initialization(self):
        """Test that the chess board initializes correctly"""
        cg = ChessGame()
        assert cg._ChessGame__board is not None
        assert isinstance(cg._ChessGame__board, chess.Board)
        assert cg._ChessGame__board.is_valid()
        
    def test_square_inversion(self):
        """Test square inversion method"""
        cg = ChessGame()
        # Test a few squares
        assert cg._ChessGame__invert_position("a1") == "a8"
        assert cg._ChessGame__invert_position("h8") == "h1"
        
    def test_piece_values(self):
        """Test piece values dictionary"""
        cg = ChessGame()
        expected_values = {
            'p': 1, 'P': -1,
            'n': 3, 'N': -3,
            'b': 3, 'B': -3,
            'r': 5, 'R': -5,
            'q': 9, 'Q': -9,
            'k': 999, 'K': -999
        }
        assert cg._ChessGame__pieces_values == expected_values

    @pytest.mark.skipif(not os.path.exists('/opt/homebrew/bin/stockfish'), 
                        reason="Stockfish not installed")
    def test_engine_connection(self):
        """Test Stockfish engine connection"""
        cg = ChessGame()
        try:
            # Try to get engine info
            info = cg._ChessGame__engine.id
            assert info["name"] == "Stockfish"
        finally:
            cg._ChessGame__engine.quit()

if __name__ == "__main__":
    pytest.main()