# 🎮 Pokemon SysBot CFW - Komplette Lösung

Ein automatisches Release-System, das die neuesten Versionen aller Komponenten für eine vollständige Pokemon SysBot CFW-Lösung überwacht und intelligent kombiniert.

## 💬 Support & Community
**Brauche Hilfe?** Tritt unserem Discord bei: [discord.gg/pokemonhideout](https://discord.gg/pokemonhideout) 🎮

## 📦 Paketinhalt

### Enthaltene Dateien:
- **SysBot Base** - Kernsystem für Bots auf Nintendo Switch ([Quelle](https://github.com/bdawg1989/sys-botbase))
- **Atmosphère** - Custom Firmware für Nintendo Switch ([Quelle](https://github.com/Atmosphere-NX/Atmosphere))
- **JKSV** - Spielstand-Manager ([Quelle](https://github.com/J-D-K/JKSV))
- **ldn_mitm** - Erforderlich für Online-Funktionen und SysBot ([Quelle](https://github.com/Lusamine/ldn_mitm))
- **ftpd pro** - FTP-Server für drahtlose Dateiverwaltung ([Quelle](https://github.com/mtheall/ftpd))
- **SysDVR** - Video-Streaming von der Switch ([Quelle](https://github.com/exelix11/SysDVR))
- **Hekate** - Bootloader für modifizierte Switches ([Quelle](https://github.com/CTCaer/hekate))

## 📋 Voraussetzungen

- **Unpatched Nintendo Switch** (anfällig für RCM-Exploit) ODER Switch mit Modchip
- **USB-C Kabel** zum Verbinden der Switch mit dem PC
- **MicroSD-Karte** (mindestens 16GB, empfohlen 32GB+)
- **RCM Jig** oder alternative Methode für RCM-Modus (nur bei unpatched)

## 🔧 Setup-Anleitung für Unpatched Switches

### Schritt 1: SD-Karte formatieren
1. MicroSD-Karte in den Computer einlegen
2. SD-Karte mit FAT32 formatieren
   - **WICHTIG**: Alle Daten werden gelöscht!
3. Formatierung abschließen und SD-Karte sicher entfernen

### Schritt 2: Dateien auf SD-Karte kopieren
1. Nach dem Formatieren alle Inhalte aus dem Release-ZIP direkt auf die SD-Karte kopieren
2. **Keine Ordnerstrukturen ändern oder Dateien umbenennen**
3. SD-Karte sicher aus dem Computer entfernen

### Schritt 3: RCM-Modus aktivieren
1. Nintendo Switch vollständig ausschalten
2. MicroSD-Karte in die Switch einlegen
3. RCM Jig in die rechte Joy-Con-Schiene einführen
4. **VOL+** gedrückt halten und gleichzeitig **POWER** drücken
5. Bildschirm bleibt schwarz (das ist korrekt!)

### Schritt 4: Payload injizieren
1. Switch mit USB-C Kabel an PC anschließen
2. TegraRcmGUI als Administrator starten
3. In TegraRCM:
   - Switch-Erkennung prüfen (unten rechts angezeigt)
   - "Install Driver" klicken falls Gerät nicht erkannt
   - Zum "Payload" Tab wechseln
   - Mitgelieferte `fusee.bin` Datei auswählen
   - "Inject Payload" klicken

## 🔧 Setup-Anleitung für Modchip Switches

Für Mariko/gepatcht Switch-Modelle mit installierten Modchips verwenden wir Hekate als Bootloader.

### Schritt 1: Dateien auf SD-Karte kopieren
1. SD-Karte mit FAT32 formatieren
2. Alle Inhalte aus dem Release auf SD-Karte kopieren
3. SD-Karte sicher entfernen

### Schritt 2: Mit Modchip booten
1. SD-Karte in Switch einlegen
2. Switch einschalten - Modchip sollte automatisch zu Hekate booten
3. Falls nicht automatisch: Modchip-Dokumentation für spezifische Boot-Anweisungen konsultieren

### Schritt 3: Atmosphère starten
1. Im Hekate Bootloader zu "Launch" navigieren
2. "CFW" auswählen
3. Switch startet in Atmosphère mit allen erforderlichen Modulen

## 🚀 Erste Einrichtung

1. Switch startet in Atmosphère Custom Firmware
2. Bildschirmanweisungen folgen für initiale Einrichtung
3. Atmosphère lädt automatisch sys-botbase und andere Module

### Mit SysBot.NET verbinden:
1. Pokemon-Spiel starten
2. Switch mit gleichem Netzwerk wie PC verbinden (WLAN-Einstellungen)
3. Switch IP-Adresse notieren (System-Einstellungen → Internet → Verbindungsstatus)
4. Diese IP-Adresse verwenden um SysBot.NET vom PC zu verbinden

## 💾 JKSV verwenden (Spielstand-Manager)

### Spielstände sichern:
1. JKSV aus dem Homebrew-Menü starten
2. Spiel aus der Liste auswählen
3. **+** Taste drücken oder "Backup" wählen
4. Namen für Backup eingeben (oder Standard verwenden)
5. Backup-Abschluss abwarten

### Spielstände wiederherstellen:
1. JKSV aus dem Homebrew-Menü starten
2. Gewünschtes Spiel auswählen
3. **Y** drücken um Backup-Liste anzuzeigen
4. Backup zum Wiederherstellen auswählen
5. "Restore" wählen und bestätigen
6. Spiel neustarten um wiederhergestellten Spielstand zu verwenden

## 📁 FTPD Pro verwenden (Dateiübertragung)

### Auf der Switch:
1. FTPD Pro aus dem Homebrew-Menü starten
2. IP-Adresse und Port (normalerweise 5000) notieren
3. FTPD Pro während gesamter Übertragung laufen lassen

### Auf dem PC:
1. FTP-Client wie FileZilla installieren
2. Verbindungsdetails eingeben:
   - **Host**: Switch IP-Adresse (auf FTPD-Bildschirm angezeigt)
   - **Port**: 5000 (oder angezeigter Port)
   - **Benutzername**: (leer lassen oder "anonymous")
   - **Passwort**: (leer lassen)
3. "Verbinden" klicken
4. Switch-Dateisystem ist nun zugänglich
5. Dateien per Drag & Drop zwischen PC und Switch übertragen

### Tipps:
- FTP zum Hinzufügen/Aktualisieren von Spielen und Homebrew verwenden
- `/atmosphere/contents/` für Spiel-Mods navigieren
- Screenshots von `/Nintendo/Album/` übertragen

## 🔄 Bestehende Installation aktualisieren

**WICHTIG**: **NICHT** den Nintendo-Ordner auf der SD-Karte löschen - er enthält alle Spielstände!

1. Inhalte der neuen Release auf SD-Karte kopieren
2. Beim Überschreiben bestehender Dateien bestätigen
3. Payload mit aktueller `fusee.bin` neu injizieren falls mitgeliefert
4. Gespeicherte Daten, Konfigurationen und Einstellungen bleiben erhalten

## 🛠️ Fehlerbehebung

| Problem | Lösung |
|---------|--------|
| Switch geht nicht in RCM | Switch ist unpatched und RCM Jig korrekt eingesetzt? |
| Payload-Injektion fehlgeschlagen | Treiber neu installieren oder anderes USB-Kabel versuchen |
| SysBot verbindet nicht | IP-Adresse prüfen und sicherstellen dass Spiel läuft |
| Schwarzer Bildschirm nach Injektion | Korrekte `fusee.bin` für Setup verwenden |
| Modchip bootet nicht | Modchip-Dokumentation für spezifische Problembehebung |

**Weitere Hilfe benötigt?** Besuche unseren Discord: [discord.gg/pokemonhideout](https://discord.gg/pokemonhideout)

## 🔒 Ban-Schutz für Pokemon Bot-Betrieb


## 🤖 Automatisches Release-System

Dieses Repository:
- **Überwacht automatisch** alle 12 Stunden nach neuen Releases
- **Kombiniert intelligent** alle Komponenten zu kompletten Paketen
- **Erstellt professionelle Releases** mit detaillierten Installationsanleitungen
- **Gewährleistet Kompatibilität** zwischen allen Komponenten

## 📞 Support & Community

### 🎮 Primärer Support:
- **Pokemon Hideout Discord**: [discord.gg/pokemonhideout](https://discord.gg/pokemonhideout) - **Unser eigener Support-Server!**

### 🌐 Weitere Community-Ressourcen:
- **Pokemon SysBot**: [SysBot.NET Discord](https://discord.gg/tDMvSRv)
- **Switch Homebrew**: [r/SwitchHaxing](https://reddit.com/r/SwitchHaxing)
- **Atmosphère**: [Atmosphère Discord](https://discord.gg/qbRAuy7)
- **Hekate**: [CTCaer/hekate GitHub](https://github.com/CTCaer/hekate)

## 📞 Zusätzliche Ressourcen

- [SysBot.NET Wiki](https://github.com/kwsch/SysBot.NET/wiki)
- [Atmosphère Dokumentation](https://github.com/Atmosphere-NX/Atmosphere/blob/master/docs/index.md)

---

## ⚠️ Disclaimer

Diese Einrichtung ist nur für den persönlichen Gebrauch bestimmt. Bitte respektiere Spieleentwickler und verwende diese Tools nicht zum Cheaten im Online-Spiel oder zur Verbreitung von unauthorisiertem Content.

**WICHTIGE WARNUNG**: Diese Konfiguration modifiziert deine primäre Switch-Installation (SysNAND). Dies birgt Risiken:
- **Console-Ban möglich**: Nintendo kann deine Switch permanent bannen
- **Account-Ban möglich**: Dein Nintendo Account kann gesperrt werden  
- **Kein Garantieerhalt**: Warranty wird durch CFW ungültig
- **Eigene Verantwortung**: Du trägst alle Risiken selbst

## 🔒 Ban-Schutz für Pokemon Bot-Betrieb

### Sichere Nutzung:
- ✅ NUR offizielle Pokemon-Spiele verwenden
- ✅ KEINE gepiratetenSpiele installieren
- ✅ KEINE NSP/XCI Dateien
- ✅ KEINE Cheats außer durch Bot
- ✅ KEINE Theme-Installationen
- ✅ Homebrew NUR über Album starten

**Für Bildungszwecke - Respektiere Nintendos Terms of Service und lokale Gesetze!** 🚀

## 📄 Lizenz & Copyright

### Dieses Repository
- **Copyright**: © 2024 - Repository-Maintainer
- **Lizenz**: MIT License (für Automation-Scripts und Dokumentation)
- **Zweck**: Automatische Kombination und Distribution von Open-Source-Projekten

### Enthaltene Projekte und deren Lizenzen

| Projekt | Lizenz | Copyright | Repository |
|---------|--------|-----------|------------|
| **Atmosphère** | GPLv2 | SciresM, TuxSH, hexkyz, fincs | [Atmosphere-NX/Atmosphere](https://github.com/Atmosphere-NX/Atmosphere) |
| **Hekate** | GPLv2 | CTCaer | [CTCaer/hekate](https://github.com/CTCaer/hekate) |
| **sys-botbase** | MIT | bdawg1989 | [bdawg1989/sys-botbase](https://github.com/bdawg1989/sys-botbase) |
| **ldn_mitm** | GPLv2 | Lusamine | [Lusamine/ldn_mitm](https://github.com/Lusamine/ldn_mitm) |
| **JKSV** | GPLv3 | J-D-K | [J-D-K/JKSV](https://github.com/J-D-K/JKSV) |
| **ftpd** | GPLv3 | mtheall | [mtheall/ftpd](https://github.com/mtheall/ftpd) |
| **SysDVR** | GPLv3 | exelix11 | [exelix11/SysDVR](https://github.com/exelix11/SysDVR) |

### Rechtliche Hinweise

#### Was dieses Repository beinhaltet:
- ✅ **Automatisierte Kombination** von öffentlich verfügbaren Releases
- ✅ **Dokumentation und Anleitungen** (eigene Erstellung)
- ✅ **GitHub Actions Workflows** (eigene Erstellung)
- ✅ **Python-Scripts für Automation** (eigene Erstellung)

#### Was dieses Repository NICHT beinhaltet:
- ❌ **Keine Spiele oder NSP/XCI Dateien**
- ❌ **Keine Nintendo-eigenen Dateien**
- ❌ **Keine modifizierten System-Dateien**
- ❌ **Keine Piraterie-Tools**

#### Lizenz für Repository-spezifische Inhalte:
```
MIT License

Copyright (c) 2025 [Taku1991]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Nutzungsbedingungen

1. **Respektiere alle Original-Lizenzen** der enthaltenen Projekte
2. **Keine kommerzielle Nutzung** ohne Genehmigung der Original-Autoren
3. **Keine Modifikation** der Original-Binärdateien
4. **Keine Garantie** für Funktionalität oder Sicherheit
5. **Keine Verantwortung** für Schäden oder Bans durch Nintendo

### Credits & Danksagungen

Besonderer Dank an:
- **SciresM, TuxSH, hexkyz, fincs** für Atmosphère
- **CTCaer** für Hekate  
- **bdawg1989** für sys-botbase
- **Lusamine** für ldn_mitm
- **J-D-K** für JKSV
- **mtheall** für ftpd
- **exelix11** für SysDVR
- **Die gesamte Nintendo Switch Homebrew Community**





