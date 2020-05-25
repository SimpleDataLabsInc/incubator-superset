import logging

logger = logging.getLogger(__name__)
try:
    from pyhive.sqlalchemy_hive import HiveDialect, HiveTypeCompiler

    class SparkSqlTypeCompiler(HiveTypeCompiler):
        def visit_TINYINT(self, type_):
            return 'INT'


    class SparkSqlDialect(HiveDialect):
        name = "tspark"
        type_compiler = HiveTypeCompiler

        def get_table_names(self, connection, schema=None, **kw):
            query = 'SHOW TABLES'
            if schema:
                query += ' IN ' + self.identifier_preparer.quote_identifier(schema)
            return [row.tableName for row in connection.execute(query)]

except ImportError as e:
    logger.info("Ignoring Spark Dialect since pyhive is not installed")
    pass
