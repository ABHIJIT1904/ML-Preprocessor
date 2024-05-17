import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd

class Download:
    

    def __init__(self, data):
        self.data = data

    def execute(self):
        toBeDownload = {}
        for column in self.data.columns.values:
            toBeDownload[column] = self.data[column]

        newFileName = simpledialog.askstring("Enter the FILENAME in which you want to store your dataset ", "")
        if newFileName=="-1":
            return
        newFileName = newFileName + ".csv"
        # index=False as this will not add an extra column of index.
        pd.DataFrame(self.data).to_csv(newFileName, index = False)

        
        
        messagebox.showinfo("Done\U0001F601" "\n")
        
        if simpledialog.askstring("Do you want to exit now? (yes/n) ", "").lower() == 'yes':
            messagebox.showinfo("Exiting...\U0001F44B" "\n")
            exit()
        else:
            return
