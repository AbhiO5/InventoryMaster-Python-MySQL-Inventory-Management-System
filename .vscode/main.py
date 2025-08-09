import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox

# ===== Database Connection =====
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Your MySQL username
        password="password",  # Your MySQL password
        database="inventory"
    )

# ===== Main App Class =====
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory & Sales Management System")
        self.root.geometry("900x600")

        title = Label(self.root, text="Inventory & Sales Management System", font=("Arial", 18, "bold"), bg="#34495E", fg="white", pady=10)
        title.pack(fill=X)

        # Buttons
        btn_frame = Frame(self.root, pady=20)
        btn_frame.pack()

        Button(btn_frame, text="Manage Products", width=20, command=self.manage_products).grid(row=0, column=0, padx=10, pady=10)
        Button(btn_frame, text="Manage Customers", width=20, command=self.manage_customers).grid(row=0, column=1, padx=10, pady=10)
        Button(btn_frame, text="Record Sale", width=20, command=self.record_sale).grid(row=1, column=0, padx=10, pady=10)
        Button(btn_frame, text="View Sales Report", width=20, command=self.sales_report).grid(row=1, column=1, padx=10, pady=10)
        Button(btn_frame, text="Low Stock Alerts", width=20, command=self.low_stock_alert).grid(row=2, column=0, padx=10, pady=10)
        Button(btn_frame, text="Exit", width=20, command=self.root.quit).grid(row=2, column=1, padx=10, pady=10)

    # Product Management
    def manage_products(self):
        win = Toplevel(self.root)
        win.title("Manage Products")
        win.geometry("800x500")

        # Entry fields
        Label(win, text="Product Name").grid(row=0, column=0, padx=10, pady=10)
        name_var = StringVar()
        Entry(win, textvariable=name_var).grid(row=0, column=1)

        Label(win, text="Category").grid(row=1, column=0, padx=10, pady=10)
        category_var = StringVar()
        Entry(win, textvariable=category_var).grid(row=1, column=1)

        Label(win, text="Price").grid(row=2, column=0, padx=10, pady=10)
        price_var = StringVar()
        Entry(win, textvariable=price_var).grid(row=2, column=1)

        Label(win, text="Quantity").grid(row=3, column=0, padx=10, pady=10)
        qty_var = StringVar()
        Entry(win, textvariable=qty_var).grid(row=3, column=1)

        def add_product():
            if not name_var.get() or not price_var.get() or not qty_var.get():
                messagebox.showerror("Error", "Please fill all fields")
                return
            db = connect_db()
            cur = db.cursor()
            cur.execute("INSERT INTO products (name, category, price, quantity) VALUES (%s, %s, %s, %s)",
                        (name_var.get(), category_var.get(), price_var.get(), qty_var.get()))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Product added successfully")
            show_products()

        Button(win, text="Add Product", command=add_product).grid(row=4, column=1, pady=10)

        # Table
        cols = ("ID", "Name", "Category", "Price", "Quantity")
        product_table = ttk.Treeview(win, columns=cols, show="headings")
        for col in cols:
            product_table.heading(col, text=col)
            product_table.column(col, width=100)
        product_table.grid(row=5, column=0, columnspan=3, pady=20)

        def show_products():
            for row in product_table.get_children():
                product_table.delete(row)
            db = connect_db()
            cur = db.cursor()
            cur.execute("SELECT * FROM products")
            for row in cur.fetchall():
                product_table.insert("", END, values=row)
            db.close()

        show_products()

    # Customer Management
    def manage_customers(self):
        win = Toplevel(self.root)
        win.title("Manage Customers")
        win.geometry("700x400")

        Label(win, text="Customer Name").grid(row=0, column=0, padx=10, pady=10)
        name_var = StringVar()
        Entry(win, textvariable=name_var).grid(row=0, column=1)

        Label(win, text="Phone").grid(row=1, column=0, padx=10, pady=10)
        phone_var = StringVar()
        Entry(win, textvariable=phone_var).grid(row=1, column=1)

        Label(win, text="Email").grid(row=2, column=0, padx=10, pady=10)
        email_var = StringVar()
        Entry(win, textvariable=email_var).grid(row=2, column=1)

        def add_customer():
            db = connect_db()
            cur = db.cursor()
            cur.execute("INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s)",
                        (name_var.get(), phone_var.get(), email_var.get()))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Customer added successfully")
            show_customers()

        Button(win, text="Add Customer", command=add_customer).grid(row=3, column=1, pady=10)

        # Table
        cols = ("ID", "Name", "Phone", "Email")
        cust_table = ttk.Treeview(win, columns=cols, show="headings")
        for col in cols:
            cust_table.heading(col, text=col)
            cust_table.column(col, width=100)
        cust_table.grid(row=4, column=0, columnspan=3, pady=20)

        def show_customers():
            for row in cust_table.get_children():
                cust_table.delete(row)
            db = connect_db()
            cur = db.cursor()
            cur.execute("SELECT * FROM customers")
            for row in cur.fetchall():
                cust_table.insert("", END, values=row)
            db.close()

        show_customers()

    #  Record Sale
    def record_sale(self):
        win = Toplevel(self.root)
        win.title("Record Sale")
        win.geometry("600x300")

        Label(win, text="Product ID").grid(row=0, column=0, padx=10, pady=10)
        pid_var = StringVar()
        Entry(win, textvariable=pid_var).grid(row=0, column=1)

        Label(win, text="Customer ID").grid(row=1, column=0, padx=10, pady=10)
        cid_var = StringVar()
        Entry(win, textvariable=cid_var).grid(row=1, column=1)

        Label(win, text="Quantity Sold").grid(row=2, column=0, padx=10, pady=10)
        qty_var = StringVar()
        Entry(win, textvariable=qty_var).grid(row=2, column=1)

        def make_sale():
            db = connect_db()
            cur = db.cursor()
            cur.execute("SELECT quantity, price FROM products WHERE product_id = %s", (pid_var.get(),))
            product = cur.fetchone()
            if not product:
                messagebox.showerror("Error", "Product not found")
                return
            stock, price = product
            if stock < int(qty_var.get()):
                messagebox.showerror("Error", "Not enough stock")
                return

            cur.execute("INSERT INTO sales (product_id, customer_id, quantity_sold) VALUES (%s, %s, %s)",
                        (pid_var.get(), cid_var.get(), qty_var.get()))
            cur.execute("UPDATE products SET quantity = quantity - %s WHERE product_id = %s",
                        (qty_var.get(), pid_var.get()))
            db.commit()
            db.close()
            messagebox.showinfo("Success", f"Sale recorded! Total ₹{price * int(qty_var.get())}")

        Button(win, text="Record Sale", command=make_sale).grid(row=3, column=1, pady=20)

    # Sales Report
    def sales_report(self):
        win = Toplevel(self.root)
        win.title("Sales Report")
        win.geometry("800x400")

        cols = ("Product", "Total Sold")
        sales_table = ttk.Treeview(win, columns=cols, show="headings")
        for col in cols:
            sales_table.heading(col, text=col)
            sales_table.column(col, width=150)
        sales_table.pack(fill=BOTH, expand=1)

        db = connect_db()
        cur = db.cursor()
        cur.execute("""
            SELECT p.name, SUM(s.quantity_sold) 
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.name
            ORDER BY SUM(s.quantity_sold) DESC
        """)
        for row in cur.fetchall():
            sales_table.insert("", END, values=row)
        db.close()

    # Low Stock Alerts
    def low_stock_alert(self):
        win = Toplevel(self.root)
        win.title("Low Stock Alerts")
        win.geometry("600x300")

        cols = ("Product", "Stock")
        stock_table = ttk.Treeview(win, columns=cols, show="headings")
        for col in cols:
            stock_table.heading(col, text=col)
            stock_table.column(col, width=150)
        stock_table.pack(fill=BOTH, expand=1)

        db = connect_db()
        cur = db.cursor()
        cur.execute("SELECT name, quantity FROM products WHERE quantity <= 5")
        for row in cur.fetchall():
            stock_table.insert("", END, values=row)
        db.close()


# Run Code
if __name__ == "__main__":
    root = Tk()
    app = InventoryApp(root)
    root.mainloop()
