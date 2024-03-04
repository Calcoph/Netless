package com.netless.database

import android.provider.BaseColumns

object EnviablesChatContract {
    object EnviablesChatEntry : BaseColumns {
        const val TABLE_NAME = "EnviablesChat"
        const val COLUMN_NAME_CHAT_ID = "chat_id"
        const val COLUMN_NAME_ENV_ID = "env_id"
    }

    const val SQL_CREATE_ENTRIES =
        "CREATE TABLE ${EnviablesChatEntry.TABLE_NAME} (" +
            "${EnviablesChatEntry.COLUMN_NAME_CHAT_ID} INTEGER," +
            "${EnviablesChatEntry.COLUMN_NAME_ENV_ID} INTEGER," +
            "CONSTRAINT prim_eky PRIMARY KEY (${EnviablesChatEntry.COLUMN_NAME_CHAT_ID}, ${EnviablesChatEntry.COLUMN_NAME_ENV_ID})" +
            "CONSTRAINT fk_chat FOREIGN KEY (${EnviablesChatEntry.COLUMN_NAME_CHAT_ID}) REFERENCES ${ChatContract.ChatEntry.TABLE_NAME} (${BaseColumns._ID})" +
            "CONSTRAINT fk_env FOREIGN KEY (${EnviablesChatEntry.COLUMN_NAME_ENV_ID}) REFERENCES ${EnviableContract.EnviableEntry.TABLE_NAME} (${BaseColumns._ID})" +
        ")"
    
    const val SQL_DELETE_ENTRIES = "DROP TABLE IF EXISTS ${EnviablesChatEntry.TABLE_NAME}"
}
