# Usage
## Windows

Powershell:
```powershell
python3 -m venv venv
./venv/Scripts/Activate.ps1
pip3 install -r requirements.txt
$env:FLASK_APP="pokedex"
$env:FLASK_ENV="development"
flask run
```

CMD:
```bat
python -m venv venv
./venv/Scripts/Activate.bat
pip3 install -r requirements.txt
$env:FLASK_APP="pokedex"
$env:FLASK_ENV="development"
flask run
```

## Unix

```bash
# With direnv
direnv allow
# Without direnv
source .envrc
pip3 install -r requirements.txt
flask run
```
