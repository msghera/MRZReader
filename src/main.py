from BarcodeReader import BarcodeReader
from MRZParser import MRZParser
import argparse

PATH = '../images/test2.jpg'

def process_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="Provide imagepath to process",
                        type=str)

    args = parser.parse_args()
    PATH = args.filepath


def main():
    barcode_reader = BarcodeReader(ImagePath = PATH)
    print(MRZParser(barcode_reader.get_text()))


if __name__ == '__main__':
    process_arg()
    main()