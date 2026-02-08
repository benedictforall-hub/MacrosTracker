from fatsecret_api import search_food, get_food_details
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.configure(bg='lightgrey')
root.title("Food Macros Tracker via fatsecret API")
root.geometry("430x650")

# Title
label = tk.Label(
    root,
    text="Calorie & Macro Tracker",
    font=("Arial", 16),
    bg="lightgrey",
)
label.pack(pady=10)

# Search Box
search_frame = tk.Frame(root, bg="lightgrey")
search_frame.pack(pady=5) 
search_frame.place(x=50, y=55)

tk.Label(search_frame, text="Food Name:", bg="lightgrey").pack(side=tk.LEFT)

search_entry = tk.Entry(root, width=20, bg="white")
search_entry.pack(pady=5)
search_entry.place(x=127, y=55)

# Results List
results_listbox = tk.Listbox(root, width=54, height=20, bg="white")
results_listbox.pack(pady=10)
results_listbox.place(x=50, y=120)

# Details Output
details_text = tk.Text(root, width=41, height=8, bg="white")
details_text.pack(pady=10)
details_text.place(x=50, y=460)

# Quantity Input
qty_frame = tk.Frame(root, bg="lightgrey")
qty_frame.pack(pady=5) 
qty_frame.place(x=50, y=80)

tk.Label(qty_frame, text="Quantity:", bg="lightgrey").pack(side=tk.LEFT)

quantity_entry = tk.Entry(qty_frame, width=8, bg="white")
quantity_entry.pack(side=tk.LEFT, padx=5)

unit_var = tk.StringVar(value="serving")
unit_menu = tk.OptionMenu(qty_frame, unit_var, "serving", "grams")
unit_menu.pack(side=tk.LEFT, anchor="w")
unit_menu.place

foods_cache = []  # store API results so we can reference food_id later
max_results = 50

def on_search():
    global foods_cache
    query = search_entry.get().strip()

    results_listbox.delete(0, tk.END)
    details_text.delete("1.0", tk.END)

    if not query:
        messagebox.showwarning("Input Error", "Please enter a food name.")
        return

    foods_cache = search_food(query)

    if not foods_cache:
        results_listbox.insert(tk.END, "No results found.")
        return

    # Remove duplicates based on food name (case-insensitive)
    seen_foods = set()

    for food in foods_cache:
        name = food['food_name'].lower()
        if name in seen_foods:
            continue
        seen_foods.add(name)

        results_listbox.insert(
            tk.END,
            f"{"▢ " + food['food_name']}"
        )
#({food.get('food_description', '')})

def on_show_details():
    selection = results_listbox.curselection()

    if not selection:
        messagebox.showwarning("Selection Error", "Please select a food.")
        return

    try:
        qty = float(quantity_entry.get())
        if qty <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Quantity Error", "Enter a valid quantity.")
        return

    unit = unit_var.get()
    index = selection[0]
    food_id = foods_cache[index]['food_id']

    details = get_food_details(food_id)

    servings = details['servings']['serving']
    serving = servings[0] if isinstance(servings, list) else servings

    # Base values (per serving)
    calories = float(serving.get('calories', 0))
    carbs = float(serving.get('carbohydrate', 0))
    protein = float(serving.get('protein', 0))
    fat = float(serving.get('fat', 0))

    multiplier = 1.0

    if unit == "serving":
        multiplier = qty

    elif unit == "grams":
        grams_per_serving = float(serving.get('metric_serving_amount', 0))
        if grams_per_serving <= 0:
            messagebox.showerror("Data Error", "Gram data not available.")
            return
        multiplier = qty / grams_per_serving

    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END, f"Name: {details['food_name']}\n")
    details_text.insert(tk.END, f"Quantity: {qty} {unit}\n\n")
    details_text.insert(tk.END, f"Calories: {calories * multiplier:.2f}\n")
    details_text.insert(tk.END, f"Carbs: {carbs * multiplier:.2f} g\n")
    details_text.insert(tk.END, f"Protein: {protein * multiplier:.2f} g\n")
    details_text.insert(tk.END, f"Fat: {fat * multiplier:.2f} g\n")

# Buttons
btn_frame = tk.Frame(root, bg="lightgrey")
btn_frame.pack(pady=5)
btn_frame.place(x=260, y=50)

search_btn = tk.Button(
    btn_frame,
    text="Search Food",
    command=on_search,
    bg="lightblue",
    width=15
)
search_btn.pack(side=tk.LEFT, padx=5)

btn_frame2 = tk.Frame(root, bg="lightgrey")
btn_frame2.pack(pady=5)
btn_frame2.place(x=260, y=80)

details_btn = tk.Button(
    btn_frame2,
    text="Show Details",
    command=on_show_details,
    bg="lightgreen",
    width=15
)
details_btn.pack(side=tk.LEFT, padx=5)


root.mainloop()
