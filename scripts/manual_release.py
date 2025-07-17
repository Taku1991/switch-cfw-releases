#!/usr/bin/env python3
import os
import json
import datetime
import subprocess
import sys

def main():
    print("🚀 Starte manuelles Release...")
    
    # Hole aktuelle Versionen
    print("📋 Hole aktuelle Versionen...")
    result = subprocess.run([sys.executable, "scripts/check_releases.py"], 
                          capture_output=True, text=True, env=os.environ)
    
    if result.returncode != 0:
        print(f"❌ Fehler beim Abrufen der Versionen: {result.stderr}")
        return
    
    # Lade die Versionen aus der JSON-Datei
    try:
        with open('last_versions.json', 'r') as f:
            versions = json.load(f)
    except Exception as e:
        print(f"❌ Fehler beim Laden der Versionen: {e}")
        return
    
    print(f"📄 Geladene Versionen: {versions}")
    
    # Setze Environment-Variablen für das Release
    os.environ['CFW_VERSION'] = versions.get('cfw_version', 'unknown')
    os.environ['BOOTLOADER_VERSION'] = versions.get('bootloader_version', 'unknown')
    os.environ['SYSDVR_VERSION'] = versions.get('sysdvr_version', 'unknown')
    os.environ['LDN_MITM_VERSION'] = versions.get('ldn_mitm_version', 'unknown')
    os.environ['SYS_BOTBASE_VERSION'] = versions.get('sys_botbase_version', 'unknown')
    os.environ['FTPD_VERSION'] = versions.get('ftpd_version', 'unknown')
    os.environ['JKSV_VERSION'] = versions.get('jksv_version', 'unknown')
    
    # Erstelle Zeitstempel für Tag
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    os.environ['RELEASE_TAG'] = f"v{versions.get('cfw_version', 'unknown')}-{timestamp}"
    
    print(f"🏷️ Release Tag: {os.environ['RELEASE_TAG']}")
    
    # Erstelle das Release
    print("📦 Erstelle kombiniertes Release...")
    result = subprocess.run([sys.executable, "scripts/combine_releases.py"], 
                          env=os.environ)
    
    if result.returncode != 0:
        print("❌ Fehler beim Erstellen des kombinierten Releases")
        return
    
    print("🎯 Erstelle GitHub Release...")
    result = subprocess.run([sys.executable, "scripts/create_release.py"], 
                          env=os.environ)
    
    if result.returncode != 0:
        print("❌ Fehler beim Erstellen des GitHub Releases")
        return
    
    print("✅ Manuelles Release erfolgreich erstellt!")

if __name__ == "__main__":
    main() 