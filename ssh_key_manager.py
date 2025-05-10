#!/usr/bin/env python3

import os
import sys
import yaml
import stat
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

class SSHKeyManager:
    def __init__(self):
        self.ssh_dir = Path.home() / '.ssh'
        self.config_file = self.ssh_dir / 'config'
        self.ensure_ssh_directory()

    def ensure_ssh_directory(self):
        """Ensure the .ssh directory exists with correct permissions."""
        if not self.ssh_dir.exists():
            self.ssh_dir.mkdir(mode=0o700)
        else:
            # Ensure correct permissions on existing directory
            self.ssh_dir.chmod(0o700)

    def generate_key_pair(self, account_name, email):
        """Generate a new SSH key pair for the given account."""
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )

        # Get private key in PEM format
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Get public key in OpenSSH format
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        )

        # Save private key
        private_key_path = self.ssh_dir / f'id_rsa_{account_name}'
        with open(private_key_path, 'wb') as f:
            f.write(private_pem)
        os.chmod(private_key_path, 0o600)

        # Save public key
        public_key_path = self.ssh_dir / f'id_rsa_{account_name}.pub'
        with open(public_key_path, 'wb') as f:
            f.write(public_pem)
        os.chmod(public_key_path, 0o644)

        return public_key_path

    def update_ssh_config(self, accounts):
        """Update the SSH config file with the new account configurations."""
        config_lines = []
        
        for account in accounts:
            host_entry = f"""
Host github.com-{account['name']}
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_{account['name']}
    IdentitiesOnly yes
"""
            config_lines.append(host_entry)

        # Write the new config
        with open(self.config_file, 'w') as f:
            f.write(''.join(config_lines))
        os.chmod(self.config_file, 0o600)

    def process_accounts(self, config_path):
        """Process all accounts from the config file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Config file '{config_path}' not found.")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML config: {e}")
            sys.exit(1)

        if 'accounts' not in config:
            print("Error: No 'accounts' section found in config file.")
            sys.exit(1)

        for account in config['accounts']:
            if not all(k in account for k in ['name', 'email']):
                print(f"Error: Account configuration missing required fields: {account}")
                continue

            print(f"\nProcessing account: {account['name']}")
            public_key_path = self.generate_key_pair(account['name'], account['email'])
            
            print(f"Generated SSH key pair for {account['name']}")
            print("\nAdd this public key to your GitHub account:")
            with open(public_key_path, 'r') as f:
                print(f.read().strip())

        self.update_ssh_config(config['accounts'])
        print("\nSSH config has been updated successfully!")
        print("\nTo use different GitHub accounts, use these URLs for your repositories:")
        for account in config['accounts']:
            print(f"git@github.com-{account['name']}:username/repository.git")

def main():
    config_path = 'config.yaml'
    manager = SSHKeyManager()
    manager.process_accounts(config_path)

if __name__ == '__main__':
    main() 