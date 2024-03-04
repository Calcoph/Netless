package com.example.netless

import android.provider.BaseColumns

object MensajeContract {
    object MensajeEntry : BaseColumns {
        const val TABLE_NAME = "Mensaje"
        const val COLUMN_NAME_MENS = "mens"
    }

    const val SQL_CREATE_ENTRIES =
        "CREATE TABLE ${MensajeEntry.TABLE_NAME} (" +
            "${BaseColumns._ID} INTEGER PRIMARY KEY," +
            "${MensajeEntry.COLUMN_NAME_MENS} TEXT," +
        ")"
    
    const val SQL_DELETE_ENTRIES = "DROP TABLE IF EXISTS ${MensajeEntry.TABLE_NAME}"
}
