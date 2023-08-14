CHATGPT_API_NAME: str = "gpt-3.5-turbo"
WHISPER_API_NAME: str = "whisper-1"

def get_msg():
    reader = open("./assests/CHATGPT_ROLE.txt","r")
    CHATGPT_ROLE = reader.read()
    messages = [{"role": "assistant", "content": CHATGPT_ROLE}]
    return messages