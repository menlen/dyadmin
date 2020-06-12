import requests
from bs4 import BeautifulSoup as bs

import config
import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types

HOST = 'https://daryo.uz'

# задаем уровень логов
logging.basicConfig(level=logging.INFO)
# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)


def get_html(url, params=None):
	r = requests.get(url)
	return r

def par(html_text):
	soup = bs(html_text, 'lxml')	
	text_teg = soup.find_all(attrs={"class": "itemDatas"})
			
	news=[]
	for item in text_teg:
		news.append({
			'mavzu': item.find('div', class_='itemTitle').get_text(),
			'heshteg': '#' + item.find('div', class_='itemCat').get_text(),
			'vaqt': item.find('div', class_='itemData').get_text(),
			'izoh': item.find('div', class_='postText').get_text(),
			'link': HOST + item.find('div', class_='itemTitle').find_next('a').get('href')
			})
	return news


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.chat.id)




async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)
		url = 'https://daryo.uz/category/texnologiyalar/'
		html_text = get_html(url).text
		news = par(html_text)
		idp = -1001471609965
		idp = -1001462619192
		await bot.send_message(idp, f'{news[0]["heshteg"]} \n<b>{news[0]["mavzu"]}</b>\n<i>{news[0]["izoh"]}</i>\n {news[0]["link"]}', parse_mode='html' )
		await bot.send_message(idp, f'{news[1]["heshteg"]} \n<b>{news[1]["mavzu"]}</b>\n<i>{news[1]["izoh"]}</i>\n {news[1]["link"]}', parse_mode='html' )
		await bot.send_message(idp, f'{news[2]["heshteg"]} \n<b>{news[3]["mavzu"]}</b>\n<i>{news[2]["izoh"]}</i>\n {news[2]["link"]}', parse_mode='html' )
		await bot.send_message(idp, f'{news[3]["heshteg"]} \n<b>{news[3]["mavzu"]}</b>\n<i>{news[3]["izoh"]}</i>\n {news[3]["link"]}', parse_mode='html' )
		await bot.send_message(idp, f'{news[4]["heshteg"]} \n<b>{news[4]["mavzu"]}</b>\n<i>{news[4]["izoh"]}</i>\n {news[4]["link"]}', parse_mode='html' )

		


if __name__ == '__main__':
	dp.loop.create_task(scheduled(50000)) # пока что оставим 10 секунд (в качестве теста)
	executor.start_polling(dp, skip_updates=True)