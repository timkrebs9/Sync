from cryptography.fernet import Fernet
from app.core.config import settings

class EncryptionService:
    def __init__(self):
        self.fernet = Fernet(settings.ENCRYPTION_KEY.encode())

    def encrypt_content(self, content: str) -> str:
        return self.fernet.encrypt(content.encode()).decode()

    def decrypt_content(self, encrypted_content: str) -> str:
        return self.fernet.decrypt(encrypted_content.encode()).decode()

encryption_service = EncryptionService() 