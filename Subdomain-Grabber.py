from bs4 import BeautifulSoup
import requests
import pandas as pd
import argparse
import os
my_parser = argparse.ArgumentParser(description='Takes in a domain and gets a lot of subdomains back from crt.sh and outputs it into a csv file')
my_parser.add_argument('-d', '--domain', type=str, help='the domain being fed to crt.sh ex: facebook.com')
my_parser.add_argument('-o', '--output', type=str, help='the file the output is going into ex ~/Documents/output.csv')
args = my_parser.parse_args()
domain = args.domain
output_file = os.path.expanduser(args.output)
if not os.path.isfile(output_file):
    os.open(output_file, os.O_CREAT | os.O_APPEND)
page = requests.get(f'https://crt.sh/?q={domain}&exclude=expired&dir=^&sort=1&group=none')
soup = BeautifulSoup(page.text, "html.parser")
table = soup.find_all('table')[1]
df = pd.read_html(str(table))[1]
df['Matching Identities'] = df['Matching Identities'].str.split(' ')
df = df.explode('Matching Identities')
df = df[~df['Matching Identities'].str.startswith('*')]
df['Matching Identities'].to_csv(output_file, index=False)