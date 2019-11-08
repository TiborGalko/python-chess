import tkinter as tk
from game import Application


def main():
    """ Main function """
    root = tk.Tk()
    root.geometry("800x600")
    root.resizable(0, 0)
    root.title("ABC")

    app = Application(0, 0, master=root)
    app.pack(side=tk.LEFT, anchor=tk.E)

    root.mainloop()


if __name__ == '__main__':
    main()
