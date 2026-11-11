# 打包：同步前端到 ui\，并把授权说明放进成品目录。
# 编译仍按更新日志第 32、36 节的 csc 命令执行，本脚本不负责编译。
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent (Split-Path -Parent $here)
$src  = Join-Path $root '前端\proto'
$ui   = Join-Path $here 'dist\莊春江讀經站\ui'
$notice = Join-Path $here 'src\授權說明.txt'

Write-Host '[1/3] 同步前端 -> ui'
if (-not (Test-Path $src)) { throw "找不到前端目录：$src" }
robocopy $src $ui /MIR /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy 失败，退出码 $LASTEXITCODE" }

Write-Host '[2/3] 写入授权说明'
if (-not (Test-Path $notice)) { throw "找不到授权说明：$notice" }
foreach ($d in @('dist\莊春江讀經站', 'dist\單文件版')) {
  $target = Join-Path $here $d
  if (Test-Path $target) {
    Copy-Item $notice (Join-Path $target '授權說明.txt') -Force
    Write-Host "  -> $d\授權說明.txt"
  }
}

Write-Host '[3/3] 完成'
Write-Host '注意：單文件版 exe 与 zip 需按日志第 38 节重新生成，才会包含新的 ui 与授权页脚。'
