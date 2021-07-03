# Teniszpálya WebScraping APP.
# The purpose of this app is to download the database of http://tenisz-palya.hu/. It collects all of the information
# of the tennis courts in this site.

import os
import string

from datetime import datetime
from openpyxl.styles import Font

from CourtClass import CourtClass
from WebScraper import WebScraperClass
from ExcelManager import ExcelManagerClass
from LogHandler import LogHandlerClass

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def get_one_court_data(page, subpage, log = None):
    one_court = CourtClass(url="{main}{subpage}".format(main=page.url, subpage=subpage))
    log.add_line(f"Site url: {one_court.url}")

    page.format_page(one_court.url)

    # Court basic info
    one_court.name = page.get_info(".title_top.info h2")
    one_court.post_code = page.get_info(".gl-postcode")
    one_court.city = page.get_info(".gl-city")
    one_court.countryside = page.get_info(".gl-county")
    one_court.address = page.get_info(".gl-address")

    # Court contact information
    one_court.contact_name = page.get_info(".contact_row.row_field_contact .row_value")
    one_court.contact_phone = page.get_info(".contact_row.row_field_phone .row_value")
    one_court.contact_email = page.get_info(".mail-web a", tag = 'href')[7:]

    # Court details
    one_court.introduction = page.get_info(".intro_desc_content")
    # TODO convert to integer somehow ("5+1")
    one_court.number = page.get_info(".row_value.field_court_num")
    one_court.number_summer = int(page.get_info(".row_value.field_indoor_court_num_summ"))
    one_court.number_winter = int(page.get_info(".row_value.field_indoor_court_num_wint"))
    one_court.material = page.get_info(".gl-value")
    one_court.annual_open = page.get_info(".row_value.field_open_year .gl-value")
    one_court.opening = page.get_info(".row_value.field_open_note")

    # print(one_court)
    log.add_line(one_court)
    return one_court


def set_excel_header(excel, log = None):
    column_size = [4, 45,40, 26, 35,30, 35, 4, 4, 4, 12, 22, 15, 150, 10, 150]
    header_names = ['ID', 'Név', 'Cím', 'Megye', 'Kontakt személy', 'Telefon', 'Email', 'Pályák száma', 'Nyári pályák',
                    'Téli pályák', 'Pálya anyaga', 'Éves nyitvatartás', 'Nyitvatartás', 'Leírás', 'Egyéb', 'URL']

    excel.set_excel_row_size(column_size)
    excel.set_excel_header_names(header_names)

    # TODO copy to the class
    for i in string.ascii_uppercase:
        excel.sheet[f'{i}1'].font = Font(bold=True)

    last_cell = chr(ord("A") + len(header_names) - 1) + '1'
    excel.color_cells("A1",f"{last_cell}", fgColor="C4BD97")
    log.add_line(f"Excel header and size is adjusted. \nSize: {column_size}\nColumn names: {header_names}")


def export_to_excel(data, log = None):
    id = 1

    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d_%H_%M")

    # Open the file, workbook, sheet and create the object
    excel_name = f"CourtData_{current_time}.xlsx"
    excel = ExcelManagerClass(excel_name, log)
    excel.create_sheet("Courts")
    excel.remove_sheet_by_name('Sheet')
    log.add_line(f"Excel is opened. Name: {excel.name}, sheet: {excel.sheet}")

    set_excel_header(excel, log)

    # Fill excel with data
    for item in data:
        length = len(data)
        print(str(id) + " / " + str(length))
        log.add_line(f"{str(id)} / {str(length)}")
        row = str(id + 1)
        address = str(item.post_code) + ' ' + item.city + ' ' + item.address

        # TODO Itt is ki lehetne szedni a sormintat....

        excel.fill_excel_cell(f"A{row}", id)
        excel.fill_excel_cell(f"B{row}", item.name)             # Név
        excel.fill_excel_cell(f"C{row}", address)               # Cim
        excel.fill_excel_cell(f"D{row}", item.countryside)      # Megye
        excel.fill_excel_cell(f"E{row}", item.contact_name)     # Telefon
        excel.fill_excel_cell(f"F{row}", item.contact_phone)    # Kontakt személy
        excel.fill_excel_cell(f"G{row}", item.contact_email)    # Email
        excel.fill_excel_cell(f"H{row}", item.number)           # Pályák száma
        excel.fill_excel_cell(f"I{row}", item.number_summer)    # Nyári pályák száma
        excel.fill_excel_cell(f"J{row}", item.number_winter)    # Téli pályák száma
        excel.fill_excel_cell(f"K{row}", item.material)         # Pálya anyaga
        excel.fill_excel_cell(f"L{row}", item.annual_open)      # Éves nyitvatartás
        excel.fill_excel_cell(f"M{row}", item.opening)          # Nyitvatartás
        excel.fill_excel_cell(f"N{row}", item.introduction)     # Leírás
        # excel.fill_excel_cell(f"O{row}", item.others)         # Egyéb
        excel.fill_excel_cell(f"P{row}", item.url)              # url link

        log.add_line(f"Cell is added.\n{item}")

        # Color cells
        if id % 2:
            excel.color_cells(f"A{row}", f"P{row}")
        id += 1

        log.add_line("Excel is colored")

    print(excel.path)
    excel.save_excel()
    log.add_line(f"Excel is saved. Name: {excel.path}{excel.name}")
    excel.close_excel()
    log.add_line(f"Excel is closed. Name: {excel.path}{excel.name}")

if __name__ == '__main__':
    print_hi('PyCharm')
    log = LogHandlerClass("Log")
    page = WebScraperClass("http://tenisz-palya.hu", log)

    start = datetime.now()
    current_time = start.strftime("%Y:%m:%d:%H:%M")
    print(current_time)
    log.add_line(f'Webscraping is started\nSite is: {page.url}')

    page.add_subpage(first_page = '/teniszpalya-katalogus?start=0',
                    last_page = '/teniszpalya-katalogus?start=760',
                    actual_page = '', next_page = '',
                    random = '/teniszpalya-katalogus?start=740')
    page.subpage['next_page'] = page.subpage['first_page']
    print("Next page url: ", page.subpage['next_page'])
    log.add_line(f"Next page url: {page.subpage['next_page']}")

    page_still_valid = True
    cnt = 0
    all_courts = []

    # Iterate through all the pages
    while page_still_valid:
        # create actual url
        page.subpage['actual_page'] = "{0}{1}".format(page.url, page.subpage['next_page'])
        print("full page url: ", page.subpage['actual_page'])
        log.add_line(f"Actual page url: {page.subpage['actual_page']}")

        page.format_page(page.subpage['actual_page'])

        court_list = page.get_raw_data('.title.Tips1')

        # Iterate throught all the courts
        print(f'Number of elements: {len(court_list)}')
        log.add_line(f'Actual site number of elements: {len(court_list)}')
        for court in court_list:
            print(court.text, end = "\t\t")
            log.add_line(court.text, end = "\t\t")
            new_court = get_one_court_data(page, court['href'], log)
            all_courts.append(new_court)
            log.add_line("Court added\n\n")

        # TODO do not break but make the go throught logic!!!
        if page.is_next_page():
            page.subpage['next_page'] = page.get_next_page()
            log.add_line(f"Next page is {page.subpage['next_page']}")
            cnt += 1
        elif not page.is_next_page():
            page_still_valid = False
        else:
            # TODO error...
            pass # TODO error logic

    
    export_to_excel(all_courts, log)

    # Print runtime
    end = datetime.now()
    current_time = start.strftime("%Y:%m:%d:%H:%M")
    print(current_time)
    log.add_line(f"\n\nRun has finished")

    diff = end - start
    print('Runtime: ', diff)
    log.add_line(f"Runtime: {diff}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
