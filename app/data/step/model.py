from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.data.database import Base


class Step(Base):
    __tablename__ = "steps"

    uuid = Column(String, primary_key=True)
    location_x = Column(Float, nullable=False)
    location_y = Column(Float, nullable=False)
    robot_id = Column(String, ForeignKey("robots.id"))
    timestamp = Column(DateTime, default=datetime.now, nullable=False)

    # Relationships
    robot = relationship("Robot", back_populates="steps")

    def to_api_model(self):
        from app.api.step.model import RobotStep

        return RobotStep(
            uuid=self.uuid,
            location=(self.location_x, self.location_y),
            timestamp=self.timestamp,
        )

    @classmethod
    def from_api_model(cls, api_model, robot_id=None):
        return cls(
            uuid=api_model.uuid,
            location_x=api_model.location[0],
            location_y=api_model.location[1],
            robot_id=robot_id,
            timestamp=api_model.timestamp,
        )
