from .mod import Mod, RepoTypes
from .config import config
from .logger import LogColors, Logger
from typing import List
from os import path
import sqlite3


class _Column:
    id = "id"
    repo_type = "repo_type"
    repo_name = "repo_name"
    upload_time = "upload_time"
    active = "active"


class Db:
    def __init__(self) -> None:
        file_path = path.join(config.dir, f".{config.app_name}.db")
        Logger.debug(f"DB location: {file_path}")
        self._connection = sqlite3.connect(file_path)
        self._cursor = self._connection.cursor()
        self._create_db()

    def _create_db(self):
        self._connection.execute(
            f"CREATE TABLE IF NOT EXISTS mod ({_Column.id} TEXT, {_Column.repo_type} TEXT, {_Column.repo_name}, {_Column.upload_time} INTEGER, {_Column.active} INTEGER)"
        )
        self._connection.commit()

    def close(self) -> None:
        self._cursor.close()
        self._connection.commit()
        self._connection.close()

    def sync_with_dir(self, mods: List[Mod]) -> List[Mod]:
        """Synchronize DB with the mods in the folder. This makes sure that we don't download
        mods that have been removed manually.

        Args:
            mods (List[Mod]): Mods present in the mods directory

        Returns:
            List[Mod]: Updated list with
        """
        mods = mods.copy()
        mods_to_add = mods.copy()
        mod_infos = {}

        # Go through all existing mods in the DB and see which should be added and removed
        self._cursor.execute(
            f"SELECT {_Column.id}, {_Column.repo_type}, {_Column.repo_name}, {_Column.upload_time}, {_Column.active} FROM mod"
        )
        rows = self._cursor.fetchall()
        for row in rows:
            id = str(row[0])
            repo_type = str(row[1])
            repo_name = str(row[2])
            upload_time = int(row[3])
            active = bool(row[4])
            mod_infos[id] = {
                _Column.repo_type: repo_type,
                _Column.repo_name: repo_name,
                _Column.upload_time: upload_time,
                _Column.active: active,
            }

            # Search for existing info
            found = False
            for mod in mods_to_add:
                if mod.id == id:
                    found = True
                    mods_to_add.remove(mod)
                    Logger.debug(f"Found mod {mod.id} in DB", LogColors.found)

                    # Reactivate mod
                    if not active:
                        self._activate_mod(mod.id)
                    break

            # Inactivate mod
            if not found:
                self._inactivate_mod(id)

        # Add mods
        for mod in mods_to_add:
            Logger.debug(f"Adding mod {mod.id} to DB", LogColors.add)
            self._connection.execute(
                f"INSERT INTO mod ({_Column.id}, {_Column.repo_type}, {_Column.repo_name}, {_Column.upload_time}, {_Column.active}) VALUES (?, ?, ?, ?, 1)",
                [mod.id, mod.repo_type.value, mod.repo_name_alias, mod.upload_time],
            )

        # Update mod info
        for mod in mods:
            if mod.id in mod_infos:
                mod_info = mod_infos[mod.id]
                mod.repo_type = RepoTypes[mod_info[_Column.repo_type]]
                mod.repo_name_alias = mod_info[_Column.repo_name]
                mod.upload_time = mod_info[_Column.upload_time]

        return mods

    def update_mod(self, mod: Mod):
        self._connection.execute(
            f"UPDATE mod SET {_Column.repo_type}=?, {_Column.repo_name}=?, {_Column.upload_time}=? WHERE {_Column.id}=?",
            [mod.repo_type.value, mod.repo_name_alias, mod.upload_time, mod.id],
        )
        self._connection.commit()

    def _activate_mod(self, id: str):
        Logger.debug(f"Reactivate mod {id} in DB", LogColors.add)
        self._connection.execute(
            f"UPDATE mod SET {_Column.active}=1 WHERE {_Column.id}=?", [id]
        )
        self._connection.commit()

    def _inactivate_mod(self, id: str):
        Logger.debug(f"Inactivate mod {id} in DB", LogColors.remove)
        self._connection.execute(
            f"UPDATE mod SET {_Column.active}=0 WHERE {_Column.id}=?", [id]
        )
        self._connection.commit()
