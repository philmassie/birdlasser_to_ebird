# Fix source file path
# [environment]::Commandline

# $srcpathfull = ''
# foreach ($arg in $args) {
# 	$srcpathfull += $arg + ' '
# }
# $srcpathfull= $srcpathfull.Trim()
conda activate py37
# python.exe "D:\My Folders\vscode_projects\2020\birdlasser_to_ebird\birdlasser_to_ebird.py" $srcpathfull
python.exe "D:\My Folders\vscode_projects\2020\birdlasser_to_ebird\birdlasser_to_ebird.py" $args