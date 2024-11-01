<!--
╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║   Copyright (c) 2020 https://prrvchr.github.io                                     ║
║                                                                                    ║
║   Permission is hereby granted, free of charge, to any person obtaining            ║
║   a copy of this software and associated documentation files (the "Software"),     ║
║   to deal in the Software without restriction, including without limitation        ║
║   the rights to use, copy, modify, merge, publish, distribute, sublicense,         ║
║   and/or sell copies of the Software, and to permit persons to whom the Software   ║
║   is furnished to do so, subject to the following conditions:                      ║
║                                                                                    ║
║   The above copyright notice and this permission notice shall be included in       ║
║   all copies or substantial portions of the Software.                              ║
║                                                                                    ║
║   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,                  ║
║   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES                  ║
║   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.        ║
║   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY             ║
║   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,             ║
║   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE       ║
║   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                    ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝
-->
# [![DerbyOOo logo][1]][2] Documentation

**Ce [document][3] en français.**

**The use of this software subjects you to our [Terms Of Use][4].**

# version [1.1.4][5]

## Introduction:

**DerbyOOo** is part of a [Suite][6] of [LibreOffice][7] ~~and/or [OpenOffice][8]~~ extensions allowing to offer you innovative services in these office suites.  

This extension allows you to use [Apache Derby][9] database in embedded mode, making the database portable (a single odb file).  
It allows you to take advantage of the [ACID][10] properties of the underlying [Apache Derby][11] database.

Being free software I encourage you:
- To duplicate its [source code][12].
- To make changes, corrections, improvements.
- To open [issue][13] if needed.

In short, to participate in the development of this extension.  
Because it is together that we can make Free Software smarter.

___

## Requirement:

The DerbyOOo extension uses the jdbcDriverOOo extension to work.  
It must therefore meet the [requirement of the jdbcDriverOOo extension][14].

**Since version 1.1.0, only LibreOffice 24.2.x or higher is supported.**
If it is not possible for you to use such a version, use the previous version of DerbyOOo. But in this case, this extension cannot be installed with the [HyperSQLOOo][15] extension, see [bug #156471][16].
In addition, it will be difficult for you to migrate odb files created under lower versions of DerbyOOo. I recommend using LibreOffice 24.2.x minimum with DerbyOOo 1.1.0 or higher.

**On Linux and macOS the Python packages** used by the extension, if already installed, may come from the system and therefore **may not be up to date**.  
To ensure that your Python packages are up to date it is recommended to use the **System Info** option in the extension Options accessible by:  
**Tools -> Options -> Base drivers -> Embedded SQLite Driver -> View log -> System Info**  
If outdated packages appear, you can update them with the command:  
`pip install --upgrade <package-name>`

___

## Installation:

It seems important that the file was not renamed when it was downloaded.  
If necessary, rename it before installing it.

- [![jdbcDriverOOo logo][17]][18] Install **[jdbcDriverOOo.oxt][19]** extension [![Version][20]][19]

    This extension is necessary to use Apache Derby with all its features.

- ![DerbyOOo logo][21] Install **[DerbyOOo.oxt][22]** extension [![Version][23]][22]

Restart LibreOffice after installation.  
**Be careful, restarting LibreOffice may not be enough.**
- **On Windows** to ensure that LibreOffice restarts correctly, use Windows Task Manager to verify that no LibreOffice services are visible after LibreOffice shuts down (and kill it if so).
- **Under Linux or macOS** you can also ensure that LibreOffice restarts correctly, by launching it from a terminal with the command `soffice` and using the key combination `Ctrl + C` if after stopping LibreOffice, the terminal is not active (no command prompt).

___

## Use:

### How to create a new database:

In LibreOffice / OpenOffice go to File -> New -> Database...:

![DerbyOOo screenshot 1][24]

In step: Select database:
- select: Create a new database
- in: Emdedded database: choose: Embedded SQLite Driver
- click on button: Next

![DerbyOOo screenshot 2][25]

In step: Save and proceed:
- adjust the parameters according to your needs...
- click on button: Finish

![DerbyOOo screenshot 3][26]

Have fun...

___

## How does it work:

DerbyOOo is an [com.sun.star.sdbc.Driver][27] UNO service written in Python.  
It is an overlay to the [jdbcDriverOOo][18] extension allowing to store the Derby database in an odb file (which is, in fact, a compressed file).

Its operation is quite basic, namely:

- When requesting a connection, several things are done:
  - If it does not already exist, a **subdirectory** with name: `.` + `odb_file_name` + `.lck` is created in the location of the odb file where all Derby files are extracted from the **database** directory of the odb file (unzip).
  - The [jdbcDriverOOo][18] extension is used to get the [com.sun.star.sdbc.XConnection][28] interface from the **subdirectory** path + `/Derby`.
  - If the connection is successful, a [DocumentHandler][29] is added as an [com.sun.star.util.XCloseListener][30] and [com.sun.star.document.XStorageChangeListener][31] to the odb file.
  - If the connection is unsuccessful and the files was extracted in phase 1, the **subdirectory** will be deleted.
- When closing or renaming (Save As) the odb file, if the connection was successful, the [DocumentHandler][29] copies all files present in the **subdirectory** into the (new) **database** directory of the odb file (zip), then delete the **subdirectory**.

The main purpose of this mode of operation is to take advantage of the ACID characteristics of the underlying database in the event of an abnormal closure of LibreOffice.
On the other hand, the function: **file -> Save** has **no effect on the underlying database**. Only closing the odb file or saving it under a different name (File -> Save As) will save the database in the odb file.

___

## Has been tested with:

* LibreOffice 24.2.1.2 (x86_64)- Windows 10

* LibreOffice 24.2.1.2 - Lubuntu 22.04

* LibreOffice 24.8.0.3 (x86_64) - Windows 10(x64) - Python version 3.9.19 (under Lubuntu 22.04 / VirtualBox 6.1.38)

I encourage you in case of problem :confused:  
to create an [issue][13]  
I will try to solve it :smile:

___

## Historical:

### What has been done for version 1.0.0:

- Implementation of a new format in odb files allowing the name of the catalog of the underlying database to be taken into account.

### What has been done for version 1.1.0:

- This version is based on [fix #154989][32] available since LibreOffice 24.2.x. It can therefore work with other extensions offering integrated database services.
- Now DerbyOOo requires LibreOffice 24.2.x minimum and will load for the url: `sdbc:embedded:derby`.

### What has been done for version 1.1.1:

- Updated the [Python packaging][33] package to version 24.1.
- Updated the [Python setuptools][34] package to version 72.1.0.
- The extension will ask you to install the jdbcDriverOOo extension in versions 1.4.2 minimum.

### What has been done for version 1.1.2:

- Fixed [issue #2][35] which appears to be a regression related to the release of JaybirdOOo. Thanks to TeddyBoomer for reporting it.
- Updated the [Python setuptools][34] package to version 73.0.1.
- Logging accessible in extension options now displays correctly on Windows.
- Derby is now properly shutdown before files are recompressed into the odb file (ie: the db.lck file is no longer present in the odb file).
- The extension options are now accessible via: **Tools -> Options... -> LibreOffice Base -> Embedded Derby Driver**
- Changes to extension options that require a restart of LibreOffice will result in a message being displayed.
- Support for LibreOffice version 24.8.x.

### What has been done for version 1.1.3:

- Requires the latest version of **jdbcDriverOOo 1.4.4**.
- In the extension options it is possible to define the options: **View system tables**, **Use bookmarks** and **Force SQL mode** which will be specific to this driver.

### What has been done for version 1.1.4:

- The extension will ask you to install jdbcDriverOOo extension in versions 1.4.6 minimum.
- Modification of the extension options accessible via: **Tools -> Options... -> LibreOffice Base -> Embedded Derby Driver** in order to comply with the new graphic charter.

### What remains to be done for version 1.1.4:

- Add new language for internationalization...

- Anything welcome...

[1]: </img/derby.svg#collapse>
[2]: <https://prrvchr.github.io/DerbyOOo/>
[3]: <https://prrvchr.github.io/DerbyOOo/README_fr>
[4]: <https://prrvchr.github.io/DerbyOOo/source/DerbyOOo/registration/TermsOfUse_en>
[5]: <https://prrvchr.github.io/DerbyOOo#what-has-been-done-for-version-114>
[6]: <https://prrvchr.github.io/>
[7]: <https://www.libreoffice.org/download/download/>
[8]: <https://www.openoffice.org/download/index.html>
[9]: <https://db.apache.org/derby/>
[10]: <https://en.wikipedia.org/wiki/ACID>
[11]: <https://db.apache.org/derby/docs/10.8/ref/rrefproperdurability.html>
[12]: <https://github.com/prrvchr/DerbyOOo/>
[13]: <https://github.com/prrvchr/DerbyOOo/issues/new>
[14]: <https://prrvchr.github.io/jdbcDriverOOo/#requirement>
[15]: <https://prrvchr.github.io/HyperSQLOOo/#requirement>
[16]: <https://bugs.documentfoundation.org/show_bug.cgi?id=156471>
[17]: <https://prrvchr.github.io/jdbcDriverOOo/img/jdbcDriverOOo.svg#middle>
[18]: <https://prrvchr.github.io/jdbcDriverOOo>
[19]: <https://github.com/prrvchr/jdbcDriverOOo/releases/latest/download/jdbcDriverOOo.oxt>
[20]: <https://img.shields.io/github/v/tag/prrvchr/jdbcDriverOOo?label=latest#right>
[21]: <img/DerbyOOo.svg#middle>
[22]: <https://github.com/prrvchr/DerbyOOo/releases/latest/download/DerbyOOo.oxt>
[23]: <https://img.shields.io/github/downloads/prrvchr/DerbyOOo/latest/total?label=v1.1.4#right>
[24]: <img/DerbyOOo-1.png>
[25]: <img/DerbyOOo-2.png>
[26]: <img/DerbyOOo-3.png>
[27]: <https://www.openoffice.org/api/docs/common/ref/com/sun/star/sdbc/Driver.html>
[28]: <https://www.openoffice.org/api/docs/common/ref/com/sun/star/sdbc/XConnection.html>
[29]: <https://github.com/prrvchr/DerbyOOo/blob/main/uno/lib/uno/embedded/documenthandler.py>
[30]: <https://www.openoffice.org/api/docs/common/ref/com/sun/star/util/XCloseListener.html>
[31]: <http://www.openoffice.org/api/docs/common/ref/com/sun/star/document/XStorageChangeListener.html>
[32]: <https://gerrit.libreoffice.org/c/core/+/154989>
[33]: <https://pypi.org/project/packaging/>
[34]: <https://pypi.org/project/setuptools/>
[35]: <https://github.com/prrvchr/HyperSQLOOo/issues/2>
