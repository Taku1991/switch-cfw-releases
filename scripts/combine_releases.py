#!/usr/bin/env python3
import os
import requests
import zipfile
import shutil
import tempfile
from pathlib import Path

def download_file(url, filename):
    """Lädt eine Datei von einer URL herunter"""
    headers = {
        'Authorization': f'token {os.environ["GITHUB_TOKEN"]}',
        'Accept': 'application/octet-stream'
    }
    
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def extract_zip(zip_path, extract_to):
    """Entpackt eine ZIP-Datei"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def find_sd_folder(base_path):
    """Findet den 'sd'-Ordner in der CFW-Struktur"""
    print(f"🔍 Suche sd-Ordner in: {base_path}")
    
    # Debug: Zeige Verzeichnisstruktur
    for root, dirs, files in os.walk(base_path):
        level = root.replace(str(base_path), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # Nur erste 5 Dateien zeigen
            print(f"{subindent}{file}")
        if len(files) > 5:
            print(f"{subindent}... ({len(files)-5} weitere Dateien)")
        if level > 3:  # Begrenze Tiefe für Debug
            break
    
    # Erste Priorität: Suche nach 'sd'-Ordner mit atmosphere
    for root, dirs, files in os.walk(base_path):
        if 'sd' in dirs:
            sd_path = Path(root) / 'sd'
            print(f"✅ sd-Ordner gefunden: {sd_path}")
            # Überprüfe ob es der richtige sd-Ordner ist
            if (sd_path / 'atmosphere').exists():
                print(f"✅ Atmosphere-Ordner in sd gefunden")
                return sd_path
            else:
                print(f"⚠️ Kein atmosphere-Ordner in {sd_path}")
    
    # Zweite Priorität: Suche nach Verzeichnis mit atmosphere und switch
    print("🔍 Suche nach Verzeichnis mit atmosphere und switch...")
    for root, dirs, files in os.walk(base_path):
        if 'atmosphere' in dirs and 'switch' in dirs:
            cfw_root = Path(root)
            print(f"✅ CFW-Root mit atmosphere und switch gefunden: {cfw_root}")
            return cfw_root
    
    # Dritte Priorität: Suche direkt nach atmosphere-Ordner
    print("🔍 Suche direkt nach atmosphere-Ordner...")
    for root, dirs, files in os.walk(base_path):
        if 'atmosphere' in dirs:
            atmosphere_parent = Path(root)
            print(f"✅ Atmosphere-Ordner gefunden in: {atmosphere_parent}")
            return atmosphere_parent
    
    # Letzte Option: Prüfe ob im base_path selbst atmosphere ist
    if (base_path / 'atmosphere').exists():
        print(f"✅ Atmosphere direkt im base_path gefunden: {base_path}")
        return base_path
    
    print("⚠️ Keine geeignete CFW-Struktur gefunden")
    return None

def find_bootloader_files(base_path):
    """Findet Hekate Bootloader-Dateien"""
    bootloader_files = []
    bootloader_dir = None
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            # Hekate Binary Files
            if file.endswith('.bin') and 'hekate' in file.lower():
                bootloader_files.append(Path(root) / file)
            # payload.bin für Chainloading
            elif file == 'payload.bin':
                bootloader_files.append(Path(root) / file)
        # Bootloader Ordner
        if 'bootloader' in dirs:
            bootloader_dir = Path(root) / 'bootloader'
    
    return bootloader_files, bootloader_dir



def copy_with_merge(src, dst):
    """Kopiert Dateien und mergt Ordner intelligent - behält ALLE Ordner (auch leere)"""
    if src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return
    
    # Erstelle Zielordner falls nicht vorhanden
    dst.mkdir(parents=True, exist_ok=True)
    
    print(f"🔄 Merge: {src.name} → {dst.name}")
    
    # Erstelle ALLE Unterverzeichnisse zuerst (auch leere) - vollständige Struktur
    for root, dirs, files in os.walk(src):
        for dir_name in dirs:
            src_subdir = Path(root) / dir_name
            rel_path = src_subdir.relative_to(src)
            dst_subdir = dst / rel_path
            dst_subdir.mkdir(parents=True, exist_ok=True)
            print(f"📁 Ordner erstellt/gemergt: {rel_path}")
    
    # Kopiere ALLE Dateien (vollständige Datei-Kopie wie beim CFW-Teil)
    for root, dirs, files in os.walk(src):
        for file in files:
            src_file = Path(root) / file
            rel_path = src_file.relative_to(src)
            dst_file = dst / rel_path
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)
            print(f"📄 Datei kopiert: {rel_path}")

def get_asset_urls():
    """Holt die Asset URLs aus den Environment-Variablen"""
    # Diese werden vom check_releases.py Script gesetzt
    with open('last_versions.json', 'r') as f:
        import json
        versions = json.load(f)
    
    # GitHub API URLs für Assets
    cfw_url = get_download_url('Atmosphere-NX/Atmosphere', 'atmosphere')
    fusee_url = get_download_url('Atmosphere-NX/Atmosphere', 'fusee.bin')
    bootloader_url = get_download_url('CTCaer/hekate', 'hekate_ctcaer')
    sysdvr_url = get_download_url('exelix11/SysDVR', 'sysdvr.zip')
    ldn_mitm_url = get_download_url('Lusamine/ldn_mitm', 'ldn_mitm')
    sys_botbase_url = get_download_url('bdawg1989/sys-botbase', '.zip')
    ftpd_url = get_download_url('mtheall/ftpd', 'ftpd.nro')
    jksv_url = get_download_url('J-D-K/JKSV', 'JKSV.nro')
    
    return cfw_url, fusee_url, bootloader_url, sysdvr_url, ldn_mitm_url, sys_botbase_url, ftpd_url, jksv_url

def get_download_url(repo, asset_pattern):
    """Holt die Download-URL für ein Asset"""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {
        'Authorization': f'token {os.environ["GITHUB_TOKEN"]}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    release = response.json()
    
    for asset in release['assets']:
        if asset_pattern.lower() in asset['name'].lower():
            return asset['browser_download_url']
    
    raise Exception(f"Asset mit Pattern '{asset_pattern}' nicht gefunden in {repo}")

def copy_assets_to_release(combined_dir):
    """Kopiert Assets aus dem assets/ Ordner in die richtige Struktur"""
    assets_dir = Path("assets")
    
    if not assets_dir.exists():
        print("⚠️ Assets-Ordner nicht gefunden, überspringe Asset-Kopierung")
        return
    
    print("🎨 Kopiere Assets aus assets/ Ordner...")
    
    # Erstelle bootloader und bootloader/res Ordner
    bootloader_dir = combined_dir / "bootloader"
    bootloader_res_dir = bootloader_dir / "res"
    bootloader_dir.mkdir(parents=True, exist_ok=True)
    bootloader_res_dir.mkdir(parents=True, exist_ok=True)
    
    # Kopiere hekate_ipl.ini direkt in bootloader/
    hekate_ini = assets_dir / "hekate_ipl.ini"
    if hekate_ini.exists():
        shutil.copy2(hekate_ini, bootloader_dir / "hekate_ipl.ini")
        print("✅ hekate_ipl.ini → bootloader/hekate_ipl.ini")
    else:
        print("⚠️ hekate_ipl.ini nicht in assets/ gefunden")
    
    # Kopiere .bmp Dateien nach bootloader/res/
    bmp_files = ["background.bmp", "icon_payload.bmp", "icon_switch.bmp"]
    
    for bmp_file in bmp_files:
        bmp_path = assets_dir / bmp_file
        if bmp_path.exists():
            shutil.copy2(bmp_path, bootloader_res_dir / bmp_file)
            print(f"✅ {bmp_file} → bootloader/res/{bmp_file}")
        else:
            print(f"⚠️ {bmp_file} nicht in assets/ gefunden")
    
    print("🎨 Asset-Kopierung abgeschlossen")

def main():
    # Erstelle Arbeitsverzeichnisse
    work_dir = Path("release_work")
    work_dir.mkdir(exist_ok=True)
    
    cfw_dir = work_dir / "cfw"
    bootloader_dir = work_dir / "bootloader" 
    sysdvr_dir = work_dir / "sysdvr"
    ldn_mitm_dir = work_dir / "ldn_mitm"
    sys_botbase_dir = work_dir / "sys_botbase"
    combined_dir = work_dir / "combined"
    
    for dir_path in [cfw_dir, bootloader_dir, sysdvr_dir, ldn_mitm_dir, sys_botbase_dir, combined_dir]:
        dir_path.mkdir(exist_ok=True)
    
    try:
        # Hole Asset URLs
        cfw_url, fusee_url, bootloader_url, sysdvr_url, ldn_mitm_url, sys_botbase_url, ftpd_url, jksv_url = get_asset_urls()
        
        # Download Assets
        cfw_zip = work_dir / "atmosphere.zip"
        fusee_bin = work_dir / "fusee.bin"
        bootloader_zip = work_dir / "hekate_ctcaer.zip"
        sysdvr_zip = work_dir / "sysdvr.zip"
        ldn_mitm_zip = work_dir / "ldn_mitm.zip"
        sys_botbase_zip = work_dir / "sys-botbase.zip"
        ftpd_nro = work_dir / "ftpd.nro"
        jksv_nro = work_dir / "JKSV.nro"
        
        print("⬇️ Downloading Components...")
        download_file(cfw_url, cfw_zip)
        download_file(fusee_url, fusee_bin)
        download_file(bootloader_url, bootloader_zip)
        download_file(sysdvr_url, sysdvr_zip)
        download_file(ldn_mitm_url, ldn_mitm_zip)
        download_file(sys_botbase_url, sys_botbase_zip)
        download_file(ftpd_url, ftpd_nro)
        download_file(jksv_url, jksv_nro)
        
        # Entpacke Assets
        extract_zip(cfw_zip, cfw_dir)
        extract_zip(bootloader_zip, bootloader_dir)
        extract_zip(sysdvr_zip, sysdvr_dir)
        extract_zip(ldn_mitm_zip, ldn_mitm_dir)
        extract_zip(sys_botbase_zip, sys_botbase_dir)
        
        # Finde den CFW 'sd'-Ordner (Basis für SD-Karte)
        cfw_sd_folder = find_sd_folder(cfw_dir)
        if not cfw_sd_folder:
            print("⚠️ Kein sd-Ordner gefunden, versuche alternative Struktur...")
            # Alternative: Kopiere alles vom CFW-Verzeichnis
            cfw_sd_folder = cfw_dir
        
        print(f"📁 Verwende CFW-Basis: {cfw_sd_folder}")
        
        # Kopiere komplette CFW-Struktur als Basis
        print("📁 Kopiere CFW-Basis...")
        
        # Erstelle alle Verzeichnisse zuerst (auch leere)
        for root, dirs, files in os.walk(cfw_sd_folder):
            for dir_name in dirs:
                src_dir = Path(root) / dir_name
                rel_path = src_dir.relative_to(cfw_sd_folder)
                dst_dir = combined_dir / rel_path
                dst_dir.mkdir(parents=True, exist_ok=True)
                print(f"📁 Ordner erstellt: {rel_path}")
        
        # Dann kopiere alle Dateien
        for root, dirs, files in os.walk(cfw_sd_folder):
            for file in files:
                src_file = Path(root) / file
                rel_path = src_file.relative_to(cfw_sd_folder)
                dst_file = combined_dir / rel_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
        
        print("🔧 Integriere fusee.bin...")
        # Erstelle bootloader/payloads Ordner falls nicht vorhanden
        payloads_dir = combined_dir / 'bootloader' / 'payloads'
        payloads_dir.mkdir(parents=True, exist_ok=True)
        
        # Kopiere fusee.bin in den Root-Ordner (VOR Hekate, um korrekte Dateinamen zu gewährleisten)
        root_fusee = combined_dir / 'fusee.bin'
        shutil.copy2(fusee_bin, root_fusee)
        print(f"✅ fusee.bin → /fusee.bin (Root)")
        
        # Kopiere fusee.bin nach bootloader/payloads/ (VOR Hekate, um korrekte Dateinamen zu gewährleisten)
        target_fusee = payloads_dir / 'fusee.bin'
        shutil.copy2(fusee_bin, target_fusee)
        print(f"✅ fusee.bin → bootloader/payloads/fusee.bin")
        
        print("🚀 Integriere Hekate Bootloader...")
        bootloader_files, bootloader_config_dir = find_bootloader_files(bootloader_dir)
        
        for bootloader_file in bootloader_files:
            target = combined_dir / bootloader_file.name
            shutil.copy2(bootloader_file, target)
        
        if bootloader_config_dir and bootloader_config_dir.exists():
            target_bootloader = combined_dir / 'bootloader'
            copy_with_merge(bootloader_config_dir, target_bootloader)
        
        print("🔗 Integriere SysDVR...")
        sysdvr_root = None
        for root, dirs, files in os.walk(sysdvr_dir):
            if 'atmosphere' in dirs and 'switch' in dirs:
                sysdvr_root = Path(root)
                break
        
        if not sysdvr_root:
            for root, dirs, files in os.walk(sysdvr_dir):
                if 'atmosphere' in dirs:
                    sysdvr_root = Path(root)
                    break
        
        if not sysdvr_root:
            raise Exception("❌ Konnte SysDVR-Struktur nicht finden!")
        
        for item in sysdvr_root.iterdir():
            if item.is_dir():
                copy_with_merge(item, combined_dir / item.name)
            else:
                shutil.copy2(item, combined_dir / item.name)
        
        print("🌐 Integriere ldn_mitm...")
        ldn_mitm_root = None
        for root, dirs, files in os.walk(ldn_mitm_dir):
            if 'atmosphere' in dirs or any(f.endswith('.kip') for f in files):
                ldn_mitm_root = Path(root)
                break
        
        if ldn_mitm_root:
            for item in ldn_mitm_root.iterdir():
                if item.is_dir():
                    copy_with_merge(item, combined_dir / item.name)
                else:
                    shutil.copy2(item, combined_dir / item.name)
        
        print("🤖 Integriere sys-botbase...")
        sys_botbase_root = None
        for root, dirs, files in os.walk(sys_botbase_dir):
            if 'atmosphere' in dirs or any(f.endswith('.kip') for f in files):
                sys_botbase_root = Path(root)
                break
        
        if sys_botbase_root:
            for item in sys_botbase_root.iterdir():
                if item.is_dir():
                    copy_with_merge(item, combined_dir / item.name)
                else:
                    shutil.copy2(item, combined_dir / item.name)
        
        print("📁 Integriere Homebrew Apps...")
        switch_dir = combined_dir / 'switch'
        switch_dir.mkdir(parents=True, exist_ok=True)
        
        # ftpd integrieren
        if ftpd_nro.exists():
            shutil.copy2(ftpd_nro, switch_dir / 'ftpd.nro')
            print("✅ ftpd.nro kopiert")
        else:
            print(f"⚠️ ftpd.nro nicht gefunden: {ftpd_nro}")
        
        # JKSV integrieren
        if jksv_nro.exists():
            shutil.copy2(jksv_nro, switch_dir / 'JKSV.nro')
            print("✅ JKSV.nro kopiert")
        else:
            print(f"⚠️ JKSV.nro nicht gefunden: {jksv_nro}")
        
        # Kopiere Assets aus dem assets/ Ordner
        copy_assets_to_release(combined_dir)
        
        # Erstelle finales ZIP
        cfw_version = os.environ.get('CFW_VERSION', 'unknown')
        bootloader_version = os.environ.get('BOOTLOADER_VERSION', 'unknown')
        sysdvr_version = os.environ.get('SYSDVR_VERSION', 'unknown')
        ldn_mitm_version = os.environ.get('LDN_MITM_VERSION', 'unknown')
        sys_botbase_version = os.environ.get('SYS_BOTBASE_VERSION', 'unknown')
        ftpd_version = os.environ.get('FTPD_VERSION', 'unknown')
        jksv_version = os.environ.get('JKSV_VERSION', 'unknown')
        
        final_zip_name = f"Pokemon-SysBot-CFW-{cfw_version}-Complete.zip"
        
        print(f"📦 Erstelle Release: {final_zip_name}")
        
        # Erstelle ZIP
        with zipfile.ZipFile(final_zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in combined_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(combined_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✅ Release erstellt: {final_zip_name}")
        
        # Erstelle Release-Notes
        release_notes = f"""# 🎮 Pokemon SysBot CFW - Complete Solution

## 🔧 Enthaltene Komponenten
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

---
*🤖 Automatisch generiert am {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""
        
        with open('release_notes.md', 'w', encoding='utf-8') as f:
            f.write(release_notes)
            
        print("✅ Release Notes erstellt")
        
    except Exception as e:
        print(f"❌ Fehler beim Kombinieren der Releases: {e}")
        raise
    
    finally:
        # Cleanup - behalte nur das finale ZIP und Release Notes
        if work_dir.exists():
            shutil.rmtree(work_dir)
        print("🧹 Temporäre Dateien bereinigt")

if __name__ == "__main__":
    main() 