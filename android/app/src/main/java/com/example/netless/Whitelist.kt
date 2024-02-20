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
    }

    fun quitar_usuario(id: String) {
        listaIds.remove(id)
    }

    fun usuario_aceptado(id: String): Boolean {
        return listaIds.contains(id)
    }
}