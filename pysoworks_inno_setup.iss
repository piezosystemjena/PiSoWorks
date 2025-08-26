;------------------------------------------------------------
; Inno Setup script for PySoWorks
; Version: 1.0.4
; Purpose: Creates a Windows installer with app, docs, and shortcuts
;------------------------------------------------------------

; Define application name (used throughout the script for consistency)
#define APP_NAME "PySoWorks"

;------------------------------------------------------------
; Setup Section: Installer configuration
;------------------------------------------------------------
[Setup]

; Application name shown in installer
AppName={#APP_NAME}

; Application version
AppVersion=1.0.4

; Default install directory (user-space, no admin rights required)
DefaultDirName={userappdata}\Programs\{#APP_NAME}

; Skip directory selection page
DisableDirPage=yes

; Skip program group (Start Menu folder) selection
DisableProgramGroupPage=yes

; Where installer EXE will be created
OutputDir=dist

; Name of generated installer file
OutputBaseFilename={#APP_NAME}_Setup

; Compression method
Compression=lzma

; Use solid compression for smaller output size
SolidCompression=yes

; No admin rights required (per-user installation)
PrivilegesRequired=lowest

; Enable 64-bit installation mode if OS supports it
ArchitecturesInstallIn64BitMode=x64compatible

; Icon shown in "Add/Remove Programs"
UninstallDisplayIcon={app}\PySoWorks.exe

; Installer icon file
SetupIconFile=pysoworks\assets\app_icon.ico

; Use modern wizard UI style
WizardStyle=modern

;------------------------------------------------------------
; Files Section: Files to be installed
;------------------------------------------------------------
[Files]

; Main executable
Source: "dist\PySoWorks.exe"; DestDir: "{app}"; Flags: ignoreversion

; Documentation (all files and subfolders from doc\_build)
Source: "doc\_build\*"; DestDir: "{app}\doc"; Flags: ignoreversion recursesubdirs createallsubdirs

;------------------------------------------------------------
; Icons Section: Shortcuts
;------------------------------------------------------------
[Icons]

; Start Menu shortcut to the main application
Name: "{userprograms}\PySoWorks"; Filename: "{app}\PySoWorks.exe"

; Start Menu shortcut to documentation (opens index.html in browser)
Name: "{userprograms}\PySoWorks Documentation"; Filename: "{app}\doc\index.html"

; Optional desktop shortcut to the main application
Name: "{userdesktop}\PySoWorks"; Filename: "{app}\PySoWorks.exe"; Tasks: desktopicon

;------------------------------------------------------------
; Tasks Section: Optional installation components
;------------------------------------------------------------
[Tasks]

; Task for creating a desktop shortcut (unchecked by default)
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

;------------------------------------------------------------
; Run Section: Post-install actions
;------------------------------------------------------------
[Run]

; Launch the application automatically after installation
Filename: "{app}\PySoWorks.exe"; Description: "Launch PySoWorks"; Flags: nowait postinstall skipifsilent
