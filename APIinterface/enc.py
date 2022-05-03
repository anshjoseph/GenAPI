import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class EncCustom:
    def __init__(self,key:str)->None:
        self.backend = default_backend()
        self.secret_key = base64.b64decode(
            # generated randomly once, kept secret
            "7Y/Ycbyw407VkBBKh7veNkpk9uBHg+h4YT+PTkcIcY8="
            # key
        )


    def fix_binary_data_length(self,binary_data):
        """
        Right padding of binary data with 0 bytes
        Fix "ValueError: The length of the provided data is not a multiple of the block length."
        """
        block_length = 16
        binary_data_length = len(binary_data)
        length_with_padding = (
            binary_data_length + (block_length - binary_data_length) % block_length
        )
        return binary_data.ljust(length_with_padding, "\0".encode()), binary_data_length


    def encrypt(self,binary_data):
        binary_data, binary_data_length = self.fix_binary_data_length(binary_data)
        iv = os.urandom(
            16
        )  # does not need to be secret, but must be unpredictable at encryption time

        # AES (Advanced Encryption Standard) is a block cipher standardized by NIST. AES is both fast, and cryptographically strong. It is a good default choice for encryption.
        # CBC (Cipher Block Chaining) is a mode of operation for block ciphers. It is considered cryptographically strong. (see https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.modes.CBC)
        cipher = Cipher(algorithms.AES(self.secret_key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(binary_data) + encryptor.finalize()
        stored_encrypted_data = "AES.MODE_CBC${iv}${binary_data_length}${encrypted_data})".format(
            iv=base64.b64encode(iv),
            binary_data_length=binary_data_length,
            encrypted_data=base64.b64encode(encrypted_data),
        )

        return stored_encrypted_data


    def decrypt(self,stored_encrypted_data):
        algorithm, iv, binary_data_length, encrypted_data = stored_encrypted_data.split("$")
        assert algorithm == "AES.MODE_CBC"
        iv = base64.b64decode(iv)
        encrypted_data = base64.b64decode(encrypted_data)
        binary_data_length = int(binary_data_length)
        cipher = Cipher(algorithms.AES(self.secret_key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        return decrypted_data[:binary_data_length]



class EncCustomNosec:


    def __init__(self,key):
        self.backend = default_backend()
        self.iterations = 100_000
        self.password = key
        self.salt = b'\xa8V\xa2^\xa2\xfe\xca\x03x?\xf3\x17\x8dY|A'

    def _derive_key(self,password: bytes) -> bytes:
        """Derive a secret key from a given password and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=self.salt,
            iterations= self.iterations, backend=self.backend
            )
        return b64e(kdf.derive(password))


    def password_encrypt(self,message: bytes) -> bytes:
        
        key = self._derive_key(self.password.encode())
        return b64e(
            b'%b%b%b' % (
                self.salt,
                self.iterations.to_bytes(4, 'big'),
                b64d(Fernet(key).encrypt(message)),
            )
        )

    def password_decrypt(self,token: bytes) -> bytes:
        decoded = b64d(token)
        iter, token =  decoded[16:20], b64e(decoded[20:])
        iterations = int.from_bytes(iter, 'big')
        key = self._derive_key(self.password.encode())
        return Fernet(self.key).decrypt(token)


class EncBase64withPass:
    def __init__(self,password:str):
        self.key = password
    def encode(self,clear):
        enc = []
        for i in range(len(clear)):
            key_c = self.key[i % len(self.key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()

    def decode(self,enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = self.key[i % len(self.key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)