"""
This module serves as the entry point to the PDF Summarizer APP.
"""

from src.Modern_GUI2 import GUI
import customtkinter

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = GUI()
    app.mainloop()