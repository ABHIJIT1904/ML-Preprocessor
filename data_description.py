import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox ,ttk

class DataDescription:
   
    tasks = [
        'Describe a specific Column',
        'Show Properties of Each Column',
        'Show the Dataset'
    ]

    def __init__(self, data):
        self.data = data


    def show_dataset(self):
        
        rows = simpledialog.askinteger("Number of Rows", "Enter the number of rows to print:")
        if rows is None or rows <= 0:
            return

        # Create a new window for displaying the dataset
        dataset_window = tk.Toplevel()
        dataset_window.title("Dataset")
        dataset_window.geometry("1500x600")

        # Create a Treeview widget
        tree = ttk.Treeview(dataset_window)

        tree["columns"] = list(self.data.columns)
        for column in self.data.columns:
            tree.heading(column, text=column)
            tree.column(column, width=100)

        for i, row in self.data.head(rows).iterrows():
            tree.insert("", tk.END, values=list(row))

        scrollbar = ttk.Scrollbar(dataset_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        horizontal_scrollbar = ttk.Scrollbar(dataset_window, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=horizontal_scrollbar.set)
        horizontal_scrollbar.pack(side="bottom", fill="x")

        tree.pack(expand=True, fill="both")



    def showColumns(self):
        column_info = "\n".join(self.data.columns)
        messagebox.showinfo("Columns", column_info)
        


    def show_properties(self):
        properties_window = tk.Toplevel()
        properties_window.title("Properties")
        properties_window.geometry("1000x800")
        tree = ttk.Treeview(properties_window)
        tree["columns"] = ("Property", "Value")
        tree.heading("Property", text="Property")
        tree.heading("Value", text="Value")
        tree.column("#0", width=200)
        tree.column("Property", width=200)
        tree.column("Value", width=200)

        describe_properties = self.data.describe().reset_index().values
        for row in describe_properties:
            tree.insert("", tk.END, values=("describe " + row[0], row[1]))

        info_properties = self.data.info()
        tree.insert("", tk.END, values=("info", info_properties))

        scrollbar = ttk.Scrollbar(properties_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(expand=True, fill="both")
                
        
    def execute(self):
        while True:
            choice = simpledialog.askinteger("Data Description Task", "\n".join([
                f"{idx}. {task}" for idx, task in enumerate(self.tasks, start=1)
            ]) + "\nEnter your choice (Press -1 to exit):")

            if choice is None or choice == -1:
                break

            if choice == 1:
                self.showColumns()
            elif choice == 2:
                self.show_properties()
            elif choice == 3:
                self.show_dataset()
            else:
                messagebox.showerror("Error", "Invalid choice!")

        return self.data
    

