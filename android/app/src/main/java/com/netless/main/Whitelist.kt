package com.example.netless

class Whitelist {
    companion object {
        // Singleton pattern
        @Volatile
        private var lista: Whitelist? = null

        fun get_whitelist() =
            lista ?: synchronized(this) {
                lista ?: Whitelist().also { lista = it }
            }
    }

    val listaIds = ArrayList<String>()

    fun añadir_usuario(id: String) {
        listaIds.add(id)
        "SELECT from Usuario WHERE usr_id = ${id}"
        "INSERT into Whitelist(usr_id, id, alias, chat_id) VALUES (${usr_id}, ${id}, ${alias}, ${chat_id})"
    }

    fun quitar_usuario(id: String) {
        listaIds.remove(id)

        "DELETE FROM Whitelist WHERE usr_id = ${id}"
    }

    fun usuario_aceptado(id: String): Boolean {
        return listaIds.contains(id)
    }
}