import jwt
from wantus.settings import ALGORITHM,SECRET_KEY
from users.models    import User
from django.http import JsonResponse


def access_token_check(func):
    def wrapper(self,request,*args,**kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, SECRET_KEY,ALGORITHM)
            
            request.user = User.objects.get(id = payload['id'])

            return func(self,request,*args,**kwargs)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=40)
        
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message' : 'Expired_Signature'}, status=401)

        except jwt.DecodeError:
            return JsonResponse({'message' : 'invalid_payload'}, status=401)

        except jwt.InvalidSignatureError:
            return JsonResponse({'message' : 'invalid_signature'}, status=401)

    return wrapper