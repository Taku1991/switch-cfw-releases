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
    
    release_name = f"Pokemon SysBot CFW {cfw_version} - Complete Solution"
    
    # Release Notes laden
    try:
        with open('release_notes.md', 'r', encoding='utf-8') as f:
            release_body = f.read()
    except FileNotFoundError:
        release_body = f"""# Pokemon SysBot CFW - Complete Solution

Automatisch kombinierte Release von:
- Atmosphère {cfw_version} (CFW)
- Hekate {bootloader_version} (Bootloader)
- SysDVR {sysdvr_version} (Video-Streaming)
- ldn_mitm {ldn_mitm_version} (Online-Gaming)
- sys-botbase {sys_botbase_version} (Pokemon-Bots)
- ftpd {ftpd_version} (FTP-Server)
- JKSV {jksv_version} (Save-Manager)

## Installation
1. Entpacke das ZIP-Archiv auf die SD-Karte deiner Nintendo Switch
2. Injiziere hekate_ctcaer_*.bin über TegraRcmGUI
3. Starte CFW über Hekate

⚠️ **Wichtig**: SysNAND-Konfiguration mit erhöhtem Ban-Risiko!

**Für Bildungszwecke - Respektiere Nintendos ToS!**
"""
    
    try:
        # Prüfe ob Release bereits existiert
        try:
            existing_release = repo.get_release(release_tag)
            existing_release.delete_release()
        except:
            pass
        
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