# ZIZIPHUS JUJUBA — Distribution & Deployment Guide

## 1. Overview
ZIZIPHUS JUJUBA is an independent statistical signal intelligence and pattern analysis laboratory for shortwave radio archives (UVB-76).
The application is self-contained and operates as an interactive analytical web application running on a local loopback server (`http://127.0.0.1:8765`).

---

## 2. Windows Portable Edition (No Python Required)

### Package
- File: `ZiziphusJujuba-v2.0.0-windows-x64.zip`
- Architecture: 64-bit Windows (Windows 10, 11, Windows Server)

### How to Run
1. Download and extract `ZiziphusJujuba-v2.0.0-windows-x64.zip` to any folder on your computer (e.g. `C:\ZiziphusJujuba` or `Desktop`).
2. Double-click `ZiziphusJujuba.exe`.
3. The server starts instantly, initializes the embedded SQLite database, and automatically opens your default web browser at `http://127.0.0.1:8765`.
4. All 13 analytical tabs, graph engines, and data export features are immediately accessible offline.
5. To stop the application, simply close the console window or press `Ctrl + C`.

---

## 3. macOS Edition (Apple Silicon & Intel)

### Packages
- `ZiziphusJujuba-macOS-AppleSilicon.zip` (M1, M2, M3, M4 — `arm64`)
- `ZiziphusJujuba-macOS-Intel.zip` (Intel Core i5, i7, i9 — `x86_64`)

### Apple Gatekeeper & Security Considerations
On macOS, applications downloaded from the internet that are not signed with a paid Apple Developer ID certificate undergo Gatekeeper inspection. Gatekeeper will display a security notice stating that the developer cannot be verified.

#### Standard, Secure Way to Launch Unsigned Open-Source Apps (Without Disabling Gatekeeper)
You do **not** need to disable Gatekeeper globally. Apple provides two built-in mechanisms to open verified open-source software:

1. **Option A: Control-Click (Right-Click) Open in Finder**
   - In Finder, right-click (or Control-click) on `ZiziphusJujuba.app`.
   - Select **Open** from the context menu.
   - A dialog will appear with an **"Open"** button (which is not shown during a standard double-click).
   - Click **Open**. macOS will remember this choice for future launches.

2. **Option B: System Settings (Privacy & Security)**
   - Double-click `ZiziphusJujuba.app`. When the warning appears, click **OK**.
   - Open **System Settings** $\rightarrow$ **Privacy & Security**.
   - Scroll down to the **Security** section.
   - You will see: *"ZiziphusJujuba was blocked from opening because it is not from an identified developer"*.
   - Click **"Open Anyway"** and authenticate with your password or Touch ID.

3. **Option C: Command-Line Launch**
   - You can also run the bundled Unix binary directly in Terminal:
     ```bash
     ./ZiziphusJujuba.app/Contents/MacOS/ZiziphusJujuba
     ```

---

## 4. Automated Multi-Platform CI/CD (GitHub Actions)

The repository includes a GitHub Actions release pipeline (`.github/workflows/build-release.yml`).
- Builds on native GitHub runners:
  - `windows-latest` for Windows x64.
  - `macos-latest` for Apple Silicon (`arm64`).
  - `macos-13` for Intel Mac (`x86_64`).
- All release artifacts are created as **Draft Releases** to prevent accidental public release without human review.
