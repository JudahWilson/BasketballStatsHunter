from abc import ABC, abstractmethod
from pathvalidate import is_valid_filename
import inspect
class BaseWebScrapeJob:
    """An interface class which makes the logic for webscraping a particular
    category of data (often one table) uniform, between the downloading,
    formatting, and importing of data
    """
    #################################################
    # Interface methods. MUST BE IMPLEMENTED
    #################################################
    @abstractmethod
    def __init__(self, data_name: str, tables: list[str]) -> None:
        """This is required so the child __init__ can actually run this code:
        ```python
        super().__init__('Teams data', ['teams','br_team_franchises'])
        ```
        """
        ### printing info
        print(self.__class__.__name__ + ' initialized')
        print(inspect.currentframe().f_code.co_name)
        
        ### Propertiess
        self.data_name = data_name
        """A human parseable name for the kind of data being processed"""
        self.tables = tables
        """The database table names that will take in data for this web scraping job"""
    
    
    @abstractmethod
    def download_html(self):
        """Logic to download as html is required to be implemented and should
        not handle importing to the database"""
        pass
    
    @abstractmethod
    def format_for_db(self):
        """Clean and save data into a reviewable format that can will also
        easily be used to import the data into the DB"""
        pass
    
    @abstractmethod
    def import_to_db(self):
        """Logic to import the data to the database"""
        pass
    
    @abstractmethod
    def get_html_file(self, *args):
        """Get a file where HTML content is stored per the given parameter

        Returns:
            str: A file path to an HTML file
        """
    
    #################################################
    # THESE PROPERTIES DO NOT NEED TO BE IMPLEMENTED.
    # THEY ARE JUST INHERITED FROM THIS PARENT CLASS.
    #################################################
    ### data_name
    @property
    def data_name(self):
        """The data_name property."""
        return self._data_name
    
    @data_name.setter
    def data_name(self, value):
        if not is_valid_filename(value):
            raise ValueError('data_name needs to be a valid file name')
        self._data_name = value
        
        
    ### html_folder
    @property
    def html_folder(self):
        """The html folder is a sibling to the current script's file

        Returns:
            str: "the script's location"/html
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, 'html')
    
    
    ### tables
    @property
    def tables(self):
        return self._data_table
        
    @tables.setter
    def tables(self, value: list[str]):
        self._data_table = value