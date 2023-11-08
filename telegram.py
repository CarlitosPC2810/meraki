import pyrogram

import telethon

# Obtenga su ID de aplicación y hash de API de Telegram
api_id = 1234567890
api_hash = "12345678901234567890123456789012"

# Cree un cliente de Telegram
client = telethon.TelegramClient("my_session", api_id, api_hash)

# Conecte el cliente a Telegram
client.connect()

# Obtenga el ID de usuario del destinatario
user_id = 123456789

# Inicie la llamada telefónica
call = client.phone.requestCall(user_id)

# Compruebe el estado de la llamada
if call.is_successful():
    print("La llamada telefónica se inició correctamente")
else:
    print("La llamada telefónica no se pudo iniciar")