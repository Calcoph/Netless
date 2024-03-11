package com.netless.main

import android.content.Context
import java.io.File

class Usuario(nombre: String, ip: String, id: String) {
    val nombre = nombre
    val ip = ip
    val chat = HistorialChat()
    val id = id

    fun obtener_confirmacion(nombre: String, tamaño: Long) {

    }

    fun enviar_fichero(fichero: File, context: Context) {
        val nombre = fichero.name
        val tamaño = fichero.totalSpace
        val fichero = Fichero(nombre, tamaño, Dirección.Saliente)
        chat.añadir_fichero(fichero, id, context)
    }

    fun enviar_mensaje(msg: String, context: Context) {
        val mens = Mensaje(msg, Dirección.Saliente)
        chat.añadir_mensaje(mens, id, context)
    }

    fun obtener_nombre(): String {
        return nombre
    }

    fun obtener_chat(): HistorialChat {
        return chat
    }

    fun obtener_id(): String {
        return id
    }

    fun acepta_conexiones(): Boolean {
        println("!!!!! acepta_conexiones() siempre devuelve true TODO")
        return true
    }

    fun solicitar_conexion(): Boolean {
        println("!!!!! solicitar_conexion() siempre devuelve true TODO")
        return true
    }
}