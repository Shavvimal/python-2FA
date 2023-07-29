import jwt 

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0c2RmIiwiZXhwIjoxNjYyOTk4NzcwLCJpYXQiOjE2NjI5OTE1NzAsInRpbWVfaXNzdWVkIjoiMTIvMDkvMjAyMiAxNDowNjoxMCJ9.1tWna2Xc4Itbnj8gA-NYi5ZyI2cI1FDjo05xky-qYgE'

header_data = jwt.get_unverified_header(token)

payload = jwt.decode(
    token,
    key='nduk-jwt-secret-2022-!!-TAPPM',
    algorithms=[header_data['alg'], ]
)

print(payload)