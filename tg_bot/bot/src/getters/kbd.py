from aiogram_dialog.widgets.kbd import Row, FirstPage, PrevPage, CurrentPage, NextPage, LastPage
from aiogram_dialog.widgets.text import Const


def get_scroll_buttons(scroll_id):
    return Row(
        FirstPage(scroll=scroll_id, id='first_page', text=Const(text='⏮️')),
        PrevPage(scroll=scroll_id, id='next_page', text=Const(text='◀️')),
        CurrentPage(scroll=scroll_id, id='current_page'),
        NextPage(scroll=scroll_id, id='next_page', text=Const(text='▶️️')),
        LastPage(scroll=scroll_id, id='last_page', text=Const(text='⏭️')),
        when='pages'
    )
