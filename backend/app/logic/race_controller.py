from app.models.session import SessionState, FlagState, FlagType, TrackSector
from typing import Dict, List
from datetime import datetime


class RaceController:
    """Manages race session state and flag logic"""
    
    def __init__(self):
        self.sessions: Dict[str, SessionState] = {}
        self.active_session_id: str | None = None
    
    def create_session(self, session_id: str, session_type: str = "race") -> SessionState:
        """Initialize a new race session"""
        session = SessionState(
            session_id=session_id,
            session_type=session_type,
            current_flag=FlagState(flag_type=FlagType.GREEN, full_course=True)
        )
        self.sessions[session_id] = session
        self.active_session_id = session_id
        return session
    
    def get_active_session(self) -> SessionState | None:
        """Get the currently active session"""
        if self.active_session_id:
            return self.sessions.get(self.active_session_id)
        return None
    
    def set_flag(
        self, 
        flag_type: FlagType, 
        full_course: bool = True,
        sectors: List[TrackSector] = None,
        message: str = None
    ) -> FlagState:
        """Change flag state"""
        session = self.get_active_session()
        if not session:
            raise ValueError("No active session")
        
        flag_state = FlagState(
            flag_type=flag_type,
            full_course=full_course,
            affected_sectors=sectors or [],
            timestamp=datetime.utcnow(),
            message=message
        )
        
        session.current_flag = flag_state
        return flag_state
    
    def register_car(self, device_id: str):
        """Add a car to the active session"""
        session = self.get_active_session()
        if session and device_id not in session.active_cars:
            session.active_cars.append(device_id)
    
    def get_flag_status(self) -> FlagState | None:
        """Get current flag status"""
        session = self.get_active_session()
        return session.current_flag if session else None


# Global race controller instance
race_controller = RaceController()