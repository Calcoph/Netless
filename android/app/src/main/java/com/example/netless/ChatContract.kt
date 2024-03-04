package com.example.netless

import android.provider.BaseColumns

object ChatContract {
    object ChatEntry : BaseColumns {
        const val TABLE_NAME = "Chat"
    }

    private const val SQL_CREATE_ENTRIES =
        "CREATE TABLE ${ChatEntry.TABLE_NAME} (" +
            "${BaseColumns._ID} INTEGER PRIMARY KEY," +
        ")"
    
    private const val SQL_DELETE_ENTRIES = "DROP TABLE IF EXISTS ${ChatEntry.TABLE_NAME}"
}
