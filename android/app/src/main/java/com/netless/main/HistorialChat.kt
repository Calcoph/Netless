package com.netless.main

import android.content.ContentValues
import android.content.Context
import com.netless.database.EnviableContract
import com.netless.database.EnviablesChatContract
import com.netless.database.FicheroContract
import com.netless.database.MensajeContract
import com.netless.database.UsuarioContract

class HistorialChat {
    private val listaEnviables = ArrayList<Enviable>()

    fun anadirFichero(fichero: Fichero, idUsuario: String, context: Context) {
        val nombre = fichero.getNombre()
        val fecha = fichero.getFecha()
        val direccion = fichero.getDireccion()

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

        anadirEnviable(fichero, envId, idUsuario, context)
    }

    fun anadirMensaje(mens: Mensaje, idUsuario: String, context: Context) {
        val msg = mens.getMsg()
        val fecha = mens.getFecha()
        val direccion = mens.getDireccion()

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

        anadirEnviable(mens, envId, idUsuario, context)
    }

    private fun anadirEnviable(enviable: Enviable, envId: Int, idUsuario: String, context: Context) {
        listaEnviables.add(enviable)
        mostrarEnPantalla()

        val dbHelper = DbHelper(context)
        val db = dbHelper.writableDatabase

        val projection = arrayOf(UsuarioContract.UsuarioEntry.COLUMN_NAME_CHAT_ID)

        val selection = "${UsuarioContract.UsuarioEntry.COLUMN_NAME_ID} = ?"
        val selectionArgs = arrayOf(idUsuario)
        val cursor = db.query(
            UsuarioContract.UsuarioEntry.TABLE_NAME,
            projection,
            selection,
            selectionArgs,
            null,
            null,
            null
        )

        val chatId: Int
        with(cursor) {
            moveToNext()
            chatId = getInt(getColumnIndexOrThrow(UsuarioContract.UsuarioEntry.COLUMN_NAME_CHAT_ID))
        }
        cursor.close()

        val values = ContentValues().apply {
            put(EnviablesChatContract.EnviablesChatEntry.COLUMN_NAME_CHAT_ID, chatId)
            put(EnviablesChatContract.EnviablesChatEntry.COLUMN_NAME_ENV_ID, envId)
        }

        val enviableChatId = db?.insert(EnviablesChatContract.EnviablesChatEntry.TABLE_NAME, null, values)
    }

    fun mostrarEnPantalla() {
        for (enviable in listaEnviables) {
            enviable.mostrarEnPantalla()
        }
    }
}