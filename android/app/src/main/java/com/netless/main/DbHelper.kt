package com.netless.main

import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import com.netless.database.ChatContract
import com.netless.database.EnviableContract
import com.netless.database.EnviablesChatContract
import com.netless.database.FicheroContract
import com.netless.database.MensajeContract
import com.netless.database.OpcionesContract
import com.netless.database.UsuarioContract
import com.netless.database.WhitelistContract
import java.text.SimpleDateFormat
import java.util.Date

class DbHelper(context: Context) : SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {
    override fun onCreate(db: SQLiteDatabase) {
        //! El orden de los SQL_CREATE_ENTRIES es importante!
        db.execSQL(MensajeContract.SQL_CREATE_ENTRIES)
        db.execSQL(FicheroContract.SQL_CREATE_ENTRIES)
        db.execSQL(EnviableContract.SQL_CREATE_ENTRIES)
        db.execSQL(ChatContract.SQL_CREATE_ENTRIES)
        db.execSQL(EnviablesChatContract.SQL_CREATE_ENTRIES)
        db.execSQL(UsuarioContract.SQL_CREATE_ENTRIES)
        db.execSQL(WhitelistContract.SQL_CREATE_ENTRIES)
        db.execSQL(OpcionesContract.SQL_CREATE_ENTRIES)

        val cur = db.rawQuery("SELECT * FROM ${OpcionesContract.OpcionesEntry.TABLE_NAME}", arrayOf())
        if (!cur.moveToNext()) {
            // No hay opciones
            // Hay que inicializar la tabla
            val id = OpcionesUsuario.generar_id_aleatorio()
            val aliasPorDefecto = "(Sin alias)"
            db.execSQL("INSERT INTO ${OpcionesContract.OpcionesEntry.TABLE_NAME}(${OpcionesContract.OpcionesEntry.COLUMN_NAME_ID}, ${OpcionesContract.OpcionesEntry.COLUMN_NAME_ALIAS}) VALUES (${id}, ${aliasPorDefecto})");
        }
        cur.close()
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        //! El orden de los SQL_DELETE_ENTRIES es importante!
        db.execSQL(OpcionesContract.SQL_DELETE_ENTRIES)
        db.execSQL(WhitelistContract.SQL_DELETE_ENTRIES)
        db.execSQL(UsuarioContract.SQL_DELETE_ENTRIES)
        db.execSQL(EnviablesChatContract.SQL_DELETE_ENTRIES)
        db.execSQL(ChatContract.SQL_DELETE_ENTRIES)
        db.execSQL(EnviableContract.SQL_DELETE_ENTRIES)
        db.execSQL(FicheroContract.SQL_DELETE_ENTRIES)
        db.execSQL(MensajeContract.SQL_DELETE_ENTRIES)
    }

    companion object {
        const val DATABASE_VERSION = 1
        const val DATABASE_NAME = "NetLess.db"

        fun dateToString(date: Date): String {
            return SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS").format(date).toString()
        }
    }
}