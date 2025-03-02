# 修复剩余未重命名的文件和文件夹

# 修复文件14
$file14 = "14梵汉对照手机版-不空羂索心王母、秘密心、秘密小心、自在王、心、心中心、身印陀罗尼。圣观自在菩萨千转灭罪、阿末[齿来]观自在、如意轮、观自在甘露、观自在闻持、观自在心.txt"
$newFile14 = $file14 -replace "汉对照手机版", "音陀罗尼"
if (Test-Path $file14) {
    Write-Host "重命名文件: $file14 -> $newFile14"
    Rename-Item -Path $file14 -NewName $newFile14 -Force
} else {
    Write-Host "文件不存在: $file14"
}

# 修复文件夹14
$folder14 = "梵汉对照手机版-不空羂索心王母、秘密心、秘密小心、自在王、心、心中心、身印陀罗尼。圣观自在菩萨千转灭罪、阿末[齿来]观自在、如意轮、观自在甘露、观自在闻持、观自在心_audio"
$newFolder14 = "14 梵音陀罗尼-不空羂索心王母、秘密心、秘密小心、自在王、心、心中心、身印陀罗尼。圣观自在菩萨千转灭罪、阿末[齿来]观自在、如意轮、观自在甘露、观自在闻持、观自在心_audio"
if (Test-Path $folder14 -PathType Container) {
    Write-Host "重命名文件夹: $folder14 -> $newFolder14"
    Rename-Item -Path $folder14 -NewName $newFolder14 -Force
} else {
    Write-Host "文件夹不存在: $folder14"
}

# 修复文件夹22
$folder22 = "月藏菩萨、六门、八名普密、变食真言、楞伽经、除一切毒、思益经、降甘雨、止风雨、止恶风雹雨_audio"
$newFolder22 = "22 月藏菩萨、六门、八名普密、变食真言、楞伽经、除一切毒、思益经、降甘雨、止风雨、止恶风雹雨_audio"
if (Test-Path $folder22 -PathType Container) {
    Write-Host "重命名文件夹: $folder22 -> $newFolder22"
    Rename-Item -Path $folder22 -NewName $newFolder22 -Force
} else {
    Write-Host "文件夹不存在: $folder22"
}

# 修复文件夹1
$folder1 = "梵音陀罗尼-佛顶系列咒语 _audio"
$newFolder1 = "1 梵音陀罗尼-佛顶系列咒语 _audio"
if (Test-Path $folder1 -PathType Container) {
    Write-Host "重命名文件夹: $folder1 -> $newFolder1"
    Rename-Item -Path $folder1 -NewName $newFolder1 -Force
} else {
    Write-Host "文件夹不存在: $folder1"
}

# 修复文件夹9
$folder9 = "无垢净光、智矩、大般涅盘经摧魔、持世、花聚、胜幢臂、一切诸法入无量门-A4 20241001_audio"
$newFolder9 = "9 无垢净光、智矩、大般涅盘经摧魔、持世、花聚、胜幢臂、一切诸法入无量门-A4 20241001_audio"
if (Test-Path $folder9 -PathType Container) {
    Write-Host "重命名文件夹: $folder9 -> $newFolder9"
    Rename-Item -Path $folder9 -NewName $newFolder9 -Force
} else {
    Write-Host "文件夹不存在: $folder9"
}

Write-Host "修复完成!" 