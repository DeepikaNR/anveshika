from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Term(Model):

    #id = columns.UUID(primary_key=True, default=uuid.uuid4)
    term = columns.Text(primary_key=True)
    df = columns.BigInt()
    idf = columns.Float()
    inverted_index = columns.Map(columns.Text, columns.List(columns.BigInt))    # url : [pos1, pos2]


class Document(Model):
    #id = columns.UUID(primary_key=True, default=uuid.uuid4)
    url = columns.Text(primary_key=True)
    tf = columns.Map(columns.Text, columns.Float)             # tf = {'rama' : 0.67}


"""
term: df idf {inverted_index}
doc: file_name url {tf}
"""