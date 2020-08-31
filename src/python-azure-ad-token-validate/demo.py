import os
import sys
import jwt
from aadtoken import get_public_key

client_id = os.environ.get('CLIENT_ID', '<your-webapp-id-goes-here>')
tenant_id = os.environ.get('TENANT_ID', '<your-tenant-id-goes-here>')
if len(sys.argv) > 1:
    token = sys.argv[1]
else:
    token = os.environ.get('TOKEN', "<your-token-goes-here>")

issuer = 'https://sts.windows.net/{tenant_id}/'.format(tenant_id=tenant_id)


public_key = get_public_key(token)
decoded = jwt.decode(token,
                     public_key,
                     verify=True,
                     algorithms=['RS256'],
                     audience=[client_id],
                     issuer=issuer)
print(decoded)
