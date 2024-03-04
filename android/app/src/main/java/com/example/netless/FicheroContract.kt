package com.example.netless

import android.provider.BaseColumns

object FicheroContract {
    object FicheroEntry : BaseColumns {
        const val TABLE_NAME = "Fichero"
        const val COLUMN_NAME_NOMBRE = "nombre"
    }

    private const val SQL_CREATE_ENTRIES =
        "CREATE TABLE ${FicheroEntry.TABLE_NAME} (" +
            "${BaseColumns._ID} INTEGER PRIMARY KEY," +
            "${FicheroEntry.COLUMN_NAME_NOMBRE} TEXT," +
        ")"
    
    private const val SQL_DELETE_ENTRIES = "DROP TABLE IF EXISTS ${FicheroEntry.TABLE_NAME}"
}
