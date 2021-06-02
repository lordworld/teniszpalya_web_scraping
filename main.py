# Teniszpálya WebScraping APP.
# The purpose of this app is to download the database of http://tenisz-palya.hu/. It collects all of the information
# of the tennis courts in this site.

import os

import bs4
import openpyxl
import requests
from datetime import datetime

from CourtClass import CourtClass

# import lxml
# import package for excel export

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

main_url = "http://tenisz-palya.hu"


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def beautiful_html():
    pass


def get_raw_data(bs, data):
    # print(type(bs))
    if type(bs) is bs4.BeautifulSoup:
        # print(bs.select(data))
        return bs.select(data)
    else:
        return -1


def get_value(variable, tag = [], num = 0):
    """

    :param tag: text
    :type variable: beautifulsoup list
    """
    # print(type(variable))#, len(variable))

    if variable and not tag:
        numth_value = variable[num]
        return numth_value.text.strip()
    if variable and tag:
        # print(variable[num][tag])
        numth_value = variable[num][tag]
        return numth_value.strip()
    elif not variable:
        return "NA"
    else:
        return -1


def save_page(page):
    one_court = CourtClass(url="{main}{subpage}".format(main=main_url, subpage=page))
    print(one_court.url)

    plain_html = requests.get(one_court.url)
    beautiful_court = bs4.BeautifulSoup(plain_html.text, 'lxml')
    # print(type(beautiful_court))

    # Court basic info
    court_name = get_raw_data(beautiful_court, ".title_top.info h2")
    one_court.name = get_value(court_name)

    court_post_code = get_raw_data(beautiful_court, ".gl-postcode")
    one_court.post_code = get_value(court_post_code)

    court_city = get_raw_data(beautiful_court, ".gl-city")
    one_court.city = get_value(court_city)

    court_country = get_raw_data(beautiful_court, ".gl-county")
    one_court.countryside = get_value(court_country)

    court_address = get_raw_data(beautiful_court, ".gl-address")
    one_court.address = get_value(court_address)

    # Court contact information
    court_contact_name = get_raw_data(beautiful_court, ".contact_row.row_field_contact .row_value")
    one_court.contact_name = get_value(court_contact_name)
    # print(one_court.contact_name)

    court_contact_phone = get_raw_data(beautiful_court, ".contact_row.row_field_phone .row_value")
    one_court.contact_phone = get_value(court_contact_phone)

    court_contact_email = get_raw_data(beautiful_court, ".mail-web a")
    print(court_contact_email)
    one_court.contact_email = get_value(court_contact_email, 'href')[7:]

    # Court details
    court_introduction = get_raw_data(beautiful_court, ".intro_desc_content")
    one_court.introduction = get_value(court_introduction)

    court_num = get_raw_data(beautiful_court, ".row_value.field_court_num")
    one_court.number = int(get_value(court_num))

    court_num_summer = get_raw_data(beautiful_court, ".row_value.field_indoor_court_num_summ")
    one_court.number_summer = int(get_value(court_num_summer))

    court_num_winter = get_raw_data(beautiful_court, ".row_value.field_indoor_court_num_wint")
    one_court.number_winter = int(get_value(court_num_winter))

    court_material = get_raw_data(beautiful_court, ".gl-value")
    one_court.material = get_value(court_material)

    court_annual_open = get_raw_data(beautiful_court, ".row_value.field_open_year .gl-value")
    one_court.annual_open = get_value(court_annual_open)

    court_opening = get_raw_data(beautiful_court, ".row_value.field_open_note")
    one_court.opening = get_value(court_opening)

    # print(court_contact_email, court_introduction, court_num, court_num_winter, court_num_summer, court_material)
    # print(f" {type(court_name)}")

    # print(court_name, type(court_name))

    # TODO here WTF???

    # TODO ezzel valamit kene kezdeni, eleg ronda a kod......

    '''
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
'''

    print(f'name: {one_court.name}\naddress: {one_court.post_code} {one_court.city}, {one_court.address}, {one_court.countryside}\n',
          f'contact: {one_court.contact_name}, phone: {one_court.contact_phone}, email: {one_court.contact_email}\n',
          f'introduction: {one_court.introduction}\nCourt number: {one_court.number},',
          f'in winter: {one_court.number_winter} or in summer: {one_court.number_summer}\n',
          f'material: {one_court.material}\nannual opening time: {one_court.annual_open}\n',
          f'opening time: {one_court.opening}')
    #print(introduction, number, number_summer, number_winter, material, annual_open, opening)
    #print("\n")
    # print(name[0].text)#, post_code[0].text, city[0].text, country[0].text, address[0].text, contact_name[0].text)

    return one_court


# Press the green button in the gutter to run the script.
def export_to_excel(data):
    path = os.getcwd()
    print(path)

    now = now = datetime.now()
    current_time = now.strftime("%Y:%m:%d:%H:%M")

    # excel_name = path + "\\CourtData.xlsx"
    excel_name = "CourtData.xlsx"
    wb = openpyxl.Workbook()
    #wb = openpyxl.load_workbook(f'CourtData{current_time}.xlsx')
    '''print(wb.get_sheet_names())
    sheet = wb.get_sheet_by_name('Sheet1')
    print(sheet.title)

    cell = sheet['A1']
    cell.value = "A1"
    
    Sheet_name = wb.sheetnames

    for x in range(1, 9):
        print(x, sheet.cell(row=x, column=4).value)
        
        
        '''

    wb.save(excel_name)


if __name__ == '__main__':
    print_hi('PyCharm')

    first_catalog_url = "/teniszpalya-katalogus?start=0"
    last_catalog_url = "/teniszpalya-katalogus?start=760"
    # next_page = first_catalog_url
    next_page = last_catalog_url

    page_still_valid = True
    cnt = 0
    all_courts = []

    while page_still_valid:
        # create actual url
        page_url = "{0}{1}".format(main_url, next_page)#, str(10 * cnt))
        # page_url + main_url + str(10*cnt)
        print(page_url)

        # request the html from the url
        catalog_html = requests.get(page_url)
        # print(catalog_html.text)

        # make it beautiful - readable to the code
        beautiful_catalog = bs4.BeautifulSoup(catalog_html.text, "lxml")
        # print(beautiful_catalog)

        court_list = get_raw_data(beautiful_catalog, '.title.Tips1')  # ['src']

        print(f'Number of elements: {len(court_list)}')
        # valami = court_list["href"]
        for court in court_list:
            # print(court['href'])
            all_courts.append(save_page(court['href']))
            #pass

        # TODO do not break but make the go throught logic!!!

        # Check if next page exists
        next_page_raw = get_raw_data(beautiful_catalog, ".pagination-next a")
        # print(next_page_raw)
        if next_page_raw:
            next_page = get_value(next_page_raw, 'href')
            cnt += 1
        elif not next_page_raw:
            page_still_valid = False
        else:
            # error...
            pass # error logic

        # print(all_courts)
    
    export_to_excel(all_courts)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
