#!/usr/bin/env python3
import os
import json
import requests

def get_latest_release_info(repo_name, asset_pattern):
    """Holt Informationen über das neueste Release"""
    try:
        url = f"https://api.github.com/repos/{repo_name}/releases"
        headers = {
            'Authorization': f'token {os.environ["GITHUB_TOKEN"]}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        releases = response.json()
        if not releases:
            raise Exception("Keine Releases gefunden")
        
        release = releases[0]
        
        matching_asset = None
        for asset in release['assets']:
            if asset_pattern in asset['name'].lower():
                matching_asset = asset
                break
                
        return {
            'tag_name': release['tag_name'],
            'name': release['name'],
            'published_at': release['published_at'],
            'prerelease': release['prerelease'],
            'asset': matching_asset
        }
    except Exception as e:
        print(f"❌ Fehler bei {repo_name}: {e}")
        return None

def load_last_versions():
    """Lädt die zuletzt verarbeiteten Versionen"""
    try:
        with open('last_versions.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            'cfw_version': '', 
            'bootloader_version': '', 
            'sysdvr_version': '', 
            'ldn_mitm_version': '', 
            'sys_botbase_version': '',
            'ftpd_version': '',
            'jksv_version': ''
        }

def save_last_versions(versions):
    """Speichert die aktuellen Versionen"""
    with open('last_versions.json', 'w') as f:
        json.dump(versions, f)

def main():
    repos = {
        'cfw': {
            'name': 'Atmosphere-NX/Atmosphere',
            'asset_pattern': 'atmosphere'
        },
        'bootloader': {
            'name': 'CTCaer/hekate',
            'asset_pattern': 'hekate_ctcaer'
        },
        'sysdvr': {
            'name': 'exelix11/SysDVR',
            'asset_pattern': 'sysdvr.zip'
        },
        'ldn_mitm': {
            'name': 'Lusamine/ldn_mitm',
            'asset_pattern': 'ldn_mitm'
        },
        'sys_botbase': {
            'name': 'bdawg1989/sys-botbase',
            'asset_pattern': '.zip'
        },
        'ftpd': {
            'name': 'mtheall/ftpd',
            'asset_pattern': 'ftpd.nro'
        },
        'jksv': {
            'name': 'J-D-K/JKSV',
            'asset_pattern': 'JKSV.nro'
        }
    }
    
    last_versions = load_last_versions()
    current_releases = {}
    
    for key, repo_info in repos.items():
        release_info = get_latest_release_info(repo_info['name'], repo_info['asset_pattern'])
        if release_info:
            current_releases[key] = release_info
        else:
            exit(1)
    
    # Prüfe auf neue Versionen
    cfw_version = current_releases['cfw']['tag_name']
    bootloader_version = current_releases['bootloader']['tag_name']
    sysdvr_version = current_releases['sysdvr']['tag_name']
    ldn_mitm_version = current_releases['ldn_mitm']['tag_name']
    sys_botbase_version = current_releases['sys_botbase']['tag_name']
    ftpd_version = current_releases['ftpd']['tag_name']
    jksv_version = current_releases['jksv']['tag_name']
    
    new_release_needed = (
        cfw_version != last_versions.get('cfw_version') or 
        bootloader_version != last_versions.get('bootloader_version') or
        sysdvr_version != last_versions.get('sysdvr_version') or
        ldn_mitm_version != last_versions.get('ldn_mitm_version') or
        sys_botbase_version != last_versions.get('sys_botbase_version') or
        ftpd_version != last_versions.get('ftpd_version') or
        jksv_version != last_versions.get('jksv_version')
    )
        
    if new_release_needed:
        save_last_versions({
            'cfw_version': cfw_version,
            'bootloader_version': bootloader_version,
            'sysdvr_version': sysdvr_version,
            'ldn_mitm_version': ldn_mitm_version,
            'sys_botbase_version': sys_botbase_version,
            'ftpd_version': ftpd_version,
            'jksv_version': jksv_version
        })
    
    # GitHub Actions Outputs setzen
    combined_tag = f"Pokemon-SysBot-CFW-{cfw_version}-Complete"
    
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"new_release={'true' if new_release_needed else 'false'}\n")
        f.write(f"cfw_version={cfw_version}\n")
        f.write(f"bootloader_version={bootloader_version}\n")
        f.write(f"sysdvr_version={sysdvr_version}\n")
        f.write(f"ldn_mitm_version={ldn_mitm_version}\n")
        f.write(f"sys_botbase_version={sys_botbase_version}\n")
        f.write(f"ftpd_version={ftpd_version}\n")
        f.write(f"jksv_version={jksv_version}\n")
        f.write(f"combined_tag={combined_tag}\n")
        f.write(f"cfw_asset_url={current_releases['cfw']['asset']['browser_download_url'] if current_releases['cfw']['asset'] else ''}\n")
        f.write(f"bootloader_asset_url={current_releases['bootloader']['asset']['browser_download_url'] if current_releases['bootloader']['asset'] else ''}\n")
        f.write(f"sysdvr_asset_url={current_releases['sysdvr']['asset']['browser_download_url'] if current_releases['sysdvr']['asset'] else ''}\n")
        f.write(f"ldn_mitm_asset_url={current_releases['ldn_mitm']['asset']['browser_download_url'] if current_releases['ldn_mitm']['asset'] else ''}\n")
        f.write(f"sys_botbase_asset_url={current_releases['sys_botbase']['asset']['browser_download_url'] if current_releases['sys_botbase']['asset'] else ''}\n")
        f.write(f"ftpd_asset_url={current_releases['ftpd']['asset']['browser_download_url'] if current_releases['ftpd']['asset'] else ''}\n")
        f.write(f"jksv_asset_url={current_releases['jksv']['asset']['browser_download_url'] if current_releases['jksv']['asset'] else ''}\n")
    
    print(f"✅ Release Status: {'Neu' if new_release_needed else 'Aktuell'}")

if __name__ == "__main__":
    main() 