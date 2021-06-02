# Teniszpálya WebScraping APP.
# The purpose of this app is to download the database of http://tenisz-palya.hu/. It collects all of the information
# of the tennis courts in this site.

import bs4
import requests
import openpyxl
import os

# import lxml
# import package for excel export

from CourtClass import CourtClass

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

main_url = "http://tenisz-palya.hu"


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def beautiful_html():
    pass


def get_data(bs, data):
    # print(type(bs))
    if type(bs) is bs4.BeautifulSoup:
        return bs.select(data)
    else:
        return -1


def get_value(variable):
    """

    :type variable: beautifulsoup list
    """
    # print(type(variable))#, len(variable))

    if variable:
        return variable[0].text
    elif not variable:
        return "NA"
    else:
        return -1


def save_page(page):
    one_court = CourtClass(url="{main}{subpage}".format(main=main_url, subpage=page))
    print(one_court.url)

    plain_html = requests.get(one_court.url)
    beautiful_court = bs4.BeautifulSoup(plain_html.text, 'lxml')
    print(type(beautiful_court))

    court_name = get_data(beautiful_court, ".title_top.info h2")
    one_court.name = get_value(court_name)

    court_post_code = get_data(beautiful_court, ".gl-postcode")
    one_court.post_code = get_value(court_post_code)

    court_city = get_data(beautiful_court, ".gl-city")
    one_court.city = get_value(court_city)

    court_country = beautiful_court.select(".gl-county")
    one_court.countryside = get_value(court_country)

    court_address = beautiful_court.select(".gl-address")
    one_court.address = get_value(court_address)

    court_contact_name = beautiful_court.select(".contact_row.row_field_contact row_value")
    one_court.contact_name = get_value(court_contact_name)

    court_contact_phone = beautiful_court.select(".contact_row.row_field_phone row_value")
    one_court.contact_phone = get_value(court_contact_phone)

    court_contact_email = beautiful_court.select(".mail-web a")
    one_court.contact_email = get_value(court_contact_email)

    court_introduction = beautiful_court.select(".intro_desc_content")
    court_num = beautiful_court.select(".row_value.field_court_num")
    court_num_summer = beautiful_court.select(".row_value.field_indoor_court_num_summ")
    court_num_winter = beautiful_court.select(".row_value.field_indoor_court_num_wint")
    court_material = beautiful_court.select(".gl-value")
    court_annual_open = beautiful_court.select(".row_value.field_open_year")
    court_opening = beautiful_court.select(".row.row_field_open_note ")

    print(court_contact_email, court_introduction, court_num, court_num_winter, court_num_summer, court_material)
    # print(f" {type(court_name)}")

    # print(court_name, type(court_name))

    # TODO here WTF???

    # TODO ezzel valamit kene kezdeni, eleg ronda a kod......

    if (court_contact_name != []):
        phone = court_contact_phone[0].text
    else:
        phone = "NA"
    email = court_contact_email[0]['href'][6:]

    introduction = court_introduction[0].text
    number = court_num[0].text
    number_summer = court_num_summer[0].text
    number_winter = court_num_winter[0].text
    # material = court_material[0].text
    material = "TODO"
    annual_open = "TODO"
    opening = court_opening[0].text

    print(name, post_code, city, country, address, contact_name, phone, email)
    print(introduction, number, number_summer, number_winter, material, annual_open, opening)
    print("\n")
    # print(name[0].text)#, post_code[0].text, city[0].text, country[0].text, address[0].text, contact_name[0].text)

    return one_court


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    catalog_url = "http://tenisz-palya.hu/teniszpalya-katalogus?start="
    page_still_valid = True
    cnt = 0
    courts = []

    while page_still_valid:
        # create actual url
        page_url = "{0}{1}".format(catalog_url, str(10 * cnt))
        # page_url + main_url + str(10*cnt)
        # print(page_url)

        # request the html from the url
        catalog_html = requests.get(page_url)
        # print(catalog_html.text)

        # make it beautiful - readable to the code
        beautiful_catalog = bs4.BeautifulSoup(catalog_html.text, "lxml")
        # print(beautiful_catalog)

        court_list = get_data(beautiful_catalog, '.title.Tips1')  # ['src']

        print(f'Number of elements: {len(court_list)}')
        # valami = court_list["href"]
        for court in court_list:
            # print(court['href'])
            courts.append(save_page(court['href']))

        # TODO do not break but make the go throught logic!!!

        print(courts)
        break

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
