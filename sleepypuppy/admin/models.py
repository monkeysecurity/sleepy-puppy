from sqlalchemy import Column, Integer, ForeignKey
from sleepypuppy import db

# Database association models
user_associations = db.Table(
    'user_associations',
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('assessment_id', Integer, ForeignKey('assessments.id')),
)
assessment_associations = db.Table(
    'assessment_associations',
    Column('assessment_id', Integer, ForeignKey('assessments.id')),
    Column('payload_id', Integer, ForeignKey('payloads.id'))
)

# Remove
# collection_associations = db.Table(
#     'collection_associations',
#     Column('collection_id', Integer, ForeignKey('collection.id')),
#     Column('payload_id', Integer, ForeignKey('payloads.id')),
# )

taxonomy = db.Table(
    'taxonomy',
    Column('javascript_id', Integer, ForeignKey('javascript.id')),
    Column('payload_id', Integer, ForeignKey('payloads.id')),
)
