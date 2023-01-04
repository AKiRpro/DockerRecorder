#!/usr/bin/env python3

from datetime import datetime
from os import environ
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from models import Room, State


def start_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--kiosk')
    options.add_argument('--no-sandbox')
    options.add_argument('--display=:99')
    options.add_argument('--autoplay-policy=no-user-gesture-required')
    options.add_argument('--ash-host-window-bounds=1920x1080')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    print(f'Start chrome web driver with {url}')
    driver.get(url)
    sleep(10000)


def main():
    engine = create_engine(
        'postgresql+psycopg2://jibri_admin:jibri_secret@jibri_db/jibri'
    )

    sqlalchemy_session_maker = sessionmaker(bind=engine)
    room_id = environ.get('ROOM_ID', None)
    sqlalchemy_session = sqlalchemy_session_maker() 
    room = sqlalchemy_session.query(Room).filter_by(id=room_id).first()
    video_url = f'https://{room.server}.collaborate.center/localrec/' \
                f'?env={room.env}' \
                f'&userId={room.selected_user}' \
                f'&conferenceId={room.session}' \
                f'&recId={room.id}' \
                f'&token={room.token}'
    start_selenium(video_url)

    while True:
        with sqlalchemy_session_maker() as sqlalchemy_session:
            try:
                room = sqlalchemy_session.query(Room).filter_by(id=room_id).first()
                print(f'{room.id}: {room.state} {datetime.now()}')
                if room.state == State.READY:
                    break
            except ValueError as e:
                print(e)
                break
        sleep(1)


if __name__ == '__main__':
    main()
