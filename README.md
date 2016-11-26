# FTPDownload

自动下载星历文件

# 环境

1. python2.6以上版本
2. wget
3. gzip

# 使用说明

## 配置项说明

**Nav** 为星历配置项，包括 **GPS**，**BDS**, **GLO**, **GAL**

各个导航系统内的配置有 **ftp**, **year**, **doy**, **nav**, **zip**, **path**, **interval**, 下面进行说明：

1. **ftp**：为文件下载地址，例如"ftp://igs.bkg.bund.de/NTRIP/BRDC"
2. **year**：**ture** 或者 **false**，表明在ftp下级目录是否为年份
3. **doy**：**true** 或者 **false**，表明在ftp下级目录是否为年积日
4. **nav**: **true** 或者 **false**，表明ftp下级目录是否为 **n** 文件夹，即 **年份+n**，例如 **16n**
5. **zip**: **true** 或者 **false**，表明星历文件是否被压缩
6. **path**：星历存储目录
7. **interval**：更新星历间隔, 单位为秒

注意：必须严格按照配置文件格式进行填写，有以下注意点：

1. **ftp** 地址必须用 **""** 字符串符号包括
2. **year**, **doy**, **nav**, **zip** 的取值只能为 **ture** 或者 **false**
3. **path** 必须用 **""** 字符串符号包括，在 **windows** 下的路径地址使用双斜杠,例如 **"E:\\\"**
4. 当 **path** 为空字符串 **""**, 或者 **interval** 为0时，不下载该导航系统的星历

## 使用方法

本脚本有两种使用方式，前台运行或者后台运行

- 前台运行：在 **cmd** 或者 **shell** 环境下，执行`python download.py`命令
- 后台运行：linux系统执行`nohup python download.py &`命令
