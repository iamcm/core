from bson.objectid import ObjectId
import datetime
from core.utils import Logger 
from application.settings import DBDEBUG

class EntityManager:
    """
    This class handles getting a list of entities, or removing one/many entities
    from a mongo collection
    """
    def __init__(self, db):
        self.db = db
        
    def get_all(self, entity, filter_criteria='', sort_by=[], skip=None, limit=None, count=False):
        """
        Get all or a selection of entities from the datastore. This returns
        a list of entities.
        
        Entity should be class object
        
        filter_criteria can be used to filter the results and should be
        a dictionary that adheres to the pymongo documentation
        http://api.mongodb.org/python/current/genindex.html
        {'name':'jim'}
        
        sort_by should be a list of tuples (attribute, direction)
        [
            ('name',1),
            ('age',1),
        ]
        
        skip and limit are both ints and are used for pagination

        count should be True if only a count of the results is required

        e.g.
        todos = EntityManager(_DBCON).get_all(Todo
                                            ,filter_criteria={'uid':self.session['uid']}
                                            ,sort_by=[('added', 1)]
                                            ,skip=20
                                            ,limit=10
                                            )
        """
        extraCriteria = ''

        if len(sort_by)>0:
            extraCriteria += '.sort(%s)' % str(sort_by)

        if skip:
            extraCriteria += '.skip(%s)' % str(skip)

        if limit:
            extraCriteria += '.limit(%s)' % str(limit)

        if count:
            extraCriteria += '.count()'
            
        command = 'self.db.%s.find(%s)%s' % (entity.__name__
                                                ,str(filter_criteria)
                                                , extraCriteria
                                            )

        if DBDEBUG: Logger.log_to_file(command)

        if count:
            return eval(command)
        else:
            entities = []
            for result in eval(command):
                e = entity(self.db)
                setattr(e, '_id', result.get('_id'))
                for f, val in e.fields:
                    setattr(e, f, result.get(f))
                entities.append(e)
            
            return entities
        
    def delete_one(self, entity, _id):
        """
        Deletes a single entity from the datastore based on the id given
        
        entity should be a string
        _id should be the string entity id
        
        e.g.
        todoId = '5047b7bb37d5e64e9a4b1c74'
        EntityManager(_DBCON).delete_one('Todo', todoId)
        """
        command = 'self.db.%s.remove({"_id":ObjectId("%s")})' % (entity, str(_id))
        if DBDEBUG: Logger.log_to_file(command)
        eval(command)
        