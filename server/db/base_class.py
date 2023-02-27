import re
from typing import Any

import inflect
from sqlalchemy.ext.declarative import as_declarative, declared_attr

p = inflect.engine()


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        res_list = re.findall("[A-Z][^A-Z]*", cls.__name__)
        name = ""
        for index, str in enumerate(res_list):
            str = (
                p.plural(str.lower())
                if index == len(res_list) - 1
                and str.lower() != "data"
                and str[-1].isnumeric() is False
                else str.lower()
            )
            if index == 0:
                name += str
            else:
                name += "_" + str
        return name
