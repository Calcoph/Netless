package com.netless.main

import android.content.ContentValues
import android.content.Context
import com.netless.database.EnviableContract
import com.netless.database.EnviablesChatContract
import com.netless.database.FicheroContract
import com.netless.database.MensajeContract
import com.netless.database.UsuarioContract
import java.text.SimpleDateFormat

class HistorialChat {
    val listaEnviables = ArrayList<Enviable>()

    fun añadir_fichero(fichero: Fichero, id_usuario: String, context: Context) {
        val nombre = fichero.get_nombre()
        val fecha = fichero.get_fecha()
        val direccion = fichero.get_direccion()

        val dbHelper = DbHelper(context)
        val db = dbHelper.writableDatabase

        var values = ContentValues().apply {
            put(FicheroContract.FicheroEntry.COLUMN_NAME_NOMBRE, nombre)
        }

        val fichId = db?.insert(FicheroContract.FicheroEntry.TABLE_NAME, null, values)

        values = ContentValues().apply {
            put(EnviableContract.EnviableEntry.COLUMN_NAME_FECHA, DbHelper.dateToString(fecha))
            put(EnviableContract.EnviableEntry.COLUMN_NAME_DIRECCION, direccion.toInt())
            put(EnviableContract.EnviableEntry.COLUMN_NAME_FICH_ID, fichId)
        }

        val envId = db?.insert(EnviableContract.EnviableEntry.TABLE_NAME, null, values)?.toInt()!!

        añadir_enviable(fichero, envId, id_usuario, context)
    }

    fun añadir_mensaje(mens: Mensaje, id_usuario: String, context: Context) {
        val msg = mens.msg
        val fecha = mens.get_fecha()
        val direccion = mens.get_direccion()

        val dbHelper = DbHelper(context)
        val db = dbHelper.writableDatabase

        var values = ContentValues().apply {
            put(MensajeContract.MensajeEntry.COLUMN_NAME_MENS, msg)
        }

        val mensId = db?.insert(MensajeContract.MensajeEntry.TABLE_NAME, null, values)

        values = ContentValues().apply {
            put(EnviableContract.EnviableEntry.COLUMN_NAME_FECHA, DbHelper.dateToString(fecha))
            put(EnviableContract.EnviableEntry.COLUMN_NAME_DIRECCION, direccion.toInt())
            put(EnviableContract.EnviableEntry.COLUMN_NAME_MENS_ID, mensId)
        }

        val envId = db?.insert(EnviableContract.EnviableEntry.TABLE_NAME, null, values)?.toInt()!!

        añadir_enviable(mens, envId, id_usuario, context)
    }

    private fun añadir_enviable(enviable: Enviable, envId: Int, id_usuario: String, context: Context) {
        listaEnviables.add(enviable)
        mostrar_en_pantalla()

        val dbHelper = DbHelper(context)
        val db = dbHelper.writableDatabase

        val projection = arrayOf(UsuarioContract.UsuarioEntry.COLUMN_NAME_CHAT_ID)

        val selection = "${UsuarioContract.UsuarioEntry.COLUMN_NAME_ID} = ?"
        val selectionArgs = arrayOf(id_usuario)
        val cursor = db.query(
            UsuarioContract.UsuarioEntry.TABLE_NAME,
            projection,
            selection,
            selectionArgs,
            null,
            null,
            null
        )

        val chatId: Int;
        with(cursor) {
            moveToNext()
            chatId = getInt(getColumnIndexOrThrow(com.netless.database.UsuarioContract.UsuarioEntry.COLUMN_NAME_CHAT_ID))
        }
        cursor.close()

        val values = ContentValues().apply {
            put(EnviablesChatContract.EnviablesChatEntry.COLUMN_NAME_CHAT_ID, chatId)
            put(EnviablesChatContract.EnviablesChatEntry.COLUMN_NAME_ENV_ID, envId)
        }

        val enviableChatId = db?.insert(EnviablesChatContract.EnviablesChatEntry.TABLE_NAME, null, values)
    }

    fun mostrar_en_pantalla() {
        for (enviable in listaEnviables) {
            enviable.mostrar_en_pantalla()
        }
    }
}