package com.netless.main

import java.util.ArrayList

class ListaUsuarios private constructor() {
    companion object {
        // Singleton pattern
        @Volatile
        private var lista: ListaUsuarios? = null

        fun getLista() =
            lista ?: synchronized(this) {
                lista ?: ListaUsuarios().also { lista = it }
            }
    }

    private val usuarios = ArrayList<Usuario>()

    fun anadirUsuario(usr: Usuario) {
        usuarios.add(usr)
    }

    fun quitarUsuario(id: String) {
        usuarios.removeIf { it.obtenerId() == id }
    }

    fun obtenerUsuario(id: String): Usuario? {
        for (usuario in usuarios) {
            if (usuario.obtenerId() == id) {
                return usuario
            }
        }

        return null
    }
}