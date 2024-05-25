def address_type_factory(text: str):
    print(text)
    if len(text.split(',')) == 6:
        return text
    raise ValueError('Неверный формат адреса')


def fio_type_factory(text: str):
    if len(text.split(' ')) == 3:
        return text
    raise ValueError('Пожалуйста, введите фамилию, имя и отчество в формате: "Фамилия Имя Отчество"')
