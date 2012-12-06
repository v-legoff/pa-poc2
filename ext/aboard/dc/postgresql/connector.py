# Copyright (c) 2012 LE GOFF Vincent
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Module defining the PostgreSQLConnector class."""

import os

driver = True

try:
    import postgresql
except ImportError:
    driver = False

from ext.aboard.dc.connector import DataConnector
from ext.aboard.dc import exceptions
from ext.aboard.model import exceptions as mod_exceptions
from ext.aboard.model.functions import *
from ext.aboard.model.types import *

PGSQL_TYPES = {
    Integer: "numeric",
    String: "text",
}

class PostgreSQLConnector(DataConnector):
    
    """Data connector for PostgreSQL.
    
    This data connector should read and write datas using the py-postgresql
    module: http://pypi.python.org/pypi/py-postgresql
    
    """
    
    name = "postgresql"
    def __init__(self):
        """Check the driver presence.
        
        If not found, raise a DriverNotFound exception.
        
        """
        if not driver:
            raise exceptions.DriverNotFound(
                    "the postgresql library (py-postgrseql module) " \
                            "can not be found")
        
        self.db_host = None
        self.db_port = None
        self.db_name = None
        self.db_user = None
        self.db_pass = ""
        self.created_tables = ()
    
    def setup(self, host=None, port=None, dbname=None, dbuser=None,
            dbpass=""):
        """Setup the data connector."""
        if host is None:
            raise exceptions.InsufficientConfiguration(
                    "the database host was not specified for " \
                    "the postgresql data connector")
        
        if port is None:
            raise exceptions.InsufficientConfiguration(
                    "the database port was not specified for " \
                    "the postgresql data connector")
        
        if dbname is None:
            raise exceptions.InsufficientConfiguration(
                    "the database name was not specified for " \
                    "the postgresql data connector")
        
        if dbuser is None:
            raise exceptions.InsufficientConfiguration(
                    "the database user was not specified for " \
                    "the postgresql data connector")
        
        DataConnector.__init__(self)
        if dbpass is None:
            dbpass = ""
        else:
            dbpass = str(dbpass)
        
        self.db_host = host
        self.db_port = port
        self.db_name = dbname
        self.db_user = dbuser
        self.db_pass = dbpass
        self.connection = postgresql.open("pq://{user}:{password}@{host}:{port}/{database}".format(
                user=dbuser, password=dbpass, host=host, port=port,
                database=dbname))
    
    def close(self):
        """Close the data connector."""
        self.connection.close()
    
    def destroy(self):
        """Erase EVERY stored data."""
        self.clear_cache()
        for model in self.models.values():
            name = get_plural_name(model)
            query = "DROP TABLE {}".format(name)
            self.connection.execute(query)
        
        self.connection.close()
    
    def record_models(self, models):
        """Record the tables."""
        query = "SELECT table_name FROM information_schema.tables"
        statement = self.connection.prepare(query)
        self.created_tables = tuple(row[0] for row in statement())
        DataConnector.record_models(self, models)
    
    def record_model(self, model):
        """Record a single model."""
        DataConnector.record_model(self, model)
        name = get_plural_name(model)
        if name not in self.created_tables:
            self.create_table(name, model)
    
    def create_table(self, name, model):
        """Create the PostgreSQL table related to the specified model."""
        fields = get_fields(model)
        sql_fields = []
        for field in fields:
            if field.auto_increment:
                sql_field = "SERIAL"
            else:
                sql_field = PGSQL_TYPES[type(field)]
            
            instruction = field.field_name + " " + sql_field
            if field.pkey:
                instruction += " PRIMARY KEY"
            sql_fields.append(instruction)
        
        query = "CREATE TABLE {} ({})".format(name, ", ".join(sql_fields))
        self.connection.execute(query)
    
    def loop(self):
        """Nothing to do right now."""
        pass
    
    def get_all_objects(self, model):
        """Return all the model's objects in a list."""
        name = get_name(model)
        plural_name = get_plural_name(model)
        fields = get_fields(model)
        objects = []
        query = "SELECT * FROM " + plural_name
        statement = self.connection.prepare(query)
        for row in statement():
            dict_fields = {}
            for i, field in enumerate(fields):
                dict_fields[field.field_name] = row[i]
            
            object = self.get_from_cache(model, dict_fields)
            if object is None:
                object = model.build(**dict_fields)
                self.cache_object(object)
            objects.append(object)
        
        return objects
    
    def find_object(self, model, pkey_values):
        """Return, if found, the specified object."""
        # First, look for the object in the cached tree
        pkey_values_list = list(pkey_values.values())
        object = self.get_from_cache(model, pkey_values)
        if object:
            return object
        
        query = "SELECT * FROM {} WHERE ".format(get_plural_name(model))
        params = []
        filters = []
        for i, (name, value) in enumerate(pkey_values.items()):
            filters.append("{}=${i}".format(name, i=i + 1))
            params.append(value)
        
        query += " AND ".join(filters)
        statement = self.connection.prepare(query)
        rows = statement(*params)
        if not rows:
            raise mod_exceptions.ObjectNotFound(model, pkey_values)
        
        row = rows[0]
        dict_fields = {}
        for i, field in enumerate(get_fields(model)):
            dict_fields[field.field_name] = row[i]
        
        object = model.build(**dict_fields)
        self.cache_object(object)
        return object
    
    def add_object(self, object):
        """Save the object, issued from a model."""
        name = get_name(type(object))
        fields = get_fields(type(object))
        plural_name = get_plural_name(type(object))
        query = "INSERT INTO " + plural_name + " ("
        names = []
        values = []
        auto_increments = []
        i = 1
        sql_fields = []
        for field in fields:
            if field.auto_increment:
                auto_increments.append(field.field_name)
                continue
            
            names.append(field.field_name)
            values.append(getattr(object, field.field_name))
            sql_fields.append("$" + str(i))
            i += 1
        
        query += ", ".join(names) + ") values("
        query += ", ".join(sql_fields) + ")"
        statement = self.connection.prepare(query)
        res = statement(*values)
        
        for field in auto_increments:
            query = "SELECT max(" + field + ") FROM " + plural_name
            statement = self.connection.prepare(query)
            value = statement()[0][0]
            update_attr(object, field, value)
        
        self.cache_object(object)
    
    def update_object(self, object, attribute):
        """Update an object."""
        self.check_update(object)
        plural_name = get_plural_name(type(object))
        keys = get_pkey_names(type(object))
        params = [getattr(object, attribute)]
        values = get_pkey_values(object)
        params.extend(values)
        names = [name + "=$" + str(i + 2) for i, name in enumerate(keys)]
        query = "UPDATE " + plural_name + " SET " + attribute + "=$1"
        query += " WHERE " + " AND ".join(names)
        statement = self.connection.prepare(query)
        res = statement(*params)
    
    def remove_object(self, object):
        """Delete the object."""
        name = get_name(type(object))
        plural_name = get_plural_name(type(object))
        keys = get_pkey_names(type(object))
        names = [name + "=$" + str(i + 1) for i, name in enumerate(keys)]
        values = tuple(get_pkey_values(object))
        query = "DELETE FROM " + plural_name
        query += " WHERE " + " AND ".join(names)
        statement = self.connection.prepare(query)
        res = statement(*values)
        
        # Delete from cache
        self.uncache_object(object)
