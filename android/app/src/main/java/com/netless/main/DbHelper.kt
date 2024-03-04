package com.example.netless

import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper

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
    }
}