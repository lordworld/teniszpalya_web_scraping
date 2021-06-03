

class CourtClass:

    def __init__(self, url, name = "", post_code = -1, city = "", countryside = "", address = "",
                 contact_name = "", contact_phone = "", contact_email = "",
                 introduction = "", number = 0, number_summer = 0, number_winter = 0,
                 material = "", annual_open = "", opening = "",
                 *args, **kwargs):

        self.url = url

        self.name = name
        self.post_code = post_code
        self.city = city
        self.countryside = countryside
        self.address = address

        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.contact_email = contact_email

        self.introduction = introduction

         # Expects numbers
        self.number = number
        self.number_summer = number_summer
        self.number_winter = number_winter
        self.material = material
        self.annual_open = annual_open
        self.opening = opening
        self.others = args

    def __str__(self):

        info = (f'name: {self.name}\naddress: {self.post_code} {self.city}, {self.address}, {self.countryside}\n'
            f'contact: {self.contact_name}, phone: {self.contact_phone}, email: {self.contact_email}\n'
            f'introduction: {self.introduction}\nCourt number: {self.number},'
            f'in winter: {self.number_winter} or in summer: {self.number_summer}\n'
            f'material: {self.material}\nannual opening time: {self.annual_open}\n'
            f'opening time: {self.opening}')

        return info

    def __len__(self):
        return self.name

    def __del__(self):
        pass

    def valami(self):
        pass
