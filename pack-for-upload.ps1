# 打包项目用于上传
$source = "C:\Users\刘涛\Desktop\hospital-vuln-mcp"
$dest = "C:\Users\刘涛\Desktop\hospital-vuln-mcp-upload.zip"

# 删除旧文件
if (Test-Path $dest) { Remove-Item $dest }

# 压缩（排除 .git）
$items = Get-ChildItem $source -Exclude ".git"
Compress-Archive -Path $items.FullName -DestinationPath $dest

Write-Host "✅ 打包完成: $dest"
Write-Host "文件大小: $([math]::Round((Get-Item $dest).Length / 1MB, 2)) MB"
