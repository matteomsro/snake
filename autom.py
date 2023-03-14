from thefrenchsnake import *
import datetime

if __name__ == "__main__":
    i = 0
    while i < 100:
        p = snake()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("resultats.txt", "a") as f:
            f.write(f"{now} - p={p}\n")
        i += 1
