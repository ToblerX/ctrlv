# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

MODE_LABELS = {
    "random": "\U0001f3b2 Випадковий",
    "monologue": "\U0001f3a4 Монолог",
    "teleshopping": "\U0001f4fa Телемагазин",
    "debates": "\u2694\ufe0f Дебати",
    "miniature": "\U0001f3ad Мініатюра",
}


def mode_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=MODE_LABELS["random"], callback_data="mode:random")],
        [
            InlineKeyboardButton(text=MODE_LABELS["monologue"], callback_data="mode:monologue"),
            InlineKeyboardButton(text=MODE_LABELS["teleshopping"], callback_data="mode:teleshopping"),
        ],
        [
            InlineKeyboardButton(text=MODE_LABELS["debates"], callback_data="mode:debates"),
            InlineKeyboardButton(text=MODE_LABELS["miniature"], callback_data="mode:miniature"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
