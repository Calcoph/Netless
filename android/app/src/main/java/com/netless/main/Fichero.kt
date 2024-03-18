package com.netless.main

class Fichero(private val nombre: String, private val tamano: Long, direccion: Direccion) : Enviable(direccion) {
    fun getNombre(): String {
        return nombre
    }
}