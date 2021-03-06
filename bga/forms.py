from wtforms import Form, StringField, PasswordField, DecimalField, IntegerField, SelectField, validators
from wtforms.fields.html5 import DateField


def strip_filter(x): return x.strip() if x else None


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(
        min=1, max=255)], filters=[strip_filter])
    password = PasswordField('Password', [validators.Length(min=3, max=255)])


class CreateCourseForm(Form):
    coursename = StringField(
        'Course Name', [validators.Length(min=1, max=255)], filters=[strip_filter])
    courselocation = StringField(
        'Course Location', [validators.Length(min=1, max=255)], filters=[strip_filter])
    rating = DecimalField('Rating', [validators.NumberRange(
        min=50, max=150, message="Must Be Between 50-150")], places=2)
    slope = IntegerField('Slope', [validators.NumberRange(
        min=55, max=155, message="Must Be Between 55-155")])
    courseimage = StringField('Course Image URL', [validators.Length(
        min=1, max=255), validators.URL(message="Must Be a URL")], filters=[strip_filter])


class CreateScoreForm(Form):
    course = SelectField('Course Name', choices=[('oops', 'oops')])
    rounddate = DateField('Round Date', format='%Y-%m-%d')
    score = IntegerField('Round Score')
    attest = SelectField('Attesting Golfer', choices=[('oops', 'oops')])
