import pygame
from collections import defaultdict

class SkillEventManager:
    """A static event manager to handle skill-related events without conflicts."""
    
    _event_callbacks = defaultdict(list)  # Stores event types and their callbacks
    _callback_sources = defaultdict(dict)  # Stores callback -> source class mapping

    @staticmethod
    def add_event_listener(event_type, callback, classFrom):
        """Registers a callback function for a specific event."""
        if callback not in SkillEventManager._event_callbacks[event_type]:
            SkillEventManager._event_callbacks[event_type].append(callback)
            SkillEventManager._callback_sources[event_type][callback] = classFrom  # Track class source

    @staticmethod
    def trigger_event(event_type, *args, **kwargs):
        """Triggers all callbacks for a given event."""
        if event_type in SkillEventManager._event_callbacks:
            callbacks = list(SkillEventManager._event_callbacks[event_type])  # Prevent modification issues
            for callback in callbacks:
                try:
                    callback(*args, **kwargs)  # Ensure all callbacks execute safely
                except Exception as e:
                    print(f"Error in event '{event_type}': {e}")

    @staticmethod
    def remove_event_listener(event_type, classFrom):
        """Removes all callbacks for a specific class under the given event."""
        if event_type in SkillEventManager._callback_sources:
            callbacks_to_remove = [cb for cb, source in SkillEventManager._callback_sources[event_type].items() if source == classFrom]
            
            for callback in callbacks_to_remove:
                if callback in SkillEventManager._event_callbacks[event_type]:
                    SkillEventManager._event_callbacks[event_type].remove(callback)
                    del SkillEventManager._callback_sources[event_type][callback]

            # ❌ Only delete the event if there are **no remaining callbacks**
            if not SkillEventManager._event_callbacks[event_type]:  
                del SkillEventManager._event_callbacks[event_type]
                del SkillEventManager._callback_sources[event_type]

    @staticmethod
    def clear_event(event_type):
        """Removes all listeners for a specific event type."""
        SkillEventManager._event_callbacks.pop(event_type, None)
        SkillEventManager._callback_sources.pop(event_type, None)

    @staticmethod
    def clear_all_events():
        """Removes all registered event callbacks."""
        SkillEventManager._event_callbacks.clear()
        SkillEventManager._callback_sources.clear()
