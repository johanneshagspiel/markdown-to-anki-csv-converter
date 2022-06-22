<img src=resources/img/markdown-to-anki-csv-converter_logo.JPG alt="<Markdown-to-Anki-CSV Converter Logo" width="534" height="100">

--------------------------------------------------------------------------------
[![MIT License](https://img.shields.io/github/license/johanneshagspiel/markdown-to-anki-csv-converter)](LICENSE)
[![Top Language](https://img.shields.io/github/languages/top/johanneshagspiel/markdown-to-anki-csv-converter)](https://github.com/johanneshagspiel/markdown-to-anki-csv-converter)
[![Latest Release](https://img.shields.io/github/v/release/johanneshagspiel/markdown-to-anki-csv-converter)](https://github.com/johanneshagspiel/markdown-to-anki-csv-converter/releases/)

# Markdown-to-Anki-CSV Converter

This repository contains a script to convert the LinkedIn Skill Assessment Quizzes from [Ebazhanov](https://github.com/Ebazhanov/linkedin-skill-assessments-quizzes) which are in the Markdown format into csv files that can be imported into Anki as well as the converted files.

[Anki](https://apps.ankiweb.net/) is a popular open-source flashcard program that follows a spaced-repetition approach so that users can learn topics more effectively in less time.

## Features

This repository includes:

- the script itself needed to convert one of [Ebazhanov's](https://github.com/Ebazhanov/linkedin-skill-assessments-quizzes) markdown files to a .csv file that can be imported into Anki. This conversion
  - reformats the markdown
  - moves any image associated to a question into the anki collections folder
- 

## Tools

| Purpose              | Name                                                                                            |
|----------------------|-------------------------------------------------------------------------------------------------|
| Programming language | [Python 3.10]                                                                                   |(
| Version              | [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install) with Ubuntu |

## Installation Process

It is assumed that the users operating system is Windows. 

- Download and install [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) preferably with the Ubuntu 18.04 LTS distribution.
- To run the shell scripts, start WSL, move into the directory of this repository and execute the scripts with ./{name_of_script}.sh

## Licence

This "Markdown-to-Anki-CSV Converter" script is published under the MIT licence, which can be found in the [LICENSE](LICENSE) file. 

## References

The [LinkedIn](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/LinkedIn_icon_circle.svg/2048px-LinkedIn_icon_circle.svg.png), [Markdown](https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Markdown-mark.svg/208px-Markdown-mark.svg.png?20190322184628), [Anki](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Anki-icon.svg/1200px-Anki-icon.svg.png) and [CSV](https://commons.wikimedia.org/wiki/File:Logo_CSV.svg) logos were all taken from Wikimedia.