from typing import List, Optional

from sqlalchemy.engine.reflection import Inspector

from superset.db_engine_specs.hive import HiveEngineSpec


class DatabricksEngineSpec(HiveEngineSpec):
    engine = "databricks"

    @classmethod
    def get_schema_names(cls, inspector: Inspector) -> List[str]:
        base_schema = super(DatabricksEngineSpec, cls).get_schema_names(inspector)
        return ["global_temp"] + base_schema
