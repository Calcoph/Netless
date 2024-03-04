package com.netless.main

import java.util.ArrayList

class ListaUsuarios private constructor() {
    companion object {
        // Singleton pattern
        @Volatile
        private var lista: ListaUsuarios? = null

        fun get_lista() =
            lista ?: synchronized(this) {
                lista ?: ListaUsuarios().also { lista = it }
            }
    }

    val usuarios = ArrayList<Usuario>()

    fun añadir_usuario(usr: Usuario) {
        usuarios.add(usr)
    }

    fun quitar_usuario(id: String) {
        usuarios.removeIf { it.id == id }
    }

    fun obtener_usuario(id: String): Usuario? {
        for (usuario in usuarios) {
            if (usuario.id == id) {
                return usuario
            }
        }

        return null
    }
}