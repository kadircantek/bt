from cryptography.fernet import Fernet
from app.config import settings
import base64
import os

# ENCRYPTION_KEY'in varlığını kontrol et, yoksa programı başlatma
if not settings.ENCRYPTION_KEY:
    # Development için otomatik key oluştur
    if settings.ENVIRONMENT == "DEVELOPMENT":
        settings.ENCRYPTION_KEY = base64.urlsafe_b64encode(os.urandom(32)).decode()
        print("⚠️  Development mode: Auto-generated encryption key")
    else:
        raise ValueError("ENCRYPTION_KEY ortam değişkeni ayarlanmamış. Lütfen .env dosyanızı kontrol edin.")

try:
    # Şifreleme anahtarını kullanarak Fernet nesnesini bir kere oluştur
    cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode())
except Exception as e:
    print(f"⚠️  Encryption key error: {e}")
    # Fallback: Basit encoding (production'da kullanılmamalı)
    cipher_suite = None

def encrypt_data(data: str) -> str:
    """
    Verilen metni (string) şifreler.
    Args:
        data (str): Şifrelenecek metin.
    Returns:
        str: Şifrelenmiş metin.
    """
    if not data:
        return ""
    
    if cipher_suite:
        encrypted_text = cipher_suite.encrypt(data.encode('utf-8'))
        return encrypted_text.decode('utf-8')
    else:
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')

def decrypt_data(encrypted_data: str) -> str:
    """
    Şifrelenmiş metni çözer.
    Args:
        encrypted_data (str): Çözülecek şifreli metin.
    Returns:
        str: Orjinal, çözülmüş metin.
    """
    if not encrypted_data:
        return ""
    try:
        if cipher_suite:
            decrypted_text = cipher_suite.decrypt(encrypted_data.encode('utf-8'))
            return decrypted_text.decode('utf-8')
        else:
            # Fallback decoding
            return base64.b64decode(encrypted_data.encode('utf-8')).decode('utf-8')
    except Exception as e:
        # Şifre çözme hatası durumunda (örneğin anahtar değiştiyse) boş string döndür
        print(f"Şifre çözme hatası: {e}")
        return ""

