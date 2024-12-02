#!/user/bin/env bash
# Exit on error

set -o errexit

pip install -r requirements.txt

python managy.py makemigrations
python managy.py migrate
