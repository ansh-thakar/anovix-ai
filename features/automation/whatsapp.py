import pywhatkit

def send_whatsapp_message(country_code: str, number: str, message: str):
    phone = f"{country_code}{number}"
    pywhatkit.sendwhatmsg_instantly(
        phone_no=phone,
        message=message,
        wait_time=10,
        tab_close=True
    )
