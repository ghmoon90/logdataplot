Option Explicit

' Constants
Const pythonDownloadURL = "https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe"
Const pythonInstaller = "python-3.7.9-amd64.exe"
Const requirementsFile = "requirements.txt"

' Create objects
Dim objShell, objFSO, pythonPath, objHTTP
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objHTTP = CreateObject("MSXML2.ServerXMLHTTP.6.0")

' Function to download a file
Function DownloadFile(url, savePath)
    On Error Resume Next
    objHTTP.Open "GET", url, False
    objHTTP.Send

    If objHTTP.Status = 200 Then
        Dim stream
        Set stream = CreateObject("ADODB.Stream")
        stream.Open
        stream.Type = 1 ' adTypeBinary
        stream.Write objHTTP.ResponseBody
        stream.SaveToFile savePath, 2 ' adSaveCreateOverWrite
        stream.Close
        Set stream = Nothing
        DownloadFile = True
    Else
        WScript.Echo "Failed to download " & url & ": " & objHTTP.Status & " " & objHTTP.StatusText
        DownloadFile = False
    End If
    On Error GoTo 0
End Function

' Download Python installer
If Not objFSO.FileExists(pythonInstaller) Then
    WScript.Echo "Downloading Python 3.7..."
    If Not DownloadFile(pythonDownloadURL, pythonInstaller) Then
        WScript.Quit 1
    End If
End If

' Install Python silently
If Not objFSO.FolderExists("C:\Python37\") Then
    WScript.Echo "Installing Python 3.7..."
    objShell.Run pythonInstaller & " /quiet InstallAllUsers=1 PrependPath=1", 1, True
End If

' Set the path to python.exe
pythonPath = "C:\Program Files\Python37\python.exe"

' Update pip
WScript.Echo "Updating pip..."
objShell.Run pythonPath & " -m pip install --upgrade pip", 1, True

' Install packages from requirements.txt
If objFSO.FileExists(requirementsFile) Then
    WScript.Echo "Installing packages from " & requirementsFile & "..."
    objShell.Run pythonPath & " -m pip install -r " & requirementsFile, 1, True
Else
    WScript.Echo "No " & requirementsFile & " found."
End If

WScript.Echo "Setup complete."
