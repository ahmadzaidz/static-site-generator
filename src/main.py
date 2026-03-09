from website_functions import  prepare_and_copy, generate_pages_recursive
import sys

def main():
    try:
        basepath = sys.argv[1]
    except:
        basepath = "/"
    prepare_and_copy("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    

main()