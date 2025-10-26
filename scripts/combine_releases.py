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
    
    # Kopiere background.bmp sowohl nach bootloader/ als auch bootloader/res/
    background_bmp = assets_dir / "background.bmp"
    if background_bmp.exists():
        # Kopiere nach bootloader/ direkt
        shutil.copy2(background_bmp, bootloader_dir / "background.bmp")
        print("✅ background.bmp → bootloader/background.bmp")
        
        # Kopiere nach bootloader/res/
        shutil.copy2(background_bmp, bootloader_res_dir / "background.bmp")
        print("✅ background.bmp → bootloader/res/background.bmp")
    else:
        print("⚠️ background.bmp nicht in assets/ gefunden")
    
    # Kopiere andere .bmp Dateien nach bootloader/res/
    other_bmp_files = ["icon_payload.bmp", "icon_switch.bmp"]
    
    for bmp_file in other_bmp_files:
        bmp_path = assets_dir / bmp_file
        if bmp_path.exists():
            shutil.copy2(bmp_path, bootloader_res_dir / bmp_file)
            print(f"✅ {bmp_file} → bootloader/res/{bmp_file}")
        else:
            print(f"⚠️ {bmp_file} nicht in assets/ gefunden")
    
    print("🎨 Asset-Kopierung abgeschlossen")

def clean_atmosphere_config(combined_dir):
    """Bereinigt Atmosphere-Konfiguration um Cheat-Probleme zu vermeiden"""
    print("🧹 Bereinige Atmosphere-Konfiguration...")
    
    atmosphere_dir = combined_dir / "atmosphere"
    if not atmosphere_dir.exists():
        print("⚠️ Atmosphere-Ordner nicht gefunden, überspringe Konfigurationsbereinigung")
        return
    
    # 1. Entferne alle Cheat-Dateien aus atmosphere/contents/
    contents_dir = atmosphere_dir / "contents"
    if contents_dir.exists():
        print("🔍 Prüfe atmosphere/contents/ auf Cheat-Dateien...")
        for title_dir in contents_dir.iterdir():
            if title_dir.is_dir():
                cheats_dir = title_dir / "cheats"
                if cheats_dir.exists():
                    print(f"🗑️ Entferne Cheat-Ordner: {cheats_dir.relative_to(combined_dir)}")
                    shutil.rmtree(cheats_dir)
                
                # Entferne auch einzelne .txt Cheat-Dateien
                for file in title_dir.glob("*.txt"):
                    if "cheat" in file.name.lower():
                        print(f"🗑️ Entferne Cheat-Datei: {file.relative_to(combined_dir)}")
                        file.unlink()
    
    # 2. Erstelle/Überschreibe system_settings.ini mit sicheren Einstellungen
    config_dir = atmosphere_dir / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    system_settings_ini = config_dir / "system_settings.ini"
    safe_config = """[atmosphere]
; Deaktiviere Cheats standardmäßig
enable_cheats = u8!0x0

; WICHTIG: Deaktiviere dmnt (Debug Monitor für Cheats)
dmnt_cheats_enabled_by_default = u8!0x0
dmnt_always_save_cheat_toggles = u8!0x0

[eupld]
; Upload-Crash-Reports deaktivieren für bessere Stabilität
upload_enabled = u8!0x0

[ro]
; Disable signature verification relaxed
ease_nro_restriction = u8!0x1

[exosphere]
; Blanking Display während Boot für sauberen Start
blank_prodinfo_sysmmc = u8!0x0
blank_prodinfo_emummc = u8!0x0

[hbl_config]
; Homebrew Loader Konfiguration
override_key = !R
override_any_app = u8!0x1

[btm]
; Bluetooth Manager - Standard-Einstellungen
fatal_auto_reboot_interval = u64!0x0
"""
    
    with open(system_settings_ini, 'w', encoding='utf-8') as f:
        f.write(safe_config)
    print("✅ system_settings.ini mit dmnt-Deaktivierung erstellt")
    
    # 3. Entferne override_config.ini falls vorhanden (kann Cheat-Settings enthalten)
    override_config = config_dir / "override_config.ini"
    if override_config.exists():
        print("🗑️ Entferne override_config.ini (kann problematische Einstellungen enthalten)")
        override_config.unlink()

    # 4. Erstelle leeren exefs_patches Ordner falls nicht vorhanden (verhindert Fehler)
    exefs_patches_dir = atmosphere_dir / "exefs_patches"
    exefs_patches_dir.mkdir(parents=True, exist_ok=True)

    # Erstelle leeren kip_patches Ordner falls nicht vorhanden
    kip_patches_dir = atmosphere_dir / "kip_patches"
    kip_patches_dir.mkdir(parents=True, exist_ok=True)

    # 5. Entferne alle .cht Dateien aus dem gesamten atmosphere-Ordner
    print("🔍 Suche nach .cht Cheat-Dateien...")
    for cht_file in atmosphere_dir.rglob("*.cht"):
        print(f"🗑️ Entferne Cheat-Datei: {cht_file.relative_to(combined_dir)}")
        cht_file.unlink()

    print("✅ Atmosphere-Konfiguration bereinigt - Cheats vollständig deaktiviert")

def add_sysdvr_config(combined_dir):
    """Fügt optimierte SysDVR-Konfiguration für Pokemon SysBot hinzu"""
    print("🎥 Konfiguriere SysDVR für Pokemon SysBot...")

    # Erstelle config/sysdvr Verzeichnis (auf SD-Karte Root-Ebene)
    sysdvr_config_dir = combined_dir / "config" / "sysdvr"
    sysdvr_config_dir.mkdir(parents=True, exist_ok=True)

    # Erstelle tcp Konfigurationsdatei für USB-Streaming (optimal für Pokemon Bot)
    # Inhalt "a" = Audio + Video über TCP/USB
    tcp_config = sysdvr_config_dir / "tcp"
    with open(tcp_config, 'w', encoding='utf-8') as f:
        f.write('a')
    print("✅ SysDVR TCP-Modus konfiguriert (Audio+Video über USB)")
    print("   Andere Modi (RTSP/USB) sind automatisch deaktiviert")

def find_component_structure(base_path, component_name):
    """Findet die korrekte Struktur für verschiedene CFW-Komponenten"""
    print(f"🔍 Analysiere {component_name}-Struktur in: {base_path}")
    
    # Debug: Zeige erste Ebene
    items = list(base_path.iterdir()) if base_path.exists() else []
    dirs = [item.name for item in items if item.is_dir()]
    files = [item.name for item in items if item.is_file()]
    print(f"📁 Ordner: {dirs}")
    print(f"📄 Dateien: {files}")
    
    # Prüfe auf direkte SD-Struktur (atmosphere/ und/oder switch/ vorhanden)
    has_atmosphere = (base_path / 'atmosphere').exists()
    has_switch = (base_path / 'switch').exists()
    has_bootloader = (base_path / 'bootloader').exists()
    
    if has_atmosphere or has_switch or has_bootloader:
        print(f"✅ {component_name}: Direkte SD-Struktur erkannt")
        return base_path
    
    # Suche nach Unterordnern mit SD-Struktur
    for item in base_path.iterdir():
        if item.is_dir():
            sub_has_atmosphere = (item / 'atmosphere').exists()
            sub_has_switch = (item / 'switch').exists()
            sub_has_bootloader = (item / 'bootloader').exists()
            
            if sub_has_atmosphere or sub_has_switch or sub_has_bootloader:
                print(f"✅ {component_name}: SD-Struktur in Unterordner gefunden: {item}")
                return item
    
    print(f"⚠️ {component_name}: Keine erkennbare SD-Struktur gefunden")
    return None

def integrate_component(component_root, combined_dir, component_name):
    """Integriert eine Komponente in das kombinierte Release"""
    if not component_root or not component_root.exists():
        print(f"⚠️ {component_name}: Komponente nicht gefunden, überspringe")
        return False
    
    print(f"🔧 Integriere {component_name}...")
    
    success = True
    for item in component_root.iterdir():
        if item.is_dir():
            target_dir = combined_dir / item.name
            try:
                copy_with_merge(item, target_dir)
                print(f"✅ {component_name}: {item.name}/ → {item.name}/")
            except Exception as e:
                print(f"❌ {component_name}: Fehler beim Kopieren von {item.name}/: {e}")
                success = False
        else:
            try:
                target_file = combined_dir / item.name
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_file)
                print(f"✅ {component_name}: {item.name} → {item.name}")
            except Exception as e:
                print(f"❌ {component_name}: Fehler beim Kopieren von {item.name}: {e}")
                success = False
    
    return success

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
        
        # 1. Integriere Atmosphere CFW als Basis
        atmosphere_root = find_component_structure(cfw_dir, "Atmosphere")
        if not integrate_component(atmosphere_root, combined_dir, "Atmosphere CFW"):
            raise Exception("❌ Konnte Atmosphere CFW nicht integrieren!")
        
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
        
        # 2. Integriere Hekate Bootloader
        bootloader_root = find_component_structure(bootloader_dir, "Hekate")
        integrate_component(bootloader_root, combined_dir, "Hekate Bootloader")
        
        # 3. Integriere SysDVR
        sysdvr_root = find_component_structure(sysdvr_dir, "SysDVR")
        integrate_component(sysdvr_root, combined_dir, "SysDVR")
        
        # 4. Integriere ldn_mitm
        ldn_mitm_root = find_component_structure(ldn_mitm_dir, "ldn_mitm")
        integrate_component(ldn_mitm_root, combined_dir, "ldn_mitm")
        
        # 5. Integriere sys-botbase
        sys_botbase_root = find_component_structure(sys_botbase_dir, "sys-botbase")
        integrate_component(sys_botbase_root, combined_dir, "sys-botbase")
        
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

        # Bereinige Atmosphere-Konfiguration
        clean_atmosphere_config(combined_dir)

        # Konfiguriere SysDVR für Pokemon SysBot
        add_sysdvr_config(combined_dir)

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
        
        # Erstelle ZIP mit ALLEN Ordnern (auch leere)
        with zipfile.ZipFile(final_zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Erst alle Ordner hinzufügen (auch leere)
            for dir_path in combined_dir.rglob('*'):
                if dir_path.is_dir():
                    arcname = dir_path.relative_to(combined_dir)
                    # Ordner mit '/' am Ende hinzufügen, damit sie im ZIP erscheinen
                    zipf.writestr(str(arcname) + '/', '')
                    print(f"📁 ZIP: {arcname}/")
            
            # Dann alle Dateien hinzufügen
            for file_path in combined_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(combined_dir)
                    zipf.write(file_path, arcname)
                    print(f"📄 ZIP: {arcname}")
        
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