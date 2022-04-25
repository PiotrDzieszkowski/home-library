from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired

class BooksForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    categories = SelectField('Rodzaj gatunku', choices=['','biografia', 'sportowe', 'fantastyka', 'turystyka', 'obcojęzyczna', 'informatyka', 'naukowa', 'romans'])
    pages = IntegerField('Liczba stron', default=0)
    year_published = IntegerField('Rok wydania', default=0)
    read = BooleanField('Przeczytana')
    cover = SelectField('Okładka', choices=['','miękka', 'twarda'])
    condition = SelectField('Stan książki', choices=['','nowa', 'używana'])
    last_read = StringField('Ostatnio czytane')