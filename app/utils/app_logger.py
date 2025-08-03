import logging
from app.models.logger import LoggerModel
from app.models.databases.base import SessionLocal


class AppLogger:
    def create_logger(self, name):
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')  # noqa: E501
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)

        if logger.handlers:
            for handler in logger.handlers:
                logger.removeHandler(handler)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.propagate = False
        return logger

    def set_log_message(self, logger, body: LoggerModel):
        type = getattr(body, 'type', 'info')

        # Log no console
        if type == 'info':
            logger.info(body)
        elif type == 'error':
            logger.error(body)
        elif type == 'warning':
            logger.warning(body)

        # Log na base de dados usando o modelo SQLAlchemy
        from app.models.databases.logs import Log
        session = SessionLocal()
        try:
            log_entry = Log(
                time=body.time,
                status_code=body.status_code,
                endpoint=body.endpoint,
                message=body.message,
                type=getattr(body, 'type', 'info'),
                method=getattr(body, 'method', None),
                latency=getattr(body, 'latency', None)
            )
            session.add(log_entry)
            session.commit()
        except Exception as e:
            logger.error(f"Erro ao registrar log na base: {e}")
            session.rollback()
        finally:
            session.close()
