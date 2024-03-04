package com.netless.database

import android.provider.BaseColumns

object EnviableContract {
    object EnviableEntry : BaseColumns {
        const val TABLE_NAME = "Enviable"
        const val COLUMN_NAME_FECHA = "fecha"
        const val COLUMN_NAME_DIRECCION = "direccion"
        const val COLUMN_NAME_FICH_ID = "fich_id"
        const val COLUMN_NAME_MENS_ID = "mens_id"
    }

    const val SQL_CREATE_ENTRIES =
        "CREATE TABLE ${EnviableEntry.TABLE_NAME} (" +
            "${BaseColumns._ID} INTEGER PRIMARY KEY," +
            "${EnviableEntry.COLUMN_NAME_FECHA} DATE," +
            "${EnviableEntry.COLUMN_NAME_DIRECCION} INTEGER," +
            "${EnviableEntry.COLUMN_NAME_FICH_ID} INTEGER," +
            "${EnviableEntry.COLUMN_NAME_MENS_ID} INTEGER," +
            "CONSTRAINT fk_fich FOREIGN KEY (${EnviableEntry.COLUMN_NAME_FICH_ID}) REFERENCES ${FicheroContract.FicheroEntry.TABLE_NAME} (${BaseColumns._ID})" +
            "CONSTRAINT fk_mens FOREIGN KEY (${EnviableEntry.COLUMN_NAME_MENS_ID}) REFERENCES ${MensajeContract.MensajeEntry.TABLE_NAME} (${BaseColumns._ID})" +
        ")"
    
    const val SQL_DELETE_ENTRIES = "DROP TABLE IF EXISTS ${EnviableEntry.TABLE_NAME}"
}
