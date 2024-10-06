import os.path
import importlib.util
import os
import sys
import hashlib

def loadModule(folder, module_name):
    full_module_name = f"{folder}.{module_name}"
    try:
        # Add the directory containing the 'analyzer' module to sys.path
        sys.path.append(folder)

        # Attempt to import the module
        module_spec = importlib.util.find_spec(full_module_name)
        if module_spec is None:
            print(f"Module '{module_name}' not found")
            return None
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return getattr(module, module_name)
    except Exception as e:
        print(f"Error loading module '{module_name}': {e}")
        return None
    
def hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key

# Function to verify the password hash
def verify_password(stored_password, provided_password):
    salt = stored_password[:32]
    stored_key = stored_password[32:]
    key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return stored_key == key