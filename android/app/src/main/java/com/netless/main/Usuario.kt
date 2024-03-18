package com.netless.main

import android.content.Context
import java.io.File

class Usuario(private val nombre: String, private val ip: String, private val id: String) {
    private val chat = HistorialChat()

    fun obtenerConfirmacion(nombre: String, tamano: Long) {

    }

    fun enviarFichero(fichero: File, context: Context) {
        val nombre = fichero.name
        val tamano = fichero.totalSpace
        val fichero = Fichero(nombre, tamano, Direccion.Saliente)
        chat.anadirFichero(fichero, id, context)
    }

    fun enviarMensaje(msg: String, context: Context) {
        val mens = Mensaje(msg, Direccion.Saliente)
        chat.anadirMensaje(mens, id, context)
    }

    fun obtenerNombre(): String {
        return nombre
    }

    fun obtenerChat(): HistorialChat {
        return chat
    }

    fun obtenerId(): String {
        return id
    }

    fun aceptaConexiones(): Boolean {
        println("!!!!! acepta_conexiones() siempre devuelve true TODO")
        return true
    }

    fun solicitarConexion(): Boolean {
        println("!!!!! solicitar_conexion() siempre devuelve true TODO")
        return true
    }
}