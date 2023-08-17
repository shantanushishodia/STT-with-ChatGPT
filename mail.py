import smtplib

def sendemail(message, subject, to_addr_list, cc_addr_list=[]):
    # try:
    sender = "user.anuj4@gmail.com"
    print(to_addr_list)
    smtpserver='smtp.gmail.com:587'

    header  = 'From: %s\n' % sender
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(sender,"lfbabtofpqzrcche")
    problems = server.sendmail(sender, to_addr_list, message)
    server.quit()
    return True
    # except:
    #     return False