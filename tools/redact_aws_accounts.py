import os
import re
import sys

AWS_ACCOUNT_REGEX = re.compile(r'\b\d{12}\b')

def redact_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    new_content = AWS_ACCOUNT_REGEX.sub('[REDACTED_AWS_ACCOUNT]', content)
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(new_content)
        print(f'Redacted: {filepath}')

def scan_and_redact(path):
    for root, _, files in os.walk(path):
        for fname in files:
            if fname.endswith(('.js', '.ts', '.jsx', '.tsx', '.py', '.env', '.json', '.yaml', '.yml', '.md', '.txt')):
                redact_file(os.path.join(root, fname))

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    scan_and_redact(target_dir)
    print('Redaction complete.')