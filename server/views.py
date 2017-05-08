from flask_admin.model import BaseModelView
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction
from flask_admin.form import BaseForm 
from flask_admin.form.rules import * 
from flask_admin import Admin, BaseView, expose
from flask_admin.actions import action

from wtforms import SelectField
from wtforms.validators import DataRequired
from wtforms import StringField

from server.filters import EqualFilter
from storage.models import Statuses


class AinView(BaseModelView):
    statuses = dict(Statuses.__dict__)

    column_filters = ('Status', 'AlienID', 'Zipcode', 'Last Step Error')
    named_filter_urls = True 

    can_set_page_size = True 
    page_size = 20

    can_view_details = True

    create_modal = True 
    details_modal = True 
    edit_modal = True 

    export_max_rows = 1000
    can_export = True
    export_types = ['csv', 'xlsx', 'json']

    #column_editable_list = ('Status',) 
    column_exclude_list = (
        'CallID', 'CallUploadUrl',
        'CallTimestamp', 'TranscribeTimestamp',
        'CallTranscript',
    )

    column_extra_row_actions = [
        EndpointLinkRowAction('glyphicon glyphicon-headphones', 'audio')
    ]

    form_create_rules = [
        Field('PartitionKey'),
    ]

    form_edit_rules = [
        Field('Status'),
    ]

    form_args = dict(
        Status=dict(label='Status', validators=[DataRequired()]),
        PartitionKey=dict(label='AlienID', validators=[DataRequired()]),
    )

    column_labels = dict(
        PartitionKey='Alien ID',
        LastErrorStep='Last Error Step',
        CallTranscript='Call Transcript',
        CallID='Call ID',
        LastModified='Last Modified',
	CallTimestamp='Call Timestamp',
        TranscribeTimestamp='Transcribe Timestamp',
        CallUploadUrl='Call Upload Url',
    )

    def get_pk_value(self, model):
        return model.PartitionKey

    def scaffold_list_columns(self):
        return [
            'PartitionKey', 'Status', 'Confidence_location', 
            'City', 'State', 'Zipcode', 
            'day', 'hour', 'minute', 'month', 'year',
            'CallTranscript', 'LastErrorStep',
            'CallID', 'CallUploadUrl',
            'CallTimestamp', 'LastModified', 'TranscribeTimestamp',
        ]

    def scaffold_sortable_columns(self):
        return None

    def init_search(self):
        return False
    
    def scaffold_filters(self, name):
        return [EqualFilter(name, name)]

    def get_list(self, page, sort_field, sort_desc, search, filters, page_size=20):
        if len(filters) > 0:
             filter_col, filter_val = filters[0][1], filters[0][2]
             results = db.query(filter_col, filter_val, page_size)
        else:
             results = db.raw_table(limit=page_size)
        results = list(results)
        return len(results), results

    def get_one(self, id):
        return db.get_ain(id)

    def delete_model(self, model):
        return db.delete_ain(model.PartitionKey) 

    def create_model(self, form):
        ain = form.PartitionKey.data 
        db.upload_new_requests([ain]) 
        return self.get_one(ain)
     
    def update_model(self, form, model):
        status = form.Status.data
        model.Status = status
        db._update_entity(model)
        return True
    
    def scaffold_form(self):
        class AinForm(BaseForm):
            PartitionKey = StringField('Alien ID')
            Status = SelectField('Status', choices=self.statuses)
            CallTranscript = StringField('CallTranscript')

        return AinForm 

    @action('reset_status', 'Reset Status', 'Are you sure you want to reset the selected records?')
    def action_upload(self, ids):
        try:
            flash('Not implemented yet')
        except Exception as ex:
            flash('Failed to reset the status', 'error')

