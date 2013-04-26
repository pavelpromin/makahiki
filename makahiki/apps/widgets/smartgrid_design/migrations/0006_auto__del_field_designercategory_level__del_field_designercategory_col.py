# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'DesignerCategory.level'
        db.delete_column('smartgrid_design_designercategory', 'level_id')

        # Deleting field 'DesignerCategory.column'
        db.delete_column('smartgrid_design_designercategory', 'column')

        # Adding M2M table for field grid_locations on 'DesignerCategory'
        db.create_table('smartgrid_design_designercategory_grid_locations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('designercategory', models.ForeignKey(orm['smartgrid_design.designercategory'], null=False)),
            ('designercategorygrid', models.ForeignKey(orm['smartgrid_design.designercategorygrid'], null=False))
        ))
        db.create_unique('smartgrid_design_designercategory_grid_locations', ['designercategory_id', 'designercategorygrid_id'])


    def backwards(self, orm):
        
        # Adding field 'DesignerCategory.level'
        db.add_column('smartgrid_design_designercategory', 'level', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['smartgrid_design.DesignerLevel']), keep_default=False)

        # Adding field 'DesignerCategory.column'
        db.add_column('smartgrid_design_designercategory', 'column', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Removing M2M table for field grid_locations on 'DesignerCategory'
        db.delete_table('smartgrid_design_designercategory_grid_locations')


    models = {
        'smartgrid_design.designeraction': {
            'Meta': {'object_name': 'DesignerAction'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'embedded_widget': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'expire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'point_value': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2013, 4, 8)'}),
            'related_resource': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'social_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'unlock_condition': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'unlock_condition_text': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'video_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'video_source': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'smartgrid_design.designeractivity': {
            'Meta': {'object_name': 'DesignerActivity', '_ormbases': ['smartgrid_design.DesignerAction']},
            'admin_note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'confirm_prompt': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'confirm_type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '20'}),
            'designeraction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid_design.DesignerAction']", 'unique': 'True', 'primary_key': 'True'}),
            'expected_duration': ('django.db.models.fields.IntegerField', [], {}),
            'point_range_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'point_range_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'smartgrid_design.designercategory': {
            'Meta': {'object_name': 'DesignerCategory'},
            'grid_locations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['smartgrid_design.DesignerCategoryGrid']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        },
        'smartgrid_design.designercategorygrid': {
            'Meta': {'object_name': 'DesignerCategoryGrid'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerCategory']"}),
            'column': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerLevel']"})
        },
        'smartgrid_design.designercommitment': {
            'Meta': {'object_name': 'DesignerCommitment', '_ormbases': ['smartgrid_design.DesignerAction']},
            'commitment_length': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'designeraction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid_design.DesignerAction']", 'unique': 'True', 'primary_key': 'True'})
        },
        'smartgrid_design.designerevent': {
            'Meta': {'object_name': 'DesignerEvent', '_ormbases': ['smartgrid_design.DesignerAction']},
            'designeraction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid_design.DesignerAction']", 'unique': 'True', 'primary_key': 'True'}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'event_max_seat': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'expected_duration': ('django.db.models.fields.IntegerField', [], {})
        },
        'smartgrid_design.designerfiller': {
            'Meta': {'object_name': 'DesignerFiller', '_ormbases': ['smartgrid_design.DesignerAction']},
            'designeraction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartgrid_design.DesignerAction']", 'unique': 'True', 'primary_key': 'True'})
        },
        'smartgrid_design.designergrid': {
            'Meta': {'ordering': "('level', 'column', 'row')", 'object_name': 'DesignerGrid'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerAction']"}),
            'column': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerLevel']"}),
            'row': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'smartgrid_design.designerlevel': {
            'Meta': {'ordering': "('priority',)", 'object_name': 'DesignerLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'unlock_condition': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'unlock_condition_text': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'})
        },
        'smartgrid_design.designerquestionchoice': {
            'Meta': {'object_name': 'DesignerQuestionChoice'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerAction']"}),
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerTextPromptQuestion']"})
        },
        'smartgrid_design.designertextpromptquestion': {
            'Meta': {'object_name': 'DesignerTextPromptQuestion'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartgrid_design.DesignerAction']"}),
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['smartgrid_design']
