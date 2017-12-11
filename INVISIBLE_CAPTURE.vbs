Set WshShell = CreateObject("WScript.Shell") 
Set objWshShell = WScript.CreateObject("WScript.Shell")

' strText = "Are you sure you want to run the " & Chr(13)
' strText = strText & "webcam recorder?"
' strTitle = "Run webcam recorder"
' intType = vbYesNoCancel + vbQuestion + vbDefaultButton2
' intResult = WshShell.Popup(strText, ,strTitle, intType)
' WScript.Echo "you clicked " & intResult 

WshShell.Popup "Running Batch file .. " , 1, "Please Wait"

WshShell.Run chr(34) & "C:\Users\vidabas\Desktop\Cloud\Notes\batchfile\capture.bat" & Chr(34), 3, TRUE  ' use 0 instead of 3 for invisible window. refer https://msdn.microsoft.com/en-us/library/d5fk67ky(VS.85).aspx
WshShell.Run chr(34) & "C:\Users\vidabas\Desktop\Cloud\Notes\batchfile\upload.bat" & Chr(34), 3, TRUE   'TRUE means wait for the file to complete execution

Set WshShell = Nothing
