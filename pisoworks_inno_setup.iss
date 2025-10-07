;------------------------------------------------------------
; Inno Setup script for PiSoWorks
; Version: 1.0.4
; Purpose: Creates a Windows installer with app, docs, and shortcuts
;------------------------------------------------------------

; Define application name (used throughout the script for consistency)
#define APP_NAME "PiSoWorks"
#define COMPANY "piezosystem jena GmbH"
#define VerFile FileOpen("VERSION")

; Read the product version from version file - it can be something like 1.0.4 for a release or 1.0.5.dev3 for a pre-release
#define PRODUCT_VERSION FileRead(VerFile)

; Find first non-digit/dot and make a version like 1.0.5.dev3 to 1.0.5 - this is required for VersionInfoVersion
#define FILE_VERSION Copy(PRODUCT_VERSION, 1, Pos("d", PRODUCT_VERSION) - 1)


;------------------------------------------------------------
; Setup Section: Installer configuration
;------------------------------------------------------------
[Setup]

; Application name shown in installer
AppName={#APP_NAME}

; Application version
AppVersion={#PRODUCT_VERSION}

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
UninstallDisplayIcon={app}\PiSoWorks.exe

; Installer icon file
SetupIconFile=pisoworks\assets\app_icon.ico

; Use modern wizard UI style
WizardStyle=modern

; The version information to show if you right click on the setup file and go to details tab
VersionInfoVersion={#FILE_VERSION} 
VersionInfoCompany={#COMPANY}
VersionInfoDescription=PiSoWorks Setup
VersionInfoCopyright=© 2025 {#COMPANY}


;------------------------------------------------------------
; Files Section: Files to be installed
;------------------------------------------------------------
[Files]

; Main executable
Source: "dist\PiSoWorks.exe"; DestDir: "{app}"; Flags: ignoreversion

; Documentation (all files and subfolders from doc\_build)
Source: "doc\_build\*"; DestDir: "{app}\doc"; Flags: ignoreversion recursesubdirs createallsubdirs

;------------------------------------------------------------
; Icons Section: Shortcuts
;------------------------------------------------------------
[Icons]

; Start Menu shortcut to the main application
Name: "{userprograms}\PiSoWorks"; Filename: "{app}\PiSoWorks.exe"

; Start Menu shortcut to documentation (opens index.html in browser)
Name: "{userprograms}\PiSoWorks Documentation"; Filename: "{app}\doc\index.html"

; Optional desktop shortcut to the main application
Name: "{userdesktop}\PiSoWorks"; Filename: "{app}\PiSoWorks.exe"; Tasks: desktopicon

;------------------------------------------------------------
; Tasks Section: Optional installation components
;------------------------------------------------------------
[Tasks]

; Task for creating a desktop shortcut (checked by default)
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"


;------------------------------------------------------------
; Run Section: Post-install actions
;------------------------------------------------------------
[Run]

; Launch the application automatically after installation
Filename: "{app}\PiSoWorks.exe"; Description: "Launch PiSoWorks"; Flags: nowait postinstall skipifsilent
