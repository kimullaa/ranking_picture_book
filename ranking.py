import re
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_next_picture_book(f):
    is_picture_book = False
    title = ""
    price = ""
    pages = ""
    isbn = ""
    id = ""
    for line in f:
        if  line == "\n":
            if (is_picture_book and pages and title and price and id):
                yield id,title, price, pages,isbn
            is_picture_book = False
            title = ""
            price = ""
            pages = ""
            isbn = ""
            id = ""

        else:
            items = line.split(" ")
            id = items[0]
            field = items[1]
            value = " ".join(items[2:])
            
            if field == "24500":
                title = value.split("|a ")[1].split("|")[0].rstrip()

            if field == "020":
                if "|a" in value:
                    isbn = value.split("|a ")[1].split("|")[0].strip()
                if "|c" in value:
                    price = value.split("|c ")[1].strip()

            if field == "084":
                if "kktb" in value and ("Y17 " in value or "Y18 " in value):
                    is_picture_book = True

            if field == "300":
                pages = value.split("|a ")[1].split("|")[0].strip()


with open('jmo_all_20230115_confirmation.txt', encoding='utf-8') as f:
    for id, title, price, pages,isbn in get_next_picture_book(f):
        m_pages = pages=re.search('\[?(\d+)\]? ?[p||P]', pages)
        m_price = price=re.search('(\d+) ?[yen|円]', price)

        if (m_pages and m_price):
            print(int(m_price.groups()[0]) / int(m_pages.groups()[0]), id, m_price.groups()[0], m_pages.groups()[0], isbn, title,  sep=", " )
