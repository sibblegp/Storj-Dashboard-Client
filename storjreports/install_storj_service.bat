@if (1==1) @if(1==0) @ELSE
@echo off&SETLOCAL ENABLEEXTENSIONS
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"||(
    cscript //E:JScript //nologo "%~f0" %*
    @goto :EOF
)
FOR %%A IN (%*) DO (
    "%%A"
)
@goto :EOF
@end @ELSE
args = WScript.Arguments;
newargs = "";
for (var i = 0; i < args.length; i++) {
    newargs += args(i) + " ";
}
objFSO = WScript.CreateObject("Scripting.FileSystemObject");
objFile = objFSO.CreateTextFile("storj_install_log.log", true);
objFile.Writeline(newargs);
ShA=new ActiveXObject("Shell.Application");
ShA.ShellExecute("python","C:\\Users\\George\\apps\\storjclient\\storjreports\\windows_service.py install" + " ","","runas",0);
@end