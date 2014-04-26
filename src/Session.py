import pickle
import base64
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto import Random

COOKIE_NAME = "auth"
AES_SECRET = b"0" * 32 # SENSITIVE
HMAC_SECRET = b"0" * 32 # SENSITIVE


def _EncryptAndSign(data):
  plaintext = pickle.dumps(data)
  iv = Random.new().read(AES.block_size)
  ciphertext = AES.new(AES_SECRET, AES.MODE_CFB, iv).encrypt(plaintext)
  value = base64.b64encode(iv + ciphertext)
  signature = HMAC.new(HMAC_SECRET, value, SHA256).hexdigest()
  return value + signature


def _CheckSignatureAndDecrypt(data):
  value = data[:-64]
  signature = data[-64:]
  expected_signature = HMAC.new(HMAC_SECRET, value, SHA256).hexdigest()
  if expected_signature != signature:
    print("signatures don't match: expected %s, got %s", expected_signature, signature)
    return {}
  value = base64.b64decode(value)
  iv, ciphertext = value[:AES.block_size], value[AES.block_size:]
  plaintext = AES.new(AES_SECRET, AES.MODE_CFB, iv).decrypt(ciphertext)
  return pickle.loads(plaintext)


class Session(object):
  def __init__(self, requestHandler):
    self._handler = requestHandler
    self._data = {}
    if self._handler.request.cookies.get(COOKIE_NAME):
      self._data = _CheckSignatureAndDecrypt(self._handler.request.cookies.get(COOKIE_NAME))

  def __getitem__(self, item):
    if not item in self._data:
      return None
    return self._data[item]

  def __setitem__(self, item, value):
    self._data[item] = value

  def save(self):
    self._handler.response.set_cookie(
      COOKIE_NAME, value=_EncryptAndSign(self._data), max_age=30*86400, path="/", httponly=True, overwrite=True)
