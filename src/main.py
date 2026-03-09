from website_functions import  prepare_and_copy, generate_pages_recursive


def main():
    prepare_and_copy("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    

main()