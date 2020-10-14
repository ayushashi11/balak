import json
from typing import Union
class SettingsNotLocked(Exception):
    pass

class Settings:
    def __init__(self, js: dict) -> None:
        self._js = js
        print(self._js)
    
    def set_sys_channel(self, guild_id: str, chan_id: int) -> None:
        if guild_id in self._js:
            self._js[guild_id]["systemchannel"] = chan_id
        else:
            self._js[guild_id] = {"systemchannel": chan_id}
    
    def get_sys_channel(self, guild_id: str) -> Union[int, None]:
        try:
            return self._js[guild_id]["systemchannel"]
        except (IndexError, KeyError):
            return None
    def set_ann_channel(self, guild_id: str, chan_id: int) -> None:
        if guild_id in self._js:
            self._js[guild_id]["announcementchannel"] = chan_id
        else:
            self._js[guild_id] = {"announcementchannel": chan_id}
    
    def add_reactor_channel(self, guild_id: str, msg_id: str, reactions: dict) -> None:
        if guild_id in self._js:
            try:
                self._js[guild_id]["reactors"][msg_id] = reactions
            except KeyError:
                self._js[guild_id]["reactors"] = {msg_id: reactions}
        else:
            self._js[guild_id] = {"reactors": {msg_id: reactions}}
    
    def get_reaction_role(self, guild_id: str, msg_id: str, emoji: str) -> Union[str, None]:
        try:
            return self._js[guild_id][msg_id][emoji]
        except (IndexError, KeyError):
            print("8h", self._js, guild_id, msg_id, emoji)
            return None
    
    def get_ann_channel(self, guild_id: str) -> Union[int, None]:
        try:
            return self._js[guild_id]["announcementchannel"]
        except (IndexError, KeyError):
            return None
    def get(self) -> dict:
        ret = self._js 
        del self
        return ret
class SettingsManager:
    def __init__(self) -> None:
        self.filename = "settings.json"
        self.lock = None
    
    def __enter__(self) -> Settings:
        while self.lock is not None:
            pass
        self.lock = Settings(json.load(open(self.filename))["settings"])
        return self.lock
    
    def __exit__(self, *_args) -> None:
        json.dump({"settings": self.lock.get()}, open(self.filename, "w"))
        self.lock = None