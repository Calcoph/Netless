package com.example.netless

import android.provider.BaseColumns

object OpcionesContract {
    object OpcionesEntry : BaseColumns {
        const val TABLE_NAME = "Opciones"
        const val COLUMN_NAME_ALIAS = "alias"
        const val COLUMN_NAME_ID = "id"
    }

    const val SQL_CREATE_ENTRIES =
        "CREATE TABLE ${OpcionesEntry.TABLE_NAME} (" +
            "${BaseColumns._ID} INTEGER PRIMARY KEY," +
            "${OpcionesEntry.COLUMN_NAME_ALIAS} TEXT," +
            "${OpcionesEntry.COLUMN_NAME_ID} TEXT," +
        ")"
    
    const val SQL_DELETE_ENTRIES = "DROP TABLE IF EXISTS ${OpcionesEntry.TABLE_NAME}"
}
