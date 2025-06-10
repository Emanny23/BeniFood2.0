import streamlit_authenticator as stauth

# this is to create a hashed password for your first admin user
passwords_to_hash = ["your_secret_password"] 

hashed_passwords = stauth.Hasher(passwords_to_hash).generate()
print(hashed_passwords)