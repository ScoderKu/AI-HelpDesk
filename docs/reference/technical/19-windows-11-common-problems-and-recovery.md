# Windows 11 — Common Problems, Diagnosis and Safe Recovery

- **Document ID:** KB-WINDOWS-19
- **Status:** general troubleshooting guidance; exact menus and commands can vary by Windows 11 release
- **Applies to:** Windows 11 desktop/laptop, development workstations and peripherals
- **Keywords:** Windows 11, troubleshooting, update, boot, blue screen, BSOD, Wi-Fi, network, Bluetooth, audio, printer, display, driver, disk, storage, permissions, PATH, PowerShell, Windows ei käynnisty, päivitysongelma

## 1. Safety first

Before changing system settings:
- Save work and back up important files.
- Record the exact error code and when it occurs.
- Prefer Windows Settings and official vendor sources.
- Create a restore point before high-impact driver/system changes when System Protection is available.
- Keep the BitLocker recovery key accessible before firmware, boot or partition changes.
- Do not disable antivirus, firewall, Secure Boot or Windows Update as a routine fix.
- Do not run destructive disk, registry or partition commands based on an unverified internet post.

For managed work/school devices, contact the administrator before changing policy or security settings.

## 2. Basic diagnostic sequence

1. Restart once if safe and save work first.
2. Check **Settings → Windows Update → Update history**.
3. Check **Device Manager** for warning icons and device status.
4. Check **Task Manager** for CPU, memory, disk and GPU pressure.
5. Check **Event Viewer → Windows Logs → System/Application** around the failure time.
6. Record the exact error code, affected application and reproduction steps.
7. Change one thing at a time and verify.

## 3. Windows Update fails

- Check internet access, date/time, available disk space and restart requirements.
- Read the update error code in Update history.
- Run the Windows Update troubleshooter if available in Settings.
- Restart and retry.
- Check Microsoft's current guidance for the exact error code before resetting update components.

Do not delete system folders or disable updates as a first response. Feature updates and cumulative updates have different failure modes.

## 4. Slow PC, high CPU, memory or disk usage

- Open Task Manager and sort by CPU, Memory and Disk.
- Identify the process and whether usage is sustained or temporary.
- Check startup apps and browser tabs.
- Ensure sufficient free disk space.
- Check Windows Security and scan if malware is suspected.
- Check drive health with the manufacturer's diagnostic utility.

High utilization is a symptom, not a root cause. Do not end unknown system processes or install random “PC cleaner” utilities.

## 5. Wi-Fi or internet does not work

1. Check whether other devices can connect to the same network.
2. Confirm Wi-Fi is enabled and Airplane mode is off.
3. Restart the router only if you control it and other users will not be disrupted.
4. Forget and reconnect to the network if the password is known.
5. Inspect the adapter in Device Manager.
6. Check whether the problem affects DNS, local network or internet access.

Useful non-destructive PowerShell checks:

```powershell
ipconfig /all
ping 127.0.0.1
ping <router-ip>
nslookup example.com
```

If an IP address works but domain names fail, investigate DNS. If the router cannot be reached, investigate Wi-Fi association, adapter and local network.

Network reset is a later step because it can remove adapters and VPN configuration. Understand the impact first.

## 6. Bluetooth, audio, camera or printer

- Check physical switches, mute, volume, privacy shutters and cable/power.
- Confirm the intended device is selected in Settings.
- Check app permissions under Privacy & security.
- Inspect Device Manager and Windows Update for the correct driver.
- Remove and pair a Bluetooth device again only after confirming its pairing method.
- For printers, check queue, default printer, connection and vendor driver.

Avoid third-party driver updater applications. Prefer Windows Update or the PC/device manufacturer's support page.

## 7. Display, resolution, flicker or GPU problems

- Check monitor power, cable and selected input.
- Press `Win + Ctrl + Shift + B` to reset the graphics driver when the display is responsive enough.
- Check display refresh rate and resolution in Settings → System → Display → Advanced display.
- Check Device Manager and GPU vendor driver version.
- If a problem began immediately after a driver update, consider the supported Roll Back Driver option.

Do not use unofficial driver packages. For gaming or AI workloads, monitor GPU temperature, power, VRAM and application logs rather than relying on utilization percentage alone.

## 8. Blue screen (BSOD) or unexpected restart

Record the stop code and any named driver. Check Reliability Monitor and Event Viewer. Consider recent driver, hardware, memory or software changes.

Windows Memory Diagnostic can help check memory, but a clean result does not rule out every hardware fault. Repeated crashes, overheating, burning smell or physical drive failure require stopping risky use and seeking qualified support.

Do not randomly edit registry values or repeatedly reinstall Windows without preserving data and identifying likely causes.

## 9. Application will not open or install

- Check whether the app supports the current Windows version and CPU architecture.
- Restart and install updates from the official vendor.
- Use Apps → Installed apps → Advanced options → Repair/Reset when available and appropriate.
- Check Event Viewer and the app's own logs.
- Verify disk space and permissions.
- For developer tools, check PATH, terminal restart, architecture and version.

Do not download replacement DLL files from unofficial DLL sites.

## 10. PowerShell, PATH and developer environment problems

- After changing PATH, open a new terminal.
- Use `Get-Command python`, `Get-Command node`, `where.exe python` and `where.exe node` to see which executable is selected.
- Check user PATH separately from system PATH.
- Avoid adding duplicate or obsolete paths.
- Do not overwrite the entire PATH with a short custom value.
- Check execution policy before running scripts; do not disable it globally as a default fix.

A tool working in one terminal but not another often indicates different PATH, shell initialization or environment activation.

## 11. Storage and file access

- Check Settings → System → Storage and Recycle Bin.
- Verify the actual drive and folder before deleting files.
- Check file permissions and whether a file is in use.
- Back up before partition resizing or filesystem repair.
- Use the manufacturer's SSD/HDD diagnostic for suspected hardware faults.

Do not run `format`, `diskpart clean`, partition deletion or destructive repair commands unless the target disk is positively identified and a verified backup exists.

## 12. System file checks

For suspected Windows component corruption, Microsoft documents DISM and System File Checker. Run an elevated terminal only when appropriate, and follow current Microsoft instructions.

Common diagnostic commands:

```powershell
DISM.exe /Online /Cleanup-Image /ScanHealth
sfc /scannow
```

These commands are not universal fixes for application, driver, hardware or network faults. Record their output and investigate any reported repair failure.

## 13. Sign-in, account and permissions

- Confirm keyboard layout, Caps Lock and network connectivity.
- Distinguish Microsoft account, local account and work/school account.
- Do not share passwords or recovery codes.
- Use official account recovery.
- Use least privilege; do not run every development tool as Administrator.
- For access denied, inspect the specific file/folder permissions rather than granting Full Control to broad groups.

## 14. When to escalate

Seek professional or administrator help when:
- BitLocker recovery is requested and the key cannot be found.
- Windows cannot boot and important files are not backed up.
- A disk reports failure or makes unusual mechanical noises.
- The PC repeatedly overheats or shuts down.
- There are signs of liquid damage, electrical smell or physical damage.
- A work/school security policy blocks an action.
- A recovery step risks data loss.

## 15. Incident record template

- Windows edition and version:
- Device model and relevant hardware:
- Exact error/stop code:
- When it started:
- Recent updates or changes:
- Steps to reproduce:
- Diagnostic output:
- Files backed up:
- Actions attempted and results:
- Current status / next safe step:


## Tiivistelmä suomeksi

Windows 11 -ongelmissa aloita oireen ja virhekoodin kirjaamisesta. Tarkista Windows Update, Laitehallinta, verkon tila, vapaa levytila ja tapahtumalokit ennen korjaustoimia. Wi-Fi-, Bluetooth-, ääni- ja näyttöongelmissa rajaa ensin laite, ajuri ja yhteys. Varmuuskopioi tärkeät tiedot ennen palautusta tai levytoimia. Käytä virallisia ajureita ja vältä satunnaisia rekisterimuutoksia tai tuntemattomia korjausohjelmia.
