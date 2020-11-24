import time as timer
from time import time

from .aogdigital import start_parse_aogdigital
from .bp import start_parse_bp
from .crudeoildaily import start_parse_crudeoildaily
from .ctc import start_parse_cpc
from .energynow import start_parse_energynow
from .exxonmobil import start_parse_exxonmobil
from .gazprom import start_parse_gazprom
from .iacng import start_parse_iacng
from .iz import start_parse_iz
from .jpt import start_parse_jpt
from .kazenergy import start_parse_kazenergy
from .kazservice import start_parse_kazservice
from .kaztransgaz import start_parse_kaztransgaz
from .king import start_parse_king
from .kmg import start_parse_kmg
from .koa import start_parse_koa
from .kpo import start_parse_kpo
from .mmg import start_parse_mmg
from .nangs import start_parse_nangs
from .neftegaz import start_parse_neftegaz
from .nsenergybusiness import start_parse_nsenergybusiness
from .nvg import start_parse_nvg
from .ogj import start_parse_ogj
from .oilandgas360 import start_parse_oilandgas360
from .oilandgaspeople import start_parse_oilandgaspeople
from .oilprice import start_parse_oilprice
from .opec import start_parse_opec
from .petrocouncil import start_parse_petrocouncil
from .petroleumeconomist import start_parse_petroleum_economist
from .prime import start_parse_prime
from .rigzone import start_parse_rigzone
from .shell import start_parse_shell
from .tengizchevroil import start_parse_tengizchevroil
from .total import start_parse_total
from ..notificator import notification


def parse_starter():
    x = 0
    while x < 1:
        start = time()
        notification('Парсинг начался', '')
        try:
            start_parse_mmg()
        except:
            notification('mmg.kz', 'Startapp error')
        notification('1', 'готово')
        # try:
        #     start_parse_king()
        # except:
        #     notification('king.kz', 'Startapp error')
        # notification('2', 'готово')
        try:
            start_parse_neftegaz()
        except:
            notification('neftegaz.ru', 'Startapp error')
        try:
            start_parse_kmg()
        except:
            notification('kmg.kz', 'Startapp error')
        try:
            start_parse_nsenergybusiness()
        except:
            notification('nsenergybusiness.com', 'Startapp error')
        try:
            start_parse_kaztransgaz()
        except:
            notification('kaztransgas.kz', 'Startapp error')
        notification('3', 'готово')
        try:
            start_parse_kazservice()
        except:
            notification('kazservice.kz', 'Startapp error')
        try:
            start_parse_kpo()
        except:
            notification('kpo.kz', 'Startapp error')
        try:
            start_parse_kazenergy()
        except:
            notification('kazenergy.com', 'Startapp error')
        try:
            start_parse_cpc()
        except:
            notification('cpc.ru', 'Startapp error')
        try:
            start_parse_iacng()
        except:
            notification('iacng', 'Startapp error')
        try:
            start_parse_opec()
        except:
            notification('opec.org', 'Startapp error')

        try:
            start_parse_total()
        except:
            notification('total.com', 'Startapp error')
        try:
            start_parse_petroleum_economist()
        except:
            notification('petroleum-economist.com', 'Startapp error')
        try:
            start_parse_gazprom()
        except:
            notification('gazprom.ru', 'Startapp error')
        try:
            start_parse_nvg()
        except:
            notification('nvg.ru', 'Startapp error')
        try:
            start_parse_oilprice()
        except:
            notification('oilprice.com', 'Startapp error')
        try:
            start_parse_nangs()
        except:
            notification('nansg.org', 'Startapp error')
        try:
            start_parse_prime()
        except:
            notification('1prime.ru', 'Startapp error')
        try:
            start_parse_ogj()
        except:
            notification('ogj.com', 'Startapp error')
        try:
            start_parse_rigzone()
        except:
            notification('ogj.com', 'Startapp error')
        try:
            start_parse_shell()
        except:
            notification('shell.com', 'Startapp error')
        try:
            start_parse_petrocouncil()
        except:
            notification('petrocouncil.kz', 'Startapp error')
        try:
            start_parse_aogdigital()
        except:
            notification('aogdigital.com', 'Startapp error')
        try:
            start_parse_oilandgaspeople()
        except:
            notification('oilandgaspeople.com', 'Startapp error')
        try:
            start_parse_tengizchevroil()
        except:
            notification('tengizchevroil.com', 'Startapp error')
        try:
            start_parse_koa()
        except:
            notification('koa.kz', 'Startapp error')
        try:
            start_parse_oilandgas360()
        except:
            notification('oilandgas360.com', 'Startapp error')
        try:
            start_parse_energynow()
        except:
            notification('energynow.ca/', 'Startapp error')
        try:
            start_parse_crudeoildaily()
        except:
            notification('crudeoildaily.com', 'Startapp error')
        try:
            start_parse_jpt()
        except:
            notification('https://pubs.spe.org/en/jpt/jpt-main-page', 'Startapp error')

        end = int(time() - start)
        notification('Парсинг законился. ', f'Время выполнения {end} сек.')
        notification('=====================', '==========================')
        timer.sleep(1)
        x += 1



