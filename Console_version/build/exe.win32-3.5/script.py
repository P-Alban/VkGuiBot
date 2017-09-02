def load_file():
    with open(r'C:\Users\user\Desktop\1.exe', 'rb') as file:
        var = file.read()
        return var
with open(r'C:\Users\user\Desktop\test\new_file_e.exe', 'wb') as file_2:
    file_2.write(load_file())