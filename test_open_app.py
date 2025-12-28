import os

def main():
    app_path1 = "taskmgr.exe"

    app_path2 = r"C:\Users\KIIT\OneDrive\Desktop\Gmail.lnk"

    os.startfile(app_path2)

    print(f"Openning application: {app_path2} ...")


if __name__ == "__main__":
    main()