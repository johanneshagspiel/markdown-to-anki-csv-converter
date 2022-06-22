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

- the script itself needed to convert all of [Ebazhanov's](https://github.com/Ebazhanov/linkedin-skill-assessments-quizzes) markdown files into a .csv file that can be imported into Anki. Any images referenced in the markdown files are copied into Anki's collection.media folder and properly referenced in the flashcard. As of this writing, Anki does not support Markdown style code formatting such as `[nums[j] for j in range(n) if bitmask[j] == '1']`. Therefore, the code examples embedded in the flashcards are sometimes hard to read.
- all of the Markdown file's as ready to import [.csv files](https://github.com/johanneshagspiel/markdown-to-anki-csv-converter/tree/main/resources/csv_files)

## Tools

| Purpose                | Name                                                         |
|------------------------|--------------------------------------------------------------|
| Programming language   | [Python 3.10](https://www.python.org/)                       |
| Version control system | [Git](https://git-scm.com/)                                  |

## Installation Process

To import the .csv files in Anki, it is assumed that you already have installed [Anki](https://apps.ankiweb.net/). 

Open Anki and go to  `File -> Import` or press `Ctrl + Shift + I` and select the .csv file you want to import. Make sure that you select as type `Basic` and that you toggle the `Allow HTML in fields` option. You will most likely also want to change the name of the deck from `Default`. Now you have imported the .csv file. 

If you want to convert the markdown files for yourself, it is assumed that your operating system is Windows and that you have installed [Python](https://www.python.org/) and [Git](https://git-scm.com/) .

Clone this repository with the following command:

    git clone https://github.com/johanneshagspiel/markdown-to-anki-csv-converter.git

You will also need [Ebazhanov's markdown files](https://github.com/Ebazhanov/linkedin-skill-assessments-quizzes). First go into the resources folder:

    cd resources

In case there is already a `linkedin-skill-assessments-quizzes` folder, delete it. Now clone Ebazhanov's repository with:

    git clone https://github.com/Ebazhanov/linkedin-skill-assessments-quizzes.git

Lastly, you need to add the path to the `collection.media` folder of your Anki installation in the main method. Most likely, you can find this directory at:

    C:\Users\@Username\AppData\Roaming\Anki2\@Username\collection.media

Now you can run the main method and convert the Markdown files yourself.

## Licence

This "Markdown-to-Anki-CSV Converter" script is published under the MIT licence, which can be found in the [LICENSE](LICENSE) file. 

## References

The [LinkedIn](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/LinkedIn_icon_circle.svg/2048px-LinkedIn_icon_circle.svg.png), [Markdown](https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Markdown-mark.svg/208px-Markdown-mark.svg.png?20190322184628), [Anki](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Anki-icon.svg/1200px-Anki-icon.svg.png) and [CSV](https://commons.wikimedia.org/wiki/File:Logo_CSV.svg) logos were all taken from Wikimedia.