package com.example.netless

import android.provider.BaseColumns

object EnviablesChatContract {
    object EnviablesChatEntry : BaseColumns {
        const val TABLE_NAME = "EnviablesChat"
        const val COLUMN_NAME_CHAT_ID = "chat_id"
        const val COLUMN_NAME_ENV_ID = "env_id"
    }

    const val SQL_CREATE_ENTRIES =
        "CREATE TABLE ${EnviablesChatEntry.TABLE_NAME} (" +
            "${EnviablesChatEntry.COLUMN_NAME_CHAT_ID} INTEGER PRIMARY KEY," + // TODO: References
            "${EnviablesChatEntry.COLUMN_NAME_ENV_ID} INTEGER PRIMARY KEY," + // TODO: References
        ")"
    
    const val SQL_DELETE_ENTRIES = "DROP TABLE IF EXISTS ${EnviablesChatEntry.TABLE_NAME}"
}
