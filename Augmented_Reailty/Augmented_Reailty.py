from Augmented_Reailty.show_words_on_chessboard import Show_Words_On_Chessboard
from Corner_Detection.Camera_Calibration import Camera_Calibration
import os

class Augmented_Reailty:
    def __init__(self):
        offset = [[7, 5, 0], [4, 5, 0], [1, 5, 0], [7, 2, 0], [4, 2, 0], [1, 2, 0]]

        db_onboard = os.path.join(os.getcwd(), "dataset/Q2_Image/Q2_db/alphabet_db_onboard.txt") 
        self.Show_Words_On_Board = Show_Words_On_Chessboard(db_onboard, offset)

        db_vertical = os.path.join(os.getcwd(), "dataset/Q2_Image/Q2_db/alphabet_db_vertical.txt")
        self.Show_Words_Vertical = Show_Words_On_Chessboard(db_vertical, offset)
        pass

    def show_words_on_board(self, parent_widget, text, Camera_Calibration:Camera_Calibration):
        self.Show_Words_On_Board.show_words_on_chessboard(parent_widget, text, Camera_Calibration)

    def show_words_vertical(self, parent_widget, text, Camera_Calibration:Camera_Calibration):
        self.Show_Words_Vertical.show_words_on_chessboard(parent_widget, text, Camera_Calibration)