from pathvalidate import is_valid_filename
from abc import ABC, abstractmethod
import inspect
class WebScrapeJob:
    """An interface class which makes the logic for webscraping a particular
    category of data (often one table) uniform, between the downloading,
    formatting, and importing of data
    """
    @abstractmethod
    def __init__(self, data_name: str) -> None:
        self.data_name = data_name
        """A human parseable name for the kind of data being processed"""
    
    @abstractmethod
    def download_html(self):
        """Logic to download as html is required to be implemented and should
        not handle importing to the database"""
        pass
    
    @abstractmethod
    def format(self):
        """Not required - Logic to convert to a reviewable format that can will also easily be
        used to import the data into the DB"""
        pass
    
    @abstractmethod
    def import_to_db(self):
        """Logic to import the data to the database"""
        pass
    
    @property
    def data_name(self):
        """The data_name property."""
        return self._data_name
    
    @data_name.setter
    def data_name(self, value):
        if not is_valid_filename(value):
            raise ValueError('data_name needs to be a valid file name')
        self._data_name = value
        
        
class WebScrapeTeamsJob(WebScrapeJob):
    def __init__(self) -> None:
        super().__init__('Teams data')
        # Print context
        print(self.__class__.__name__ + ' initialized')
        print(inspect.currentframe().f_code.co_name)
        """name
            br_id
            nba
            baa
            aba
            season_start_year
            season_end_year
            location
        """
        
        
    def download_html(self):
        url = base_url + "/teams/"
        soup = get_soup(url)
        # Get franchise urls - one franchise has many teams
        franchise_anchor_tag = soup.select('th[data-stat=franch_name] a')
        for a in franchise_anchor_tag:
            # Get the team overview html
            team_url = base_url + a['href']
            get_soup(team_url)
            
            # TODO Store the individual team rows for the one franchise. There
            # are separate team rows if
            # - the franchise moved cities
            # - the franchise changed from the ABA league to the NBA league
            
            # NOTE: (BAA and NBA are counted as the same team br_id because they
            # never coexisted. BAA merged with NBL to make NBA)
        breakpoint()
        
    def format(self):
        pass
    
    def import_to_db(self):
        pass
    

    
x=WebScrapeTeamsJob()

breakpoint()