from pydantic import GetPydanticSchema
from pydantic_core import CoreSchema, core_schema

class CustomField:
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: type, handler: GetPydanticSchema) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            handler(int)
        )
        
    @classmethod
    def validate(cls, value: int) -> int:
        raise NotImplementedError('CustomField must implement validate method')