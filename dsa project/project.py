import tkinter as tk  # Tkinter GUI banane ke liye use hota hai
from tkinter import messagebox  # Tkinter ka messagebox alerts aur messages show karne ke liye
from tkinter import simpledialog  # Tkinter ka simpledialog input dialogs ke liye
import numpy as np  # Numpy high-performance arrays aur data processing ke liye
from tkinter import ttk  # Tkinter themed widgets jaise modern buttons aur tables ke liye
import re  # Regular Expressions strings validate karne aur pattern matching ke liye
from PIL import Image, ImageTk  # Pillow library images ko process aur GUI par dikhane ke liye

# Queue aur booking history ko store karne ke liye numpy arrays
queue = np.array([], dtype=str)
booking_history = np.array([], dtype=str)

# Movies aur prices ko numpy arrays mein store karna
movies = np.array([
    "Forrest Gump", "A Beautiful Mind", "The Godfather",
    "Bol", "Verna",
    "Inception", "The Dark Knight", "Pulp Fiction",
    "The Shawshank Redemption", "The Matrix",
    "Gladiator", "Fight Club", "Interstellar",
    "The Social Network", "Parasite",
    "Avengers: Endgame", "Titanic", "Jurassic Park",
    "The Lion King", "Star Wars: A New Hope",
    "The Silence of the Lambs"
], dtype=str)

prices = np.array([
    500, 700, 600, 800, 750,
    900, 950, 850, 700, 800,
    600, 650, 1000, 1200, 1100,
    1300, 1400, 1600, 1700, 1800,
    1900
], dtype=int)

# Total seats aur booked seats ki initialization
total_seats = 100
booked_seats = np.array([], dtype=int)

# Har customer ke liye seat count ko track karne ke liye dictionary
customer_seat_count = {}

# Last ID ko track karne ke liye variable
last_id = 0

# Queue ko file me save karne ka function
def save_queue():
    # "queue.txt" file ko write mode mein open karo
    with open("queue.txt", "w") as f:   # Agar file exist karti hai to overwrite ho jayegi, agar nahi hai to nayi file create hogi
        for record in queue:
            f.write(record + "\n")   # Har record ko file mein likho, har record ke baad ek nayi line add karo


# Queue ko file se load karne ka function
def load_queue():
    global queue, last_id
    try:
        # "queue.txt" file ko read mode mein open karo
        with open("queue.txt", "r") as f:
            # strip(): Line ke start aur end ke spaces ko remove karta hai
            # readlines(): File se saari lines ko ek list mein read karta hai
            queue = np.array([line.strip() for line in f.readlines()], dtype=str)

            if queue.size > 0:
                # Last record se ID ko extract karke last_id update karo
                # split(" - "): Line ko " - " se split karta hai, aur pehla part (ID) ko fetch karta hai
                last_id = int(queue[-1].split(" - ")[0])
    except FileNotFoundError:
        # Agar file nahi milti, queue ko empty array set karo
        queue = np.array([], dtype=str)


# Booking history ko file me save karne ka function
def save_booking_history():
    with open("booking_history.txt", "w") as f:
        for record in booking_history:
            f.write(record + "\n")

# Booking history ko file se load karne ka function
def load_booking_history():
    global booking_history
    try:
        with open("booking_history.txt", "r") as f:
            booking_history = np.array([line.strip() for line in f.readlines()], dtype=str)
    except FileNotFoundError:
        booking_history = np.array([], dtype=str)  # Agar file nahi milti to booking history ko khali array set karna

# Queue aur booking history ko load karna
load_queue()
load_booking_history()

# Email ki validity check karne ka function
def is_valid_email(email):
    # Email format ko check karne ke liye regex pattern
    # Starts with alphanumeric or allowed symbols, contains @, domain, and extension.
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    # Return True if email matches regex, otherwise False
    return re.match(regex, email) is not None


# Queue me shamil hone ke liye dialog box
def join_queue():
    dialog = tk.Toplevel(root)  # Naya dialog window create karna
    dialog.title("Join Queue")  # Dialog ka title set karna
    dialog.geometry("400x300")  # Dialog ki size set karna
    dialog.configure(bg="#F5DEB3")  # Dialog ka background color set karna 3configure window ka appearance change krna like bg set krna

    # User se name input lene ka label aur entry field
    tk.Label(dialog, text="Enter your name:", bg="#F5DEB3").pack(pady=5)
    name_entry = tk.Entry(dialog, bg="white")
    name_entry.pack(pady=5) #pack widget ko window ya frame k andar adjust krta

    # User se email input lene ka label aur entry field
    tk.Label(dialog, text="Enter your email:", bg="#F5DEB3").pack(pady=5)
    email_entry = tk.Entry(dialog, bg="white")
    email_entry.pack(pady=5)

    # User se age input lene ka label aur entry field
    tk.Label(dialog, text="Enter your age:", bg="#F5DEB3").pack(pady=5)
    age_entry = tk.Entry(dialog, bg="white")
    age_entry.pack(pady=5)

    # OK button ka function, jab user click karega
    def on_ok():
        name = name_entry.get()  # Name input get karna
        email = email_entry.get()  # Email input get karna
        age_str = age_entry.get()  # Age input get karna
        age = int(age_str) if age_str.isdigit() else None  # Age ko valid integer me convert karna

        dialog.destroy()  # Dialog window ko band karna
        process_queue(name, email, age)  # Queue me user ko add karna

    # OK button create karna aur on_ok function ko bind karna
    tk.Button(dialog, text="OK", command=on_ok, bg="white").pack(pady=10)

    dialog.transient(root)  # Dialog ko root ke upar display karna
    dialog.grab_set()  # Dialog ko focus me lana, baki window pe click nahi hoga
    root.wait_window(dialog)  # Root ko wait karna jab tak dialog band nahi hota


# Queue me shamil hone ka process
def process_queue(name, email, age):
    global queue, last_id

    if age is None or age < 18:
        messagebox.showerror("Error", "You must be 18 years or older to join the queue.")  # Agar age 18 se kam hai to error
        return

    if name and email:
        if not is_valid_email(email):
            messagebox.showerror("Error", "Please enter a valid email address.")  # Agar email valid nahi hai to error
            return

        last_id += 1  # Last ID ko increment karna
        queue = np.append(queue, f"{last_id} - {name} - {email} - {age} - waiting")  # Queue me naya record add karna
        save_queue()  # Queue ko file me save karna
        messagebox.showinfo("Queue Status ", f"{name}, you have joined the queue. Position: {len(queue)} (ID: {last_id})")  # Confirmation message
    else:
        messagebox.showerror("Error", "Please provide valid name and email.")  # Agar name ya email nahi diya to error

# Queue ki status dekhne ka function
def view_queue_status():
    if queue.size > 0:  # Agar queue me records hain
        queue_window = tk.Toplevel(root)  # Naya window create karna
        queue_window.title("Current Queue")  # Window ka title set karna
        queue_window.geometry("500x300")  # Window ka size set karna
        queue_window.config(bg="#F5DEB3")  # Window ka background color set karna

        # Treeview widget create karna, jo queue ke records dikhayega
        tree = ttk.Treeview(queue_window, columns=("ID", "Name", "Email", "Age", "Status"), show="headings")
        tree.heading("ID", text="ID")  # "ID" column ka heading set karna
        tree.heading("Name", text="Name")  # "Name" column ka heading set karna
        tree.heading("Email", text="Email")  # "Email" column ka heading set karna
        tree.heading("Age", text="Age")  # "Age" column ka heading set karna
        tree.heading("Status", text="Status")  # "Status" column ka heading set karna

        # Columns ki width set karna
        tree.column("ID", width=50)
        tree.column("Name", width=150)
        tree.column("Email", width=150)
        tree.column("Age", width=50)
        tree.column("Status", width=100)

        # Queue ke records ko treeview me insert karna
        for record in queue:
            fields = record.split(" - ")  # Record ko " - " se split karna
            tree.insert("", tk.END, values=(fields[0], fields[1], fields[2], fields[3], fields[4]))  # Values insert karna

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Treeview ko window me pack karna
    else:
        messagebox.showinfo("Queue Status", "No one is in the queue!")  # Agar queue khali ho to message dikhana


def book_ticket():
    global queue, booking_history  # Queue aur booking history ko global scope me use karne ke liye declare karna

    # Queue agar khali hai to user ko error dikhana
    if queue.size == 0:
        messagebox.showerror("Error", "No one is in the queue!")  # Queue me koi nahi hai, isliye error show karna
        return

    front_customer = queue[0]  # Queue ka sabse pehla customer fetch karna
    front_customer_details = front_customer.split(" - ")  # Customer ka record split kar ke details extract karna
    front_customer_id = int(front_customer_details[0])  # Customer ID ko extract karna
    front_customer_name = front_customer_details[1]  # Customer ka naam extract karna

    # User se Customer ID aur naam confirm karne ke liye dialog box open karna
    customer_id = simpledialog.askinteger("Confirm Booking", "Enter your customer ID:")  # ID input lena
    name = simpledialog.askstring("Confirm Booking", "Enter your name to confirm booking:")  # Name input lena

    # Agar entered details correct hain to booking ka form open karna
    if customer_id == front_customer_id and name == front_customer_name:
        booking_form = tk.Toplevel(root)  # Naya booking form window open karna
        booking_form.title("Book Your Ticket")  # Booking form ka title set karna
        booking_form.geometry("600x600")  # Booking form ka size set karna
        booking_form.configure(bg="#F5DEB3")  # Background color set karna

        # Default movie select karne ke liye variable create karna
        selected_movie = tk.StringVar(value=movies[0])  # Pehli movie ko default value set karna
        movie_label = tk.Label(booking_form, text="Available Movies", font=("Times New Roman", 12), bg="#F5DEB3")
        movie_label.grid(row=0, column=0, padx=10, pady=10)  # Movie label ko position karna

        # Movies ka listbox create karna
        movie_listbox = tk.Listbox(booking_form, height=20)  # Listbox widget movies dikhane ke liye
        for movie in movies:
            movie_listbox.insert(tk.END, movie)  # Har movie ko listbox me add karna
        movie_listbox.grid(row=1, column=0, padx=10, pady=10)  # Listbox ko position karna

        price_label = tk.Label(booking_form, text="Movie Prices", font=("Times New Roman", 12), bg="#F5DEB3")
        price_label.grid(row=0, column=1, padx=10, pady=10)  # Prices ka label position karna

        # Prices ka listbox create karna
        price_listbox = tk.Listbox(booking_form, height=20)  # Listbox widget prices dikhane ke liye
        for price in prices:
            price_listbox.insert(tk.END, f"{price} PKR")  # Har price ko listbox me add karna
        price_listbox.grid(row=1, column=1, padx=10, pady=10)  # Price listbox ko position karna

        ticket_quantity_label = tk.Label(booking_form, text="Select Ticket Quantity", font=("Times New Roman", 12), bg="#F5DEB3")
        ticket_quantity_label.grid(row=2, column=0, padx=10, pady=10)  # Ticket quantity label ko position karna

        # Spinbox create karna ticket quantity select karne ke liye
        ticket_quantity = tk.Spinbox(booking_form, from_=1, to=10, width=5)  # Quantity select karne ka spinbox
        ticket_quantity.grid(row=3, column=0, padx=10, pady=10)  # Spinbox ko position karna

        # Payment ka button create karna
        payment_button = tk.Button(booking_form, text="Make Payment",
                                   command=lambda: open_payment_form(movie_listbox, ticket_quantity, booking_form), bg="white")
        payment_button.grid(row=4, column=0, padx=10, pady=20)  # Payment button ko position karna
    else:
        messagebox.showerror("Error", f"You are not at the front of the queue. Current front: {front_customer_name}.")
        # Agar user queue ke front me nahi hai to error dikhana



# Payment form kholne ka function
def open_payment_form(movie_listbox, ticket_quantity, booking_form):
    payment_form = tk.Toplevel(root)  # Naya payment form kholna
    payment_form.title("Payment Form")  # Form ka title set karna
    payment_form.geometry("400x700")  # Form ki size set karna
    payment_form.config(bg="#F5DEB3")  # Background color set karna
    # curselection() is a method in Tkinter used with widgets like Listbox, Text, or Treeview to get the currently selected item(s).
    # selected_idx = movie_listbox.curselection() selected movie ka index leta hai
    selected_idx = movie_listbox.curselection()  # Selected movie ka index

    selected_movie_name = movies[selected_idx[0]]  # Selected movie ka naam
    price = prices[selected_idx[0]]  # Movie ka price
    quantity = int(ticket_quantity.get())  # Ticket quantity lena
    total_amount = price * quantity  # Total amount calculate karna

    # Account number, name, balance fields
    tk.Label(payment_form, text="Enter Account Number:", bg="#F5DEB3").pack(pady=10)
    account_number = tk.Entry(payment_form)  # Account number ka entry field
    account_number.pack(pady=10)

    tk.Label(payment_form, text="Enter Account Name:", bg="#F5DEB3").pack(pady=10)
    account_name = tk.Entry(payment_form)  # Account name ka entry field
    account_name.pack(pady=10)

    tk.Label(payment_form, text="Enter Account Balance:", bg="#F5DEB3").pack(pady=10)
    account_balance = tk.Entry(payment_form)  # Account balance ka entry field
    account_balance.pack(pady=10)

    # Payment method options (EasyPaisa, JazzCash, Bank)
    payment_method = tk.StringVar(value="EasyPaisa")  # Default payment method
    tk.Label(payment_form, text="Select Payment Method:", bg="#F5DEB3").pack(pady=10)
    tk.Radiobutton(payment_form, text="EasyPaisa", variable=payment_method, value="EasyPaisa", bg="#F5DEB3").pack(pady=5)  # Payment method options
    tk.Radiobutton(payment_form, text="JazzCash", variable=payment_method, value="JazzCash", bg="#F5DEB3").pack(pady=5)
    tk.Radiobutton(payment_form, text="Bank", variable=payment_method, value="Bank", bg="#F5DEB3").pack(pady=5)

    # Confirm payment button
    confirm_payment_button = tk.Button(payment_form, text="Confirm Payment",
                                       command=lambda: confirm_payment(account_number, account_name, account_balance, payment_method, total_amount, payment_form, booking_form, quantity), bg="white")  # Confirm payment button
    confirm_payment_button.pack(pady=20)


# Payment confirm karne ka function
def confirm_payment(account_number, account_name, account_balance, payment_method, total_amount, payment_form, booking_form, quantity):
    try:
        balance = float(account_balance.get())  # Account balance ko float me convert karna
        if balance < total_amount:
            messagebox.showerror("Error", "Insufficient balance!")  # Agar balance kam hai to error
            return
        else:
            new_balance = balance - total_amount  # Naya balance calculate karna
            messagebox.showinfo("Payment", f"Payment of {total_amount} PKR made successfully via {payment_method.get()} from account {account_number.get()} of {account_name.get()}. Remaining balance: {new_balance} PKR")  # Payment confirmation message
            payment_form.destroy()  # Payment form ko band karna
            booking_form.destroy()  # Booking form ko band karna
            confirm_booking(quantity)  # Booking confirm karna
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid balance.")  # Agar balance valid nahi hai to error

# Seat selection ka form kholne ka function
def open_seat_selection(quantity, name, customer_id):
    seat_selection_form = tk.Toplevel(root)
    seat_selection_form.title("Seat Selection")
    seat_selection_form.geometry("400x300")
    seat_selection_form.config(bg="#F5DEB3")
    tk.Label(seat_selection_form, text=f"{name}, you have booked {quantity} tickets.", font=("Arial", 12), bg="#F5DEB3").pack(pady=10)  # Ticket quantity ka message

    seat_grid = tk.Frame(seat_selection_form)  # Seat grid banane ka frame
    seat_grid.pack(pady=10)

    seats = []  # Seats ka list banani hai
    for i in range(total_seats):  # yh loop har seat k liye button banata
        # Seat button create karna aur usme select_seat function ko assign karna
        seat = tk.Button(seat_grid, text=f"Seat {i+1}", width=10, command=lambda i=i: select_seat(i, seat_selection_form, quantity, name, customer_id), bg="white") #har button ek label milna seat1,seat2,seat3
        seat.grid(row=i//10, column=i%10, padx=5, pady=5)  # Seat button ko grid mein place karna
        seats.append(seat)  # Seat ko list mein add karna

    for seat in booked_seats:  # Jo seats already booked hain unko disable karna
        seats[seat].config(state="disabled", bg="gray")  # Booked seats ko disable aur gray karna



# Seat select karne ka function
def select_seat(seat_number, seat_selection_form, quantity, name, customer_id):
    global booked_seats, customer_seat_count

    # Agar customer ka seat count pehle se nahi hai, toh initialize karna
    if customer_id not in customer_seat_count:
        customer_seat_count[customer_id] = 0  # Customer ka seat count initialize karna

    # Agar customer ne required number of seats nahi book ki hain
    if customer_seat_count[customer_id] < quantity:
        booked_seats = np.append(booked_seats, seat_number)  # Seat ko booked seats mein add karna
        customer_seat_count[customer_id] += 1  # Customer ka seat count increment karna
        messagebox.showinfo("Seat Selection", f"Seat {seat_number + 1} has been booked by {name}!")  # Seat booking confirmation message

        # Agar customer ne apni required seats book kar li hain
        if customer_seat_count[customer_id] == quantity:
            messagebox.showinfo("Booking Complete", f"{name}, you have booked your required seats: {quantity} according to your tickets.")  # Booking complete message
            seat_selection_form.destroy()  # Seat selection form ko band karna

    else:
        # Agar customer ne pehle se required seats book kar li hain
        messagebox.showerror("Error", f"{name} has already booked the required number of seats!")  # Error message

# Booking confirm karne ka function
def confirm_booking(quantity):
    global queue, booking_history
    front_customer = queue[0]  # Queue ka pehla customer
    front_customer_details = front_customer.split(" - ")
    customer_id = int(front_customer_details[0])
    name = front_customer_details[1]

    selected_movie_name = movies[0]  # Pehli movie ko select karna
    price = prices[0]  # Pehli movie ka price
    queue = np.delete(queue, 0)  # Queue se pehle customer ko delete karna or booking history me daldena
    save_queue()  # Updated queue ko file me save karna
    booking_history = np.append(booking_history, f"{customer_id} - {name} - {selected_movie_name} - {quantity} - {price} PKR - booked")  # Booking history me record add karna
    save_booking_history()  # Booking history ko file me save karna
    messagebox.showinfo("Booking Status", f"{name}, your booking has been confirmed!")  # Booking confirmation message
    open_seat_selection(quantity, name, customer_id)  # Seat selection form kholna

# Booking history dekhne ka function
def view_booking_history():
    # Booking history ka naya window create karna
    history_window = tk.Toplevel(root)
    history_window.title("Booking History")
    history_window.geometry("600x400")
    history_window.config(bg="#F5DEB3")

    # Treeview widget banane ka, jisme booking history display hogi
    tree = ttk.Treeview(history_window, columns=("Customer ID", "Customer", "Movie", "Quantity", "Amount", "Status"), show="headings")

    # Treeview ke columns ka headings set karna
    tree.heading("Customer ID", text="Customer ID")
    tree.heading("Customer", text="Customer")
    tree.heading("Movie", text="Movie")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Amount", text="Amount")
    tree.heading("Status", text="Status")

    # Treeview ke columns ki width set karna
    tree.column("Customer ID", width=100)
    tree.column("Customer", width=150)
    tree.column("Movie", width=150)
    tree.column("Quantity", width=100)
    tree.column("Amount", width=100)
    tree.column("Status", width=100)

    # Booking history ke records ko treeview mein insert karna
    for record in booking_history:
        fields = record.split(" - ")  # Record ko split karna
        values = [field for field in fields if field]  # Empty fields ko ignore karna
        tree.insert("", tk.END, values=values)  # Treeview mein record insert karna 3tk.end is ab naya record last me insert krna

    # Treeview ko window mein pack karna
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Clear all bookings ka button, jisme saari bookings delete hongi
    clear_all_button = tk.Button(history_window, text="Clear All Bookings", command=lambda: clear_all_bookings(tree), bg="white")
    clear_all_button.pack(pady=10)

    # Search by customer ID ka button, jisme customer ID ke basis pe bookings search ki jayengi
    search_button = tk.Button(history_window, text="Search Bookings by Customer ID", command=search_bookings_by_customer_id, bg="white")
    search_button.pack(pady=10)

    # Cancel booking ka button, jisme kisi booking ko cancel kiya ja sakta hai
    cancel_button = tk.Button(history_window, text="Cancel Any Booking", command=lambda: cancel_booking(tree), bg="white")
    cancel_button.pack(pady=10)


# Customer ki booking history dikhane ka function
def display_booking_history(customer_history):
    history_window = tk.Toplevel(root)
    history_window.title("Customer Booking History")
    history_window.geometry("600x400")
    history_window.config(bg="#F5DEB3")

    tree = ttk.Treeview(history_window, columns=("Customer ID", "Customer", "Movie", "Quantity", "Amount", "Status"), show="headings")
    tree.heading("Customer ID", text="Customer ID")
    tree.heading("Customer", text="Customer")
    tree.heading("Movie", text="Movie")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Amount", text="Amount")
    tree.heading("Status", text="Status")

    tree.column("Customer ID", width=100)
    tree.column("Customer", width=150)
    tree.column("Movie", width=150)
    tree.column("Quantity", width=100)
    tree.column("Amount", width=100)
    tree.column("Status", width=100)

    for record in customer_history:
        fields = record.split(" - ")
        values = [field for field in fields if field]  #none values ko nh dalna list me
        tree.insert("", tk.END, values=values)  # Customer ki booking history ke records ko tree me insert karna

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Customer ki booking history dekhne ka function
def view_customer_booking_history():
    customer_id = simpledialog.askinteger("Customer Booking History", "Enter your customer ID:")  # Customer ID puchne ke liye dialog box
    if customer_id:  # Agar customer ne ID di hai
        # Booking history mein se customer ID ke records filter kar rahe hain
        customer_history = [record for record in booking_history if int(record.split(" - ")[0]) == customer_id]

        if customer_history:  # Agar customer ki history milti hai
            display_booking_history(customer_history)  # Customer ki booking history dikhana
        else:  # Agar customer ki koi booking history nahi hai
            messagebox.showinfo("Customer Booking History", "No bookings found for this customer.")  # Message dikhana agar koi booking nahi hai
    else:  # Agar customer ne ID nahi di
        messagebox.showerror("Error", "Please enter your customer ID.")  # Error message dikhana


# Available seats dikhane ka function
def view_seats():
    seat_selection_form = tk.Toplevel(root)
    seat_selection_form.title("Available Seats")
    seat_selection_form.geometry("400x300")
    seat_selection_form.config(bg="#F5DEB3")

    seat_grid = tk.Frame(seat_selection_form)  # Seat buttons ko display karne ke liye ek frame create karna
    seat_grid.pack(pady=10)  # Frame ko window mein pack karna

    seats = []  # Seats ka list banani hai
    for i in range(total_seats):  # Total seats ke liye loop chalana
        seat = tk.Button(seat_grid, text=f"Seat {i+1}", width=10, bg="white")  # Har seat ke liye ek button create karna
        seat.grid(row=i//10, column=i%10, padx=5, pady=5)  # Seat button ko grid mein arrange karna
        seats.append(seat)  # Seat ko list mein add karna

    for seat in booked_seats:  # Booked seats ko disable karna
        seats[seat - 1].config(state="disabled", bg="gray")  # Booked seats ko gray color aur disabled state mein convert karna

    available_seats_count = total_seats - booked_seats.size  # Available seats ka count calculate karna

    available_seats_label = tk.Label(seat_selection_form, text=f"Available Seats: {available_seats_count}", font=("Arial", 12), bg="#F5DEB3")  # Label banake available seats dikhana
    available_seats_label.pack(pady=10)  # Label ko window mein pack karna


# Saari bookings ko clear karne ka function
def clear_all_bookings(tree):
    global booking_history
    booking_history = np.array([], dtype=str)  # Booking history ko khali array set karna
    save_booking_history()  # Updated booking history ko file me save karna

    for item in tree.get_children(): #get_children() se hum treeview ke sabhi child items (rows) ko access karte hain.

        tree.delete(item)  #Phir tree.delete(item) ke through un items ko delete kiya jata hai.

    messagebox.showinfo("Success", "All bookings have been cleared!")  # Success message

# Customer ID se bookings search karne ka function
def search_bookings_by_customer_id():
    customer_id = simpledialog.askinteger("Search Booking", "Enter Customer ID:")  # Customer ID puchne ka dialog
    if customer_id is not None:
        customer_history = [record for record in booking_history if int(record.split(" - ")[0]) == customer_id]  # Customer ki history filter karna
        if customer_history:
            display_booking_history(customer_history)  # Customer ki booking history dikhana
        else:
            messagebox.showinfo("Search Result", "No bookings found for this customer ID.")  # Agar koi booking nahi hai to message

# Booking cancel karne ka function
def cancel_booking(tree):
    global booking_history
    customer_id = simpledialog.askinteger("Cancel Booking", "Enter Customer ID:")  # Customer ID puchne ka dialog
    if customer_id is not None:  # Agar customer ID di gayi ho
        booking_to_cancel = simpledialog.askstring("Cancel Booking", "Enter the movie name to cancel:")  # Cancel karne wali movie ka naam puchna
        updated_history = []  # Updated booking history store karne ke liye list
        booking_found = False  # Booking milne ka flag set karna

        for record in booking_history:  # Sab booking records ko check karna
            if (int(record.split(" - ")[0]) == customer_id and booking_to_cancel in record):  # Agar customer ID match ho aur movie naam bhi match ho
                booking_found = True  # Booking mil gayi
                continue  # Agar booking milti hai to usay skip karna (matlab us record ko history se remove karna)
            updated_history.append(record)  # Baaki records ko updated history mein add karna

        if booking_found:  # Agar matching booking mil gayi ho
            booking_history = np.array(updated_history, dtype=str)  # Updated booking history ko set karna
            save_booking_history()  # Updated booking history ko file mein save karna

            for item in tree.get_children():  # Treeview ke saare items ko delete karna
                tree.delete(item)  # Tree se saare items ko delete karna

            for record in booking_history:  # Updated booking history ko treeview mein daalna
                fields = record.split(" - ")  # Record ko split karna fields mein
                values = [field for field in fields if field]  # Empty fields ko hata kar values ko list mein store karna
                tree.insert("", tk.END, values=values)  # Updated booking history ko tree mein insert karna

            messagebox.showinfo("Success", "Booking has been canceled.")  # Success message dikhana
        else:
            messagebox.showinfo("Error", "No matching booking found.")  # Agar koi matching booking nahi milti to error dikhana


# Queue ko clear karne ka function
def clear_queue():
    if queue.size > 0:
        queue_window = tk.Toplevel(root)
        queue_window.title("Clear Queue")
        queue_window.geometry("600x500")
        queue_window.config(bg="#F5DEB3")

        tree = ttk.Treeview(queue_window, columns=("ID", "Name", "Email", "Age", "Status"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        tree.heading("Age", text="Age")
        tree.heading("Status", text="Status")

        tree.column("ID", width=50)
        tree.column("Name", width=150)
        tree.column("Email", width=150)
        tree.column("Age", width=50)
        tree.column("Status", width=100)

        for record in queue:
            fields = record.split(" - ")
            tree.insert("", tk.END, values=(fields[0], fields[1], fields[2], fields[3], fields[4]))  # Queue ke records ko tree me insert karna

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Selected customers ko clear karne ka function
        def clear_selected():
            global queue
            selected_item = tree.selection() #CURRENTLY SELECTED ITEM KI ID MILTI
            if selected_item:
                for item in selected_item:
                    tree.delete(item)  # Selected item ko tree se delete karna
                    index = int(tree.item(item)["values"][0]) - 1  # id se index nikalan kuinke selected item ki id ki basis per hum us item ko queue se remove krrhe or indexing 0 base hoti isliye 0-1
                    queue = np.delete(queue, index)  # Queue se selected customer ko delete karna
                save_queue()  # Updated queue ko file me save karna
                messagebox.showinfo("Success", "Selected customers have been removed from the queue.")  # Success message
            else:
                messagebox.showerror("Error", "Please select a customer to delete.")  # Agar koi customer select nahi kiya to error

        clear_button = tk.Button(queue_window, text="Clear Selected", command=clear_selected, bg="white")  # Clear selected button
        clear_button.pack(pady=10)

        # Saari queue ko clear karne ka function
        def clear_all():
            global queue
            queue = np.array([], dtype=str)  # Queue ko khali array set karna
            save_queue()  # Updated queue ko file me save karna
            messagebox.showinfo("Queue Cleared", "The queue has been cleared!")  # Success message
            tree.delete(*tree.get_children())  # Tree se saare items ko delete karna * means tree.get_children() se return hone wale har item ko alag-alag argument ke taur par delete() method ko pass kiya jata hai. Isse har ek child item ko delete kiya jata hai.

        clear_all_button = tk.Button(queue_window, text="Clear All", command=clear_all, bg="white")  # Clear all button
        clear_all_button.pack(pady=10)

    else:
        messagebox.showinfo("Queue Status", "The queue is empty!")  # Agar queue khali hai to message

# Thank you message dikhane ka function
def show_thank_you_message():
    thank_you_window = tk.Toplevel(root)
    thank_you_window.title("Thank You")
    thank_you_window.geometry("400x200")
    thank_you_window.config(bg="#F5DEB3")
    thank_you_label = tk.Label(thank_you_window, text="Thank you for booking, Awaiting for your feedback!", font=("Times New Roman", 16), wraplength=350)
    thank_you_label.pack(pady=50)  # Thank you message dikhana

# Background image update karne ka function
def update_background(image_path, label):
    # Image ko open karte hain jo diye gaye image_path se hai
    bg_image = Image.open(image_path)
    # Image ko resize karte hain takay wo label ki width aur height ke hisaab se ho
    bg_image = bg_image.resize((label.winfo_width(), label.winfo_height()), Image.Resampling.LANCZOS)
    # Image ko PhotoImage format mein convert karte hain takay wo tkinter ke label pe set ho sake
    bg_photo = ImageTk.PhotoImage(bg_image)
    # Label ki image ko new background se update karte hain
    label.configure(image=bg_photo)
    # Label ke andar image object ko store karte hain, takay garbage collection usay hata na de
    label.image = bg_photo  # Background image ko update karna


# Customer panel kholne ka function
def open_customer_form():
    customer_form = tk.Toplevel(root)
    customer_form.title("Customer Panel")
    customer_form.geometry("400x400")

    bg_label = tk.Label(customer_form) #yh method label ko ek specific pos pe set krta
    bg_label.place(relwidth=1, relheight=1) #se label ki width aur height ko parent container ke 100% ke barabar set kiya jata hai, jisse label poora container cover kar leta hai.
    update_background("customerbg.PNG", bg_label)  # Background image set karna

    tk.Label(customer_form, text="Customer Panel", font=("Times New Roman", 16), bg="white").pack(pady=10) #command se woh specific function call hoga
    tk.Button(customer_form, text="Join Queue", command=join_queue, bg="white").pack(pady=10)  # Join queue button
    tk.Button(customer_form, text="Book Ticket", command=book_ticket, bg="white").pack(pady=10)  # Book ticket button
    tk.Button(customer_form, text="View Queue Status", command=view_queue_status, bg="white").pack(pady=10)  # View queue status button
    tk.Button(customer_form, text="View Seats", command=view_seats, bg="white").pack(pady=10)  # View seats button
    tk.Button(customer_form, text="Customer Booking History", command=view_customer_booking_history, bg="white").pack(pady=10)  # View booking history button
    tk.Button(customer_form, text="Exit", command=lambda: [show_thank_you_message(), customer_form.destroy()], bg="white").pack(pady=10)  # Exit button

    customer_form.bind("<Configure>", lambda e: update_background("customerbg.PNG", bg_label))  # Background update on resize

# Admin panel kholne ka function
def open_admin_form():
    admin_form = tk.Toplevel(root)
    admin_form.title("Admin Panel")
    admin_form.geometry("400x400")

    bg_label = tk.Label(admin_form)
    bg_label.place(relwidth=1, relheight=1)
    update_background("adminbg.PNG", bg_label)  # Background image set karna

    tk.Label(admin_form, text="Admin Panel", font=("Times New Roman", 16), bg="white").pack(pady=10)
    tk.Button(admin_form, text="View Booking History", command=view_booking_history, bg="white").pack(pady=10)  # View booking history button
    tk.Button(admin_form, text="Clear Queue", command=clear_queue, bg="white").pack(pady=10)  # Clear queue button
    tk.Button(admin_form, text="Exit", command=admin_form.destroy, bg="white").pack(pady=10)  # Exit
    admin_form.bind("<Configure>", lambda e: update_background("adminbg.PNG", bg_label))
# Exit button

# Admin login ka function
def admin_login():
    password = simpledialog.askstring("Admin Login", "Enter admin password:", show="*")  # Admin password puchne ka dialog
    if password == "admin123":  # Agar password sahi hai
        open_admin_form()  # Admin panel kholna
    else:
        messagebox.showerror("Error", "Invalid password!")  # Agar password galat hai to error

# Main application ka initialization
root = tk.Tk()
root.title("Movie Ticket Booking System")
root.geometry("400x400")
bg_label = tk.Label(root)
bg_label.place(relwidth=1, relheight=1)
update_background("mainmenu.png", bg_label)  # Background image set karna
tk.Label(root, text="Movie Ticket Booking System", font=("Times New Roman", 20), bg="white").pack(pady=20)  # Title label
tk.Button(root, text="Customer Panel", command=open_customer_form, bg="white").pack(pady=20)  # Customer panel button
tk.Button(root, text="Admin Panel", command=admin_login, bg="white").pack(pady=20)  # Admin panel button

root.bind("<Configure>", lambda e: update_background("mainmenu.png", bg_label))  # Background update on resize bind is ek specific func ko ksi event se jorna

# Last ID ko save karne ka function
def save_last_id():
    with open("last_id.txt", "w") as f:
        f.write(str(last_id))  # Last ID ko file me save karna

#root.protocol is jab program close ho to koi specific operation perform hojaye WM_DELETE_WINDOW event triggers when we close(X) program
# Application close hone par last ID ko save karna taake jab wapis run ho program to new id se start ho
root.protocol("WM_DELETE_WINDOW", lambda: [save_last_id(), root.destroy()])

# Main loop ko start karna
root.mainloop()