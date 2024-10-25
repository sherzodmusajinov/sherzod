import logging
from os import remove
from PIL import Image, ImageFont, ImageDraw
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, MediaGroup

logging.basicConfig(level=logging.INFO)
bot = Bot('7975170508:AAHvhsDP9mRrXveNFhgZV737Xfz5NDqMmRQ')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
    phone = State()
    pochta = State()
    manzil = State()
    email = State()
    name_copani=State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer('Assalomu alaykum, biznis uchun vizit karta qiling.')
    await UserState.phone.set()
    await message.answer("Telefon raqam kiriting:")

@dp.message_handler(state=UserState.phone)
async def get_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await UserState.next()
    await message.answer('Biznis nomini kiriting')

@dp.message_handler(state=UserState.pochta)
async def get_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pochta'] = message.text
    await UserState.next()
    await message.answer('Manzilni kiriting:')

@dp.message_handler(state=UserState.manzil)
async def get_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['manzil'] = message.text
    await UserState.next()
    await message.answer('Elektron pochtani kiriting:')

@dp.message_handler(state=UserState.email)
async def get_company_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text




    writer_func(data['phone'], data['pochta'], data['manzil'], data['email'])
    visit(data['pochta'])

    await state.finish()
    await message.answer('Vizit kartangiz tayyorlandi!vizit cartani korish uchun /card ni bosing')


def writer_func(phone, pochta, manzil, email):
    img1 = Image.open('1.png')
    draw = ImageDraw.Draw(img1)

    font1 = ImageFont.truetype("font.ttf", 28)
    # image size fg
    font2 = ImageFont.truetype("font.ttf", 28)


    draw.text(
        (500, 260),
        phone.title(), fill=(255, 0, 0),
        font=font1,
    ),

    # set job
    draw.text(
        (500, 316),
        pochta.title(), fill=(255, 0, 0),
        font=font1,
    ),


    draw.text(
        (500, 368),
        manzil.title(), fill=(255, 0, 0),
        font=font2,
    ),

    # set email
    draw.text(
        (500, 417),
        email, fill=(255, 0, 0 ),
        font=ImageFont.truetype("font.ttf", 28)
    ),
    img1.save(f'vizit_card.png')




def visit(name_kopani):
    img3 = Image.open('2.png')
    draw = ImageDraw.Draw(img3)
    W,H = img3.size
    font = ImageFont.truetype("font.ttf", 72)

    draw.text(((W - draw.textbbox((0, 0), name_kopani, font=font)[2]) / 2, 290), name_kopani.upper(), fill='red', font=font)
    img3.save('vizit_card2.png')
    print('Successfully created and saved the company card.')

    @dp.message_handler(commands=['card'])
    async def send_image(message: types.Message):
        media = MediaGroup()
        media.attach_photo(InputFile('vizit_card.png'))
        media.attach_photo(InputFile('vizit_card2.png'))
        await bot.send_media_group(chat_id=message.chat.id, media=media)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)