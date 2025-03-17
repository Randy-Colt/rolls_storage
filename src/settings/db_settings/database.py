from sqlalchemy.orm import (
    declared_attr,
    DeclarativeBase,
    Mapped,
    mapped_column
)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls):
        return f'{cls.__name__.lower()}s'
