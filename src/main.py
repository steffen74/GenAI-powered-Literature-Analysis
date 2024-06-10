"""
This module serves as the entry point to the PDF Summarizer APP.
"""

import argparse
from src.Modern_GUI2 import GUI
import customtkinter

def main():
    parser = argparse.ArgumentParser(description='Start the application in kiosk mode.')
    parser.add_argument('--kiosk', action='store_true', help='Start in kiosk mode')

    args = parser.parse_args()

    customtkinter.set_appearance_mode("dark")
    app = GUI(kiosk=args.kiosk)
    app.mainloop()

if __name__ == "__main__":
    main()