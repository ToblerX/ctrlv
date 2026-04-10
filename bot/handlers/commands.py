# -*- coding: utf-8 -*-
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from bot.api_client import ApiClient
from bot.keyboards import mode_keyboard, MODE_LABELS

router = Router()

MODE_DISPLAY_NAMES = {
    "monologue": "Монолог",
    "teleshopping": "Телемагазин",
    "debates": "Дебати",
    "miniature": "Мініатюра",
}

RULES_MESSAGES = [
    (
        "\U0001f3ac <b>Правила гри «Ctrl V»</b>\n"
        "\n"
        "«Ctrl V» — це імпровізаційна гра для компаній. "
        "Гравці діляться на дві команди: одна грає сцену, "
        "інша — вгадує приховані слова.\n"
        "\n"
        "\U0001f4cb <b>Як грати:</b>\n"
        "\n"
        "1\u20e3 Ведучий генерує картку: <b>режим</b>, <b>тема</b> та <b>3 таємних слова</b>\n"
        "2\u20e3 Виступаючі бачать картку, суперники — тільки режим\n"
        "3\u20e3 Потрібно розіграти ситуацію та непомітно вплести всі 3 слова\n"
        "4\u20e3 Суперники слухають і вгадують, які слова були таємними"
    ),
    (
        "\U0001f3ad <b>Режими гри</b>\n"
        "\n"
        "\U0001f3a4 <b>Монолог</b>  \u2022  1 гравець  \u2022  1 хв\n"
        "Розповісти історію або виголосити промову за темою\n"
        "<i>Приклад: «Тост колишньої на весіллі»</i>\n"
        "\n"
        "\U0001f4fa <b>Телемагазин</b>  \u2022  1 гравець  \u2022  1 хв\n"
        "Прорекламувати предмет у стилі телемагазину\n"
        "<i>Приклад: «Продати пакет з пакетами»</i>\n"
        "\n"
        "\u2694\ufe0f <b>Дебати</b>  \u2022  2 гравці  \u2022  2 хв\n"
        "Сперечатися на тему, відстоюючи протилежні позиції\n"
        "<i>Приклад: «Зумери — найкраще чи найгірше покоління?»</i>\n"
        "\n"
        "\U0001f3ad <b>Мініатюра</b>  \u2022  2 гравці  \u2022  1.5\u20132 хв\n"
        "Розіграти сценку за заданою ситуацією\n"
        "<i>Приклад: «Два однокласники зустрілися через 20 років у маршрутці»</i>"
    ),
    (
        "\U0001f3c6 <b>Підрахунок балів</b>\n"
        "\n"
        "\u2705 Вгадане слово \u2014 <b>1 бал</b> команді суперників\n"
        "\u274c Невгадане слово \u2014 <b>1 бал</b> команді, що виступала\n"
        "\u2b50 Бонус за артистизм \u2014 на розсуд ведучого\n"
        "\n"
        "\U0001f4a1 <b>Поради</b>\n"
        "\n"
        "\u2022 Не вставляйте слова занадто очевидно\n"
        "\u2022 Будуйте історію навколо слів — нехай звучать природно\n"
        "\u2022 Суперники: слухайте, що звучить «не до місця»\n"
        "\u2022 Імпровізуйте та не бійтеся бути смішними!"
    ),
]


@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "Привіт! Я бот для гри \u00abCtrl V\u00bb \U0001f3ac\n\n"
        "Доступні команди:\n"
        "/card \u2014 отримати ігрову картку\n"
        "/rules \u2014 правила гри\n\n"
        "Натисни /card щоб почати!"
    )
    await message.answer(text)


@router.message(Command("card"))
async def cmd_card(message: Message):
    await message.answer("Оберіть режим гри:", reply_markup=mode_keyboard())


@router.callback_query(F.data.startswith("mode:"))
async def on_mode_selected(callback: CallbackQuery, api_client: ApiClient):
    mode = callback.data.split(":", 1)[1]

    try:
        card = await api_client.get_game_card(mode)
    except Exception:
        await callback.message.answer("Не вдалося отримати картку. Спробуйте ще раз.")
        await callback.answer()
        return

    display_mode = MODE_DISPLAY_NAMES.get(card["mode"], card["mode"])
    text = (
        f"\U0001f3ae <b>Режим:</b> {display_mode}\n"
        f"\U0001f4cb <b>Тема:</b> {card['topic']}\n\n"
        f"\U0001f524 <b>Таємні слова:</b>\n"
        f"  1. {card['words'][0]}\n"
        f"  2. {card['words'][1]}\n"
        f"  3. {card['words'][2]}"
    )

    await callback.message.answer(text, parse_mode=ParseMode.HTML)
    await callback.answer()


@router.message(Command("rules"))
async def cmd_rules(message: Message):
    for msg in RULES_MESSAGES:
        await message.answer(msg, parse_mode=ParseMode.HTML)
