#!/usr/bin/env python3
import os
import glob
from github import Github

def main():
    g = Github(os.environ['GITHUB_TOKEN'])
    
    repo_owner = os.environ.get('GITHUB_REPOSITORY_OWNER', 'dein-username')
    repo_name = os.environ.get('GITHUB_REPOSITORY', 'SysCFW_Update').split('/')[-1]
    
    try:
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
    except Exception as e:
        print(f"❌ Repository-Zugriff fehlgeschlagen: {e}")
        return
    
    release_tag = os.environ['RELEASE_TAG']
    cfw_version = os.environ['CFW_VERSION']
    bootloader_version = os.environ['BOOTLOADER_VERSION']
    sysdvr_version = os.environ['SYSDVR_VERSION']
    ldn_mitm_version = os.environ['LDN_MITM_VERSION']
    sys_botbase_version = os.environ['SYS_BOTBASE_VERSION']
    ftpd_version = os.environ['FTPD_VERSION']
    jksv_version = os.environ['JKSV_VERSION']
    changes = os.environ.get('CHANGES', '').replace('\\n', '\n')
    
    release_name = f"Pokemon SysBot CFW {cfw_version} - Complete Solution"
    
    # Release Notes laden oder generieren
    try:
        with open('release_notes.md', 'r', encoding='utf-8') as f:
            release_body = f.read()
    except FileNotFoundError:
        # Generiere Release Notes mit Änderungen
        changes_section = ""
        if changes:
            changes_section = f"""
## 🔄 Aktualisierungen in diesem Release
{changes}

"""
        
        release_body = f"""# 🎮 Pokemon SysBot CFW - Complete Solution

{changes_section}## 🔧 Enthaltene Komponenten
- **Atmosphère** {cfw_version} - Custom Firmware
- **Hekate** {bootloader_version} - Bootloader  
- **SysDVR** {sysdvr_version} - Video-Streaming
- **ldn_mitm** {ldn_mitm_version} - Online-Gaming
- **sys-botbase** {sys_botbase_version} - Pokemon-Bot-Framework
- **ftpd** {ftpd_version} - FTP-Server
- **JKSV** {jksv_version} - Save-Manager

## 📁 Installation
1. Backup der SD-Karte erstellen
2. ZIP-Inhalt auf SD-Karte entpacken
3. Payload injizieren (unpatched) oder mit Modchip booten

## 💬 Support
**Discord**: [discord.gg/pokemonhideout](https://discord.gg/pokemonhideout)

⚠️ **Warnung**: SysNAND-Konfiguration mit erhöhtem Ban-Risiko!

---
*🤖 Automatisch generiert am {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""
    
    try:
        # Prüfe ob Release bereits existiert (sollte nicht passieren mit Zeitstempel)
        try:
            existing_release = repo.get_release(release_tag)
            print(f"⚠️ Release {release_tag} existiert bereits, überspringe...")
            return
        except:
            pass  # Release existiert nicht, das ist gut
        
        # Erstelle neues Release
        release = repo.create_git_release(
            tag=release_tag,
            name=release_name,
            message=release_body,
            draft=False,
            prerelease=False
        )
        
        # Finde das kombinierte ZIP-File
        zip_files = glob.glob("Pokemon-SysBot-CFW-*-Complete.zip")
        
        if not zip_files:
            print("❌ Kein kombiniertes ZIP-File gefunden!")
            return
        
        zip_file = zip_files[0]
        
        # Asset hochladen
        with open(zip_file, 'rb') as f:
            asset = release.upload_asset(
                path=zip_file,
                content_type='application/zip'
            )
        
        print(f"✅ Release erstellt: {release.html_url}")
        
    except Exception as e:
        print(f"❌ Fehler beim Erstellen des Releases: {e}")
        raise

if __name__ == "__main__":
    main() 