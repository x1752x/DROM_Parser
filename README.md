# DROM.RU Parser

This parser scrapes Russian car sales service named <a href="http://drom.ru">DROM</a>. DROM's built-in advanced search allows you to specify many parameters, but not the initial registration date, which is vital for some resellers, for whom this project was originally created.
This parser solves this problem, in addition to automating the process of searching for the necessary cars. <br>

Desktop application, mainly for work under Windows 10. Working on older versions is theoretically possible when compiled with an older version of Python. Working under Linux or macOS is not guaranteed, but is theoretically possible with additional modifications.
This app has a simple and independent API, which makes it theoretically possible to also create a web and/or mobile version of it.

Parsing is performed using static attributes, but changes in layout of DROM frontend are still possible, which will require fixes. There is no dynamic interaction like Selenium under the hood.

## How to run
You will need:
* OS: Windows 10 and later

Unzip the archive with the program to any directory and run the executable.

## How to build
You will need:
* Python 3.13.2 and newer (with tkinter)
* See `requirements.txt`

Run the `build.ps1` script and you're done.