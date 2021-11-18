# inflation-calculator
A tool for projecting future consumer price index expenditures using data from the U.S. Bureau of Labor Statistics

## dependencies

```bash
pip install pandas
pip install beautifulsoup4
pip install requests
```

## usage

```bash
./main.py
```
runs the script using default parameters (uses test-1.xlsx file)

```bash
./main.py your_file_name.xlsx
```
runs the script using the file name provided as a command line argument (file must be saved in the \files directory)

the file (template.xlsx) has been provided for the creation of new files with personal data for calculations

```bash
https://www.bls.gov/cpi/tables/supplemental-files/news-release-table2-202110.xlsx :: 0
https://www.bls.gov/cpi/tables/supplemental-files/news-release-table2-202109.xlsx :: 1
https://www.bls.gov/cpi/tables/supplemental-files/news-release-table2-202108.xlsx :: 2
...
select table:
```
the most recent files from U.S. B.L.S. website are pulled for selection by user (select using number to the right of url)

```bash
name file:
```
you are prompted to name the output file to be saved in the \files firectory with calculated projections

```bash
          category                    current annual      projected annual      current month     projected month
0         net income                  63179.00            67096.09              5264.92           5292.99
1         food at home                3935.00             4147.49               327.92            330.76
                                                          ...
                                                          ...
                                                          ...
20        other personal services     600.00              624.00000             50.00             50.166667
```
the results are printed to the console

## contributors

Austin Gray