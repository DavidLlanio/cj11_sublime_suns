# Python Discord Code Jam - Sublime Suns

## Local Setup

> This project built using `Python 3.12.x`

### Token

Create a discord application and get token from the [Discord Developer Portal](https://discord.com/developers/applications) and add it to the `.env` file. Refer to the `.env.example` file for the format.

### Virutal Environment

Clone this repo and open the folder, then run the below to commands in the terminal to create a virtual environment.

```bash
#windows
py -m venv venv

#linux
python3 -m venv venv
```

Activate virutal environment

```bash
.\venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements-dev.txt
```

### Run the application

```bash
# Windows
py main.py

# Linux
python3 main.py
```
