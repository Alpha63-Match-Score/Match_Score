import os
import sys
from pathlib import Path

# Добавяме root директорията в sys.path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from sqlalchemy import text
from src.database.session import engine, init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_db():
    try:
        # Проверка на връзката
        logger.info("Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful!")

        # Създаване на таблици
        logger.info("Attempting to create tables...")
        init_db()

        # Проверка на създадените таблици
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = result.fetchall()
            logger.info("\nCreated tables:")
            for table in tables:
                logger.info(f"- {table[0]}")

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Project root: {project_root}")
    test_db()