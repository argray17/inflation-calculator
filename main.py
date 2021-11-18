import pandas as pd
import re
import requests
import warnings
from bs4 import BeautifulSoup


key_expenditure_categories = ['all items',
                              'food at home',
                              'food away from home',
                              'energy commodities',
                              'energy services',
                              'household furnishings and supplies',
                              'apparel',
                              'transportation commodities less motor fuel',
                              'medical care commodities',
                              'recreation commodities',
                              'education and communication commodities',
                              'alcoholic beverages',
                              'other goods',
                              'shelter',
                              'water and sewer and trash collection services',
                              'household operations',
                              'medical care services',
                              'transportation services',
                              'recreation services',
                              'education and communication services',
                              'other personal services']


def load_cpi_data(cpi_file_path):
    with warnings.catch_warnings(record=True):
        warnings.simplefilter('always')
        cpi_data = pd.read_excel(cpi_file_path, sheet_name=0, skiprows=5)

    cpi_data = cpi_data.dropna()
    cpi_data = cpi_data.drop(cpi_data.columns[[0, 2, 4]], axis=1)

    for index, row in cpi_data.iterrows():
        expenditure_category = re.sub(r'[^a-zA-Z ]', '', row[0]).lower()

        if expenditure_category not in key_expenditure_categories:
            cpi_data = cpi_data.drop([index])

    cpi_data = cpi_data.reset_index(drop=True)

    for index, row in cpi_data.iterrows():
        cpi_data.iat[index, 0] = re.sub(r'[^a-zA-Z ]', '', row[0]).lower()

    cpi_data.columns = ['expenditure category', 'year to month', 'two months ago', 'last month', 'this month']

    return cpi_data


def get_url_paths():
    url = 'https://www.bls.gov/cpi/tables/supplemental-files'
    ext = 'xlsx'
    response = requests.get(url)

    if response.ok:
        response_text = response.text
    else:
        return response.raise_for_status()

    soup = BeautifulSoup(response_text, 'html.parser')
    parent = ['https://www.bls.gov' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
    return parent


def select_xlsx():
    paths = get_url_paths()
    result_set = []

    for i in range(len(paths)):
        if 'table2' in paths[i]:
            result_set.append(paths[i])
            print(f'{paths[i]} :: {len(result_set)-1}')
    while True:
        user_selection = int(input('select table:'))
        if 0 <= user_selection < len(result_set):
            return result_set[user_selection]
        else:
            print('invalid input')


def load_user_data(local_file_path):
    with warnings.catch_warnings(record=True):
        warnings.simplefilter('always')
        user_data = pd.read_excel(local_file_path, sheet_name=0)
    user_data = user_data.dropna()
    user_data = user_data.reset_index(drop=True)
    return user_data


def main(file_name):
    cpi_data = load_cpi_data(cpi_file_path=select_xlsx())
    user_data = load_user_data('files/'+file_name+'.xlsx')

    projected_costs = pd.DataFrame()
    projected_costs['category'] = user_data['category']
    projected_costs['current annual'] = user_data['annual']
    projected_costs['projected annual'] = user_data['annual'] * ((cpi_data['year to month'] / 100) + 1)

    mean_month_change = (((cpi_data['two months ago'] / 100) + 1)
                         + ((cpi_data['last month'] / 100) + 1)
                         + ((cpi_data['this month'] / 100) + 1)) / 3

    projected_costs['current month'] = user_data['last month']
    projected_costs['projected month'] = user_data['last month'] * mean_month_change

    new_file_name = input('name file:')
    new_file_path = 'files/' + new_file_name + '.xlsx'

    projected_costs.to_excel(new_file_path)

    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(projected_costs)


if __name__ == '__main__':
    main('test-1')


