package com.example.netless

import android.provider.BaseColumns

object WhitelistContract {
    object WhitelistEntry : BaseColumns {
        const val TABLE_NAME = "Whitelist"
        const val COLUMN_NAME_USR_ID = "usr_id"
    }

    const val SQL_CREATE_ENTRIES =
        "CREATE TABLE ${WhitelistEntry.TABLE_NAME} (" +
            "${BaseColumns._ID} INTEGER PRIMARY KEY," +
            "${WhitelistEntry.COLUMN_NAME_USR_ID} TEXT," + // TODO: References
        ")"
    
    const val SQL_DELETE_ENTRIES = "DROP TABLE IF EXISTS ${WhitelistEntry.TABLE_NAME}"
}
