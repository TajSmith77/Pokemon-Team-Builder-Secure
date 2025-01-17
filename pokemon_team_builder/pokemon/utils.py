from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_datetime

class ExpiringTokenGenerator(default_token_generator.__class__):
    def make_token(self, user):
        
        token = super().make_token(user) #Call the parent method to generate the token
        expiry_time = timezone.now() + timedelta(seconds=10)  # Set the token expiration time to 4 hours from now
        return f"{token}|{expiry_time.isoformat()}"
    
    def check_token(self, user, token):
        try:
            token_value, expiry_time_str = token.split("|") #Split the token and expiry time
            expiry_time = parse_datetime(expiry_time_str) #Parse the expiry time
            if timezone.now() > expiry_time: #Check if the token has expired
                return False  # Token has expired
            return super().check_token(user, token_value) 
        except (ValueError): #If the token value is invalid
            return False  # Invalid token