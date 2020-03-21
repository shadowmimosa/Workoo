import os

from peewee import CharField, Model, SqliteDatabase, TextField

db_path = os.path.join(os.path.dirname(__file__), 'PROFF.sqlite3')
database = SqliteDatabase(db_path)


class BaseModel(Model):
    class Meta:
        database = database


class Company(BaseModel):
    uri = CharField(primary_key=True)
    name = CharField(max_length=255)
    domain = CharField(max_length=255, default='')
    email_address = CharField(max_length=255, default='')
    phone_number = CharField(max_length=255)
    category = TextField()
    city = CharField(max_length=255)

    @classmethod
    def new(cls, uri, name, phone_number, category, city):
        return cls.create(uri=uri,
                          name=name,
                          phone_number=phone_number,
                          category=category,
                          city=city)

    def update_detail(self, domain, email_address):
        self.domain = domain
        self.email_address = email_address
        self.save()


if __name__ == '__main__':
    database.create_tables([
        Company,
    ])
