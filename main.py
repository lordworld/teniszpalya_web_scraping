# Teniszpálya WebScraping APP.
# The purpose of this app is to download the database of http://tenisz-palya.hu/. It collects all of the information
# of the tennis courts in this site.

import os
import string

import bs4
import openpyxl
import requests
from datetime import datetime
from openpyxl.styles import Font

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
        return 0
    else:
        return -1


def save_page(page):
    one_court = CourtClass(url="{main}{subpage}".format(main=main_url, subpage=page))
    # print(one_court.url)

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
    # print(court_contact_email)
    one_court.contact_email = get_value(court_contact_email, 'href')[7:]

    # Court details
    court_introduction = get_raw_data(beautiful_court, ".intro_desc_content")
    one_court.introduction = get_value(court_introduction)

    court_num = get_raw_data(beautiful_court, ".row_value.field_court_num")
    one_court.number = get_value(court_num)
    # TODO convert to integer somehow ("5+1")

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

    # TODO Class own print function'''
    # print(one_court)

    return one_court


# Press the green button in the gutter to run the script.
def set_excel_size(sheet):
    sheet.column_dimensions['A'].width = 4
    sheet.column_dimensions['B'].width = 45
    sheet.column_dimensions['C'].width = 40
    sheet.column_dimensions['D'].width = 26
    sheet.column_dimensions['E'].width = 35
    sheet.column_dimensions['F'].width = 30
    sheet.column_dimensions['G'].width = 35
    sheet.column_dimensions['H'].width = 4
    sheet.column_dimensions['I'].width = 4
    sheet.column_dimensions['J'].width = 4
    sheet.column_dimensions['K'].width = 12
    sheet.column_dimensions['L'].width = 22
    sheet.column_dimensions['M'].width = 15
    sheet.column_dimensions['N'].width = 200
    sheet.column_dimensions['O'].width = 10
    sheet.column_dimensions['P'].width = 150
    # sheet.column_dimensions['Q'].width = 2.5


def set_excel_header(sheet):
    set_excel_size(sheet)

    sheet["A1"] = 'ID'
    sheet["B1"] = 'Név'
    sheet["C1"] = 'Cím'
    sheet["D1"] = 'Megye'
    sheet["E1"] = 'Kontakt személy'
    sheet["F1"] = 'Telefon'
    sheet["G1"] = 'Email'
    sheet["H1"] = 'Pályák száma'
    sheet["I1"] = 'Nyári pályák'
    sheet["J1"] = 'Téli pályák'
    sheet["K1"] = 'Pálya anyaga'
    sheet["L1"] = 'Éves nyitvatartás'
    sheet["M1"] = 'Nyitvatartás'
    sheet["N1"] = 'Leírás'
    sheet["O1"] = 'Egyéb'
    sheet["P1"] = 'URL'

    for i in string.ascii_uppercase:
        sheet[f'{i}1'].font = Font(bold=True)


def export_to_excel(data):
    path = os.getcwd()
    print(path)
    id = 1

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
    sheet = wb.create_sheet("Courts")
    print(type(sheet))

    print(wb.get_sheet_names())
    sheet1 = wb.get_sheet_by_name('Sheet')
    sheet1.title = 'valami'
    """
    sheet = wb.get_sheet_by_name('Courts')
    print(type(sheet))"""

    set_excel_header(sheet)

    for item in data:
        length = len(data)
        print(str(id) + " / " + str(length))
        row = str(id + 1)

        sheet[f"A{row}"] = id
        sheet[f"B{row}"] = item.name
        sheet[f"C{row}"] = str(item.post_code) + ' ' + item.city + ' ' + item.address # 'Cím'
        sheet[f"D{row}"] = item.countryside      # 'Megye'
        sheet[f"E{row}"] = item.contact_name     # 'Kontakt személy'
        sheet[f"F{row}"] = item.contact_phone    # 'Telefon'
        sheet[f"G{row}"] = item.contact_email    # 'Email'
        sheet[f"H{row}"] = item.number           # 'Pályák száma'
        sheet[f"I{row}"] = item.number_summer    # 'Nyári pályák'
        sheet[f"J{row}"] = item.number_winter    # 'Téli pályák'
        sheet[f"K{row}"] = item.material         # 'Pálya anyaga'
        sheet[f"L{row}"] = item.annual_open      #'Éves nyitvatartás'
        sheet[f"M{row}"] = item.opening          # 'Nyitvatartás'
        sheet[f"N{row}"] = item.introduction     # 'Lerírás'
        # sheet[f"O{id}"] = item.others           # 'Egyéb'
        sheet[f"P{row}"] = item.url

        id += 1

    wb.remove_sheet(sheet1)

    wb.save(excel_name)


if __name__ == '__main__':
    print_hi('PyCharm')

    start = datetime.now()
    current_time = start.strftime("%Y:%m:%d:%H:%M")
    print(current_time)

    first_catalog_url = "/teniszpalya-katalogus?start=0"
    last_catalog_url = "/teniszpalya-katalogus?start=760"
    next_page = first_catalog_url
    # next_page = last_catalog_url

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
            pass

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

        # break

        # print(all_courts)
    
    export_to_excel(all_courts)

    end = datetime.now()
    current_time = start.strftime("%Y:%m:%d:%H:%M")
    print(current_time)

    diff = end - start
    print('Runtime: ', diff)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
