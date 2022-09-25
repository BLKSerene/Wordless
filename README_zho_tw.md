<!--
# Wordless: README - Chinese (Traditional)
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

<div align="center"><img src="/doc/wl_logo.png" alt="Wordless：一款擁有多語種支援的語料庫整合工具，可用於語言學、文學及翻譯研究"></div>

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
    <a href="#下載">
        <img src="https://img.shields.io/github/downloads/BLKSerene/Wordless/total?label=%E4%B8%8B%E8%BC%89%E9%87%8F" alt="下載量"></a>
    <a href="/LICENSE.txt">
        <img src="https://img.shields.io/github/license/BLKSerene/Wordless?label=%E8%A8%B1%E5%8F%AF" alt="許可"></a>
</div>

<br>

<div align="center">
    <a href="/README_zho_cn.md">中文（简体）</a> | <b>中文（繁體）</b> | <a href="https://github.com/BLKSerene/Wordless#readme">English</a>
</div>

<br>

Wordless 是一款擁有多語種支援的語料庫整合工具，其可用於語言學、文學及翻譯研究，由當時就讀於上海外國語大學口譯研究專業的碩士研究生葉磊設計並開發。

## 下載

Wordless 最新版（**2.3.0**）支援 **Windows 7/8/8.1/10/11**、**macOS 10.9 或更高版本**、**Ubuntu 16.04 或更高版本**、**Debian 9 或更高版本**，均僅支援**64位作業系統**。Intel 和 M1 處理器的蘋果電腦均支援。

如需完整的更新日誌，請參閱 [CHANGELOG.md](/CHANGELOG.md)（待翻譯）。

版本|備註
----|---
[Windows 最新版](https://github.com/BLKSerene/Wordless/releases/download/2.3.0/wordless_2.3.0_windows.zip)|1. 解壓縮所有檔案<br>2. 雙擊執行 **Wordless/Wordless.exe**
[macOS 最新版](https://github.com/BLKSerene/Wordless/releases/download/2.3.0/wordless_2.3.0_macos.zip)|1. 解壓縮所有檔案<br>2. 雙擊執行 **Wordless.app**
[Linux 最新版](https://github.com/BLKSerene/Wordless/releases/download/2.3.0/wordless_2.3.0_linux.tar.gz)|1. 解壓縮所有檔案<br>2. 右鍵單擊 **Wordless/Wordless.sh** 並選擇**作為程式執行**或在**終端**中執行該 shell 指令碼<br>3. 在彈出的視窗中輸入你的 sudo 密碼後回車<br>4. [可選] 雙擊 **Wordless/Wordless - Create Shortucut** 在**顯示應用程式**中建立一個快捷方式
[歷史版本](https://github.com/BLKSerene/Wordless/releases)|不推薦
[百度網盤](https://pan.baidu.com/s/1--ZzABrDQBZlZagWlVQMbg)|中國使用者若 Github 連線不穩定可嘗試該下載連結（**提取碼：wdls**）

**備註 1**：Wordless 的路徑中**不建議包含任何非 ASCII 字元，如漢字和帶變音記號的字母等**。

**備註 2**：macOS 系統使用者如遇提示 **“Wordless”已損壞，無法開啟**，請開啟**終端**（啟動臺 → 其他）後執行：

    xattr -rc /Applications/Wordless.app

請注意將 **/Applications/Wordless.app** 替換為 Wordless 在電腦上的實際存放路徑（可直接拖拽 **Wordless.app** 檔案至**終端**中）。然後，**再次執行 Wordless**（若程式可成功執行，終端中提示的警告可忽略）。

## 需要幫助？

如果你有任何問題、發現了軟體錯誤、需要提供反饋資訊或想要提交功能需求，你可以透過下方所列的任一支援渠道來獲取開源社群的支援或直接與我聯絡。

支援渠道|資訊
-------|----
官方文檔|[文檔](/doc/doc_eng.md)（待翻譯）
影片教程|[B站](https://space.bilibili.com/34963752/video)
Bug 提交|[Github Issues](https://github.com/BLKSerene/Wordless/issues)
使用疑問|[Github Discussions](https://github.com/BLKSerene/Wordless/discussions)
郵件諮詢|[blkserene<i>@</i>gmail<i>.</i>com](mailto:blkserene@gmail.com)
[微信](https://weixin.qq.com/)公眾號|![微信公眾號](/imgs/wechat_official_account.jpg)

## 引用

如果你在發表的成果中使用了 Wordless，請按如下格式進行引用。

APA（第7版）：

<pre><code>Ye, L. (2022). <i>Wordless</i> (Version 2.3.0) [Computer software]. Github. https://github.com/BLKSerene/Wordless</code></pre>

MLA（第8版）：

<pre><code>Ye Lei. <i>Wordless</i>, version 2.3.0, 2022. <i>Github</i>, https://github.com/BLKSerene/Wordless.</code></pre>

## 許可

    版權所有（C）2018-2022 葉磊
    本程式為自由軟體，在自由軟體聯盟發佈的GNU通用公共授權合約的約束下，你可以對其進行再發佈及修改。協議版本為第三版或（隨你）更新的版本。
    我們希望發佈的這款程式有用，但不保證，甚至不保證它有經濟價值和適合特定用途。詳情參見GNU通用公共授權合約。
    你理當已收到一份GNU通用公共授權合約的副本，如果沒有，請查閱<http://www.gnu.org/licenses/>

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FBLKSerene%2FWordless.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FBLKSerene%2FWordless?ref=badge_large)

## 助力

如果你想要助力 Wordless 的開發工作，你可以在 Github 上提交 [pull requests](https://github.com/BLKSerene/Wordless/pulls) 來幫助修復程式錯誤、改善效能或實現新功能。

此外，你還可以在 Github 上撰寫[百科](https://github.com/BLKSerene/Wordless/wiki)、製作影片教程、或幫助將使用者介面及[文檔](/doc/doc_eng.md)翻譯為其他語言。

## 贊助

如果你願意支援 Wordless 的開發工作，你可以透過 [PayPal](https://www.paypal.com/)、[支付寶](https://www.alipay.com/)或[微信支付](https://pay.weixin.qq.com/)進行贊助。

PayPal|支付寶|微信支付
------|------|--------
[![PayPal](/imgs/donating_paypal.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=V2V54NYE2YD32)|![支付寶](/imgs/donating_alipay.png)|![微信支付](/imgs/donating_wechat_pay.png)

## 致謝

詳情請參閱 [ACKNOWLEDGMENTS_zho_tw.md](/ACKNOWLEDGMENTS_zho_tw.md)。
