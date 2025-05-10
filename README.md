# Auto SSH Config Generator

This Python tool helps you manage multiple GitHub accounts by automatically generating and configuring SSH keys for each account.

## Features

- Generate SSH key pairs for multiple GitHub accounts
- Automatically configure SSH config file
- Support for different email addresses per account
- Secure key generation and management

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/auto-ssh-config.git
cd auto-ssh-config
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Create a configuration file named `config.yaml` with your GitHub accounts:
```yaml
accounts:
  - name: personal
    email: your.personal@email.com
    hostname: github.com
  - name: work
    email: your.work@email.com
    hostname: github.com
```

2. Run the script:
```bash
python ssh_key_manager.py
```

The script will:
- Generate SSH keys for each account
- Create or update your SSH config file
- Display the public keys to add to your GitHub accounts

## Security

- SSH keys are generated with 4096-bit RSA encryption
- Private keys are stored with appropriate permissions
- Each account uses a unique key pair

## License

MIT License 