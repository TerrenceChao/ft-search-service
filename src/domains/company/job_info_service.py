import awoc
from typing import List
from ..public_value_objects import *
from ...configs.exceptions import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


my_world = awoc.AWOC()


class JobInfoService:
    def __init__(self):
        pass

    def __get_continent_vos(self) -> (List[ContinentVO]):
        continents = my_world.get_continents()
        continent_vos = list(map(
            lambda x: ContinentVO(
                continent_code=x.get('Continent Code', 'unknown'),
                continent_name=x.get('Continent Name', 'unknown'),
            ),
            continents
        ))
        return continent_vos

    def get_continents(self) -> (ContinentListVO):
        continent_vos = self.__get_continent_vos()
        return ContinentListVO(continents=continent_vos)
    
    def __get_country_vos(self, continent_name: str) -> (List[CountryVO]):
        countries = my_world.get_countries_data_of(continent_name)
        return list(map(
            lambda x: CountryVO(
                code=x.get('ISO3', 'unknown'),
                name=x.get('Country Name', 'unknown'),
            ),
            countries,
        ))

    def get_countries(self, continent_code: str) -> (List[CountryListVO]):
        continent_iter = filter(
            lambda x: x.continent_code == continent_code,
            self.__get_continent_vos()
        )
        try:
            continent_vo = next(continent_iter)
        except StopIteration:
            raise ClientException(
                f'Continent code {continent_code} is not found.')

        country_vos = self.__get_country_vos(continent_vo.continent_name)
        return [CountryListVO(
            countries=country_vos,
            continent=continent_vo,
        )]

    def get_all_continents_and_countries(self) -> (List[CountryListVO]):
        continent_vos = self.__get_continent_vos()
        continent_country_vos = list(map(
            lambda continent: CountryListVO(
                continent=continent,
                countries=self.__get_country_vos(continent.continent_name),
            ),
            continent_vos
        ))
        return continent_country_vos
