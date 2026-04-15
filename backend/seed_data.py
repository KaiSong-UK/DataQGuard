"""
DataQGuard - Database seeding script
Creates demo data on first startup for a visually impressive demo.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import engine, async_session, Base
from core.security import get_password_hash
from models.models import User, Datasource, Rule, RuleExecution, Alert
from datetime import datetime, timedelta, timezone


async def seed_database():
    """Seed the database with demo data."""
    print("🌱 Seeding database with demo data...")

    async with async_session() as session:
        # Check if already seeded
        result = await session.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        if count > 0:
            print(f"✅ Database already has {count} users, skipping seed.")
            return

        # 1. Create admin user
        admin = User(
            email="admin@dataqguard.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Kai Song",
            is_active=True,
            is_superuser=True
        )
        session.add(admin)
        await session.flush()
        print("✅ Admin user created: admin@dataqguard.com / admin123")

        # 2. Create demo datasources
        datasources = [
            Datasource(
                name="Production PostgreSQL",
                type="postgresql",
                host="db",
                port=5432,
                database="dataqguard",
                username="postgres",
                password="postgres",
                is_active=True,
                created_by=admin.id
            ),
            Datasource(
                name="Analytics MySQL",
                type="mysql",
                host="mysql-analytics",
                port=3306,
                database="analytics",
                username="analyst",
                password="analyst123",
                is_active=True,
                created_by=admin.id
            ),
        ]
        for ds in datasources:
            session.add(ds)
        await session.flush()
        print(f"✅ Created {len(datasources)} datasources")

        # 3. Create demo rules
        rules = [
            Rule(
                name="orders.user_id completeness",
                description="Ensure user_id is never null in orders table",
                datasource_id=datasources[0].id,
                table_name="orders",
                rule_type="completeness",
                rule_config={
                    "columns": ["user_id", "email", "phone"]
                },
                schedule="0 */4 * * *",
                is_active=True,
                created_by=admin.id
            ),
            Rule(
                name="orders.amount accuracy",
                description="Ensure order amounts are within valid range",
                datasource_id=datasources[0].id,
                table_name="orders",
                rule_type="accuracy",
                rule_config={
                    "column": "amount",
                    "min": 0,
                    "max": 100000
                },
                schedule="0 */2 * * *",
                is_active=True,
                created_by=admin.id
            ),
            Rule(
                name="users.email uniqueness",
                description="Email should be unique across users",
                datasource_id=datasources[0].id,
                table_name="users",
                rule_type="uniqueness",
                rule_config={
                    "columns": ["email"]
                },
                schedule="0 6 * * *",
                is_active=True,
                created_by=admin.id
            ),
            Rule(
                name="orders.created_at timeliness",
                description="Orders must be synced within the last hour",
                datasource_id=datasources[0].id,
                table_name="orders",
                rule_type="timeliness",
                rule_config={
                    "column": "created_at",
                    "max_delay_hours": 1
                },
                schedule="*/15 * * * *",
                is_active=True,
                created_by=admin.id
            ),
            Rule(
                name="products.price accuracy",
                description="Product prices must be positive",
                datasource_id=datasources[0].id,
                table_name="products",
                rule_type="accuracy",
                rule_config={
                    "column": "price",
                    "min": 0.01
                },
                schedule="0 8 * * *",
                is_active=True,
                created_by=admin.id
            ),
        ]
        for rule in rules:
            session.add(rule)
        await session.flush()
        print(f"✅ Created {len(rules)} demo rules")

        # 4. Create historical execution records (last 7 days)
        now = datetime.now(timezone.utc)
        exec_statuses = ["success", "success", "success", "failed"]
        exec_pass_rates = [98.4, 100, 95.2, 0, 99.8, 97.3, 98.1, 99.5, 96.8, 100]

        executions = []
        for i, rule in enumerate(rules):
            for day_offset in range(7):
                # 2-3 executions per day
                for exec_num in range(2):
                    started = now - timedelta(days=day_offset, hours=exec_num * 8 + i)
                    status_idx = (i * 3 + day_offset + exec_num) % len(exec_statuses)
                    pass_idx = (i * 3 + day_offset + exec_num) % len(exec_pass_rates)
                    status = exec_statuses[status_idx]
                    pass_rate = exec_pass_rates[pass_idx] if status == "success" else 0.0
                    total = 12480 + (i * 320)
                    failed = int(total * (100 - pass_rate) / 100)

                    exec_record = RuleExecution(
                        rule_id=rule.id,
                        status=status,
                        started_at=started,
                        completed_at=started + timedelta(seconds=30),
                        total_rows=total,
                        failed_rows=failed,
                        pass_rate=pass_rate,
                        details={
                            "duration_ms": 2840 + i * 210,
                            "rows_checked": total,
                            "threshold": 95
                        }
                    )
                    executions.append(exec_record)

        for e in executions:
            session.add(e)
        await session.flush()
        print(f"✅ Created {len(executions)} execution records")

        # 5. Create sample alerts
        alerts = [
            Alert(
                rule_id=rules[0].id,
                execution_id=executions[3].id,
                severity="critical",
                message="users.email — 3 null values detected in last sync",
                channel="email",
                is_sent=True,
                sent_at=now - timedelta(hours=1),
                created_at=now - timedelta(hours=1)
            ),
            Alert(
                rule_id=rules[1].id,
                execution_id=executions[10].id,
                severity="warning",
                message="orders.amount — 48 rows exceeded max threshold 100000",
                channel="slack",
                is_sent=True,
                sent_at=now - timedelta(hours=4),
                created_at=now - timedelta(hours=4)
            ),
            Alert(
                rule_id=rules[3].id,
                execution_id=executions[7].id,
                severity="error",
                message="orders.created_at — data is 3.2 hours stale, exceeds 1h threshold",
                channel="webhook",
                is_sent=False,
                created_at=now - timedelta(minutes=20)
            ),
        ]
        for alert in alerts:
            session.add(alert)
        print(f"✅ Created {len(alerts)} demo alerts")

        await session.commit()
        print("\n🎉 Database seeding complete!")
        print("   Login: admin@dataqguard.com / admin123")


if __name__ == "__main__":
    asyncio.run(seed_database())
