import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import pandas as pd
from data_description import DataDescription
from sklearn.preprocessing import MinMaxScaler, StandardScaler

class FeatureScaling:
    bold_start = "\033[1m"
    bold_end = "\033[0;0m"

    tasks = [
        'Perform Normalization (MinMax Scaler)',
        'Perform Standardization (Standard Scaler)',
        'Show The Dataset'
        
    ]

    tasks_normalization = [
        'Normalize a specific Column',
        'Normalize the whole Dataset',
        
    ]

    tasks_standardization = [
        'Standardize a specific Column',
        'Standardize the whole Dataset',
        
    ]

    def __init__(self, data):
        self.data = data

    def normalization(self):
        def normalize_column():
            column = simpledialog.askstring("Normalize Column", "Enter column name to normalize (Press -1 to go back):")
            if column == "-1":
                return
            try:
                self.data[column] = (self.data[column] - self.data[column].min()) / (self.data[column].max() - self.data[column].min())
                messagebox.showinfo("Success", "Column normalized successfully!")
            except KeyError:
                messagebox.showerror("Error", "Column not found!")

        def normalize_dataset():
            try:
                self.data = pd.DataFrame(MinMaxScaler().fit_transform(self.data))
                messagebox.showinfo("Success", "Dataset normalized successfully!")
            except ValueError:
                messagebox.showerror("Error", "Normalization failed! Make sure the data contains only numerical values.")

        tasks = [
            normalize_column,
            normalize_dataset,
            lambda: DataDescription(self.data).show_dataset()
        ]

        while True:
            choice = simpledialog.askinteger("Normalization Tasks", "\n".join([
                f"{idx}. {task}" for idx, task in enumerate(self.tasks_normalization, start=1)
            ]) + "\nEnter your choice (Press -1 to exit):")

            if choice is None or choice == -1:
                break

            task = tasks[choice - 1]
            task()

    def standardization(self):
        def standardize_column():
            column = simpledialog.askstring("Standardize Column", "Enter column name to standardize (Press -1 to go back):")
            if column == "-1":
                return
            try:
                self.data[column] = (self.data[column] - self.data[column].mean()) / self.data[column].std()
                messagebox.showinfo("Success", "Column standardized successfully!")
            except KeyError:
                messagebox.showerror("Error", "Column not found!")

        def standardize_dataset():
            try:
                self.data = pd.DataFrame(StandardScaler().fit_transform(self.data))
                messagebox.showinfo("Success", "Dataset standardized successfully!")
            except ValueError:
                messagebox.showerror("Error", "Standardization failed! Make sure the data contains only numerical values.")

        tasks = [
            standardize_column,
            standardize_dataset,
            lambda: DataDescription(self.data).show_dataset()
        ]

        while True:
            choice = simpledialog.askinteger("Standardization Tasks", "\n".join([
                f"{idx}. {task}" for idx, task in enumerate(self.tasks_standardization, start=1)
            ]) + "\nEnter your choice (Press -1 to exit):")

            if choice is None or choice == -1:
                break

            task = tasks[choice - 1]
            task()


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
            choice = simpledialog.askinteger("Feature Scaling Tasks", "\n".join([
                f"{idx}. {task}" for idx, task in enumerate(self.tasks, start=1)
            ]) + "\nEnter your choice (Press -1 to exit):")

            if choice is None or choice == -1:
                break

            if choice == 1:
                self.normalization()
            elif choice == 2:
                self.standardization()

            elif choice == 3:
                self.show_dataset()
            
            else:
                messagebox.showerror("Error", "Invalid choice!")

        return self.data
