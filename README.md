# Numusic

Numusic is a text-based descriptive language for writing numbered musical notation. Details of its syntax can be found in [overview.txt](https://github.com/ansharlubis/numusic/blob/master/overview.txt).

Its purpose currently is only to calculate the optimum assignment of the musical instrument [Angklung](https://en.wikipedia.org/wiki/Angklung) in a group. An angklung can only produce a specific tone, thus it requires a lot of people to perform songs. A score written in this language can easily be converted into a list of players with their assigned instruments and play intervals, free from conflicts.

## Using Numusic

Simply run `parse.py` (optimized assignment) or `plain_parse.py` (normal assignment) with a score file.

```python
python parse.py file/path
python simple_parse.py file/path
```

Using the optimized version on `example_score.txt` prepared here will output the following result

```
Player 1, beats: 53, instruments: {'3', '13'}
intervals: [[0, 1, '13'], [2, 3, '13'], [4, 5, '13'], [6, 7, '13'], [8, 15, '13'], [16, 17, '13'], [19, 20, '13'], [21, 24, '13'], [65, 66, '13'], [74, 79, '13'], [84, 86, '13'], [91, 92, '13'], [94, 95, '13'], [101, 102, '13'], [103, 105, '13'], [106, 109, '13'], [34, 38, '3']]

Player 2, beats: 47, instruments: {'22', '12', '5'}
intervals: [[0, 15, '12'], [18, 19, '12'], [21, 22, '12'], [23, 24, '12'], [66, 71, '12'], [79, 80, '12'], [83, 84, '12'], [85, 86, '12'], [95, 96, 
'12'], [98, 100, '12'], [104, 105, '12'], [16, 17, '22'], [47, 50, '5']]

...

Player 13, beats: 31, instruments: {'F#', 'C', 'C#'}
intervals: [[32, 36, 'C'], [46, 48, 'C'], [62, 65, 'C'], [100, 102, 'C'], [86, 90, 'C#'], [52, 54, 'F#'], [38, 42, 'F#'], [104, 106, 'F#']]
```

This shows that at minimum 13 players are needed to play this score. In this example, Player 1 plays the instruments numbered `'3'` and `'13'` in the intervals listed above.

The normal assignment will output the following result

```
Player 1, beats: 48, instruments: {'13'}
intervals: [[0, 1, '13'], [2, 3, '13'], [4, 5, '13'], [6, 7, '13'], [8, 15, '13'], [16, 17, '13'], [19, 20, '13'], [21, 24, '13'], [65, 66, '13'], [74, 79, '13'], [84, 86, '13'], [91, 92, '13'], [94, 95, '13'], [101, 102, '13'], [103, 105, '13'], [106, 109, '13']]

Player 2, beats: 41, instruments: {'12'}
intervals: [[0, 15, '12'], [18, 19, '12'], [21, 22, '12'], [23, 24, '12'], [66, 71, '12'], [79, 80, '12'], [83, 84, '12'], [85, 86, '12'], [95, 96, 
'12'], [98, 100, '12'], [104, 105, '12']]

...

Player 16, beats: 13, instruments: {'F#'}
intervals: [[38, 42, 'F#'], [52, 54, 'F#'], [59, 60, 'F#'], [104, 106, 'F#']]
```

### Disclaimer

Numusic is designed as a language design project during my internship at [Nau Data Lab](https://www.nau.co.jp/company/).

なうデータ研究所で言語・方式インターンシップのプロジェクトとしてNumusicを設計した。