import tkinter as tk
from tkinter import ttk, messagebox
import os, sys

# ---------------- File Storage ----------------
FILE = "stocks.txt"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------------- Functions ----------------
def load_data():
    items = []
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    name, category, qty = parts
                    items.append((name, category, qty))
    return items

def save_data():
    with open(FILE, "w", encoding="utf-8") as f:
        for item in tree.get_children():
            vals = tree.item(item, "values")
            f.write("|".join(vals) + "\n")

def add_item():
    name = entry_name.get().strip()
    category = combo_category.get().strip()
    qty = entry_qty.get().strip()

    if not name or not qty:
        messagebox.showwarning("Missing Info", "Please enter Item Name and Quantity.")
        return

    try:
        qty_int = int(qty)
    except:
        messagebox.showerror("Invalid Input", "Quantity must be a number.")
        return

    tree.insert("", "end", values=(name, category, qty))
    save_data()
    clear_fields()
    check_low_stock()
    messagebox.showinfo("Added", f"{name} added successfully!")

def delete_item():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select an item to delete.")
        return
    for s in selected:
        tree.delete(s)
    save_data()
    messagebox.showinfo("Deleted", "Selected item(s) deleted successfully.")

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_qty.delete(0, tk.END)
    combo_category.set("")

def on_item_select(event):
    selected = tree.selection()
    if selected:
        vals = tree.item(selected[0], "values")
        entry_name.delete(0, tk.END)
        entry_name.insert(0, vals[0])
        combo_category.set(vals[1])
        entry_qty.delete(0, tk.END)
        entry_qty.insert(0, vals[2])

def update_item():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "Select an item to update.")
        return

    name = entry_name.get().strip()
    category = combo_category.get().strip()
    qty = entry_qty.get().strip()

    if not name or not qty:
        messagebox.showwarning("Missing Info", "Please enter Item Name and Quantity.")
        return

    try:
        int(qty)
    except:
        messagebox.showerror("Invalid Input", "Quantity must be a number.")
        return

    tree.item(selected[0], values=(name, category, qty))
    save_data()
    clear_fields()
    check_low_stock()
    messagebox.showinfo("Updated", f"{name} updated successfully!")

def check_low_stock():
    for item in tree.get_children():
        vals = tree.item(item, "values")
        qty = int(vals[2])
        if qty < 5:
            tree.item(item, tags=("low",))
        else:
            tree.item(item, tags=("normal",))

def show_low_stock_alert():
    low_items = []
    for item in tree.get_children():
        vals = tree.item(item, "values")
        name, qty = vals[0], int(vals[2])
        if qty < 5:
            low_items.append(f"{name} ({qty})")

    if low_items:
        messagebox.showwarning(
            "Low Stock Alert 🚨",
            "Mababa na ang stock ng mga sumusunod:\n\n" + "\n".join(low_items)
        )

def filter_category(event=None):
    selected_cat = combo_filter.get()
    for item in tree.get_children():
        tree.delete(item)
    for (name, cat, qty) in load_data():
        if selected_cat == "All" or selected_cat == cat:
            tree.insert("", "end", values=(name, cat, qty))
    check_low_stock()

# ------------------------- ANALYTICS -------------------------
def open_analytics():
    data = load_data()

    if not data:
        messagebox.showinfo("Analytics", "No data available.")
        return

    # --- Calculations ---
    total_items = len(data)
    total_qty = sum(int(qty) for _, _, qty in data)
    low_stock = len([x for x in data if int(x[2]) < 5])

    # Items per category
    categories = {}
    for _, cat, qty in data:
        categories[cat] = categories.get(cat, 0) + 1

    # Stock statistics
    quantities = [int(qty) for _, _, qty in data]
    highest = max(quantities)
    lowest = min(quantities)
    average = total_qty / total_items if total_items > 0 else 0

    # --- Analytics Window ---
    win = tk.Toplevel(root)
    win.title("📊 Stock Analytics")
    win.geometry("350x500")
    win.config(bg="#d8ecff")
    win.iconbitmap(resource_path("pic.ico"))

    tk.Label(win, text="📊 STOCK ANALYTICS",
             font=("Segoe UI", 16, "bold"),
             bg="#d8ecff", fg="#1a1a1a").pack(pady=10)

    tk.Label(win, text=f"Total Item Types: {total_items}",
             font=("Segoe UI", 12), bg="#d8ecff").pack(anchor="w", padx=20)
    tk.Label(win, text=f"Total Quantity: {total_qty}",
             font=("Segoe UI", 12), bg="#d8ecff").pack(anchor="w", padx=20)
    tk.Label(win, text=f"Low-stock Items (<5): {low_stock}",
             font=("Segoe UI", 12), bg="#d8ecff").pack(anchor="w", padx=20, pady=5)

    tk.Label(win, text=f"Highest Stock: {highest}",
             font=("Segoe UI", 12), bg="#d8ecff").pack(anchor="w", padx=20)
    tk.Label(win, text=f"Lowest Stock: {lowest}",
             font=("Segoe UI", 12), bg="#d8ecff").pack(anchor="w", padx=20)
    tk.Label(win, text=f"Average Stock: {average:.1f}",
             font=("Segoe UI", 12), bg="#d8ecff").pack(anchor="w", padx=20, pady=10)

    tk.Label(win, text="Items per Category:",
             font=("Segoe UI", 14, "bold"), bg="#d8ecff").pack(anchor="w", padx=20, pady=5)

    for cat, count in categories.items():
        tk.Label(win, text=f"• {cat}: {count}",
                 font=("Segoe UI", 12), bg="#d8ecff").pack(anchor="w", padx=35)


# ---------------- GUI ----------------
root = tk.Tk()
root.title("StockManager")
root.geometry("850x550")
root.config(bg="#d8ecff")  # 💙 Light Blue background
root.resizable(True, True)
root.iconbitmap(resource_path("pic.ico"))

# Title Label
tk.Label(root, text="🧾 StockManager+", font=("Segoe UI", 22, "bold"), bg="#d8ecff", fg="#1a1a1a").pack(pady=10)

# Input Frame
frame_inputs = tk.Frame(root, bg="#d8ecff")
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Item Name:", bg="#d8ecff", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=3)
entry_name = tk.Entry(frame_inputs, width=25)
entry_name.grid(row=0, column=1, padx=10)

tk.Label(frame_inputs, text="Category:", bg="#d8ecff", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=3)
combo_category = ttk.Combobox(frame_inputs, values=["Drinks", "Snacks", "Dairy", "Others"], width=22)
combo_category.grid(row=1, column=1, padx=10)

tk.Label(frame_inputs, text="Quantity:", bg="#d8ecff", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, sticky="w", padx=5)
entry_qty = tk.Entry(frame_inputs, width=25)
entry_qty.grid(row=1, column=3, padx=10)

# Buttons Frame
frame_btns = tk.Frame(root, bg="#d8ecff")
frame_btns.pack(pady=5)

btn_add = tk.Button(frame_btns, text="Add Item", command=add_item, bg="#4caf50", fg="white", width=12)
btn_add.grid(row=0, column=0, padx=5)

btn_update = tk.Button(frame_btns, text="Update", command=update_item, bg="#2196f3", fg="white", width=12)
btn_update.grid(row=0, column=1, padx=5)

btn_delete = tk.Button(frame_btns, text="Delete", command=delete_item, bg="#f44336", fg="white", width=12)
btn_delete.grid(row=0, column=2, padx=5)

btn_clear = tk.Button(frame_btns, text="Clear", command=clear_fields, bg="#9e9e9e", fg="white", width=12)
btn_clear.grid(row=0, column=3, padx=5)

# ⭐ NEW ANALYTICS BUTTON
btn_analytics = tk.Button(frame_btns, text="Analytics", command=open_analytics,
                          bg="#673ab7", fg="white", width=12)
btn_analytics.grid(row=0, column=4, padx=5)

# Filter Frame
frame_filter = tk.Frame(root, bg="#d8ecff")
frame_filter.pack(pady=5)
tk.Label(frame_filter, text="Filter by Category:", bg="#d8ecff", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
combo_filter = ttk.Combobox(frame_filter, values=["All", "Drinks", "Snacks", "Dairy", "Others"], width=20)
combo_filter.current(0)
combo_filter.pack(side="left")
combo_filter.bind("<<ComboboxSelected>>", filter_category)

# Table
columns = ("Item Name", "Category", "Quantity")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)
tree.pack(pady=10, fill="x", padx=20)

# Style for low-stock items
tree.tag_configure("low", background="#ffdddd", foreground="red")
tree.tag_configure("normal", background="white", foreground="black")

tree.bind("<<TreeviewSelect>>", on_item_select)

# Load existing data
for (name, cat, qty) in load_data():
    tree.insert("", "end", values=(name, cat, qty))
check_low_stock()

# 🔔 Auto-check low stock when app starts
root.after(200, show_low_stock_alert)

root.mainloop()
