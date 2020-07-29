
from craigslist import CraigslistForSale

def main():
    #CraigslistForSale.show_filters()
    cl_fs = CraigslistForSale(site='sfbay', filters={'query': 'weber smoker', 'search_distance': 50})

    for result in cl_fs.get_results(sort_by='newest'):

        print(f"{result['datetime']}, {result['name']}, {result['price']}, {result['url']} ")


if __name__ == '__main__':
    main()