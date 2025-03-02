# 获取所有包含"汉对照手机版"的txt文件
$txtFiles = Get-ChildItem -Filter "*汉对照手机版*.txt"

# 创建重命名映射
$renames = @{}
foreach ($file in $txtFiles) {
    $newName = $file.Name -replace "汉对照手机版", "音陀罗尼"
    $renames[$file.Name] = $newName
}

# 获取所有包含"汉对照手机版"的目录
$folders = Get-ChildItem -Directory -Filter "*汉对照手机版*"

# 创建目录重命名映射
$dirRenames = @{}
foreach ($folder in $folders) {
    $folderName = $folder.Name
    # 提取文件名前面的数字（如果有）
    $numberMatch = [regex]::Match($folderName, "^(\d+)")
    $number = ""
    if ($numberMatch.Success) {
        $number = $numberMatch.Groups[1].Value
    }
    else {
        # 尝试匹配文件夹名中的数字
        $numberMatch = [regex]::Match($folderName, "汉对照手机版-.*?(\d+)")
        if ($numberMatch.Success) {
            $number = $numberMatch.Groups[1].Value
        }
        else {
            # 如果还是找不到，从关联的txt文件名中提取
            foreach ($txtFile in $txtFiles) {
                if ($folderName.Contains($txtFile.BaseName)) {
                    $numberMatch = [regex]::Match($txtFile.Name, "^(\d+)")
                    if ($numberMatch.Success) {
                        $number = $numberMatch.Groups[1].Value
                        break
                    }
                }
            }
        }
    }
    
    # 如果找不到数字，则使用一个默认值
    if ([string]::IsNullOrEmpty($number)) {
        $number = (Get-Random -Minimum 100 -Maximum 999).ToString()
    }
    
    # 创建新的文件夹名（替换文本并添加序号）
    $newFolderName = $folderName -replace "汉对照手机版", "音陀罗尼"
    $newFolderName = "$number $newFolderName"
    
    $dirRenames[$folderName] = $newFolderName
}

# 重命名txt文件
foreach ($key in $renames.Keys) {
    if (Test-Path $key) {
        Write-Host "重命名文件: $key -> $($renames[$key])"
        Rename-Item -Path $key -NewName $renames[$key] -Force
    } else {
        Write-Host "文件不存在: $key"
    }
}

# 重命名文件夹
foreach ($key in $dirRenames.Keys) {
    if (Test-Path $key -PathType Container) {
        Write-Host "重命名文件夹: $key -> $($dirRenames[$key])"
        Rename-Item -Path $key -NewName $dirRenames[$key] -Force
    } else {
        Write-Host "文件夹不存在: $key"
    }
}

Write-Host "重命名完成!" 