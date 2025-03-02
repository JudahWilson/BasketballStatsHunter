'''
MAC ONLY: brew install python-tk
pip install pyinstaller tkhtmlview
'''
import tkinter as tk
from tkinter import ttk, Tk
# from ttkthemes import ThemedTk
import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkhtmlview import HTMLLabel

def dummy_event_handler(*args):
    print("Dummy event handler")


root = Tk() 
'''
THEMES = ['classic', 'breeze', 'scidmint', 'elegance', 'clearlooks', 'xpnative', 'default', 'adapta', 'plastik', 'arc', 'winnative', 'alt', 'scidgreen', 'clam', 'black', 'scidpurple', 'blue', 'smog', 'scidgrey', 'kroc', 'equilux', 'scidblue', 'scidpink', 'scidsand', 'ubuntu', 'radiance', 'winxpblue', 'aquativo', 'vista', 'itft1', 'yaru', 'keramik']
'''
root.title("StatBucket Admin")

# Create a tabbed notebook interface
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")

# region Tab basic
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Per-game Stats')
ttk.Label(tab1, text='Text Input:').grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
ttk.Entry(tab1).grid(row=0, column=1, padx=10, pady=5)

ttk.Label(tab1, text='Password:').grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
ttk.Entry(tab1, show='*').grid(row=1, column=1, padx=10, pady=5)

ttk.Label(tab1, text='Check:').grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
ttk.Checkbutton(tab1).grid(row=0, column=3, padx=10, pady=5)

ttk.Label(tab1, text='Radio:').grid(row=1, column=2, sticky=tk.W, padx=10, pady=5)
r_var = tk.IntVar()
ttk.Radiobutton(tab1, text="Option 1", variable=r_var, value=1).grid(row=1, column=3, sticky=tk.W, padx=10, pady=5)
ttk.Radiobutton(tab1, text="Option 2", variable=r_var, value=2).grid(row=2, column=3, sticky=tk.W, padx=10, pady=5)

btn = ttk.Button(tab1, text="Click Me!", command=dummy_event_handler)
btn.grid(row=4, column=0, columnspan=2, pady=20)
#endregion

# region Tab advanced inputs
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Advanced')
ttk.Label(tab2, text='ComboBox:').grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
combo_values = ['Option 1', 'Option 2', 'Option 3']
combobox = ttk.Combobox(tab2, values=combo_values)
combobox.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(tab2, text='Spinbox:').grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
ttk.Spinbox(tab2, from_=1, to=10).grid(row=1, column=1, padx=10, pady=5)

ttk.Label(tab2, text='Slider:').grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
ttk.Scale(tab2, orient=tk.HORIZONTAL).grid(row=0, column=3, padx=10, pady=5)

ttk.Label(tab2, text='Text Area:').grid(row=1, column=2, sticky=tk.W, padx=10, pady=5)
text_area = tk.Text(tab2, height=3, width=20)
text_area.grid(row=1, column=3, padx=10, pady=5)

# "dynamic_entry" input until checkbox is checked
global check_var
check_var = tk.IntVar()
def toggle_entry_visibility(*args):
    # Check the value of the check_var. If it's 1 (checked), show the Entry; otherwise, hide it.
    if check_var.get() == 1:
        dynamic_entry.grid(row=2, column=3, padx=10, pady=5)
    else:
        dynamic_entry.grid_remove()
check_var.trace_add("write", toggle_entry_visibility)
checkbutton = ttk.Checkbutton(tab2, variable=check_var)
ttk.Label(tab2, text='Show/Hide an input..').grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
checkbutton.grid(row=2, column=2, padx=10, pady=5)

global dynamic_entry
dynamic_entry = ttk.Entry(tab2)
# Initially, the Entry is not visible.
#endregion

# region Tab HTML
tab5 = ttk.Frame(notebook)
notebook.add(tab5, text='HTML')
html_content = """
<h1 style="color: blue;">Hello, Tkinter!</h1>
<p>This is an <strong>HTMLLabel</strong> example in <span style="color: red;">Tkinter</span>.</p>
<ul>
    <li>Item 1</li>
    <li>Item 2</li>
</ul>
"""

html_label = HTMLLabel(tab5, html=html_content)
html_label.pack(padx=10, pady=10)
#endregion

root.mainloop()