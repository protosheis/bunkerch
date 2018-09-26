from flask_wtf import Form
from wtforms import StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

class PostForm(Form):
 post = StringField("post", widget=TextArea(), validators=[DataRequired()])
 name = StringField("name")
 delt = StringField("delt")
 nsub = StringField("nsub")
 opti = StringField("opti")
 subj = StringField("subj")

class ReportForm(Form):
    number = StringField("number", widget=TextArea(), validators=[DataRequired()])
    reason = StringField("reason", widget=TextArea(), validators=[DataRequired()])
