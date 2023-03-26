import argparse
import requests

def main():
    # create an argument parser
    parser = argparse.ArgumentParser()

    # add an argument for the input file
    parser.add_argument('--input', type=str, required=True, help='input file containing a list of domain names')

    # parse the arguments
    args = parser.parse_args()

    # read domain names from file
    with open(args.input, 'r') as f:
        domains = f.read().splitlines()

    # print status code for each domain
    for domain in domains:
        try:
            r = requests.get(domain)
            print(f'{domain}: {r.status_code}')
        except requests.exceptions.ConnectionError:
            print(f'{domain}: ConnectionError')

if __name__ == '__main__':
    main()
