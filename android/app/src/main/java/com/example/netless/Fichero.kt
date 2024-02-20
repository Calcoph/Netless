package com.example.netless

class Fichero(nombre: String, tamaño: Int, dirección: Dirección) : Enviable(dirección) {
    val nombre = nombre
    val tamaño = tamaño

    fun get_nombre(): String {
        return nombre
    }
}