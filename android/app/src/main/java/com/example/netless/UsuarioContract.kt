package com.example.netless

import android.provider.BaseColumns

object UsuarioContract {
    object UsuarioEntry : BaseColumns {
        const val TABLE_NAME = "Usuarios"
        const val COLUMN_NAME_ALIAS = "alias"
        const val COLUMN_NAME_ID = "id"
        const val COLUMN_NAME_CHAT_ID = "chat_id"
    }

    const val SQL_CREATE_ENTRIES =
        "CREATE TABLE ${UsuarioEntry.TABLE_NAME} (" +
            "${BaseColumns._ID} INTEGER PRIMARY KEY," +
            "${UsuarioEntry.COLUMN_NAME_ALIAS} TEXT," +
            "${UsuarioEntry.COLUMN_NAME_SUBTITLE} TEXT" +
            "${UsuarioEntry.COLUMN_NAME_CHAT_ID} INTEGER" + // TODO: References
        ")"
    
    const val SQL_DELETE_ENTRIES = "DROP TABLE IF EXISTS ${UsuarioEntry.TABLE_NAME}"
}
