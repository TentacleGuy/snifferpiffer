import os
import subprocess
import sys

# Funktion zum Ausführen eines Shell-Kommandos
def run_command(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        sys.exit(f"Fehler beim Ausführen des Befehls: {command}")

# Prüfen, ob pip installiert ist
def ensure_pip():
    try:
        __import__('pip')
        print("pip ist bereits installiert.")
    except ImportError:
        print("pip ist nicht installiert. Installation wird gestartet...")
        run_command(f"{sys.executable} -m ensurepip --upgrade")
        run_command(f"{sys.executable} -m pip install --upgrade pip")

# Installiere die Bibliotheken aus requirements.txt
def install_requirements():
    if not os.path.exists("requirements.txt"):
        sys.exit("Die Datei 'requirements.txt' wurde nicht gefunden.")
    
    print("Installiere Abhängigkeiten aus requirements.txt...")
    run_command(f"{sys.executable} -m pip install -r requirements.txt")

if __name__ == "__main__":
    print("Prüfen auf pip...")
    ensure_pip()
    install_requirements()
    print("Alle Bibliotheken sind erfolgreich installiert.")
