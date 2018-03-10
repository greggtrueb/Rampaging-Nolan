

def notepad_test():
    import pywinauto
    import subprocess
    import time
    import psutil

    proc = subprocess.Popen(['Notepad.exe'])
    pid = proc.pid

    app = pywinauto.application.Application()
    app.connect(process=pid)
    window = app['UntitledNotepad']
    window.type_keys("Simple Start Text")
    window.menu_select("File -> Save")
    time.sleep(.5)

    save_window = app['SaveAs']
    save_window['Edit'].select().SetEditText("Testing.txt")
    save_window.Save.Click()

    count = 3
    time.sleep(1)
    while count > 0:
        count = count - 1
        try:
            overwrite_window = app['ConfirmSaveAs']
            overwrite_window['Yes'].Click()
            count = -1
        except IndexError:
            time.sleep(.5)

    window = app['Testing.txt']
    window.type_keys("This is after the save")
    window.menu_select("File -> Save")

    app.kill()


if __name__ == "__main__":
    notepad_test()
