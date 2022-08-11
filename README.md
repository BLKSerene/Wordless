<!--
# Wordless: README
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

<div align="center"><img src="/doc/wl_logo.png" alt="logo"></div>

---
Wordless is an integrated corpus tool with multilingual support for the study of language, literature, and translation designed and developed by Ye Lei (叶磊), then MA student in interpreting studies at Shanghai International Studies University (上海外国语大学).

<div align="center">
    <a href="https://ci.appveyor.com/project/BLKSerene/wordless">
        <img src="https://ci.appveyor.com/api/projects/status/github/BLKSerene/Wordless?svg=true" alt="AppVeyor"></a>
    <a href="https://dev.azure.com/blkserene/BLKSerene%20-%20Github/_build/latest?definitionId=1&branchName=main">
        <img src="https://dev.azure.com/blkserene/BLKSerene%20-%20Github/_apis/build/status/BLKSerene.Wordless?branchName=main" alt="Azure Pipelines"></a>
    <a href="https://github.com/BLKSerene/Wordless/actions?query=workflow%3ATests">
        <img src="https://github.com/BLKSerene/Wordless/workflows/Tests/badge.svg" alt="Github Actions"></a>
    <a href="https://codecov.io/gh/BLKSerene/Wordless">
        <img src="https://codecov.io/gh/BLKSerene/Wordless/branch/main/graph/badge.svg?token=ED6TW92A7G" alt="Codecov"></a>
    <a href="https://app.fossa.com/projects/git%2Bgithub.com%2FBLKSerene%2FWordless?ref=badge_shield">
        <img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2FBLKSerene%2FWordless.svg?type=shield" alt="FOSSA Status"></a>
</div>

<div align="center">
    <a href="https://github.com/PyCQA/pylint">
        <img src="https://img.shields.io/badge/linting-pylint-yellowgreen" alt="linting: pylint"></a>
    <a href="https://lgtm.com/projects/g/BLKSerene/Wordless/context:python">
        <img src="https://img.shields.io/lgtm/grade/python/g/BLKSerene/Wordless.svg?logo=lgtm&logoWidth=18" alt="Language grade: Python"></a>
    <a href="https://github.com/BLKSerene/Wordless/actions?query=workflow%3ACodeQL">
        <img src="https://github.com/BLKSerene/Wordless/workflows/CodeQL/badge.svg" alt="CodeQL"></a>
    <a href="https://github.com/BLKSerene/Wordless/releases">
        <img src="https://img.shields.io/github/v/release/BLKSerene/Wordless?include_prereleases&label=Release&sort=semver" alt="Release"></a>
    <a href="https://github.com/BLKSerene/Wordless#download">
        <img src="https://img.shields.io/github/downloads/BLKSerene/Wordless/total?label=Downloads" alt="Downloads"></a>
    <a href="https://github.com/BLKSerene/Wordless/blob/main/LICENSE.txt">
        <img src="https://img.shields.io/github/license/BLKSerene/Wordless?label=License" alt="License"></a>
</div>

<div align="center">
    <a href="https://app.codecov.io/gh/BLKSerene/Wordless">
        <img src="https://codecov.io/gh/BLKSerene/Wordless/branch/main/graphs/tree.svg?token=ED6TW92A7G" alt="Codecov Graph"></a>
    <a href="https://app.fossa.com/projects/git%2Bgithub.com%2FBLKSerene%2FWordless?ref=badge_large">
        <img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2FBLKSerene%2FWordless.svg?type=large" alt="FOSSA Status"></a>
</div>

## Download
The latest version (**2.2.0**) of Wordless supports **Windows 7/8/8.1/10/11**, **macOS 10.9 or later**, and **Ubuntu 14.04 or later**, all **64-bit only**.

For detailed changelog, please see [CHANGELOG.md](/CHANGELOG.md).

Release|Remarks
-------|------------
[Latest Version for Windows](https://github.com/BLKSerene/Wordless/releases/download/2.2.0/wordless_2.2.0_windows.zip)|1. Unzip the file<br>2. Double-click **Wordless/Wordless.exe** to run
[Latest Version for macOS](https://github.com/BLKSerene/Wordless/releases/download/2.2.0/wordless_2.2.0_macos.zip)|1. Unzip the file<br>2. Double-click **Wordless.app** to run
[Latest Version for Linux](https://github.com/BLKSerene/Wordless/releases/download/2.2.0/wordless_2.2.0_linux.tar.gz)|1. Unzip the file<br>2. Double-click **Wordless/Wordless** to run
[Older Versions](https://github.com/BLKSerene/Wordless/releases)|Not recommended
[Baidu Netdisk (百度网盘)](https://pan.baidu.com/s/1--ZzABrDQBZlZagWlVQMbg)|For Chinese users with slow connections to Github (**PASSWORD: wdls**)<br>中国用户若 Github 下载速度较慢可尝试从百度网盘下载 (**提取码: wdls**)

**Note 1:** It is recommended that the path to Wordless **not contain any non-ASCII chatacters, such as Chinese characters and letters with diacritics**.<br>
**备注 1**：Wordless 的路径中**不建议包含任何非 ASCII 字符，如汉字和带变音记号的字母等**。

**Note 2:** If your Mac says that **“Wordless” is damaged and can’t be opened**, please open **Terminal** (Launchpad → Other) and run:<br>
**备注 2**：如果苹果电脑提示 **“Wordless”已损坏，无法打开**，请打开**终端**（启动台 → 其他）后运行：

    xattr -rc /Applications/Wordless.app

remember to replace **/Applications/Wordless.app** with the actual path of Wordless on your computer (you could drag **Wordless.app** to the **Terminal**). Then, **run Wordless again** (the warning prompted in Terminal could be ignored if the program could be successfully opened).<br>
记得把 **/Applications/Wordless.app** 替换为 Wordless 在电脑上的实际路径（可直接拖拽 **Wordless.app** 文件至**终端**中）。然后，**再次运行 Wordless**（如果程序可成功打开，终端中提示的警告可忽略）。

<span id="doc"></span>
## Documentation
- [Documentation - English](/doc/doc_eng.md)
- 文档 - 汉语（待添加）

## Need Help?
If you encounter a problem, find a bug, or require any further information, feel free to ask questions, submit bug reports, or provide feedback by [creating an issue](https://github.com/BLKSerene/Wordless/issues/new) on Github if you fail to find the answer by searching [existing issues](https://github.com/BLKSerene/Wordless/issues) first.

If you need to post sample texts or other information that cannot be shared or you do not want to share publicly, you may send me an email.

Channel      |Contact Information
:-----------:|-------------------
Documentation|https://github.com/BLKSerene/Wordless#documentation
Email        |[blkserene<i>@</i>gmail<i>.</i>com](mailto:blkserene@gmail.com)
[WeChat](https://www.wechat.com/en/) Official Account|![WeChat Official Account](/imgs/wechat_official_account.jpg)

## Citing
If you publish work that uses Wordless, please cite as follows.

APA (7th Edition):

<pre><code>Ye, L. (2022). <i>Wordless</i> (Version 2.2.0) [Computer software]. Github. https://github.com/BLKSerene/Wordless</code></pre>

MLA (8th Edition):

<pre><code>Ye Lei. <i>Wordless</i>, version 2.2.0, 2022. <i>Github</i>, https://github.com/BLKSerene/Wordless.</code></pre>

## License
    Copyright (C) 2018-2022  Ye Lei (叶磊)
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Contributing
If you have an interest in helping the development of Wordless, you may contribute bug fixes, enhancements, or new features by [creating a pull request](https://github.com/BLKSerene/Wordless/pulls) on Github.

Besides, you may contribute by submitting enhancement proposals or feature requests, write tutorials or [Github Wiki](https://github.com/BLKSerene/Wordless/wiki) for Wordless, or helping me translate Wordless and its documentation to other languages.

## Donating
If you would like to support the development of Wordless, you may donate via [PayPal](https://www.paypal.com/), [Alipay](https://global.alipay.com/), or [WeChat Pay](https://pay.weixin.qq.com/index.php/public/wechatpay_en).

PayPal|Alipay|WeChat Pay
------|------|----------
[![PayPal](/imgs/donating_paypal.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=V2V54NYE2YD32)|![Alipay](/imgs/donating_alipay.png)|![WeChat Pay](/imgs/donating_wechat_pay.png)

## Acknowledgments
See [ACKNOWLEDGMENTS.md](/ACKNOWLEDGMENTS.md) for details.
