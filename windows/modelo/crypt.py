# https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives import serialization

def generar_claves():
    clave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    clave_publica = clave_privada.public_key()

    return (clave_privada, clave_publica)

def serializar_claves(clave_privada: RSAPrivateKey, clave_publica: RSAPublicKey) -> tuple[bytes, bytes]:
    private_pem = clave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = clave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem

    """ with open('private_key.pem', 'wb') as f:
        f.write(private_pem)

    with open('public_key.pem', 'wb') as f:
        f.write(public_pem) """

def encriptar_mensaje(clave_privada: RSAPrivateKey):
    raise NotImplementedError
    pass

def generar_id_aleatorio() -> str:
    c_privada, c_publica = generar_claves()
    c_privada, c_publica = serializar_claves(c_privada, c_publica)
    c_publica = c_publica.decode()
    return c_publica