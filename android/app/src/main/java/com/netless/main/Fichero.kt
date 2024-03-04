package com.netless.main

class Fichero(nombre: String, tamaño: Long, dirección: Dirección) : Enviable(dirección) {
    val nombre = nombre
    val tamaño = tamaño

    fun get_nombre(): String {
        return nombre
    }
}