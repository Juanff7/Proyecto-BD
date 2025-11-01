from jose import jwt

SECRET_KEY = "super_clave_secreta_123"  # la misma de security.py
ALGORITHM = "HS256"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzYwMDI5OTYxfQ.nIlQe2wy81tKcq3YTWQvcVoWjkCgFlJXRN2BnvGP4UI"

payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
print(payload)
