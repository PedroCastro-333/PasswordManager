import random
import string
import hashlib
import os

class Senha:
    def __init__(self):
        pass

    @staticmethod
    def gerar_senha(tamanho: int = 12) -> str:
        """
        Gera uma senha aleatória com caracteres e números.

        Args:
            tamanho (int): O tamanho da senha a ser gerada. O padrão é 12.

        Returns:
            str: A senha gerada.
        """
        if tamanho == "":
            tamanho=12
        else:
            tamanho = int(tamanho)

        caracteres = string.ascii_letters + string.digits + string.punctuation

        senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
        return senha
    
    @staticmethod
    def __gerar_salt(tamanho=16) -> bytes:
        """
        Gera um salt aleatório.

        Args:
            tamanho (int): O tamanho do salt a ser gerado.

        Returns:
            bytes: O salt gerado.
        """
        return os.urandom(tamanho)
    
    @staticmethod
    def gerar_hash(senha: str, salt: bytes = None) -> tuple:
        """
        Gera um hash para a senha fornecida.

        Args:
            senha (str): A senha a ser hashada.
            salt (bytes): O salt a ser usado na geração do hash (opcional).

        Returns:
            tuple: Uma tupla contendo o salt e o hash gerado.
        """
        if salt is None:
            salt = Senha.__gerar_salt()
        senha_salgada = senha.encode('utf-8') + salt
        hash_obj = hashlib.sha256(senha_salgada)
        hash_hex = hash_obj.hexdigest()
        return salt, hash_hex