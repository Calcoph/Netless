package com.netless.main

import java.util.Date

open class Enviable(dirección: Dirección) {
    val fecha = Date()
    val dirección = dirección

    fun mostrar_en_pantalla() {

    }

    fun get_fecha(): Date {
        return fecha
    }

    fun get_direccion(): Dirección {
        return dirección
    }
}