import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
from scipy.stats import binom
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sv_ttk
import darkdetect

class GoalProbabilitySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title('Goal Probability Simulator')
        self.root.geometry('900x800')
        self.dark_mode = (darkdetect.theme() == "Dark")
        sv_ttk.set_theme("dark" if self.dark_mode else "light")
        self.style = ttk.Style()

        self.create_widgets()
        self.setup_defaults()

    def create_widgets(self):
        # Toolbar
        bar = ttk.Frame(self.root)
        bar.pack(fill='x', padx=5, pady=5)
        self.dark_var = tk.BooleanVar(value=self.dark_mode)
        ttk.Checkbutton(bar, text="Dark Mode", variable=self.dark_var,
                        command=self.toggle_theme).pack(side='left')
        ttk.Button(bar, text="Export Chart", command=self.open_export_dialog).pack(side='right')

        # Input frame
        inp = ttk.Frame(self.root)
        inp.pack(fill='x', pady=10, padx=10)

        self.entries = {}
        self.scales = {}
        for i, (label, name, mn, mx, step) in enumerate([
            ("xG Total", 'xg', 0, 20, 0.1),
            ("Shots", 'shots', 1, 100, 1),
            ("Goals", 'goals', 0, 50, 1),
        ]):
            ttk.Label(inp, text=label).grid(row=i, column=0, sticky='e', padx=5, pady=5)
            var = tk.DoubleVar() if step<1 else tk.IntVar()
            scale = ttk.Scale(inp, from_=mn, to=mx, variable=var, command=lambda v,n=name: self.update_entry(n))
            scale.grid(row=i, column=1, sticky='ew')
            self.scales[name] = var

            ent = ttk.Entry(inp, width=6)
            ent.grid(row=i, column=2, padx=5)
            self.entries[name] = ent
            ent.bind('<FocusOut>', lambda e,name=name: self.update_scale(name))

        ttk.Label(inp, text="Player Name").grid(row=3,column=0, sticky='e', padx=5, pady=5)
        self.player_ent = ttk.Entry(inp)
        self.player_ent.grid(row=3, column=1, columnspan=2, sticky='we', padx=5)

        inp.columnconfigure(1, weight=1)

        ttk.Button(self.root, text="Analyze xG", command=self.analyze).pack(pady=5)

        self.chart_frame = ttk.Frame(self.root)
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.placeholder = ttk.Label(self.chart_frame, text="Analyze to see chart", anchor='center')
        self.placeholder.pack(expand=True)

    def setup_defaults(self):
        self.entries['xg'].insert(0, "5.0")
        self.entries['shots'].insert(0, "20")
        self.entries['goals'].insert(0, "3")
        self.player_ent.insert(0, "Player")

        self.scales['xg'].set(5.0)
        self.scales['shots'].set(20)
        self.scales['goals'].set(3)

    def update_entry(self, name):
        val = self.scales[name].get()
        self.entries[name].delete(0, 'end')
        self.entries[name].insert(0, f"{val:.1f}" if name=='xg' else str(int(val)))

    def update_scale(self, name):
        try:
            val = float(self.entries[name].get())
            self.scales[name].set(val)
        except:
            pass

    def toggle_theme(self):
        mode = "dark" if self.dark_var.get() else "light"
        sv_ttk.set_theme(mode)

    def analyze(self):
        for w in self.chart_frame.winfo_children(): w.destroy()
        try:
            player = self.player_ent.get().strip() or "Player"
            xg = float(self.entries['xg'].get())
            shots = int(self.entries['shots'].get())
            goals = int(self.entries['goals'].get())
            if xg<=0 or shots<=0 or goals<0: raise
        except:
            return messagebox.showerror("Error","Check your inputs")
        p = xg/shots
        maxg = min(int(xg)*2, shots) or shots
        xs = np.arange(maxg+1)
        probs = binom.pmf(xs, shots, p)
        cdf = np.cumsum(binom.pmf(np.arange(shots+1), shots, p))

        fig = Figure(figsize=(8,5), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(xs, probs, color=['red' if i==goals else 'gray' for i in xs])
        ax.plot(xs, probs, color='blue')
        ax.set_title(f"{player}\nProb ≥ {goals}: {(1-cdf[goals])*100:.2f}%")
        ax.set_xlabel("Goals"); ax.set_ylabel("Probability")
        ax.grid(True)
        fig.tight_layout()

        container = ttk.Frame(self.chart_frame, width=800, height=500)
        container.pack_propagate(False); container.pack()
        canvas = FigureCanvasTkAgg(fig, container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        self.current_fig = fig

    def open_export_dialog(self):
        if not hasattr(self, 'current_fig'):
            return messagebox.showinfo("Oops","Analyze first!")
        dlg = tk.Toplevel(self.root)
        dlg.title("Export Chart")
        dlg.geometry("300x150")
        ttk.Label(dlg, text="Filename:").pack(pady=5)
        fname = tk.StringVar(value="chart.png")
        ttk.Entry(dlg, textvariable=fname).pack(fill='x', padx=10)
        fmt = tk.StringVar(value="png")
        ttk.OptionMenu(dlg, fmt, "png", "png", "pdf").pack(pady=5)
        def do_export():
            path = filedialog.asksaveasfilename(defaultextension=f".{fmt.get()}",
                filetypes=[(fmt.get().upper(),f"*.{fmt.get()}")])
            if not path: return
            self.current_fig.savefig(path)
            messagebox.showinfo("Saved",f"Saved to {path}")
            dlg.destroy()
        ttk.Button(dlg, text="Export", command=do_export).pack(pady=10)

def main():
    root = tk.Tk()
    GoalProbabilitySimulator(root)
    root.mainloop()

if __name__=="__main__":
    main()
