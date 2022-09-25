<!--
# Wordless: README - English
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

<div align="center"><img src="/doc/wl_logo.png" alt="Wordless: An Integrated Corpus Tool With Multilingual Support for the Study of Language, Literature, and Translation"></div>

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
        <img src="https://img.shields.io/github/v/release/BLKSerene/Wordless?include_prereleases&label=Release&sort=semver" alt="Release"></a>
    <a href="#download">
        <img src="https://img.shields.io/github/downloads/BLKSerene/Wordless/total?label=Downloads" alt="Downloads"></a>
    <a href="/LICENSE.txt">
        <img src="https://img.shields.io/github/license/BLKSerene/Wordless?label=License" alt="License"></a>
</div>

<br>

<div align="center">
    <a href="/README_zho_cn.md">中文 (简体)</a> | <a href="/README_zho_tw.md">中文 (繁體)</a> | <b>English</b>
</div>

<br>

Wordless is an integrated corpus tool with multilingual support for the study of language, literature, and translation designed and developed by Ye Lei (叶磊), then MA student in interpreting studies at Shanghai International Studies University (上海外国语大学).

## Download

The latest version (**2.3.0**) of Wordless supports **Windows 7/8/8.1/10/11**, **macOS 10.9 or later**, and **Ubuntu 16.04 or later**, all **64-bit only**. Both Intel-based and M1-based MacBooks are supported.

For a detailed changelog, please see [CHANGELOG.md](/CHANGELOG.md).

Release|Remarks
-------|-------
[Latest Release for Windows](https://github.com/BLKSerene/Wordless/releases/download/2.3.0/wordless_2.3.0_windows.zip)|1. Extract all files<br>2. Double-click **Wordless/Wordless.exe** to run
[Latest Release for macOS](https://github.com/BLKSerene/Wordless/releases/download/2.3.0/wordless_2.3.0_macos.zip)|1. Extract all files<br>2. Double-click **Wordless.app** to run
[Latest Release for Linux](https://github.com/BLKSerene/Wordless/releases/download/2.3.0/wordless_2.3.0_linux.tar.gz)|1. Extract all files<br>2. Right-click **Wordless/Wordless.sh** and select **Run as a program** or run the shell script from **Terminal**<br>3. Type your sudo password in the prompted window and press Enter<br>4. [Optional] Double-click **Wordless/Wordless - Create Shortucut** to create a shortcut in **Show Applications**
[Past Releases](https://github.com/BLKSerene/Wordless/releases)|Not recommended
[Baidu Netdisk](https://pan.baidu.com/s/1--ZzABrDQBZlZagWlVQMbg)|For Chinese users with unstable connections to Github (**PASSWORD: wdls**)

**Note 1:** It is recommended that the path to Wordless **not contain any non-ASCII chatacters, such as Chinese characters and letters with diacritics**.<br>

**Note 2:** If your Mac says that **“Wordless” is damaged and can’t be opened**, please open **Terminal** (Launchpad → Other) and run:<br>

    xattr -rc /Applications/Wordless.app

remember to replace **/Applications/Wordless.app** with the actual path of Wordless on your computer (you could drag **Wordless.app** to the **Terminal**). Then, **run Wordless again** (the warning prompted in Terminal could be ignored if the program could be successfully opened).<br>

## Need Help?

If you have any questions, find software bugs, need to provide feedback, or want to submit feature requests, you may seek support from the open-source community or contact me directly via any of the support channels listed below.

Support Channel       |Information
----------------------|-----------
Official Documentation|[Documentation](/doc/doc_eng.md)
Tutorial Videos       |[bilibili](https://space.bilibili.com/34963752/video)
Bug Reports           |[Github Issues](https://github.com/BLKSerene/Wordless/issues)
Usage Questions       |[Github Discussions](https://github.com/BLKSerene/Wordless/discussions)
Email Support         |[blkserene<i>@</i>gmail<i>.</i>com](mailto:blkserene@gmail.com)
[WeChat](https://www.wechat.com/en/) Official Account|![WeChat Official Account](/imgs/wechat_official_account.jpg)

## Citing

If you publish work that uses Wordless, please cite as follows.

APA (7th Edition):

<pre><code>Ye, L. (2022). <i>Wordless</i> (Version 2.3.0) [Computer software]. Github. https://github.com/BLKSerene/Wordless</code></pre>

MLA (8th Edition):

<pre><code>Ye Lei. <i>Wordless</i>, version 2.3.0, 2022. <i>Github</i>, https://github.com/BLKSerene/Wordless.</code></pre>

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

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FBLKSerene%2FWordless.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FBLKSerene%2FWordless?ref=badge_large)

## Contributing

If you would like to contribute to the development of Wordless, you can help with bug fixes, performance enhancements, or implementation of new features by submitting [pull requests](https://github.com/BLKSerene/Wordless/pulls) on Github.

Besides, you may contribute by writing [wikis](https://github.com/BLKSerene/Wordless/wiki) on Github, making tutorial videos, or helping with the translation of the user interface and [documentation](/doc/doc_eng.md) into other languages.

## Donating

If you would like to support the development of Wordless, you may donate via [PayPal](https://www.paypal.com/), [Alipay](https://global.alipay.com/), or [WeChat Pay](https://pay.weixin.qq.com/index.php/public/wechatpay_en).

PayPal|Alipay|WeChat Pay
------|------|----------
[![PayPal](/imgs/donating_paypal.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=V2V54NYE2YD32)|![Alipay](/imgs/donating_alipay.png)|![WeChat Pay](/imgs/donating_wechat_pay.png)

## Acknowledgments

See [ACKNOWLEDGMENTS.md](/ACKNOWLEDGMENTS.md) for details.
