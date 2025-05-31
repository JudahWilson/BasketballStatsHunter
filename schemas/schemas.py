from pydantic import BaseModel
from schemas.helper import CustomField
from datetime import date



class GameBrId(int, CustomField):
    def __new__(cls, value: int) -> 'GameBrId':
        GameBrId.validate(value)
        return super().__new__(cls, value)
    
    @classmethod
    def validate(cls, value: str):
        year = value[0:4]
        month = value[5:7]
        day = value[7:9]
        
        # first 4 characters are a digit between 1946 and 2100
        if not (year.isdigit() and 1946 <= int(year) <= 2100):
            raise ValueError('First four digits of the GameBrId must be between 1946 and 2100')

        # 5th character is a 0
        if value[4] != '0':
            raise ValueError('5th character of the GameBrId must be a 0')
        # 6th and 7th characters are a digit between 1 and 12
        if not (month.isdigit() and 1 <= int(month) <= 12):
            raise ValueError('6th and 7th characters of the GameBrId must be between 01 and 12')
        
        # 8th and 9th characters are a valid day of the month using the month
        try:
            date(int(year), int(month), int(day))
        except ValueError:
            raise ValueError(f'The date (8th and 9th characters) in the GameBrId is an invalid date: {year}-{month}-{day}')
        
        return value