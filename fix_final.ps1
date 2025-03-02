# 修复最后的文件和文件夹

$fileFullName = "14梵汉对照手机版-不空羂索心王母、秘密心、秘密小心、自在王、心、心中心、身印陀罗尼。圣观自在菩萨千转灭罪、阿末[齿来]观自在、如意轮、观自在甘露、观自在闻持、观自在心.txt"
$newFileFullName = $fileFullName -replace "汉对照手机版", "音陀罗尼"

Write-Host "正在尝试修复文件: $fileFullName"
if (Test-Path $fileFullName) {
    Write-Host "重命名文件: $fileFullName -> $newFileFullName"
    Rename-Item -Path $fileFullName -NewName $newFileFullName -Force
} else {
    Write-Host "文件不存在: $fileFullName"
}

$folderFullName = "梵汉对照手机版-不空羂索心王母、秘密心、秘密小心、自在王、心、心中心、身印陀罗尼。圣观自在菩萨千转灭罪、阿末[齿来]观自在、如意轮、观自在甘露、观自在闻持、观自在心_audio"
$newFolderFullName = "14 梵音陀罗尼-不空羂索心王母、秘密心、秘密小心、自在王、心、心中心、身印陀罗尼。圣观自在菩萨千转灭罪、阿末[齿来]观自在、如意轮、观自在甘露、观自在闻持、观自在心_audio"

Write-Host "正在尝试修复文件夹: $folderFullName"
if (Test-Path $folderFullName -PathType Container) {
    Write-Host "重命名文件夹: $folderFullName -> $newFolderFullName"
    Rename-Item -Path $folderFullName -NewName $newFolderFullName -Force
} else {
    Write-Host "文件夹不存在: $folderFullName"
}

Write-Host "修复完成!" 