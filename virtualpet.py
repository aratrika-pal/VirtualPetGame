from datetime import datetime
import tkinter as tk
import random

# ------------------- REPORTS -------------------
healthReport = []
expenseReport = []

# ------------------- ITEMS -------------------
toys = {"ball": 3, "frisbee": 6, "yarn": 11, "bone": 10, "toy car": 13, "toy boat": 8, "toy plane": 9, "toy train": 14, "laser pointer": 10, "toy mouse": 7}
foods = {"apple": 4, "banana": 6, "carrot": 2, "chicken": 6, "pork": 10, "steak": 15, "bread": 3, "milk": 7}
jobs = {"doctor": 100, "teacher": 80, "engineer": 120, "artist": 70, "chef": 90}

ownedToys = {}
ownedFoods = {}
balance = 1000

# ------------------- LOG FUNCTIONS -------------------
def logHealthUpdate(pet, change, reason):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # gets today's date/time
    healthReport.append({
        "timestamp": timestamp,
        "pet_name": pet["name"],
        "old_health": pet["health"] - change,
        "new_health": pet["health"],
        "change": change,
        "reason": reason
    })

def logExpense(change, reason):
    global balance
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # gets today's date/time
    expenseReport.append({
        "timestamp": timestamp,
        "old_balance": balance + change,
        "new_balance": balance,
        "change": change,
        "reason": reason
    })

# ------------------- GUI SETUP -------------------
root = tk.Tk()
root.title("Kawaii Virtual Pet 🐾")
root.geometry("720x700")
root.minsize(600, 600)

canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)

def draw_gradient(event=None):
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    for i in range(height):
        r = 255
        g = min(255, int(214 + i * 0.03))
        b = max(0, int(236 - i * 0.1))
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, width, i, fill=color)
canvas.bind("<Configure>", draw_gradient)

# ------------------- AESTHETIC POPUPS -------------------
def show_kawaii_popup(message): # used for reports, sickness, etc.
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    frame = tk.Frame(popup, bg="#ffccff", bd=5, relief="ridge")
    frame.pack(fill="both", expand=True)
    label = tk.Label(frame, text=f"✨ {message} ✨", font=("Comic Sans MS", 14, "bold"), bg="#ffccff", fg="#6b3e5e", justify="left")
    label.pack(padx=20, pady=10)
    popup.update_idletasks()
    x = root.winfo_x() + root.winfo_width()//4
    y = root.winfo_y() + root.winfo_height()//4
    popup.geometry(f"+{x}+{y}")
    alpha = 0.0
    def fade_in():
        nonlocal alpha
        alpha += 0.1
        if alpha > 1: alpha = 1
        popup.attributes("-alpha", alpha)
        if alpha < 1: popup.after(50, fade_in)
        else: popup.after(1500, fade_out)
    def fade_out():
        nonlocal alpha
        alpha -= 0.1
        if alpha < 0: alpha = 0
        popup.attributes("-alpha", alpha)
        if alpha > 0: popup.after(50, fade_out)
        else: popup.destroy()
    fade_in()

def kawaii_input(title, prompt, input_type="string", max_value=None, choices=None): # used for user input
    result = {"value": None}
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    frame = tk.Frame(popup, bg="#ffccff", bd=5, relief="ridge")
    frame.pack(fill="both", expand=True)
    label = tk.Label(frame, text=f"✨ {prompt} ✨", font=("Comic Sans MS", 14, "bold"), bg="#ffccff", fg="#6b3e5e")
    label.pack(padx=20, pady=10)
    entry = tk.Entry(frame, font=("Comic Sans MS", 12), justify="center")
    entry.pack(padx=10, pady=5)
    entry.focus()
    if choices:
        label2 = tk.Label(frame, text=f"Choices: {choices}", font=("Comic Sans MS", 12), bg="#ffccff", fg="#aa5588")
        label2.pack(pady=5)
    def submit():
        val = entry.get().strip()
        if input_type == "integer":
            try:
                val = int(val)
                if max_value is not None and val > max_value:
                    show_kawaii_popup(f"Maximum allowed is {max_value}! 😅")
                    return
            except:
                show_kawaii_popup("Please enter a valid number! 😳")
                return
        elif choices:
            if val not in choices:
                show_kawaii_popup("Please choose a valid option! 😳")
                return
        result["value"] = val
        popup.destroy()
    btn = tk.Button(frame, text="OK", command=submit, font=("Comic Sans MS", 12, "bold"),
                    bg="#ffccff", fg="#6b3e5e", activebackground="#ffb3ee", relief="flat", padx=10, pady=5)
    btn.pack(pady=10)
    popup.update_idletasks()
    x = root.winfo_x() + root.winfo_width()//4
    y = root.winfo_y() + root.winfo_height()//4
    popup.geometry(f"+{x}+{y}")
    popup.grab_set()
    root.wait_window(popup)
    return result["value"]

# ------------------- PET CREATION -------------------
name = kawaii_input("Pet Name", "Name your pet:")
ptype = kawaii_input("Pet Type", "Type of pet (Dog, Cat, Hamster):", choices=["Dog","Cat","Hamster"])
color = kawaii_input("Pet Color", "Pet color:")
pet = {"name": name, "type": ptype, "color": color, "age": 0, "happiness": 100, "health": 100, "hunger": 100, "sick": False}

# ------------------- LOAD IMAGES -------------------
happy_img = tk.PhotoImage(file="happy.png")
neutral_img = tk.PhotoImage(file="neutral.png")
sad_img = tk.PhotoImage(file="sad.png")
sick_img = tk.PhotoImage(file="sick.png")
pet_images = {}
basic_animals = ["dog", "cat", "hamster"]
moods = ["happy", "neutral", "sad", "sick"]
for animal in basic_animals:
    pet_images[animal] = {}
    for mood in moods:
        try:
            pet_images[animal][mood] = tk.PhotoImage(file=f"{animal}_{mood}.png")
        except:
            pet_images[animal][mood] = neutral_img

# ------------------- DISPLAY -------------------
info = tk.Frame(root, bg="#ffeaf4", bd=3, relief="ridge", padx=15, pady=15)
info.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.18)
title = tk.Label(info, font=("Comic Sans MS", 22, "bold"), bg="#ffeaf4", fg="#ff77cc")
title.pack(pady=5)
stats = tk.Label(info, font=("Comic Sans MS", 14), bg="#ffeaf4", fg="#aa5588")
stats.pack()
money = tk.Label(root, font=("Comic Sans MS", 16, "bold"), bg="#ffd6ec", fg="#ff55aa")
money.place(relx=0.02, rely=0.22, relwidth=0.3, relheight=0.06)
pet_image_label = tk.Label(root, bg="#ffd6ec")
pet_image_label.place(relx=0.35, rely=0.22, relwidth=0.3, relheight=0.35)

# ------------------- PET MOOD & DISPLAY -------------------
def get_pet_mood():
    if pet["health"] <= 0: return "dead"
    if pet.get("sick", False) and pet["health"] < 70: return "sick"
    if pet["hunger"] < 25: return "sad"
    if pet["happiness"] < 40: return "neutral"
    return "happy"

def update_display():
    mood = get_pet_mood()
    title.config(text=f"{pet['name']} the {pet['color']} {pet['type']} 🐾")
    stats.config(text=f"💖 Health: {pet['health']}   😊 Happiness: {pet['happiness']}   🍎 Hunger: {pet['hunger']}   🎂 Age: {pet['age']}")
    money.config(text=f"💰 Balance: ${balance}")
    pet_type_lower = pet["type"].lower()
    if pet_type_lower in pet_images:
        pet_image_label.config(image=pet_images[pet_type_lower].get(mood, pet_images[pet_type_lower]["neutral"]))
    else:
        pet_image_label.config(image=neutral_img)
    if pet["health"] <= 0:
        show_kawaii_popup(f"{pet['name']} has passed away 💀")
        root.destroy()

# ------------------- SPARKLE -------------------
def sparkle_animation(): # for aesthetic purposes
    for _ in range(10):
        x = random.randint(int(root.winfo_width()*0.35), int(root.winfo_width()*0.65))
        y = random.randint(int(root.winfo_height()*0.22), int(root.winfo_height()*0.57))
        sparkle = canvas.create_text(x, y, text="✨", font=("Arial", 20))
        root.after(500, lambda s=sparkle: canvas.delete(s))

# ------------------- RANDOM SICKNESS -------------------
def random_sickness():
    if random.random() < 0.05: # 5% chance
        pet["health"] = max(0, pet["health"] - 30)
        pet["sick"] = True
        logHealthUpdate(pet, -30, "Extreme sickness")
        show_kawaii_popup(f"{pet['name']} got extremely sick! 🤢")
    elif random.random() < 0.2: # 20% chance
        pet["health"] = max(0, pet["health"] - 10)
        pet["sick"] = True
        logHealthUpdate(pet, -10, "Sickness")
        show_kawaii_popup(f"{pet['name']} got sick! 🤒")

# ------------------- FULL ACTIONS -------------------
feed_count = 0
play_count = 0

def check_age():
    global feed_count, play_count
    if feed_count >= 5 and play_count >= 5 and pet["health"] > 50:
        pet["age"] += 1
        pet["happiness"] = max(0, pet["happiness"] - 5)
        pet["health"] = max(0, pet["health"] - 5)
        show_kawaii_popup(f"{pet['name']} is now {pet['age']} years old! 🎂✨")
        sparkle_animation()
        feed_count = 0
        play_count = 0

# ------------------- ACTION FUNCTIONS -------------------
def feed_action(): # feed pet
    global feed_count
    if not ownedFoods:
        show_kawaii_popup("No food owned! 😢")
        return
    food = kawaii_input("Feed", "Choose a food to feed:", choices=list(ownedFoods.keys()))
    if not food: return
    amount = kawaii_input("Feed Amount", f"How many {food}? (max {ownedFoods[food]})", input_type="integer", max_value=ownedFoods[food])
    if not amount: return
    multiplier = amount
    pet["hunger"] = min(100, pet["hunger"] + 10*multiplier)
    pet["health"] = min(100, pet["health"] + 5*multiplier)
    pet["happiness"] = min(100, pet["happiness"] + 5*multiplier)
    ownedFoods[food] -= amount
    if ownedFoods[food] == 0: del ownedFoods[food]
    logHealthUpdate(pet, 5*multiplier, f"Ate {amount} {food}")
    logExpense(foods[food]*amount, f"Fed {food} x{amount}")
    show_kawaii_popup(f"{pet['name']} ate {amount} {food}! 🍽️")
    sparkle_animation()
    feed_count += 1
    check_age()
    update_display()

def play_action(): # play with pet
    global play_count
    if not ownedToys:
        show_kawaii_popup("No toys owned! 😢")
        return
    toy = kawaii_input("Play", "Choose a toy to play with:", choices=list(ownedToys.keys()))
    if not toy: return
    amount = kawaii_input("Play Amount", f"How many times to play? (max {ownedToys[toy]})", input_type="integer", max_value=ownedToys[toy])
    if not amount: return
    multiplier = amount
    pet["happiness"] = min(100, pet["happiness"] + 10*multiplier)
    pet["health"] = min(100, pet["health"] + 5*multiplier)
    pet["hunger"] = max(0, pet["hunger"] - 5*multiplier)
    ownedToys[toy] -= amount
    if ownedToys[toy] == 0: del ownedToys[toy]
    logHealthUpdate(pet, 5*multiplier, f"Played with {toy} x{amount}")
    show_kawaii_popup(f"{pet['name']} played with {toy} {amount} times! 🎾")
    sparkle_animation()
    play_count += 1
    check_age()
    update_display()

def heal_action(): # heal pet
    global balance
    if balance < 100:
        show_kawaii_popup("Not enough money to heal! 💸")
        return
    pet["health"] = min(100, pet["health"] + 20)
    pet["happiness"] = max(0, pet["happiness"] - 5)
    balance -= 100
    logExpense(-100, "Healed pet")
    logHealthUpdate(pet, 20, "Healed by doctor")
    show_kawaii_popup(f"{pet['name']} has been healed! 💉")
    update_display()

def buy_food_action(): # purchase food
    global balance
    food = kawaii_input("Buy Food", f"Choose food to buy:", choices=list(foods.keys()))
    if not food: return
    max_amt = balance // foods[food]
    if max_amt <= 0:
        show_kawaii_popup("Not enough money to buy this food! 💸")
        return
    amount = kawaii_input("Amount", f"How many {food}? (max {max_amt})", input_type="integer", max_value=max_amt)
    if not amount: return
    balance -= foods[food] * amount
    if food in ownedFoods: ownedFoods[food] += amount
    else: ownedFoods[food] = amount
    logExpense(foods[food]*amount, f"Bought {food} x{amount}")
    show_kawaii_popup(f"You bought {amount} {food}! 🛒")
    update_display()

def buy_toy_action(): # purchase toys
    global balance
    toy = kawaii_input("Buy Toy", f"Choose toy to buy:", choices=list(toys.keys()))
    if not toy: return
    max_amt = balance // toys[toy]
    if max_amt <= 0:
        show_kawaii_popup("Not enough money to buy this toy! 💸")
        return
    amount = kawaii_input("Amount", f"How many {toy}? (max {max_amt})", input_type="integer", max_value=max_amt)
    if not amount: return
    balance -= toys[toy] * amount
    if toy in ownedToys: ownedToys[toy] += amount
    else: ownedToys[toy] = amount
    logExpense(toys[toy]*amount, f"Bought {toy} x{amount}")
    show_kawaii_popup(f"You bought {amount} {toy}! 🎁")
    update_display()

def work_action(): # earn money for the user
    global balance
    job = kawaii_input("Work", "Choose a job to do:", choices=list(jobs.keys()))
    if not job: return
    balance += jobs[job]
    happiness_loss = jobs[job] // 10
    pet["happiness"] = max(0, pet["happiness"] - happiness_loss)
    logExpense(jobs[job], f"Earned from {job}")
    show_kawaii_popup(f"You worked as a {job} and earned ${jobs[job]}! 🏢")
    update_display()

def view_health_report(): # summary of health changes
    report_text = "\n--- Health Report ---\n"
    if not healthReport:
        report_text += "No health updates recorded yet."
    else:
        for entry in healthReport:
            change_str = f"+{entry['change']}" if entry['change'] > 0 else f"{entry['change']}"
            report_text += f"[{entry['timestamp']}] {entry['reason']}: {entry['old_health']} -> {entry['new_health']} ({change_str})\n"
    show_kawaii_popup(report_text)

def view_expense_report(): # summary of balance changes (like transactions in bank account)
    report_text = "\n--- Expense Report ---\n"
    if not expenseReport:
        report_text += "No expenses recorded yet."
    else:
        for entry in expenseReport:
            change_str = f"+{entry['change']}" if entry['change'] > 0 else f"{entry['change']}"
            report_text += f"[{entry['timestamp']}] {entry['reason']}: {entry['old_balance']} -> {entry['new_balance']} ({change_str})\n"
    show_kawaii_popup(report_text)

# ------------------- BUTTONS -------------------
button_frame = tk.Frame(root, bg="#ffd6ec")
button_frame.place(relx=0.02, rely=0.6, relwidth=0.96, relheight=0.35)

actions = [
    ("Feed", feed_action),
    ("Play", play_action),
    ("Heal", heal_action),
    ("Buy Food", buy_food_action),
    ("Buy Toy", buy_toy_action),
    ("Work", work_action),
    ("Health Report", view_health_report),
    ("Expense Report", view_expense_report)
]

for i, (text, action) in enumerate(actions):
    btn = tk.Button(button_frame, text=text, command=action, font=("Comic Sans MS", 12, "bold"),
                    bg="#ffccff", fg="#6b3e5e", activebackground="#ffb3ee", relief="raised")
    btn.grid(row=i//2, column=i%2, sticky="nsew", padx=5, pady=5)

for r in range(4):
    button_frame.rowconfigure(r, weight=1)
for c in range(2):
    button_frame.columnconfigure(c, weight=1)

# ------------------- GAME TICK -------------------
def game_tick(): # counts each game loop, one loop is 20 seconds
    pet["hunger"] = max(0, pet["hunger"] - 2)
    if pet["hunger"] < 40: pet["happiness"] = max(0, pet["happiness"] - 5)
    if pet["hunger"] <= 10: pet["health"] = max(0, pet["health"] - 10)
    pet["sick"] = False
    random_sickness()
    update_display()
    root.after(20000, game_tick)  # every 20 seconds

update_display()
game_tick()
root.mainloop()

# ------------------- END -------------------