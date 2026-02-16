import tkinter as tk
from tkinter import ttk, messagebox
from db import insert_record, fetch_all, delete_record, search_record, filter_records
from models import calculate_bmi


class HealthApp:
    def __init__(self, root):
        self.root = root
        root.title("Student Health Record Management System")
        root.geometry("1200x700")
        root.configure(bg="#ECEFF1")

        style = ttk.Style()
        style.theme_use("clam")

        self.sidebar_color = "#263238"
        self.header_color = "#37474F"
        self.accent_color = "#1565C0"
        self.bg_color = "#ECEFF1"

        header = tk.Frame(root, bg=self.header_color, height=60)
        header.pack(side="top", fill="x")

        tk.Label(
            header,
            text="Student Health Record Management System",
            bg=self.header_color,
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15)

        main_frame = tk.Frame(root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)

        sidebar = tk.Frame(main_frame, bg=self.sidebar_color, width=220)
        sidebar.pack(side="left", fill="y")

        content = tk.Frame(main_frame, bg=self.bg_color)
        content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        def sidebar_button(text, command):
            return tk.Button(
                sidebar,
                text=text,
                command=command,
                bg=self.sidebar_color,
                fg="white",
                activebackground=self.accent_color,
                activeforeground="white",
                bd=0,
                font=("Segoe UI", 11),
                pady=12
            )

        sidebar_button("Add Record", self.add_record_window).pack(fill="x")
        sidebar_button("View All Records", self.view_records).pack(fill="x")
        sidebar_button("Search Record", self.search_record_window).pack(fill="x")
        sidebar_button("Delete Record", self.delete_record_window).pack(fill="x")
        sidebar_button("Filter by Class/Section", self.filter_window).pack(fill="x")
        sidebar_button("Exit", root.destroy).pack(fill="x")

        columns = ("ID", "Name", "Surname", "Age", "Gender", "Blood", "Class", "Section")

        self.tree = ttk.Treeview(content, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(fill="both", expand=True)

    # ---------------- VIEW ----------------
    def view_records(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        records = fetch_all()

        for record in records:
            self.tree.insert("", "end", values=record)

    # ---------------- ADD ----------------
    def add_record_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Student Record")
        win.geometry("600x650")
        win.configure(bg="#ECEFF1")

        form_frame = tk.Frame(win, bg="#ECEFF1")
        form_frame.pack(pady=20)

        fields = [
            "Name", "Surname", "Age", "Gender",
            "Blood Type", "Class", "Section",
            "Height(cm)", "Weight(kg)",
            "Blood Pressure", "DOB(YYYY-MM-DD)",
            "Right Eye", "Left Eye"
        ]

        entries = {}

        for i, field in enumerate(fields):
            label = tk.Label(form_frame, text=field, bg="#ECEFF1", font=("Segoe UI", 10))
            label.grid(row=i, column=0, sticky="w", padx=15, pady=6)

            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=15, pady=6)

            entries[field] = entry

        def submit():
            try:
                height = float(entries["Height(cm)"].get())
                weight = float(entries["Weight(kg)"].get())
                bmi = calculate_bmi(height, weight)

                record = {
                    'Name': entries["Name"].get(),
                    'Surname': entries["Surname"].get(),
                    'Age': int(entries["Age"].get()),
                    'Gender': entries["Gender"].get(),
                    'BloodType': entries["Blood Type"].get(),
                    'Class': entries["Class"].get(),
                    'Section': entries["Section"].get(),
                    'Height': height,
                    'Weight': weight,
                    'BMI': bmi,
                    'BloodPressure': entries["Blood Pressure"].get(),
                    'DOB': entries["DOB(YYYY-MM-DD)"].get(),
                    'RightEye': entries["Right Eye"].get(),
                    'LeftEye': entries["Left Eye"].get(),
                }

                insert_record(record)
                messagebox.showinfo("Success", "Record added successfully")
                win.destroy()
                self.view_records()

            except ValueError:
                messagebox.showerror("Error", "Age, Height and Weight must be numbers.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Submit", command=submit).pack(pady=20)

    # ---------------- SEARCH ----------------
    def search_record_window(self):
        win = tk.Toplevel(self.root)
        win.title("Search Record")

        ttk.Label(win, text="Enter Name").pack(pady=5)
        name_entry = ttk.Entry(win)
        name_entry.pack(pady=5)

        def search():
            for row in self.tree.get_children():
                self.tree.delete(row)

            record = search_record(name_entry.get())

            if record:
                self.tree.insert("", "end", values=record)
            else:
                messagebox.showinfo("Not Found", "Record not found")

            win.destroy()

        ttk.Button(win, text="Search", command=search).pack(pady=10)

    # ---------------- DELETE ----------------
    def delete_record_window(self):
        win = tk.Toplevel(self.root)
        win.title("Delete Record")

        ttk.Label(win, text="Enter Name to Delete").pack(pady=5)
        name_entry = ttk.Entry(win)
        name_entry.pack(pady=5)

        def delete():
            delete_record(name_entry.get())
            messagebox.showinfo("Deleted", "Record deleted successfully")
            win.destroy()
            self.view_records()

        ttk.Button(win, text="Delete", command=delete).pack(pady=10)

    # ---------------- FILTER ----------------
    def filter_window(self):
        win = tk.Toplevel(self.root)
        win.title("Filter Records")

        ttk.Label(win, text="Class").pack(pady=5)
        class_entry = ttk.Entry(win)
        class_entry.pack(pady=5)

        ttk.Label(win, text="Section").pack(pady=5)
        section_entry = ttk.Entry(win)
        section_entry.pack(pady=5)

        def filter_records_btn():
            for row in self.tree.get_children():
                self.tree.delete(row)

            records = filter_records(class_entry.get(), section_entry.get())

            for record in records:
                self.tree.insert("", "end", values=record)

            win.destroy()

        ttk.Button(win, text="Filter", command=filter_records_btn).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = HealthApp(root)
    root.mainloop()
