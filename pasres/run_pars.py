from pasres.pars_links import parse_links
from pasres.pars_film import parse_films
from pasres.pars_person import parse_person


def main():
    parse_links()
    parse_films()
    parse_person()
    print('finish')


if __name__ == '__main__':
    main()