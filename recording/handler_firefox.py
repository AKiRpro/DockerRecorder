#!/usr/bin/env python3

from datetime import datetime
from os import environ
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from models import Room, State

def start_selenium(url):
    options = Options()
    options.add_argument('--kiosk')
    profile = webdriver.FirefoxProfile()
    options.set_preference('media.autoplay.default', 0)

    driver = webdriver.Firefox(
        service=Service(),
        options=options,
    )
    print(f'Start firefox web driver with {url}')
    driver.get(url)


def main():
    engine = create_engine(
        'postgresql+psycopg2://jibri_admin:jibri_secret@jibri_db/jibri'
    )
    sqlalchemy_session_maker = sessionmaker(bind=engine)
    room_id = environ.get('ROOM_ID', None)

    with sqlalchemy_session_maker() as sqlalchemy_session:
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
