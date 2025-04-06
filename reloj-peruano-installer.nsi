; Script de instalación para Reloj Peruano
!include "MUI2.nsh"

; Definir iconos
!define MUI_ICON "reloj.ico"
!define MUI_UNICON "reloj.ico"

Name "Reloj Peruano"
OutFile "InstaladorRelojPeruano.exe"
InstallDir "$PROGRAMFILES\Reloj Peruano"
RequestExecutionLevel admin

; Páginas del instalador
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Páginas del desinstalador
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Spanish"

Section "Instalar"
  SetOutPath "$INSTDIR"
  
  ; Archivos de la aplicación
  File /r "build\exe.win-amd64-3.x\*.*"
  
  ; Asegurarse de que el icono está presente
  File "reloj.ico"
  
  ; Crear acceso directo en el menú de inicio
  CreateDirectory "$SMPROGRAMS\Reloj Peruano"
  CreateShortcut "$SMPROGRAMS\Reloj Peruano\Reloj Peruano.lnk" "$INSTDIR\RelojPeruano.exe" "" "$INSTDIR\reloj.ico"
  CreateShortcut "$DESKTOP\Reloj Peruano.lnk" "$INSTDIR\RelojPeruano.exe" "" "$INSTDIR\reloj.ico"
  
  ; Configurar inicio automático
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "RelojPeruano" '"$INSTDIR\RelojPeruano.exe"'
  
  ; Información de desinstalación
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelojPeruano" "DisplayName" "Reloj Peruano"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelojPeruano" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelojPeruano" "DisplayIcon" "$INSTDIR\reloj.ico"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelojPeruano" "Publisher" "Tu Nombre"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelojPeruano" "DisplayVersion" "1.0"
  
  ; Crear desinstalador
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateShortcut "$SMPROGRAMS\Reloj Peruano\Desinstalar.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\reloj.ico"
SectionEnd

Section "Uninstall"
  ; Eliminar archivos
  RMDir /r "$INSTDIR"
  
  ; Eliminar accesos directos
  RMDir /r "$SMPROGRAMS\Reloj Peruano"
  Delete "$DESKTOP\Reloj Peruano.lnk"
  
  ; Eliminar registro de inicio automático
  DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "RelojPeruano"
  
  ; Eliminar información de desinstalación
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelojPeruano"
SectionEnd