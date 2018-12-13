from wtforms import Form, StringField, PasswordField, DecimalField, IntegerField, SelectField, DateField, validators


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
    rating = DecimalField('Slope', [validators.NumberRange(
        min=50, max=150, message="Must Be Between 50-150")], places=2)
    slope = IntegerField('Rating', [validators.NumberRange(
        min=55, max=155, message="Must Be Between 55-155")])
    courseimage = StringField('Course Image URL', [validators.Length(
        min=1, max=255), validators.URL(message="Must Be a URL")], filters=[strip_filter])


class CreateScoreForm(Form):
    course = SelectField('Course Name', choices=[(
        'abc', 'ABC Course'), ('123', '123 Course')])
    rounddate = DateField('Round Date')
    score = IntegerField('Round Score', [validators.NumberRange(
        min=55, max=155, message="Must Be Between 55-155")])
    attest = SelectField('Attesting Golfer', choices=[(
        'abc', 'ABC User'), ('123', '123 User')])
