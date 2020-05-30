import main_functionality
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mb

def select_file():
    global file_path_text
    global file_path

    # Tk().withdraw()
    file_path_text = askopenfilename()
    file_path.set(file_path_text)

def call_backend():
    global file_path_text
    result = main_functionality.start_processing(file_path_text)
    answer = mb.showinfo(title="Резульати аналізу", message=result)


root = Tk()
root.title("КП 6.4 - Глушко Б.С.")
root.geometry("300x200")

file_path_text = "Очікую вводу..."
file_path = StringVar()
file_path.set(file_path_text)

message_entry = Entry(textvariable=file_path)
message_entry.place(relx=.5, rely=.1, anchor="c")
 
message_button = Button(text="Обрати файл", command=select_file)
message_button.place(relx=.5, rely=.5, anchor="c")

message_button = Button(text="Почати аналіз", command=call_backend)
message_button.place(relx=.5, rely=.7, anchor="c")

root.mainloop()