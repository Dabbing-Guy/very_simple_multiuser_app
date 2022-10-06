try:
    import curses
except ImportError:
    print("This program requires the curses module")
    print("Please install it with 'pip install windows-curses' on Windows")
    exit(1)
from typing import NoReturn
import requests

url: str = "http://very-simple-multiuser-app-api.tk/"

def clean_exit(us: dict, exception: Exception = None) -> NoReturn:
    requests.delete(url + "users", json={"user_id": us["user_id"], "user_password": us["user_password"]}).raise_for_status()
    if exception is not None:
        raise exception
    exit(0)

def main(stdscr: curses.window):
    curses.echo()
    curses.curs_set(1)
    stdscr.keypad(True)
    stdscr.addstr(0, 0, "Welcome to the chat!")
    stdscr.addstr(1, 0, "Please enter your nickname: ")
    nickname: str = stdscr.getstr(1, 28).decode("utf-8")
    messagescr = curses.newpad(curses.LINES - 3, curses.COLS - 1)

    # Register with the server
    response = requests.post(url + "users", json={"user_nickname": nickname, "message": "joined the chat"})
    response.raise_for_status()
    us: dict = response.json()

    # Set some variables
    messagescr_y: int = 0
    messagescr_x: int = 0
    message: str = ""

    curses.halfdelay(10)
    try: 
        # Main Loop
        while True:
            # Get new messages from server
            response = requests.get(url + "users")
            response.raise_for_status()
            all_users: list[dict] = response.json()["users"]

            # Display messages
            messagescr.clear()
            messagescr.resize(len(all_users) + 1, curses.COLS - 1)
            messagescr.move(0, 0)
            for user in all_users:
                messagescr.addstr(f"{user['user_nickname']}: {user['message']}\n")
            messagescr.refresh(messagescr_y, messagescr_x, 0, 0, curses.LINES - 2, curses.COLS - 1)

            # Get new message from user
            stdscr.addstr(curses.LINES - 1, 0, ">" + " " * (curses.COLS - 2))
            stdscr.addstr(curses.LINES - 1, 2, message)
            stdscr.move(curses.LINES - 1, len(message) + 2)
            next_ch = stdscr.getch()
            if next_ch == curses.KEY_RESIZE: continue
            if next_ch == curses.ERR: continue
            if next_ch == curses.KEY_UP:
                if messagescr_y == 0: continue
                messagescr_y -= 1
                continue
            if next_ch == curses.KEY_DOWN:
                if messagescr_y == len(all_users) - (curses.LINES - 1): continue
                messagescr_y += 1
                continue
            if next_ch == curses.KEY_BACKSPACE or next_ch == 127:
                message = message[:-1]
                continue
            if next_ch == ord("\n") or next_ch == curses.KEY_ENTER:
                if message == "exit":
                    clean_exit(us)
                # Send message to server
                requests.patch(url + f"message/{us['user_id']}", json={"message": message, "user_password": us["user_password"]}).raise_for_status()
                # Clear message input area
                stdscr.addstr(curses.LINES - 1, 0, ">" + " " * (curses.COLS - 2))
                message = ""
                continue
            message = message + chr(next_ch)
            
    except Exception as e:
        clean_exit(us, e)

if __name__ == "__main__":
    curses.wrapper(main)