import tkinter as tk
from tkinter import messagebox
import subprocess

class HostelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostel Administrator Portal (Python + C++)")
        self.root.geometry("550x550")
        self.root.configure(bg="#2D2D2D") # Dark Mode Aesthetic
        
        # 1. Start the C++ Backend Processing Engine Secretly
        try:
            self.process = subprocess.Popen(
                ["./main_backend"], 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True # Auto-convert bytes to string
            )
        except Exception as e:
            messagebox.showerror("System Error", "Could not run C++ backend! Did you compile it?\nError: " + str(e))
            self.root.destroy()
            return

        # UI Styling Tokens
        bg_col = "#2D2D2D"
        fg_col = "#FFFFFF"
        field_font = ("Helvetica", 14)
        
        tk.Label(root, text="HOSTEL DASHBOARD", font=("Helvetica", 18, "bold"), bg=bg_col, fg="#4DA6FF").pack(pady=15)
        
        # INPUT FRAME
        frame = tk.Frame(root, bg=bg_col)
        frame.pack(pady=5)
        
        tk.Label(frame, text="Register No:", font=field_font, bg=bg_col, fg=fg_col).grid(row=0, column=0, padx=10, pady=10)
        self.reg_entry = tk.Entry(frame, font=field_font, width=15)
        self.reg_entry.grid(row=0, column=1, padx=10)
        self.reg_entry.insert(0, "25XYZ9861") # Default value
        
        tk.Label(frame, text="Time (e.g. 14.5):", font=field_font, bg=bg_col, fg=fg_col).grid(row=1, column=0, padx=10, pady=10)
        self.time_entry = tk.Entry(frame, font=field_font, width=15)
        self.time_entry.grid(row=1, column=1, padx=10)
        self.time_entry.insert(0, "10.0")

        # BUTTTONS FRAME
        btn_frame = tk.Frame(root, bg=bg_col)
        btn_frame.pack(pady=15)
        
        btn_checkout = tk.Button(btn_frame, text="CHECK OUT", font=field_font, width=10, bg="#E63946", fg="black", command=self.do_checkout)
        btn_checkin = tk.Button(btn_frame, text="CHECK IN", font=field_font, width=10, bg="#2A9D8F", fg="black", command=self.do_checkin)
        
        btn_checkout.grid(row=0, column=0, padx=10)
        btn_checkin.grid(row=0, column=1, padx=10)
        
        # ADVANCED COMMANDS FRAME
        tk.Button(root, text="View Violation History (Queue View)", width=35, command=lambda: self.do_cmd("HISTORY\n")).pack(pady=5)
        tk.Button(root, text="Show Highest Violators (Max Heap View)", width=35, command=lambda: self.do_cmd("TOP\n")).pack(pady=5)

        # TERMINAL LOG OUTPUT
        self.log_text = tk.Text(root, height=10, width=60, font=("Courier", 11), bg="#1E1E1E", fg="#00FF00")
        self.log_text.pack(pady=15)
        self.log_text.insert(tk.END, ">>> System initialized successfully.\n")
        
        # Cleanup when closing window
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # Core logic to talk to internal C++ Engine
    def talk_to_cpp(self, command_str):
        self.process.stdin.write(command_str)
        self.process.stdin.flush()
        
        output = []
        while True:
            line = self.process.stdout.readline()
            if not line or "END_RESPONSE" in line:
                break
            output.append(line.strip())
            
        return "\n".join(output)

    # Wrapper Functions for GUI Buttons
    def do_checkout(self):
        reg = self.reg_entry.get()
        time = self.time_entry.get()
        res = self.talk_to_cpp(f"CHECKOUT {reg} {time}\n")
        self.print_log(res)

    def do_checkin(self):
        reg = self.reg_entry.get()
        time = self.time_entry.get()
        res = self.talk_to_cpp(f"CHECKIN {reg} {time}\n")
        self.print_log(res)
        
    def do_cmd(self, cmd):
        res = self.talk_to_cpp(cmd)
        self.print_log(res)

    def print_log(self, text):
        self.log_text.insert(tk.END, "\n" + text)
        self.log_text.see(tk.END) # Scroll to bottom automatically

    def on_close(self):
        try:
            self.process.stdin.write("EXIT\n")
            self.process.stdin.flush()
        except: pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HostelApp(root)
    root.mainloop()
