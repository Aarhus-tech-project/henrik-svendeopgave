import os
import base64

new_key = base64.urlsafe_b64encode(os.urandom(32))
print('your_field_encryption_key:', new_key)
