import asyncpg
import pandas as pd
from typing import Dict, Any

from models.models import Rule, Datasource


class RuleEngine:
    def __init__(self, datasource: Datasource):
        self.datasource = datasource
        self.connection_string = self._build_connection_string()
    
    def _build_connection_string(self) -> str:
        return f"postgresql://{self.datasource.username}:{self.datasource.password}@{self.datasource.host}:{self.datasource.port}/{self.datasource.database}"
    
    async def execute_rule(self, rule: Rule) -> Dict[str, Any]:
        """Execute a rule and return results"""
        conn = await asyncpg.connect(self.connection_string)
        
        try:
            if rule.rule_type == "completeness":
                return await self._check_completeness(conn, rule)
            elif rule.rule_type == "accuracy":
                return await self._check_accuracy(conn, rule)
            elif rule.rule_type == "uniqueness":
                return await self._check_uniqueness(conn, rule)
            elif rule.rule_type == "timeliness":
                return await self._check_timeliness(conn, rule)
            else:
                raise ValueError(f"Unknown rule type: {rule.rule_type}")
        finally:
            await conn.close()
    
    async def _check_completeness(self, conn: asyncpg.Connection, rule: Rule) -> Dict[str, Any]:
        """Check for null values in specified columns"""
        config = rule.rule_config
        columns = config.get("columns", [])
        
        results = {}
        total_rows = await conn.fetchval(f"SELECT COUNT(*) FROM {rule.table_name}")
        
        for column in columns:
            null_count = await conn.fetchval(
                f"SELECT COUNT(*) FROM {rule.table_name} WHERE {column} IS NULL"
            )
            completeness = (total_rows - null_count) / total_rows * 100 if total_rows > 0 else 100
            results[column] = {
                "total": total_rows,
                "null_count": null_count,
                "completeness": round(completeness, 2)
            }
        
        # Calculate overall pass rate
        avg_completeness = sum(r["completeness"] for r in results.values()) / len(results) if results else 100
        failed_rows = sum(r["null_count"] for r in results.values())
        
        return {
            "rule_type": "completeness",
            "total_rows": total_rows,
            "failed_rows": failed_rows,
            "pass_rate": round(avg_completeness, 2),
            "details": results
        }
    
    async def _check_accuracy(self, conn: asyncpg.Connection, rule: Rule) -> Dict[str, Any]:
        """Check value ranges and formats"""
        config = rule.rule_config
        column = config.get("column")
        min_val = config.get("min")
        max_val = config.get("max")
        
        total_rows = await conn.fetchval(f"SELECT COUNT(*) FROM {rule.table_name}")
        
        conditions = []
        if min_val is not None:
            conditions.append(f"{column} >= {min_val}")
        if max_val is not None:
            conditions.append(f"{column} <= {max_val}")
        
        where_clause = " AND ".join(conditions) if conditions else "TRUE"
        
        valid_count = await conn.fetchval(
            f"SELECT COUNT(*) FROM {rule.table_name} WHERE {where_clause}"
        )
        
        invalid_count = total_rows - valid_count
        pass_rate = (valid_count / total_rows * 100) if total_rows > 0 else 100
        
        return {
            "rule_type": "accuracy",
            "total_rows": total_rows,
            "failed_rows": invalid_count,
            "pass_rate": round(pass_rate, 2),
            "details": {
                "column": column,
                "min": min_val,
                "max": max_val,
                "valid_count": valid_count,
                "invalid_count": invalid_count
            }
        }
    
    async def _check_uniqueness(self, conn: asyncpg.Connection, rule: Rule) -> Dict[str, Any]:
        """Check for duplicate values"""
        config = rule.rule_config
        columns = config.get("columns", [])
        column_str = ", ".join(columns)
        
        total_rows = await conn.fetchval(f"SELECT COUNT(*) FROM {rule.table_name}")
        
        # Count duplicates
        duplicate_query = f"""
            SELECT COUNT(*) FROM (
                SELECT {column_str}, COUNT(*) as cnt
                FROM {rule.table_name}
                GROUP BY {column_str}
                HAVING COUNT(*) > 1
            ) dupes
        """
        duplicate_count = await conn.fetchval(duplicate_query)
        
        unique_count = total_rows - duplicate_count
        pass_rate = (unique_count / total_rows * 100) if total_rows > 0 else 100
        
        return {
            "rule_type": "uniqueness",
            "total_rows": total_rows,
            "failed_rows": duplicate_count,
            "pass_rate": round(pass_rate, 2),
            "details": {
                "columns": columns,
                "duplicate_count": duplicate_count
            }
        }
    
    async def _check_timeliness(self, conn: asyncpg.Connection, rule: Rule) -> Dict[str, Any]:
        """Check data freshness"""
        config = rule.rule_config
        column = config.get("column")
        max_delay_hours = config.get("max_delay_hours", 24)
        
        # Get latest timestamp
        latest_query = f"SELECT MAX({column}) FROM {rule.table_name}"
        latest_ts = await conn.fetchval(latest_query)
        
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        
        if latest_ts:
            if isinstance(latest_ts, str):
                latest_ts = datetime.fromisoformat(latest_ts.replace('Z', '+00:00'))
            delay_hours = (now - latest_ts).total_seconds() / 3600
            is_fresh = delay_hours <= max_delay_hours
        else:
            delay_hours = None
            is_fresh = False
        
        return {
            "rule_type": "timeliness",
            "total_rows": 1,
            "failed_rows": 0 if is_fresh else 1,
            "pass_rate": 100 if is_fresh else 0,
            "details": {
                "column": column,
                "latest_timestamp": str(latest_ts) if latest_ts else None,
                "delay_hours": round(delay_hours, 2) if delay_hours else None,
                "max_delay_hours": max_delay_hours,
                "is_fresh": is_fresh
            }
        }
