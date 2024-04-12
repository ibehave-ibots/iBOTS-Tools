@REM Comment here
winget install --accept-package-agreements --id=Microsoft.VCLibs.Desktop.14 ^
&& winget install --accept-package-agreements --id=Microsoft.VCRedist.2010.x64 ^
&& winget install --accept-package-agreements --id=Microsoft.VCRedist.2010.x86 ^
&& winget install --accept-package-agreements --id=Microsoft.VCRedist.2015+.x64 ^
&& winget install --accept-package-agreements --id=Microsoft.VCRedist.2015+.x86 ^
&& winget install --accept-package-agreements --id=Microsoft.DotNet.DesktopRuntime.6
