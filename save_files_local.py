import os
import json
from cryptography.fernet import Fernet
from config import AppConfig

class SaveInvoiceLocally:

    def __init__(self) -> None:
        self.local_dir = os.path.join(os.getcwd(), "invoices")
        self.file_path = os.path.join(self.local_dir, "invoice.ndjson")
        AppConfig().set_invoice_path(self.file_path)

        # Encryption key (base64-encoded 32 bytes)
        self.key = b'gqgFgFFhZIdikVEV1rfR8XKhkeA-v5r17YRDc7fFHh8='
        self.cipher = Fernet(self.key)

        if not os.path.exists(self.local_dir):
            os.makedirs(self.local_dir)
            with open(self.file_path, "a+") as f:
                pass

    def __call__(self, invoice: dict) -> None:
        encrypted_invoice = self.encrypt_data(json.dumps(invoice))
        
        with open(self.file_path, 'r') as f:
            lines = f.readlines()

        if len(lines) >= 30:
            del lines[29]

        with open(self.file_path, "a+") as f:
            f.write(encrypted_invoice + "\n")

    def encrypt_data(self, data: str) -> str:
        """Encrypt data."""
        encrypted_data = self.cipher.encrypt(data.encode())
        return encrypted_data.decode()

    def decrypt_data(self, data: str) -> str:
        """Decrypt data."""
        decrypted_data = self.cipher.decrypt(data.encode())
        return decrypted_data.decode()
