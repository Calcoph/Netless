package com.netless.main

import android.content.ContentValues
import android.content.Context
import android.provider.BaseColumns
import com.netless.database.UsuarioContract
import com.netless.database.WhitelistContract

class Whitelist {
    companion object {
        // Singleton pattern
        @Volatile
        private var lista: Whitelist? = null

        fun getWhitelist() =
            lista ?: synchronized(this) {
                lista ?: Whitelist().also { lista = it }
            }
    }

    private val listaIds = ArrayList<String>()

    fun anadirUsuario(id: String, context: Context) {
        listaIds.add(id)

        val dbHelper = DbHelper(context)
        val db = dbHelper.writableDatabase

        val projection = arrayOf(BaseColumns._ID)

        val selection = "${UsuarioContract.UsuarioEntry.COLUMN_NAME_ID} = ?"
        val selectionArgs = arrayOf(id)
        val cursor = db.query(
            UsuarioContract.UsuarioEntry.TABLE_NAME,
            projection,
            selection,
            selectionArgs,
            null,
            null,
            null
        )

        val usrId: Int;
        with(cursor) {
            moveToNext()
            usrId = getInt(getColumnIndexOrThrow(com.netless.database.UsuarioContract.UsuarioEntry.COLUMN_NAME_CHAT_ID))
        }
        cursor.close()

        val values = ContentValues().apply {
            put(WhitelistContract.WhitelistEntry.COLUMN_NAME_USR_ID, usrId)
        }

        val whitelistEntryId = db?.insert(WhitelistContract.WhitelistEntry.TABLE_NAME, null, values)
    }

    fun quitarUsuario(id: String, context: Context) {
        listaIds.remove(id)

        val dbHelper = DbHelper(context)
        val db = dbHelper.writableDatabase

        val selection = "${WhitelistContract.WhitelistEntry.COLUMN_NAME_USR_ID} = ?"
        val selectionArgs = arrayOf(id)

        val deletedRows = db.delete(WhitelistContract.WhitelistEntry.TABLE_NAME, selection, selectionArgs)
    }

    fun usuarioAceptado(id: String): Boolean {
        return listaIds.contains(id)
    }
}