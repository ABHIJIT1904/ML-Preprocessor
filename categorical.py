import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from data_description import DataDescription

class Categorical:
    tasks = [
        'Show Categorical Columns',
        'Perform One Hot encoding',
        'Show Dataset'
        
    ]

    def __init__(self, data):
        self.data = data

    def show_categorical_columns(self):
        categorical_columns = self.data.select_dtypes(include="object")
        messagebox.showinfo("Categorical Columns", f"Categorical Columns:\n{', '.join(categorical_columns)}")

    def encoding(self):
        column = simpledialog.askstring("One Hot Encoding", "Enter column name to one hot encode (Press -1 to go back):")
        if column == "-1":
            return
        if column not in self.data.columns:
            messagebox.showerror("Error", "Column not found!")
            return
        if self.data[column].dtype != 'object':
            messagebox.showerror("Error", "Column is not categorical!")
            return
        
        encoded_data = pd.get_dummies(self.data[column], prefix=column)
        self.data = pd.concat([self.data, encoded_data], axis=1)
        self.data.drop(columns=[column], inplace=True)
        messagebox.showinfo("Success", "One Hot Encoding done!")

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

    def execute(self):
        while True:
            choice = simpledialog.askinteger("Categorical Tasks", "\n".join([
                f"{idx}. {task}" for idx, task in enumerate(self.tasks, start=1)
            ]) + "\nEnter your choice (Press -1 to exit):")

            if choice is None or choice == -1:
                break

            if choice == 1:
                self.show_categorical_columns()
            elif choice == 2:
                self.encoding()
            elif choice == 3:
                self.show_dataset()
            else:
                messagebox.showerror("Error", "Invalid choice!")

        return self.data
