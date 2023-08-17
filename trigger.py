from Alfred.mail import sendemail

def frequency_check(response, value):
  str_list = response.split()
  # create an empty dictionary
  frequency = {}
  frequency.setdefault(value, 0)
  # count frequency of each word
  for word in str_list:
      frequency[word] = frequency.setdefault(word, 0) + 1
  
  return frequency[value]
  
def get_alarm_reminder_details(response):
  print(response)
  Time = response.split("Time:")[1].split("Label:")[0]
  Time = Time.replace("\n", "")
  
  Label = response.split("Label: ")[1].split("Days:")[0]
  Label = Label.replace("\n", "")

  days_to_remind = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
  days_in_string = response.split("Days:")[1].lower()
  Days = []
  for i in days_to_remind:
    if i.lower() in days_in_string:
      Days.append(i)

  reminder_details = {
      "time": Time,
      "label": Label,
      "days": Days
  }

  return reminder_details

def get_sms_details(response):
  To = response.split("To:")[1].split("Text:")[0]
  Text = response.split("Text:")[1]
  To = To.replace("\n", "")

  sms_details = {
    "to": To,
    "content": Text
  }

  return sms_details

def get_email_details(response):
  To = response.split("To:")[1].split("Subject:")[0]
  Subject = response.split("Subject:")[1].split("Text:")[0]
  Text = response.split("Text:")[1]
  To = To.replace("\n", "")
  Subject = Subject.replace("\n", "")

  email_details = {
    "to": To,
    "subject": Subject,
    "content": Text
  }

  return email_details

def set_reminder(response, email):
  reminder_details = get_alarm_reminder_details(response)
  print(reminder_details)
  Reminder = reminder_details["label"] + " at " + reminder_details["time"] + " on "
  for i in reminder_details['days']:
    Reminder += i + " "
  print(sendemail(str(Reminder), "Reminder", email, []))


def set_alarm(response, email):
  alarm_details = get_alarm_reminder_details(response)
  print(alarm_details)
  Alarm = alarm_details["label"] + " at " + alarm_details["time"] + " on "
  for i in alarm_details['days']:
    Alarm += i + " "
  print(sendemail(str(Alarm), "Reminder", email, []))

def send_sms(response):
  sms_details = get_sms_details(response)
  print(sms_details)

def send_email(response):
  email_details = get_email_details(response)
  print(email_details)
  print(sendemail(email_details['content'], email_details['subject'], email_details['to'], []))

def trigger(response, email):
  if frequency_check(response, "Reminder:") == 2:
    set_reminder(response.split("Reminder:")[1].split("Reminder:")[0], email)
  elif frequency_check(response, "Alarm:") == 2:
    set_alarm(response.split("Alarm:")[1].split("Alarm:")[0], email)
  elif frequency_check(response, "SMS:") == 2:
    send_sms(response.split("SMS:")[1].split("SMS:")[0])
  elif frequency_check(response, "Email:") == 2:
    send_email(response.split("Email:")[1].split("Email:")[0])