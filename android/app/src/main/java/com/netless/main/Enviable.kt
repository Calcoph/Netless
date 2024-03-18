package com.netless.main

import java.util.Date

open class Enviable(private val direccion: Direccion) {
    private val fecha = Date()

    fun mostrarEnPantalla() {

    }

    fun getFecha(): Date {
        return fecha
    }

    fun getDireccion(): Direccion {
        return direccion
    }
}