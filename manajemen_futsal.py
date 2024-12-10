import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Fungsi untuk koneksi ke database
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="futsal_booking_system"
    )

# Fungsi untuk menambahkan booking
def add_booking():
    name = entry_name.get()
    phone = entry_phone.get()
    field = combo_field.get()
    booking_time = entry_time.get()
    booking_date = entry_date.get()

    if name and phone and field and booking_time and booking_date:
        try:
            field = int(field)
        except ValueError:
            messagebox.showerror("Input Error", "Lapangan harus dipilih!")
            return

        connection = create_connection()
        cursor = connection.cursor()

        query = "INSERT INTO bookings (name, phone, field, booking_time, booking_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, phone, field, booking_time, booking_date))
        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo("Success", f"Booking untuk {name} berhasil ditambahkan!")
        clear_fields()  # Automatically clear the fields after adding a booking
        show_bookings()
    else:
        messagebox.showwarning("Input Error", "Semua field harus diisi!")

# Fungsi untuk menampilkan semua booking
def show_bookings():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()

    for row in booking_table.get_children():
        booking_table.delete(row)

    for row in rows:
        booking_table.insert("", "end", values=row)

    cursor.close()
    connection.close()

# Fungsi untuk menghapus booking
def delete_booking():
    selected_item = booking_table.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Pilih booking yang ingin dihapus.")
        return

    booking_id = booking_table.item(selected_item[0], "values")[0]

    connection = create_connection()
    cursor = connection.cursor()

    query = "DELETE FROM bookings WHERE id = %s"
    cursor.execute(query, (booking_id,))
    connection.commit()

    cursor.close()
    connection.close()

    messagebox.showinfo("Success", f"Booking dengan ID {booking_id} berhasil dihapus!")
    clear_fields()  # Automatically clear the fields after deleting a booking
    show_bookings()

# Fungsi untuk memperbarui booking
def update_booking():
    selected_item = booking_table.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Pilih booking yang ingin diupdate.")
        return

    booking_id = booking_table.item(selected_item[0], "values")[0]
    name = entry_name.get()
    phone = entry_phone.get()
    field = combo_field.get()
    booking_time = entry_time.get()
    booking_date = entry_date.get()

    if name and phone and field and booking_time and booking_date:
        try:
            field = int(field)
        except ValueError:
            messagebox.showerror("Input Error", "Lapangan harus dipilih!")
            return

        connection = create_connection()
        cursor = connection.cursor()

        query = """
        UPDATE bookings 
        SET name = %s, phone = %s, field = %s, booking_time = %s, booking_date = %s 
        WHERE id = %s
        """
        cursor.execute(query, (name, phone, field, booking_time, booking_date, booking_id))
        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo("Success", f"Booking dengan ID {booking_id} berhasil diupdate!")
        clear_fields()  # Automatically clear the fields after updating a booking
        show_bookings()
    else:
        messagebox.showwarning("Input Error", "Semua field harus diisi!")

# Fungsi untuk mengisi field input berdasarkan item yang dipilih
def fill_fields():
    selected_item = booking_table.selection()
    if not selected_item:
        return

    values = booking_table.item(selected_item[0], "values")
    entry_name.delete(0, "end")
    entry_name.insert(0, values[1])
    entry_phone.delete(0, "end")
    entry_phone.insert(0, values[2])
    combo_field.set(values[3])
    entry_time.delete(0, "end")
    entry_time.insert(0, values[4])
    entry_date.delete(0, "end")
    entry_date.insert(0, values[5])

# Fungsi untuk membersihkan input
def clear_fields():
    entry_name.delete(0, "end")
    entry_phone.delete(0, "end")
    combo_field.set("")
    entry_time.delete(0, "end")
    entry_date.delete(0, "end")

# Fungsi utama untuk membuat GUI
def create_gui():
    global entry_name, entry_phone, combo_field, entry_time, entry_date, booking_table

    app = tk.Tk()
    app.title("Sistem Booking Lapangan Futsal")
    app.geometry("950x600")

    # Frame Input
    frame_input = tk.Frame(app, padx=10, pady=10)
    frame_input.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(frame_input, text="Nama", width=10).grid(row=0, column=0, padx=5, pady=5)
    entry_name = tk.Entry(frame_input, width=30)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_input, text="No. HP", width=10).grid(row=0, column=2, padx=5, pady=5)
    entry_phone = tk.Entry(frame_input, width=30)
    entry_phone.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame_input, text="Lapangan", width=10).grid(row=1, column=0, padx=5, pady=5)
    combo_field = ttk.Combobox(frame_input, values=["1", "2", "3"], width=28, state="readonly")
    combo_field.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_input, text="Jam Booking", width=10).grid(row=1, column=2, padx=5, pady=5)
    entry_time = tk.Entry(frame_input, width=30)
    entry_time.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(frame_input, text="Tanggal Booking", width=15).grid(row=2, column=0, padx=5, pady=5)
    entry_date = tk.Entry(frame_input, width=30)
    entry_date.grid(row=2, column=1, padx=5, pady=5)

    # Frame Tombol
    frame_buttons = tk.Frame(app, padx=10, pady=10)
    frame_buttons.pack(fill=tk.X, padx=10, pady=10)

    tk.Button(frame_buttons, text="Tambah Booking", command=add_booking).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Update Booking", command=update_booking).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Hapus Booking", command=delete_booking).pack(side=tk.LEFT, padx=10)

    # Tabel Booking
    frame_table = tk.Frame(app, padx=10, pady=10)
    frame_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    columns = ("ID", "Nama", "No. HP", "Lapangan", "Jam Booking", "Tanggal Booking")
    booking_table = ttk.Treeview(frame_table, columns=columns, show="headings")

    for col in columns:
        booking_table.heading(col, text=col, anchor="center")
        booking_table.column(col, anchor="center")

    booking_table.bind("<<TreeviewSelect>>", lambda e: fill_fields())
    booking_table.pack(fill=tk.BOTH, expand=True)

    show_bookings()
    app.mainloop()

# Menjalankan aplikasi
if __name__ == "__main__":
    create_gui()
