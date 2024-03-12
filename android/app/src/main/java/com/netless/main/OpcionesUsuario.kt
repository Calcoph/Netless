package com.netless.main

class OpcionesUsuario {
    companion object {
        // Singleton pattern
        @Volatile
        private var opciones: OpcionesUsuario? = null

        fun get_opciones() =
            opciones ?: synchronized(this) {
                opciones ?: OpcionesUsuario().also { opciones = it }
            }

        fun generar_id_aleatorio(): String {
            // TODO: No es aleatorio
            return "93507297509234"
        }
    }

    var alias = String()
    var id = String()

    fun cambiar_alias(nuevo_alias: String) {
        alias = nuevo_alias
    }

    fun cambiar_id(nuevo_id: String) {
        id = nuevo_id
    }
}