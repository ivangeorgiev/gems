import logging
import functools
import base64
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import requests
import jwt

OID_DISCOVERY_COMMON_URL = 'https://login.microsoftonline.com/common/.well-known/openid-configuration'
OID_DISCOVERY_TENANT_URL = 'https://login.microsoftonline.com/{tenant_id}/.well-known/openid-configuration'

_jwks_cache = {}

class TokenError(Exception):
    pass

class CommunicationError(TokenError):
    pass

class InvalidToken(TokenError):
    pass



def ensure_bytes(key):
    if isinstance(key, str):
        key = key.encode('utf-8')
    return key


def decode_value(val):
    decoded = base64.urlsafe_b64decode(ensure_bytes(val) + b'==')
    return int.from_bytes(decoded, 'big')


def rsa_pem_from_jwk(jwk):
    return RSAPublicNumbers(
        n=decode_value(jwk['n']),
        e=decode_value(jwk['e'])
    ).public_key(default_backend()).public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def _fetch_discovery_meta(tenant_id=None):
    discovery_url = OID_DISCOVERY_TENANT_URL.format(tenant_id=tenant_id) if tenant_id else OID_DISCOVERY_COMMON_URL
    try:
        response = requests.get(discovery_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.debug(response.text)
        raise CommunicationError(f'Error getting issuer discovery meta from {discovery_url}', err)
    return response.json()

def get_kid(token):
    headers = jwt.get_unverified_header(token)
    if not headers:
        raise InvalidToken('missing headers')
    try:
        return headers['kid']
    except KeyError:
        raise InvalidToken('missing kid')

def get_jwks_uri(tenant_id=None):
    meta = _fetch_discovery_meta(tenant_id)
    if 'jwks_uri' in meta:
        return meta['jwks_uri']
    else:
        raise CommunicationError('jwks_uri not found in the issuer meta')

@functools.lru_cache
def get_jwks(tenant_id=None):
    jwks_uri= get_jwks_uri(tenant_id)
    try:
        response = requests.get(jwks_uri)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.debug(response.text)
        raise CommunicationError(f'Error getting issuer jwks from {jwks_uri}', err)
    return response.json()

def get_jwk(kid, tenant_id=None):
    for jwk in get_jwks(tenant_id).get('keys'):
        if jwk.get('kid') == kid:
            return jwk
    raise InvalidToken('Unknown kid')


def get_public_key(token, tenant_id=None):
    kid = get_kid(token)
    jwk = get_jwk(kid, tenant_id)
    return rsa_pem_from_jwk(jwk)

    return rsa_pem_from_jwk(get_jwk(get_kid(token)))

