import sys
import console.parser_api.parser as Parser

def main():
    args = sys.argv[1::]
    Parser.parse(args)


if __name__ == '__main__':
    main()
