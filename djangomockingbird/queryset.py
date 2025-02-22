import datetime
import collections
from djangomockingbird.queryset_utils import *


#queryset that returns mock class objects
class MockBaseQueryset(object):

    def __init__(self, mock_class, model_dict):
        self.mock_class = mock_class
        self.model_dict = model_dict

    #methods that return new querysets
    def filter(self, *args, **kwargs):
        return self

    def exclude(self, *args, **kwargs):
        return self

    def annotate(self, *args, **kwargs):

        model_class = annotate_mock_class(kwargs, self.mock_class)

        return self      

    def order_by(self, *args, **kwargs):
        return self

    def reverse(self, *args, **kwargs):
        return self

    def distinct(self, *args, **kwargs):
        return self  

    def values(self, *args, **kwargs):
        return MockDerivedQueryset(self.model_dict)

    def values_list(self, *args, **kwargs):

        mock_values_list = make_mock_list_from_args(args)
        mock_values_tuple = tuple(mock_values_list)
        mock_fields_list = get_keys_from_dict(self.model_dict)
        mock_named_tuple = collections.namedtuple('Mock_named_tuple', mock_fields_list)

        if 'flat' in kwargs and kwargs['flat'] == True:
            return MockDerivedQueryset(mock_values_list)

        elif 'named' in kwargs and kwargs['named'] == True:

            return MockDerivedQueryset(mock_named_tuple) 
        else:
            return MockDerivedQueryset(mock_values_tuple)

    def dates(self, *args, **kwargs):
        return MockDerivedQueryset(datetime.datetime(2000, 1, 1))

    def datetimes(self, *args, **kwargs):
        return MockDerivedQueryset(datetime.datetime(2000, 1, 1))    

    def none(self, *args, **kwargs):
        return None   

    def all(self):
        return self  

    def union(self, *args, **kwargs):
        return self

    def intersection(self, *args, **kwargs):
        return self

    def difference(self, *args, **kwargs):
        return self

    def select_related(self, *args, **kwargs):
        return self

    def prefetch_related(self, *args, **kwargs):
        return  self   

    def extra(self, *args, **kwargs):
        return self

    def defer(self, *args, **kwargs):
        return self

    def only(self, *args, **kwargs):
        return self

    def using(self, *args, **kwargs):
        return self

    def select_for_update(self, *args, **kwargs):
        return self

    def raw(self, *args, **kwargs):
        return self       

    #methods that do not return querysets
    def get(self, *args, **kwargs):
        return self.mock_class()

    def create(self, *args, **kwargs):
        return None

    def get_or_create(self, *args, **kwargs):
        return (self.mock_class(), True)

    def update_or_create(self, *args, **kwargs):
        return (self.mock_class(), True)

    def bulk_create(self, *args, **kwargs):
        return None

    def bulk_update(self, *args, **kwargs):
        return None

    def count(self, *args, **kwargs):
        return 1

    def in_bulk(self, *args, **kwargs):

        mock_in_bulk_dict = make_mock_in_bulk_dict(args)
    
        return mock_in_bulk_dict

    def iterator(self, *args, **kwargs):
        return [self.mock_class()]    
    
    def latest(self, *args, **kwargs):
        return self.mock_class() 
    
    def earliest(self, *args, **kwargs):
        return self.mock_class()    

    def first(self, *args, **kwargs):
        return self.mock_class()

    def last(self, *args, **kwargs):
        return self.mock_class()         
    
    def aggregate(self, *args, **kwargs):

        mock_aggregate_dict = make_mock_aggregate_dict(kwargs)

        return mock_aggregate_dict


    def exists(self, *args, **kwargs):
        return True   

    def update(self, *args, **kwargs):
        return 1    
    
    def delete(self, *args, **kwargs):
        return 1

    def as_manager(self, *args, **kwargs):
        return self
    #TODO

    def explain(self, *args, **kwargs):
        return 'mock explain'

    #extra methods/protocols
    def __len__(self):
        return 1

    def __iter__(self):
        return iter([self.mock_class()])

    def __next__(self):
        return self.mock_class()

    def __getitem__(self, key):
        return self.mock_class()

    #methods for evaluating querysets
    def repr(self, *args, **kwargs):
        return self.mock_class()

    def list(self, *args, **kwargs):
        return [self.mock_class()]

    def bool(self, *args, **kwargs):
        return True


#queryset that returns something other than mock class objects: dicts, tuples, datetime objects etc.
class MockDerivedQueryset(MockBaseQueryset):

    def __init__(self,return_value):
        self.return_value = return_value

    #methods that do not return querysets
    def get(self, *args, **kwargs):
        return self.return_value

    def get_or_create(self, *args, **kwargs):
        return (self.return_value, True)

    def update_or_create(self, *args, **kwargs):
        return (self.return_value, True)

    def iterator(self, *args, **kwargs):
        return [self.return_value]    
    
    def latest(self, *args, **kwargs):
        return self.return_value
    
    def earliest(self, *args, **kwargs):
        return self.return_value

    def first(self, *args, **kwargs):
        return self.return_value

    def last(self, *args, **kwargs):
        return self.return_value

    #extra methods/protocols
    def __iter__(self):
        return iter([self.return_value])

    def __next__(self):
        return self.return_value

    def __getitem__(self, key):
        return self.return_value   

    #methods for evaluating querysets
    def repr(self, *args, **kwargs):
        return self.return_value

    def list(self, *args, **kwargs):
        return [self.return_value]

    #other methods
    def annotate(self, *args, **kwargs):

        annotated_return_value = annotate_return_value(self.return_value, kwargs)
       
        return MockDerivedQueryset(annotated_return_value)



class MockRelatedManager(MockBaseQueryset):
    def __init__(self, mock_class, model_dict):
        self.mock_class = mock_class
        self.model_dict = model_dict

    def add(self, *args, **kwargs):
        MockBaseQueryset(self.mock_class, self.model_dict)

    def create(self, *args, **kwargs):
        MockBaseQueryset(self.mock_class, self.model_dict)

    def set(self, *args, **kwargs):
        MockBaseQueryset(self.mock_class, self.model_dict)

    def remove(self, *args, **kwargs):
        MockBaseQueryset(self.mock_class, self.model_dict)

    def clear(self, *args, **kwargs):
        MockBaseQueryset(self.mock_class, self.model_dict)

