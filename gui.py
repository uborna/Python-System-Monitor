
import tkinter as tk
import cairosvg
from io import BytesIO
from PIL import Image, ImageTk
from engine import SystemMonitor


class PyMonGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyMon - System Monitor")
        self.geometry("900x650")
        self.minsize(760, 580)
        self.dark_mode = True
        self.monitor = SystemMonitor()

        self.themes = {
            "dark": {"bg": "#1e1e2e", "card": "#313244", "fg": "#ffffff", "secondary": "#a6adc8", "border": "#45475a", "button": "#45475a", "active": "#585b70", "accent": "#89b4fa"},
            "light": {"bg": "#eff1f5", "card": "#ffffff", "fg": "#4c4f69", "secondary": "#6c6f85", "border": "#ccd0da", "button": "#ccd0da", "active": "#bcc0cc", "accent": "#1e66f5"}
        }

        png_data = cairosvg.svg2png(url="./src/icons/moon.svg", output_width=24, output_height=24)
        self.theme_icon = ImageTk.PhotoImage(Image.open(BytesIO(png_data)))

        self.create_widgets()
        self.apply_theme()
        self.update_info()

    def create_card(self, parent, title, value, subtitle):
        theme = self.themes["dark"]
        card = tk.Frame(parent, bg=theme["card"], highlightbackground=theme["border"], highlightthickness=1, bd=0)
        tk.Label(card, text=title, bg=theme["card"], fg=theme["secondary"], font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=(12, 4))
        value_label = tk.Label(card, text=value, bg=theme["card"], fg=theme["accent"], font=("Arial", 24, "bold"))
        value_label.pack(anchor="w", padx=15, pady=4)
        sub_label = tk.Label(card, text=subtitle, bg=theme["card"], fg=theme["secondary"], font=("Arial", 10))
        sub_label.pack(anchor="w", padx=15, pady=(3, 12))
        return card, value_label, sub_label

    def create_widgets(self):
        theme = self.themes["dark"]
        self.configure(bg=theme["bg"])
        self.grid_columnconfigure(0, weight=1)

        self.header = tk.Frame(self, bg=theme["bg"])
        self.header.grid(row=0, column=0, sticky="ew", padx=24, pady=20)
        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = tk.Label(self.header, text="PyMon", bg=theme["bg"], fg=theme["fg"], font=("Arial", 25, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.subtitle_label = tk.Label(self.header, text="SYSTEM MONITOR", bg=theme["bg"], fg=theme["secondary"], font=("Arial", 9, "bold"))
        self.subtitle_label.grid(row=1, column=0, sticky="w")

        self.theme_button = tk.Button(self.header, image=self.theme_icon, command=self.toggle_theme, relief="flat", bd=0, padx=8, pady=8, cursor="hand2")
        self.theme_button.grid(row=0, column=1, rowspan=2)

        self.overview = tk.Label(self, text="Performance Overview", bg=theme["bg"], fg=theme["fg"], font=("Arial", 16, "bold"), anchor="w")
        self.overview.grid(row=1, column=0, sticky="ew", padx=24, pady=10)

        self.cards = tk.Frame(self, bg=theme["bg"])
        self.cards.grid(row=2, column=0, sticky="ew", padx=24)
        self.cards.grid_columnconfigure((0, 1), weight=1, uniform="cards")

        self.cpu_card, self.cpu_label, self.cpu_sub = self.create_card(self.cards, "CPU USAGE", "0%", "Processor usage")
        self.cpu_card.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.ram_card, self.ram_label, self.ram_sub = self.create_card(self.cards, "RAM USAGE", "0%", "Used: 0 GB")
        self.ram_card.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        self.resources_title = tk.Label(self, text="System Resources", bg=theme["bg"], fg=theme["fg"], font=("Arial", 16, "bold"), anchor="w")
        self.resources_title.grid(row=3, column=0, sticky="ew", padx=24, pady=(20, 10))

        self.resources = tk.Frame(self, bg=theme["bg"])
        self.resources.grid(row=4, column=0, sticky="ew", padx=24)
        self.resources.grid_columnconfigure((0, 1, 2), weight=1, uniform="resources")

        self.disk_card, self.disk_label, self.disk_sub = self.create_card(self.resources, "DISK", "0%", "Disk usage")
        self.disk_card.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.net_card, self.net_label, self.net_sub = self.create_card(self.resources, "NETWORK", "0 KB/s", "Download + upload")
        self.net_card.grid(row=0, column=1, sticky="ew", padx=6)

        self.battery_card, self.battery_label, self.battery_sub = self.create_card(self.resources, "BATTERY", "N/A", "Battery status")
        self.battery_card.grid(row=0, column=2, sticky="ew", padx=(6, 0))

        self.system_card = tk.Frame(self, bg=theme["card"], highlightbackground=theme["border"], highlightthickness=1, bd=0)
        self.system_card.grid(row=5, column=0, sticky="ew", padx=24, pady=20)

        self.os_label = tk.Label(self.system_card, text="OS: --", bg=theme["card"], fg=theme["secondary"], font=("Arial", 10))
        self.os_label.pack(anchor="w", padx=15, pady=(12, 4))

        self.pc_label = tk.Label(self.system_card, text="Computer: --", bg=theme["card"], fg=theme["secondary"], font=("Arial", 10))
        self.pc_label.pack(anchor="w", padx=15, pady=4)

        self.processor_label = tk.Label(self.system_card, text="Processor: --", bg=theme["card"], fg=theme["secondary"], font=("Arial", 10))
        self.processor_label.pack(anchor="w", padx=15, pady=4)

        self.status_label = tk.Label(self.system_card, text="Monitoring is running", bg=theme["card"], fg=theme["fg"], font=("Arial", 10))
        self.status_label.pack(anchor="w", padx=15, pady=(4, 12))

    def update_info(self):
        try:
            self.cpu_label.config(text=f"{self.monitor.get_cpu_usage()}%")
            self.ram_label.config(text=f"{self.monitor.get_memory_usage_percentage()}%")
            self.ram_sub.config(text=f"Used: {self.monitor.get_memory_used()} GB")

            self.disk_label.config(text=f"{self.monitor.get_disk_usage()}%")
            self.disk_sub.config(text=f"{self.monitor.get_disk_used()} GB used")

            self.net_label.config(text=f"{self.monitor.get_network_speed()} KB/s")

            battery, status = self.monitor.get_battery()
            self.battery_label.config(text=f"{battery}%" if battery is not None else "N/A")
            self.battery_sub.config(text=status)

            info = self.monitor.user_system()
            self.os_label.config(text=f"OS: {info['OS']}")
            self.pc_label.config(text=f"Computer: {info['OS_Type']}")
            self.processor_label.config(text=f"Processor: {info['Processor']}")

        except Exception as error:
            print(f"Monitoring error: {error}")

        self.after(1000, self.update_info)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes["dark" if self.dark_mode else "light"]
        self.configure(bg=theme["bg"])

        cards = (self.cpu_card, self.ram_card, self.disk_card, self.net_card, self.battery_card, self.system_card)
        card_labels = (self.os_label, self.pc_label, self.processor_label, self.status_label)

        def update(widget):
            if isinstance(widget, tk.Frame):
                is_card = widget in cards
                widget.configure(bg=theme["card"] if is_card else theme["bg"])
                if is_card:
                    widget.configure(highlightbackground=theme["border"])

            elif isinstance(widget, tk.Label):
                is_card = widget.master in cards
                widget.configure(bg=theme["card"] if is_card else theme["bg"], fg=theme["fg"])

            elif isinstance(widget, tk.Button):
                widget.configure(bg=theme["button"], fg=theme["fg"], activebackground=theme["active"], activeforeground=theme["fg"], relief="flat", bd=0)

            for child in widget.winfo_children():
                update(child)

        update(self)

        self.title_label.configure(fg=theme["fg"])
        self.subtitle_label.configure(fg=theme["secondary"])
        self.overview.configure(fg=theme["fg"])
        self.resources_title.configure(fg=theme["fg"])

        for card in cards[:-1]:
            labels = card.winfo_children()
            labels[0].configure(fg=theme["secondary"])
            labels[1].configure(fg=theme["accent"])
            labels[2].configure(fg=theme["secondary"])

        for label in card_labels:
            label.configure(bg=theme["card"], fg=theme["secondary"] if label != self.status_label else theme["fg"])


if __name__ == "__main__":
    app = PyMonGUI()
    app.mainloop()
