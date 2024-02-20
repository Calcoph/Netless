package com.example.netless

import java.io.File

class Usuario(nombre: String, ip: String, id: String) {
    val nombre = nombre
    val ip = ip
    val chat = HistorialChat()
    val id = id

    fun obtener_confirmacion() {

    }

    fun enviar_fichero(fichero: File) {

    }

    fun enviar_mensaje(msg: String) {

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
}