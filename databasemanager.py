"""DatabaseManager Class."""

import sqlite3
from typing import Tuple, Dict, Any


class DatabaseManager:
    """Interface for Persistence Layer."""

    def __init__(self, database_filename: str) -> None:
        """Init method for DatabaseManager Class."""
        self.connection = sqlite3.connect(database_filename)

    def __del__(self) -> None:
        """Del method for DatabaseManager Class."""
        self.connection.close()

    def _execute(self,
                 statement: str,
                 values: Tuple = ()) -> Any:
        print(statement)
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values)
            return cursor

    def create_table(self,
                     table_name: str,
                     columns: Dict[str, str]) -> None:
        """Create table with given name and columns."""
        cols = [
            f"{col} {columns[col]}"
            for col in columns
        ]
        statement = f"""CREATE TABLE IF NOT EXISTS {table_name} \
            ( {', '.join(cols)} );"""
        self._execute(statement)

    def add(self,
            table_name: str,
            data: Dict[str, Any]) -> None:
        """Add a new record to the table."""
        placeholders = ", ".join("?" * len(data.values()))
        column_names = ", ".join(data.keys())
        column_values = tuple(data.values())
        statement = f"""INSERT INTO {table_name}({column_names}) VALUES \
            ({placeholders});"""
        self._execute(statement, column_values)

    def delete(self,
               table_name: str,
               criteria: Dict[str, Any]) -> None:
        """Delete record/records from the table."""
        placeholders = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholders)
        criteria_values = tuple(criteria.values())
        statement = f"""DELETE FROM {table_name} WHERE {delete_criteria}"""
        self._execute(statement, criteria_values)

    def update(self,
               table_name: str,
               criteria: Dict[str, Any],
               values: Dict[str, Any]) -> None:
        """Update record/records from the table."""
        placeholders = [f"{column} = ?" for column in criteria.keys()]
        update_criteria = " AND ".join(placeholders)
        criteria_values = tuple(criteria.values())
        placeholders = [f"{column} = ?" for column in values.keys()]
        updates = ", ".join(placeholders)
        update_values = tuple(values.values())
        statement = f"UPDATE {table_name} SET {updates}"
        statement += f" WHERE {update_criteria}"
        self._execute(statement, update_values + criteria_values)

    def select(self,
               table_name,
               criteria: Dict[str, Any] | None = None,
               order_by: str = '') -> Any:
        """Select record/records from the table."""
        statement = f"""SELECT * FROM {table_name}"""
        criteria_values = ()

        if criteria:
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            criteria_values = tuple(criteria.values())
            statement += f""" WHERE {select_criteria}"""

        if order_by:
            statement += f" ORDER BY {order_by}"

        statement += ";"

        return self._execute(statement, criteria_values)
