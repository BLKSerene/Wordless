<!--
# Wordless: README - Chinese (Simplified)
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->

<div align="center"><img src="/doc/wl_logo.png" alt="Wordless：一款拥有多语种支持的语料库集成工具，可用于语言学、文学及翻译研究"></div>

<br>

<div align="center">
    <a href="https://ci.appveyor.com/project/BLKSerene/wordless">
        <img src="https://ci.appveyor.com/api/projects/status/github/BLKSerene/Wordless?svg=true" alt="AppVeyor"></a>
    <a href="https://dev.azure.com/blkserene/BLKSerene%20-%20Github/_build/latest?definitionId=1&branchName=main">
        <img src="https://dev.azure.com/blkserene/BLKSerene%20-%20Github/_apis/build/status/BLKSerene.Wordless?branchName=main" alt="Azure Pipelines"></a>
    <a href="https://github.com/BLKSerene/Wordless/actions?query=workflow%3ATests">
        <img src="https://github.com/BLKSerene/Wordless/workflows/Tests/badge.svg" alt="Github Actions"></a>
    <a href="https://codecov.io/gh/BLKSerene/Wordless">
        <img src="https://codecov.io/gh/BLKSerene/Wordless/branch/main/graph/badge.svg?token=ED6TW92A7G" alt="Codecov"></a>
</div>

<div align="center">
    <a href="https://github.com/PyCQA/pylint">
        <img src="https://img.shields.io/badge/linting-pylint-yellowgreen" alt="linting: pylint"></a>
    <a href="https://www.codacy.com/gh/BLKSerene/Wordless/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=BLKSerene/Wordless&amp;utm_campaign=Badge_Grade">
        <img src="https://app.codacy.com/project/badge/Grade/8226d15d1c4b4268beee760f9b59b3db" alt="Codacy"></a>
    <a href="https://sonarcloud.io/summary/new_code?id=BLKSerene_Wordless">
        <img src="https://sonarcloud.io/api/project_badges/measure?project=BLKSerene_Wordless&metric=alert_status" alt="Quality Gate Status"></a>
    <a href="https://github.com/BLKSerene/Wordless/actions?query=workflow%3ACodeQL">
        <img src="https://github.com/BLKSerene/Wordless/workflows/CodeQL/badge.svg" alt="CodeQL"></a>
    <a href="https://app.fossa.com/projects/git%2Bgithub.com%2FBLKSerene%2FWordless?ref=badge_shield">
        <img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2FBLKSerene%2FWordless.svg?type=shield" alt="FOSSA Status"></a>
</div>

<div align="center">
    <a href="https://github.com/BLKSerene/Wordless/releases">
        <img src="https://img.shields.io/github/v/release/BLKSerene/Wordless?include_prereleases&label=%E7%89%88%E6%9C%AC&sort=semver" alt="版本"></a>
    <a href="#下载">
        <img src="https://img.shields.io/github/downloads/BLKSerene/Wordless/total?label=%E4%B8%8B%E8%BD%BD%E9%87%8F" alt="下载量"></a>
    <a href="/LICENSE.txt">
        <img src="https://img.shields.io/github/license/BLKSerene/Wordless?label=%E8%AE%B8%E5%8F%AF" alt="许可"></a>
</div>

<br>

<div align="center">
    <b>中文（简体）</b> | <a href="/README_zho_tw.md">中文（繁體）</a> | <a href="https://github.com/BLKSerene/Wordless#readme">English</a>
</div>

<br>

Wordless 是一款拥有多语种支持的语料库集成工具，其可用于语言学、文学及翻译研究，由当时就读于上海外国语大学口译研究专业的硕士研究生叶磊设计并开发。

## 下载

Wordless 最新版（**2.3.0**）支持 **Windows 7/8/8.1/10/11**、**macOS 10.9 或更高版本**、**Ubuntu 16.04 或更高版本**、**Debian 9 或更高版本，**均仅支持**64位操作系统**。Intel 和 M1 处理器的苹果电脑均支持。

如需完整的更新日志，请参阅 [CHANGELOG.md](/CHANGELOG.md)（待翻译）。

版本|备注
----|---
[Windows 最新版](https://github.com/BLKSerene/Wordless/releases/download/2.3.0/wordless_2.3.0_windows.zip)|1. 解压缩所有文件<br>2. 双击运行 **Wordless/Wordless.exe**
[macOS 最新版](https://github.com/BLKSerene/Wordless/releases/download/2.3.0/wordless_2.3.0_macos.zip)|1. 解压缩所有文件<br>2. 双击运行 **Wordless.app**
[Linux 最新版](https://github.com/BLKSerene/Wordless/releases/download/2.3.0/wordless_2.3.0_linux.tar.gz)|1. 解压缩所有文件<br>2. 右键单击 **Wordless/Wordless.sh** 并选择**作为程序运行**或在**终端**中运行该 shell 脚本<br>3. 在弹出的窗口中输入你的 sudo 密码后回车<br>4. [可选] 双击 **Wordless/Wordless - Create Shortucut** 在**显示应用程序**中创建一个快捷方式
[历史版本](https://github.com/BLKSerene/Wordless/releases)|不推荐
[百度网盘](https://pan.baidu.com/s/1--ZzABrDQBZlZagWlVQMbg)|中国用户若 Github 连接不稳定可尝试该下载链接（**提取码：wdls**）

**备注 1**：Wordless 的路径中**不建议包含任何非 ASCII 字符，如汉字和带变音记号的字母等**。

**备注 2**：苹果电脑用户如遇提示 **“Wordless”已损坏，无法打开**，请打开**终端**（启动台 → 其他）后运行：

    xattr -rc /Applications/Wordless.app

请注意将 **/Applications/Wordless.app** 替换为 Wordless 在电脑上的实际存放路径（可直接拖拽 **Wordless.app** 文件至**终端**中）。然后，**再次运行 Wordless**（若程序可成功运行，终端中提示的警告可忽略）。

## 需要帮助？

如果你有任何问题、发现了软件错误、需要提供反馈信息或想要提交功能需求，你可以通过下方所列的任一支持渠道来获取开源社区的支持或直接与我联络。

支持渠道|信息
-------|----
官方文档|[文档](/doc/doc_eng.md)（待翻译）
视频教程|[B站](https://space.bilibili.com/34963752/video)
Bug 提交|[Github Issues](https://github.com/BLKSerene/Wordless/issues)
使用疑问|[Github Discussions](https://github.com/BLKSerene/Wordless/discussions)
邮件咨询|[blkserene<i>@</i>gmail<i>.</i>com](mailto:blkserene@gmail.com)
[微信](https://weixin.qq.com/)公众号|![微信公众号](/imgs/wechat_official_account.jpg)

## 引用

如果你在发表的成果中使用了 Wordless，请按如下格式进行引用。

APA（第7版）：

<pre><code>Ye, L. (2022). <i>Wordless</i> (Version 2.3.0) [Computer software]. Github. https://github.com/BLKSerene/Wordless</code></pre>

MLA（第8版）：

<pre><code>Ye Lei. <i>Wordless</i>, version 2.3.0, 2022. <i>Github</i>, https://github.com/BLKSerene/Wordless.</code></pre>

## 许可

    版权所有（C）2018-2022 叶磊
    本程序为自由软件，在自由软件联盟发布的GNU通用公共许可协议的约束下，你可以对其进行再发布及修改。协议版本为第三版或（随你）更新的版本。
    我们希望发布的这款程序有用，但不保证，甚至不保证它有经济价值和适合特定用途。详情参见GNU通用公共许可协议。
    你理当已收到一份GNU通用公共许可协议的副本，如果没有，请查阅<http://www.gnu.org/licenses/>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FBLKSerene%2FWordless.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FBLKSerene%2FWordless?ref=badge_large)

## 助力

如果你想要助力 Wordless 的开发工作，你可以在 Github 上提交 [pull requests](https://github.com/BLKSerene/Wordless/pulls) 来帮助修复程序错误、改善性能或实现新功能。

此外，你还可以在 Github 上撰写[百科](https://github.com/BLKSerene/Wordless/wiki)、制作视频教程、或帮助将用户界面及[文档](/doc/doc_eng.md)翻译为其他语言。

## 赞助

如果你愿意支持 Wordless 的开发工作，你可以通过 [PayPal](https://www.paypal.com/)、[支付宝](https://www.alipay.com/)或[微信支付](https://pay.weixin.qq.com/)进行赞助。

PayPal|支付宝|微信支付
------|-----|--------
[![PayPal](/imgs/donating_paypal.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=V2V54NYE2YD32)|![支付宝](/imgs/donating_alipay.png)|![微信支付](/imgs/donating_wechat_pay.png)

## 致谢

详情请参阅 [ACKNOWLEDGMENTS_zho_cn.md](/ACKNOWLEDGMENTS_zho_cn.md)。
