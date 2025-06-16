from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.data.models import Alert
from app.data.enums import AlertSeverity, AlertType

class AlertRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, alert: Alert) -> Alert:
        """Create a new alert."""
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def get_by_id(self, alert_id: int) -> Optional[Alert]:
        """Get alert by ID."""
        return self.db.query(Alert).filter(Alert.id == alert_id).first()

    def get_by_robot_id(self, robot_id: str) -> List[Alert]:
        """Get all alerts for a robot."""
        return self.db.query(Alert).filter(Alert.robot_id == robot_id).all()

    def get_by_severity(self, severity: AlertSeverity) -> List[Alert]:
        """Get all alerts of a specific severity."""
        return self.db.query(Alert).filter(Alert.severity == severity.value).all()

    def get_by_type(self, alert_type: AlertType) -> List[Alert]:
        """Get all alerts of a specific type."""
        return self.db.query(Alert).filter(Alert.type == alert_type.value).all()

    def update(self, alert_id: int, data: dict) -> Optional[Alert]:
        """Update an alert."""
        alert = self.get_by_id(alert_id)
        if alert:
            for key, value in data.items():
                setattr(alert, key, value)
            self.db.commit()
            self.db.refresh(alert)
        return alert

    def delete(self, alert_id: int) -> bool:
        """Delete an alert."""
        alert = self.get_by_id(alert_id)
        if alert:
            self.db.delete(alert)
            self.db.commit()
            return True
        return False

    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts (not older than 24 hours)."""
        cutoff_time = datetime.utcnow() - datetime.timedelta(hours=24)
        return self.db.query(Alert).filter(Alert.timestamp >= cutoff_time).all() 